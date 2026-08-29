from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "e0"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prepare_transfer import build_representation


def _state_in_order(keys: list[str]) -> dict:
    values = {
        "goal": "continue safely",
        "rationale": "preserve semantics",
        "unresolved_question": "which substrate is sufficient?",
        "rejected_alternative": "blind replay",
        "artifact_reference": "artifact-17",
    }
    return {key: values[key] for key in keys}


def _serialized(arm: str, state: dict) -> str:
    representation = build_representation(
        arm,
        state,
        {"source_context": "unused"},
        None,
        None,
        None,
    )
    return json.dumps(representation, ensure_ascii=False, separators=(",", ":"))


def test_t0_to_t3_are_invariant_to_input_key_insertion_order() -> None:
    keys = ["goal", "rationale", "unresolved_question", "rejected_alternative", "artifact_reference"]
    left = _state_in_order(keys)
    right = _state_in_order(list(reversed(keys)))

    assert left == right
    for arm in ("T0", "T1", "T2", "T3"):
        assert _serialized(arm, left) == _serialized(arm, right)


def test_t2_event_sequence_uses_canonical_field_order() -> None:
    state = _state_in_order(["rationale", "goal", "artifact_reference", "unresolved_question", "rejected_alternative"])
    representation = build_representation("T2", state, {"source_context": "unused"}, None, None, None)

    fields = [event["field"] for event in representation["events"]]
    assert fields == sorted(state)
    assert representation["projection"] == state
