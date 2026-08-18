from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

from review_snapshot import DEFAULT_PATHS, SNAPSHOT_VERSION, build_snapshot
from validate_human_reference_approval import APPROVAL_FORMAT, EXPECTED_DECISIONS, ValidationError, validate


def write_text(root: Path, relative: str, text: str) -> tuple[str, str]:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return relative, hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(root: Path, relative: str, payload: dict) -> tuple[str, str]:
    return write_text(root, relative, json.dumps(payload, sort_keys=True))


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


class ApprovalValidatorTests(unittest.TestCase):
    def create_review_inputs(self, root: Path, *, capture_status: str = "AI_PROPOSED_DRAFT") -> tuple[str, str, str, str]:
        write_text(root, "experiments/e0/review/ISSUE_9_HUMAN_REVIEW_PROTOCOL.md", "14-row protocol baseline\n")
        write_text(root, "docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md", "prereg baseline\n")
        write_json(root, "experiments/e0/fixtures/capture/pilot/fixtures.json", {"partition": "PILOT", "fixtures": []})
        write_json(root, "experiments/e0/fixtures/capture/evidence/fixtures.json", {"partition": "EVIDENCE", "fixtures": []})
        write_json(root, "experiments/e0/fixtures/transfer/scenarios.json", {"scenarios": []})
        capture_path, capture_hash = write_json(
            root,
            "experiments/e0/gold/candidates/capture-gold.ai-proposed.json",
            {"gold_version": "0.3-candidate", "authorship_status": capture_status},
        )
        oracle_path, oracle_hash = write_json(
            root,
            "experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json",
            {"oracle_version": "0.1-candidate", "authorship_status": "AI_PROPOSED_DRAFT"},
        )
        return capture_path, capture_hash, oracle_path, oracle_hash

    def commit_review_inputs(self, root: Path) -> str:
        git(root, "add", ".")
        git(root, "commit", "-q", "-m", "review inputs")
        return git(root, "rev-parse", "HEAD")

    def build_valid_case(self, root: Path) -> dict:
        init_git_repo(root)
        capture_candidate_path, capture_candidate_hash, oracle_candidate_path, oracle_candidate_hash = self.create_review_inputs(root)
        reviewed_commit = self.commit_review_inputs(root)
        snapshot = build_snapshot(root, reviewed_commit, DEFAULT_PATHS)

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
        return {
            "approval_format": APPROVAL_FORMAT,
            "status": "HUMAN_APPROVED",
            "reviewer": {"name": "Named Experimenter", "role": "Owner / Human Experimenter"},
            "approved_at": "2026-08-16T15:30:00Z",
            "reviewed_repository_commit": reviewed_commit,
            "review_snapshot": {
                "snapshot_version": snapshot["snapshot_version"],
                "snapshot_sha256": snapshot["snapshot_sha256"],
                "reviewed_tree": snapshot["reviewed_tree"],
            },
            "issue_url": "https://github.com/velantrian/Velantrim-Continuum/issues/9",
            "decisions": {item: {"decision": "ACCEPT", "note": f"reviewed {item}"} for item in EXPECTED_DECISIONS},
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

    def test_snapshot_scope_binds_review_protocol(self) -> None:
        self.assertEqual(SNAPSHOT_VERSION, "0.3")
        self.assertEqual(len(DEFAULT_PATHS), 7)
        self.assertIn("experiments/e0/review/ISSUE_9_HUMAN_REVIEW_PROTOCOL.md", DEFAULT_PATHS)

    def test_canonical_human_decision_ids_are_exactly_fourteen(self) -> None:
        self.assertEqual(len(EXPECTED_DECISIONS), 14)
        self.assertIn("F5_PRE", EXPECTED_DECISIONS)
        self.assertIn("F5_POST", EXPECTED_DECISIONS)
        self.assertIn("F8_PRE", EXPECTED_DECISIONS)
        self.assertIn("F8_POST", EXPECTED_DECISIONS)
        self.assertNotIn("F5", EXPECTED_DECISIONS)
        self.assertNotIn("F8", EXPECTED_DECISIONS)
        self.assertNotIn("AUTHORITY_AMBIGUITY_PROVENANCE", EXPECTED_DECISIONS)

    def test_valid_binding_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            messages = validate(self.build_valid_case(root), root, 9)
            self.assertEqual(len(messages), 7)
            self.assertTrue(any(message.startswith("reviewed_commit=") for message in messages))
            self.assertTrue(any(message.startswith("review_snapshot_sha256=") for message in messages))

    def test_nonexistent_commit_shaped_string_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["reviewed_repository_commit"] = "a" * 40
            with self.assertRaisesRegex(ValidationError, "commit/tree binding invalid"):
                validate(approval, root, 9)

    def test_snapshot_hash_must_match_reviewed_commit_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["review_snapshot"]["snapshot_sha256"] = "b" * 64
            with self.assertRaisesRegex(ValidationError, "does not match exact bytes"):
                validate(approval, root, 9)

    def test_reviewed_tree_must_match_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["review_snapshot"]["reviewed_tree"] = "b" * 40
            with self.assertRaisesRegex(ValidationError, "does not match reviewed_repository_commit tree"):
                validate(approval, root, 9)

    def test_working_tree_candidate_drift_is_rejected_even_with_updated_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            path = root / approval["references"]["capture_gold"]["candidate_path"]
            path.write_text(json.dumps({"gold_version": "0.3-candidate", "authorship_status": "AI_PROPOSED_DRAFT", "drift": True}), encoding="utf-8")
            approval["references"]["capture_gold"]["candidate_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValidationError, "current review input differs from reviewed-commit bytes"):
                validate(approval, root, 9)

    def test_non_candidate_review_input_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            prereg = root / "docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md"
            prereg.write_text("prereg changed after review\n", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "current review input differs from reviewed-commit bytes"):
                validate(approval, root, 9)

    def test_review_protocol_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            protocol = root / "experiments/e0/review/ISSUE_9_HUMAN_REVIEW_PROTOCOL.md"
            protocol.write_text("changed decision rows after review\n", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "current review input differs from reviewed-commit bytes"):
                validate(approval, root, 9)

    def test_candidate_must_remain_draft_in_reviewed_commit_and_current_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            init_git_repo(root)
            capture_path, capture_hash, oracle_path, oracle_hash = self.create_review_inputs(root, capture_status="HUMAN_APPROVED")
            reviewed_commit = self.commit_review_inputs(root)
            snapshot = build_snapshot(root, reviewed_commit, DEFAULT_PATHS)
            approved_capture_path, approved_capture_hash = write_json(root, "experiments/e0/gold/approved/capture-gold.v0.1.json", {"gold_version": "0.1", "authorship_status": "HUMAN_APPROVED"})
            approved_oracle_path, approved_oracle_hash = write_json(root, "experiments/e0/oracle/approved/transfer-oracle.v0.1.json", {"oracle_version": "0.1", "authorship_status": "HUMAN_APPROVED"})
            approval = {
                "approval_format": APPROVAL_FORMAT,
                "status": "HUMAN_APPROVED",
                "reviewer": {"name": "Named Experimenter", "role": "Owner"},
                "approved_at": "2026-08-16T15:30:00Z",
                "reviewed_repository_commit": reviewed_commit,
                "review_snapshot": {"snapshot_version": snapshot["snapshot_version"], "snapshot_sha256": snapshot["snapshot_sha256"], "reviewed_tree": snapshot["reviewed_tree"]},
                "issue_url": "https://github.com/velantrian/Velantrim-Continuum/issues/9",
                "decisions": {item: {"decision": "ACCEPT", "note": "reviewed"} for item in EXPECTED_DECISIONS},
                "open_semantic_revisions": [],
                "evidence_lock": {"status": "NOT_CREATED", "sha256": None},
                "references": {
                    "capture_gold": {"candidate_path": capture_path, "candidate_sha256": capture_hash, "approved_path": approved_capture_path, "approved_sha256": approved_capture_hash, "approved_version": "0.1"},
                    "transfer_oracle": {"candidate_path": oracle_path, "candidate_sha256": oracle_hash, "approved_path": approved_oracle_path, "approved_sha256": approved_oracle_hash, "approved_version": "0.1"},
                },
            }
            with self.assertRaisesRegex(ValidationError, "must remain AI_PROPOSED_DRAFT"):
                validate(approval, root, 9)

    def test_machine_only_assertion_cannot_occupy_human_decision_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["decisions"]["AUTHORITY_AMBIGUITY_PROVENANCE"] = {"decision": "ACCEPT", "note": "machine-only"}
            with self.assertRaisesRegex(ValidationError, "14 canonical human review decision IDs"):
                validate(approval, root, 9)

    def test_non_accept_decision_blocks_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["decisions"]["F8_POST"]["decision"] = "REVISE"
            with self.assertRaisesRegex(ValidationError, "must be ACCEPT"):
                validate(approval, root, 9)

    def test_approved_hash_mismatch_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["references"]["capture_gold"]["approved_sha256"] = "b" * 64
            with self.assertRaisesRegex(ValidationError, "does not match"):
                validate(approval, root, 9)

    def test_evidence_lock_cannot_be_declared_in_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["evidence_lock"] = {"status": "EVIDENCE_READY", "sha256": "b" * 64}
            with self.assertRaisesRegex(ValidationError, "NOT_CREATED"):
                validate(approval, root, 9)

    def test_wrong_issue_host_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            approval = self.build_valid_case(root)
            approval["issue_url"] = "https://example.com/velantrian/Velantrim-Continuum/issues/9"
            with self.assertRaisesRegex(ValidationError, "canonical GitHub URL"):
                validate(approval, root, 9)

    def test_candidate_correction_path_does_not_require_approval_record(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "human-reference-approval-gate.yml").read_text(encoding="utf-8")
        self.assertNotIn('experiments/e0/gold/candidates/**', workflow)
        self.assertNotIn('experiments/e0/oracle/candidates/**', workflow)


if __name__ == "__main__":
    unittest.main()
