#!/usr/bin/env python3
"""Single supported execution endpoint for an explicitly authorized Experiment 0 Pilot.

The command validates canonical authorization, the exact Pilot manifest, human approval,
Git head/tree/worktree, and the request hash immediately before reserving one bounded
attempt and spawning the internal adapter primitive. Pilot artifacts are written only to
a dedicated sibling directory outside the Git repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import sys
from pathlib import Path
from typing import Any

from preflight_pilot import PILOT_OUTPUT_DESTINATION, PreflightError, load_json, sha256_file, validate_human_approval, validate_manifest
from run_adapter import AdapterError, bounded_run


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def manifest_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reserve_attempt(package_root: Path, max_runs: int) -> tuple[int, Path]:
    package_root.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, max_runs + 1):
        attempt_dir = package_root / f"attempt-{attempt:03d}"
        try:
            attempt_dir.mkdir()
        except FileExistsError:
            continue
        return attempt, attempt_dir
    raise PreflightError(f"Pilot max_runs exhausted: {max_runs} attempt(s) already reserved")


def safe_adapter_cwd(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
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
        manifest = load_json(manifest_path)

        # Authority and drift are checked immediately before any attempt is reserved.
        validate_manifest(manifest, root, check_git=True, check_authority_state=True)
        validate_human_approval(root)

        expected_request_hash = manifest.get("request_sha256")
        if not isinstance(expected_request_hash, str) or len(expected_request_hash) != 64:
            raise PreflightError("request_sha256 must be present in the Pilot manifest")
        if not request_path.is_file() or sha256_file(request_path) != expected_request_hash:
            raise PreflightError("request file SHA-256 does not match authorized Pilot manifest")
        request = load_json(request_path)

        limits = manifest["limits"]
        max_runs = limits["max_runs"]
        output_root = root.parent / PILOT_OUTPUT_DESTINATION
        if output_root == root or root in output_root.parents:
            raise PreflightError("Pilot output root must be outside the Git repository")

        package_hash = manifest_digest(manifest_path)
        package_root = output_root / package_hash
        attempt_number, attempt_dir = reserve_attempt(package_root, max_runs)

        atomic_write_json(attempt_dir / "manifest.json", manifest)
        atomic_write_json(attempt_dir / "request.json", request)
        atomic_write_json(
            attempt_dir / "reservation.json",
            {
                "package_sha256": package_hash,
                "attempt": attempt_number,
                "max_runs": max_runs,
                "status": "RESERVED",
                "label": "PILOT — NOT EVIDENCE",
            },
        )

        cwd = safe_adapter_cwd(root, manifest["adapter_cwd"])
        env = build_child_env(manifest["environment_allowlist"])
        returncode, stdout, stderr, elapsed_ms = bounded_run(
            shlex.split(manifest["adapter_command"]),
            request_text=json.dumps(request, ensure_ascii=False),
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
        atomic_write_json(attempt_dir / "response.json", response)
        atomic_write_json(attempt_dir / "metrics.json", metrics)
        atomic_write_json(
            attempt_dir / "result.json",
            {
                "status": "COMPLETED",
                "label": "PILOT — NOT EVIDENCE",
                "package_sha256": package_hash,
                "attempt": attempt_number,
                "request_sha256": sha256_file(attempt_dir / "request.json"),
                "response_sha256": sha256_file(attempt_dir / "response.json"),
                "metrics_sha256": sha256_file(attempt_dir / "metrics.json"),
            },
        )
        print(f"PILOT_EXECUTION_COMPLETED: {attempt_dir}")
        return 0
    except (PreflightError, AdapterError) as exc:
        if attempt_dir is not None:
            try:
                atomic_write_json(
                    attempt_dir / "result.json",
                    {"status": "FAILED", "label": "PILOT — NOT EVIDENCE", "error": str(exc)},
                )
            except OSError:
                pass
        print(f"PILOT_EXECUTION_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
