from __future__ import annotations

import unittest

from scripts.state_sync_rules import (
    GitHubLifecycle,
    read_derived_state_surfaces,
    read_provenance_base,
    validate_github_lifecycle,
    validate_internal_lifecycle_records,
    validate_provenance_lineage,
    validate_state_bundle,
)

BASE_SHA = "a" * 40
MERGE_SHA = "b" * 40
NEW_HEAD_SHA = "c" * 40
MERGED_AT = "2026-08-15T09:06:37Z"


def state_fixture() -> dict:
    return {
        "current_workstream": "NEXT_BOUNDED_ENGINEERING_MILESTONE_SELECTION",
        "current_workstream_status": "PENDING_EXPLICIT_SELECTION",
        "current_workstream_pr": None,
        "completed_workstreams": [
            {
                "name": "DOCUMENTATION_ARCHITECTURE_V1",
                "pull_request": 2,
                "status": "MERGED",
                "merged_at": MERGED_AT,
                "merge_commit_sha": MERGE_SHA,
            }
        ],
        "state_provenance": {
            "verified_base_head_sha": BASE_SHA,
            "reconciled_at": "2026-08-16T06:58:16Z",
            "reconciliation_kind": "STATE_CHANGE",
        },
        "state_sync": {
            "github": {
                "tracked_pull_request": {
                    "number": 2,
                    "expected_state": "MERGED",
                    "expected_merge_commit_sha": MERGE_SHA,
                }
            },
            "derived_state_surfaces": [
                "STATUS.md",
                "docs/ai/CURRENT_STATE.md",
            ],
        },
    }


def merged_pr() -> GitHubLifecycle:
    return GitHubLifecycle(
        pr_number=2,
        state="MERGED",
        merged_at=MERGED_AT,
        merge_commit_sha=MERGE_SHA,
    )


class GitHubLifecycleTests(unittest.TestCase):
    def test_matching_merged_pr_passes(self) -> None:
        self.assertEqual(validate_github_lifecycle(state_fixture(), merged_pr()), [])

    def test_open_pr_when_merged_expected_fails(self) -> None:
        live = GitHubLifecycle(2, "OPEN", None, None)
        errors = validate_github_lifecycle(state_fixture(), live)
        self.assertTrue(any("is OPEN, expected MERGED" in error for error in errors))

    def test_wrong_merge_sha_fails(self) -> None:
        live = GitHubLifecycle(2, "MERGED", MERGED_AT, "d" * 40)
        self.assertTrue(validate_github_lifecycle(state_fixture(), live))

    def test_wrong_completed_merged_at_fails_against_live(self) -> None:
        state = state_fixture()
        state["completed_workstreams"][0]["merged_at"] = "2026-08-15T09:06:38Z"
        errors = validate_github_lifecycle(state, merged_pr())
        self.assertTrue(any("merged_at" in error for error in errors))


class InternalConsistencyTests(unittest.TestCase):
    def test_matching_completed_workstream_passes(self) -> None:
        self.assertEqual(validate_internal_lifecycle_records(state_fixture()), [])

    def test_duplicate_lifecycle_sha_fails(self) -> None:
        state = state_fixture()
        state["completed_workstreams"][0]["merge_commit_sha"] = "e" * 40
        errors = validate_internal_lifecycle_records(state)
        self.assertTrue(any("merge SHA differs" in error for error in errors))

    def test_missing_completed_workstream_fails(self) -> None:
        state = state_fixture()
        state["completed_workstreams"] = []
        self.assertTrue(validate_internal_lifecycle_records(state))

    def test_tracked_open_but_completed_merged_fails(self) -> None:
        state = state_fixture()
        tracked = state["state_sync"]["github"]["tracked_pull_request"]
        tracked["expected_state"] = "OPEN"
        tracked["expected_merge_commit_sha"] = None
        errors = validate_internal_lifecycle_records(state)
        self.assertTrue(any("also appears in completed_workstreams" in e for e in errors))

    def test_invalid_completed_merged_at_format_fails(self) -> None:
        state = state_fixture()
        state["completed_workstreams"][0]["merged_at"] = "yesterday"
        errors = validate_internal_lifecycle_records(state)
        self.assertTrue(any("ISO-8601 UTC" in e for e in errors))


class ProvenanceLineageTests(unittest.TestCase):
    def test_nonsemantic_later_main_commit_is_allowed(self) -> None:
        state = state_fixture()
        base_sha = read_provenance_base(state)
        self.assertEqual(
            validate_provenance_lineage("ahead", base_sha, NEW_HEAD_SHA),
            [],
        )

    def test_identical_reviewed_head_is_allowed(self) -> None:
        base_sha = read_provenance_base(state_fixture())
        self.assertEqual(
            validate_provenance_lineage("identical", base_sha, base_sha),
            [],
        )

    def test_rewritten_or_diverged_history_fails(self) -> None:
        base_sha = read_provenance_base(state_fixture())
        errors = validate_provenance_lineage("diverged", base_sha, NEW_HEAD_SHA)
        self.assertTrue(any("no longer linear" in error for error in errors))

    def test_main_behind_reviewed_base_fails(self) -> None:
        base_sha = read_provenance_base(state_fixture())
        self.assertTrue(
            validate_provenance_lineage("behind", base_sha, NEW_HEAD_SHA)
        )

    def test_invalid_provenance_sha_fails(self) -> None:
        state = state_fixture()
        state["state_provenance"]["verified_base_head_sha"] = "x"
        with self.assertRaisesRegex(ValueError, "40-character lowercase Git SHA"):
            read_provenance_base(state)


class StateBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state = state_fixture()
        self.derived = read_derived_state_surfaces(self.state)

    def test_readme_only_commit_is_allowed(self) -> None:
        self.assertEqual(
            validate_state_bundle({"README.md", "README.ru.md"}, self.derived),
            [],
        )

    def test_ai_router_only_structural_change_is_allowed(self) -> None:
        self.assertEqual(
            validate_state_bundle({"docs/ai/README.md"}, self.derived),
            [],
        )

    def test_json_and_all_derived_surfaces_pass(self) -> None:
        changed = {"project-state.json", *self.derived}
        self.assertEqual(validate_state_bundle(changed, self.derived), [])

    def test_json_without_current_state_fails(self) -> None:
        changed = {"project-state.json", "STATUS.md"}
        errors = validate_state_bundle(changed, self.derived)
        self.assertTrue(any("docs/ai/CURRENT_STATE.md" in error for error in errors))

    def test_status_without_json_fails(self) -> None:
        errors = validate_state_bundle({"STATUS.md"}, self.derived)
        self.assertTrue(any("without project-state.json" in error for error in errors))

    def test_non_state_source_file_change_is_allowed(self) -> None:
        changed = {
            "scripts/check_state_sync.py",
            "tests/test_state_sync_rules.py",
        }
        self.assertEqual(validate_state_bundle(changed, self.derived), [])


if __name__ == "__main__":
    unittest.main()
