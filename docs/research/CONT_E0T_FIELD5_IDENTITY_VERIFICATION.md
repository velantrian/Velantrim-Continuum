# CONT-E0T Field 5 — Model identity verification

**Return:** `FIELD_5 = SOURCE_CONFLICT`  
**Also:** `FIELD_5_MODEL_IDENTITY = SOURCE_CONFLICT`  
**Not:** experiment GO. No reader call. No fixture sent. No Evidence. No PR/merge.

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
NO READER INVOCATION
NO COMPLETION
NO FIXTURE TO DEEPSEEK
```

Labs does **not** choose which official source is authoritative.

---

## 1. Live GET /models (this computer)

| Field | Value |
|-------|--------|
| UTC | `2026-09-12T16:22:28Z` |
| Endpoint | `https://api.deepseek.com/models` |
| Method | `GET` |
| Request body | none |
| HTTP | `200` |
| `content-type` | `application/json` |
| `content-length` | `153` |
| `date` | `Sat, 12 Sep 2026 16:22:28 GMT` |
| `x-ds-trace-id` | `3269e1f4012aaec7f5fe1792188eb74d` |
| `x-cache` | `Miss from cloudfront` |
| Body SHA-256 | `0c5d2ba6ebb791e893b0e7efed32c64415a633ed774e8d89dad8e33c4d69ae77` |
| Returned IDs | `deepseek-flash`, `deepseek-v4-pro` |

Raw artifact (Authorization redacted):  
`docs/research/cont_e0t_v2/field5_identity/GET_models_raw_2026-09-12.md`  
JSON sidecar: `docs/research/cont_e0t_v2/field5_identity/GET_models_2026-09-12.json`

Exact body:

```json
{"object":"list","data":[{"id":"deepseek-flash","object":"model","owned_by":"deepseek"},{"id":"deepseek-v4-pro","object":"model","owned_by":"deepseek"}]}
```

`deepseek-v4-flash` is **absent** from the live list.

---

## 2. Official DeepSeek docs (fetched 2026-09-12, `api-docs.deepseek.com`)

Doc scan sidecar: `docs/research/cont_e0t_v2/field5_identity/official_docs_scan_2026-09-12.json`

### 2a. Current primary pages — IDs match live `/models`

https://api-docs.deepseek.com/ and https://api-docs.deepseek.com/quick_start/pricing/ (HTTP 200, this computer):

> MODEL `deepseek-flash` (1) `deepseek-v4-pro` (2)  
> MODEL VERSION `DeepSeek-V4.1-Flash` / `DeepSeek-V4-Pro-0813`

> (1) Use `deepseek-flash` as the model name. The legacy names `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` are still accepted, but the corresponding models have been retired, their requests are served by the DeepSeek-V4.1-Flash model and billed at the Flash price.

> (2) In response to user demand, we have decided to continue providing API services for DeepSeek V4 Pro after September 14, 2026, with the billing method remaining unchanged. We will provide further notice should there be any changes.

https://api-docs.deepseek.com/api/create-chat-completion/ :

> Possible values: [`deepseek-flash`, `deepseek-v4-pro`]. Use `deepseek-flash` or `deepseek-v4-pro`.

`DeepSeek-V4-Flash-0731` does **not** appear on these current primary pages.

### 2b. Official news page — same current Flash id; **different** Pro story

https://api-docs.deepseek.com/news/news260910/ (HTTP 200):

> Set your model to `deepseek-flash`.

> V4-Flash & V4-Flash-Vision-Exp are retired. For compatibility, `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` temporarily route to V4.1-Flash.

> Starting at 04:00 UTC on Sept 14, 2026, all `deepseek-v4-pro` requests will route to V4.1-Flash at V4.1-Flash rates. This will continue until V4.1-Pro launches.

The remap claim **does exist** on this official news page.  
The same official site's current pricing/home footnote **contradicts** it (Pro continues after September 14).

### 2c. Official changelog — historical identity the external check cited

https://api-docs.deepseek.com/updates/ dated **2026-07-31** (still published):

> `DeepSeek-V4-Flash-0731` keeps the same model architecture and size as DeepSeek-V4-Flash-Preview, and was only re-post-trained.

Earlier changelog text still says to set the model name to `deepseek-v4-flash`.

Changelog **2026-09-10** on the same page:

> Change the model name to `deepseek-flash` to call the latest V4.1 Flash model. The previous-generation models V4 Flash and V4 Flash Vision Exp have been retired; for compatibility, the model names `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` are temporarily routed to V4.1 Flash. In response to user demand, we have decided to continue providing API services for DeepSeek V4 Pro after September 14, 2026…

---

## 3. Comparison (no authority pick)

| Claim | Live `/models` | Current primary docs | Official news 2026-09-10 | Official changelog 2026-07-31 |
|-------|----------------|----------------------|--------------------------|-------------------------------|
| Usable Flash id | `deepseek-flash` | `deepseek-flash` | `deepseek-flash` | `deepseek-v4-flash` |
| Lists `deepseek-v4-flash` as current | no | no (legacy / retired) | no (legacy route) | yes (then-current) |
| Version label | not in payload | `DeepSeek-V4.1-Flash` | `DeepSeek-V4.1-Flash` | `DeepSeek-V4-Flash-0731` |
| Pro after 2026-09-14 | n/a | continues, billing unchanged | remaps to V4.1-Flash @ 04:00 UTC | n/a |

External check (`deepseek-v4-flash` + `DeepSeek-V4-Flash-0731` as *current*) matches **historical official changelog**, not live `/models` and not current primary docs.

Live `/models` vs current primary docs: **IDs agree**.  
Official DeepSeek sources vs each other: **disagree** (current Flash id across generations; Pro remap vs continue).  
That is enough for `SOURCE_CONFLICT`. Labs does not pick.

---

## 4. Contract action this pass

- Did **not** rewrite the candidate id to `deepseek-v4-flash`. Live list does not contain that id.
- Did **not** treat the 2026-09-14 Pro remap as settled. Official pages disagree.
- Sampling pins unchanged if a later owner pick re-freezes the same wrapper: `thinking=disabled`, `temperature=0`, `top_p=1`, tools/memory/web=NONE, one fresh call per fixture/arm/probe.
- Previous `FIELD_5 = FROZEN_CANDIDATE` identity is **withdrawn** until owner names the authoritative source.

```text
FIELD_5                    = SOURCE_CONFLICT
FIELD_5_MODEL_IDENTITY     = SOURCE_CONFLICT
FINAL_PREREG_REVIEW        = NOT_READY
EXPERIMENT_AUTHORIZATION   = NOT_AUTHORIZED
```

STOP.
