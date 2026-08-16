#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from e0_core import verify_lock


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    lock = json.loads(Path(args.lock).read_text(encoding="utf-8"))
    errors = verify_lock(lock, args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("EVIDENCE LOCK: VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
