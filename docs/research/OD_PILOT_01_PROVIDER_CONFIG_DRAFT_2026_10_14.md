# OD-PILOT-01 — Provider/Model Config Draft (2026-10-14)

> **Status:** `CONFIG_DRAFT (CAPTURE_ONLY) — NOT_RUN — NOT ADOPTED — NOT EXECUTABLE`
> **Label:** `PILOT — NOT EVIDENCE`
> **Baseline:** `main@42449ea`

This document records the owner's provider/model selection for the first Continuum Pilot and a draft configuration. It is **not** an OD-PILOT-01 adoption record, **not** package A, **not** activation B, and it does not authorize `scripts/e0/execute_pilot.py`. It is deliberately placed under `docs/research/` and **not** under `experiments/e0/pilot/` (the manifest/activation prefix).

## 1. Owner selection (recorded)

- Recorded: 2026-10-14, owner Quitzon Trey, via voice instruction.
- Provider: **OpenRouter**.
- Model requested: "ChatGPT 6 Luna", reasoning effort **xhigh**.
- Budget: **USD 5.00** cap for the first run — confirmed by owner 2026-10-14 (still re-confirmed inside the formal adoption record).
- Scope decision (2026-10-14, owner, chat): **option (a)** — Capture-only Pilot first on fixture `F1-P-A`; Handoff/Transfer deferred to a separate, later pilot.

## 2. Catalog verification (2026-10-14, public `GET https://openrouter.ai/api/v1/models`)

- Exact id: **`openai/gpt-6-luna`** — prompt USD 0.10 / 1M tokens, completion USD 0.50 / 1M tokens; supports `reasoning`, `reasoning_effort`.
- Related, not selected: `openai/gpt-6-luna-pro` (same listed price), `:batch` variants, alias `~openai/gpt-luna-latest` (floating alias — rejected, not pinnable).
- No id contains `chatgpt` or `xhigh`; `xhigh` is treated as the `reasoning.effort` setting. Whether the provider accepts `xhigh` (vs. `high`) is **UNVERIFIED** until a preflight; no completion was made.

## 3. Scope: `CAPTURE_ONLY`

- Arm: Capture Pilot only; fixture `F1-P-A` (per `OD_PILOT_01_CANDIDATE_PREP.md` §1).
- Transfer / Handoff / Rehydration: **DEFERRED** to a separate later pilot (own OD, own Transfer Oracle path + SHA-256, own worksheet revision). Not part of this config.
- Transfer Oracle: `N/A` for this run.
- The §4 scope conflict of the previous revision is **RESOLVED** by owner choice (a).

## 4. Draft manifest values (mapped to `experiments/e0/pilot/pilot-manifest.template.json`)

`PENDING_OWNER` = requires owner action/signature; `PENDING_IMPLEMENTATION` = requires a separate reviewed change.

```json
{
  "run_type": "PILOT",
  "label": "PILOT — NOT EVIDENCE",
  "scope": "CAPTURE_ONLY",
  "transfer": "DEFERRED — separate later pilot",
  "owner_decision_id": "OD-PILOT-01",
  "owner_decision_status": "DRAFT — NOT ADOPTED",
  "owner_github_login": "PENDING_OWNER",
  "owner_adopted_at": "PENDING_OWNER",
  "activation_policy": "DIRECT_CHILD_ONLY",
  "human_approval": {
    "path": "experiments/e0/approval/human-reference-approval.v0.2.json",
    "sha256": "PENDING_OWNER (computed at main@42449ea: d013923186090545941b881999cba456d04cece0cf94721bd240c438bda50641 — owner must re-pin from authoritative bytes at adoption)"
  },
  "approved_references": [
    {"path": "experiments/e0/gold/approved/capture-gold.v0.1.json",
     "sha256": "9b806fdb44ff84ba0456d0dd480c328398915ca40f9de7f9e0232452678e2025"}
  ],
  "fixture_or_scenario_ids": ["F1-P-A"],
  "request_sha256": "a223938a0618f894e139c72c51d7d652f56eb3e40792c8011ce89a8b7a8331c9",
  "execution_posture": "UNCONTROLLED_LOCAL_ADVISORY",
  "isolation": {"isolation_enforcement": "NOT_ENFORCED", "network_isolation": "NOT_ENFORCED",
                "filesystem_isolation": "NOT_ENFORCED", "process_isolation": "NOT_ENFORCED"},
  "limits": {"timeout_seconds": 120, "max_output_bytes": 1048576, "max_runs": 1},
  "evidence_lock": {"status": "NOT_CREATED", "sha256": null},
  "model": {"provider": "openrouter", "identifier": "openai/gpt-6-luna",
            "settings": {"reasoning": {"effort": "xhigh"}, "max_tokens": 24000}},
  "credentials": {"profile": "openrouter-pilot", "scope": "inference only; key-level spend limit <= USD 5.00 recommended",
                  "environment_variables": ["OPENROUTER_API_KEY"]},
  "adapter_command": "python3 scripts/e0/adapters/openrouter_capture_adapter.py  (IMPLEMENTED as offline-tested draft; PENDING AUTHORIZATION — not an execution entrypoint)",
  "adapter_cwd": ".",
  "environment_allowlist": ["OPENROUTER_API_KEY"],
  "output_destination": ".velantrim-continuum-pilot-runs",
  "tool_policy": {"mode": "NO_TOOLS", "allowlist": []},
  "budget": {"max_total_tokens": 32000, "max_cost": 5.00, "currency": "USD"},
  "network_dependency": {"required": true, "allowed_hosts": ["openrouter.ai"]},
  "manual_stop": {
    "owner_github_login": "PENDING_OWNER",
    "contact_ref": "PENDING_OWNER (repository owner via this PR / chat)",
    "procedure": "see §6"
  }
}
```

