from __future__ import annotations

import hashlib
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts/e0"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

spec = importlib.util.spec_from_file_location("preflight_pilot_arm_binding", SCRIPTS / "preflight_pilot.py")
assert spec and spec.loader
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference(path: str) -> dict[str, str]:
    return {"path": path, "sha256": sha256(ROOT / path)}


def manifest(ids: list[str], refs: list[str]) -> dict:
    return {
        "run_type": "PILOT",
        "label": "PILOT — NOT EVIDENCE",
        "owner_decision_id": "OD-PILOT-01",
        "owner_decision_status": "ADOPTED",
        "owner_github_login": "velantrian",
        "owner_adopted_at": "2026-08-23T00:00:00Z",
        "activation_policy": preflight.ACTIVATION_POLICY,
        "human_approval": {"path": preflight.APPROVAL_PATH, "sha256": sha256(ROOT / preflight.APPROVAL_PATH)},
        "approved_references": [reference(path) for path in refs],
        "fixture_or_scenario_ids": ids,
        "request_sha256": "d" * 64,
        "execution_posture": "UNCONTROLLED_LOCAL_ADVISORY",
        "isolation": {"isolation_enforcement": "NOT_ENFORCED", "network_isolation": "NOT_ENFORCED", "filesystem_isolation": "NOT_ENFORCED", "process_isolation": "NOT_ENFORCED"},
        "limits": {"timeout_seconds": 2, "max_output_bytes": 4096, "max_runs": 1},
        "evidence_lock": {"status": "NOT_CREATED", "sha256": None},
        "model": {"provider": "example", "identifier": "model-v1", "settings": {}},
        "credentials": {"profile": "pilot-minimal", "scope": "inference-only"},
        "adapter_command": "python -c \"print('{}')\"",
        "adapter_cwd": ".",
        "environment_allowlist": [],
        "output_destination": preflight.PILOT_OUTPUT_DESTINATION,
    }


def validate(value: dict):
    return preflight.validate_manifest(value, ROOT, check_git=False, check_authority_state=False)


class PilotArmReferenceBindingTests(unittest.TestCase):
    def test_capture_requires_capture_gold(self):
        with self.assertRaisesRegex(preflight.PreflightError, "Capture Pilot requires exact approved Capture Gold"):
            validate(manifest(["F1-P-A"], [preflight.TRANSFER_ORACLE_PATH]))

    def test_transfer_requires_transfer_oracle(self):
        with self.assertRaisesRegex(preflight.PreflightError, "Transfer Pilot requires exact approved Transfer Oracle"):
            validate(manifest(["T-PILOT-01"], [preflight.CAPTURE_GOLD_PATH]))

    def test_mixed_requires_both(self):
        with self.assertRaisesRegex(preflight.PreflightError, "Transfer Pilot requires exact approved Transfer Oracle"):
            validate(manifest(["F1-P-A", "T-PILOT-01"], [preflight.CAPTURE_GOLD_PATH]))

    def test_mixed_with_both_passes(self):
        messages = validate(manifest(["F1-P-A", "T-PILOT-01"], [preflight.CAPTURE_GOLD_PATH, preflight.TRANSFER_ORACLE_PATH]))
        self.assertTrue(any(item.startswith("pilot_ids=") for item in messages))


if __name__ == "__main__":
    unittest.main()
