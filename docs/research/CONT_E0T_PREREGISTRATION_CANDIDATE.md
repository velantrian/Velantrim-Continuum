# CONT-E0T Preregistration Candidate

**BASELINE SHA:** `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`  
**Repository:** `velantrian/Velantrim-Continuum`  
**Branch intent:** `research/cont-e0t-prereg-author`  
**Document role:** `CONT-E0T_PREREGISTRATION_CANDIDATE`  
**Status:** **CANDIDATE ONLY** — not evidence-locked, not Pilot, not Evidence, not architecture authority  
**Protocol family:** `CONT-E0T` (successor protocol; **≠** historical `E0-T`)

---

## 0. Authority and non-claims

### 0.1 What this document is

Smallest defensible preregistration **candidate** for **CONT-E0T**, a new Continuum successor protocol that corrects a causal isolation failure of historical E0-T arm `T2` (event-log → deterministic projection): a projection-equivalent final state can be derived without a **genuine accepted trajectory**, so ordinary continuation probes do not isolate trajectory value.

### 0.2 What this document is not

- Not a rewrite, deletion, or edit of `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`.
- Not a change to historical E0-T arms `T0`–`T4`, Gold/Oracle, harness, Pilot, or Evidence Lock state.
- Not experiment execution, paid model run, merge authority, PR authority, or architecture promotion.
- Not a claim that event sourcing / ledgers are required IDPS architecture (see AGENTS.md / Experiment 0 null hypothesis).
- Not a freeze of production event alphabet, storage backend, or ontology.

### 0.3 Namespace freeze (candidate)

| Identifier | Meaning |
|---|---|
| `CONT-E0T` | This successor protocol family |
| `CONT-T1` / `CONT-E0T:T1` | Bounded **current** resume-relevant representation |
| `CONT-T2` / `CONT-E0T:T2` | Same current resume-relevant semantics **plus** bounded **genuine accepted trajectory** |

Do **not** use bare `T1` / `T2` in CONT-E0T prose where collision with historical E0-T arms is possible.

Historical E0-T `T0`–`T4` remain reserved exclusively for Experiment 0 Transfer Isolation.

### 0.4 Owner decision already recorded for this candidate effort

- CONT-E0T is a **new** successor protocol in this repo.
- E0-T ≠ CONT-E0T.
- Historical E0-T `T2` failed to isolate genuine trajectory (final state could be projection-derived without trajectory credit).
- CONT-E0T is the causal correction: compare competent current resume state vs same current semantics + bounded genuine accepted trajectory.
- `Graphiti_fractal_lab` is **pointer-only**, not a write target of this candidate.
- No experiment / merge / architecture promotion from this document alone.

### 0.5 Frozen read set used for this candidate (this SHA only)

- `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` (historical, read-only)
- `STATUS.md`, `docs/ai/CURRENT_STATE.md`, `docs/ai/README.md`, `docs/research/README.md`
- `RESEARCH_OVERVIEW.md`, `README.md`, `AGENTS.md`, `project-state.json`

MODEL OUTPUT ≠ STATE AUTHORITY. GitHub remains lifecycle authority; `project-state.json` remains selected semantic authorization authority for Experiment 0 gates (unchanged by this candidate).

### 0.6 Classification legend

Each field below is tagged exactly one of:

- **FROZEN** — binding for this candidate as written
- **PARTIAL** — direction fixed; concrete binding incomplete
- **MISSING** — required before any CONT-E0T lock/evidence; not invented here
- **SOURCE CONFLICT** — frozen sources disagree (none identified for CONT-E0T semantics at this SHA)

Numeric acceptance thresholds are **not invented**. Historical Experiment 0 explicitly refuses arbitrary percentages (e.g. 95%/98%/0.85) and this candidate inherits that refusal. Gates of the form 100%/0%/0% are **not imported**.

**Structured comparison + blind semantic equivalence** for non-byte-identical current-state packages remains **PROPOSED** (not independently justified to selection in this candidate).

---

## 1. Research question (CONT-E0T)

> After correct resume-relevant **current** process semantics already exist, does a bounded **genuine accepted trajectory** add material value for **primary resume continuation** beyond a competent bounded current representation — after cost/complexity and without giving trajectory automatic credit?

