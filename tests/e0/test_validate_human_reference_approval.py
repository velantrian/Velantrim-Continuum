from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

from validate_human_reference_approval import APPROVAL_FORMAT, ValidationError, validate


def write_json(root: Path, relative: str, payload: dict) -> tuple[str, str]:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return relative, hashlib.sha256(path.read_bytes()).hexdigest()


class ApprovalValidatorTests(unittest.TestCase):
    def build_valid_case(self, root: Path) -> dict:
        capture_candidate_path, capture_candidate_hash = write_json(
            root,
            "experiments/e0/gold/candidates/capture-gold.ai-proposed.json",
            {"gold_version": "0.2-candidate", "authorship_status": "AI_PROPOSED_DRAFT"},
        )
        oracle_candidate_path, oracle_candidate_hash = write_json(
            root,
            "experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json",
            {"oracle_version": "0.1-candidate", "authorship_status": "AI_PROPOSED_DRAFT"},
        )
        capture_approved_path, capture_approved_hash = write_json(
            root,
            "experiments/e0/gold/approved/capture-gold.v0.1.json",
            {"gold_version": "0.1", "authorship_status": "HUMAN_APPROVED"},
        )
        oracle_approved_path, oracle_approved_hash = write_json(
            root,
            "experiments/e0/oracle/approved/transfer-oracle.v0.1.json",
            {"oracle_version": "0.1", "authorship_status": "HUMAN_APPROVED"},
        )
        decision_ids = (
            "F1", "F2_PRE", "F2_POST", "F3", "F4", "F5", "F6", "F7", "F8",
            "T-PILOT-01", "T-EVIDENCE-01", "T-EVIDENCE-02", "AUTHORITY_AMBIGUITY_PROVENANCE",
        )
        return {
            "approval_format": APPROVAL_FORMAT,
            "status": "HUMAN_APPROVED",
            "reviewer": {"name": "Named Experimenter", "role": "Owner / Human Experimenter"},
            "approved_at": "2026-08-16T15:30:00Z",
            "reviewed_repository_commit": "a" * 40,
            "issue_url": "https://github.com/velantrian/Velantrim-Continuum/issues/9",
            "decisions": {item: {"decision": "ACCEPT", "note": f"reviewed {item}"} for item in decision_ids},
            "open_semantic_revisions": [],
            "evidence_lock": {"status": "NOT_CREATED", "sha256": None},
            "references": {
                "capture_gold": {
                    "candidate_path": capture_candidate_path,
                    "candidate_sha256": capture_candidate_hash,
                    "approved_path": capture_approved_path,
                    "approved_sha256": capture_approved_hash,
                    "approved_version": "0.1",
                },
                "transfer_oracle": {
                    "candidate_path": oracle_candidate_path,
                    "candidate_sha256": oracle_candidate_hash,
                    "approved_path": oracle_approved_path,
                    "approved_sha256": oracle_approved_hash,
                    "approved_version": "0.1",
                },
            },
        }

    def test_valid_binding_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            messages = validate(self.build_valid_case(Path(temp)), Path(temp), 9)
            self.assertEqual(len(messages), 4)
            self.assertTrue(all("sha256=" in message for message in messages))

    def test_non_accept_decision_blocks_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            approval = self.build_valid_case(Path(temp))
            approval["decisions"]["F8"]["decision"] = "REVISE"
            with self.assertRaisesRegex(ValidationError, "must be ACCEPT"):
                validate(approval, Path(temp), 9)

    def test_open_semantic_revision_blocks_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            approval = self.build_valid_case(Path(temp))
            approval["open_semantic_revisions"] = ["F8"]
            with self.assertRaisesRegex(ValidationError, "must be empty"):
                validate(approval, Path(temp), 9)

    def test_candidate_must_remain_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            path = root / approval["references"]["capture_gold"]["candidate_path"]
            path.write_text(json.dumps({"gold_version": "0.2-candidate", "authorship_status": "HUMAN_APPROVED"}), encoding="utf-8")
            approval["references"]["capture_gold"]["candidate_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValidationError, "must remain AI_PROPOSED_DRAFT"):
                validate(approval, root, 9)

    def test_approved_hash_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            approval = self.build_valid_case(Path(temp))
            approval["references"]["capture_gold"]["approved_sha256"] = "b" * 64
            with self.assertRaisesRegex(ValidationError, "does not match"):
                validate(approval, Path(temp), 9)

    def test_evidence_lock_cannot_be_declared_in_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            approval = self.build_valid_case(Path(temp))
            approval["evidence_lock"] = {"status": "EVIDENCE_READY", "sha256": "b" * 64}
            with self.assertRaisesRegex(ValidationError, "NOT_CREATED"):
                validate(approval, Path(temp), 9)

    def test_wrong_issue_host_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            approval = self.build_valid_case(Path(temp))
            approval["issue_url"] = "https://example.com/velantrian/Velantrim-Continuum/issues/9"
            with self.assertRaisesRegex(ValidationError, "canonical GitHub URL"):
                validate(approval, Path(temp), 9)

    def test_candidate_correction_path_does_not_require_approval_record(self) -> None:
        # Regression marker for workflow design: candidate edits are intentionally
        # excluded from the dedicated approval-binding workflow. Their safety is
        # covered by the normal Experiment 0 harness and Issue #9 review cycle.
        workflow = (ROOT / ".github" / "workflows" / "human-reference-approval-gate.yml").read_text(encoding="utf-8")
        self.assertNotIn('experiments/e0/gold/candidates/**', workflow)
        self.assertNotIn('experiments/e0/oracle/candidates/**', workflow)


if __name__ == "__main__":
    unittest.main()
