from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts/e0"


def load_preflight():
    spec = importlib.util.spec_from_file_location("preflight_pilot_r7", SCRIPTS / "preflight_pilot.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["preflight_pilot_r7"] = module
    spec.loader.exec_module(module)
    return module


preflight = load_preflight()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ActivationAuthorityGitBindingTests(unittest.TestCase):
    def test_activation_project_state_symlink_to_external_authority_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = temp / "repo"
            subprocess.run(["git", "clone", "-q", "--local", str(ROOT), str(repo)], check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)

            request = temp / "request.json"
            request.write_text("{}\n", encoding="utf-8")
            manifest = {
                "run_type": "PILOT",
                "label": "PILOT — NOT EVIDENCE",
                "owner_decision_id": "OD-PILOT-01",
                "owner_decision_status": "ADOPTED",
                "owner_github_login": "velantrian",
                "owner_adopted_at": "2026-08-23T00:00:00Z",
                "activation_policy": preflight.ACTIVATION_POLICY,
                "human_approval": {
                    "path": preflight.APPROVAL_PATH,
                    "sha256": sha256(repo / preflight.APPROVAL_PATH),
                },
                "approved_references": [
                    {
                        "path": "experiments/e0/gold/approved/capture-gold.v0.1.json",
                        "sha256": sha256(repo / "experiments/e0/gold/approved/capture-gold.v0.1.json"),
                    }
                ],
                "fixture_or_scenario_ids": ["F1-P-A"],
                "request_sha256": sha256(request),
                "execution_posture": "UNCONTROLLED_LOCAL_ADVISORY",
                "isolation": {
                    "isolation_enforcement": "NOT_ENFORCED",
                    "network_isolation": "NOT_ENFORCED",
                    "filesystem_isolation": "NOT_ENFORCED",
                    "process_isolation": "NOT_ENFORCED",
                },
                "limits": {"timeout_seconds": 2, "max_output_bytes": 4096, "max_runs": 1},
                "evidence_lock": {"status": "NOT_CREATED", "sha256": None},
                "model": {"provider": "example", "identifier": "model-v1", "settings": {}},
                "credentials": {"profile": "pilot-minimal", "scope": "inference-only"},
                "adapter_command": "python -c \"import json; print(json.dumps({'ok': True}))\"",
                "adapter_cwd": ".",
                "environment_allowlist": [],
                "output_destination": preflight.PILOT_OUTPUT_DESTINATION,
            }

            package_dir = repo / "experiments/e0/pilot/packages"
            package_dir.mkdir(parents=True, exist_ok=True)
            manifest_path = package_dir / "od-pilot-01.v0.1.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            subprocess.run(["git", "add", manifest_path.relative_to(repo)], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "package"], cwd=repo, check=True)

            base = git(repo, "rev-parse", "HEAD")
            base_tree = git(repo, "rev-parse", "HEAD^{tree}")
            manifest_sha = sha256(manifest_path)

            external_state = temp / "authority.json"
            state = json.loads((repo / "project-state.json").read_text(encoding="utf-8"))
            state["experiment_0_pilot_status"] = preflight.AUTHORIZED_PILOT_STATE
            state["experiment_0_pilot_authorization"] = {
                "status": preflight.AUTHORIZATION_PACKAGE_STATE,
                "authorization_id": "OD-PILOT-01-v0.1",
                "manifest_path": manifest_path.relative_to(repo).as_posix(),
                "manifest_sha256": manifest_sha,
                "authorization_base_commit": base,
                "authorization_base_tree": base_tree,
                "activation_policy": preflight.ACTIVATION_POLICY,
                "activation_paths": ["project-state.json"],
            }
            external_state.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            project_state = repo / "project-state.json"
            project_state.unlink()
            project_state.symlink_to(external_state)
            subprocess.run(["git", "add", "project-state.json"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "activate via external symlink"], cwd=repo, check=True)

            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertTrue(git(repo, "ls-tree", "HEAD", "--", "project-state.json").startswith("120000 blob "))

            with self.assertRaisesRegex(
                preflight.PreflightError,
                "project-state.json must be a regular non-executable Git blob",
            ):
                preflight.validate_canonical_authorization(
                    repo,
                    manifest=manifest,
                    manifest_path=manifest_path,
                    manifest_sha256=manifest_sha,
                )


if __name__ == "__main__":
    unittest.main()
