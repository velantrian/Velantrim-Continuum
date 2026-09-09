from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class CaptureContractAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = load("experiments/e0/schema/capture-fixture.schema.json")
        cls.validator = Draft202012Validator(cls.schema)
        cls.fixture_set = load("experiments/e0/fixtures/capture/pilot/fixtures.json")

    def errors(self, document: dict) -> list[str]:
        return [error.message for error in self.validator.iter_errors(document)]

    def test_committed_capture_pilot_fixture_set_remains_schema_valid(self):
        self.assertEqual(self.errors(self.fixture_set), [])

    def test_action_only_hard_fail_class_is_rejected_by_capture_schema(self):
        document = copy.deepcopy(self.fixture_set)
        document["fixtures"][0]["hard_fail_bindings"][0]["hard_fail_class"] = "UNAUTHORIZED_IRREVERSIBLE_ACTION"
        self.assertTrue(self.errors(document))

    def test_duplicate_side_effect_class_is_rejected_by_capture_schema(self):
        document = copy.deepcopy(self.fixture_set)
        document["fixtures"][0]["hard_fail_bindings"][0]["hard_fail_class"] = "DUPLICATE_IRREVERSIBLE_SIDE_EFFECT"
        self.assertTrue(self.errors(document))

    def test_match_spec_requires_runtime_supported_strategy(self):
        document = copy.deepcopy(self.fixture_set)
        document["fixtures"][0]["match_spec"] = {"strategy": "unsupported"}
        self.assertTrue(self.errors(document))

    def test_match_spec_rejects_extra_contract_fields(self):
        document = copy.deepcopy(self.fixture_set)
        document["fixtures"][0]["match_spec"]["threshold"] = 0.5
        self.assertTrue(self.errors(document))


if __name__ == "__main__":
    unittest.main()
