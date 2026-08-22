#!/usr/bin/env python3
"""Single supported execution endpoint for an explicitly authorized Experiment 0 Pilot."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import os
import shlex
import stat
from pathlib import Path
from typing import Any

from preflight_pilot import (
    PILOT_OUTPUT_DESTINATION,
    PreflightError,
    ensure_clean_worktree,
    run_git,
    sha256_bytes,
    validate_human_approval,
    validate_manifest,
)
from run_adapter import AdapterError, bounded_run


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    parent = path.parent
    if parent.is_symlink():
        raise PreflightError(f"Pilot output parent must not be a symlink: {parent}")
    parent.mkdir(parents=True, exist_ok=True)
    resolved_parent = parent.resolve()
    if resolved_parent != parent:
        raise PreflightError(f"Pilot output parent resolved unexpectedly: {parent}")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
        except Exception:
            try:
                os.close(fd)
            except OSError:
                pass
            raise
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def read_regular_file_once(path: Path, *, label: str) -> bytes:
    if path.is_symlink():
        raise PreflightError(f"{label} must not be a symlink")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise PreflightError(f"cannot open {label}: {exc}") from exc
    try:
        metadata = os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode):
            raise PreflightError(f"{label} must be a regular file")
        with os.fdopen(fd, "rb", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(fd)


def parse_json_object(payload: bytes, *, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PreflightError(f"invalid JSON in {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise PreflightError(f"{label} must contain a JSON object")
    return value


def ensure_output_root(root: Path) -> Path:
    lexical = root.parent / PILOT_OUTPUT_DESTINATION
    if lexical.exists() and lexical.is_symlink():
        raise PreflightError("Pilot output root must not be a symlink")
    lexical.mkdir(mode=0o700, exist_ok=True)
    if lexical.is_symlink():
        raise PreflightError("Pilot output root became a symlink")
    resolved = lexical.resolve()
    if resolved == root or root in resolved.parents:
        raise PreflightError("Pilot output root resolves inside the Git repository")
    if resolved != lexical:
        raise PreflightError("Pilot output root must resolve to its dedicated sibling path")
    return resolved


def reserve_attempt(output_root: Path, package_hash: str, max_runs: int) -> tuple[int, Path]:
    package_root = output_root / package_hash
    if package_root.exists() and package_root.is_symlink():
        raise PreflightError("Pilot package root must not be a symlink")
    package_root.mkdir(mode=0o700, exist_ok=True)
    if package_root.is_symlink() or package_root.resolve() != package_root:
        raise PreflightError("Pilot package root must remain a real directory")
    for attempt in range(1, max_runs + 1):
        attempt_dir = package_root / f"attempt-{attempt:03d}"
        try:
            attempt_dir.mkdir(mode=0o700)
        except FileExistsError:
            if attempt_dir.is_symlink():
                raise PreflightError("Pilot attempt path must not be a symlink")
            continue
        if attempt_dir.is_symlink() or attempt_dir.resolve() != attempt_dir:
            raise PreflightError("Pilot attempt directory must remain a real directory")
        return attempt, attempt_dir
    raise PreflightError(f"Pilot max_runs exhausted: {max_runs} attempt(s) already reserved")


def safe_adapter_cwd(root: Path, relative: str) -> Path:
    lexical = root / relative
    if lexical.is_symlink():
        raise PreflightError("adapter_cwd must not be a symlink")
    candidate = lexical.resolve()
    if candidate != root and root not in candidate.parents:
        raise PreflightError("adapter_cwd resolves outside repository")
    if not candidate.is_dir():
        raise PreflightError(f"adapter_cwd is not a directory: {relative}")
    return candidate


def build_child_env(allowlist: list[str]) -> dict[str, str]:
    env: dict[str, str] = {}
    if "PATH" in os.environ:
        env["PATH"] = os.environ["PATH"]
    for name in allowlist:
        if name in os.environ:
            env[name] = os.environ[name]
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    request_path = args.request if args.request.is_absolute() else root / args.request

    attempt_dir: Path | None = None
    try:
        manifest_bytes = read_regular_file_once(manifest_path, label="Pilot manifest")
        manifest = parse_json_object(manifest_bytes, label="Pilot manifest")
        manifest_sha = sha256_bytes(manifest_bytes)

        validate_manifest(
            manifest,
            root,
            manifest_path=manifest_path,
            manifest_sha256=manifest_sha,
            check_git=True,
            check_authority_state=True,
        )
        validate_human_approval(root)
        ensure_clean_worktree(root)
        runtime_head = run_git(root, "rev-parse", "HEAD")
        runtime_tree = run_git(root, "rev-parse", "HEAD^{tree}")

        request_bytes = read_regular_file_once(request_path, label="Pilot request")
        expected_request_hash = manifest.get("request_sha256")
        if not isinstance(expected_request_hash, str) or sha256_bytes(request_bytes) != expected_request_hash:
            raise PreflightError("request bytes SHA-256 do not match authorized Pilot manifest")
        parse_json_object(request_bytes, label="Pilot request")

        limits = manifest["limits"]
        max_runs = limits["max_runs"]
        output_root = ensure_output_root(root)
        attempt_number, attempt_dir = reserve_attempt(output_root, manifest_sha, max_runs)

        atomic_write_bytes(attempt_dir / "manifest.json", manifest_bytes)
        atomic_write_bytes(attempt_dir / "request.json", request_bytes)
        atomic_write_json(
            attempt_dir / "reservation.json",
            {
                "package_sha256": manifest_sha,
                "authorization_base_commit": manifest["authorization_base_commit"],
                "authorization_base_tree": manifest["authorization_base_tree"],
                "runtime_head_commit": runtime_head,
                "runtime_tree": runtime_tree,
                "attempt": attempt_number,
                "max_runs": max_runs,
                "status": "RESERVED",
                "label": "PILOT — NOT EVIDENCE",
            },
        )

        cwd = safe_adapter_cwd(root, manifest["adapter_cwd"])
        env = build_child_env(manifest["environment_allowlist"])
        ensure_clean_worktree(root)
        returncode, stdout, stderr, elapsed_ms = bounded_run(
            shlex.split(manifest["adapter_command"]),
            request_text=request_bytes.decode("utf-8"),
            cwd=cwd,
            env=env,
            timeout_seconds=limits["timeout_seconds"],
            max_output_bytes=limits["max_output_bytes"],
        )
        if returncode != 0:
            raise AdapterError(f"adapter failed ({returncode}): {stderr.strip()}")
        try:
            response = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise AdapterError(f"adapter stdout is not JSON: {exc}") from exc

        metrics = {
            "latency_ms": {"provenance": "MEASURED", "value": elapsed_ms, "unit": "ms"},
            "model_calls": {"provenance": "MEASURED", "value": 1, "unit": "calls"},
            "tool_calls": {"provenance": "UNAVAILABLE", "value": None, "unit": "calls"},
            "input_tokens": {"provenance": "UNAVAILABLE", "value": None, "unit": "tokens"},
            "output_tokens": {"provenance": "UNAVAILABLE", "value": None, "unit": "tokens"},
            "cost": {"provenance": "UNAVAILABLE", "value": None, "unit": None},
            "execution_limits": {
                "timeout_seconds": limits["timeout_seconds"],
                "max_output_bytes": limits["max_output_bytes"],
                "max_runs": max_runs,
                "adapter_cwd": manifest["adapter_cwd"],
                "environment_allowlist": manifest["environment_allowlist"],
                "sandbox": False,
            },
        }
        response_payload = (json.dumps(response, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        metrics_payload = (json.dumps(metrics, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        atomic_write_bytes(attempt_dir / "response.json", response_payload)
        atomic_write_bytes(attempt_dir / "metrics.json", metrics_payload)
        atomic_write_json(
            attempt_dir / "result.json",
            {
                "status": "COMPLETED",
                "label": "PILOT — NOT EVIDENCE",
                "package_sha256": manifest_sha,
                "authorization_base_commit": manifest["authorization_base_commit"],
                "authorization_base_tree": manifest["authorization_base_tree"],
                "runtime_head_commit": runtime_head,
                "runtime_tree": runtime_tree,
                "attempt": attempt_number,
                "request_sha256": sha256_bytes(request_bytes),
                "response_sha256": sha256_bytes(response_payload),
                "metrics_sha256": sha256_bytes(metrics_payload),
            },
        )
        print(f"PILOT_EXECUTION_COMPLETED: {attempt_dir}")
        return 0
    except (PreflightError, AdapterError, OSError) as exc:
        if attempt_dir is not None:
            try:
                atomic_write_json(attempt_dir / "result.json", {"status": "FAILED", "label": "PILOT — NOT EVIDENCE", "error": str(exc)})
            except OSError:
                pass
        print(f"PILOT_EXECUTION_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
