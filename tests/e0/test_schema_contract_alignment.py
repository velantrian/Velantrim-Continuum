from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "e0"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from e0_core import evaluate_capture
from evaluate_capture import validate_schema


class SchemaContractAlignmentTests(unittest.TestCase):
    def test_current_evaluator_output_matches_evaluation_schema(self) -> None:
        item = {
            "item_id": "x1",
            "entity": "artifact",
            "kind": "restriction",
            "value": "DO_NOT_SEND",
            "scope": "send",
            "condition": None,
            "origin": "user",
            "authority": "user",
            "temporal_validity": None,
            "epistemic_status": "CONFIRMED",
            "resolution_status": "RESOLVED",
            "lifecycle_status": "ACTIVE",
            "rationale": None,
            "source_refs": ["test:user"],
        }
        state = {"schema_version": "0.1", "items": [item]}
        result = evaluate_capture([item], state, [], None)
        result["fixture_id"] = "SCHEMA-TEST"
        result["clarification_stage"] = "pre"

        self.assertEqual(result["measurement_law_version"], "e0-correspondence-v0.3")
        validate_schema(result, "experiments/e0/schema/evaluation.schema.json", "evaluation result")

    def test_state_schema_rejects_unknown_top_level_fields(self) -> None:
        state = {"schema_version": "0.1", "items": [], "unexpected": True}
        with self.assertRaisesRegex(ValueError, "captured state schema violation"):
            validate_schema(state, "experiments/e0/schema/e0-state.schema.json", "captured state")


if __name__ == "__main__":
    unittest.main()