### 4.1 Request JSON (exact bytes)

- File: `docs/research/OD_PILOT_01_CAPTURE_REQUEST_CANDIDATE_F1_P_A.json` (1283 bytes, UTF-8, sorted keys, indent 2, trailing newline).
- SHA-256: `a223938a0618f894e139c72c51d7d652f56eb3e40792c8011ce89a8b7a8331c9`.
- Binds: fixture set `experiments/e0/fixtures/capture/pilot/fixtures.json` (`f07a028f…d17c`), fixture `F1-P-A` interaction verbatim, output schema `experiments/e0/schema/e0-state.schema.json` (`9f11ba4c…94fd`), model/settings, `NO_TOOLS`.
- `execute_pilot.py` checks the request bytes against `request_sha256`; any edit to the file requires re-hashing and a new owner review. At package A the file is expected to be copied byte-identically to the package location chosen there.

### 4.2 Adapter contract (derived from `scripts/e0/execute_pilot.py`)

- Invoked as `shlex.split(adapter_command)` in `adapter_cwd`, environment = `PATH` + `environment_allowlist` only.
- Receives the request JSON on **stdin**; must print exactly **one JSON object** on stdout (the captured state, valid against `e0-state.schema.json`); non-zero exit = attempt FAILED.
- One OpenRouter `POST /api/v1/chat/completions` call, no retries, no tools, no streaming; must enforce `max_tokens` from the request and abort if the reported usage exceeds `budget.max_total_tokens`.
- Status: **PENDING_IMPLEMENTATION** — the adapter is code and needs its own reviewed PR with offline tests (mocked HTTP). Not added here.

### 4.3 Token limit rationale

Input ≈ 1–5k tokens (interaction + schema + instructions); output cap 24,000 (includes reasoning at `xhigh`). Total cap 32,000 tokens. At listed prices (USD 0.10 / 0.50 per 1M) worst case ≈ USD 0.02, far below the USD 5.00 cap.

## 5. `xhigh` support

Still **UNVERIFIED**. Per instruction no paid completion was made. Verification (one minimal call, or the provider's parameter docs) is a step for the owner to authorize; if `xhigh` is rejected, fallback `high` requires changing the request bytes and therefore a new `request_sha256`.

## 6. Manual-stop procedure (draft)

1. Stop the process: Ctrl-C in the terminal running `scripts/e0/execute_pilot.py`, or `kill <pid>` of the adapter process; the 120 s timeout in `run_adapter.bounded_run` is the automatic backstop.
2. Revoke spend: disable/delete the `openrouter-pilot` key in the OpenRouter dashboard (key-level limit ≤ USD 5.00 is the hard monetary stop).
3. Do not retry: `max_runs = 1`; any further attempt needs a new owner decision.
4. Record: leave the attempt directory under `.velantrim-continuum-pilot-runs` untouched; note the stop in the PR.

Contact/owner login: `PENDING_OWNER`.

## 7. Remaining steps for the owner (in order)

1. Confirm `owner_github_login`, `contact_ref` and the manual-stop procedure (§6).
2. Re-pin the Human Reference approval SHA-256 from authoritative bytes.
3. Authorize the adapter implementation PR (§4.2) and review/merge it.
4. Authorize one minimal `xhigh` compatibility check (or accept fallback `high` → new request hash).
5. Create a dedicated `openrouter-pilot` key with a USD 5.00 limit.
6. Formally adopt OD-PILOT-01 (exact package intent with all values above).
7. Package commit A, then activation B (separate gates, `DIRECT_CHILD_ONLY`).
8. Only then: run `scripts/e0/execute_pilot.py` once.

## 8. Authority remains closed

`experiment_0_pilot_status = NOT_AUTHORIZED`; `experiment_0_pilot_authorization = null`; `OD-PILOT-01 = DRAFT — NOT ADOPTED`; Evidence Lock `NOT_CREATED`. No API completion was made while preparing this file. This document is not package A and does not authorize `scripts/e0/execute_pilot.py`.

## Adapter exit codes (`scripts/e0/adapters/openrouter_capture_adapter.py`)

| Exit | stderr prefix | Meaning |
|---|---|---|
| 0 | — | one validated e0-state object printed to stdout |
| 2 | `CAPTURE_ADAPTER_ERROR:` | definite failure (bad request/config, request not sent, HTTP != 200, invalid/oversized output, schema violation) |
| 3 | `CAPTURE_ADAPTER_ERROR: unexpected <Type>` | unexpected internal exception (fail closed) |
| 4 | `CAPTURE_ADAPTER_UNKNOWN_OUTCOME:` | timeout or connection lost **after send**: the provider may have processed/billed the call; outcome unknown. Never retried automatically |

Single attempt, no retries in all cases. `scripts/e0/execute_pilot.py` preserves adapter exit 4 as Pilot `UNKNOWN_OUTCOME` (CLI exit 4), not `FAILED` or `COMPLETED`. A bounded runner timeout is also conservatively `UNKNOWN_OUTCOME` because it cannot prove whether the request reached the provider. Neither status authorizes a Pilot or creates Evidence Lock.
