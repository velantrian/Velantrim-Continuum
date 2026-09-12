# CONT-E0T Field 5 — Reader contract (candidate)

**Status:** `FIELD_5 = FROZEN_CANDIDATE`  
**Identity:** `FIELD_5_MODEL_IDENTITY = CLEARED` — `deepseek-flash` / DeepSeek-V4.1-Flash; `SNAPSHOT_PINNED = NO`; `ALIAS_MUTABLE = YES`. See `docs/research/CONT_E0T_FIELD5_SOURCE_RECONCILIATION.md`  
**Not:** experiment GO. Not a model run. Not Evidence. Not architecture.  
**Parent science SHA:** `bc48a15148d6b7d2f1a9863214cf8a5c734ae10d`  
**This branch:** `research/cont-e0t-prereg-v22`  
**Date (record):** 2026-09-12

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
READY_FOR_FIELD_5 accepted as gate only
NO READER INVOCATION IN THIS PASS
```

Labs / Grok Bot persistent agent context is **forbidden** as reader context.

---

## 1. Why this model (pre-output only)

Only live LLM credential on this computer: `DEEPSEEK_API_KEY`.  
`GET https://api.deepseek.com/models` (no prompt, no fixture) returned exactly:

- `deepseek-flash`
- `deepseek-v4-pro`

Selection **not** based on CAND-03/CAND-04 outputs. Those fixtures were not sent to any model.

| Criterion | Decision |
|-----------|----------|
| Availability | DeepSeek only |
| Stable/versionable identity | **Neither** id is a date-pinned snapshot. See limitations. |
| Reproducibility | Thinking **disabled**; temperature 0; same wrapper both arms. Seed **UNSUPPORTED**. |
| Context | Official Flash context length 1M — sufficient for these packages |
| Cost | Flash cheaper than Pro; no fixture screening |
| Fallible replaceable reader | Non-thinking Flash is a generic chat model, not a hidden Labs agent |

**Rejected `deepseek-v4-pro`:** provider-stated route change **2026-09-14 04:00 UTC** — all `deepseek-v4-pro` requests become V4.1 Flash. Using Pro now would silently change identity in two days.

**Selected request id:** `deepseek-flash`  
**Provider-stated version label (docs, 2026-09-12):** DeepSeek-V4.1-Flash  
**Alias mutable:** **YES**  
**Snapshot pinned:** **NO** — MODEL IDENTITY KNOWN; WEIGHTS NOT IMMUTABLY PINNED

---

## 2. Frozen reader contract

| Field | Value |
|-------|--------|
| Provider | DeepSeek (`https://api.deepseek.com`) |
| API | OpenAI-compatible `POST /chat/completions` |
| Model identifier | `deepseek-flash` |
| Provider version label | DeepSeek-V4.1-Flash (docs; not a snapshot SHA) |
| Alias mutable | **YES** — record `response.model` on any later authorized call |
| Context limit | 1_000_000 tokens (provider docs) |
| Temperature | `0` |
| top_p | `1` |
| max output tokens | `1024` |
| seed | **UNSUPPORTED** — not invented |
| stream | `false` |
| tools | **NONE** |
| tool_choice | absent |
| web / retrieval / browser / files / apps | **NONE** |
| memory / conversation | **NONE** — one isolated HTTP call |
| thinking / reasoning | **PINNED DISABLED**: `thinking: {type: "disabled"}` |
| reasoning_effort | absent (unused while thinking disabled) |
| n | `1` |
| stop | unset |
| Tokenizer / token count | **Provider `usage` on the response** (`prompt_tokens`, `completion_tokens`). No offline tokenizer claimed for V4.1-Flash. Do not invent a tiktoken mapping. |
| Reader prompt file | `docs/research/cont_e0t_v2/reader_prompt_field5.txt` |
| Reader prompt SHA-256 | `966400916b79e7025ed22c325e7d858e08ff2e89c0cc024606d7eb429878a349` |
| Call topology | **One fresh stateless invocation per (fixture_id, arm_package, probe_id)**. No batch reuse of a client session as memory. |
| Retry | No retry on HTTP 200. One retry only on transport timeout / connection reset. Record `RETRY`. 4xx/5xx fail-closed (`CALL_FAIL`). |
| Timeout | 60 seconds per invocation |
| Same wrapper both arms | **YES** |
| Arm labels exposed | **NO** — do not send `T1`, `T2`, `CONT-T1`, `CONT-T2` |