Primary null (aligned with Experiment 0 / AGENTS.md, restated for CONT-E0T):

> A competent bounded current resume-relevant representation (`CONT-T1`) may be sufficient for primary resume continuation; trajectory credit requires material gain that survives separate cost accounting.

---

## 2. Causal correction relative to historical E0-T `T2`

```text
Historical E0-T T2 risk:
  Oracle current state
        ↓
  event log that can be reconstructed from final projection
        ↓
  deterministic projection ≡ T1 current state
        ↓
  continuation probes pass without isolating genuine trajectory

CONT-E0T correction:
  shared current resume-relevant semantics
        ├─ CONT-T1: deliver current package only
        └─ CONT-T2: deliver same current semantics + bounded genuine accepted trajectory
              ↓
  (a) final-state equivalence check on current resume fields
  (b) primary resume probes (THEN/historical off primary)
  (c) separate cost/complexity
  (d) absolute adequacy ≠ mere equivalence
```

---

## 3. Ten-field candidate

### Field 1 — Primary confirmatory surface

**Status: PARTIAL**

**FROZEN direction**

- Primary confirmatory surface = **resume-now functional continuation** from the delivered package alone.
- Successor receives only the arm package (`CONT-T1` or `CONT-T2`) plus frozen reader instructions; no hidden Oracle, no evaluator metadata, no sibling-arm leakage.
- Target is **functional continuity**, not hidden-state identity (Experiment 0 / RESEARCH_OVERVIEW).

**PARTIAL**

- Exact primary probe templates, action space, and per-fixture allowed/forbidden/undetermined actions are not locked in this candidate.

**MISSING**

- Concrete held-out primary probe wording set and probe-order randomization rule for CONT-E0T.

**Hard exclusion (FROZEN direction)**

- Historical / `THEN` / trajectory-audit / “what happened earlier” queries are **off the PRIMARY resume outcome**. They may exist only as **secondary diagnostic** surfaces and must not decide primary confirmatory success.

---

### Field 2 — Frozen fixture set

**Status: MISSING** (requirements PARTIAL)

**PARTIAL requirements (not a freeze of IDs)**

Each CONT-E0T fixture must, before any evidence lock:

- be human-authored / experimenter-fixed before runs;
- include mid-task resume position with active goal, constraints, decisions, rejected alternatives, unresolved/contested items, and execution unknowns where relevant (reuse Experiment 0 Oracle *intent*, not E0 fixture IDs as automatic CONT fixtures);
- include a **genuine accepted trajectory** subset that is **not reconstructible solely by expanding the final snapshot** into synthetic `SET_*` / backfilled events;
- declare pilot vs evidence partition if Cont-E0T ever reaches those modes;
- keep evaluator metadata out of model prompts.

**MISSING**

- Concrete CONT-E0T `fixture_id` set, family taxonomy, variant IDs, and hashes.
- Binding to any existing Experiment 0 approved Transfer Oracle path is **not** automatic and is **not** performed by this candidate.

**Pointer-only**

- `Graphiti_fractal_lab` may be cited elsewhere as external pointer context; it is **not** a fixture write target here.

---

### Field 3 — Frozen queries per fixture

**Status: MISSING** (dual-class rule PARTIAL)

**PARTIAL rule**

For every fixture, queries must be pre-declared in two disjoint classes:

1. **PRIMARY — resume-now** (confirmatory)
2. **SECONDARY — historical / THEN / trajectory-audit** (diagnostic only)

**MISSING**

- Exact query text per fixture, expected answer keys, and secondary-only scoring sheets.

**FROZEN direction**

- Secondary-class performance must not be averaged into the primary confirmatory surface.

---

### Field 4 — Operational CONT-T1 / CONT-T2 final-state equivalence check

**Status: PARTIAL**

**FROZEN direction**

1. **CONT-T1** delivers a competent bounded **current** resume-relevant representation. It must **not** be deliberately impoverished and must **not** be disguised CONT-T2 (no smuggled trajectory ledger under another name).
2. **CONT-T2** delivers the **same** current resume-relevant semantics **plus** a bounded genuine accepted trajectory envelope (Field 9).
3. Before attributing any primary resume difference to trajectory, run an operational **final-state equivalence check** on the **current resume-relevant fields** implied by CONT-T1 vs CONT-T2.
4. If CONT-T2’s “events” are only a serialization of the final snapshot (fake SET-from-final-state), the arm is **protocol-invalid** for trajectory credit, regardless of probe scores.

