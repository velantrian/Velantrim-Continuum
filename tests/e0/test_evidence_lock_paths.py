from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
