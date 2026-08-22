#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import tempfile
import time
from pathlib import Path


def bounded_run(command: list[str], *, request_text: str, cwd: Path, env: dict[str, str], timeout_seconds: int, max_output_bytes: int) -> tuple[int, str, str, float]:
    started = time.perf_counter()
    with tempfile.TemporaryFile(mode="w+b") as stdout_file, tempfile.TemporaryFile(mode="w+b") as stderr_file:
        proc = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
        )
        try:
            assert proc.stdin is not None
            proc.stdin.write(request_text)
            proc.stdin.close()
            deadline = time.monotonic() + timeout_seconds
            while proc.poll() is None:
                if time.monotonic() >= deadline:
                    proc.kill()
                    proc.wait()
                    raise SystemExit(f"adapter timeout after {timeout_seconds}s")
                if stdout_file.tell() > max_output_bytes or stderr_file.tell() > max_output_bytes:
                    proc.kill()
                    proc.wait()
                    raise SystemExit(f"adapter output exceeded {max_output_bytes} bytes")
                time.sleep(0.02)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
        if stdout_file.tell() > max_output_bytes or stderr_file.tell() > max_output_bytes:
            raise SystemExit(f"adapter output exceeded {max_output_bytes} bytes")
        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout = stdout_file.read(max_output_bytes + 1).decode("utf-8", errors="replace")
        stderr = stderr_file.read(max_output_bytes + 1).decode("utf-8", errors="replace")
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    return proc.returncode, stdout, stderr, elapsed_ms


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one bounded external model/worker adapter over stdin/stdout JSON. This is not a sandbox.")
    parser.add_argument("--adapter-cmd", required=True, help="Command executed without shell expansion.")
    parser.add_argument("--request", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--metrics-output", required=True)
    parser.add_argument("--cwd", required=True, help="Explicit adapter working directory.")
    parser.add_argument("--timeout-seconds", type=int, required=True)
    parser.add_argument("--max-output-bytes", type=int, required=True)
    parser.add_argument(
        "--inherit-env",
        action="append",
        default=[],
        metavar="NAME",
        help="Environment variable to pass through. May be repeated. PATH is always retained if present.",
    )
    args = parser.parse_args()

    if args.timeout_seconds <= 0:
        raise SystemExit("--timeout-seconds must be > 0")
    if args.max_output_bytes <= 0:
        raise SystemExit("--max-output-bytes must be > 0")

    cwd = Path(args.cwd).resolve()
    if not cwd.is_dir():
        raise SystemExit(f"adapter cwd is not a directory: {cwd}")

    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    env: dict[str, str] = {}
    if "PATH" in os.environ:
        env["PATH"] = os.environ["PATH"]
    for name in args.inherit_env:
        if not name or "=" in name:
            raise SystemExit(f"invalid --inherit-env name: {name!r}")
        if name in os.environ:
            env[name] = os.environ[name]

    returncode, stdout, stderr, elapsed_ms = bounded_run(
        shlex.split(args.adapter_cmd),
        request_text=json.dumps(request, ensure_ascii=False),
        cwd=cwd,
        env=env,
        timeout_seconds=args.timeout_seconds,
        max_output_bytes=args.max_output_bytes,
    )
    if returncode != 0:
        raise SystemExit(f"adapter failed ({returncode}): {stderr.strip()}")
    try:
        response = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"adapter stdout is not JSON: {exc}") from exc

    Path(args.output).write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metrics = {
        "latency_ms": {"provenance": "MEASURED", "value": elapsed_ms, "unit": "ms"},
        "model_calls": {"provenance": "MEASURED", "value": 1, "unit": "calls"},
        "tool_calls": {"provenance": "UNAVAILABLE", "value": None, "unit": "calls"},
        "input_tokens": {"provenance": "UNAVAILABLE", "value": None, "unit": "tokens"},
        "output_tokens": {"provenance": "UNAVAILABLE", "value": None, "unit": "tokens"},
        "cost": {"provenance": "UNAVAILABLE", "value": None, "unit": None},
        "execution_limits": {
            "timeout_seconds": args.timeout_seconds,
            "max_output_bytes": args.max_output_bytes,
            "cwd": str(cwd),
            "inherited_env_names": sorted(set((["PATH"] if "PATH" in env else []) + args.inherit_env)),
            "sandbox": False,
        },
    }
    Path(args.metrics_output).write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
