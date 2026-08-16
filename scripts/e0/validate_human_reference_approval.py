#!/usr/bin/env python3
"""Validate a versioned human-reference approval binding before merge.

This validator proves only repository facts: attestation structure, ACCEPT decisions,
exact candidate/approved SHA-256 bindings, approved artifact status/version, and the
continued absence of an Evidence Lock. It cannot prove that a human actually read
or authored the attestation; that remains an external governance fact recorded in
Issue #9 / the approval PR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
APPROVAL_FORMAT = "velantrim-continuum:e0-human-reference-approval:v0.1"
DEFAULT_APPROVAL = "experiments/e0/approval/human-reference-approval.v0.1.json"
EXPECTED_REFERENCES = ("capture_gold", "transfer_oracle")
EXPECTED_DECISIONS = (
    "F1",
    "F2_PRE",
    "F2_POST",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "T-PILOT-01",
    "T-EVIDENCE-01",
    "T-EVIDENCE-02",
    "AUTHORITY_AMBIGUITY_PROVENANCE",
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
    resolved = (root / text).resolve()
    if root not in resolved.parents:
        raise ValidationError(f"{field} escapes repository root")
    if not resolved.is_file():
        raise ValidationError(f"{field} does not name a regular file: {text}")
    return resolved


def validate_decisions(approval: dict[str, Any]) -> None:
    decisions = approval.get("decisions")
    if not isinstance(decisions, dict) or set(decisions) != set(EXPECTED_DECISIONS):
        raise ValidationError("decisions must contain exactly the Issue #9 review decision IDs")
    for item_id in EXPECTED_DECISIONS:
        entry = decisions[item_id]
        if not isinstance(entry, dict):
            raise ValidationError(f"decisions.{item_id} must be an object")
        if entry.get("decision") != "ACCEPT":
            raise ValidationError(f"decisions.{item_id}.decision must be ACCEPT before approval")
        require_string(entry.get("note"), f"decisions.{item_id}.note")
    if approval.get("open_semantic_revisions") not in ([], None):
        raise ValidationError("open_semantic_revisions must be empty before approval")


def validate_reference(repo_root: Path, name: str, value: Any) -> list[str]:
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
        raise ValidationError(f"references.{name}.candidate_sha256 does not match {candidate_text}")
    if load_json(candidate).get("authorship_status") != "AI_PROPOSED_DRAFT":
        raise ValidationError(f"{candidate_text} must remain AI_PROPOSED_DRAFT")

    approved_text = require_string(value.get("approved_path"), f"references.{name}.approved_path")
    approved = resolve_repo_file(repo_root, approved_text, f"references.{name}.approved_path", prefix=approved_prefix)
    approved_hash = require_sha256(value.get("approved_sha256"), f"references.{name}.approved_sha256")
    if sha256_file(approved) != approved_hash:
        raise ValidationError(f"references.{name}.approved_sha256 does not match {approved_text}")
    document = load_json(approved)
    if document.get("authorship_status") != "HUMAN_APPROVED":
        raise ValidationError(f"{approved_text} must declare authorship_status HUMAN_APPROVED")
    artifact_version = require_string(document.get(version_key), f"{approved_text}.{version_key}")
    if require_string(value.get("approved_version"), f"references.{name}.approved_version") != artifact_version:
        raise ValidationError(f"references.{name}.approved_version differs from artifact version")

    return [
        f"{name}: candidate={candidate_text} sha256={candidate_hash}",
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

    reviewed_commit = require_string(approval.get("reviewed_repository_commit"), "reviewed_repository_commit")
    if not COMMIT_RE.fullmatch(reviewed_commit):
        raise ValidationError("reviewed_repository_commit must be a 40-character lowercase Git SHA")

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

    messages: list[str] = []
    for name in EXPECTED_REFERENCES:
        messages.extend(validate_reference(repo_root, name, references[name]))
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
    print("HUMAN_REFERENCE_APPROVAL_BINDINGS_VALID: attestation structure and SHA-256 bindings verified.")
    for message in messages:
        print(f"HUMAN_REFERENCE_APPROVAL_BINDING: {message}")
    print("HUMAN_REFERENCE_APPROVAL_BOUNDARY: machine validation does not prove human authorship; evidence lock remains NOT_CREATED; no pilot/evidence authorized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
