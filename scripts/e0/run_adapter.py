#!/usr/bin/env python3
"""Internal bounded adapter primitive for Experiment 0 Pilot execution.

This module is not an authorization boundary and must not be invoked directly. The only
supported Pilot execution entrypoint is execute_pilot.py, which performs fail-closed
manifest, canonical-state, and approval validation before calling bounded_run().
"""
from __future__ import annotations

import os
import signal
import subprocess
import tempfile
import time
from pathlib import Path


class AdapterError(RuntimeError):
    pass


def terminate_process_tree(proc: subprocess.Popen[str]) -> None:
    """Terminate the adapter process tree with best available platform semantics."""
    if os.name == "posix":
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        deadline = time.monotonic() + 0.5
        while time.monotonic() < deadline and proc.poll() is None:
            time.sleep(0.02)
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            proc.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            pass
        return

    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
            text=True,
            capture_output=True,
            check=False,
        )
        try:
            proc.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        return

    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def bounded_run(
    command: list[str],
    *,
    request_text: str,
    cwd: Path,
    env: dict[str, str],
    timeout_seconds: int,
    max_output_bytes: int,
) -> tuple[int, str, str, float]:
    if not command:
        raise AdapterError("adapter command is empty")
    if timeout_seconds <= 0:
        raise AdapterError("timeout_seconds must be > 0")
    if max_output_bytes <= 0:
        raise AdapterError("max_output_bytes must be > 0")
    if not cwd.is_dir():
        raise AdapterError(f"adapter cwd is not a directory: {cwd}")

    started = time.perf_counter()
    with tempfile.TemporaryFile(mode="w+b") as stdout_file, tempfile.TemporaryFile(mode="w+b") as stderr_file:
        popen_kwargs: dict[str, object] = {}
        if os.name == "posix":
            popen_kwargs["start_new_session"] = True
        elif os.name == "nt":
            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

        proc = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
            **popen_kwargs,
        )
        try:
            assert proc.stdin is not None
            proc.stdin.write(request_text)
            proc.stdin.close()
            deadline = time.monotonic() + timeout_seconds
            while proc.poll() is None:
                if time.monotonic() >= deadline:
                    terminate_process_tree(proc)
                    raise AdapterError(f"adapter timeout after {timeout_seconds}s")
                if stdout_file.tell() > max_output_bytes or stderr_file.tell() > max_output_bytes:
                    terminate_process_tree(proc)
                    raise AdapterError(f"adapter output exceeded {max_output_bytes} bytes")
                time.sleep(0.02)
        finally:
            if proc.poll() is None:
                terminate_process_tree(proc)

        if stdout_file.tell() > max_output_bytes or stderr_file.tell() > max_output_bytes:
            raise AdapterError(f"adapter output exceeded {max_output_bytes} bytes")
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout = stdout_file.read(max_output_bytes + 1).decode("utf-8", errors="replace")
        stderr = stderr_file.read(max_output_bytes + 1).decode("utf-8", errors="replace")

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    return proc.returncode, stdout, stderr, elapsed_ms


def main() -> int:
    raise SystemExit(
        "run_adapter.py is an internal helper and cannot execute a Pilot directly; use scripts/e0/execute_pilot.py with an authorized manifest"
    )


if __name__ == "__main__":
    raise SystemExit(main())
