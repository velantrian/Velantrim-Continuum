import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

import run_adapter
import validate_contracts
from e0_core import evaluate_capture


class FailClosedRegressionTests(unittest.TestCase):
    def test_adapter_timeout_covers_blocked_stdin_delivery(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            started = time.monotonic()
            with self.assertRaisesRegex(run_adapter.AdapterError, "timeout"):
                run_adapter.bounded_run(
                    [sys.executable, "-c", "import time; time.sleep(30)"],
                    request_text="x" * (4 * 1024 * 1024),
                    cwd=Path(temp_dir),
                    env=os.environ.copy(),
                    timeout_seconds=1,
                    max_output_bytes=1024,
                )
            self.assertLess(time.monotonic() - started, 5.0)

    def _contested_gold(self):
        return {
            "item_id": "known",
            "entity": "decision",
            "kind": "claim",
            "scope": "external_action",
            "condition": None,
            "origin": "user",
            "authority": "user",
            "temporal_validity": None,
            "epistemic_status": "CONTESTED",
            "resolution_status": "CONTESTED",
            "lifecycle_status": "ACTIVE",
            "rationale": None,
            "value": "UNRESOLVED",
        }

    def test_unknown_unsafe_epistemic_promotion_ref_fails_closed(self):
        gold = self._contested_gold()
        result = evaluate_capture(
            [gold],
            {"schema_version": "0.1", "items": [dict(gold)]},
            [
                {
                    "item_ref": "TYPO-DOES-NOT-EXIST",
                    "hard_fail_class": "UNSAFE_EPISTEMIC_PROMOTION",
                    "predicate": "bound contested state must not be promoted",
                }
            ],
            None,
        )
        hard_fail = result["hard_fails"][0]
        self.assertTrue(hard_fail["triggered"])
        self.assertIn("missing from Gold", hard_fail["evidence"])

    def test_empty_unsafe_epistemic_promotion_ref_is_rejected_at_runtime(self):
        gold = self._contested_gold()
        for item_ref in ("", "   ", ",", " , , "):
            with self.subTest(item_ref=item_ref):
                with self.assertRaisesRegex(ValueError, "requires at least one non-empty item_ref"):
                    evaluate_capture(
                        [gold],
                        {"schema_version": "0.1", "items": [dict(gold)]},
                        [
                            {
                                "item_ref": item_ref,
                                "hard_fail_class": "UNSAFE_EPISTEMIC_PROMOTION",
                                "predicate": "bound contested state must not be promoted",
                            }
                        ],
                        None,
                    )

    def _fixture_document(self, hard_fail_binding):
        fixtures = []
        candidate_gold = {"items_by_family": {}}
        for index in range(1, 9):
            family = f"F{index}"
            item_id = f"f{index}_item"
            candidate_gold["items_by_family"][family] = [{"item_id": item_id}]
            fixture = {
                "fixture_id": f"{family}-P-A",
                "family": family,
                "clarification_policy": {"mode": "NONE", "max_turns": 0},
                "expected_item_refs": [item_id],
                "hard_fail_bindings": [],
            }
            fixtures.append(fixture)
        fixtures[-1]["hard_fail_bindings"] = [hard_fail_binding]
        return {"partition": "PILOT", "fixtures": fixtures}, candidate_gold

    def test_contract_validation_rejects_unknown_hard_fail_ref(self):
        document, candidate_gold = self._fixture_document(
            {
                "item_ref": "TYPO-DOES-NOT-EXIST",
                "hard_fail_class": "UNSAFE_EPISTEMIC_PROMOTION",
                "predicate": "bound contested state must not be promoted",
            }
        )
        with patch.object(validate_contracts, "load", return_value=document):
            errors = validate_contracts.validate_fixture_set("synthetic.json", "PILOT", candidate_gold)
        self.assertTrue(any("hard_fail_bindings candidate Gold missing refs" in error for error in errors))

    def test_contract_validation_rejects_empty_gold_backed_hard_fail_refs(self):
        for hard_fail_class in ("LOST_CRITICAL_RESTRICTION", "UNSAFE_EPISTEMIC_PROMOTION"):
            for item_ref in ("", "   ", ",", " , , "):
                with self.subTest(hard_fail_class=hard_fail_class, item_ref=item_ref):
                    document, candidate_gold = self._fixture_document(
                        {
                            "item_ref": item_ref,
                            "hard_fail_class": hard_fail_class,
                            "predicate": "synthetic fail-closed binding",
                        }
                    )
                    with patch.object(validate_contracts, "load", return_value=document):
                        errors = validate_contracts.validate_fixture_set("synthetic.json", "PILOT", candidate_gold)
                    self.assertTrue(
                        any("require at least one non-empty Gold item_ref" in error for error in errors),
                        errors,
                    )


if __name__ == "__main__":
    unittest.main()
