# CONT-E0T Field 5 — Source reconciliation (bounded)

**Return:** `FIELD_5 = FROZEN_CANDIDATE`  
**Identity:** `FIELD_5_MODEL_IDENTITY = CLEARED`  
**Weights:** `SNAPSHOT_PINNED = NO` — identity known, weights not immutably pinned.  
**Not:** experiment GO. No reader. No fixture. No Evidence.

Fetched again on this computer: `2026-09-12T16:31:54Z`.

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
NO READER INVOCATION
```

---

## 1. Owner classification accepted

| Item | Class |
|------|--------|
| Live `/models` IDs `deepseek-flash`, `deepseek-v4-pro` | current catalog |
| 2026-09-10 release/changelog: `deepseek-flash` = DeepSeek-V4.1-Flash | current official identity |
| `deepseek-v4-flash` | retired compatibility alias |
| `deepseek-v4-pro` routes to V4.1-Flash from 2026-09-14 04:00 UTC | official route notice (`news260910`) |
| `DeepSeek-V4-Flash-0731` | **HISTORICAL** (changelog dated 2026-07-31) — not a competing current identity |

---

## 2. Alleged contradictory footnote — exact sources

Same sentence on three current official URLs (HTTP 200, this computer):

| URL | HTML SHA-256 (this fetch) |
|-----|---------------------------|
| https://api-docs.deepseek.com/ | `6e2eb037db92ebef6a8f6408d87c12318c973388d6e27321606bb0e67dd67a6c` |
| https://api-docs.deepseek.com/quick_start/pricing/ | `755aa9b488d1185cba016ca4de3b3b6b8f593f5e13e5f9f961305289a5c8d242` |
| https://api-docs.deepseek.com/updates/ (entry Date: 2026-09-10) | `da7f5c4919ed8874ff575dc1c7c91da36e5b141a1b17b43309f3d75156469185` |

**Exact quote:**

> In response to user demand, we have decided to continue providing API services for DeepSeek V4 Pro after September 14, 2026, with the billing method remaining unchanged. We will provide further notice should there be any changes.

**Classification (this sentence only):**

| Clause | Class |
|--------|--------|
| "continue providing API services for DeepSeek V4 Pro" | **(b) API route availability** — the `deepseek-v4-pro` id remains callable |
| "billing method remaining unchanged" | **(c) billing** |
| served weights / model identity after 2026-09-14 04:00 UTC | **not stated** |

It does **not** say that `deepseek-v4-pro` continues serving V4-Pro weights after 2026-09-14 04:00 UTC.  
It does **not** name `DeepSeek-V4-Pro-0813` as the post-cutoff served model.  
It does **not** contradict the 2026-09-10 Flash identity (`deepseek-flash` = DeepSeek-V4.1-Flash).

Official route notice (https://api-docs.deepseek.com/news/news260910/ , HTML SHA `420cbb7b5e8e97632fa45cb49cd2b5f22b57c8f9e125d1c34a22bd67bbc33705`):

> Starting at 04:00 UTC on Sept 14, 2026, all `deepseek-v4-pro` requests will route to V4.1-Flash at V4.1-Flash rates.

Availability of the Pro **id** plus unchanged **billing** can coexist with a later **route** of that id onto V4.1-Flash. That is not a served-identity contradiction for `deepseek-flash`.

---

## 3. Pricing table note (not the footnote; not used to re-open conflict)

https://api-docs.deepseek.com/quick_start/pricing/ still prints a MODEL VERSION cell `DeepSeek-V4-Pro-0813` on the `deepseek-v4-pro` column. Today is 2026-09-12 (before the stated cutoff). That cell does not say weights remain V4-Pro after 04:00 UTC on 2026-09-14. Not treated as a current-identity competitor to `deepseek-flash`.

---

## 4. Cleared identity (candidate)

| Field | Value |
|-------|--------|
| API id | `deepseek-flash` |
| Provider label | DeepSeek-V4.1-Flash |
| Snapshot pinned | **NO** |
| Alias mutable | **YES** |
| Status | **MODEL IDENTITY KNOWN; WEIGHTS NOT IMMUTABLY PINNED** |

`FIELD_5_MODEL_IDENTITY` source conflict **cleared**.  
Previous `SOURCE_CONFLICT` on this axis is withdrawn.

Wrapper pins unchanged: `thinking=disabled`, `temperature=0`, `top_p=1`, tools/memory/web=NONE, one fresh call per fixture/arm/probe.

```text
FIELD_5                    = FROZEN_CANDIDATE
FIELD_5_MODEL_IDENTITY     = CLEARED
SNAPSHOT_PINNED            = NO
ALIAS_MUTABLE              = YES
FINAL_PREREG_REVIEW        = NOT_READY
EXPERIMENT_AUTHORIZATION   = NOT_AUTHORIZED
```

STOP.
