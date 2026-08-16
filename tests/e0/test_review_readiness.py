import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

from e0_core import require_human_reference
from review_snapshot import build_snapshot

EVALUATE_PATH = ROOT / "scripts" / "e0" / "evaluate_capture.py"
spec = importlib.util.spec_from_file_location("evaluate_capture_module", EVALUATE_PATH)
evaluate_capture_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(evaluate_capture_module)
gold_for_fixture = evaluate_capture_module.gold_for_fixture


class ReviewReadinessTests(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_candidates_remain_non_authoritative(self):
        for relative in (
            "experiments/e0/gold/candidates/capture-gold.ai-proposed.json",
            "experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json",
        ):
            candidate = self.load(relative)
            self.assertEqual(candidate["authorship_status"], "AI_PROPOSED_DRAFT")
            with self.assertRaises(ValueError):
                require_human_reference(candidate)

    def test_pre_post_clarification_are_separate(self):
        gold = self.load("experiments/e0/gold/candidates/capture-gold.ai-proposed.json")
        # Exercise selection logic only; copy is explicitly human-approved in-memory for unit testing.
        approved = dict(gold)
        approved["authorship_status"] = "HUMAN_APPROVED"
        fixture_set = self.load("experiments/e0/fixtures/capture/pilot/fixtures.json")
        fixture = next(item for item in fixture_set["fixtures"] if item["family"] == "F2")
        pre = gold_for_fixture(approved, fixture, "pre")
        post = gold_for_fixture(approved, fixture, "post")
        self.assertNotEqual(pre[0]["condition"], post[0]["condition"])
        self.assertNotIn("substantive", pre[0]["condition"].lower())
        self.assertIn("substantive", post[0]["condition"].lower())

    def test_f8_remains_contested_after_clarification(self):
        gold = self.load("experiments/e0/gold/candidates/capture-gold.ai-proposed.json")
        post = gold["post_clarification_items_by_family"]["F8"]
        self.assertEqual({item["value"] for item in post}, {"APPROVED", "PENDING"})
        self.assertTrue(all(item["epistemic_status"] == "CONTESTED" for item in post))
        self.assertTrue(all(item["resolution_status"] == "CONTESTED" for item in post))

    def test_review_snapshot_is_hash_bound(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            snapshot = build_snapshot(root, "deadbeef", ["a.txt"])
            self.assertEqual(snapshot["reviewed_commit"], "deadbeef")
            self.assertEqual(len(snapshot["artifacts"][0]["sha256"]), 64)
            before = snapshot["artifacts"][0]["sha256"]
            (root / "a.txt").write_text("beta", encoding="utf-8")
            after = build_snapshot(root, "deadbeef", ["a.txt"])["artifacts"][0]["sha256"]
            self.assertNotEqual(before, after)


if __name__ == "__main__":
    unittest.main()
