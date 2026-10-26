#!/usr/bin/env python3
"""Read-only classification of Pilot attempt directories (never writes, never retries).

Covers the case execute_pilot.py cannot handle itself: the supervisor was killed
(e.g. SIGKILL, power loss) before it could write result.json. Such an attempt is
consumed and its provider-side outcome is unknown; it must never be read as
FAILED, COMPLETED or "not spent".

Classification per attempt directory:
  COMPLETED / FAILED / UNKNOWN_OUTCOME  - result.json present (status copied, binding checked)
  ORPHANED_RESERVATION -> outcome UNKNOWN_OUTCOME
                         reservation.json present, no result.json: adapter may have run
  RESERVATION_INCOMPLETE -> outcome NOT_STARTED
                         directory exists without reservation.json: killed before the
                         reservation was written, the adapter is only started afterwards
  RESULT_UNREADABLE   -> outcome UNKNOWN_OUTCOME (corrupt/partial result.json)
Every attempt directory counts as spent regardless of outcome (max_runs protocol unchanged).
Artifact integrity here is not evidence that a provider did or did not process the request.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path
from typing import Any

KNOWN_RESULT_STATUSES = {"COMPLETED", "FAILED", "UNKNOWN_OUTCOME"}


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def classify_attempt(attempt_dir: Path) -> dict[str, Any]:
    name = attempt_dir.name
    try:
        number = int(name.split("-", 1)[1])
    except (IndexError, ValueError):
        number = None
    entry: dict[str, Any] = {"attempt_dir": str(attempt_dir), "attempt": number, "spent": True}
    reservation_path = attempt_dir / "reservation.json"
    result_path = attempt_dir / "result.json"
    reservation = _read_json(reservation_path) if reservation_path.is_file() else None
    if result_path.exists():
        result = _read_json(result_path)
        status = result.get("status") if result else None
        if status not in KNOWN_RESULT_STATUSES:
            entry.update(classification="RESULT_UNREADABLE", outcome="UNKNOWN_OUTCOME")
            return entry
        entry.update(classification=status, outcome=status)
        problems = []
        if result.get("attempt") is not None and number is not None and result.get("attempt") != number:
            problems.append("result attempt does not match directory")
        if reservation and result.get("package_sha256") not in (None, reservation.get("package_sha256")):
            problems.append("result package_sha256 does not match reservation")
        if problems:
            entry.update(classification="BINDING_MISMATCH", outcome="UNKNOWN_OUTCOME", problems=problems)
        return entry
    if reservation_path.exists():
        entry.update(classification="ORPHANED_RESERVATION", outcome="UNKNOWN_OUTCOME",
                     reason="supervisor stopped after reservation without writing result.json; "
                            "adapter may have been started")
        if reservation:
            entry["package_sha256"] = reservation.get("package_sha256")
        return entry
    entry.update(classification="RESERVATION_INCOMPLETE", outcome="NOT_STARTED",
                 reason="attempt directory reserved but reservation.json never written; "
                        "adapter is only launched after reservation.json")
    return entry


def classify_package(package_root: Path) -> list[dict[str, Any]]:
    return [classify_attempt(path) for path in sorted(package_root.glob("attempt-*")) if path.is_dir()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_root", type=Path, help="<pilot output root>/<package_sha256>")
    args = parser.parse_args()
    entries = classify_package(args.package_root)
    print(json.dumps({"attempts": entries, "spent": len(entries)}, ensure_ascii=False, indent=2))
    return 4 if any(e["outcome"] == "UNKNOWN_OUTCOME" for e in entries) else 0


if __name__ == "__main__":
    raise SystemExit(main())
