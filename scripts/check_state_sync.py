#!/usr/bin/env python3
"""Fail-closed repository state reconciliation for Velantrim Continuum.

This checker validates three independent properties:

* live GitHub lifecycle facts for the tracked PR;
* provenance lineage from the reviewed base to current ``main``;
* atomic file-level updates of the primary state and always-derived volatile
  state surfaces.

It does not choose milestones, start Experiment 0, authorize runtime work, or
publish to Notion.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from state_sync_rules import (
    GitHubLifecycle,
    read_derived_state_surfaces,
    read_expected_lifecycle,
    read_provenance_base,
    validate_github_lifecycle,
    validate_internal_lifecycle_records,
    validate_provenance_lineage,
    validate_state_bundle,
)


GITHUB_API = "https://api.github.com"


class ConfigurationError(RuntimeError):
    pass


class RemoteServiceError(RuntimeError):
    pass


@dataclass(frozen=True)
class SyncConfig:
    repository: str
    branch: str
    tracked_pr_number: int


@dataclass(frozen=True)
class GitHubSnapshot:
    head_sha: str
    pr_number: int
    canonical_pr_state: str
    merged_at: str | None
    merge_commit_sha: str | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state-file",
        type=Path,
        default=Path("project-state.json"),
        help="Path to the semantic project-state JSON.",
    )
    parser.add_argument(
        "--changed-files-file",
        type=Path,
        help="UTF-8 file with one repository-relative changed path per line.",
    )
    parser.add_argument(
        "--mode",
        choices=("check",),
        default="check",
        help="Only read-only check mode is supported by this repository gate.",
    )
    return parser.parse_args()


def request_json(
    method: str,
    url: str,
    headers: dict[str, str],
) -> dict[str, Any]:
    request = Request(url, method=method, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RemoteServiceError(
            f"GitHub request failed with HTTP {exc.code}: {detail}"
        ) from exc
    except (URLError, TimeoutError) as exc:
        raise RemoteServiceError(f"GitHub request failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RemoteServiceError("GitHub returned invalid JSON.") from exc

    if not isinstance(payload, dict):
        raise RemoteServiceError("GitHub returned an unexpected non-object payload.")
    return payload


def github_headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "velantrim-continuum-state-sync",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def load_state(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigurationError(f"State file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"State file is invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ConfigurationError("State file root must be a JSON object.")
    return payload


def load_sync_config(state: dict[str, Any]) -> SyncConfig:
    sync = state.get("state_sync")
    if not isinstance(sync, dict):
        raise ConfigurationError("state_sync must be an object.")
    github = sync.get("github")
    if not isinstance(github, dict):
        raise ConfigurationError("state_sync.github must be an object.")

    repository = github.get("repository")
    branch = github.get("branch")
    if not isinstance(repository, str) or repository.count("/") != 1:
        raise ConfigurationError(
            "state_sync.github.repository must use owner/repository form."
        )
    if not isinstance(branch, str) or not branch.strip():
        raise ConfigurationError("state_sync.github.branch must be non-empty.")

    try:
        tracked_pr_number, _, _ = read_expected_lifecycle(state)
    except ValueError as exc:
        raise ConfigurationError(str(exc)) from exc

    return SyncConfig(
        repository=repository,
        branch=branch.strip(),
        tracked_pr_number=tracked_pr_number,
    )


def _repo_api_path(repository: str) -> str:
    owner, repo = repository.split("/", 1)
    return f"{quote(owner, safe='')}/{quote(repo, safe='')}"


def canonical_pr_state(payload: dict[str, Any]) -> str:
    if payload.get("merged_at") is not None:
        return "MERGED"
    state = payload.get("state")
    if state == "open":
        return "OPEN"
    if state == "closed":
        return "CLOSED_UNMERGED"
    raise RemoteServiceError(f"GitHub returned unsupported PR state: {state!r}")


def fetch_github_snapshot(
    config: SyncConfig,
    token: str | None,
) -> GitHubSnapshot:
    repo_path = _repo_api_path(config.repository)
    headers = github_headers(token)

    commit = request_json(
        "GET",
        f"{GITHUB_API}/repos/{repo_path}/commits/{quote(config.branch, safe='')}",
        headers,
    )
    head_sha = commit.get("sha")
    if not isinstance(head_sha, str) or len(head_sha) != 40:
        raise RemoteServiceError("GitHub branch response is missing a valid HEAD SHA.")

    pr = request_json(
        "GET",
        f"{GITHUB_API}/repos/{repo_path}/pulls/{config.tracked_pr_number}",
        headers,
    )
    merge_commit_sha = pr.get("merge_commit_sha")
    if merge_commit_sha is not None and not isinstance(merge_commit_sha, str):
        raise RemoteServiceError("GitHub PR returned an invalid merge_commit_sha.")
    merged_at = pr.get("merged_at")
    if merged_at is not None and not isinstance(merged_at, str):
        raise RemoteServiceError("GitHub PR returned an invalid merged_at.")

    return GitHubSnapshot(
        head_sha=head_sha,
        pr_number=config.tracked_pr_number,
        canonical_pr_state=canonical_pr_state(pr),
        merged_at=merged_at,
        merge_commit_sha=merge_commit_sha,
    )


def fetch_compare_status(
    config: SyncConfig,
    base_sha: str,
    head_sha: str,
    token: str | None,
) -> str:
    repo_path = _repo_api_path(config.repository)
    payload = request_json(
        "GET",
        f"{GITHUB_API}/repos/{repo_path}/compare/"
        f"{quote(base_sha, safe='')}...{quote(head_sha, safe='')}",
        github_headers(token),
    )
    status = payload.get("status")
    if status not in {"identical", "ahead", "behind", "diverged"}:
        raise RemoteServiceError(
            f"GitHub Compare returned an unknown status: {status!r}"
        )
    return status


def read_changed_files(path: Path | None) -> list[str]:
    if path is None:
        return []
    try:
        return [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except FileNotFoundError as exc:
        raise ConfigurationError(f"Changed-files file not found: {path}") from exc


def compare_state(
    state: dict[str, Any],
    snapshot: GitHubSnapshot,
    compare_status: str,
    changed_files: list[str],
) -> list[str]:
    live_lifecycle = GitHubLifecycle(
        pr_number=snapshot.pr_number,
        state=snapshot.canonical_pr_state,
        merged_at=snapshot.merged_at,
        merge_commit_sha=snapshot.merge_commit_sha,
    )

    try:
        errors = validate_internal_lifecycle_records(state)
        errors += validate_github_lifecycle(state, live_lifecycle)

        base_sha = read_provenance_base(state)
        errors += validate_provenance_lineage(
            compare_status,
            base_sha,
            snapshot.head_sha,
        )

        if changed_files:
            errors += validate_state_bundle(
                changed_files,
                read_derived_state_surfaces(state),
            )
    except ValueError as exc:
        raise ConfigurationError(str(exc)) from exc
    return errors


def main() -> int:
    args = parse_args()
    try:
        state = load_state(args.state_file)
        config = load_sync_config(state)
        token = os.environ.get("GITHUB_TOKEN")

        snapshot = fetch_github_snapshot(config, token)
        base_sha = read_provenance_base(state)
        compare_status = fetch_compare_status(
            config,
            base_sha,
            snapshot.head_sha,
            token,
        )
        changed_files = read_changed_files(args.changed_files_file)
        mismatches = compare_state(
            state,
            snapshot,
            compare_status,
            changed_files,
        )
    except (ConfigurationError, RemoteServiceError, ValueError) as exc:
        print(f"STATE_SYNC_ERROR: {exc}", file=sys.stderr)
        return 2

    print(
        "STATE_SYNC_SNAPSHOT "
        f"repository={config.repository} "
        f"branch={config.branch} "
        f"head={snapshot.head_sha} "
        f"pr={snapshot.pr_number} "
        f"pr_state={snapshot.canonical_pr_state} "
        f"compare={compare_status}"
    )

    if mismatches:
        for mismatch in mismatches:
            print(f"STATE_SYNC_MISMATCH: {mismatch}", file=sys.stderr)
        return 1

    if not changed_files:
        print(
            "STATE_SYNC_OK: lifecycle and provenance valid; "
            "state-bundle check skipped because no changed-files list was supplied."
        )
    else:
        print("STATE_SYNC_OK: lifecycle, provenance, and state-bundle checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
