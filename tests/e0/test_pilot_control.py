from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preflight = load_module("preflight_pilot", ROOT / "scripts/e0/preflight_pilot.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_manifest() -> dict:
    return {
        "run_type": "PILOT",
        "label": "PILOT — NOT EVIDENCE",
        "owner_decision_id": "OD-PILOT-01",
        "owner_decision_status": "ADOPTED",
        "owner_github_login": "velantrian",
        "owner_adopted_at": "2026-08-22T10:00:00Z",
        "execution_head_commit": "a" * 40,
        "execution_tree": "b" * 40,
        "human_approval": {
            "path": preflight.APPROVAL_PATH,
            "sha256": sha256(ROOT / preflight.APPROVAL_PATH),
        },
        "approved_references": [
            {
                "path": "experiments/e0/gold/approved/capture-gold.v0.1.json",
                "sha256": sha256(ROOT / "experiments/e0/gold/approved/capture-gold.v0.1.json"),
            }
        ],
        "fixture_or_scenario_ids": ["F1-P-A", "T-PILOT-01"],
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
        "adapter_command": "python adapter.py",
        "output_destination": "artifacts/pilot/example",
    }


class PilotPreflightTests(unittest.TestCase):
    def test_valid_bounded_manifest_passes_without_git_runtime_check(self):
        messages = preflight.validate_manifest(valid_manifest(), ROOT, check_git=False)
        self.assertTrue(any(item.startswith("pilot_ids=") for item in messages))

    def test_draft_owner_decision_fails_closed(self):
        manifest = valid_manifest()
        manifest["owner_decision_status"] = "DRAFT — NOT ADOPTED"
        with self.assertRaisesRegex(preflight.PreflightError, "not authorized"):
            preflight.validate_manifest(manifest, ROOT, check_git=False)

    def test_evidence_fixture_is_forbidden(self):
        manifest = valid_manifest()
        manifest["fixture_or_scenario_ids"] = ["T-EVIDENCE-01"]
        with self.assertRaisesRegex(preflight.PreflightError, "Evidence fixture/scenario"):
            preflight.validate_manifest(manifest, ROOT, check_git=False)

    def test_secret_value_field_is_forbidden(self):
        manifest = valid_manifest()
        manifest["credentials"]["api_key"] = "do-not-store-this"
        with self.assertRaisesRegex(preflight.PreflightError, "secret-bearing field"):
            preflight.validate_manifest(manifest, ROOT, check_git=False)

    def test_uncontrolled_posture_cannot_claim_isolation(self):
        manifest = valid_manifest()
        manifest["isolation"]["network_isolation"] = "ENFORCED"
        with self.assertRaisesRegex(preflight.PreflightError, "NOT_ENFORCED"):
            preflight.validate_manifest(manifest, ROOT, check_git=False)

    def test_evidence_lock_must_remain_not_created(self):
        manifest = valid_manifest()
        manifest["evidence_lock"] = {"status": "CREATED", "sha256": "c" * 64}
        with self.assertRaisesRegex(preflight.PreflightError, "Evidence Lock NOT_CREATED"):
            preflight.validate_manifest(manifest, ROOT, check_git=False)


class RunAdapterTests(unittest.TestCase):
    def run_adapter(self, adapter_source: str, *, timeout: int = 2, cap: int = 4096, extra_env: dict[str, str] | None = None):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            adapter = temp / "adapter.py"
            adapter.write_text(adapter_source, encoding="utf-8")
            request = temp / "request.json"
            request.write_text('{"ping":"pong"}\n', encoding="utf-8")
            output = temp / "output.json"
            metrics = temp / "metrics.json"
            env = os.environ.copy()
            if extra_env:
                env.update(extra_env)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/e0/run_adapter.py"),
                    "--adapter-cmd", f"{sys.executable} {adapter}",
                    "--request", str(request),
                    "--output", str(output),
                    "--metrics-output", str(metrics),
                    "--cwd", str(temp),
                    "--timeout-seconds", str(timeout),
                    "--max-output-bytes", str(cap),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            return proc, output.read_text(encoding="utf-8") if output.exists() else None, json.loads(metrics.read_text(encoding="utf-8")) if metrics.exists() else None

    def test_adapter_success_records_limits_and_no_sandbox_claim(self):
        proc, output, metrics = self.run_adapter("import json,sys; print(json.dumps({'ok': True}))")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('"ok": true', output)
        self.assertFalse(metrics["execution_limits"]["sandbox"])
        self.assertEqual(metrics["execution_limits"]["max_output_bytes"], 4096)

    def test_adapter_timeout_fails(self):
        proc, output, metrics = self.run_adapter("import time; time.sleep(5); print('{}')", timeout=1)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("timeout", proc.stderr.lower())
        self.assertIsNone(output)
        self.assertIsNone(metrics)

    def test_adapter_output_cap_fails(self):
        proc, output, metrics = self.run_adapter("print('x' * 20000)", cap=1024)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("exceeded", proc.stderr.lower())
        self.assertIsNone(output)
        self.assertIsNone(metrics)

    def test_unlisted_environment_is_not_inherited(self):
        source = "import json,os; print(json.dumps({'leaked': os.getenv('VELANTRIM_TEST_SECRET')}))"
        proc, output, _ = self.run_adapter(source, extra_env={"VELANTRIM_TEST_SECRET": "secret-value"})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('"leaked": null', output)


if __name__ == "__main__":
    unittest.main()
