# CONT-E0T Fields 1–4 + run-integrity (candidate freeze)

**Document role:** `CONT-E0T_FIELDS_1_4_RUN_INTEGRITY_CANDIDATE`  
**Status:** `READY_TO_AUTHOR_EVIDENCE`  
**Parent rules:** `PRE_EVIDENCE_RULES` accepted (`305eb4f8e520702ffc5d1425299d5a75438e60e2`)  
**Branch:** `research/cont-e0t-prereg-v22`  
**Date (record):** 2026-09-12

Not: experiment GO. Not Evidence objects. Not a reader call.

```text
PRE_EVIDENCE_RULES           = FROZEN_CANDIDATE   # owner-accepted
READY_TO_AUTHOR_EVIDENCE     = YES
EVIDENCE                     = []
ROSTER_PERSONS_UNFILLED      = YES  # blocks experiment GO, not authoring
EXPERIMENT_AUTHORIZATION     = NOT_AUTHORIZED
FINAL_PREREG_REVIEW          = NOT_READY
NO READER / NO EVIDENCE OBJECTS
```

CAND-03 / CAND-04 remain `DEVELOPMENT_DESIGN`. Do **not** promote.

---

## Field 1 — Confirmatory surface

### 1.1 Unit of analysis

**Confirmatory unit** = one PRIMARY probe × one Evidence fixture × the T1/T2 pair.

Justification: Field 10 already defines `T2_SUPERIOR` / `T2_INFERIOR` / `TIE_BOTH_ADEQUATE` / `BOTH_INADEQUATE` at that grain.  
This pass uses **one PRIMARY probe per fixture**, so unit = fixture-pair. No within-fixture probe cluster.

SECONDARY_HISTORY is recorded only. It does not enter the experiment-level rule.

### 1.2 Experiment-level Claim B decision rule

Let the planned set have `N = 4` confirmatory units (Field 2).  
A unit is **completed** only if both arms returned a scorable output under the locked `response.model` (run-integrity).

Counts on completed units:

| Symbol | Field 10 label |
|--------|----------------|
| `S` | `T2_SUPERIOR` |
| `I` | `T2_INFERIOR` |
| `T` | `TIE_BOTH_ADEQUATE` |
| `U` | `BOTH_INADEQUATE` |

**Fail-closed preconditions** (any one ⇒ cannot declare `B_SUPPORTED_BOUNDED`):

- any unit not completed (`PAIR_INCOMPLETE` / `CALL_FAIL` / identity abort);
- run abort under §Run integrity.

**Decision (invented now, not after outputs):**

| Result | Rule |
|--------|------|
| `B_SUPPORTED_BOUNDED` | all 4 completed **and** `S ≥ 3` **and** `I = 0` |
| `B_NOT_SUPPORTED` | all 4 completed **and** (`I ≥ 1` **or** `S = 0`) **and** `U < 4` |
| `MIXED` | all 4 completed **and** `I = 0` **and** `S ∈ {1,2}` |
| `UNDERDETERMINED` | any unit incomplete **or** identity abort **or** `U = 4` |

Reading:

- all ties (`S=0,I=0,T=4`) → `B_NOT_SUPPORTED` (no PRIMARY adequacy gain);
- all both-inadequate → `UNDERDETERMINED` (not a B test);
- one or two superiors, no inferior → `MIXED`, not a bounded support claim;
- any T2 inferior → `B_NOT_SUPPORTED`.

This is **not** Claim A, not event-sourcing necessity, not “no better T1 exists.”

---

## Field 2 — Evidence-set design

| Quantity | Freeze |
|----------|--------|
| NEW Evidence fixtures | **4** (`EVID-01` … `EVID-04`) |
| Scenario families | **2** |
| Fixtures per family | **2** |
| PRIMARY probes per fixture | **1** |
| Independent confirmatory units | **4** |
| SECONDARY probes | optional, non-confirmatory; at most 1; must pass D8 (gold not a T1 substring) |
| Stopping rule | **fixed N = 4**. No optional stopping. No adding / dropping fixtures after any reader output |

Families (patterns only; **new objects**, not CAND bytes):

| Family | Sketch |
|--------|--------|
| `FAM-HOLD-CLASS` | compose class-hold + channel-type + precedence + UNKNOWN |
| `FAM-MEMBER-CHANNEL` | compose member-of-class + class-hold + precedence + UNKNOWN |

Slots: EVID-01 and EVID-03 → `FAM-HOLD-CLASS`. EVID-02 and EVID-04 → `FAM-MEMBER-CHANNEL`.

CAND-03 / CAND-04 stay design references. Copying them into `partition: EVIDENCE` is forbidden.

---

## Field 3 — Query design