The presence of `thin_trajectory` in the package **is** the treatment.

---

## 3. Exact input serialization

Canonical JSON: UTF-8, `sort_keys=True`, separators `(",", ":")`.

User message body:

```text
PACKAGE
<canonical JSON of the arm object>

PROBE
<probe.wording exactly as frozen>
```

Arm objects (no arm-name key):

| Arm | Object |
|-----|--------|
| CONT-T1 (builder only) | `{"current_semantics": <T1 lists already id-sorted>}` |
| CONT-T2 (builder only) | `{"current_semantics": <same object>, "thin_trajectory": <ID_REFS_ONLY>}` |

HTTP body:

```json
{
  "model": "deepseek-flash",
  "temperature": 0,
  "top_p": 1,
  "max_tokens": 1024,
  "stream": false,
  "thinking": {"type": "disabled"},
  "messages": [
    {"role": "system", "content": "<reader_prompt_field5.txt exact bytes>"},
    {"role": "user", "content": "<PACKAGE/PROBE body above>"}
  ]
}
```

No prior messages. No Labs transcript. No project files except the bytes above.

---

## 4. Unresolved limitations (do not paper over)

1. **No pin-able snapshot id.** `/models` does not return `DeepSeek-V4.1-Flash-YYYYMMDD`. Alias can move.
2. **`deepseek-v4-pro` scheduled silent remap** 2026-09-14 04:00 UTC. Not used.
3. **Seed UNSUPPORTED.** temperature 0 is an attempt, not a determinism proof.
4. **Provider default thinking** on Flash is thinking-enabled in some docs examples. Contract **requires** `thinking.type=disabled`. A later run that omits this field is off-contract.
5. **Context-cache** is provider-side. Do not implement custom KV. Repeated system prefix is allowed; do not treat cache hits as science.
6. **Single-provider.** Results will not generalize. Pre-declare non-generalizing.
7. **I7 MINOR** remains: CAND-03 S1 gold is the interior pair of id-sorted holds. Protocol forbids reading T1 order as time. Task unchanged.

---

## 5. Hygiene this pass

| Item | Action |
|------|--------|
| CAND-03 `why_not_on_T1` | Updated to id-order + pine + I7 |
| I7 | Documented MINOR on CAND-03; gold unchanged |
| CAND-04 | Serialized under `CANONICAL_ID_ASC_NON_TEMPORAL`; probes/wording/gold unchanged; item bags unchanged; `why_not_on_T1` + I7-class MINOR (rye last under id-sort) |

| File | SHA-256 |
|------|---------|
| CAND-03 | `1dcab73a20e9e6156af21c9e7cdf85faf088df57452897eacae027bab5a96167` |
| CAND-04 (pre-hygiene) | `a83e22c0377f491fad465a9a2993979560a4c6060e95c085b20d7a2b4340cb9e` |
| CAND-04 (this pass) | `33238523bb2d0edef8de234fb25a62ad766281b1792353acb97f03f81cb3aac2` |
| `reader_prompt_field5.txt` | `966400916b79e7025ed22c325e7d858e08ff2e89c0cc024606d7eb429878a349` |

---

## 6. Ten-field matrix after Field 5 candidate

| # | Field | Status |
|---|-------|--------|
| 1 | Primary confirmatory surface | **PARTIAL** |
| 2 | Fixture set | **PARTIAL** (CAND-03/04 candidates; EVIDENCE empty; PILOT_ONLY FX-01/02) |
| 3 | Queries | **PARTIAL** |
| 4 | Equivalence | **PARTIAL** |
| 5 | Reader / model freeze | **FROZEN_CANDIDATE** — identity known; weights unpinned |
| 6 | Semantic rubric | **PARTIAL** |
| 7 | Reviewer procedure | **PARTIAL** |
| 8 | Complexity / cost | **PARTIAL** |
| 9 | Ledger envelope | **PARTIAL** |
| 10 | Absolute adequacy | **PARTIAL** |

**FROZEN science fields: 0 / 10.** Field 5 is a candidate contract, not a 10-field freeze.

```text
FIELD_5                    = FROZEN_CANDIDATE
FIELD_5_MODEL_IDENTITY     = CLEARED
SNAPSHOT_PINNED            = NO
ALIAS_MUTABLE              = YES
FINAL_PREREG_REVIEW        = NOT_READY
EXPERIMENT_AUTHORIZATION   = NOT_AUTHORIZED
```

STOP. No model output. No Evidence. No merge. No PR.
