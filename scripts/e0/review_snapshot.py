#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_VERSION = "0.3"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_PATHS = [
    "experiments/e0/review/ISSUE_9_HUMAN_REVIEW_PROTOCOL.md",
    "docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md",
    "experiments/e0/fixtures/capture/pilot/fixtures.json",
    "experiments/e0/fixtures/capture/evidence/fixtures.json",
    "experiments/e0/fixtures/transfer/scenarios.json",
    "experiments/e0/gold/candidates/capture-gold.ai-proposed.json",
    "experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json",
]


class SnapshotError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_repo_relative_path(relative: str) -> str:
    if not isinstance(relative, str) or not relative or "\x00" in relative:
        raise SnapshotError("review path must be a non-empty repository-relative string")
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise SnapshotError(f"review path must be normalized and repository-relative: {relative!r}")
    normalized = path.as_posix()
    if normalized != relative or normalized in ("", "."):
        raise SnapshotError(f"review path must be normalized and repository-relative: {relative!r}")
    return normalized


def run_git(repo_root: Path, args: list[str], *, text: bool = False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root.resolve()), *args],
            check=True,
            capture_output=True,
            text=text,
        )
    except FileNotFoundError as exc:
        raise SnapshotError("git executable is required for commit-tree review binding") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if isinstance(exc.stderr, str) else exc.stderr.decode("utf-8", errors="replace").strip()
        detail = f": {stderr}" if stderr else ""
        raise SnapshotError(f"git command failed ({' '.join(args)}){detail}") from exc


def resolve_commit(repo_root: Path, reviewed_commit: str) -> str:
    if not COMMIT_RE.fullmatch(reviewed_commit):
        raise SnapshotError("reviewed_commit must be a full 40-character lowercase Git commit SHA")
    resolved = run_git(repo_root, ["rev-parse", "--verify", f"{reviewed_commit}^{{commit}}"], text=True).stdout.strip()
    if resolved != reviewed_commit:
        raise SnapshotError("reviewed_commit must resolve exactly to the supplied full commit SHA")
    return resolved


def commit_tree_sha(repo_root: Path, reviewed_commit: str) -> str:
    return run_git(repo_root, ["rev-parse", "--verify", f"{reviewed_commit}^{{tree}}"], text=True).stdout.strip()


def read_blob_at_commit(repo_root: Path, reviewed_commit: str, relative: str) -> tuple[bytes, str]:
    relative = normalize_repo_relative_path(relative)
    listing = run_git(repo_root, ["ls-tree", "-z", "--full-tree", reviewed_commit, "--", relative]).stdout
    records = [record for record in listing.split(b"\x00") if record]
    if len(records) != 1:
        raise SnapshotError(f"reviewed commit does not contain exactly one tracked artifact at {relative!r}")
    try:
        metadata, raw_path = records[0].split(b"\t", 1)
        mode, object_type, object_sha = metadata.decode("ascii").split(" ", 2)
        listed_path = raw_path.decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise SnapshotError(f"could not parse Git tree entry for {relative!r}") from exc
    if listed_path != relative:
        raise SnapshotError(f"Git tree path mismatch for {relative!r}")
    if object_type != "blob" or mode == "160000":
        raise SnapshotError(f"reviewed artifact must be a Git blob, not {object_type}: {relative!r}")
    data = run_git(repo_root, ["cat-file", "blob", object_sha]).stdout
    return data, object_sha


def canonical_snapshot_bytes(snapshot: dict) -> bytes:
    material = {key: value for key, value in snapshot.items() if key != "snapshot_sha256"}
    return json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build_snapshot(repo_root: Path, reviewed_commit: str, paths: list[str]) -> dict:
    root = repo_root.resolve()
    commit = resolve_commit(root, reviewed_commit)
    tree = commit_tree_sha(root, commit)
    artifacts = []
    seen: set[str] = set()
    for relative in paths:
        normalized = normalize_repo_relative_path(relative)
        if normalized in seen:
            raise SnapshotError(f"duplicate review artifact path: {normalized}")
        seen.add(normalized)
        data, blob_sha = read_blob_at_commit(root, commit, normalized)
        artifacts.append({"path": normalized, "git_blob_sha": blob_sha, "sha256": sha256_bytes(data)})
    snapshot = {
        "snapshot_version": SNAPSHOT_VERSION,
        "purpose": "ISSUE_9_HUMAN_REFERENCE_REVIEW_INPUT",
        "reviewed_commit": commit,
        "reviewed_tree": tree,
        "candidate_status_required": "AI_PROPOSED_DRAFT",
        "artifacts": artifacts,
    }
    snapshot["snapshot_sha256"] = sha256_bytes(canonical_snapshot_bytes(snapshot))
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--reviewed-commit", required=True)
    parser.add_argument("--output", default="-")
    args = parser.parse_args()

    try:
        snapshot = build_snapshot(Path(args.repo_root), args.reviewed_commit, DEFAULT_PATHS)
    except SnapshotError as exc:
        parser.error(str(exc))
    rendered = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    if args.output == "-":
        print(rendered, end="")
    else:
        Path(args.output).write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
