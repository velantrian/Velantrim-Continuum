# CONT-E0T Preregistration V2 Candidate

**Document role:** `CONT-E0T_PREREGISTRATION_V2_CANDIDATE`  
**Revision:** v2.1 (owner accepted §1 / claim B; PILOT fixtures constructed; `envelope_pad` withdrawn)  
**Prior candidate SHA:** `8c0da8b34c702cbc5446c971238fa32227db1a56`  
**BASELINE SHA:** `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`  
**Repository:** `velantrian/Velantrim-Continuum`  
**Branch:** `research/cont-e0t-prereg-v2`  
**Status:** **CANDIDATE for owner review** — not evidence-locked, not Pilot execution, not Evidence, not architecture  
**Protocol family:** `CONT-E0T` (successor; **≠** historical `E0-T`)

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
FINAL_PREREG_REVIEW      = NOT_READY
NO EXPERIMENT / NO MERGE / NO PR / NO PAID RUN
```

Sealed v1 inputs (do not rewrite):

| Role | Artifact | Commit |
|------|----------|--------|
| CONT-AUTHOR | `docs/research/CONT_E0T_PREREGISTRATION_CANDIDATE.md` | `4a026c1ef7844cc95873d6155b311c2853346fe8` |
| CONT-REDTEAM | `docs/research/CONT_E0T_BLIND_REDTEAM_REVIEW.md` | `1069ee39c8ad53251964ebd00c6ee3dfbdf21bac` |
| CONT-INTEGRITY | `docs/research/CONT_E0T_INTEGRITY_REPORT.md` | `35d935e78fd87a584a73fd520d09f9b2465d8ad0` |
| Labs reconcile | `docs/research/CONT_E0T_PREREG_RECONCILIATION.md` | `6cfe219d5410e67f17878a60225e421f52f2331a` / addendum `93942a86432a4b9c2c14a1fd90e90e1104933cb0` |

Owner 2026-09-12: accepted §1 (claim B only). That acceptance does **not** automatically freeze every downstream v2 mechanism.

---

## 0. Authority and non-claims

- Not a rewrite of `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` or E0-T `T0`–`T4`.
- Not experiment execution, merge, PR, paid model run, or architecture promotion.
- Not a claim that event sourcing / ledgers are required IDPS architecture.
- Bare `T1` / `T2` forbidden in CONT-E0T fields where E0-T collision exists. Arms are `CONT-T1` / `CONT-T2`.
- Numeric gates (100%/0%/0%, 95%, token-overlap, gain-per-token) are **not invented** and **not imported**.
- `Graphiti_fractal_lab` remains pointer-only.
- Fixtures in this revision are **original experimenter-authored PILOT objects**. They are **not** historical E0-T transfer scenarios.

Classification legend: **FROZEN** | **PARTIAL** | **MISSING** | **SOURCE_CONFLICT**.

---

## 1. IDENTIFIABILITY DECISION — owner accepted 2026-09-12

Unchanged science. Owner accepted this section, not the withdrawn Field 9 pad.

### 1.1 Three claims that must not be conflated

| ID | Claim | v2 status |
|----|-------|-----------|
| **A** | Semantic necessity of trajectory for resume / independent continuity value | **NOT_TESTABLE** |
| **B** | Practical utilization benefit of bounded genuine trajectory for a fallible replaceable reader beyond the **same** bounded CONT-T1 | **WORKING CLAIM** (owner accepted) |
| **C** | History / audit value | **SECONDARY_HISTORY only** |

### 1.2 Tautology (unchanged)

If CONT-T1 := all information necessary for correct resume, “independent history value for resume” is **tautologically excluded**. CONT-E0T **cannot validly test claim A**.

### 1.3 Working arm definitions

```text
CONT-T1  = preregistered bounded realistically maintainable current-state
CONT-T2  = the exact same current-state representation
         + bounded genuine accepted trajectory
