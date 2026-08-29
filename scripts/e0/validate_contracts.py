#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from e0_core import evaluate_capture

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "experiments/e0/schema"
SCHEMA_INSTANCE_BINDINGS = {
    "capture-fixture.schema.json": (
        "experiments/e0/fixtures/capture/pilot/fixtures.json",
        "experiments/e0/fixtures/capture/evidence/fixtures.json",
    ),
}
SCHEMA_COVERAGE = {
    "capture-fixture.schema.json": "COMMITTED_INSTANCES",
    "e0-state.schema.json": "DERIVED_FROM_COMMITTED_GOLD",
    "evaluation.schema.json": "GENERATED_FROM_CURRENT_EVALUATOR",
    "evidence-lock.schema.json": "NO_COMMITTED_INSTANCE_YET",
    "run-manifest.schema.json": "NO_COMMITTED_INSTANCE_YET",
}


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def render_json_path(parts) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def validate_instance(schema: dict, instance: object, label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"{label} {render_json_path(error.absolute_path)}: schema violation: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    ]


def validate_derived_state_instances(schema: dict) -> list[str]:
    errors: list[str] = []
    reference_paths = (
        "experiments/e0/gold/candidates/capture-gold.ai-proposed.json",
        "experiments/e0/gold/approved/capture-gold.v0.1.json",
    )
    sections = (
        "items_by_family",
        "post_clarification_items_by_family",
        "post_clarification_items_by_fixture",
    )
    for relative in reference_paths:
        reference = load(relative)
        for section in sections:
            for key, items in reference.get(section, {}).items():
                instance = {"schema_version": "0.1", "items": items}
                errors += validate_instance(schema, instance, f"{relative}::{section}.{key}")
    return errors


def validate_generated_evaluation_instance(schema: dict) -> list[str]:
    approved_gold = load("experiments/e0/gold/approved/capture-gold.v0.1.json")
    reference_items = approved_gold["items_by_family"]["F1"]
    captured_state = {"schema_version": "0.1", "items": reference_items}
    result = evaluate_capture(reference_items, captured_state, [], None)
    result["fixture_id"] = "SCHEMA-CONTRACT-F1"
    result["clarification_stage"] = "pre"
    return validate_instance(schema, result, "generated evaluator contract")


def validate_json_schemas() -> list[str]:
    errors: list[str] = []
    schemas: dict[str, dict] = {}
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid Draft 2020-12 schema: {exc.message}")
            continue
        schemas[path.name] = schema

    discovered = set(schemas)
    classified = set(SCHEMA_COVERAGE)
    if discovered != classified:
        missing = sorted(discovered - classified)
        stale = sorted(classified - discovered)
        if missing:
            errors.append(f"schemas missing explicit coverage classification: {missing}")
        if stale:
            errors.append(f"coverage classification references missing schemas: {stale}")

    for schema_name, instances in SCHEMA_INSTANCE_BINDINGS.items():
        schema = schemas.get(schema_name)
        if schema is None:
            errors.append(f"missing or invalid schema required for instance validation: {schema_name}")
            continue
        for relative in instances:
            try:
                instance = load(relative)
            except (FileNotFoundError, json.JSONDecodeError) as exc:
                errors.append(f"{relative}: cannot load schema-bound instance: {exc}")
                continue
            errors += validate_instance(schema, instance, relative)

    state_schema = schemas.get("e0-state.schema.json")
    if state_schema is not None:
        errors += validate_derived_state_instances(state_schema)

    evaluation_schema = schemas.get("evaluation.schema.json")
    if evaluation_schema is not None:
        errors += validate_generated_evaluation_instance(evaluation_schema)

    return errors


def validate_fixture_set(relative: str, expected_partition: str, candidate_gold: dict) -> list[str]:
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
        family = fixture.get("family")
        candidate_ids = {item.get("item_id") for item in candidate_gold.get("items_by_family", {}).get(family, [])}
        missing_refs = set(fixture.get("expected_item_refs", [])) - candidate_ids
        if missing_refs:
            errors.append(f"{fixture.get('fixture_id')}: candidate Gold missing refs {sorted(missing_refs)}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += validate_json_schemas()

    candidate_gold = load("experiments/e0/gold/candidates/capture-gold.ai-proposed.json")
    candidate_oracle = load("experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json")
    errors += validate_fixture_set("experiments/e0/fixtures/capture/pilot/fixtures.json", "PILOT", candidate_gold)
    errors += validate_fixture_set("experiments/e0/fixtures/capture/evidence/fixtures.json", "EVIDENCE", candidate_gold)

    pilot = load("experiments/e0/fixtures/capture/pilot/fixtures.json")
    evidence = load("experiments/e0/fixtures/capture/evidence/fixtures.json")
    if len(pilot.get("fixtures", [])) != 8:
        errors.append("pilot capture fixture count must be 8")
    if len(evidence.get("fixtures", [])) != 16:
        errors.append("evidence capture fixture count must be 16")
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
    print("Experiment 0 contracts: VALID (Draft 2020-12 schema + explicit coverage + research invariants)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
