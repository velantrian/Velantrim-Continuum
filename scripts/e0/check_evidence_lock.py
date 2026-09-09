#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from e0_core import verify_lock


EVIDENCE_LOCK_SCHEMA = Path("experiments/e0/schema/evidence-lock.schema.json")


def _render_json_path(parts) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def validate_lock_schema(lock: object, repo_root: str | Path) -> list[str]:
    schema_path = Path(repo_root).resolve() / EVIDENCE_LOCK_SCHEMA
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [
        f"{_render_json_path(error.absolute_path)}: schema violation: {error.message}"
        for error in sorted(
            validator.iter_errors(lock),
            key=lambda item: tuple(str(part) for part in item.absolute_path),
        )
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    lock = json.loads(Path(args.lock).read_text(encoding="utf-8"))
    schema_errors = validate_lock_schema(lock, args.repo_root)
    if schema_errors:
        for error in schema_errors:
            print(f"ERROR: {error}")
        return 1

    errors = verify_lock(lock, args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("EVIDENCE LOCK: VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
