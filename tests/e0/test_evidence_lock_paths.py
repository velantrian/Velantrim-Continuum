from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "scripts" / "e0"))

from e0_core import sha256_file, verify_lock


def approved_lock(path: str, sha256: str) -> dict:
    return {
        "status": "EVIDENCE_READY",
        "human_gold_approval": {"status": "HUMAN_APPROVED"},
        "artifacts": [{"path": path, "sha256": sha256}],
    }


def schema_shaped_lock(artifacts: list[dict]) -> dict:
    versioned_hash = {"version": "0.1", "sha256": "0" * 64}
    return {
        "lock_version": "0.1",
        "status": "EVIDENCE_READY",
        "protocol": dict(versioned_hash),
        "schemas": [dict(versioned_hash)],
        "evidence_fixtures": dict(versioned_hash),
        "gold_oracle": dict(versioned_hash),
        "evaluator": dict(versioned_hash),
        "run_config": dict(versioned_hash),
        "prompts": [],
        "randomization": dict(versioned_hash),
        "clarification_policy": dict(versioned_hash),
        "generator_config": dict(versioned_hash),
        "supersession_rule": dict(versioned_hash),
        "human_gold_approval": {
            "status": "HUMAN_APPROVED",
            "approved_by": "test-owner",
            "approved_at": "2026-09-09T00:00:00Z",
        },
        "artifacts": artifacts,
    }


def run_lock_checker(lock: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temp:
        lock_path = Path(temp) / "lock.json"
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "e0" / "check_evidence_lock.py"),
                "--repo-root",
                str(ROOT),
                "--lock",
                str(lock_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )


class EvidenceLockPathTests(unittest.TestCase):
    def test_repository_relative_artifact_with_matching_hash_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / "locked" / "artifact.txt"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("bound bytes", encoding="utf-8")
            self.assertEqual(verify_lock(approved_lock("locked/artifact.txt", sha256_file(artifact)), root), [])

    def test_absolute_external_path_is_rejected_even_with_matching_hash(self) -> None:
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as outside:
            root = Path(repo)
            external = Path(outside) / "artifact.txt"
            external.write_text("external bytes", encoding="utf-8")
            errors = verify_lock(approved_lock(str(external), sha256_file(external)), root)
            self.assertIn(f"invalid locked artifact path: {external}", errors)
            self.assertFalse(any(error.startswith("hash mismatch") for error in errors))

    def test_parent_traversal_is_rejected_even_when_target_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent / "repo"
            root.mkdir()
            external = parent / "outside.txt"
            external.write_text("outside", encoding="utf-8")
            errors = verify_lock(approved_lock("../outside.txt", sha256_file(external)), root)
            self.assertIn("invalid locked artifact path: ../outside.txt", errors)

    def test_symlink_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent / "repo"
            root.mkdir()
            external = parent / "outside.txt"
            external.write_text("outside", encoding="utf-8")
            link = root / "escape.txt"
            try:
                link.symlink_to(external)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable on this platform")
            errors = verify_lock(approved_lock("escape.txt", sha256_file(external)), root)
            self.assertIn("invalid locked artifact path: escape.txt", errors)

    def test_non_normalized_and_backslash_paths_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for bad in ("a//b.txt", "./a.txt", "a\\b.txt", ""):
                with self.subTest(path=bad):
                    errors = verify_lock(approved_lock(bad, "0" * 64), root)
                    self.assertIn(f"invalid locked artifact path: {bad}", errors)

    def test_duplicate_locked_artifact_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / "a.txt"
            artifact.write_text("same", encoding="utf-8")
            digest = sha256_file(artifact)
            lock = {
                "status": "EVIDENCE_READY",
                "human_gold_approval": {"status": "HUMAN_APPROVED"},
                "artifacts": [
                    {"path": "a.txt", "sha256": digest},
                    {"path": "a.txt", "sha256": digest},
                ],
            }
            errors = verify_lock(lock, root)
            self.assertIn("duplicate locked artifact path: a.txt", errors)

    def test_cli_rejects_missing_required_evidence_lock_fields(self) -> None:
        proc = run_lock_checker(
            {
                "status": "EVIDENCE_READY",
                "human_gold_approval": {"status": "HUMAN_APPROVED"},
            }
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("schema violation", proc.stdout)
        self.assertIn("'artifacts' is a required property", proc.stdout)
        self.assertNotIn("EVIDENCE LOCK: VALID", proc.stdout)

    def test_cli_rejects_empty_artifacts(self) -> None:
        proc = run_lock_checker(schema_shaped_lock([]))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("$.artifacts: schema violation", proc.stdout)
        self.assertNotIn("EVIDENCE LOCK: VALID", proc.stdout)

    def test_cli_accepts_schema_valid_lock_with_matching_artifact(self) -> None:
        relative = "experiments/e0/schema/evidence-lock.schema.json"
        digest = sha256_file(ROOT / relative)
        proc = run_lock_checker(schema_shaped_lock([{"path": relative, "sha256": digest}]))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("EVIDENCE LOCK: VALID", proc.stdout)


if __name__ == "__main__":
    unittest.main()
