#!/usr/bin/env python3
"""OpenRouter Capture adapter for the OD-PILOT-01 Capture-only Pilot (F1-P-A).

STATUS: IMPLEMENTATION DRAFT — PENDING AUTHORIZATION.
Label: PILOT — NOT EVIDENCE.

Authorized by the owner (2026-10-14) only as step 3 of the PR #62 §7 list: implement
the adapter with offline tests. This file does NOT adopt OD-PILOT-01, does NOT change
`experiment_0_pilot_status = NOT_AUTHORIZED`, and is not an execution entrypoint.
The only supported Pilot entrypoint remains scripts/e0/execute_pilot.py, which invokes
this adapter as a bounded child process after manifest/authorization validation.

Contract (derived from scripts/e0/execute_pilot.py and the PR #62 config draft §4.2):
- request JSON on stdin; credential only from env OPENROUTER_API_KEY (fail closed, never logged);
- exactly one POST https://openrouter.ai/api/v1/chat/completions, no retries, no tools,
  no streaming, host allowlist enforced, socket timeout;
- max_tokens from request.model.max_tokens; reported usage must not exceed --max-total-tokens;
- model output parsed into exactly one JSON object, validated against the referenced
  e0-state schema (schema bytes must match request.output_contract.schema_sha256);
- the object is printed to stdout; any error -> non-zero exit with a short stderr message.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
ALLOWED_HOSTS = frozenset({"openrouter.ai"})
API_KEY_ENV = "OPENROUTER_API_KEY"
DEFAULT_TIMEOUT_SECONDS = 100.0
DEFAULT_MAX_TOTAL_TOKENS = 32000
MAX_RESPONSE_BYTES = 4 * 1024 * 1024
REPO_ROOT = Path(__file__).resolve().parents[3]


class CaptureAdapterError(RuntimeError):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        raise CaptureAdapterError(f"redirect refused (HTTP {code})")


def check_host(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https":
        raise CaptureAdapterError("only https endpoints are allowed")
    if parsed.hostname not in ALLOWED_HOSTS or parsed.port not in (None, 443):
        raise CaptureAdapterError(f"host not in allowlist: {parsed.hostname!r}")


def load_request(text: str) -> dict[str, Any]:
    try:
        request = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CaptureAdapterError(f"request is not JSON: {exc}") from exc
    if not isinstance(request, dict):
        raise CaptureAdapterError("request must be a JSON object")
    if request.get("arm") != "CAPTURE_ONLY":
        raise CaptureAdapterError("request.arm must be CAPTURE_ONLY")
    tool_policy = request.get("tool_policy")
    if not isinstance(tool_policy, dict) or tool_policy.get("mode") != "NO_TOOLS" or tool_policy.get("allowlist"):
        raise CaptureAdapterError("request.tool_policy must be NO_TOOLS with an empty allowlist")
    model = request.get("model")
    if not isinstance(model, dict):
        raise CaptureAdapterError("request.model must be an object")
    if model.get("provider") != "openrouter":
        raise CaptureAdapterError("request.model.provider must be openrouter")
    identifier = model.get("identifier")
    if not isinstance(identifier, str) or not identifier or identifier.startswith("~"):
        raise CaptureAdapterError("request.model.identifier must be a pinned model id")
    max_tokens = model.get("max_tokens")
    if not isinstance(max_tokens, int) or isinstance(max_tokens, bool) or max_tokens <= 0:
        raise CaptureAdapterError("request.model.max_tokens must be a positive integer")
    interaction = request.get("interaction")
    if not isinstance(interaction, list) or not interaction:
        raise CaptureAdapterError("request.interaction must be a non-empty list")
    for turn in interaction:
        if not isinstance(turn, dict) or turn.get("role") not in ("user", "assistant") or not isinstance(turn.get("content"), str):
            raise CaptureAdapterError("request.interaction turns must be {role: user|assistant, content: str}")
    if not isinstance(request.get("instructions"), str):
        raise CaptureAdapterError("request.instructions must be a string")
    contract = request.get("output_contract")
    if not isinstance(contract, dict) or not isinstance(contract.get("schema_path"), str) or not isinstance(contract.get("schema_sha256"), str):
        raise CaptureAdapterError("request.output_contract must name schema_path and schema_sha256")
    return request


def load_schema(request: dict[str, Any], repo_root: Path) -> tuple[dict[str, Any], str]:
    contract = request["output_contract"]
    path = (repo_root / contract["schema_path"]).resolve()
    if repo_root.resolve() not in path.parents:
        raise CaptureAdapterError("schema_path resolves outside repository")
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise CaptureAdapterError(f"cannot read schema: {exc}") from exc
    if hashlib.sha256(data).hexdigest() != contract["schema_sha256"]:
        raise CaptureAdapterError("schema bytes SHA-256 do not match request.output_contract.schema_sha256")
    return json.loads(data.decode("utf-8")), data.decode("utf-8")


def build_payload(request: dict[str, Any], schema_text: str) -> dict[str, Any]:
    model = request["model"]
    system = (
        request["instructions"]
        + "\n\nOutput JSON Schema (draft 2020-12):\n"
        + schema_text
        + "\nRespond with exactly one JSON object and nothing else."
    )
    payload: dict[str, Any] = {
        "model": model["identifier"],
        "messages": [{"role": "system", "content": system}]
        + [{"role": t["role"], "content": t["content"]} for t in request["interaction"]],
        "max_tokens": model["max_tokens"],
        "stream": False,
        "response_format": {"type": "json_object"},
    }
    settings = model.get("settings") or {}
    if not isinstance(settings, dict):
        raise CaptureAdapterError("request.model.settings must be an object")
    if "reasoning" in settings:
        payload["reasoning"] = settings["reasoning"]
    return payload


def default_transport(url: str, body: bytes, headers: dict[str, str], timeout: float) -> tuple[int, bytes]:
    check_host(url)
    opener = urllib.request.build_opener(_NoRedirect())
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with opener.open(req, timeout=timeout) as resp:
            return resp.status, resp.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        return exc.code, b""
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        raise CaptureAdapterError(f"transport error: {type(exc).__name__}") from None


def extract_state(response: dict[str, Any], max_total_tokens: int) -> dict[str, Any]:
    if "error" in response:
        raise CaptureAdapterError("provider returned an error object")
    usage = response.get("usage")
    if isinstance(usage, dict):
        total = usage.get("total_tokens")
        if isinstance(total, int) and total > max_total_tokens:
            raise CaptureAdapterError(f"reported usage {total} exceeds max_total_tokens {max_total_tokens}")
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1:
        raise CaptureAdapterError("response must contain exactly one choice")
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict):
        raise CaptureAdapterError("response choice has no message")
    if message.get("tool_calls"):
        raise CaptureAdapterError("model attempted tool calls under NO_TOOLS")
    content = message.get("content")
    if not isinstance(content, str):
        raise CaptureAdapterError("response message content is not a string")
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 2 and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1]).strip()
    try:
        value, end = json.JSONDecoder().raw_decode(text)
    except json.JSONDecodeError as exc:
        raise CaptureAdapterError(f"model output is not JSON: {exc.msg}") from None
    if text[end:].strip():
        raise CaptureAdapterError("model output contains more than one JSON value")
    if not isinstance(value, dict):
        raise CaptureAdapterError("model output must be a JSON object")
    return value


def validate_state(state: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        import jsonschema  # pinned in requirements-e0.txt
    except ImportError:
        raise CaptureAdapterError("jsonschema not installed; refusing unvalidated output") from None
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(state), key=lambda e: list(e.path))
    if errors:
        raise CaptureAdapterError(f"model output violates e0-state schema: {errors[0].message[:200]}")


def run(
    request_text: str,
    *,
    env: dict[str, str],
    transport: Callable[[str, bytes, dict[str, str], float], tuple[int, bytes]] | None = None,
    repo_root: Path = REPO_ROOT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    max_total_tokens: int = DEFAULT_MAX_TOTAL_TOKENS,
) -> dict[str, Any]:
    api_key = env.get(API_KEY_ENV, "")
    if not api_key.strip():
        raise CaptureAdapterError(f"{API_KEY_ENV} is not set")
    if timeout <= 0 or max_total_tokens <= 0:
        raise CaptureAdapterError("timeout and max_total_tokens must be > 0")
    request = load_request(request_text)
    if request["model"]["max_tokens"] > max_total_tokens:
        raise CaptureAdapterError("request.model.max_tokens exceeds max_total_tokens")
    schema, schema_text = load_schema(request, repo_root)
    payload = build_payload(request, schema_text)
    check_host(ENDPOINT)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-Title": "Velantrim Continuum E0 Pilot (PILOT - NOT EVIDENCE)",
    }
    if transport is None:
        transport = default_transport
    status, body = transport(ENDPOINT, json.dumps(payload).encode("utf-8"), headers, timeout)  # single attempt, no retry
    if status != 200:
        raise CaptureAdapterError(f"provider HTTP status {status}")
    if len(body) > MAX_RESPONSE_BYTES:
        raise CaptureAdapterError("provider response too large")
    try:
        response = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise CaptureAdapterError("provider response is not JSON") from None
    if not isinstance(response, dict):
        raise CaptureAdapterError("provider response must be a JSON object")
    state = extract_state(response, max_total_tokens)
    validate_state(state, schema)
    return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OpenRouter Capture adapter (PENDING AUTHORIZATION)")
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-total-tokens", type=int, default=DEFAULT_MAX_TOTAL_TOKENS)
    args = parser.parse_args(argv)
    try:
        state = run(
            sys.stdin.read(),
            env=dict(os.environ),
            timeout=args.timeout_seconds,
            max_total_tokens=args.max_total_tokens,
        )
    except CaptureAdapterError as exc:
        print(f"CAPTURE_ADAPTER_ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # fail closed; never echo request/headers
        print(f"CAPTURE_ADAPTER_ERROR: unexpected {type(exc).__name__}", file=sys.stderr)
        return 3
    sys.stdout.write(json.dumps(state, ensure_ascii=False, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
