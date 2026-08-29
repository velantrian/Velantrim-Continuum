from __future__ import annotations

import json
import sys
import unittest
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


class TransferRepresentationOrderTests(unittest.TestCase):
    def test_t0_to_t3_are_invariant_to_input_key_insertion_order(self) -> None:
        keys = ["goal", "rationale", "unresolved_question", "rejected_alternative", "artifact_reference"]
        left = _state_in_order(keys)
        right = _state_in_order(list(reversed(keys)))

        self.assertEqual(left, right)
        for arm in ("T0", "T1", "T2", "T3"):
            with self.subTest(arm=arm):
                self.assertEqual(_serialized(arm, left), _serialized(arm, right))

    def test_t0_to_t3_are_invariant_to_nested_object_key_order(self) -> None:
        left = {
            "goal": "continue safely",
            "committed_operation": {"id": "op-17", "status": "COMMITTED"},
            "unknown_operation": {"id": "op-18", "status": "UNKNOWN"},
            "ordered_steps": [
                {"step": 1, "detail": {"kind": "READ", "target": "state"}},
                {"step": 2, "detail": {"kind": "WRITE", "target": "summary"}},
            ],
        }
        right = {
            "ordered_steps": [
                {"detail": {"target": "state", "kind": "READ"}, "step": 1},
                {"detail": {"target": "summary", "kind": "WRITE"}, "step": 2},
            ],
            "unknown_operation": {"status": "UNKNOWN", "id": "op-18"},
            "committed_operation": {"status": "COMMITTED", "id": "op-17"},
            "goal": "continue safely",
        }

        self.assertEqual(left, right)
        for arm in ("T0", "T1", "T2", "T3"):
            with self.subTest(arm=arm):
                self.assertEqual(_serialized(arm, left), _serialized(arm, right))

    def test_array_order_remains_semantically_significant(self) -> None:
        left = {"goal": "continue safely", "ordered_steps": ["first", "second"]}
        right = {"goal": "continue safely", "ordered_steps": ["second", "first"]}

        self.assertNotEqual(left, right)
        for arm in ("T0", "T1", "T2", "T3"):
            with self.subTest(arm=arm):
                self.assertNotEqual(_serialized(arm, left), _serialized(arm, right))

    def test_t2_event_sequence_uses_canonical_field_order(self) -> None:
        state = _state_in_order(["rationale", "goal", "artifact_reference", "unresolved_question", "rejected_alternative"])
        representation = build_representation("T2", state, {"source_context": "unused"}, None, None, None)

        fields = [event["field"] for event in representation["events"]]
        self.assertEqual(fields, sorted(state))
        self.assertEqual(representation["projection"], state)


if __name__ == "__main__":
    unittest.main()
