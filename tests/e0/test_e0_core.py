import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

from e0_core import (
    MEASUREMENT_LAW_VERSION,
    clarification_allowed,
    evaluate_capture,
    norm,
    require_human_reference,
    t4_eligibility,
    validate_manifest,
    verify_lock,
)

BASE = {"schema_version": "0.1", "items": []}
GOLD = {
    "item_id": "g1",
    "entity": "release_note",
    "kind": "restriction",
    "scope": "publish",
    "condition": "requires approval",
    "origin": "user",
    "authority": "user",
    "temporal_validity": None,
    "epistemic_status": "CONFIRMED",
    "resolution_status": "RESOLVED",
    "lifecycle_status": "ACTIVE",
    "rationale": None,
}


class EvaluatorTests(unittest.TestCase):
    def state(self, item):
        return {"schema_version": "0.1", "items": [item]}

    def outcome(self, gold, actual):
        return evaluate_capture([gold], self.state(actual))["item_results"][0]["primary_outcome"]

    def test_exact(self):
        self.assertEqual(self.outcome(GOLD, dict(GOLD)), "EXACT")

    def test_missed(self):
        result = evaluate_capture([GOLD], BASE)
        self.assertEqual(result["item_results"][0]["primary_outcome"], "MISSED")

    def test_under_specified(self):
        actual = dict(GOLD)
        actual["condition"] = None
        self.assertEqual(self.outcome(GOLD, actual), "UNDER_SPECIFIED")
        atoms = evaluate_capture([GOLD], self.state(actual))["item_results"][0]["mismatch_atoms"]
        self.assertEqual([atom["field"] for atom in atoms], ["condition"])

    def test_partial_is_not_double_counted_as_under_specified(self):
        gold = dict(GOLD)
        gold["rationale"] = "reason"
        actual = dict(gold)
        actual["rationale"] = None
        self.assertEqual(self.outcome(gold, actual), "PARTIAL")

    def test_misattributed_entity_when_other_semantic_anchors_remain_compatible(self):
        actual = dict(GOLD)
        actual["entity"] = "other_release_artifact"
        self.assertEqual(self.outcome(GOLD, actual), "MISATTRIBUTED")

    def test_exact_id_does_not_override_origin_conflict(self):
        actual = dict(GOLD)
        actual["origin"] = "assistant"
        result = evaluate_capture([GOLD], self.state(actual))
        self.assertEqual(result["item_results"][0]["primary_outcome"], "MISSED")
        self.assertEqual(result["fabrications"], [{"actual_item_id": "g1", "primary_outcome": "FABRICATED"}])

    def test_exact_id_does_not_override_authority_conflict(self):
        actual = dict(GOLD)
        actual["authority"] = "assistant"
        result = evaluate_capture([GOLD], self.state(actual))
        self.assertEqual(result["item_results"][0]["primary_outcome"], "MISSED")
        self.assertEqual(len(result["fabrications"]), 1)

    def test_exact_id_does_not_override_symbolic_value_conflict(self):
        gold = dict(GOLD)
        gold["value"] = "APPROVED"
        actual = dict(gold)
        actual["value"] = "PENDING"
        result = evaluate_capture([gold], self.state(actual))
        self.assertEqual(result["item_results"][0]["primary_outcome"], "MISSED")
        self.assertEqual(len(result["fabrications"]), 1)

    def test_same_kind_alone_is_not_sufficient_for_association(self):
        actual = dict(GOLD)
        actual.update({
            "item_id": "x",
            "entity": "different_entity",
            "scope": "different_scope",
            "condition": "different_condition",
            "origin": None,
            "authority": None,
        })
        result = evaluate_capture([GOLD], self.state(actual))
        self.assertEqual(result["item_results"][0]["primary_outcome"], "MISSED")
        self.assertEqual(result["fabrications"][0]["actual_item_id"], "x")

    def test_equal_best_score_is_ambiguous_not_index_tiebroken(self):
        first = dict(GOLD)
        first["item_id"] = "a"
        second = dict(GOLD)
        second["item_id"] = "b"
        state = {"schema_version": "0.1", "items": [first, second]}
        result = evaluate_capture([GOLD], state)
        self.assertEqual(result["item_results"][0]["primary_outcome"], "MISSED")
        self.assertEqual({item["actual_item_id"] for item in result["fabrications"]}, {"a", "b"})

    def test_unicode_normalization_preserves_non_ascii_semantic_anchor(self):
        self.assertEqual(norm("Клиент — чувствительность"), "клиент чувствительность")
        gold = dict(GOLD)
        gold.update({"item_id": "unicode-gold", "entity": "клиент", "scope": None, "condition": None})
        actual = dict(gold)
        actual["item_id"] = "unicode-actual"
        result = evaluate_capture([gold], self.state(actual))
        self.assertEqual(result["item_results"][0]["primary_outcome"], "EXACT")
        self.assertEqual(result["item_results"][0]["actual_item_id"], "unicode-actual")

    def test_fixture_match_spec_is_validated_and_reported(self):
        result = evaluate_capture(
            [GOLD],
            self.state(dict(GOLD)),
            match_spec={"strategy": "deterministic_semantic_fields"},
        )
        self.assertEqual(result["measurement_law_version"], MEASUREMENT_LAW_VERSION)
        self.assertEqual(result["match_strategy"], "deterministic_semantic_fields")
        with self.assertRaisesRegex(ValueError, "unsupported match_spec.strategy"):
            evaluate_capture([GOLD], self.state(dict(GOLD)), match_spec={"strategy": "unused_strategy"})

    def test_temporally_wrong(self):
        gold = dict(GOLD)
        gold["temporal_validity"] = "before Friday"
        actual = dict(gold)
        actual["temporal_validity"] = "after Friday"
        self.assertEqual(self.outcome(gold, actual), "TEMPORALLY_WRONG")

    def test_over_promoted(self):
        gold = dict(GOLD)
        gold["epistemic_status"] = "CAUTION"
        gold["resolution_status"] = "UNRESOLVED"
        actual = dict(gold)
        actual["epistemic_status"] = "CONFIRMED"
        self.assertEqual(self.outcome(gold, actual), "OVER_PROMOTED")

    def test_conflict_collapsed_has_precedence(self):
        gold = dict(GOLD)
        gold["epistemic_status"] = "CONTESTED"
        gold["resolution_status"] = "CONTESTED"
        actual = dict(gold)
        actual["resolution_status"] = "RESOLVED"
        actual["epistemic_status"] = "CONFIRMED"
        self.assertEqual(self.outcome(gold, actual), "CONFLICT_COLLAPSED")

    def test_fabricated(self):
        actual = dict(GOLD)
        actual["item_id"] = "x"
        result = evaluate_capture([], self.state(actual))
        self.assertEqual(result["fabrications"][0]["primary_outcome"], "FABRICATED")

    def test_hard_fail_lost_restriction(self):
        bindings = [{"item_ref": "g1", "hard_fail_class": "LOST_CRITICAL_RESTRICTION", "predicate": "x"}]
        result = evaluate_capture([GOLD], BASE, bindings)
        self.assertTrue(result["hard_fails"][0]["triggered"])

    def test_fabricated_authorization_hard_fail(self):
        actual = dict(GOLD)
        actual.update({"item_id": "fake", "kind": "approval", "scope": "publish approval", "lifecycle_status": "ACTIVE"})
        bindings = [{"item_ref": "ABSENT_AUTHORIZATION", "hard_fail_class": "FABRICATED_USER_AUTHORIZATION", "predicate": "x"}]
        result = evaluate_capture([], self.state(actual), bindings)
        self.assertTrue(result["hard_fails"][0]["triggered"])

    def test_human_reference_gate(self):
        with self.assertRaises(ValueError):
            require_human_reference({"authorship_status": "AI_PROPOSED_DRAFT"})
        require_human_reference({"authorship_status": "HUMAN_APPROVED"})

    def test_clarification_budget(self):
        self.assertTrue(clarification_allowed({"mode": "AT_MOST_ONE", "max_turns": 1}, 1))
        self.assertFalse(clarification_allowed({"mode": "AT_MOST_ONE", "max_turns": 1}, 2))
        self.assertFalse(clarification_allowed({"mode": "NONE", "max_turns": 0}, 1))

    def test_t4_no_silent_truncation(self):
        self.assertEqual(t4_eligibility(800, 1000, 200), (True, "ELIGIBLE"))
        self.assertEqual(t4_eligibility(801, 1000, 200), (False, "T4_INELIGIBLE_CONTEXT_LIMIT"))

    def test_manifest_requires_hashes(self):
        errors = validate_manifest({"run_type": "PILOT"})
        self.assertGreaterEqual(len(errors), 6)

    def test_evidence_lock_requires_human_approval_and_hash_integrity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / "x.txt"
            artifact.write_text("abc", encoding="utf-8")
            lock = {
                "status": "EVIDENCE_READY",
                "human_gold_approval": {"status": "REQUIRED"},
                "artifacts": [{"path": "x.txt", "sha256": "0" * 64}],
            }
            errors = verify_lock(lock, root)
            self.assertIn("human Gold/Oracle approval missing", errors)
            self.assertIn("hash mismatch: x.txt", errors)


if __name__ == "__main__":
    unittest.main()
