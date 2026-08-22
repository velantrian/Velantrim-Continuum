from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts/e0"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


preflight = load_module("preflight_pilot", SCRIPTS / "preflight_pilot.py")
run_adapter = load_module("run_adapter", SCRIPTS / "run_adapter.py")
execute_pilot = load_module("execute_pilot", SCRIPTS / "execute_pilot.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_manifest() -> dict:
    return {
        "run_type": "PILOT",
        "label": "PILOT — NOT EVIDENCE",
        "owner_decision_id": "OD-PILOT-01",
        "owner_decision_status": "ADOPTED",
        "owner_github_login": "velantrian",
        "owner_adopted_at": "2026-08-23T00:00:00Z",
        "authorization_base_commit": "a" * 40,
        "authorization_base_tree": "b" * 40,
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
        "request_sha256": "d" * 64,
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
        "adapter_cwd": ".",
        "environment_allowlist": [],
        "output_destination": preflight.PILOT_OUTPUT_DESTINATION,
    }


def validate_structure(manifest: dict):
    return preflight.validate_manifest(manifest, ROOT, check_git=False, check_authority_state=False)


class PilotPreflightTests(unittest.TestCase):
    def test_valid_bounded_manifest_passes_structural_validation(self):
        messages = validate_structure(valid_manifest())
        self.assertTrue(any(item.startswith("pilot_ids=") for item in messages))

    def test_canonical_project_state_blocks_pilot_before_owner_authorization(self):
        with self.assertRaisesRegex(preflight.PreflightError, "canonical project state does not authorize Pilot"):
            preflight.validate_manifest(valid_manifest(), ROOT, check_git=False, check_authority_state=True)

    def test_future_authorized_state_requires_exact_manifest_binding(self):
        manifest = valid_manifest()
        pilot_root = ROOT / "experiments/e0/pilot"
        with tempfile.TemporaryDirectory(dir=pilot_root) as temp_dir:
            manifest_path = Path(temp_dir) / "pilot.json"
            payload = json.dumps(manifest).encode("utf-8")
            manifest_path.write_bytes(payload)
            fake_state = {
                "experiment_0_pilot_status": preflight.AUTHORIZED_PILOT_STATE,
                "experiment_0_pilot_authorization": {
                    "status": preflight.AUTHORIZATION_PACKAGE_STATE,
                    "authorization_id": "AUTH-1",
                    "manifest_path": manifest_path.relative_to(ROOT).as_posix(),
                    "manifest_sha256": "0" * 64,
                    "authorization_base_commit": manifest["authorization_base_commit"],
                    "authorization_base_tree": manifest["authorization_base_tree"],
                },
                "experiment_0_evidence_lock_sha": None,
                "experiment_0_evidence_ready": False,
                "e0c_started": False,
                "e0t_started": False,
            }
            with mock.patch.object(preflight, "load_json", return_value=fake_state):
                with self.assertRaisesRegex(preflight.PreflightError, "does not match canonical owner-approved package binding"):
                    preflight.validate_canonical_authorization(
                        ROOT,
                        manifest=manifest,
                        manifest_path=manifest_path,
                        manifest_sha256=hashlib.sha256(payload).hexdigest(),
                    )

    def test_draft_owner_decision_fails_closed(self):
        manifest = valid_manifest()
        manifest["owner_decision_status"] = "DRAFT — NOT ADOPTED"
        with self.assertRaisesRegex(preflight.PreflightError, "not authorized"):
            validate_structure(manifest)

    def test_evidence_fixture_is_forbidden(self):
        manifest = valid_manifest()
        manifest["fixture_or_scenario_ids"] = ["T-EVIDENCE-01"]
        with self.assertRaisesRegex(preflight.PreflightError, "Evidence fixture/scenario"):
            validate_structure(manifest)

    def test_secret_value_field_is_forbidden(self):
        manifest = valid_manifest()
        manifest["credentials"]["api_key"] = "do-not-store-this"
        with self.assertRaisesRegex(preflight.PreflightError, "secret-bearing field"):
            validate_structure(manifest)

    def test_uncontrolled_posture_cannot_claim_isolation(self):
        manifest = valid_manifest()
        manifest["isolation"]["network_isolation"] = "ENFORCED"
        with self.assertRaisesRegex(preflight.PreflightError, "NOT_ENFORCED"):
            validate_structure(manifest)

    def test_isolated_runner_posture_fails_until_real_contract_exists(self):
        manifest = valid_manifest()
        manifest["execution_posture"] = "ISOLATED_RUNNER_CONTRACT"
        manifest["isolation"] = {"claimed": "ENFORCED_WITHOUT_CONTRACT_REFERENCE"}
        with self.assertRaisesRegex(preflight.PreflightError, "not implemented or contract-bound"):
            validate_structure(manifest)

    def test_evidence_lock_must_remain_not_created(self):
        manifest = valid_manifest()
        manifest["evidence_lock"] = {"status": "CREATED", "sha256": "c" * 64}
        with self.assertRaisesRegex(preflight.PreflightError, "Evidence Lock NOT_CREATED"):
            validate_structure(manifest)

    def test_output_destination_cannot_target_repository_file(self):
        manifest = valid_manifest()
        manifest["output_destination"] = "project-state.json"
        with self.assertRaisesRegex(preflight.PreflightError, "dedicated non-repository Pilot root"):
            validate_structure(manifest)

    def test_adapter_cwd_cannot_escape_repository(self):
        manifest = valid_manifest()
        manifest["adapter_cwd"] = "../outside"
        with self.assertRaisesRegex(preflight.PreflightError, "without parent traversal"):
            validate_structure(manifest)

    def test_non_circular_authorization_transition_accepts_only_governance_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
            (repo / "project-state.json").write_text("{}\n", encoding="utf-8")
            (repo / "STATUS.md").write_text("base\n", encoding="utf-8")
            (repo / "docs/ai").mkdir(parents=True)
            (repo / "docs/ai/CURRENT_STATE.md").write_text("base\n", encoding="utf-8")
            (repo / "docs/research").mkdir(parents=True)
            (repo / "docs/research/OD_PILOT_01_DRAFT.md").write_text("draft\n", encoding="utf-8")
            (repo / "experiments/e0/pilot").mkdir(parents=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
            tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=repo, text=True).strip()
            manifest = valid_manifest()
            manifest["authorization_base_commit"] = base
            manifest["authorization_base_tree"] = tree
            manifest_path = repo / "experiments/e0/pilot/authorized.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            (repo / "project-state.json").write_text('{"experiment_0_pilot_status":"AUTHORIZED_BOUNDED_PILOT"}\n', encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "authorize"], cwd=repo, check=True)
            head, runtime_tree, paths = preflight.validate_authorization_transition(repo, manifest, manifest_path)
            self.assertNotEqual(head, base)
            self.assertEqual(len(runtime_tree), 40)
            self.assertIn("project-state.json", paths)
            self.assertIn("experiments/e0/pilot/authorized.json", paths)

    def test_authorization_transition_rejects_runtime_code_change(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
            (repo / "project-state.json").write_text("{}\n", encoding="utf-8")
            (repo / "experiments/e0/pilot").mkdir(parents=True)
            (repo / "runtime.py").write_text("safe=True\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "base"], cwd=repo, check=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
            tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=repo, text=True).strip()
            manifest = valid_manifest()
            manifest["authorization_base_commit"] = base
            manifest["authorization_base_tree"] = tree
            manifest_path = repo / "experiments/e0/pilot/authorized.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            (repo / "runtime.py").write_text("safe=False\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "bad transition"], cwd=repo, check=True)
            with self.assertRaisesRegex(preflight.PreflightError, "non-allowed paths"):
                preflight.validate_authorization_transition(repo, manifest, manifest_path)

    def test_human_validator_child_does_not_create_bytecode_drift(self):
        pycache = SCRIPTS / "__pycache__"
        before = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
        proc = subprocess.run(
            [sys.executable, "-B", "scripts/e0/validate_human_reference_approval.py", "--repo-root", str(ROOT)],
            cwd=ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        after = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
        self.assertEqual(after, before)
        self.assertFalse(pycache.exists(), "child validator created __pycache__")


class RunAdapterTests(unittest.TestCase):
    def bounded(self, adapter_source: str, *, timeout: int = 2, cap: int = 4096):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            adapter = temp / "adapter.py"
            adapter.write_text(adapter_source, encoding="utf-8")
            return run_adapter.bounded_run(
                [sys.executable, str(adapter)],
                request_text='{"ping":"pong"}',
                cwd=temp,
                env={"PATH": os.environ.get("PATH", "")},
                timeout_seconds=timeout,
                max_output_bytes=cap,
            )

    def test_direct_run_adapter_cli_is_rejected(self):
        proc = subprocess.run([sys.executable, str(SCRIPTS / "run_adapter.py")], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("internal helper", proc.stderr)

    def test_adapter_success_returns_bounded_output(self):
        returncode, output, _, _ = self.bounded("import json; print(json.dumps({'ok': True}))")
        self.assertEqual(returncode, 0)
        self.assertIn('"ok": true', output)

    def test_adapter_timeout_fails(self):
        with self.assertRaisesRegex(run_adapter.AdapterError, "timeout"):
            self.bounded("import time; time.sleep(5); print('{}')", timeout=1)

    def test_adapter_output_cap_fails(self):
        with self.assertRaisesRegex(run_adapter.AdapterError, "exceeded"):
            self.bounded("print('x' * 20000)", cap=1024)

    @unittest.skipUnless(os.name == "posix", "POSIX process-group regression")
    def test_timeout_kills_descendant_process_group(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            pid_file = temp / "child.pid"
            adapter = temp / "adapter.py"
            adapter.write_text(
                "import subprocess,sys,time\n"
                "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)'])\n"
                "open(sys.argv[1],'w').write(str(child.pid))\n"
                "time.sleep(10)\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(run_adapter.AdapterError, "timeout"):
                run_adapter.bounded_run(
                    [sys.executable, str(adapter), str(pid_file)], request_text="{}", cwd=temp,
                    env={"PATH": os.environ.get("PATH", "")}, timeout_seconds=1, max_output_bytes=4096,
                )
            pid = int(pid_file.read_text(encoding="utf-8"))
            deadline = time.monotonic() + 2.0
            alive = True
            while time.monotonic() < deadline:
                stat_path = Path(f"/proc/{pid}/stat")
                if not stat_path.exists():
                    alive = False
                    break
                parts = stat_path.read_text(encoding="utf-8", errors="replace").split()
                if len(parts) > 2 and parts[2] == "Z":
                    alive = False
                    break
                time.sleep(0.05)
            self.assertFalse(alive, f"adapter descendant {pid} survived bounded timeout")


class ExecutePilotTests(unittest.TestCase):
    def test_max_runs_reservation_is_atomic_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            attempt, first = execute_pilot.reserve_attempt(root, "a" * 64, 1)
            self.assertEqual(attempt, 1)
            self.assertTrue(first.is_dir())
            with self.assertRaisesRegex(preflight.PreflightError, "max_runs exhausted"):
                execute_pilot.reserve_attempt(root, "a" * 64, 1)

    def test_output_root_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            parent = Path(temp_dir)
            repo = parent / "repo"
            repo.mkdir()
            output = parent / preflight.PILOT_OUTPUT_DESTINATION
            output.symlink_to(repo, target_is_directory=True)
            with self.assertRaisesRegex(preflight.PreflightError, "must not be a symlink"):
                execute_pilot.ensure_output_root(repo.resolve())

    def test_request_symlink_is_rejected_before_hash_or_parse(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            target = temp / "target.json"
            target.write_text('{"safe":true}', encoding="utf-8")
            link = temp / "request.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(preflight.PreflightError, "must not be a symlink"):
                execute_pilot.read_regular_file_once(link, label="Pilot request")

    def test_normal_executor_import_does_not_create_pycache(self):
        pycache = SCRIPTS / "__pycache__"
        if pycache.exists():
            for child in pycache.iterdir():
                child.unlink()
            pycache.rmdir()
        proc = subprocess.run([sys.executable, str(SCRIPTS / "execute_pilot.py"), "--help"], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(pycache.exists(), "official executor created bytecode before preflight")

    def test_official_executor_fails_before_spawn_while_canonical_state_unauthorized(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            marker = temp / "spawned"
            adapter = temp / "adapter.py"
            adapter.write_text(f"open({str(marker)!r},'w').write('spawned'); print('{{}}')", encoding="utf-8")
            request = temp / "request.json"
            request.write_text("{}", encoding="utf-8")
            manifest = valid_manifest()
            manifest["adapter_command"] = f"{sys.executable} {adapter}"
            manifest["request_sha256"] = sha256(request)
            manifest_path = temp / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "execute_pilot.py"), "--repo-root", str(ROOT), "--manifest", str(manifest_path), "--request", str(request)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("canonical project state does not authorize Pilot", proc.stderr)
            self.assertFalse(marker.exists(), "adapter spawned despite absent canonical Pilot authority")


if __name__ == "__main__":
    unittest.main()
