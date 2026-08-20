import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

from e0_core import MEASUREMENT_LAW_VERSION, evaluate_capture
from global_assignment import forced_optimal_pairs


BASE_ITEM = {
    "kind": "restriction",
    "origin": "user",
    "authority": "user",
    "temporal_validity": None,
    "epistemic_status": "CONFIRMED",
    "resolution_status": "RESOLVED",
    "lifecycle_status": "ACTIVE",
    "rationale": None,
}


def item(item_id, entity, scope, condition):
    value = dict(BASE_ITEM)
    value.update({
        "item_id": item_id,
        "entity": entity,
        "scope": scope,
        "condition": condition,
    })
    return value


def semantic_result(result):
    return {
        "items": {
            row["gold_item_id"]: (
                row["actual_item_id"],
                row["primary_outcome"],
                tuple(
                    (atom["field"], atom["kind"], atom["expected"], atom["actual"])
                    for atom in row["mismatch_atoms"]
                ),
            )
            for row in result["item_results"]
        },
        "fabrications": frozenset(row["actual_item_id"] for row in result["fabrications"]),
        "hard_fails": tuple(
            (row["class"], row["triggered"], row["evidence"])
            for row in result["hard_fails"]
        ),
        "measurement_law_version": result["measurement_law_version"],
        "match_strategy": result["match_strategy"],
    }


class GlobalAssignmentPrimitiveTests(unittest.TestCase):
    def test_greedy_failure_shape_uses_global_optimum(self):
        scores = {
            (0, 0): 13,
            (0, 1): 10,
            (1, 0): 13,
        }
        self.assertEqual(forced_optimal_pairs(2, 2, scores), {0: 1, 1: 0})

    def test_global_tie_accepts_no_ambiguous_pair(self):
        scores = {
            (0, 0): 10,
            (0, 1): 10,
        }
        self.assertEqual(forced_optimal_pairs(1, 2, scores), {})

    def test_pair_common_to_all_optima_is_still_accepted(self):
        scores = {
            (0, 0): 10,
            (0, 1): 10,
            (1, 0): 10,
            (1, 1): 10,
            (2, 2): 20,
        }
        self.assertEqual(forced_optimal_pairs(3, 3, scores), {2: 2})


class CapturePermutationInvariantTests(unittest.TestCase):
    def test_measurement_law_version_is_v03(self):
        self.assertEqual(MEASUREMENT_LAW_VERSION, "e0-correspondence-v0.3")

    def test_gold_and_actual_permutations_preserve_semantic_result(self):
        # G1 can consume either Actual. G2 can only consume A1. Under the old
        # greedy rule, Gold order could decide whether G2 was MISSED. Under
        # v0.3 the unique global optimum must associate G1->A2 and G2->A1.
        g1 = item(
            "G1",
            "release public note",
            "publish public",
            "requires explicit approval",
        )
        g2 = item(
            "G2",
            "release",
            "publish",
            "requires approval",
        )
        a1 = item(
            "A1",
            "release",
            "publish",
            "requires approval",
        )
        a2 = item(
            "A2",
            "public note",
            "public",
            "explicit",
        )

        expected = None
        for gold_items in itertools.permutations([g1, g2]):
            for actual_items in itertools.permutations([a1, a2]):
                result = evaluate_capture(
                    list(gold_items),
                    {"schema_version": "0.1", "items": list(actual_items)},
                    match_spec={"strategy": "deterministic_semantic_fields"},
                )
                normalized = semantic_result(result)
                if expected is None:
                    expected = normalized
                self.assertEqual(normalized, expected)

        self.assertEqual(expected["items"]["G1"][0], "A2")
        self.assertEqual(expected["items"]["G2"][0], "A1")
        self.assertEqual(expected["fabrications"], frozenset())

    def test_global_ambiguity_is_fail_closed_under_permutation(self):
        gold = item("G", "release", "publish", "requires approval")
        a1 = item("A1", "release", "publish", "requires approval")
        a2 = item("A2", "release", "publish", "requires approval")

        for actual_items in itertools.permutations([a1, a2]):
            result = evaluate_capture(
                [gold],
                {"schema_version": "0.1", "items": list(actual_items)},
            )
            self.assertEqual(result["item_results"][0]["primary_outcome"], "MISSED")
            self.assertEqual(
                {row["actual_item_id"] for row in result["fabrications"]},
                {"A1", "A2"},
            )


if __name__ == "__main__":
    unittest.main()
