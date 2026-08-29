#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from e0_core import evaluate_capture, require_human_reference

ROOT = Path(__file__).resolve().parents[2]


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_schema(instance: object, schema_relative: str, label: str) -> None:
    schema = load(ROOT / schema_relative)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    if errors:
        rendered = "; ".join(f"{list(error.absolute_path)}: {error.message}" for error in errors)
        raise ValueError(f"{label} schema violation: {rendered}")


def find_fixture(fixture_set: dict, fixture_id: str) -> dict:
    for fixture in fixture_set.get("fixtures", []):
        if fixture.get("fixture_id") == fixture_id:
            return fixture
    raise ValueError(f"fixture not found: {fixture_id}")


def gold_for_fixture(reference: dict, fixture: dict, clarification_stage: str) -> list[dict]:
    require_human_reference(reference)
    family = fixture["family"]
    if clarification_stage == "post":
        fixture_id = fixture.get("fixture_id")
        if fixture_id:
            fixture_specific = reference.get("post_clarification_items_by_fixture", {}).get(fixture_id)
            if fixture_specific is not None:
                return fixture_specific
        post = reference.get("post_clarification_items_by_family", {}).get(family)
        if post is not None:
            return post
    items = reference.get("items_by_family", {}).get(family)
    if items is None:
        raise ValueError(f"approved Gold has no family entry: {family}")
    return items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-set", required=True)
    parser.add_argument("--fixture-id", required=True)
    parser.add_argument("--gold", required=True)
    parser.add_argument("--captured-state", required=True)
    parser.add_argument("--clarification-stage", choices=["pre", "post"], default="pre")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    fixture_set = load(args.fixture_set)
    fixture = find_fixture(fixture_set, args.fixture_id)
    gold = load(args.gold)
    captured = load(args.captured_state)
    validate_schema(captured, "experiments/e0/schema/e0-state.schema.json", "captured state")

    reference_items = gold_for_fixture(gold, fixture, args.clarification_stage)
    result = evaluate_capture(
        reference_items,
        captured,
        fixture.get("hard_fail_bindings", []),
        fixture.get("match_spec"),
    )
    result["fixture_id"] = args.fixture_id
    result["clarification_stage"] = args.clarification_stage
    validate_schema(result, "experiments/e0/schema/evaluation.schema.json", "evaluation result")

    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
