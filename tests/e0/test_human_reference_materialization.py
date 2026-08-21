from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPROVAL_PATH = ROOT / "experiments/e0/approval/human-reference-approval.v0.2.json"
CAPTURE_CANDIDATE = ROOT / "experiments/e0/gold/candidates/capture-gold.ai-proposed.json"
CAPTURE_APPROVED = ROOT / "experiments/e0/gold/approved/capture-gold.v0.1.json"
ORACLE_CANDIDATE = ROOT / "experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json"
ORACLE_APPROVED = ROOT / "experiments/e0/oracle/approved/transfer-oracle.v0.1.json"
STATE_PATH = ROOT / "project-state.json"

EXPECTED_DECISIONS = {
    "F1", "F2_PRE", "F2_POST", "F3", "F4", "F5_PRE", "F5_POST",
    "F6", "F7", "F8_PRE", "F8_POST", "T-PILOT-01", "T-EVIDENCE-01",
    "T-EVIDENCE-02",
}
EXPECTED_REVIEW_BINDINGS = {
    "experiments/e0/review/ISSUE_9_HUMAN_REVIEW_PROTOCOL.md": {
        "git_mode": "100644", "git_blob_sha": "57c2ff6c3246d1f572b83cf3594735eedd92ba48",
        "sha256": "2d703ae4f029438c54cae3a0d1f38cacef8605fbc50ec3742c246744fefc5b06",
    },
    "docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md": {
        "git_mode": "100644", "git_blob_sha": "82a11e13e44fc44e86e3327a2a7a69509571118c",
        "sha256": "d98a049eb5ff24c0be68c47d59e0a04a5418a62ae63886c5a7be604c9a3243e9",
    },
    "experiments/e0/fixtures/capture/pilot/fixtures.json": {
        "git_mode": "100644", "git_blob_sha": "d66401bd665fd63f42780940f44fc999c03a5054",
        "sha256": "f07a028f7331a02d54add8f360ce11b7b87666db5687c0bf33295338ade5d17c",
    },
    "experiments/e0/fixtures/capture/evidence/fixtures.json": {
        "git_mode": "100644", "git_blob_sha": "8c60614a07cbef245d840dce8d45a32105ecc253",
        "sha256": "f97e2d31917b3f556a74851c269057d97f0e923fd03a873ecca2884487a11ad9",
    },
    "experiments/e0/fixtures/transfer/scenarios.json": {
        "git_mode": "100644", "git_blob_sha": "24c78e2e9eee533670733bba080aa6096ddd2f32",
        "sha256": "8afea55d5c92b67b50ad11f12156fb2626f2a582bd5d7898bd1c282482f79b9e",
    },
    "experiments/e0/gold/candidates/capture-gold.ai-proposed.json": {
        "git_mode": "100644", "git_blob_sha": "e77f874b2e611548747e72487b2d2274df270d0e",
        "sha256": "7773aac446c7386847aa68bfb7b66556840458438e9ac9bfa8de046a4f264eee",
    },
    "experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json": {
        "git_mode": "100644", "git_blob_sha": "3e9b79ccc48408e4857de19415c6d7a1e6ccf588",
        "sha256": "3da790f8052d03d6faa7eeebf803c3f7e90835a74d3b0c73aee57bc55a581c71",
    },
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_payload(document: dict, version_key: str) -> dict:
    value = copy.deepcopy(document)
    for key in (version_key, "authorship_status", "human_approval_required", "warning"):
        value.pop(key, None)
    return value


class HumanReferenceMaterializationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.approval = load(APPROVAL_PATH)
        cls.state = load(STATE_PATH)

    def test_exactly_fourteen_human_accept_decisions(self) -> None:
        decisions = self.approval["decisions"]
        self.assertEqual(set(decisions), EXPECTED_DECISIONS)
        self.assertEqual(len(decisions), 14)
        self.assertTrue(all(item["decision"] == "ACCEPT" for item in decisions.values()))
        self.assertNotIn("AUTHORITY_AMBIGUITY_PROVENANCE", decisions)
        self.assertNotEqual("F5_PRE", "F5_POST")
        self.assertNotEqual("F8_PRE", "F8_POST")

    def test_review_binding_records_exact_reviewed_git_identity(self) -> None:
        self.assertEqual(self.approval["reviewed_paths"], EXPECTED_REVIEW_BINDINGS)
        self.assertEqual(
            self.approval["reviewed_repository_commit"],
            "dbda5c364f5bc76eb033f90031ce03bf3f4f29e9",
        )
        self.assertEqual(
            self.approval["review_snapshot"],
            {
                "snapshot_version": "0.4",
                "snapshot_sha256": "e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4",
                "reviewed_tree": "03be5376d592ec9c12299627a6ec0507548363b8",
            },
        )

    def test_candidate_and_approved_hashes_are_bound_and_locations_distinct(self) -> None:
        capture = self.approval["references"]["capture_gold"]
        oracle = self.approval["references"]["transfer_oracle"]
        self.assertEqual(sha256(CAPTURE_CANDIDATE), capture["candidate_sha256"])
        self.assertEqual(sha256(CAPTURE_APPROVED), capture["approved_sha256"])
        self.assertEqual(sha256(ORACLE_CANDIDATE), oracle["candidate_sha256"])
        self.assertEqual(sha256(ORACLE_APPROVED), oracle["approved_sha256"])
        self.assertIn("/candidates/", capture["candidate_path"])
        self.assertIn("/approved/", capture["approved_path"])
        self.assertIn("/candidates/", oracle["candidate_path"])
        self.assertIn("/approved/", oracle["approved_path"])

    def test_materialization_changes_authority_metadata_not_reference_semantics(self) -> None:
        capture_candidate = load(CAPTURE_CANDIDATE)
        capture_approved = load(CAPTURE_APPROVED)
        oracle_candidate = load(ORACLE_CANDIDATE)
        oracle_approved = load(ORACLE_APPROVED)
        self.assertEqual(capture_candidate["authorship_status"], "AI_PROPOSED_DRAFT")
        self.assertEqual(oracle_candidate["authorship_status"], "AI_PROPOSED_DRAFT")
        self.assertEqual(capture_approved["authorship_status"], "HUMAN_APPROVED")
        self.assertEqual(oracle_approved["authorship_status"], "HUMAN_APPROVED")
        self.assertEqual(
            semantic_payload(capture_candidate, "gold_version"),
            semantic_payload(capture_approved, "gold_version"),
        )
        self.assertEqual(
            semantic_payload(oracle_candidate, "oracle_version"),
            semantic_payload(oracle_approved, "oracle_version"),
        )

    def test_approval_closes_only_human_reference_gate(self) -> None:
        self.assertEqual(self.approval["gate_status"], "HUMAN_REFERENCE_APPROVED")
        boundary = self.approval["boundary"]
        self.assertEqual(boundary["pilot"], "NOT_AUTHORIZED")
        self.assertEqual(boundary["evidence_lock"], "NOT_CREATED")
        self.assertEqual(boundary["e0_c_evidence"], "NOT_AUTHORIZED / NOT_RUN")
        self.assertEqual(boundary["e0_t_evidence"], "NOT_AUTHORIZED / NOT_RUN")
        self.assertEqual(boundary["production_runtime"], "NO")
        self.assertEqual(boundary["production_architecture"], "NO")
        self.assertEqual(boundary["event_sourcing_requirement"], "NO")
        self.assertEqual(boundary["ecosystem_integration"], "NO")
        self.assertEqual(self.approval["evidence_lock"], {"status": "NOT_CREATED", "sha256": None})

    def test_machine_state_preserves_authority_boundaries(self) -> None:
        review = self.state["human_reference_review"]
        self.assertEqual(review["status"], "HUMAN_APPROVED")
        self.assertEqual(review["gate_status"], "CLOSED")
        self.assertEqual(review["required_decisions"], 14)
        self.assertEqual(review["accepted_decisions"], 14)
        self.assertEqual(self.state["experiment_0_pilot_status"], "NOT_AUTHORIZED")
        self.assertFalse(self.state["experiment_0_evidence_ready"])
        self.assertIsNone(self.state["experiment_0_evidence_lock_sha"])
        self.assertFalse(self.state["e0c_started"])
        self.assertFalse(self.state["e0t_started"])
        self.assertFalse(self.state["architecture_frozen"])
        self.assertFalse(self.state["production_runtime_authorized"])
        self.assertFalse(self.state["ecosystem_integration_authorized"])
        self.assertFalse(self.state["event_sourcing_required"])


if __name__ == "__main__":
    unittest.main()