**PARTIAL**

- Exact field list / schema version for “current resume-relevant semantics” is not frozen here.
- Byte-identical current projections are sufficient for equivalence when applicable.

**PROPOSED (not selected)**

- Where current packages are semantically equal but not byte-identical: **structured comparison + blind semantic equivalence** remains **PROPOSED** only. This candidate does **not** independently justify or select that method as locked CONT-E0T law.

**MISSING**

- Executable equivalence evaluator, acceptance atoms, and fail-closed invalid-arm detectors for fake trajectory.

---

### Field 5 — Reader / model freeze

**Status: PARTIAL**

**PARTIAL / reusable from Experiment 0 discipline**

When any CONT-E0T run is eventually authorized, record at minimum for generator and successor/reader:

- provider; exact model identifier/version where exposed; settings/temperature/seed where exposed;
- prompt/template version; input hash; output hash; token use; latency; cost provenance (`MEASURED` | `ESTIMATED` | `UNAVAILABLE`).

**FROZEN direction**

- CONT-T1 and CONT-T2 in a paired comparison use the **same frozen reader/successor configuration** unless a separately versioned protocol revision explicitly studies reader swap.
- Missing provider telemetry must not be replaced with invented measurements (Experiment 0 §21).

**MISSING**

- Exact CONT-E0T reader model IDs, settings, and prompt hashes (repository Experiment 0 pilot runtime values are also unresolved at this baseline; this candidate does not pin them).

---

### Field 6 — Semantic rubric

**Status: PARTIAL**

**PARTIAL candidate vocabulary** (adapted from Experiment 0 Transfer outcome labels; not re-proven)

Per primary resume item / probe, record separate labels rather than one weighted continuity score, e.g.:

- `PRESERVED`, `LOST`, `CORRECTED`, `PROMOTED`, `FABRICATED`, `MISATTRIBUTED`, `WRONG_LIFECYCLE_STATUS`

Epistemic preservation remains mandatory in spirit: unresolved must not be collapsed; caution must not become unauthorized hard prohibition; absent authorization must not be fabricated (Experiment 0 / RESEARCH_OVERVIEW).

**FROZEN refusals**

- No invented numeric acceptance thresholds in this candidate.
- No import of 100% / 0% / 0% (or similar) gates.
- No single NetValue / weighted utility collapse for architecture preference.

**MISSING**

- CONT-E0T-specific match specification, precedence table, and HARD FAIL bindings (if any) for resume probes.
- Any selected non-deterministic judge rule (LLM judge must not be primary truth for deterministic authorization/constraint/provenance fields — Experiment 0 posture retained as candidate discipline).

---

### Field 7 — Reviewer procedure

**Status: PARTIAL**

**PARTIAL procedure sketch**

1. Fixtures, expected primary resume answers, and secondary diagnostics authored before runs.
2. Deterministic package validation and final-state equivalence check run before human semantic scoring where contracts allow.
3. Human reviewers score primary resume adequacy against pre-bound expectations.
4. Arm identity (`CONT-T1` vs `CONT-T2`) **blinded** to semantic reviewers when feasible; unblinding only after scores are recorded.
5. Secondary historical/THEN diagnostics scored on separate sheets; cannot override primary surface.
6. Representation-generation failures attributed separately from successor interpretation failures when a generator is used (Experiment 0 §17 posture).

**MISSING**

- Binding review forms, attestation record schema, and CONT-E0T-specific human-reference gate analogous to Experiment 0 Issue #9 machinery.

---

### Field 8 — Complexity / cost accounting

**Status: PARTIAL** (accounting **structure** largely reusable; CONT binding incomplete)

**FROZEN direction**

Record separately — **do not collapse into NetValue**:

| Channel | Examples |
|---|---|
| Injection | input tokens/bytes to successor; object/record counts |
| Durable storage | bytes; record counts |
| Generation | summary/manifest/trajectory-packing calls; tokens; latency; cost |
| Projection / replay | deterministic materialization work; latency |
| Verification | schema checks; equivalence checks; probes; extra model/tool calls |
| Runtime / continuation | latency; model/tool calls; duplicated work; reorientation turns |

