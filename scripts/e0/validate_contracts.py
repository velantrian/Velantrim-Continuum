#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate_fixture_set(relative: str, expected_partition: str) -> list[str]:
    document = load(relative)
    errors: list[str] = []
    if document.get("partition") != expected_partition:
        errors.append(f"{relative}: wrong partition")
    fixtures = document.get("fixtures", [])
    ids = [fixture.get("fixture_id") for fixture in fixtures]
    if len(ids) != len(set(ids)):
        errors.append(f"{relative}: duplicate fixture ids")
    families = {fixture.get("family") for fixture in fixtures}
    if families != {f"F{index}" for index in range(1, 9)}:
        errors.append(f"{relative}: F1-F8 coverage incomplete")
    for fixture in fixtures:
        policy = fixture.get("clarification_policy", {})
        mode = policy.get("mode")
        turns = policy.get("max_turns")
        if mode == "NONE" and turns != 0:
            errors.append(f"{fixture.get('fixture_id')}: NONE must have max_turns=0")
        if mode == "AT_MOST_ONE" and turns != 1:
            errors.append(f"{fixture.get('fixture_id')}: AT_MOST_ONE must have max_turns=1")
        if turns not in {0, 1}:
            errors.append(f"{fixture.get('fixture_id')}: clarification budget exceeds protocol")
    return errors


def main() -> int:
    errors: list[str] = []
    schema_dir = ROOT / "experiments/e0/schema"
    for path in schema_dir.glob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
    errors += validate_fixture_set("experiments/e0/fixtures/capture/pilot/fixtures.json", "PILOT")
    errors += validate_fixture_set("experiments/e0/fixtures/capture/evidence/fixtures.json", "EVIDENCE")

    pilot = load("experiments/e0/fixtures/capture/pilot/fixtures.json")
    evidence = load("experiments/e0/fixtures/capture/evidence/fixtures.json")
    if len(pilot.get("fixtures", [])) != 8:
        errors.append("pilot capture fixture count must be 8")
    if len(evidence.get("fixtures", [])) != 16:
        errors.append("evidence capture fixture count must be 16")

    candidate_gold = load("experiments/e0/gold/candidates/capture-gold.ai-proposed.json")
    candidate_oracle = load("experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json")
    if candidate_gold.get("authorship_status") != "AI_PROPOSED_DRAFT":
        errors.append("candidate Gold must remain AI_PROPOSED_DRAFT")
    if candidate_oracle.get("authorship_status") != "AI_PROPOSED_DRAFT":
        errors.append("candidate Oracle must remain AI_PROPOSED_DRAFT")

    transfer = load("experiments/e0/fixtures/transfer/scenarios.json")
    scenarios = transfer.get("scenarios", [])
    if sum(item.get("partition") == "PILOT" for item in scenarios) != 1:
        errors.append("transfer scenarios must contain exactly one pilot scenario")
    if sum(item.get("partition") == "EVIDENCE" for item in scenarios) != 2:
        errors.append("transfer scenarios must contain exactly two evidence scenarios")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Experiment 0 contracts: VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
