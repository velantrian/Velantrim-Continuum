"""Offline tests for the OpenRouter Capture adapter (PENDING AUTHORIZATION).

No network: every test injects a mocked transport, and urllib openers are patched to fail.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "scripts" / "e0" / "adapters" / "openrouter_capture_adapter.py"
SCHEMA = "experiments/e0/schema/e0-state.schema.json"

spec = importlib.util.spec_from_file_location("openrouter_capture_adapter", ADAPTER)
adapter = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(adapter)

FAKE_KEY = "sk-or-test-NOT-A-REAL-KEY"
VALID_STATE = {
    "schema_version": "0.1",
    "items": [{
        "item_id": "C1", "entity": "release_note", "kind": "constraint",
        "value": "do not publish without explicit approval",
        "epistemic_status": "OBSERVED", "resolution_status": "RESOLVED", "lifecycle_status": "ACTIVE",
    }],
}


def make_request(**overrides):
    request = {
        "arm": "CAPTURE_ONLY",
        "instructions": "Capture state. Return one JSON object.",
        "interaction": [{"role": "user", "content": "Do not publish the release note without my explicit approval."}],
        "label": "PILOT — NOT EVIDENCE",
        "model": {"identifier": "openai/gpt-6-luna", "max_tokens": 24000, "provider": "openrouter",
                  "settings": {"reasoning": {"effort": "xhigh"}}},
        "output_contract": {"schema_path": SCHEMA,
                            "schema_sha256": hashlib.sha256((ROOT / SCHEMA).read_bytes()).hexdigest()},
        "tool_policy": {"allowlist": [], "mode": "NO_TOOLS"},
    }
    request.update(overrides)
    return json.dumps(request)


def completion(content, total_tokens=1200, **extra):
    message = {"role": "assistant", "content": content}
    message.update(extra)
    return {"choices": [{"message": message}], "usage": {"total_tokens": total_tokens}}


class MockTransport:
    def __init__(self, status=200, body=None):
        self.status = status
        self.body = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.calls = []

    def __call__(self, url, body, headers, timeout):
        self.calls.append((url, json.loads(body), headers, timeout))
        return self.status, self.body


def no_network(*args, **kwargs):
    raise AssertionError("network access attempted in offline test")


@mock.patch("urllib.request.urlopen", no_network)
@mock.patch("urllib.request.OpenerDirector.open", no_network)
class OpenRouterCaptureAdapterTests(unittest.TestCase):
    def run_ok(self, transport, request=None, **kw):
        return adapter.run(request or make_request(), env={"OPENROUTER_API_KEY": FAKE_KEY}, transport=transport, **kw)

    def test_valid_capture_single_post(self):
        t = MockTransport(body=completion(json.dumps(VALID_STATE)))
        self.assertEqual(self.run_ok(t), VALID_STATE)
        self.assertEqual(len(t.calls), 1)
        url, payload, headers, timeout = t.calls[0]
        self.assertEqual(url, "https://openrouter.ai/api/v1/chat/completions")
        self.assertEqual(payload["model"], "openai/gpt-6-luna")
        self.assertEqual(payload["max_tokens"], 24000)
        self.assertEqual(payload["reasoning"], {"effort": "xhigh"})
        self.assertFalse(payload["stream"])
        self.assertNotIn("tools", payload)
        self.assertEqual(headers["Authorization"], f"Bearer {FAKE_KEY}")
        self.assertGreater(timeout, 0)

    def test_fenced_json_accepted(self):
        t = MockTransport(body=completion("```json\n" + json.dumps(VALID_STATE) + "\n```"))
        self.assertEqual(self.run_ok(t), VALID_STATE)

    def test_missing_key_fails_closed_without_call(self):
        t = MockTransport(body=completion(json.dumps(VALID_STATE)))
        for env in ({}, {"OPENROUTER_API_KEY": "  "}):
            with self.assertRaises(adapter.CaptureAdapterError):
                adapter.run(make_request(), env=env, transport=t)
        self.assertEqual(t.calls, [])

    def test_http_error_no_retry(self):
        t = MockTransport(status=500, body=b"{}")
        with self.assertRaises(adapter.CaptureAdapterError):
            self.run_ok(t)
        self.assertEqual(len(t.calls), 1)

    def test_rejects_non_json_and_multiple_values(self):
        for content in ("not json", json.dumps(VALID_STATE) + " {}", "[1,2]"):
            with self.subTest(content=content), self.assertRaises(adapter.CaptureAdapterError):
                self.run_ok(MockTransport(body=completion(content)))

    def test_rejects_schema_violation(self):
        bad = {"schema_version": "0.1", "items": [{"item_id": "x"}]}
        with self.assertRaises(adapter.CaptureAdapterError):
            self.run_ok(MockTransport(body=completion(json.dumps(bad))))

    def test_rejects_usage_over_budget(self):
        with self.assertRaises(adapter.CaptureAdapterError):
            self.run_ok(MockTransport(body=completion(json.dumps(VALID_STATE), total_tokens=40000)))

    def test_rejects_max_tokens_over_budget_before_call(self):
        t = MockTransport(body=completion(json.dumps(VALID_STATE)))
        with self.assertRaises(adapter.CaptureAdapterError):
            self.run_ok(t, max_total_tokens=1000)
        self.assertEqual(t.calls, [])

    def test_rejects_tool_calls_and_provider_error(self):
        for body in (completion(json.dumps(VALID_STATE), tool_calls=[{"id": "1"}]), {"error": {"message": "x"}}):
            with self.subTest(body=body), self.assertRaises(adapter.CaptureAdapterError):
                self.run_ok(MockTransport(body=body))

    def test_rejects_bad_requests_before_call(self):
        t = MockTransport(body=completion(json.dumps(VALID_STATE)))
        bad = [
            make_request(arm="TRANSFER"),
            make_request(tool_policy={"mode": "TOOLS", "allowlist": ["x"]}),
            make_request(model={"identifier": "~openai/gpt-luna-latest", "max_tokens": 10, "provider": "openrouter"}),
            make_request(model={"identifier": "openai/gpt-6-luna", "max_tokens": 10, "provider": "openai"}),
            make_request(output_contract={"schema_path": SCHEMA, "schema_sha256": "0" * 64}),
            make_request(output_contract={"schema_path": "../../etc/passwd", "schema_sha256": "0" * 64}),
            "not json",
        ]
        for request in bad:
            with self.subTest(request=request[:60]), self.assertRaises(adapter.CaptureAdapterError):
                self.run_ok(t, request=request)
        self.assertEqual(t.calls, [])

    def test_host_allowlist(self):
        adapter.check_host("https://openrouter.ai/api/v1/chat/completions")
        for url in ("http://openrouter.ai/x", "https://evil.example/x", "https://openrouter.ai.evil.example/x",
                    "https://openrouter.ai:8443/x"):
            with self.subTest(url=url), self.assertRaises(adapter.CaptureAdapterError):
                adapter.check_host(url)

    def test_main_exit_codes_and_no_key_leak(self):
        state_body = completion(json.dumps(VALID_STATE))
        cases = [({"OPENROUTER_API_KEY": FAKE_KEY}, 200, 0), ({"OPENROUTER_API_KEY": FAKE_KEY}, 401, 2), ({}, 200, 2)]
        for env, status, code in cases:
            with self.subTest(status=status, env=bool(env)):
                t = MockTransport(status=status, body=state_body)
                out, err = io.StringIO(), io.StringIO()
                with mock.patch.dict("os.environ", env, clear=True), \
                     mock.patch.object(adapter, "default_transport", t), \
                     mock.patch("sys.stdin", io.StringIO(make_request())), \
                     mock.patch("sys.stdout", out), mock.patch("sys.stderr", err):
                    self.assertEqual(adapter.main([]), code)
                self.assertNotIn(FAKE_KEY, out.getvalue() + err.getvalue())
                if code == 0:
                    self.assertEqual(json.loads(out.getvalue()), VALID_STATE)
                else:
                    self.assertEqual(out.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