Each cost field carries provenance: `MEASURED` | `ESTIMATED` | `UNAVAILABLE`.

**PARTIAL**

- CONT-T2 ledger byte/record overhead vs CONT-T1 package must be reported as first-class deltas, but exact instrumentation hooks are not specified here.

**MISSING**

- CONT-E0T run-manifest schema version and mandatory hash set (Experiment 0 §22 is a template only).

---

### Field 9 — CONT-T2 ledger envelope

**Status: PARTIAL**

**FROZEN direction**

The CONT-T2 envelope must:

1. Carry the **same current resume-relevant semantics** used for CONT-T1 (Field 4).
2. Add a **bounded genuine accepted trajectory**: events/decisions that actually occurred in the fixture’s accepted history, with enough provenance to show they are not inferred solely from the final snapshot.
3. Remain **bounded** to resume-relevant accepted trajectory — not an unbounded world log.
4. **Forbid** fake trajectory construction whose event list is merely `SET`/`UPSERT` expansions of final state fields.

**PARTIAL**

- Logical envelope sections: `current_semantics`, `accepted_trajectory[]`, `provenance`, `bounds`, `hashes`.

**MISSING**

- Concrete envelope schema, event types, size bounds, and canonical hash algorithm for the envelope.

**Explicit non-freeze**

- Production event alphabet / ledger technology remain **not frozen** (AGENTS.md; Experiment 0 non-goals).

---

### Field 10 — Absolute adequacy boundary

**Status: PARTIAL**

**FROZEN direction**

```text
final-state equivalence ≠ absolute resume adequacy
CONT-T1 ≡ CONT-T2 (current fields) ≠ either arm is adequate
primary resume success ≠ license to credit trajectory without Field 4 + Field 8
```

- Adequacy for the primary surface means: from the delivered package alone, the frozen reader can continue functionally on **PRIMARY resume-now** queries/probes for that fixture.
- Equivalence only licenses a fair comparison; it does not declare sufficiency.
- Architecture-level comparison, if ever authorized, should follow Experiment 0’s qualitative classes without invented percentages:
  - `MATERIAL_GAIN`
  - `NO_MATERIAL_GAIN`
  - `TRADEOFF_INCONCLUSIVE`
  with HARD FAIL dominance retained as candidate discipline when HARD FAILs are eventually bound.

**MISSING**

- Absolute adequacy checklist atoms per fixture (pre-bound, non-post-hoc).
- Any numeric adequacy cutoffs (intentionally refused until independently justified in a later versioned protocol).

---

## 4. Field status summary

| # | Field | Status |
|---|---|---|
| 1 | Primary confirmatory surface | **PARTIAL** |
| 2 | Frozen fixture set | **MISSING** |
| 3 | Frozen queries per fixture | **MISSING** |
| 4 | Operational CONT-T1/CONT-T2 final-state equivalence check | **PARTIAL** |
| 5 | Reader/model freeze | **PARTIAL** |
| 6 | Semantic rubric | **PARTIAL** |
| 7 | Reviewer procedure | **PARTIAL** |
| 8 | Complexity/cost accounting | **PARTIAL** |
| 9 | CONT-T2 ledger envelope | **PARTIAL** |
| 10 | Absolute adequacy boundary | **PARTIAL** |

**SOURCE CONFLICT:** none identified among the frozen read set for CONT-E0T successor framing at baseline `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`.

**Selection note:** structured comparison + blind semantic equivalence = **PROPOSED**, not selected.

---

## 5. Stopping rule for this candidate artifact

```text
write CONT_E0T_PREREGISTRATION_CANDIDATE.md
        ↓
docs-only commit on research/cont-e0t-prereg-author
        ↓
🛑 STOP — no experiment, no Pilot, no Evidence, no merge, no architecture promotion
```

Further fixture/query/evaluator binding requires a separate owner-authorized protocol revision. This file alone does not alter `project-state.json` Experiment 0 authorization flags.

---

## 6. Canonical research posture (inherited, not re-litigated)

> Do not decide the architecture first. Measure the causal contrast that the protocol can actually isolate. Prefer minimum sufficient state. Complexity receives no prior credit.
