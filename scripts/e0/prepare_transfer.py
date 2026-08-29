#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from e0_core import require_human_reference, t4_eligibility


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def scenario_source(fixtures: dict, scenario_id: str) -> dict:
    for scenario in fixtures.get("scenarios", []):
        if scenario.get("scenario_id") == scenario_id:
            return scenario
    raise ValueError(f"scenario not found: {scenario_id}")


def oracle_state(oracle: dict, scenario_id: str) -> dict:
    require_human_reference(oracle)
    value = oracle.get("scenarios", {}).get(scenario_id)
    if not isinstance(value, dict):
        raise ValueError(f"approved Oracle has no scenario: {scenario_id}")
    return value


def ordered_state(state: dict) -> dict:
    """Return a semantically equivalent state with deterministic top-level key order."""
    return {key: state[key] for key in sorted(state)}


def event_projection(state: dict) -> tuple[list[dict], dict]:
    canonical = ordered_state(state)
    events = [
        {"seq": index + 1, "op": "SET", "field": key, "value": value}
        for index, (key, value) in enumerate(canonical.items())
    ]
    projected: dict = {}
    for event in events:
        projected[event["field"]] = event["value"]
    return events, projected


def build_representation(arm: str, state: dict, source: dict, context_limit: int | None, reserved_tokens: int | None, full_context_tokens: int | None) -> dict:
    canonical = ordered_state(state)
    if arm == "T0":
        lines = [f"{key}: {json.dumps(value, ensure_ascii=False, sort_keys=True)}" for key, value in canonical.items()]
        return {"arm": arm, "format": "structured_summary", "summary": "\n".join(lines)}
    if arm == "T1":
        return {"arm": arm, "format": "canonical_current_state", "state": canonical}
    if arm == "T2":
        events, projection = event_projection(canonical)
        if projection != state:
            raise RuntimeError("deterministic projection failed fidelity check")
        return {"arm": arm, "format": "event_log_plus_projection", "events": events, "projection": projection}
    if arm == "T3":
        events, projection = event_projection(canonical)
        manifest_fields = {"rationale", "unresolved_question", "rejected_alternative", "artifact_reference"}
        manifest = " | ".join(f"{key}={value}" for key, value in canonical.items() if key in manifest_fields)
        return {"arm": arm, "format": "projection_plus_reconstructive_manifest", "projection": projection, "manifest": manifest, "events": events}
    if arm == "T4":
        if None in {context_limit, reserved_tokens, full_context_tokens}:
            raise ValueError("T4 requires context-limit, reserved-tokens and full-context-tokens")
        eligible, status = t4_eligibility(int(full_context_tokens), int(context_limit), int(reserved_tokens))
        if not eligible:
            return {"arm": arm, "format": "full_context_reference", "eligibility": status, "context": None}
        return {"arm": arm, "format": "full_context_reference", "eligibility": status, "context": source["source_context"]}
    raise ValueError(f"unsupported arm: {arm}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", required=True)
    parser.add_argument("--oracle", required=True)
    parser.add_argument("--scenario-id", required=True)
    parser.add_argument("--arm", required=True, choices=["T0", "T1", "T2", "T3", "T4"])
    parser.add_argument("--context-limit", type=int)
    parser.add_argument("--reserved-tokens", type=int)
    parser.add_argument("--full-context-tokens", type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    fixture_doc = load(args.fixtures)
    source = scenario_source(fixture_doc, args.scenario_id)
    state = oracle_state(load(args.oracle), args.scenario_id)
    representation = build_representation(args.arm, state, source, args.context_limit, args.reserved_tokens, args.full_context_tokens)
    Path(args.output).write_text(json.dumps(representation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
