import importlib.util
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

from e0_core import require_human_reference
from review_snapshot import SnapshotError, build_snapshot

EVALUATE_PATH = ROOT / "scripts" / "e0" / "evaluate_capture.py"
spec = importlib.util.spec_from_file_location("evaluate_capture_module", EVALUATE_PATH)
evaluate_capture_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(evaluate_capture_module)
gold_for_fixture = evaluate_capture_module.gold_for_fixture


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def init_git_repo(root: Path) -> None:
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test Reviewer")


class ReviewReadinessTests(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def approved_candidate(self):
        gold = self.load("experiments/e0/gold/candidates/capture-gold.ai-proposed.json")
        approved = dict(gold)
        approved["authorship_status"] = "HUMAN_APPROVED"
        return approved

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
        approved = self.approved_candidate()
        fixture_set = self.load("experiments/e0/fixtures/capture/pilot/fixtures.json")
        fixture = next(item for item in fixture_set["fixtures"] if item["family"] == "F2")
        pre = gold_for_fixture(approved, fixture, "pre")
        post = gold_for_fixture(approved, fixture, "post")
        self.assertNotEqual(pre[0]["condition"], post[0]["condition"])
        self.assertNotIn("substantive", pre[0]["condition"].lower())
        self.assertIn("substantive", post[0]["condition"].lower())

    def test_f5_e1_post_keeps_confirmation_rule(self):
        approved = self.approved_candidate()
        fixture_set = self.load("experiments/e0/fixtures/capture/evidence/fixtures.json")
        fixture = next(item for item in fixture_set["fixtures"] if item["fixture_id"] == "F5-E-1")
        post = gold_for_fixture(approved, fixture, "post")
        self.assertEqual({item["item_id"] for item in post}, {"f5_caution", "f5_confirmation_rule"})
        confirmation = next(item for item in post if item["item_id"] == "f5_confirmation_rule")
        self.assertEqual(confirmation["value"], "ASK_BEFORE_STRONG_COMPARISON")

    def test_f5_e2_post_preserves_unresolved_caution_without_e1_rule(self):
        approved = self.approved_candidate()
        fixture_set = self.load("experiments/e0/fixtures/capture/evidence/fixtures.json")
        fixture = next(item for item in fixture_set["fixtures"] if item["fixture_id"] == "F5-E-2")
        post = gold_for_fixture(approved, fixture, "post")
        self.assertEqual([item["item_id"] for item in post], ["f5_caution"])
        caution = post[0]
        self.assertEqual(caution["value"], "CLIENT_SENSITIVITY")
        self.assertEqual(caution["epistemic_status"], "CAUTION")
        self.assertEqual(caution["resolution_status"], "UNRESOLVED")
        self.assertEqual(caution["lifecycle_status"], "ACTIVE")
        self.assertIn("blanket ban", caution["rationale"].lower())
        self.assertNotIn("ASK_BEFORE_STRONG_COMPARISON", json.dumps(post))

    def test_f5_pilot_post_still_uses_family_default(self):
        approved = self.approved_candidate()
        fixture_set = self.load("experiments/e0/fixtures/capture/pilot/fixtures.json")
        fixture = next(item for item in fixture_set["fixtures"] if item["fixture_id"] == "F5-P-A")
        post = gold_for_fixture(approved, fixture, "post")
        self.assertEqual({item["item_id"] for item in post}, {"f5_caution", "f5_confirmation_rule"})

    def test_f8_remains_contested_after_clarification(self):
        gold = self.load("experiments/e0/gold/candidates/capture-gold.ai-proposed.json")
        post = gold["post_clarification_items_by_family"]["F8"]
        self.assertEqual({item["value"] for item in post}, {"APPROVED", "PENDING"})
        self.assertTrue(all(item["epistemic_status"] == "CONTESTED" for item in post))
        self.assertTrue(all(item["resolution_status"] == "CONTESTED" for item in post))

    def test_review_snapshot_is_bound_to_commit_tree_not_working_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            init_git_repo(root)
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            git(root, "add", "a.txt")
            git(root, "commit", "-q", "-m", "review baseline")
            reviewed_commit = git(root, "rev-parse", "HEAD")
            expected_hash = hashlib.sha256(b"alpha").hexdigest()

            first = build_snapshot(root, reviewed_commit, ["a.txt"])
            self.assertEqual(first["reviewed_commit"], reviewed_commit)
            self.assertEqual(first["artifacts"][0]["sha256"], expected_hash)
            self.assertEqual(len(first["reviewed_tree"]), 40)
            self.assertEqual(len(first["artifacts"][0]["git_blob_sha"]), 40)
            self.assertEqual(len(first["snapshot_sha256"]), 64)

            (root / "a.txt").write_text("beta", encoding="utf-8")
            second = build_snapshot(root, reviewed_commit, ["a.txt"])
            self.assertEqual(second, first)

    def test_review_snapshot_rejects_nonexistent_commit_shaped_string(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            init_git_repo(root)
            with self.assertRaises(SnapshotError):
                build_snapshot(root, "a" * 40, ["a.txt"])

    def test_review_snapshot_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            init_git_repo(root)
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            git(root, "add", "a.txt")
            git(root, "commit", "-q", "-m", "review baseline")
            reviewed_commit = git(root, "rev-parse", "HEAD")
            with self.assertRaises(SnapshotError):
                build_snapshot(root, reviewed_commit, ["../a.txt"])


if __name__ == "__main__":
    unittest.main()
