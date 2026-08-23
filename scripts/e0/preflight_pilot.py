#!/usr/bin/env python3
"""Fail-closed preflight for an explicitly owner-authorized E0 Pilot.

This module grants no authority. A future Pilot can run only when canonical state
binds an immutable manifest blob from package commit A and the current activation
commit B is the direct child of A with a bounded governance-only diff.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
APPROVAL_PATH = "experiments/e0/approval/human-reference-approval.v0.2.json"
PROJECT_STATE_PATH = "project-state.json"
CAPTURE_PILOT_PATH = "experiments/e0/fixtures/capture/pilot/fixtures.json"
TRANSFER_PATH = "experiments/e0/fixtures/transfer/scenarios.json"
ALLOWED_POSTURES = {"UNCONTROLLED_LOCAL_ADVISORY"}
PILOT_OUTPUT_DESTINATION = ".velantrim-continuum-pilot-runs"
PILOT_MANIFEST_PREFIX = "experiments/e0/pilot/"
FORBIDDEN_SECRET_KEYS = {"api_key", "token", "secret", "password", "credential_secret_value"}
AUTHORIZED_PILOT_STATE = "AUTHORIZED_BOUNDED_PILOT"
AUTHORIZATION_PACKAGE_STATE = "AUTHORIZED_BOUNDED_PILOT_PACKAGE"
ACTIVATION_POLICY = "DIRECT_CHILD_ONLY"
ACTIVATION_PATHS_DEFAULT = {
    PROJECT_STATE_PATH,
    "STATUS.md",
    "docs/ai/CURRENT_STATE.md",
    "docs/research/OD_PILOT_01_DRAFT.md",
}
OBSOLETE_SELF_REFERENTIAL_FIELDS = {
    "execution_head_commit",
    "execution_tree",
    "authorization_base_commit",
    "authorization_base_tree",
}


class PreflightError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise PreflightError(f"cannot load JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PreflightError(f"{path} must contain a JSON object")
    return value


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PreflightError(f"missing/invalid {field}")
    return value.strip()


def require_sha(value: Any, field: str) -> str:
    text = require_string(value, field)
    if not GIT_SHA_RE.fullmatch(text):
        raise PreflightError(f"{field} must be a lowercase 40-character Git SHA")
    return text


def require_sha256(value: Any, field: str) -> str:
    text = require_string(value, field)
    if not SHA256_RE.fullmatch(text):
        raise PreflightError(f"{field} must be a lowercase SHA-256")
    return text


def run_git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise PreflightError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def ensure_clean_worktree(root: Path) -> None:
    dirty = run_git(root, "status", "--porcelain")
    if dirty:
        raise PreflightError(f"execution worktree is not clean: {dirty.splitlines()[0]}")


def reject_secret_material(value: Any, path: str = "manifest") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized in FORBIDDEN_SECRET_KEYS or normalized.endswith("_api_key") or normalized.endswith("_token"):
                raise PreflightError(f"secret-bearing field forbidden in Pilot manifest: {path}.{key}")
            reject_secret_material(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_secret_material(child, f"{path}[{index}]")


def pilot_ids(root: Path) -> set[str]:
    capture = load_json(root / CAPTURE_PILOT_PATH)
    transfer = load_json(root / TRANSFER_PATH)
    ids = {item.get("fixture_id") for item in capture.get("fixtures", []) if item.get("fixture_id")}
    ids.update(
        item.get("scenario_id")
        for item in transfer.get("scenarios", [])
        if item.get("partition") == "PILOT" and item.get("scenario_id")
    )
    return ids


def evidence_ids(root: Path) -> set[str]:
    evidence_capture = load_json(root / "experiments/e0/fixtures/capture/evidence/fixtures.json")
    transfer = load_json(root / TRANSFER_PATH)
    ids = {item.get("fixture_id") for item in evidence_capture.get("fixtures", []) if item.get("fixture_id")}
    ids.update(
        item.get("scenario_id")
        for item in transfer.get("scenarios", [])
        if item.get("partition") == "EVIDENCE" and item.get("scenario_id")
    )
    return ids


def canonical_manifest_path(root: Path, manifest_path: Path) -> str:
    if manifest_path.is_symlink():
        raise PreflightError("authorized Pilot manifest must not be a symlink")
    resolved = manifest_path.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise PreflightError("authorized Pilot manifest must be a repository-relative canonical artifact") from exc
    path = relative.as_posix()
    if not path.startswith(PILOT_MANIFEST_PREFIX):
        raise PreflightError(f"authorized Pilot manifest must live under {PILOT_MANIFEST_PREFIX}")
    return path


def require_manifest_blob_at_base(
    root: Path,
    manifest_path: Path,
    base_commit: str,
    expected_sha256: str,
) -> str:
    relative = canonical_manifest_path(root, manifest_path)
    entry = run_git(root, "ls-tree", base_commit, "--", relative)
    if not entry:
        raise PreflightError("authorized manifest is absent from authorization package commit")
    metadata, _, returned_path = entry.partition("\t")
    parts = metadata.split()
    if len(parts) != 3 or parts[0] != "100644" or parts[1] != "blob" or returned_path != relative:
        raise PreflightError("authorized manifest must be a regular non-executable Git blob at package commit")
    proc = subprocess.run(
        ["git", "show", f"{base_commit}:{relative}"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise PreflightError("cannot read authorized manifest blob from package commit")
    if sha256_bytes(proc.stdout) != expected_sha256:
        raise PreflightError("authorization package manifest bytes do not match canonical manifest SHA-256")
    return relative


def require_activation_paths(value: Any) -> set[str]:
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
        raise PreflightError("experiment_0_pilot_authorization.activation_paths must be a non-empty string list")
    if len(value) != len(set(value)):
        raise PreflightError("experiment_0_pilot_authorization.activation_paths must not contain duplicates")
    paths = set(value)
    if not paths.issubset(ACTIVATION_PATHS_DEFAULT):
        raise PreflightError("canonical Pilot activation_paths exceed bounded governance paths")
    if PROJECT_STATE_PATH not in paths:
        raise PreflightError("canonical Pilot activation_paths must include project-state.json")
    return paths


def require_direct_activation(
    root: Path,
    *,
    authorization: dict[str, Any],
    manifest: dict[str, Any],
    manifest_path: Path,
    manifest_sha256: str,
) -> dict[str, Any]:
    base_commit = require_sha(
        authorization.get("authorization_base_commit"),
        "experiment_0_pilot_authorization.authorization_base_commit",
    )
    base_tree = require_sha(
        authorization.get("authorization_base_tree"),
        "experiment_0_pilot_authorization.authorization_base_tree",
    )
    if authorization.get("activation_policy") != ACTIVATION_POLICY:
        raise PreflightError(f"canonical Pilot activation_policy must be {ACTIVATION_POLICY}")
    if manifest.get("activation_policy") != ACTIVATION_POLICY:
        raise PreflightError("manifest activation_policy does not match canonical package authorization")
    allowed_paths = require_activation_paths(authorization.get("activation_paths"))

    actual_base_tree = run_git(root, "rev-parse", f"{base_commit}^{{tree}}")
    if actual_base_tree != base_tree:
        raise PreflightError("canonical authorization base tree does not match package commit")

    manifest_rel = require_manifest_blob_at_base(root, manifest_path, base_commit, manifest_sha256)
    if manifest_rel in allowed_paths:
        raise PreflightError("authorized manifest must not be mutable during activation commit")

    head = run_git(root, "rev-parse", "HEAD")
    parents = run_git(root, "show", "-s", "--format=%P", "HEAD").split()
    if parents != [base_commit]:
        raise PreflightError("activation HEAD must be the direct child of authorization package commit")
    activation_tree = run_git(root, "rev-parse", "HEAD^{tree}")

    changed_text = run_git(root, "diff", "--name-only", "--no-renames", f"{base_commit}..{head}")
    changed_paths = {item for item in changed_text.splitlines() if item}
    forbidden = sorted(changed_paths - allowed_paths)
    if forbidden:
        raise PreflightError(f"activation commit changed files outside declared bounded authorization paths: {forbidden}")
    if PROJECT_STATE_PATH not in changed_paths:
        raise PreflightError("activation commit must materialize canonical project-state authorization")

    ensure_clean_worktree(root)
    return {
        "authorization_base_commit": base_commit,
        "authorization_base_tree": base_tree,
        "activation_head_commit": head,
        "activation_tree": activation_tree,
        "activation_paths": sorted(changed_paths),
        "manifest_path": manifest_rel,
        "manifest_sha256": manifest_sha256,
    }


def validate_canonical_authorization(
    root: Path,
    *,
    manifest: dict[str, Any] | None = None,
    manifest_path: Path | None = None,
    manifest_sha256: str | None = None,
) -> dict[str, Any]:
    state = load_json(root / PROJECT_STATE_PATH)
    status = state.get("experiment_0_pilot_status")
    if status != AUTHORIZED_PILOT_STATE:
        raise PreflightError(
            f"canonical project state does not authorize Pilot: experiment_0_pilot_status={status!r}; "
            f"expected {AUTHORIZED_PILOT_STATE!r}"
        )
    if state.get("experiment_0_evidence_lock_sha") is not None:
        raise PreflightError("canonical project state must keep Evidence Lock absent for Pilot")
    if state.get("experiment_0_evidence_ready") is not False:
        raise PreflightError("Pilot authorization must not set experiment_0_evidence_ready=true")
    if state.get("e0c_started") is not False or state.get("e0t_started") is not False:
        raise PreflightError("Pilot authorization must not mark E0-C/E0-T Evidence started")

    authorization = state.get("experiment_0_pilot_authorization")
    if not isinstance(authorization, dict):
        raise PreflightError("canonical Pilot authorization package binding is absent")
    if authorization.get("status") != AUTHORIZATION_PACKAGE_STATE:
        raise PreflightError("canonical Pilot authorization package status is invalid")
    require_string(authorization.get("authorization_id"), "experiment_0_pilot_authorization.authorization_id")
    approved_path = require_string(authorization.get("manifest_path"), "experiment_0_pilot_authorization.manifest_path")
    approved_sha = require_sha256(authorization.get("manifest_sha256"), "experiment_0_pilot_authorization.manifest_sha256")

    if manifest is None or manifest_path is None or manifest_sha256 is None:
        raise PreflightError("exact manifest bytes/path are required for canonical Pilot authorization binding")
    actual_path = canonical_manifest_path(root, manifest_path)
    if actual_path != approved_path or manifest_sha256 != approved_sha:
        raise PreflightError("Pilot manifest does not match canonical owner-approved package binding")

    provenance = require_direct_activation(
        root,
        authorization=authorization,
        manifest=manifest,
        manifest_path=manifest_path,
        manifest_sha256=manifest_sha256,
    )
    result = dict(authorization)
    result["_verified_activation"] = provenance
    return result


def validate_manifest(
    manifest: dict[str, Any],
    root: Path,
    *,
    manifest_path: Path | None = None,
    manifest_sha256: str | None = None,
    check_git: bool = True,
    check_authority_state: bool = True,
) -> list[str]:
    reject_secret_material(manifest)
    obsolete = sorted(OBSOLETE_SELF_REFERENTIAL_FIELDS & set(manifest))
    if obsolete:
        raise PreflightError(f"obsolete self-referential Pilot manifest fields are forbidden: {obsolete}")
    if manifest.get("activation_policy") != ACTIVATION_POLICY:
        raise PreflightError(f"manifest activation_policy must be {ACTIVATION_POLICY}")

    authorization: dict[str, Any] | None = None
    provenance: dict[str, Any] | None = None
    if check_authority_state:
        authorization = validate_canonical_authorization(
            root,
            manifest=manifest,
            manifest_path=manifest_path,
            manifest_sha256=manifest_sha256,
        )
        provenance = authorization.get("_verified_activation")
    elif check_git:
        raise PreflightError("Git activation validation requires canonical authority state")

    if manifest.get("run_type") != "PILOT" or manifest.get("label") != "PILOT — NOT EVIDENCE":
        raise PreflightError("manifest must be explicitly labelled PILOT — NOT EVIDENCE")
    if manifest.get("owner_decision_id") != "OD-PILOT-01":
        raise PreflightError("owner_decision_id must be OD-PILOT-01")
    if manifest.get("owner_decision_status") != "ADOPTED":
        raise PreflightError("Pilot is not authorized: owner_decision_status must be ADOPTED")
    require_string(manifest.get("owner_github_login"), "owner_github_login")
    require_string(manifest.get("owner_adopted_at"), "owner_adopted_at")

    approval = manifest.get("human_approval")
    if not isinstance(approval, dict) or approval.get("path") != APPROVAL_PATH:
        raise PreflightError(f"human_approval.path must be {APPROVAL_PATH}")
    approval_hash = require_sha256(approval.get("sha256"), "human_approval.sha256")
    if sha256_file(root / APPROVAL_PATH) != approval_hash:
        raise PreflightError("human approval record hash mismatch")

    refs = manifest.get("approved_references")
    if not isinstance(refs, list) or not refs:
        raise PreflightError("approved_references must be a non-empty list")
    allowed_ref_paths = {
        "experiments/e0/gold/approved/capture-gold.v0.1.json",
        "experiments/e0/oracle/approved/transfer-oracle.v0.1.json",
    }
    for index, ref in enumerate(refs):
        if not isinstance(ref, dict):
            raise PreflightError(f"approved_references[{index}] must be an object")
        path = require_string(ref.get("path"), f"approved_references[{index}].path")
        if path not in allowed_ref_paths:
            raise PreflightError(f"unapproved reference path: {path}")
        expected_hash = require_sha256(ref.get("sha256"), f"approved_references[{index}].sha256")
        if sha256_file(root / path) != expected_hash:
            raise PreflightError(f"approved reference hash mismatch: {path}")

    requested = manifest.get("fixture_or_scenario_ids")
    if not isinstance(requested, list) or not requested or any(not isinstance(item, str) for item in requested):
        raise PreflightError("fixture_or_scenario_ids must be a non-empty string list")
    known_pilot = pilot_ids(root)
    forbidden_ids = evidence_ids(root)
    if set(requested) & forbidden_ids:
        raise PreflightError("Evidence fixture/scenario requested by Pilot manifest")
    unknown = set(requested) - known_pilot
    if unknown:
        raise PreflightError(f"unknown/non-Pilot fixture or scenario IDs: {sorted(unknown)}")

    posture = manifest.get("execution_posture")
    if posture == "ISOLATED_RUNNER_CONTRACT":
        raise PreflightError(
            "ISOLATED_RUNNER_CONTRACT is not implemented or contract-bound; only UNCONTROLLED_LOCAL_ADVISORY is currently supported"
        )
    if posture not in ALLOWED_POSTURES:
        raise PreflightError("invalid execution_posture")
    expected_isolation = {
        "isolation_enforcement": "NOT_ENFORCED",
        "network_isolation": "NOT_ENFORCED",
        "filesystem_isolation": "NOT_ENFORCED",
        "process_isolation": "NOT_ENFORCED",
    }
    if manifest.get("isolation") != expected_isolation:
        raise PreflightError("UNCONTROLLED_LOCAL_ADVISORY must explicitly declare all isolation guarantees NOT_ENFORCED")

    limits = manifest.get("limits")
    if not isinstance(limits, dict):
        raise PreflightError("limits must be an object")
    for field in ("timeout_seconds", "max_output_bytes", "max_runs"):
        value = limits.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise PreflightError(f"limits.{field} must be a positive integer")

    if manifest.get("evidence_lock") != {"status": "NOT_CREATED", "sha256": None}:
        raise PreflightError("Pilot manifest must keep Evidence Lock NOT_CREATED")

    model = manifest.get("model")
    if not isinstance(model, dict):
        raise PreflightError("model must be an object")
    require_string(model.get("provider"), "model.provider")
    require_string(model.get("identifier"), "model.identifier")
    if not isinstance(model.get("settings"), dict):
        raise PreflightError("model.settings must be an object")
    credentials = manifest.get("credentials")
    if not isinstance(credentials, dict):
        raise PreflightError("credentials must be an object")
    require_string(credentials.get("profile"), "credentials.profile")
    require_string(credentials.get("scope"), "credentials.scope")
    require_string(manifest.get("adapter_command"), "adapter_command")
    require_sha256(manifest.get("request_sha256"), "request_sha256")

    adapter_cwd = require_string(manifest.get("adapter_cwd"), "adapter_cwd")
    adapter_cwd_path = Path(adapter_cwd)
    if adapter_cwd_path.is_absolute() or ".." in adapter_cwd_path.parts:
        raise PreflightError("adapter_cwd must be a normalized repository-relative path without parent traversal")

    env_allowlist = manifest.get("environment_allowlist")
    if not isinstance(env_allowlist, list) or any(not isinstance(item, str) or not ENV_NAME_RE.fullmatch(item) for item in env_allowlist):
        raise PreflightError("environment_allowlist must be a list of valid environment variable names")
    if len(env_allowlist) != len(set(env_allowlist)):
        raise PreflightError("environment_allowlist must not contain duplicates")

    output_destination = require_string(manifest.get("output_destination"), "output_destination")
    if output_destination != PILOT_OUTPUT_DESTINATION:
        raise PreflightError(
            f"output_destination must be the dedicated non-repository Pilot root {PILOT_OUTPUT_DESTINATION!r}"
        )

    return [
        f"authorization_base={provenance['authorization_base_commit'] if provenance else '<unbound>'}",
        f"authorization_base_tree={provenance['authorization_base_tree'] if provenance else '<unbound>'}",
        f"activation_head={provenance['activation_head_commit'] if provenance else '<unchecked>'}",
        f"activation_tree={provenance['activation_tree'] if provenance else '<unchecked>'}",
        f"activation_paths={','.join(provenance['activation_paths']) if provenance else '<unchecked>'}",
        f"pilot_ids={','.join(requested)}",
        f"posture={posture}",
    ]


def validate_human_approval(root: Path) -> None:
    child_env = {"PYTHONDONTWRITEBYTECODE": "1"}
    if "PATH" in os.environ:
        child_env["PATH"] = os.environ["PATH"]
    proc = subprocess.run(
        [sys.executable, "-B", "scripts/e0/validate_human_reference_approval.py", "--repo-root", str(root)],
        cwd=root,
        env=child_env,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0 or "HUMAN_REFERENCE_APPROVAL_BINDINGS_VALID" not in proc.stdout:
        raise PreflightError(f"human-reference approval validator failed: {(proc.stderr or proc.stdout).strip()}")
    ensure_clean_worktree(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    try:
        ensure_clean_worktree(root)
        manifest_bytes = manifest_path.read_bytes()
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        if not isinstance(manifest, dict):
            raise PreflightError("Pilot manifest must contain a JSON object")
        messages = validate_manifest(
            manifest,
            root,
            manifest_path=manifest_path,
            manifest_sha256=sha256_bytes(manifest_bytes),
        )
        validate_human_approval(root)
        ensure_clean_worktree(root)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, PreflightError) as exc:
        print(f"PILOT_PREFLIGHT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("PILOT_PREFLIGHT_VALID: exact package blob binding and direct-child bounded activation are valid.")
    for message in messages:
        print(f"PILOT_PREFLIGHT_BINDING: {message}")
    print("PILOT_PREFLIGHT_BOUNDARY: this check does not create Evidence Lock, authorize Evidence, or prove sandbox isolation/scientific validity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
