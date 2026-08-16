"""Pure validation rules for scripts/check_state_sync.py.

The rules deliberately keep three invariants separate:

1. GitHub lifecycle reconciliation: live PR facts must match the committed
   lifecycle expectation.
2. Provenance lineage: the reviewed base must remain in the ancestry of
   current ``main``; later non-semantic commits are allowed.
3. State-bundle integrity: when the primary semantic state file changes, all
   declared derived state surfaces must change with it, and vice versa.

A new README-only, translation-only, or engineering-only commit may advance
``main`` without changing semantic project state. It must not fail solely
because HEAD is newer than the previously reviewed base SHA.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable


@dataclass(frozen=True)
class GitHubLifecycle:
    pr_number: int
    state: str  # OPEN, MERGED, or CLOSED_UNMERGED
    merged_at: str | None
    merge_commit_sha: str | None


ALLOWED_PR_STATES = frozenset({"OPEN", "MERGED", "CLOSED_UNMERGED"})
ALLOWED_COMPARE_STATUSES = frozenset({"identical", "ahead"})
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_UTC_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def _as_nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _as_positive_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValueError(f"{field} must be a positive integer")
    return value


def _as_sha(value: Any, field: str) -> str:
    text = _as_nonempty_string(value, field)
    if not _SHA_RE.fullmatch(text):
        raise ValueError(f"{field} must be a 40-character lowercase Git SHA")
    return text


def _as_utc_timestamp(value: Any, field: str) -> str:
    text = _as_nonempty_string(value, field)
    if not _UTC_TS_RE.fullmatch(text):
        raise ValueError(f"{field} must be an ISO-8601 UTC timestamp ending in Z")
    return text


def read_expected_lifecycle(
    state: dict[str, Any],
) -> tuple[int, str, str | None]:
    """Extract the committed expectation for the GitHub-owned PR lifecycle."""
    sync = state.get("state_sync")
    if not isinstance(sync, dict):
        raise ValueError("state_sync must be an object")
    github = sync.get("github")
    if not isinstance(github, dict):
        raise ValueError("state_sync.github must be an object")
    tracked = github.get("tracked_pull_request")
    if not isinstance(tracked, dict):
        raise ValueError("state_sync.github.tracked_pull_request must be an object")

    number = _as_positive_int(
        tracked.get("number"),
        "state_sync.github.tracked_pull_request.number",
    )
    expected_state = _as_nonempty_string(
        tracked.get("expected_state"),
        "state_sync.github.tracked_pull_request.expected_state",
    )
    if expected_state not in ALLOWED_PR_STATES:
        raise ValueError(
            "state_sync.github.tracked_pull_request.expected_state is not supported"
        )

    expected_sha = tracked.get("expected_merge_commit_sha")
    if expected_sha is not None:
        expected_sha = _as_sha(
            expected_sha,
            "state_sync.github.tracked_pull_request.expected_merge_commit_sha",
        )
    if expected_state == "MERGED" and expected_sha is None:
        raise ValueError("a MERGED PR must declare expected_merge_commit_sha")
    if expected_state != "MERGED" and expected_sha is not None:
        raise ValueError(
            "expected_merge_commit_sha must be null unless expected_state is MERGED"
        )

    return number, expected_state, expected_sha


def _matching_completed_records(
    state: dict[str, Any],
    pr_number: int,
) -> list[dict[str, Any]]:
    completed = state.get("completed_workstreams", [])
    if not isinstance(completed, list):
        raise ValueError("completed_workstreams must be an array when present")
    return [
        item
        for item in completed
        if isinstance(item, dict) and item.get("pull_request") == pr_number
    ]


def validate_internal_lifecycle_records(state: dict[str, Any]) -> list[str]:
    """Prevent duplicate JSON lifecycle representations from diverging.

    A tracked MERGED PR must have exactly one completed-workstream record with
    the same merge SHA. A tracked OPEN/CLOSED_UNMERGED PR must not already
    appear as completed.
    """
    number, expected_state, expected_sha = read_expected_lifecycle(state)
    try:
        matching = _matching_completed_records(state, number)
    except ValueError as exc:
        return [str(exc)]

    if expected_state != "MERGED":
        if matching:
            return [
                f"Tracked PR #{number} is expected {expected_state} but also appears "
                "in completed_workstreams."
            ]
        return []

    if len(matching) != 1:
        return [
            f"Expected exactly one completed_workstreams record for merged PR #{number}."
        ]

    record = matching[0]
    errors: list[str] = []
    if record.get("status") != "MERGED":
        errors.append(f"completed_workstreams PR #{number} must have status MERGED.")
    if record.get("merge_commit_sha") != expected_sha:
        errors.append(
            f"completed_workstreams PR #{number} merge SHA differs from state_sync.github."
        )
    try:
        _as_utc_timestamp(
            record.get("merged_at"),
            f"completed_workstreams PR #{number}.merged_at",
        )
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def validate_github_lifecycle(
    state: dict[str, Any],
    live: GitHubLifecycle,
) -> list[str]:
    """Compare live GitHub lifecycle facts with committed lifecycle evidence.

    This function never treats current main HEAD as a lifecycle fact.
    """
    number, expected_state, expected_sha = read_expected_lifecycle(state)
    errors: list[str] = []

    if live.pr_number != number:
        errors.append(f"GitHub returned PR #{live.pr_number}, expected PR #{number}.")
    if live.state != expected_state:
        errors.append(f"GitHub PR #{number} is {live.state}, expected {expected_state}.")
    if expected_sha is not None and live.merge_commit_sha != expected_sha:
        errors.append(
            "GitHub merge SHA does not match "
            "state_sync.github.tracked_pull_request."
        )

    if live.state == "MERGED":
        if not live.merged_at:
            errors.append("GitHub reports MERGED without merged_at.")
        else:
            try:
                _as_utc_timestamp(live.merged_at, "GitHub merged_at")
            except ValueError as exc:
                errors.append(str(exc))

        matching = _matching_completed_records(state, number)
        if len(matching) == 1:
            expected_merged_at = matching[0].get("merged_at")
            if (
                isinstance(expected_merged_at, str)
                and live.merged_at is not None
                and live.merged_at != expected_merged_at
            ):
                errors.append(
                    f"GitHub merged_at for PR #{number} differs from "
                    "completed_workstreams."
                )

    return errors


def read_provenance_base(state: dict[str, Any]) -> str:
    """Read the reviewed base SHA; it need not equal every later main HEAD."""
    provenance = state.get("state_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("state_provenance must be an object")
    return _as_sha(
        provenance.get("verified_base_head_sha"),
        "state_provenance.verified_base_head_sha",
    )


def validate_provenance_lineage(
    compare_status: str,
    base_sha: str,
    live_head_sha: str,
) -> list[str]:
    """Accept a main HEAD identical to or descended from the reviewed base.

    GitHub Compare returns ``ahead`` when HEAD contains the reviewed base plus
    later commits. That is expected after a README-only or engineering-only
    commit. ``behind`` or ``diverged`` means the reviewed base is no longer in
    the current main lineage and requires manual reconciliation.
    """
    if compare_status in ALLOWED_COMPARE_STATUSES:
        return []
    return [
        "Provenance lineage is no longer linear: "
        f"reviewed base {base_sha} versus live main {live_head_sha} returned "
        f"{compare_status}. Reconcile state manually before publishing derived "
        "surfaces."
    ]


def read_derived_state_surfaces(state: dict[str, Any]) -> frozenset[str]:
    sync = state.get("state_sync")
    if not isinstance(sync, dict):
        raise ValueError("state_sync must be an object")
    surfaces = sync.get("derived_state_surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise ValueError("state_sync.derived_state_surfaces must be a non-empty array")
    normalised = frozenset(
        _as_nonempty_string(value, "derived_state_surfaces item")
        for value in surfaces
    )
    if "project-state.json" in normalised:
        raise ValueError("project-state.json is primary state, not a derived surface")
    return normalised


def validate_state_bundle(
    changed_files: Iterable[str],
    derived_surfaces: frozenset[str],
) -> list[str]:
    """Conservative file-level state-bundle gate.

    This intentionally does not claim to understand arbitrary JSON semantics.
    If ``project-state.json`` changes, the declared always-derived volatile
    state surfaces must change in the same reviewable bundle. If one of those
    derived surfaces changes, the primary state file must also change.

    Structural files such as ``docs/ai/README.md`` are deliberately not
    unconditional members of the bundle; they may still be updated in a state
    change when their wording is affected.
    """
    changed = frozenset(path.strip() for path in changed_files if path.strip())
    primary_changed = "project-state.json" in changed
    changed_derived = changed.intersection(derived_surfaces)
    errors: list[str] = []

    if primary_changed:
        missing = sorted(derived_surfaces.difference(changed))
        if missing:
            errors.append(
                "project-state.json changed without all derived state surfaces: "
                + ", ".join(missing)
            )
    elif changed_derived:
        errors.append(
            "Derived state surfaces changed without project-state.json: "
            + ", ".join(sorted(changed_derived))
        )
    return errors
