#!/usr/bin/env python3
"""Validate a versioned human-reference approval binding before merge.

This validator proves only repository facts: attestation structure, 14 ACCEPT decisions,
reviewed-commit existence, exact review-input Git tree entries and bytes, candidate and
approved SHA-256 bindings, semantic-copy materialization, explicit non-authorization
boundaries, and the continued absence of an Evidence Lock. It cannot prove that a human
actually performed or understood the review.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from review_snapshot import DEFAULT_PATHS as REVIEW_PATHS
from review_snapshot import (
    REGULAR_FILE_MODES,
    SNAPSHOT_VERSION,
    SnapshotError,
    build_snapshot,
    read_tree_entry_at_commit,
    run_git,
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
APPROVAL_FORMAT = "velantrim-continuum:e0-human-reference-approval:v0.2"
APPROVAL_SEMANTIC_VERSION = "e0-human-reference-v0.1"
DEFAULT_APPROVAL = "experiments/e0/approval/human-reference-approval.v0.2.json"
EXPECTED_REFERENCES = ("capture_gold", "transfer_oracle")
EXPECTED_DECISIONS = (
    "F1",
    "F2_PRE",
    "F2_POST",
    "F3",
    "F4",
    "F5_PRE",
    "F5_POST",
    "F6",
    "F7",
    "F8_PRE",
    "F8_POST",
    "T-PILOT-01",
    "T-EVIDENCE-01",
    "T-EVIDENCE-02",
)
EXPECTED_BOUNDARY = {
    "human_reference": "HUMAN_REFERENCE_APPROVED",
    "pilot": "NOT_AUTHORIZED",
    "evidence_lock": "NOT_CREATED",
    "e0_c_evidence": "NOT_AUTHORIZED / NOT_RUN",
    "e0_t_evidence": "NOT_AUTHORIZED / NOT_RUN",
    "production_runtime": "NO",
    "production_architecture": "NO",
    "event_sourcing_requirement": "NO",
    "ecosystem_integration": "NO",
}
EXPECTED_BOUNDARY_STATEMENT = (
    "HUMAN_REFERENCE_APPROVED; PILOT = NOT_AUTHORIZED; EVIDENCE_LOCK = NOT_CREATED; "
    "E0_C_EVIDENCE = NOT_AUTHORIZED / NOT_RUN; E0_T_EVIDENCE = NOT_AUTHORIZED / NOT_RUN; "
    "PRODUCTION_RUNTIME = NO; PRODUCTION_ARCHITECTURE = NO; EVENT_SOURCING_REQUIREMENT = NO; "
    "ECOSYSTEM_INTEGRATION = NO"
)
REFERENCE_AUTHORITY_METADATA = frozenset(
    {"authorship_status", "human_approval_required", "warning"}
)


class ValidationError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--approval", type=Path, default=Path(DEFAULT_APPROVAL))
    parser.add_argument("--issue-number", type=int, default=9)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"required approval artifact not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path} must contain a JSON object")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"missing or invalid {field}")
    return value.strip()


def require_sha256(value: Any, field: str) -> str:
    value = require_string(value, field)
    if not SHA256_RE.fullmatch(value):
        raise ValidationError(f"{field} must be a 64-character lowercase SHA-256")
    return value


def require_git_sha(value: Any, field: str) -> str:
    value = require_string(value, field)
    if not GIT_SHA_RE.fullmatch(value):
        raise ValidationError(f"{field} must be a full 40-character lowercase Git SHA")
    return value


def require_timestamp(value: Any, field: str) -> str:
    value = require_string(value, field)
    if not value.endswith("Z"):
        raise ValidationError(f"{field} must be a UTC RFC3339 timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{field} is not a valid RFC3339 timestamp") from exc
    if parsed.utcoffset() is None or parsed.utcoffset().total_seconds() != 0:
        raise ValidationError(f"{field} must be UTC")
    return value


def resolve_repo_file(repo_root: Path, relative_path: Any, field: str, *, prefix: str) -> Path:
    text = require_string(relative_path, field)
    pure = Path(text)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValidationError(f"{field} must be a normalized repository-relative path")
    if not text.startswith(prefix):
        raise ValidationError(f"{field} must begin with {prefix!r}")
    root = repo_root.resolve()
    unresolved = root / text
    if unresolved.is_symlink():
        raise ValidationError(f"{field} must not be a symlink: {text}")
    resolved = unresolved.resolve()
    if root not in resolved.parents:
        raise ValidationError(f"{field} escapes repository root")
    if not resolved.is_file():
        raise ValidationError(f"{field} does not name a regular file: {text}")
    return resolved


def semantic_reference_payload(document: dict[str, Any], version_key: str) -> dict[str, Any]:
    value = copy.deepcopy(document)
    value.pop(version_key, None)
    for key in REFERENCE_AUTHORITY_METADATA:
        value.pop(key, None)
    return value


def validate_decisions(approval: dict[str, Any]) -> None:
    decisions = approval.get("decisions")
    if not isinstance(decisions, dict) or set(decisions) != set(EXPECTED_DECISIONS):
        raise ValidationError("decisions must contain exactly the 14 canonical human review decision IDs")
    for item_id in EXPECTED_DECISIONS:
        entry = decisions[item_id]
        if not isinstance(entry, dict):
            raise ValidationError(f"decisions.{item_id} must be an object")
        if entry.get("decision") != "ACCEPT":
            raise ValidationError(f"decisions.{item_id}.decision must be ACCEPT before approval")
        require_string(entry.get("note"), f"decisions.{item_id}.note")
    if approval.get("open_semantic_revisions") not in ([], None):
        raise ValidationError("open_semantic_revisions must be empty before approval")


def validate_human_provenance_and_boundary(approval: dict[str, Any]) -> None:
    if require_string(approval.get("semantic_version"), "semantic_version") != APPROVAL_SEMANTIC_VERSION:
        raise ValidationError(f"semantic_version must be exactly {APPROVAL_SEMANTIC_VERSION!r}")
    if approval.get("gate_status") != "HUMAN_REFERENCE_APPROVED":
        raise ValidationError("gate_status must be HUMAN_REFERENCE_APPROVED")

    reviewer = approval.get("reviewer")
    if not isinstance(reviewer, dict):
        raise ValidationError("reviewer must be an object")
    reviewer_login = require_string(reviewer.get("github_login"), "reviewer.github_login")

    provenance = approval.get("human_approval_provenance")
    if not isinstance(provenance, dict):
        raise ValidationError("human_approval_provenance must be an object")
    if provenance.get("source") != "GITHUB_ISSUE_9_CANONICAL_CHECKLIST":
        raise ValidationError("human_approval_provenance.source must identify the canonical Issue #9 checklist")
    if require_string(provenance.get("recorded_by_github_login"), "human_approval_provenance.recorded_by_github_login") != reviewer_login:
        raise ValidationError("human approval provenance GitHub login must match reviewer.github_login")
    require_timestamp(provenance.get("issue_updated_at"), "human_approval_provenance.issue_updated_at")
    if provenance.get("required_decisions") != len(EXPECTED_DECISIONS):
        raise ValidationError("human_approval_provenance.required_decisions must be exactly 14")
    if provenance.get("recorded_decisions") != len(EXPECTED_DECISIONS):
        raise ValidationError("human_approval_provenance.recorded_decisions must be exactly 14")
    if provenance.get("all_decisions") != "ACCEPT":
        raise ValidationError("human_approval_provenance.all_decisions must be ACCEPT")

    if approval.get("boundary") != EXPECTED_BOUNDARY:
        raise ValidationError("boundary must preserve the exact human-reference-only non-authorization boundary")
    if require_string(approval.get("boundary_statement"), "boundary_statement") != EXPECTED_BOUNDARY_STATEMENT:
        raise ValidationError("boundary_statement must preserve the exact human-reference-only non-authorization boundary")


def validate_review_binding(
    approval: dict[str, Any], repo_root: Path, reviewed_commit: str
) -> dict[str, dict[str, str]]:
    binding = approval.get("review_snapshot")
    if not isinstance(binding, dict) or set(binding) != {"snapshot_version", "snapshot_sha256", "reviewed_tree"}:
        raise ValidationError("review_snapshot must contain exactly snapshot_version, snapshot_sha256, and reviewed_tree")
    if binding.get("snapshot_version") != SNAPSHOT_VERSION:
        raise ValidationError(f"review_snapshot.snapshot_version must be exactly {SNAPSHOT_VERSION!r}")
    expected_snapshot_hash = require_sha256(binding.get("snapshot_sha256"), "review_snapshot.snapshot_sha256")
    expected_tree = require_git_sha(binding.get("reviewed_tree"), "review_snapshot.reviewed_tree")
    try:
        snapshot = build_snapshot(repo_root, reviewed_commit, REVIEW_PATHS)
    except SnapshotError as exc:
        raise ValidationError(f"reviewed_repository_commit/tree binding invalid: {exc}") from exc
    if snapshot["reviewed_tree"] != expected_tree:
        raise ValidationError("review_snapshot.reviewed_tree does not match reviewed_repository_commit tree")
    if snapshot["snapshot_sha256"] != expected_snapshot_hash:
        raise ValidationError("review_snapshot.snapshot_sha256 does not match exact bytes and Git entries from reviewed_repository_commit")
    return {
        item["path"]: {
            "git_mode": item["git_mode"],
            "git_blob_sha": item["git_blob_sha"],
            "sha256": item["sha256"],
        }
        for item in snapshot["artifacts"]
    }


def validate_recorded_reviewed_paths(
    approval: dict[str, Any], reviewed_artifacts: dict[str, dict[str, str]]
) -> None:
    recorded = approval.get("reviewed_paths")
    if not isinstance(recorded, dict) or set(recorded) != set(REVIEW_PATHS):
        raise ValidationError("reviewed_paths must contain exactly the seven canonical review/control paths")
    for relative in REVIEW_PATHS:
        entry = recorded.get(relative)
        expected = reviewed_artifacts[relative]
        if not isinstance(entry, dict) or set(entry) != {"git_mode", "git_blob_sha", "sha256"}:
            raise ValidationError(f"reviewed_paths.{relative} must contain exactly git_mode, git_blob_sha, and sha256")
        if entry != expected:
            raise ValidationError(f"reviewed_paths.{relative} does not match the independently recomputed reviewed snapshot")


def validate_current_review_inputs(repo_root: Path, reviewed_artifacts: dict[str, dict[str, str]]) -> None:
    if set(reviewed_artifacts) != set(REVIEW_PATHS):
        raise ValidationError("recomputed review snapshot scope differs from the canonical review-input manifest")
    root = repo_root.resolve()
    try:
        current_head = run_git(root, ["rev-parse", "--verify", "HEAD^{commit}"], text=True).stdout.strip()
    except SnapshotError as exc:
        raise ValidationError(f"cannot resolve current approval-head commit: {exc}") from exc

    for relative in REVIEW_PATHS:
        expected = reviewed_artifacts[relative]
        try:
            current_mode, current_type, current_blob = read_tree_entry_at_commit(root, current_head, relative)
        except SnapshotError as exc:
            raise ValidationError(f"current approval-head Git entry invalid for {relative}: {exc}") from exc
        if current_type != "blob" or current_mode not in REGULAR_FILE_MODES:
            raise ValidationError(
                f"current approval-head review input is not a regular Git blob: {relative} ({current_mode} {current_type})"
            )
        if current_mode != expected["git_mode"]:
            raise ValidationError(
                f"current approval-head Git mode differs from reviewed commit for {relative}: {current_mode} != {expected['git_mode']}"
            )
        if current_blob != expected["git_blob_sha"]:
            raise ValidationError(
                f"current approval-head Git blob differs from reviewed commit for {relative}: {current_blob} != {expected['git_blob_sha']}"
            )

        unresolved = root / relative
        if unresolved.is_symlink():
            raise ValidationError(f"current review input is a symlink: {relative}")
        current = unresolved.resolve()
        if root not in current.parents or not current.is_file():
            raise ValidationError(f"current review input is missing or outside repository root: {relative}")
        if sha256_file(current) != expected["sha256"]:
            raise ValidationError(f"current review input differs from reviewed-commit bytes: {relative}")


def validate_reference(
    repo_root: Path,
    name: str,
    value: Any,
    reviewed_artifacts: dict[str, dict[str, str]],
) -> list[str]:
    if not isinstance(value, dict):
        raise ValidationError(f"references.{name} must be an object")
    if name == "capture_gold":
        candidate_prefix = "experiments/e0/gold/candidates/"
        approved_prefix = "experiments/e0/gold/approved/"
        version_key = "gold_version"
    else:
        candidate_prefix = "experiments/e0/oracle/candidates/"
        approved_prefix = "experiments/e0/oracle/approved/"
        version_key = "oracle_version"

    candidate_text = require_string(value.get("candidate_path"), f"references.{name}.candidate_path")
    candidate = resolve_repo_file(repo_root, candidate_text, f"references.{name}.candidate_path", prefix=candidate_prefix)
    candidate_hash = require_sha256(value.get("candidate_sha256"), f"references.{name}.candidate_sha256")
    if sha256_file(candidate) != candidate_hash:
        raise ValidationError(f"references.{name}.candidate_sha256 does not match current {candidate_text}")
    reviewed = reviewed_artifacts.get(candidate_text)
    if reviewed is None:
        raise ValidationError(f"references.{name}.candidate_path is not in the exact review snapshot scope")
    if reviewed["sha256"] != candidate_hash:
        raise ValidationError(f"references.{name}.candidate_sha256 differs from reviewed-commit bytes for {candidate_text}")
    candidate_document = load_json(candidate)
    if candidate_document.get("authorship_status") != "AI_PROPOSED_DRAFT":
        raise ValidationError(f"{candidate_text} must remain AI_PROPOSED_DRAFT")

    approved_text = require_string(value.get("approved_path"), f"references.{name}.approved_path")
    approved = resolve_repo_file(repo_root, approved_text, f"references.{name}.approved_path", prefix=approved_prefix)
    approved_hash = require_sha256(value.get("approved_sha256"), f"references.{name}.approved_sha256")
    if sha256_file(approved) != approved_hash:
        raise ValidationError(f"references.{name}.approved_sha256 does not match {approved_text}")
    document = load_json(approved)
    if document.get("authorship_status") != "HUMAN_APPROVED":
        raise ValidationError(f"{approved_text} must declare authorship_status HUMAN_APPROVED")
    if document.get("human_approval_required") is not False:
        raise ValidationError(f"{approved_text} must set human_approval_required to false after approval")
    artifact_version = require_string(document.get(version_key), f"{approved_text}.{version_key}")
    if require_string(value.get("approved_version"), f"references.{name}.approved_version") != artifact_version:
        raise ValidationError(f"references.{name}.approved_version differs from artifact version")
    if semantic_reference_payload(candidate_document, version_key) != semantic_reference_payload(document, version_key):
        raise ValidationError(f"{approved_text} changes reviewed reference semantics instead of only approval/version metadata")

    return [
        f"{name}: reviewed candidate={candidate_text} sha256={candidate_hash}",
        f"{name}: approved={approved_text} sha256={approved_hash}",
    ]


def validate(approval: dict[str, Any], repo_root: Path, issue_number: int) -> list[str]:
    if approval.get("approval_format") != APPROVAL_FORMAT:
        raise ValidationError(f"approval_format must be exactly {APPROVAL_FORMAT!r}")
    if approval.get("status") != "HUMAN_APPROVED":
        raise ValidationError("status must be HUMAN_APPROVED")

    reviewer = approval.get("reviewer")
    if not isinstance(reviewer, dict):
        raise ValidationError("reviewer must be an object")
    require_string(reviewer.get("name"), "reviewer.name")
    require_string(reviewer.get("role"), "reviewer.role")
    require_timestamp(approval.get("approved_at"), "approved_at")
    validate_human_provenance_and_boundary(approval)

    reviewed_commit = require_git_sha(approval.get("reviewed_repository_commit"), "reviewed_repository_commit")
    reviewed_artifacts = validate_review_binding(approval, repo_root.resolve(), reviewed_commit)
    validate_recorded_reviewed_paths(approval, reviewed_artifacts)
    validate_current_review_inputs(repo_root, reviewed_artifacts)

    issue_url = require_string(approval.get("issue_url"), "issue_url")
    parsed = urlparse(issue_url)
    if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.path.rstrip("/") != f"/velantrian/Velantrim-Continuum/issues/{issue_number}":
        raise ValidationError(f"issue_url must be the canonical GitHub URL for Issue #{issue_number}")

    validate_decisions(approval)

    lock = approval.get("evidence_lock")
    if not isinstance(lock, dict) or lock.get("status") != "NOT_CREATED" or lock.get("sha256") is not None:
        raise ValidationError("approval must keep evidence_lock as {status: NOT_CREATED, sha256: null}")

    references = approval.get("references")
    if not isinstance(references, dict) or set(references) != set(EXPECTED_REFERENCES):
        raise ValidationError("references must contain exactly capture_gold and transfer_oracle")

    messages = [
        f"reviewed_commit={reviewed_commit}",
        f"reviewed_tree={approval['review_snapshot']['reviewed_tree']}",
        f"review_snapshot_sha256={approval['review_snapshot']['snapshot_sha256']}",
    ]
    for name in EXPECTED_REFERENCES:
        messages.extend(validate_reference(repo_root, name, references[name], reviewed_artifacts))
    return messages


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    approval_path = args.approval if args.approval.is_absolute() else root / args.approval
    try:
        messages = validate(load_json(approval_path), root, args.issue_number)
    except ValidationError as exc:
        print(f"HUMAN_REFERENCE_APPROVAL_ERROR: {exc}", file=sys.stderr)
        return 1
    print("HUMAN_REFERENCE_APPROVAL_BINDINGS_VALID: review commit/tree/blob identity, exact bytes, recorded per-path bindings, semantic-copy materialization, attestation structure, explicit non-authorization boundary, and SHA-256 bindings verified.")
    for message in messages:
        print(f"HUMAN_REFERENCE_APPROVAL_BINDING: {message}")
    print("HUMAN_REFERENCE_APPROVAL_BOUNDARY: machine validation does not prove human authorship or semantic correctness; evidence lock remains NOT_CREATED; pilot/evidence/production authority remain ungranted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