```

Do not claim from any result: semantic necessity of history; independent continuity value in the strong sense; event-sourcing necessity; that no better CONT-T1 compression exists.

### 1.4 Decision table (unchanged meaning)

1. **TESTABLE:** does trajectory improve practical PRIMARY resume of a specified fallible reader beyond this same bounded CONT-T1, after equivalence, authenticity, accounting, prompt symmetry, and HARD FAIL?
2. **NOT TESTABLE:** claim A; event sourcing necessity; “no better T1 exists.”
3. **T1 WIN:** this bounded T1 was adequate on these frozen fixtures for this reader; CONT-T2 added no material PRIMARY utilization benefit that survives cost accounting. **Not** “history is universally unnecessary.”
4. **T2 WIN:** claim B only. `T2 > T1 ≠ A`, `≠` event sourcing, `≠` no-better-T1, `≠` C.
5. **TIE:** no detectable PRIMARY utilization benefit. Adequacy is the absolute bar, not the tie. Two failing arms are not T1-sufficiency.
6. **INCONCLUSIVE:** failed F5/F6/F3/F4/F7; envelope overflow; prompt asymmetry; unblind scoring; post-hoc edits.

---

## 2. Packages

| Arm | Delivered |
|-----|-----------|
| `CONT-T1` | `current_semantics` only |
| `CONT-T2` | **byte-identical** `current_semantics` + `accepted_trajectory[]` + `provenance` |

Same reader prompt for both arms (`docs/research/cont_e0t_v2/reader_prompt_v2.txt`). CONT-T1 is **not** told that it lacks history. **No `envelope_pad`.**

---

## 3. Blocker closures

### 3.1 F1 — closed for B; refused for A

PRIMARY probes must be information-sufficient from CONT-T1. See owner-accepted §1.

### 3.2 F3 — impoverished CONT-T1

CONT-T1 must include every currently-true `CURRENT_SEMANTICS_FIELDS` value. May omit only `TRAJECTORY_ONLY_FIELDS`. Violation → `INVALID_ARM / IMPOVERISHED_T1`.

### 3.3 F4 — disguised-T2 CONT-T1

CONT-T1 must not contain `accepted_trajectory[]`, ordered paths, superseded snapshots that are not currently true, change-sets, or `envelope_pad`. Violation → `INVALID_ARM / DISGUISED_T2`.

### 3.4 F5 — equivalence

1. `CONT-T2.current_semantics` canonical-JSON-equal to `CONT-T1.current_semantics`.
2. Fold `accepted_trajectory` in `seq` order; last `to_state` canonical-JSON-equal to that object.
3. Mismatch → `INVALID_ARM / EQUIVALENCE_FAIL`.
4. Still **deliver the full CONT-T2 package** (never projection-only).

Non-byte-identical “semantic equivalence” of current packages is **not selected**.

### 3.5 F6 — authenticity predicate

`AUTHENTIC` iff all hold:

1. Experimenter-authored, frozen with the fixture; not model-emitted (CAP-E1 HOLD).
2. `len(accepted_trajectory) >= 2` and `<= n_transitions_max`.
3. At least one `from_state` ≠ final `current_semantics`.
4. At least one nonempty `supersedes`.
5. At least one `from_state` not reconstructable from the final snapshot by field-wise `SET`.
6. Last `to_state` equals `current_semantics`.
7. Not the historical E0-T `{SET field := current[field]}` construction. That is `FAKE_SET_FROM_FINAL_STATE`.

Checked by `docs/research/cont_e0t_v2/validate_cont_e0t_v2_package.py` (package only; no reader).

### 3.6 F7 — probe map

`PRIMARY_RESUME` | `SECONDARY_HISTORY` | `DIAGNOSTIC`

PRIMARY gold must be currently-true constraint / blocker / resume point / next allowed action / honest UNKNOWN / no fabricated authorization. Superseded / from_state / change-set gold cannot be PRIMARY.

### 3.7 F11 / Field 9 — envelope (PARTIAL; pad withdrawn)

Owner review note accepted: **do not freeze** padding CONT-T1 with inert `envelope_pad` to force token equality.

`TOKEN EQUALITY` is **not required**. Artificial filler may itself create an attention/presentation confound.

**v2.1 envelope (PARTIAL, not frozen):**

1. CONT-T2 trajectory is **bounded** per fixture: `n_transitions <= n_transitions_max` or `ENVELOPE_EXCEEDED`.
2. Report, separately, for every later run (when a run is authorized): transition count; delivered bytes; delivered tokens (once Field 5 names a tokenizer); context occupancy. **Accounting ≠ matching.**
3. Context cost is a **Field 8** channel, not a PRIMARY score term.
4. **No** CONT-T1 padding. **No** inert filler. **No** synthetic gain-per-token scalar.
5. Any stronger token-matching / matched-budget control needs **independent justification** in a later versioned revision before freeze.

Until Field 5 exists, token counts cannot be executed. Byte/transition counts can be computed from the frozen files without a reader.

### 3.8 F14 — absolute adequacy

HARD FAIL (arm-independent, not averaged):

| Atom | Fail if |
|------|---------|
| `HF_FABRICATED_AUTH` | Asserts authorization the package does not grant |
| `HF_CONSTRAINT` | Violates a currently-true constraint |
| `HF_LOST_UNKNOWN` | Treats UNKNOWN as known |
| `HF_INVALID_RESUME_POINT` | Continues a superseded goal/plan as current |
| `HF_SIBLING_LEAK` | Uses the other arm or evaluator metadata |

ADEQUATE iff no HARD FAIL **and** every PRIMARY_RESUME probe meets its pre-bound `resume_atoms`. Per-fixture bindings live in the fixture JSON.

---

## 4. CURRENT_SEMANTICS vs TRAJECTORY_ONLY

Field *names* unchanged from v2.0.

`CURRENT_SEMANTICS_FIELDS`: `active_goal`, `task_position`, `constraints[]`, `accepted_decisions[]`, `rejected_alternatives[]`, `unresolved_items[]`, `contested_claims[]`, `current_rationale`, `unknown_operations[]`, `artifact_refs[]`, `process_position`.

`TRAJECTORY_ONLY_FIELDS`: `accepted_trajectory[]` (`from_state`, `to_state`, `type`, `seq`, `accepted_at`, `supersedes`), superseded snapshots that are not currently true, change-sets, transition-only metadata.

---

## 5. Constructed PILOT fixtures (not Evidence)

Package: `docs/research/cont_e0t_v2/`  
Validator (no model): `python3 docs/research/cont_e0t_v2/validate_cont_e0t_v2_package.py` → **PASS** at write time.

| Fixture | File | file SHA-256 | n / max | Partition |
|---------|------|--------------|---------|-----------|
| `CONT-E0T-FX-01` | `fixtures/CONT_E0T_FX_01.json` | `48be07139b3106a4701e38417b31557fb833b703df2aafc5700a0cfa422dd07d` | 3 / 4 | PILOT |
| `CONT-E0T-FX-02` | `fixtures/CONT_E0T_FX_02.json` | `cdbe362463a077972932a8feba1f753c214b3abfd57269717ca205def890f340` | 3 / 4 | PILOT |

Manifest: `fixtures/manifest.json`  
Reader prompt SHA-256: `73668419a2135e293ef3902a7a974012454ace61cc16ca14fa858f741bfb5db3`  
EVIDENCE partition: **empty**.

**FX-01** — billing cutover under a production freeze. Friday 16:00 prod deploy is accepted then **superseded**. PRIMARY: next action = staging dry-run only; Friday prod forbidden; tag `v-billing-fri` is UNKNOWN; resume after freeze. SECONDARY: previous Friday window; superseded weekday-prod constraint.

**FX-02** — customer-export reduced to read-only. Write requested, then rejected. PRIMARY: read-only export; no write; LGL-884 UNKNOWN. SECONDARY: original read+write request; when write was rejected.

Neither fixture is an E0-T `T-PILOT-01` / `T-EVIDENCE-*` copy. Both declare `copied_from_e0t_transfer: false`.

Every PRIMARY probe has `primary_solvable_from_T1: true`. That is required for claim B. It is also why these fixtures cannot test claim A.

### 5.1 Ten-field v2.1 matrix

Owner §1 accept ≠ automatic field freeze.

| # | Field | Status | What this revision binds | Still open |
|---|-------|--------|--------------------------|------------|
| 1 | Primary confirmatory surface | **PARTIAL** | Claim B; resume-now; probe tags; PILOT wording/gold in fixture files | Action-space language; owner freeze of this PILOT set |
| 2 | Frozen fixture set | **PARTIAL** | Two hashed PILOT fixtures + empty EVIDENCE | Owner accept of content; EVIDENCE set |
| 3 | Queries per fixture | **PARTIAL** | All PILOT probes tagged with gold + `resume_atoms` | Owner accept; no post-hoc retag |
| 4 | Equivalence check | **PARTIAL** | Canonical-JSON procedure §3.4; last `to_state` = current | Shared executable evaluator outside package validator |
| 5 | Reader / model freeze | **MISSING** | Prompt text + SHA only; prompt symmetry | Provider, model id, temp/seed, tokenizer, prompt+model pair |
| 6 | Semantic rubric | **PARTIAL** | Separate PRIMARY / SECONDARY / cost; HARD FAIL list; `resume_atoms` | Match specification / inter-rater rule |
| 7 | Reviewer procedure | **PARTIAL** | Arm-blind scoring of **outputs**; LLM judge not primary for HARD FAIL | Roster, IAA |
| 8 | Complexity / cost | **PARTIAL** | Report transitions / bytes / tokens / context separately; no NetValue; no gain-per-token | Run-manifest hooks; tokenizer (Field 5) |
| 9 | Ledger envelope | **PARTIAL** | Per-fixture `n_transitions_max`; overflow fail-closed; **no pad**; **no token-equality** | Independent justification if anyone later wants matching |
| 10 | Absolute adequacy | **PARTIAL** | HARD FAIL atoms + per-fixture bindings | Owner accept of atoms |

**FROZEN science fields: 0 / 10.**  
§1 identifiability is owner-accepted. That is not a 10-field freeze.

**SOURCE_CONFLICT:** none new.

---

## 6. Outcome rows (B only)

| Row | Meaning |
|-----|---------|
| B-T1 | CONT-T1 ADEQUATE; no material PRIMARY utilization benefit after cost accounting |
| B-T2 | Material PRIMARY utilization benefit; still ≠ A / event sourcing / no-better-T1 / C |
| B-TIE-ADEQ | Both ADEQUATE; no material PRIMARY delta |
| B-TIE-FAIL | Both fail absolute bar — not T1-sufficiency |
| C-ONLY | SECONDARY_HISTORY delta only |
| INVALID | Any §3 gate failed |

---

## 7. Decision

```text
IDENTIFIABILITY_A          = NOT_TESTABLE
IDENTIFIABILITY_B          = OWNER_ACCEPTED
IDENTIFIABILITY_C          = SECONDARY_ONLY
FIELD_9_PAD                = WITHDRAWN
FROZEN_FIELDS              = 0 / 10
FINAL_PREREG_REVIEW        = NOT_READY
EXPERIMENT_AUTHORIZATION   = NOT_AUTHORIZED
```

Ready for **owner review of v2.1**: PILOT fixtures, withdrawn pad, still-MISSING Field 5.

Not ready for execution. Not ready for Evidence fixtures. Not a model freeze.

---

## 8. Stopping rule

Docs-only on `research/cont-e0t-prereg-v2`.  
Do not merge. Do not open a PR. Do not run CONT-E0T.  
Do not edit sealed Author / RedTeam / Integrity commits.  
Do not start FM-17 / CAP-E1 / ORNT-E1-CONFIRM from this file.
