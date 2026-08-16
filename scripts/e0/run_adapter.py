#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one external model/worker adapter over stdin/stdout JSON.")
    parser.add_argument("--adapter-cmd", required=True, help="Command executed without shell expansion.")
    parser.add_argument("--request", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--metrics-output", required=True)
    args = parser.parse_args()

    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    started = time.perf_counter()
    proc = subprocess.run(
        shlex.split(args.adapter_cmd),
        input=json.dumps(request, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    if proc.returncode != 0:
        raise SystemExit(f"adapter failed ({proc.returncode}): {proc.stderr.strip()}")
    try:
        response = json.loads(proc.stdout)
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
    }
    Path(args.metrics_output).write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
