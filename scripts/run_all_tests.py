#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys


COMMANDS = (
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    [sys.executable, "-m", "unittest", "discover", "-s", "tests/e0", "-v"],
)


def main() -> int:
    for command in COMMANDS:
        print(f"+ {' '.join(command)}", flush=True)
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
