# OD-PILOT-01 — Provider/Model Config Draft (2026-10-14)

> **Status:** `CONFIG_DRAFT — NOT_RUN — NOT ADOPTED — NOT EXECUTABLE`
> **Label:** `PILOT — NOT EVIDENCE`
> **Baseline:** `main@42449ea`

This document records the owner's provider/model selection for the first Continuum Pilot and a draft configuration. It is **not** an OD-PILOT-01 adoption record, **not** package A, **not** activation B, and it does not authorize `scripts/e0/execute_pilot.py`. It is deliberately placed under `docs/research/` and **not** under `experiments/e0/pilot/` (the manifest/activation prefix).

## 1. Owner selection (recorded)

- Recorded: 2026-10-14, owner Quitzon Trey, via voice instruction.
- Provider: **OpenRouter**.
- Model requested: "ChatGPT 6 Luna", reasoning effort **xhigh**.
- Budget proposal: **USD 5.00** cap for the first run (proposed by assistant, accepted as draft value; must be confirmed at adoption).

## 2. Catalog verification (2026-10-14, public `GET https://openrouter.ai/api/v1/models`)

- Exact id: **`openai/gpt-6-luna`** — prompt USD 0.10 / 1M tokens, completion USD 0.50 / 1M tokens; supports `reasoning`, `reasoning_effort`.
- Related, not selected: `openai/gpt-6-luna-pro` (same listed price), `:batch` variants, alias `~openai/gpt-luna-latest` (floating alias — rejected, not pinnable).
- No id contains `chatgpt` or `xhigh`; `xhigh` is treated as the `reasoning.effort` setting. Whether the provider accepts `xhigh` (vs. `high`) is **UNVERIFIED** until a preflight; no completion was made.

## 3. Draft config

```json
{
  "config_status": "CONFIG_DRAFT",
  "run_status": "NOT_RUN",
  "owner_decision_id": "OD-PILOT-01",
  "owner_decision_status": "DRAFT — NOT ADOPTED",
  "owner_selection_recorded": {"date": "2026-10-14", "by": "Quitzon Trey", "channel": "voice"},
  "model": {
    "provider": "openrouter",
    "identifier": "openai/gpt-6-luna",
    "identifier_verified_in_catalog": "2026-10-14",
    "settings": {"reasoning": {"effort": "xhigh"}, "reasoning_effort_support": "UNVERIFIED"}
  },
  "credentials": {
    "profile": "openrouter-pilot",
    "scope": "inference only; key-level spend limit",
    "environment_variables": ["OPENROUTER_API_KEY"]
  },
  "network_dependency": {"required": true, "allowed_hosts": ["openrouter.ai"]},
  "budget": {"max_cost": 5.00, "currency": "USD", "max_total_tokens": "UNPINNED"},
  "limits": {"timeout_seconds": 120, "max_output_bytes": 1048576, "max_runs": 1},
  "tool_policy": {"mode": "NO_TOOLS", "allowlist": []},
  "execution_posture": "UNCONTROLLED_LOCAL_ADVISORY",
  "requested_run_shape": "single short Capture -> Handoff -> Rehydration across one simulated model switch",
  "repository_candidate_scope": "Capture Pilot only, fixture F1-P-A (see OD_PILOT_01_CANDIDATE_PREP.md)",
  "unresolved": ["adapter_command", "request JSON + request_sha256", "human approval sha256", "max_total_tokens", "manual_stop", "scope conflict (see §4)"]
}
```

## 4. Scope conflict — owner must choose

The owner asked for one Capture → Handoff → Rehydration run. The repository candidate (`OD_PILOT_01_CANDIDATE_PREP.md`) is **Capture-only `F1-P-A`**; adding Transfer requires an approved Transfer Oracle path + SHA-256 and revising the worksheet, and AGENTS.md requires Capture and Transfer to stay experimentally isolated. Options: (a) keep Capture-only first, Transfer as a separate later pilot; (b) revise the worksheet to include a Transfer Pilot scenario.

## 5. Authority remains closed

`experiment_0_pilot_status = NOT_AUTHORIZED`; `experiment_0_pilot_authorization = null`; Evidence Lock `NOT_CREATED`. No API completion was made while preparing this file.
