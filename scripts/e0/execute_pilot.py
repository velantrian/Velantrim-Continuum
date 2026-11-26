#!/usr/bin/env python3
"""Single supported execution endpoint for an explicitly authorized Experiment 0 Pilot."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
import shlex
import signal
import stat
from pathlib import Path
from typing import Any

from preflight_pilot import (
    PILOT_OUTPUT_DESTINATION,
    PreflightError,
    ensure_clean_worktree,
    sha256_bytes,
    validate_canonical_authorization,
    validate_human_approval,
    validate_manifest,
)
from run_adapter import AdapterError, AdapterOutputLimitError, AdapterTimeoutError, bounded_run
from classify_attempts import classify_package, unknown_outcome_attempts


class PilotUnknownOutcome(AdapterError):
    """Request may have been processed without a usable response (never retried)."""


class PilotDefiniteFailure(AdapterError):
    """The trusted adapter reported an error before the external request."""


class PilotInterrupted(BaseException):
    """SIGINT/SIGTERM received; BaseException so it is never mistaken for a definite error."""


# Adapter exit codes that prove a definite outcome. 0 = response; 2 = proven
# pre-send failure (CAPTURE_ADAPTER_ERROR: request was not sent).
# Every other code (4 UNKNOWN_OUTCOME, 3 unexpected exception, 1 uncaught crash,
# negative = killed by signal) cannot prove the provider call did not happen and is
# preserved conservatively as UNKNOWN_OUTCOME.
DEFINITE_FAILURE_EXIT_CODES = frozenset({2})
TERMINAL_SEAL_PROTOCOL = "terminal-seal-v1"


def _raise_interrupted(signum: int, _frame: Any) -> None:
    raise PilotInterrupted(f"received signal {signum}")


def _fsync_directory(path: Path) -> None:
    """Persist directory entries after mkdir/rename, or fail before Pilot spawn.

    POSIX flock is already required for the Pilot journal. Do not silently
    downgrade durability guarantees on an unsupported platform/filesystem.
    """
    if os.name != "posix":
        raise PreflightError("durable Pilot journal directory fsync requires POSIX")
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    directory_fd = os.open(path, flags)
    try:
        if not stat.S_ISDIR(os.fstat(directory_fd).st_mode):
            raise PreflightError(f"Pilot journal parent must be a directory: {path}")
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    parent = path.parent
    if parent.is_symlink():
        raise PreflightError(f"Pilot output parent must not be a symlink: {parent}")
    # Journal directories must be created and fsynced explicitly before
    # invoking this writer; implicit mkdir would leave unflushed parents.
    if not parent.is_dir():
        raise PreflightError(f"Pilot output parent is not a directory: {parent}")
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
        # Persist the renamed journal entry as well as the file contents.
        _fsync_directory(parent)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def atomic_write_json(path: Path, value: Any) -> None:
    atomic_write_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def write_terminal_result(attempt_dir: Path, payload: dict[str, Any]) -> None:
    """Only a separately fsynced matching seal makes a terminal status durable.

    A renamed result.json can be visible when its directory fsync failed.
    Without the seal, its classification remains UNKNOWN_OUTCOME.
    """
    status = payload.get("status")
    if status not in {"COMPLETED", "FAILED"}:
        raise ValueError("terminal seal requires COMPLETED or FAILED")
    result_bytes = (json.dumps({"label": "PILOT — NOT EVIDENCE", **payload},
                               ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomic_write_bytes(attempt_dir / "result.json", result_bytes)
    atomic_write_json(attempt_dir / "terminal-seal.json", {
        "protocol": TERMINAL_SEAL_PROTOCOL,
        "status": status,
        "attempt": payload["attempt"],
        "package_sha256": payload["package_sha256"],
        "result_sha256": sha256_bytes(result_bytes),
    })


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
    try:
        lexical.mkdir(mode=0o700)
    except FileExistsError:
        pass
    if lexical.is_symlink():
        raise PreflightError("Pilot output root became a symlink")
    resolved = lexical.resolve()
    if resolved == root or root in resolved.parents:
        raise PreflightError("Pilot output root resolves inside the Git repository")
    if resolved != lexical:
        raise PreflightError("Pilot output root must resolve to its dedicated sibling path")
    # Check even on reopen: a prior mkdir may have succeeded but fsync failed.
    _fsync_directory(lexical.parent)
    return resolved


@contextmanager
def package_reservation_lock(package_root: Path):
    """Serialize check+reservation across POSIX processes sharing this directory.

    The lock file remains on disk: unlinking it could let two processes lock
    different inodes. Unsupported platforms fail closed rather than race.
    """
    if os.name != "posix":
        raise PreflightError("interprocess Pilot reservation lock requires POSIX flock")
    import fcntl

    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    lock_path = package_root / ".reservation.lock"
    try:
        fd = os.open(lock_path, flags, 0o600)
    except OSError as exc:
        raise PreflightError(f"cannot open Pilot reservation lock: {exc}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise PreflightError("Pilot reservation lock must be a regular file")
        # Persist the lock directory entry before it coordinates a slot.
        _fsync_directory(package_root)
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _read_reservation_for_gate(attempt_dir: Path) -> dict[str, Any] | None:
    """Fail-closed read for the bounded reserve gate, inside package flock."""
    path = attempt_dir / "reservation.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def reserve_attempt(
    output_root: Path,
    package_hash: str,
    max_runs: int,
    *,
    reservation_metadata: dict[str, Any] | None = None,
) -> tuple[int, Path]:
    package_root = output_root / package_hash
    if package_root.exists() and package_root.is_symlink():
        raise PreflightError("Pilot package root must not be a symlink")
    try:
        package_root.mkdir(mode=0o700)
    except FileExistsError:
        pass
    if package_root.is_symlink() or package_root.resolve() != package_root:
        raise PreflightError("Pilot package root must remain a real directory")
    # Rechecking existing directories is required after failed fsync.
    _fsync_directory(output_root)
    with package_reservation_lock(package_root):
        # The journal check and the durable blocking reservation form one
        # interprocess critical section. No adapter may start before it ends.
        unknown = unknown_outcome_attempts(package_root)
        if unknown:
            names = ", ".join(Path(e["attempt_dir"]).name for e in unknown)
            raise PreflightError(
                f"Pilot refuses a new attempt: unresolved UNKNOWN_OUTCOME in {names}; "
                "the provider may have processed it, an owner must resolve it out of band")
        # A matching terminal-seal file proves byte consistency but NOT that
        # fsync of its directory succeeded. If that fsync raised, the caller
        # returned 4 even though the seal remains visible. Another process
        # cannot distinguish that case from a fully synced seal by reading
        # the journal. For v1, any terminal result consumes the package's
        # automatic continuation right. Owner must independently resolve it.
        terminal = [
            e for e in classify_package(package_root)
            if e["outcome"] in {"COMPLETED", "FAILED"}
            and (reservation := _read_reservation_for_gate(Path(e["attempt_dir"])))
            and reservation.get("journal_protocol") == TERMINAL_SEAL_PROTOCOL
        ]
        if terminal:
            names = ", ".join(Path(e["attempt_dir"]).name for e in terminal)
            raise PreflightError(
                f"Pilot refuses a new attempt: terminal result in {names} "
                "requires separate owner review; visible seal cannot prove fsync success")
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
            # Persist the newly allocated attempt directory before its
            # reservation.json is fsynced and before releasing the lock.
            _fsync_directory(package_root)
            reservation = {
                **(reservation_metadata or {}),
                "package_sha256": package_hash,
                "attempt": attempt,
                "max_runs": max_runs,
                "status": "RESERVED",
                "journal_protocol": TERMINAL_SEAL_PROTOCOL,
                "label": "PILOT — NOT EVIDENCE",
            }
            # A failed write spends this slot; the adapter is never started.
            # A persisted reservation without result.json blocks all later slots.
            atomic_write_json(attempt_dir / "reservation.json", reservation)
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
    binding: dict[str, Any] = {}
    adapter_started = False
    previous_sigterm = signal.signal(signal.SIGTERM, _raise_interrupted)
    try:
        ensure_clean_worktree(root)
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
        authorization = validate_canonical_authorization(
            root,
            manifest=manifest,
            manifest_path=manifest_path,
            manifest_sha256=manifest_sha,
        )
        provenance = authorization["_verified_activation"]

        validate_human_approval(root)
        ensure_clean_worktree(root)

        request_bytes = read_regular_file_once(request_path, label="Pilot request")
        expected_request_hash = manifest.get("request_sha256")
        if not isinstance(expected_request_hash, str) or sha256_bytes(request_bytes) != expected_request_hash:
            raise PreflightError("request bytes SHA-256 do not match authorized Pilot manifest")
        parse_json_object(request_bytes, label="Pilot request")

        limits = manifest["limits"]
        max_runs = limits["max_runs"]
        ensure_clean_worktree(root)
        output_root = ensure_output_root(root)
        attempt_number, attempt_dir = reserve_attempt(
            output_root, manifest_sha, max_runs,
            reservation_metadata={
                "authorization_base_commit": provenance["authorization_base_commit"],
                "authorization_base_tree": provenance["authorization_base_tree"],
                "activation_head_commit": provenance["activation_head_commit"],
                "activation_tree": provenance["activation_tree"],
            },
        )
        binding = {
            "package_sha256": manifest_sha,
            "attempt": attempt_number,
            "request_sha256": sha256_bytes(request_bytes),
        }

        atomic_write_bytes(attempt_dir / "manifest.json", manifest_bytes)
        atomic_write_bytes(attempt_dir / "request.json", request_bytes)
        # reservation.json was durably written under the lock before
        # any manifest/request copy or child process can run.
        cwd = safe_adapter_cwd(root, manifest["adapter_cwd"])
        env = build_child_env(manifest["environment_allowlist"])
        ensure_clean_worktree(root)
        adapter_started = True
        returncode, stdout, stderr, elapsed_ms = bounded_run(
            shlex.split(manifest["adapter_command"]),
            request_text=request_bytes.decode("utf-8"),
            cwd=cwd,
            env=env,
            timeout_seconds=limits["timeout_seconds"],
            max_output_bytes=limits["max_output_bytes"],
        )
        if returncode != 0:
            stderr_text_utf8 = stderr.encode("utf-8", errors="replace")
            detail = (
                f"adapter exited with return code {returncode}; "
                f"stderr_text_utf8_sha256={hashlib.sha256(stderr_text_utf8).hexdigest()}; "
                f"stderr_text_utf8_bytes={len(stderr_text_utf8)}"
            )
            if returncode not in DEFINITE_FAILURE_EXIT_CODES:
                raise PilotUnknownOutcome(detail, returncode)
            raise PilotDefiniteFailure(detail)
        try:
            response = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise PilotUnknownOutcome(f"adapter stdout is not JSON: {exc}") from exc
        if not isinstance(response, dict):
            raise PilotUnknownOutcome("adapter stdout must contain exactly one JSON object")

        metrics = {
            "latency_ms": {"provenance": "MEASURED", "value": elapsed_ms, "unit": "ms"},
            "model_calls": {"provenance": "UNAVAILABLE", "value": None, "unit": "calls"},
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
        write_terminal_result(
            attempt_dir,
            {
                "status": "COMPLETED",
                "label": "PILOT — NOT EVIDENCE",
                "package_sha256": manifest_sha,
                "authorization_base_commit": provenance["authorization_base_commit"],
                "authorization_base_tree": provenance["authorization_base_tree"],
                "activation_head_commit": provenance["activation_head_commit"],
                "activation_tree": provenance["activation_tree"],
                "attempt": attempt_number,
                "request_sha256": sha256_bytes(request_bytes),
                "response_sha256": sha256_bytes(response_payload),
                "metrics_sha256": sha256_bytes(metrics_payload),
            },
        )
        print(f"PILOT_EXECUTION_COMPLETED: {attempt_dir}")
        return 0
    except (PilotUnknownOutcome, AdapterTimeoutError, AdapterOutputLimitError) as exc:
        exit_code = exc.args[1] if isinstance(exc, PilotUnknownOutcome) and len(exc.args) > 1 else None
        return _unknown_outcome(attempt_dir, binding, str(exc.args[0]), exit_code)
    except (KeyboardInterrupt, PilotInterrupted) as exc:
        reason = f"interrupted ({type(exc).__name__}: {exc})"
        if adapter_started:
            return _unknown_outcome(attempt_dir, binding, reason, None)
        persisted = _write_result(attempt_dir, {"status": "FAILED", **binding, "error": reason + " before adapter start"})
        if attempt_dir is not None and not persisted:
            return _unknown_outcome(attempt_dir, binding, "definite failure could not be durably sealed", None)
        print(f"PILOT_EXECUTION_ERROR: {reason} before adapter start", file=sys.stderr)
        return 1
    except PilotDefiniteFailure as exc:
        if not _write_result(attempt_dir, {"status": "FAILED", **binding, "error": str(exc)}):
            return _unknown_outcome(attempt_dir, binding, "definite failure could not be durably sealed", None)
        print(f"PILOT_EXECUTION_ERROR: {exc}", file=sys.stderr)
        return 1
    except (PreflightError, AdapterError, OSError) as exc:
        if adapter_started:
            return _unknown_outcome(attempt_dir, binding, str(exc), None)
        persisted = _write_result(attempt_dir, {"status": "FAILED", **binding, "error": str(exc)})
        if attempt_dir is not None and not persisted:
            return _unknown_outcome(attempt_dir, binding, "pre-spawn failure could not be durably sealed", None)
        print(f"PILOT_EXECUTION_ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        # Unexpected post-spawn failures cannot prove the provider did nothing.
        if adapter_started:
            return _unknown_outcome(attempt_dir, binding, f"unexpected {type(exc).__name__}", None)
        raise
    finally:
        signal.signal(signal.SIGTERM, previous_sigterm)


def _write_result(attempt_dir: Path | None, payload: dict[str, Any]) -> bool:
    if attempt_dir is None:
        return False
    try:
        if payload.get("status") == "FAILED":
            write_terminal_result(attempt_dir, payload)
        else:
            atomic_write_json(attempt_dir / "result.json", {"label": "PILOT — NOT EVIDENCE", **payload})
    except OSError:
        return False
    return True


def _unknown_outcome(attempt_dir: Path | None, binding: dict[str, Any], error: str, exit_code: int | None) -> int:
    """Provider call may have happened: not COMPLETED, not FAILED, attempt stays consumed, no retry."""
    _write_result(attempt_dir, {"status": "UNKNOWN_OUTCOME", **binding, "adapter_exit_code": exit_code, "error": error})
    print(f"PILOT_EXECUTION_UNKNOWN_OUTCOME: {error}", file=sys.stderr)
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