| Rule | Freeze |
|------|--------|
| PRIMARY probes per Evidence fixture | **1** |
| Non-independence | none inside a fixture (single PRIMARY). Families are repeated once; units remain separately scored; no pooling into a “family win” |
| Composition depth | gold must compose **≥ 4** current relations, including **one precedence** and **one UNKNOWN** |
| Wording | one direct resume question; no arm labels; no “history / trajectory / ledger” priming |
| No verbatim gold | gold sentence must not appear in `current_semantics` or `thin_trajectory` |
| No answer in rationale / position | `current_rationale` and `process_position` must not state the PRIMARY decision or the UNKNOWN resolution |
| No positional / order leakage | T1 lists `CANONICAL_ID_ASC_NON_TEMPORAL`; do not encode time in id strings or list position |
| No model screening | do not edit or keep a fixture because a model showed a T1/T2 delta |

---

## Field 4 — T1/T2 equivalence (executable)

A future Evidence object is admissible only if **all** hold (fail-closed):

| ID | Check |
|----|--------|
| E4.1 | Reader CONT-T1 and CONT-T2 `current_semantics` are byte-identical (canonical JSON) |
| E4.2 | `current_semantics` keys = frozen CURRENT_SEMANTICS schema; no smuggled trajectory / provenance / pad |
| E4.3 | T1 is schema-complete (every required field present; list items have `id` + `text` + `current`); **not** intentionally impoverished vs that schema |
| E4.4 | `thin_trajectory` is `ID_REFS_ONLY`: `{seq, changes:[{op, field, id}]}` only; `op ∈ {ADD,SET,REMOVE}` |
| E4.5 | Trajectory contains no current-answer text (`from`/`to`/gold substring forbidden) |
| E4.6 | `provenance_validator_only` and `audit_snapshots_validator_only` never appear in either reader package |
| E4.7 | Every T1 list is `CANONICAL_ID_ASC_NON_TEMPORAL` |
| E4.8 | `2 ≤ n_transitions ≤ 4`; `fold(thin)` (validator-only) equals current; no `envelope_pad` |
| E4.9 | PRIMARY remains T1-solvable: every `must_compose` id exists on T1 |
| E4.10 | SECONDARY gold, if present, is not a substring of CONT-T1 JSON |

Existing PILOT validator stays the PILOT checker. Evidence objects use these E4.* checks before any reader call. No Evidence files exist in this pass, so the checks are not executed on confirmatory bytes.

---

## Run integrity — mutable alias

`deepseek-flash` is a mutable alias. `SNAPSHOT_PINNED = NO`.  
Order is frozen **now**, before any call.

Committed schedule: `docs/research/cont_e0t_v2/RUN_ORDER_SCHEDULE.json`

| Slot | Family | Arm order |
|------|--------|-----------|
| EVID-01 | FAM-HOLD-CLASS | T1 then T2 |
| EVID-02 | FAM-MEMBER-CHANNEL | T2 then T1 |
| EVID-03 | FAM-HOLD-CLASS | T2 then T1 |
| EVID-04 | FAM-MEMBER-CHANNEL | T1 then T2 |

Rules:

- each T1/T2 pair is **adjacent** (no other fixture between the two arms);
- arm-first order is **ABBA** (2 T1-first, 2 T2-first);
- do not choose or swap order after outputs;
- same Field 5 reader contract both arms;
- record UTC timestamp, `response.model`, `RETRY` / `CALL_FAIL` on every call.

### Fail-closed (do not silently continue)

| Event | Action |
|-------|--------|
| First scorable `response.model` | lock as `RUN_MODEL_LOCK` |
| Later `response.model` ≠ lock | **abort run**; remaining slots uncalled; result `UNDERDETERMINED` |
| Provider / request id changes (`deepseek-flash` no longer the request, or endpoint identity changes) | **abort**; `UNDERDETERMINED` |
| Only one arm of a pair succeeds | that unit `PAIR_INCOMPLETE`; **do not** score the surviving arm confirmatory; experiment cannot be `B_SUPPORTED_BOUNDED` |
| Transport retry | at most one, as Field 5; still record `RETRY` |

A model-identity transition mid-run is a stop, not a footnote.

---

## Field 7 reminder

`ROSTER_PERSONS_UNFILLED` may stay open while Evidence is **authored**.  
It **must** be filled before `EXPERIMENT_AUTHORIZATION`.

---

## Ten-field matrix

| # | Field | Status |
|---|-------|--------|
| 1 | Confirmatory surface | **FROZEN_CANDIDATE** (unit + B decision rule) |
| 2 | Evidence set | **FROZEN_CANDIDATE** (N=4, 2 families; objects not yet authored) |
| 3 | Queries | **FROZEN_CANDIDATE** (1 PRIMARY; compose ≥4) |
| 4 | Equivalence | **FROZEN_CANDIDATE** (E4.1–E4.10) |
| 5 | Reader / model | **FROZEN_CANDIDATE** (weights unpinned) |
| 6–10 | Pre-evidence rules | **FROZEN_CANDIDATE** (owner-accepted) |

**FROZEN science fields: 0 / 10.**  
Evidence objects: **0**.

```text
READY_TO_AUTHOR_EVIDENCE     = YES
EVIDENCE                     = []
FINAL_PREREG_REVIEW          = NOT_READY
EXPERIMENT_AUTHORIZATION     = NOT_AUTHORIZED
```

STOP. No Evidence objects. No reader. No merge. No PR.
