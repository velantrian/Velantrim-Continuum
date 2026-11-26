from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shlex
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path

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
classify = load_module("classify_attempts", SCRIPTS / "classify_attempts.py")
run_adapter = load_module("run_adapter", SCRIPTS / "run_adapter.py")
execute_pilot = load_module("execute_pilot", SCRIPTS / "execute_pilot.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def valid_manifest(root: Path = ROOT, *, request_sha: str = "d" * 64) -> dict:
    return {
        "run_type": "PILOT",
        "label": "PILOT — NOT EVIDENCE",
        "owner_decision_id": "OD-PILOT-01",
        "owner_decision_status": "ADOPTED",
        "owner_github_login": "velantrian",
        "owner_adopted_at": "2026-08-23T00:00:00Z",
        "activation_policy": preflight.ACTIVATION_POLICY,
        "human_approval": {
            "path": preflight.APPROVAL_PATH,
            "sha256": sha256(root / preflight.APPROVAL_PATH),
        },
        "approved_references": [
            {
                "path": preflight.CAPTURE_GOLD_PATH,
                "sha256": sha256(root / preflight.CAPTURE_GOLD_PATH),
            },
            {
                "path": preflight.TRANSFER_ORACLE_PATH,
                "sha256": sha256(root / preflight.TRANSFER_ORACLE_PATH),
            },
        ],
        "fixture_or_scenario_ids": ["F1-P-A", "T-PILOT-01"],
        "request_sha256": request_sha,
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
        "credentials": {"profile": "pilot-minimal", "scope": "inference-only", "environment_variables": []},
        "tool_policy": {"mode": "NO_TOOLS", "allowlist": []},
        "budget": {"max_total_tokens": 4096, "max_cost": 0.0, "currency": "USD"},
        "network_dependency": {"required": False, "allowed_hosts": []},
        "manual_stop": {
            "owner_github_login": "velantrian",
            "contact_ref": "test-owner",
            "procedure": "terminate the local bounded Pilot process",
        },
        "adapter_command": "python -c \"import json; print(json.dumps({'ok': True}))\"",
        "adapter_cwd": ".",
        "environment_allowlist": [],
        "output_destination": preflight.PILOT_OUTPUT_DESTINATION,
    }


def validate_structure(manifest: dict):
    return preflight.validate_manifest(manifest, ROOT, check_git=False, check_authority_state=False)


def make_package_and_activation(
    repo: Path, *, mutate_between: tuple[str, str] | None = None,
    adapter_command: str | None = None, timeout_seconds: int | None = None,
    max_runs: int | None = None,
) -> tuple[Path, Path, str, str, str, str]:
    request = repo.parent / "request.json"
    request.write_text("{}\n", encoding="utf-8")
    manifest = valid_manifest(repo, request_sha=sha256(request))
    if adapter_command is not None:
        manifest["adapter_command"] = adapter_command
    if timeout_seconds is not None:
        manifest["limits"]["timeout_seconds"] = timeout_seconds
    if max_runs is not None:
        manifest["limits"]["max_runs"] = max_runs
    package_dir = repo / "experiments/e0/pilot/packages"
    package_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = package_dir / "od-pilot-01.v0.1.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run(["git", "add", manifest_path.relative_to(repo)], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "package"], cwd=repo, check=True)
    base = git(repo, "rev-parse", "HEAD")
    base_tree = git(repo, "rev-parse", "HEAD^{tree}")
    manifest_sha = sha256(manifest_path)

    if mutate_between is not None:
        relative, content = mutate_between
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    state_path = repo / "project-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
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
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "activate"], cwd=repo, check=True)
    head = git(repo, "rev-parse", "HEAD")
    head_tree = git(repo, "rev-parse", "HEAD^{tree}")
    return manifest_path, request, base, base_tree, head, head_tree


class PilotPreflightTests(unittest.TestCase):
    def test_valid_bounded_manifest_passes_structural_validation(self):
        messages = validate_structure(valid_manifest())
        self.assertTrue(any(item.startswith("pilot_ids=") for item in messages))

    def test_canonical_project_state_blocks_pilot_before_owner_authorization(self):
        manifest = valid_manifest()
        with tempfile.TemporaryDirectory(dir=ROOT / "experiments/e0/pilot") as temp_dir:
            path = Path(temp_dir) / "manifest.json"
            payload = (json.dumps(manifest) + "\n").encode()
            path.write_bytes(payload)
            with self.assertRaisesRegex(preflight.PreflightError, "canonical project state does not authorize Pilot"):
                preflight.validate_manifest(manifest, ROOT, manifest_path=path, manifest_sha256=hashlib.sha256(payload).hexdigest())

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

    def test_missing_tool_policy_fails_closed(self):
        manifest = valid_manifest()
        del manifest["tool_policy"]
        with self.assertRaisesRegex(preflight.PreflightError, "tool_policy"):
            validate_structure(manifest)

    def test_no_tools_cannot_carry_tool_allowlist(self):
        manifest = valid_manifest()
        manifest["tool_policy"]["allowlist"] = ["browser"]
        with self.assertRaisesRegex(preflight.PreflightError, "empty tool allowlist"):
            validate_structure(manifest)

    def test_missing_budget_fails_closed(self):
        manifest = valid_manifest()
        del manifest["budget"]
        with self.assertRaisesRegex(preflight.PreflightError, "budget"):
            validate_structure(manifest)

    def test_network_dependency_requires_explicit_host_binding(self):
        manifest = valid_manifest()
        manifest["network_dependency"] = {"required": True, "allowed_hosts": []}
        with self.assertRaisesRegex(preflight.PreflightError, "requires at least one allowed host"):
            validate_structure(manifest)

    def test_manual_stop_owner_must_match_owner(self):
        manifest = valid_manifest()
        manifest["manual_stop"]["owner_github_login"] = "someone-else"
        with self.assertRaisesRegex(preflight.PreflightError, "must match owner_github_login"):
            validate_structure(manifest)

    def test_credential_environment_must_be_allowlisted(self):
        manifest = valid_manifest()
        manifest["credentials"]["environment_variables"] = ["MODEL_API_KEY"]
        with self.assertRaisesRegex(preflight.PreflightError, "not included in environment_allowlist"):
            validate_structure(manifest)

    def test_missing_credential_scope_fails_closed(self):
        manifest = valid_manifest()
        manifest["credentials"]["scope"] = ""
        with self.assertRaisesRegex(preflight.PreflightError, "credentials.scope"):
            validate_structure(manifest)

    def test_non_finite_budget_fails_closed(self):
        manifest = valid_manifest()
        manifest["budget"]["max_cost"] = float("nan")
        with self.assertRaisesRegex(preflight.PreflightError, "finite non-negative"):
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

    def test_obsolete_self_referential_fields_are_rejected(self):
        manifest = valid_manifest()
        manifest["authorization_base_commit"] = "a" * 40
        with self.assertRaisesRegex(preflight.PreflightError, "obsolete self-referential"):
            validate_structure(manifest)


class ActivationIntegrationTests(unittest.TestCase):
    def clone_repo(self, temp: Path) -> Path:
        repo = temp / "repo"
        subprocess.run(["git", "clone", "-q", "--local", str(ROOT), str(repo)], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
        return repo

    def run_synthetic_adapter(self, behavior: str, *, timeout_seconds: int = 2, send_signal: int | None = None):
        """Only synthetic child processes in disposable Git clones; never a real Pilot."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = self.clone_repo(temp)
            counter = temp / "synthetic-provider-calls.txt"
            child_source = (
                "import sys, time\n"
                "from pathlib import Path\n"
                "counter = Path(sys.argv[1])\n"
                "counter.write_text(str(int(counter.read_text()) + 1 if counter.exists() else 1))\n"
                + behavior
            )
            command = shlex.join([sys.executable, "-c", child_source, str(counter)])
            manifest_path, request, *_ = make_package_and_activation(
                repo, adapter_command=command, timeout_seconds=timeout_seconds,
                max_runs=2,  # spare capacity proves no implicit second attempt
            )
            argv = [sys.executable, "scripts/e0/execute_pilot.py", "--repo-root", str(repo),
                    "--manifest", str(manifest_path), "--request", str(request)]
            if send_signal is None:
                proc = subprocess.run(argv, cwd=repo, text=True, capture_output=True, check=False)
            else:
                popen = subprocess.Popen(argv, cwd=repo, text=True,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                deadline = time.monotonic() + 20
                while not counter.exists() and popen.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue(counter.exists(), "synthetic adapter never started")
                popen.send_signal(send_signal)
                out, err = popen.communicate(timeout=20)
                proc = subprocess.CompletedProcess(argv, popen.returncode, out, err)
            output_root = temp / preflight.PILOT_OUTPUT_DESTINATION
            attempts = list(output_root.glob("*/attempt-*"))
            self.assertEqual(len(attempts), 1, proc.stderr)
            result_path = attempts[0] / "result.json"
            self.assertTrue(result_path.is_file(), proc.stderr)
            result = json.loads(result_path.read_text(encoding="utf-8"))
            artifacts = {path.name for path in attempts[0].iterdir()}
            return proc, result, artifacts, int(counter.read_text()), len(attempts)

    def test_synthetic_adapter_bad_stdout_is_unknown(self):
        for value in ("not-json", "null", "[]", "[1]", "123", "true", '"string"'):
            with self.subTest(value=value):
                proc, result, artifacts, calls, attempts = self.run_synthetic_adapter(
                    f"print({value!r})\n"
                )
                self.assert_unknown_bound(proc, result, artifacts, calls, attempts)

    def _prewrite_race_probe(self, *, baseline_sha: str | None) -> dict:
        """Pause before the first reservation write and race two supervisors.

        In an old main checkout, reserve_attempt() releases its implicit
        'check' before reservation.json is written, allowing the second slot.
        In the patched checkout, the same interception happens under flock.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = self.clone_repo(temp)
            if baseline_sha is not None:
                subprocess.run(["git", "checkout", "-q", baseline_sha], cwd=repo, check=True)
            launches = temp / "launches"
            launches.mkdir()
            release_reservation = temp / "release-reservation"
            release_adapter = temp / "release-adapter"
            reservation_paused = temp / "reservation-paused"
            second_at_reserve = temp / "second-at-reserve"
            child = (
                "import os,sys,time\n"
                "from pathlib import Path\n"
                "launches, release = Path(sys.argv[1]), Path(sys.argv[2])\n"
                "(launches / str(os.getpid())).write_text('launched')\n"
                "deadline = time.monotonic() + 18\n"
                "while not release.exists() and time.monotonic() < deadline: time.sleep(.02)\n"
                "print('{}')\n"
            )
            command = shlex.join([sys.executable, "-c", child, str(launches), str(release_adapter)])
            manifest_path, request, *_ = make_package_and_activation(
                repo, adapter_command=command, timeout_seconds=24, max_runs=2
            )
            launcher = [
                "--repo-root", str(repo),
                "--manifest", str(manifest_path),
                "--request", str(request),
            ]
            first_script = (
                "import os,sys,time\n"
                "from pathlib import Path\n"
                "sys.path.insert(0, 'scripts/e0')\n"
                "import execute_pilot as ep\n"
                "original = ep.atomic_write_json\n"
                "def paused_write(path, value):\n"
                "    if path.name == 'reservation.json':\n"
                "        Path(os.environ['RACE_PAUSED']).write_text('paused')\n"
                "        release = Path(os.environ['RACE_RELEASE_RESERVATION'])\n"
                "        deadline = time.monotonic() + 18\n"
                "        while not release.exists() and time.monotonic() < deadline: time.sleep(.02)\n"
                "        if not release.exists(): raise RuntimeError('reservation gate timeout')\n"
                "    return original(path, value)\n"
                "ep.atomic_write_json = paused_write\n"
                "raise SystemExit(ep.main())\n"
            )
            second_script = (
                "import os,sys\n"
                "from pathlib import Path\n"
                "sys.path.insert(0, 'scripts/e0')\n"
                "import execute_pilot as ep\n"
                "original = ep.reserve_attempt\n"
                "def observed_reserve(*args, **kwargs):\n"
                "    Path(os.environ['RACE_SECOND_READY']).write_text('entered')\n"
                "    return original(*args, **kwargs)\n"
                "ep.reserve_attempt = observed_reserve\n"
                "raise SystemExit(ep.main())\n"
            )
            first_env = {
                **os.environ,
                "RACE_PAUSED": str(reservation_paused),
                "RACE_RELEASE_RESERVATION": str(release_reservation),
            }
            second_env = {**os.environ, "RACE_SECOND_READY": str(second_at_reserve)}
            first = subprocess.Popen(
                [sys.executable, "-c", first_script, *launcher], cwd=repo, env=first_env,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            second = None
            try:
                deadline = time.monotonic() + 18
                while not reservation_paused.exists() and first.poll() is None and time.monotonic() < deadline:
                    time.sleep(.02)
                self.assertTrue(reservation_paused.exists(), "first process never reached reservation.json write")
                second = subprocess.Popen(
                    [sys.executable, "-c", second_script, *launcher], cwd=repo, env=second_env,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                )
                deadline = time.monotonic() + 18
                while not second_at_reserve.exists() and second.poll() is None and time.monotonic() < deadline:
                    time.sleep(.02)
                self.assertTrue(second_at_reserve.exists(), "second process never attempted reservation")
                # Allow the old unprotected implementation to reach attempt-002
                # while the first reservation is deliberately not yet written.
                package_root = next((temp / preflight.PILOT_OUTPUT_DESTINATION).glob("*"))
                deadline = time.monotonic() + 3.0
                # Do not stop at attempt-002: the older implementation creates
                # its slot before the fake adapter process has started.
                while not list(launches.iterdir()) and second.poll() is None and time.monotonic() < deadline:
                    time.sleep(.02)
                second_slot = (package_root / "attempt-002").exists()
                launched_before_first_write = bool(list(launches.iterdir()))
                # Free the first to complete the fsynced reservation. It will
                # then launch a fake adapter held at a separate marker.
                release_reservation.write_text("go")
                if not second_slot:
                    second_out, second_err = second.communicate(timeout=18)
                else:
                    second_out, second_err = "", ""
                deadline = time.monotonic() + 10
                while not list(launches.iterdir()) and first.poll() is None and time.monotonic() < deadline:
                    time.sleep(.02)
                release_adapter.write_text("go")
                first_out, first_err = first.communicate(timeout=18)
                if second_slot:
                    second_out, second_err = second.communicate(timeout=18)
                count = len(list(launches.iterdir()))
                return {
                    "second_slot": second_slot,
                    "launched_before_first_write": launched_before_first_write,
                    "adapter_calls": count,
                    "second_rc": second.returncode,
                    "second_stderr": second_err,
                    "first_rc": first.returncode,
                    "first_stderr": first_err,
                }
            finally:
                release_reservation.write_text("go")
                release_adapter.write_text("go")
                for proc in (first, second):
                    if proc is None:
                        continue
                    if proc.poll() is None:
                        proc.kill()
                    proc.communicate()

    def assert_prewrite_reservation_is_protected(self, result: dict) -> None:
        """One acceptance assertion shared by patched and historical code."""
        self.assertFalse(result["second_slot"], result)
        self.assertFalse(result["launched_before_first_write"], result)
        self.assertEqual(result["adapter_calls"], 1, result)
        self.assertNotEqual(result["second_rc"], 0, result)
        self.assertIn("unresolved UNKNOWN_OUTCOME", result["second_stderr"], result)

    @unittest.skipUnless(os.name == "posix", "POSIX two-process reservation race")
    def test_prewrite_reservation_race_passes_on_fixed_branch(self):
        result = self._prewrite_race_probe(baseline_sha=None)
        self.assert_prewrite_reservation_is_protected(result)
        print("PREWRITE_RACE fixed HEAD: PASS (second adapter never ran)")

    @unittest.skipUnless(os.name == "posix", "POSIX two-process reservation race")
    def test_prewrite_reservation_race_reproduces_failure_on_old_main(self):
        old_main = "51d8ce16f3b13816165db0aa0adc5352feecf136"
        result = self._prewrite_race_probe(baseline_sha=old_main)
        # The same acceptance assertion must fail against historical main.
        with self.assertRaises(AssertionError):
            self.assert_prewrite_reservation_is_protected(result)
        self.assertTrue(result["second_slot"], result)
        self.assertTrue(result["launched_before_first_write"], result)
        self.assertEqual(result["adapter_calls"], 2, result)
        self.assertEqual(result["second_rc"], 0, result)
        print(f"PREWRITE_RACE old main {old_main[:12]}: RED (second adapter launched before first reservation)")

    @unittest.skipUnless(os.name == "posix", "POSIX flock integration")
    def test_concurrent_supervisors_share_reservation_and_second_never_starts(self):
        """Two real processes, max_runs=2, common output directory, no provider."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = self.clone_repo(temp)
            calls = temp / "calls"
            calls.mkdir()
            release = temp / "release"
            child = (
                "import os,sys,time\n"
                "from pathlib import Path\n"
                "calls = Path(sys.argv[1]); release = Path(sys.argv[2])\n"
                " (calls / ('called-' + str(os.getpid()))).write_text('started')\n"
                "deadline = time.monotonic() + 15\n"
                "while not release.exists() and time.monotonic() < deadline: time.sleep(.02)\n"
                "print('{}')\n"
            )
            child = child.replace("\n (calls", "\n(calls")
            command = shlex.join([sys.executable, "-c", child, str(calls), str(release)])
            manifest_path, request, *_ = make_package_and_activation(
                repo, adapter_command=command, timeout_seconds=25, max_runs=2
            )
            argv = [sys.executable, "scripts/e0/execute_pilot.py", "--repo-root", str(repo),
                    "--manifest", str(manifest_path), "--request", str(request)]
            first = subprocess.Popen(argv, cwd=repo, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)
            try:
                deadline = time.monotonic() + 15
                while not list(calls.glob("called-*")) and first.poll() is None and time.monotonic() < deadline:
                    time.sleep(.02)
                self.assertEqual(len(list(calls.glob("called-*"))), 1, "first synthetic adapter did not start")
                package_root = next((temp / preflight.PILOT_OUTPUT_DESTINATION).glob("*"))
                self.assertTrue((package_root / "attempt-001" / "reservation.json").is_file())
                second = subprocess.run(argv, cwd=repo, capture_output=True, text=True, timeout=15, check=False)
                self.assertNotEqual(second.returncode, 0)
                self.assertIn("unresolved UNKNOWN_OUTCOME", second.stderr)
                self.assertEqual(len(list(calls.glob("called-*"))), 1, "second synthetic adapter started")
                self.assertFalse((package_root / "attempt-002").exists())
            finally:
                release.write_text("go")
                try:
                    first.communicate(timeout=15)
                except subprocess.TimeoutExpired:
                    first.kill()
                    first.communicate()

    def test_synthetic_adapter_success_completes_once(self):
        proc, result, artifacts, calls, attempts = self.run_synthetic_adapter(
            "import json; print(json.dumps({'ok': True}))\n"
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertIn("PILOT_EXECUTION_COMPLETED", proc.stdout)
        self.assertIn("response.json", artifacts)
        self.assertIn("metrics.json", artifacts)
        self.assertEqual((calls, attempts), (1, 1))

    def test_synthetic_adapter_definite_error_is_failed(self):
        proc, result, artifacts, calls, attempts = self.run_synthetic_adapter(
            "sys.exit(2)\n"
        )
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(result["status"], "FAILED")
        self.assertIn("PILOT_EXECUTION_ERROR", proc.stderr)
        self.assertNotIn("response.json", artifacts)
        self.assertNotIn("metrics.json", artifacts)
        self.assertEqual((calls, attempts), (1, 1))

    def test_synthetic_adapter_exit_four_is_unknown_and_not_retried(self):
        proc, result, artifacts, calls, attempts = self.run_synthetic_adapter(
            "print('CAPTURE_ADAPTER_UNKNOWN_OUTCOME: timeout', file=sys.stderr)\n"
            "sys.exit(4)\n"
        )
        self.assertEqual(proc.returncode, 4, proc.stderr)
        self.assertEqual(result["status"], "UNKNOWN_OUTCOME")
        self.assertEqual(result["adapter_exit_code"], 4)
        self.assertIn("stderr_text_utf8_sha256=", result["error"])
        self.assertNotIn("CAPTURE_ADAPTER_UNKNOWN_OUTCOME:", result["error"])
        self.assertIn("PILOT_EXECUTION_UNKNOWN_OUTCOME", proc.stderr)
        self.assertNotIn("response.json", artifacts)
        self.assertNotIn("metrics.json", artifacts)
        self.assertEqual((calls, attempts), (1, 1))

    def test_synthetic_runner_timeout_is_unknown_and_not_retried(self):
        proc, result, artifacts, calls, attempts = self.run_synthetic_adapter(
            "time.sleep(30)\n", timeout_seconds=1
        )
        self.assertEqual(proc.returncode, 4, proc.stderr)
        self.assertEqual(result["status"], "UNKNOWN_OUTCOME")
        self.assertIsNone(result["adapter_exit_code"])
        self.assertIn("adapter timeout", result["error"])
        self.assertIn("PILOT_EXECUTION_UNKNOWN_OUTCOME", proc.stderr)
        self.assertNotIn("response.json", artifacts)
        self.assertNotIn("metrics.json", artifacts)
        self.assertEqual((calls, attempts), (1, 1))

    def assert_unknown_bound(self, proc, result, artifacts, calls, attempts):
        self.assertEqual(proc.returncode, 4, proc.stderr)
        self.assertEqual(result["status"], "UNKNOWN_OUTCOME")
        self.assertIn("PILOT_EXECUTION_UNKNOWN_OUTCOME", proc.stderr)
        self.assertNotIn("response.json", artifacts)
        self.assertNotIn("metrics.json", artifacts)
        self.assertIn("reservation.json", artifacts)  # attempt stays consumed
        self.assertEqual(result["attempt"], 1)
        self.assertRegex(result["package_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["request_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual((calls, attempts), (1, 1))

    def test_synthetic_adapter_unexpected_exit_three_is_unknown(self):
        out = self.run_synthetic_adapter("sys.exit(3)\n")
        self.assert_unknown_bound(*out)
        self.assertEqual(out[1]["adapter_exit_code"], 3)

    def test_synthetic_adapter_uncaught_crash_is_unknown(self):
        out = self.run_synthetic_adapter("raise RuntimeError('boom after send')\n")
        self.assert_unknown_bound(*out)
        self.assertEqual(out[1]["adapter_exit_code"], 1)

    @unittest.skipUnless(os.name == "posix", "POSIX signals")
    def test_synthetic_adapter_killed_by_signal_is_unknown(self):
        out = self.run_synthetic_adapter("import os, signal; os.kill(os.getpid(), signal.SIGKILL)\n")
        self.assert_unknown_bound(*out)
        self.assertLess(out[1]["adapter_exit_code"], 0)

    def test_synthetic_adapter_output_cap_is_unknown(self):
        out = self.run_synthetic_adapter("print('x' * 20000)\n")
        self.assert_unknown_bound(*out)
        self.assertIn("output exceeded", out[1]["error"])

    @unittest.skipUnless(os.name == "posix", "POSIX signals")
    def test_sigterm_during_adapter_is_unknown_not_retried(self):
        import signal
        out = self.run_synthetic_adapter("time.sleep(30)\n", timeout_seconds=60, send_signal=signal.SIGTERM)
        self.assert_unknown_bound(*out)
        self.assertIn("interrupted", out[1]["error"])

    @unittest.skipUnless(os.name == "posix", "POSIX signals")
    def test_sigint_during_adapter_is_unknown_not_retried(self):
        import signal
        out = self.run_synthetic_adapter("time.sleep(30)\n", timeout_seconds=60, send_signal=signal.SIGINT)
        self.assert_unknown_bound(*out)
        self.assertIn("KeyboardInterrupt", out[1]["error"])

    def test_definite_failure_result_carries_attempt_binding(self):
        proc, result, *_ = self.run_synthetic_adapter("sys.exit(2)\n")
        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["attempt"], 1)
        self.assertRegex(result["package_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["request_sha256"], r"^[0-9a-f]{64}$")

    def test_committed_activation_package_reaches_harmless_adapter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = self.clone_repo(temp)
            manifest_path, request, base, base_tree, head, head_tree = make_package_and_activation(repo)
            proc = subprocess.run(
                [sys.executable, "scripts/e0/execute_pilot.py", "--repo-root", str(repo), "--manifest", str(manifest_path), "--request", str(request)],
                cwd=repo,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("PILOT_EXECUTION_COMPLETED", proc.stdout)
            output_root = temp / preflight.PILOT_OUTPUT_DESTINATION
            result_files = list(output_root.glob("*/attempt-001/result.json"))
            self.assertEqual(len(result_files), 1)
            result = json.loads(result_files[0].read_text(encoding="utf-8"))
            self.assertEqual(result["authorization_base_commit"], base)
            self.assertEqual(result["authorization_base_tree"], base_tree)
            self.assertEqual(result["activation_head_commit"], head)
            self.assertEqual(result["activation_tree"], head_tree)
            self.assertEqual(git(repo, "status", "--porcelain"), "")

    def test_generic_authorized_state_without_package_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = self.clone_repo(Path(temp_dir))
            state_path = repo / "project-state.json"
            state = json.loads(state_path.read_text())
            state["experiment_0_pilot_status"] = preflight.AUTHORIZED_PILOT_STATE
            state["experiment_0_pilot_authorization"] = None
            state_path.write_text(json.dumps(state) + "\n")
            subprocess.run(["git", "add", "project-state.json"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "generic auth only"], cwd=repo, check=True)
            manifest = valid_manifest(repo)
            path = repo / "experiments/e0/pilot/generic.json"
            path.write_text(json.dumps(manifest) + "\n")
            with self.assertRaisesRegex(preflight.PreflightError, "package binding is absent"):
                preflight.validate_canonical_authorization(repo, manifest=manifest, manifest_path=path, manifest_sha256=sha256(path))

    def test_activation_must_be_direct_child_of_package_commit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = self.clone_repo(Path(temp_dir))
            manifest_path, _, base, _, head, _ = make_package_and_activation(repo)
            (repo / "STATUS.md").write_text((repo / "STATUS.md").read_text() + "\nintervening\n")
            subprocess.run(["git", "add", "STATUS.md"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "intervening"], cwd=repo, check=True)
            manifest = json.loads(manifest_path.read_text())
            with self.assertRaisesRegex(preflight.PreflightError, "direct child"):
                preflight.validate_canonical_authorization(repo, manifest=manifest, manifest_path=manifest_path, manifest_sha256=sha256(manifest_path))
            self.assertNotEqual(base, head)

    def test_activation_diff_rejects_non_activation_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = self.clone_repo(Path(temp_dir))
            manifest_path, _, _, _, _, _ = make_package_and_activation(repo, mutate_between=("scripts/e0/execute_pilot.py", "raise SystemExit('changed')\n"))
            manifest = json.loads(manifest_path.read_text())
            with self.assertRaisesRegex(preflight.PreflightError, "outside declared bounded authorization paths"):
                preflight.validate_canonical_authorization(repo, manifest=manifest, manifest_path=manifest_path, manifest_sha256=sha256(manifest_path))

    def test_manifest_blob_at_package_commit_must_match_canonical_sha(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = self.clone_repo(Path(temp_dir))
            manifest_path, _, _, _, _, _ = make_package_and_activation(repo)
            manifest = json.loads(manifest_path.read_text())
            state_path = repo / "project-state.json"
            state = json.loads(state_path.read_text())
            state["experiment_0_pilot_authorization"]["manifest_sha256"] = "0" * 64
            state_path.write_text(json.dumps(state) + "\n")
            subprocess.run(["git", "add", "project-state.json"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "--amend", "-qm", "activate wrong hash"], cwd=repo, check=True)
            with self.assertRaisesRegex(preflight.PreflightError, "does not match canonical owner-approved package binding"):
                preflight.validate_canonical_authorization(repo, manifest=manifest, manifest_path=manifest_path, manifest_sha256=sha256(manifest_path))

    def test_supervisor_sigkill_leaves_orphan_classified_unknown_and_spent(self):
        """SIGKILL of execute_pilot itself: no result.json can be written. The next look must
        classify the attempt as UNKNOWN_OUTCOME (spent), and a later explicit run takes the next
        attempt slot instead of reusing or silently retrying the orphan."""
        import signal as _signal
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = self.clone_repo(temp)
            counter = temp / "calls.txt"
            go = temp / "go"
            child = ("import sys, time\nfrom pathlib import Path\nc = Path(sys.argv[1])\n"
                     "c.write_text(str(int(c.read_text()) + 1 if c.exists() else 1))\n"
                     "g = Path(sys.argv[2])\n"
                     "while not g.exists(): time.sleep(0.05)\n"
                     "print('{\"ok\": true}')\n")
            command = shlex.join([sys.executable, "-c", child, str(counter), str(go)])
            manifest_path, request, *_ = make_package_and_activation(
                repo, adapter_command=command, timeout_seconds=30, max_runs=2)
            argv = [sys.executable, "scripts/e0/execute_pilot.py", "--repo-root", str(repo),
                    "--manifest", str(manifest_path), "--request", str(request)]
            popen = subprocess.Popen(argv, cwd=repo, text=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, start_new_session=True)
            deadline = time.monotonic() + 20
            while not counter.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue(counter.exists(), "synthetic adapter never started")
            os.killpg(popen.pid, _signal.SIGKILL)  # supervisor and adapter die together
            popen.communicate(timeout=20)
            package_root = next((temp / preflight.PILOT_OUTPUT_DESTINATION).glob("*"))
            first = classify.classify_package(package_root)
            self.assertEqual(len(first), 1)
            self.assertEqual(first[0]["classification"], "ORPHANED_RESERVATION")
            self.assertEqual(first[0]["outcome"], "UNKNOWN_OUTCOME")
            self.assertTrue(first[0]["spent"])
            self.assertFalse((package_root / "attempt-001" / "result.json").exists())
            cli = subprocess.run([sys.executable, str(SCRIPTS / "classify_attempts.py"), str(package_root)],
                                 text=True, capture_output=True, check=False)
            self.assertEqual(cli.returncode, 4, cli.stderr)
            self.assertEqual(int(counter.read_text()), 1)
            # A new attempt must never start while an outcome is unknown: the provider may have
            # processed attempt-001. The re-run is refused before reserving a slot or launching.
            go.write_text("1")
            second_run = subprocess.run(argv, cwd=repo, text=True, capture_output=True, check=False)
            self.assertNotEqual(second_run.returncode, 0)
            self.assertIn("unresolved UNKNOWN_OUTCOME", second_run.stderr)
            self.assertFalse((package_root / "attempt-002").exists())
            after = {e["attempt"]: e for e in classify.classify_package(package_root)}
            self.assertEqual(set(after), {1})
            self.assertEqual(after[1]["outcome"], "UNKNOWN_OUTCOME")  # orphan never rewritten
            self.assertEqual(int(counter.read_text()), 1)

    def test_new_journal_terminal_requires_matching_durable_seal(self):
        h = "a" * 64
        for status in ("COMPLETED", "FAILED"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as tmp:
                package = Path(tmp) / h
                att = package / "attempt-001"
                att.mkdir(parents=True)
                reservation = {
                    "journal_protocol": execute_pilot.TERMINAL_SEAL_PROTOCOL,
                    "package_sha256": h, "attempt": 1,
                }
                (att / "reservation.json").write_text(json.dumps(reservation))
                result = {"status": status, "attempt": 1, "package_sha256": h}
                (att / "result.json").write_text(json.dumps(result))
                self.assertEqual(classify.classify_attempt(att)["classification"],
                                 "UNSEALED_TERMINAL_RESULT")
                with self.assertRaisesRegex(execute_pilot.PreflightError, "unresolved UNKNOWN_OUTCOME"):
                    execute_pilot.reserve_attempt(Path(tmp), h, 2)
                payload = (att / "result.json").read_bytes()
                seal = {
                    "protocol": execute_pilot.TERMINAL_SEAL_PROTOCOL,
                    "status": status, "attempt": 1, "package_sha256": h,
                    "result_sha256": hashlib.sha256(payload).hexdigest(),
                }
                (att / "terminal-seal.json").write_text(json.dumps(seal))
                self.assertEqual(classify.classify_attempt(att)["outcome"], status)
                seal["result_sha256"] = "0" * 64
                (att / "terminal-seal.json").write_text(json.dumps(seal))
                self.assertEqual(classify.classify_attempt(att)["outcome"], "UNKNOWN_OUTCOME")

    def test_after_completed_rename_fsync_failure_retry_stays_blocked(self):
        """Mock disk fsync failure after publishing COMPLETED, and again for UNKNOWN.

        The first synthetic adapter runs once. Later CLI has exit 4 and no
        terminal seal; even a readable COMPLETED result must not enable run 2.
        """
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            repo = self.clone_repo(temp)
            calls = temp / "provider-calls.txt"
            child = ("import sys,json\n"
                     "from pathlib import Path\n"
                     "p=Path(sys.argv[1]);p.write_text(str(int(p.read_text())+1 if p.exists() else 1))\n"
                     "print(json.dumps({'ok': True}))\n")
            command = shlex.join([sys.executable, "-c", child, str(calls)])
            manifest_path, request, *_ = make_package_and_activation(
                repo, adapter_command=command, max_runs=2,
            )
            script = (
                "import sys,os,json\n"
                "from pathlib import Path\n"
                "sys.path.insert(0,'scripts/e0')\n"
                "import execute_pilot as ep\n"
                "original=ep._fsync_directory\n"
                "original_json=ep.atomic_write_json\n"
                "def flaky(path):\n"
                "    result=Path(path)/'result.json'\n"
                "    if result.is_file() and json.loads(result.read_text()).get('status')=='COMPLETED':\n"
                "        raise OSError('injected fsync after COMPLETED rename')\n"
                "    return original(path)\n"
                "def failed_unknown_write(path, payload):\n"
                "    if path.name=='result.json' and payload.get('status')=='UNKNOWN_OUTCOME':\n"
                "        raise OSError('injected failure to rewrite UNKNOWN_OUTCOME')\n"
                "    return original_json(path,payload)\n"
                "ep._fsync_directory=flaky\n"
                "ep.atomic_write_json=failed_unknown_write\n"
                "raise SystemExit(ep.main())\n"
            )
            argv = ["--repo-root", str(repo), "--manifest", str(manifest_path),
                    "--request", str(request)]
            first = subprocess.run(
                [sys.executable, "-c", script, *argv], cwd=repo,
                text=True, capture_output=True, timeout=25, check=False,
            )
            self.assertEqual(first.returncode, 4, first.stderr)
            self.assertEqual(int(calls.read_text()), 1)
            package = next((temp / preflight.PILOT_OUTPUT_DESTINATION).glob("*"))
            att = package / "attempt-001"
            self.assertEqual(json.loads((att / "result.json").read_text())["status"], "COMPLETED")
            self.assertFalse((att / "terminal-seal.json").exists())
            self.assertEqual(classify.classify_attempt(att)["classification"],
                             "UNSEALED_TERMINAL_RESULT")
            second = subprocess.run(
                [sys.executable, "scripts/e0/execute_pilot.py", *argv], cwd=repo,
                text=True, capture_output=True, timeout=25, check=False,
            )
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("unresolved UNKNOWN_OUTCOME", second.stderr)
            self.assertEqual(int(calls.read_text()), 1)
            self.assertFalse((package / "attempt-002").exists())

    def test_after_terminal_seal_rename_fsync_failure_does_not_retry(self):
        """Seal bytes may be visible despite a failed fsync and failed UNKNOWN rewrite.

        Acceptance: first supervisor returns 4, second supervisor using the SAME
        journal and max_runs=2 must not even spawn the synthetic adapter.
        """
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            repo = self.clone_repo(temp)
            counter = temp / "synthetic-adapter-calls.txt"
            child = (
                "import json,sys\n"
                "from pathlib import Path\n"
                "p=Path(sys.argv[1]); p.write_text(str(int(p.read_text())+1 if p.exists() else 1))\n"
                "print(json.dumps({'ok': True}))\n"
            )
            command = shlex.join([sys.executable, "-c", child, str(counter)])
            manifest_path, request, *_ = make_package_and_activation(
                repo, adapter_command=command, max_runs=2,
            )
            injected = (
                "import sys,os\n"
                "from pathlib import Path\n"
                "sys.path.insert(0,'scripts/e0')\n"
                "import execute_pilot as ep\n"
                "original_fsync=ep._fsync_directory\n"
                "original_json=ep.atomic_write_json\n"
                "def fail_after_seal_is_visible(path):\n"
                "    if (Path(path)/'terminal-seal.json').is_file():\n"
                "        raise OSError('injected fsync failure after terminal-seal.json rename')\n"
                "    return original_fsync(path)\n"
                "def fail_unknown_rewrite(path, payload):\n"
                "    if path.name=='result.json' and payload.get('status')=='UNKNOWN_OUTCOME':\n"
                "        raise OSError('injected UNKNOWN_OUTCOME rewrite failure')\n"
                "    return original_json(path, payload)\n"
                "ep._fsync_directory=fail_after_seal_is_visible\n"
                "ep.atomic_write_json=fail_unknown_rewrite\n"
                "raise SystemExit(ep.main())\n"
            )
            args = ["--repo-root", str(repo), "--manifest", str(manifest_path),
                    "--request", str(request)]
            first = subprocess.run(
                [sys.executable, "-c", injected, *args], cwd=repo,
                text=True, capture_output=True, timeout=25, check=False,
            )
            self.assertEqual(first.returncode, 4, first.stderr)
            self.assertEqual(int(counter.read_text()), 1)
            package = next((temp / preflight.PILOT_OUTPUT_DESTINATION).glob("*"))
            attempt = package / "attempt-001"
            self.assertEqual(json.loads((attempt / "result.json").read_text())["status"], "COMPLETED")
            self.assertTrue((attempt / "terminal-seal.json").is_file())
            self.assertEqual(classify.classify_attempt(attempt)["outcome"], "COMPLETED")
            second = subprocess.run(
                [sys.executable, "scripts/e0/execute_pilot.py", *args],
                cwd=repo, text=True, capture_output=True, timeout=25, check=False,
            )
            self.assertNotEqual(second.returncode, 0, second.stderr)
            self.assertIn("unresolved UNKNOWN_OUTCOME", second.stderr)
            self.assertEqual(int(counter.read_text()), 1, "second synthetic adapter must not start")
            self.assertFalse((package / "attempt-002").exists())

    def test_classifier_reservation_incomplete_and_corrupt_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pkg = Path(temp_dir)
            (pkg / "attempt-001").mkdir()
            (pkg / "attempt-002").mkdir()
            (pkg / "attempt-002" / "reservation.json").write_text('{"package_sha256": "a"}')
            (pkg / "attempt-002" / "result.json").write_text('{"status": "COMPL')
            (pkg / "attempt-003").mkdir()
            (pkg / "attempt-003" / "reservation.json").write_text('{"package_sha256": "a"}')
            (pkg / "attempt-003" / "result.json").write_text('{"status": "COMPLETED", "attempt": 1}')
            got = {e["attempt"]: e for e in classify.classify_package(pkg)}
            self.assertEqual(got[1]["outcome"], "NOT_STARTED")
            self.assertTrue(got[1]["spent"])
            self.assertEqual(got[2]["classification"], "RESULT_UNREADABLE")
            self.assertEqual(got[2]["outcome"], "UNKNOWN_OUTCOME")
            self.assertEqual(got[3]["classification"], "BINDING_MISMATCH")
            self.assertEqual(got[3]["outcome"], "UNKNOWN_OUTCOME")

    def test_classifier_completed_requires_full_binding(self):
        """COMPLETED counts only with attempt + package_sha256 present and matching the directory
        and a readable reservation; any missing field is a BINDING_MISMATCH (UNKNOWN_OUTCOME)."""
        h = "a" * 64
        good = {"status": "COMPLETED", "attempt": 1, "package_sha256": h}
        cases = {
            "ok": (good, {"package_sha256": h, "attempt": 1}, "COMPLETED"),
            "no_attempt": ({"status": "COMPLETED", "package_sha256": h}, {"package_sha256": h}, "BINDING_MISMATCH"),
            "no_hash": ({"status": "COMPLETED", "attempt": 1}, {"package_sha256": h}, "BINDING_MISMATCH"),
            "other_pkg": ({**good, "package_sha256": "b" * 64}, {"package_sha256": "b" * 64}, "BINDING_MISMATCH"),
            "no_reservation": (good, None, "BINDING_MISMATCH"),
            "bad_reservation": (good, "{", "BINDING_MISMATCH"),
            "res_attempt": (good, {"package_sha256": h, "attempt": 2}, "BINDING_MISMATCH"),
        }
        for label, (result, reservation, expected) in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as temp_dir:
                att = Path(temp_dir) / h / "attempt-001"
                att.mkdir(parents=True)
                (att / "result.json").write_text(json.dumps(result))
                if isinstance(reservation, dict):
                    (att / "reservation.json").write_text(json.dumps(reservation))
                elif isinstance(reservation, str):
                    (att / "reservation.json").write_text(reservation)
                got = classify.classify_attempt(att)
                self.assertEqual(got["classification"], expected, got)
                if expected != "COMPLETED":
                    self.assertEqual(got["outcome"], "UNKNOWN_OUTCOME")

    def test_reserve_attempt_refuses_while_outcome_unknown(self):
        h = "c" * 64
        for status in ("UNKNOWN_OUTCOME", None):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir).resolve()
                att = root / h / "attempt-001"
                att.mkdir(parents=True)
                (att / "reservation.json").write_text(json.dumps({"package_sha256": h, "attempt": 1}))
                if status:
                    (att / "result.json").write_text(json.dumps({"status": status, "attempt": 1, "package_sha256": h}))
                with self.assertRaisesRegex(execute_pilot.PreflightError, "unresolved UNKNOWN_OUTCOME"):
                    execute_pilot.reserve_attempt(root, h, 3)
                self.assertFalse((root / h / "attempt-002").exists())
        with tempfile.TemporaryDirectory() as temp_dir:  # definite FAILED still allows the next slot
            root = Path(temp_dir).resolve()
            att = root / h / "attempt-001"
            att.mkdir(parents=True)
            (att / "reservation.json").write_text(json.dumps({"package_sha256": h, "attempt": 1}))
            (att / "result.json").write_text(json.dumps({"status": "FAILED", "attempt": 1, "package_sha256": h}))
            self.assertEqual(execute_pilot.reserve_attempt(root, h, 3)[0], 2)


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
        with self.assertRaisesRegex(run_adapter.AdapterTimeoutError, "timeout"):
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
            pid = int(pid_file.read_text())
            deadline = time.monotonic() + 2.0
            alive = True
            while time.monotonic() < deadline:
                stat_path = Path(f"/proc/{pid}/stat")
                if not stat_path.exists():
                    alive = False
                    break
                parts = stat_path.read_text(errors="replace").split()
                if len(parts) > 2 and parts[2] == "Z":
                    alive = False
                    break
                time.sleep(0.05)
            self.assertFalse(alive)


class ExecutePilotTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "posix", "POSIX directory fsync")
    def test_new_journal_parent_directories_are_fsynced(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            original = execute_pilot._fsync_directory
            with mock.patch.object(execute_pilot, "_fsync_directory", wraps=original) as spy:
                output_root = execute_pilot.ensure_output_root(repo.resolve())
                attempt, attempt_dir = execute_pilot.reserve_attempt(output_root, "f" * 64, 2)
            self.assertEqual(attempt, 1)
            self.assertTrue((attempt_dir / "reservation.json").is_file())
            synced = [args[0] for args, _ in (item for item in spy.call_args_list)]
            self.assertIn(repo.parent, synced)  # output directory entry
            self.assertIn(output_root, synced)  # package directory entry
            self.assertIn(output_root / ("f" * 64), synced)  # attempt and lock entries
            self.assertIn(attempt_dir, synced)  # atomic reservation rename

    @unittest.skipUnless(os.name == "posix", "POSIX directory fsync")
    @unittest.skipUnless(os.name == "posix", "POSIX directory fsync")
    def test_reopened_output_root_retries_required_parent_fsync(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            repo.mkdir()
            target_parent = root.resolve()
            original = execute_pilot._fsync_directory
            for run in (1, 2):
                with self.subTest(run=run):
                    def failing(path):
                        if path == target_parent:
                            raise OSError("persistent output parent fsync fault")
                        return original(path)
                    with mock.patch.object(execute_pilot, "_fsync_directory", side_effect=failing):
                        with self.assertRaisesRegex(OSError, "persistent output parent fsync fault"):
                            execute_pilot.ensure_output_root(repo.resolve())
                    self.assertTrue((root / preflight.PILOT_OUTPUT_DESTINATION).is_dir())

    @unittest.skipUnless(os.name == "posix", "POSIX directory fsync")
    def test_reopened_package_root_retries_required_parent_fsync(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            h = "b" * 64
            original = execute_pilot._fsync_directory
            for run in (1, 2):
                with self.subTest(run=run):
                    def failing(path):
                        if path == root:
                            raise OSError("persistent package parent fsync fault")
                        return original(path)
                    with mock.patch.object(execute_pilot, "_fsync_directory", side_effect=failing):
                        with self.assertRaisesRegex(OSError, "persistent package parent fsync fault"):
                            execute_pilot.reserve_attempt(root, h, 1)
                    self.assertTrue((root / h).is_dir())
                    self.assertFalse((root / h / "attempt-001").exists())

    def test_fsync_failure_prevents_durable_reservation_completion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with mock.patch.object(execute_pilot, "_fsync_directory", side_effect=OSError("simulated fsync failure")):
                with self.assertRaisesRegex(OSError, "simulated fsync failure"):
                    execute_pilot.reserve_attempt(root, "a" * 64, 2)
            self.assertFalse((root / ("a" * 64) / "attempt-001" / "reservation.json").exists())

    def test_max_runs_reservation_is_atomic_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            attempt, first = execute_pilot.reserve_attempt(root, "a" * 64, 1)
            self.assertEqual(attempt, 1)
            self.assertTrue(first.is_dir())
            self.assertTrue((first / "reservation.json").is_file())
            with self.assertRaisesRegex(preflight.PreflightError, "unresolved UNKNOWN_OUTCOME"):
                execute_pilot.reserve_attempt(root, "a" * 64, 1)

    def test_failed_result_write_preserves_blocking_reservation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            package_hash = "a" * 64
            attempt, attempt_dir = execute_pilot.reserve_attempt(root, package_hash, 2)
            self.assertEqual(attempt, 1)
            with mock.patch.object(execute_pilot, "atomic_write_json", side_effect=OSError("write failed")):
                execute_pilot._write_result(attempt_dir, {
                    "status": "UNKNOWN_OUTCOME", "attempt": attempt, "package_sha256": package_hash,
                })
            self.assertFalse((attempt_dir / "result.json").exists())
            self.assertTrue((attempt_dir / "reservation.json").is_file())
            with self.assertRaisesRegex(preflight.PreflightError, "unresolved UNKNOWN_OUTCOME"):
                execute_pilot.reserve_attempt(root, package_hash, 2)
            self.assertFalse((root / package_hash / "attempt-002").exists())

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
            target.write_text('{"safe":true}')
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
        self.assertFalse(pycache.exists())

    def test_human_validator_child_does_not_create_bytecode_drift(self):
        pycache = SCRIPTS / "__pycache__"
        if pycache.exists():
            for child in pycache.iterdir():
                child.unlink()
            pycache.rmdir()
        before = git(ROOT, "status", "--porcelain")
        proc = subprocess.run(
            [sys.executable, "-B", "scripts/e0/validate_human_reference_approval.py", "--repo-root", str(ROOT)],
            cwd=ROOT,
            env={"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(git(ROOT, "status", "--porcelain"), before)
        self.assertFalse(pycache.exists())


if __name__ == "__main__":
    unittest.main()
