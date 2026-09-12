# CONT-E0T Preregistration V2 Candidate

**Document role:** `CONT-E0T_PREREGISTRATION_V2_CANDIDATE`  
**BASELINE SHA:** `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`  
**Repository:** `velantrian/Velantrim-Continuum`  
**Branch:** `research/cont-e0t-prereg-v2`  
**Status:** **CANDIDATE for owner review** — not evidence-locked, not Pilot, not Evidence, not architecture  
**Protocol family:** `CONT-E0T` (successor; **≠** historical `E0-T`)

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
FINAL_PREREG_REVIEW = NOT_READY
NO EXPERIMENT / NO MERGE / NO PR / NO PAID RUN
```

Sealed v1 inputs (do not rewrite):

| Role | Artifact | Commit |
|------|----------|--------|
| CONT-AUTHOR | `docs/research/CONT_E0T_PREREGISTRATION_CANDIDATE.md` | `4a026c1ef7844cc95873d6155b311c2853346fe8` |
| CONT-REDTEAM | `docs/research/CONT_E0T_BLIND_REDTEAM_REVIEW.md` | `1069ee39c8ad53251964ebd00c6ee3dfbdf21bac` |
| CONT-INTEGRITY | `docs/research/CONT_E0T_INTEGRITY_REPORT.md` | `35d935e78fd87a584a73fd520d09f9b2465d8ad0` |
| Labs reconcile | `docs/research/CONT_E0T_PREREG_RECONCILIATION.md` | first `6cfe219d5410e67f17878a60225e421f52f2331a`; Integrity addendum `93942a86432a4b9c2c14a1fd90e90e1104933cb0` |

Owner review accepted: `FINAL_PREREG_REVIEW = NOT_READY`, Integrity PASS as **process only**. This file is the one authorized v2 freeze pass. It does not edit those commits.

---

## 0. Authority and non-claims

- Not a rewrite of `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` or E0-T `T0`–`T4`.
- Not experiment execution, merge, PR, paid model run, or architecture promotion.
- Not a claim that event sourcing / ledgers are required IDPS architecture.
- Bare `T1` / `T2` forbidden in CONT-E0T fields where E0-T collision exists. Arms are `CONT-T1` / `CONT-T2`.
- Numeric gates (100%/0%/0%, 95%, token-overlap) are **not invented** and **not imported**.
- `Graphiti_fractal_lab` remains pointer-only.

Classification legend: **FROZEN** | **PARTIAL** | **MISSING** | **SOURCE_CONFLICT**.

---

## 1. IDENTIFIABILITY DECISION

This section is written **before any fixture construction**. It is the point of v2. Filling ten fields without this section would repeat v1.

### 1.1 Three claims that must not be conflated

| ID | Claim | Plain meaning |
|----|-------|----------------|
| **A** | Semantic necessity of trajectory for resume | Correct bounded resume is impossible unless the successor sees the accepted trajectory, even given a competent current-state package. (“Independent continuity value.”) |
| **B** | Practical utilization / representation benefit | For a **fallible replaceable LLM**, under a **preregistered bounded** CONT-T1, adding a bounded genuine accepted trajectory improves **practical** PRIMARY resume performance. |
| **C** | History / audit value | Trajectory helps answer THEN / superseded / change-set / as-of / audit probes. |

A, B, and C are different questions. A v2 win, loss, or tie on one is not a result on the others.

### 1.2 Critical question (tautology)

> If CONT-T1 is defined as containing **all information necessary for correct resume**, does “independent history value for resume” become unfalsifiable or tautologically excluded?

**Answer: YES — tautologically excluded, not merely hard.**

- If CONT-T1 already holds every fact PRIMARY resume needs, then a PRIMARY probe whose gold is determined by currently-true facts is solvable from CONT-T1. Trajectory cannot be *semantically necessary* for that probe.
- If a PRIMARY probe is *not* solvable from that CONT-T1, then either CONT-T1 omitted a currently-true resume fact (F3 impoverishment) or the probe is historical (F7 / claim C). Neither is claim A.
- Therefore claim A cannot be isolated by any PRIMARY_RESUME probe that is allowed to exist under F3 + F7.

RedTeam F1 is accepted: there is no probe class that is simultaneously (i) bounded resume, (ii) not recoverable from competent current state, (iii) not a THEN/supersession quiz, (iv) not a reconstructive-manifest (historical E0-T `T3`) task.

**STOP for claim A.** CONT-E0T **cannot validly test independent continuity value** (semantic necessity of trajectory for resume) in the present form. Hiding this and “filling fields” would be a protocol failure.

This STOP does **not** by itself kill a narrower empirical claim. It kills A.

### 1.3 What remains identifiable (working claim — owner must accept)

Owner-supplied candidate interpretation, **evaluated and adopted as the v2 working claim**, not treated as architecture:

```text
CONT-T1  = a preregistered, bounded, realistically maintainable
           current-state representation
           (complete vs CURRENT_SEMANTICS schema;
            incomplete vs full accepted trajectory)

CONT-T2  = the exact same current-state representation
         + a bounded genuine accepted trajectory
```

This **redefines** CONT-T1 away from “all information necessary for correct resume” and toward “this frozen schema, competently filled.” Relative to trajectory it is incomplete by design. Relative to F3 it is **not** allowed to be impoverished: it must carry every currently-true CURRENT_SEMANTICS field.

| Claim | Testable in v2? | How |
|-------|-----------------|-----|
| **A** | **NO** | Tautology + F1. Do not run, score, or narrate as A. |
| **B** | **YES, if owner accepts this section** | PRIMARY gold is information-sufficient from CONT-T1. CONT-T2 adds authentic trajectory under envelope. A PRIMARY delta is then utilization/representation for the frozen reader, not semantic necessity. |
| **C** | **YES, secondary only** | SECONDARY_HISTORY table. Must not enter PRIMARY ResumeAdequacy. |

**v2 tests B. It does not test A. C is diagnostic.**

### 1.4 Decision table

#### 1. CLAIM THAT IS TESTABLE

Does adding a bounded genuine accepted trajectory improve **practical PRIMARY resume** of a specified fallible reader beyond this **same** bounded CONT-T1, after equivalence, authenticity, envelope, prompt symmetry, and absolute HARD FAIL?

#### 2. CLAIM THAT IS NOT TESTABLE

That trajectory is **semantically necessary** for correct resume given a complete-for-resume current state. That history has **independent continuity value**. That event sourcing is required. That no better CONT-T1 compression exists.

#### 3. WHAT A T1 WIN WOULD MEAN

On these frozen fixtures, this frozen reader, this frozen CONT-T1 schema: CONT-T1 was **adequate** for PRIMARY resume and CONT-T2 did not add material PRIMARY utilization benefit that survives cost accounting.

It does **not** mean: history is universally unnecessary; claim A is false; a better CONT-T1 is impossible; audit/history (C) is worthless.

#### 4. WHAT A T2 WIN WOULD MEAN

On these frozen fixtures, this frozen reader, this frozen schema: trajectory improved **practical** PRIMARY resume beyond this bounded CONT-T1 (claim B).

```text
T2 > T1  ≠  universal necessity of history          (not A)
T2 > T1  ≠  event-sourcing necessity
T2 > T1  ≠  proof that no better T1 compression exists
T2 > T1  ≠  history/audit value                     (that is C)
```

#### 5. WHAT A TIE WOULD MEAN

No detectable PRIMARY utilization benefit of trajectory for this reader on these fixtures. CONT-T1 adequacy is then decided only by the **absolute** bar (Field 10), not by the tie itself. A tie of two failing arms is not adequacy.

#### 6. WHAT WOULD BE INCONCLUSIVE

Any of: failed F5 equivalence; failed F6 authenticity; F3/F4 package invalid; PRIMARY contaminated by SECONDARY_HISTORY (F7); `ENVELOPE_EXCEEDED` or unmatched budget (F11); prompt asymmetry; arm-unblind semantic scoring; post-hoc fixture/query edits; numeric thresholds invented after outputs.

### 1.5 F1 status after this section

| Target | Status |
|--------|--------|
| F1 vs claim A | **NOT RESOLVABLE** without making CONT-T1 intentionally incomplete *and* scoring that incompleteness as “continuity value.” Forbidden. |
| F1 vs claim B | **RESOLVED in protocol** by forcing PRIMARY information-sufficiency on CONT-T1, pairing the same current object, and attributing leftover PRIMARY delta only to utilization under envelope. |
| F1 vs claim C | **RESOLVED in protocol** by a fail-closed probe map (Field 1 / Field 3). |

If the owner rejects the bounded-T1 working claim, there is **no** identifiable PRIMARY experiment left. STOP there; do not construct fixtures.

---

## 2. Working arm definitions (v2)

| ID | Package |
|----|---------|
| `CONT-T1` | `current_semantics` only, filled against `CURRENT_SEMANTICS_FIELDS` |
| `CONT-T2` | **byte-identical** `current_semantics` **plus** `accepted_trajectory[]` + `provenance` inside the Field 9 envelope |

Successor on both arms receives the arm package plus the **same** frozen reader instructions. CONT-T1 must **not** be told that it “lacks history.”

---

## 3. Blocker closures (protocol, not architecture)

### 3.1 F1 — Identifiability — **closed for B; refused for A**

See §1. Fail-closed probe map is Field 1. No PRIMARY_RESUME probe may require a fact that CONT-T1 is forbidden to hold.

### 3.2 F3 — Impoverished CONT-T1 — **operational exclusion**

CONT-T1 **must** include every currently-true value of `CURRENT_SEMANTICS_FIELDS` that the fixture gold marks `current=true`.

CONT-T1 **may omit only** `TRAJECTORY_ONLY_FIELDS`.

A package that drops a currently-true CURRENT_SEMANTICS field is `INVALID_ARM / IMPOVERISHED_T1`. Scores from that pair are not confirmatory.

### 3.3 F4 — Disguised-T2 CONT-T1 — **operational exclusion**

CONT-T1 **must not** contain: `accepted_trajectory[]`, ordered `S0→S1→…`, superseded snapshots that are not currently true, change-sets, transition acceptance metadata, or from_state objects.

It **may** hold currently-true accepted decision D and currently-true rejected alternative R (those are current semantics).

Violation → `INVALID_ARM / DISGUISED_T2`.

### 3.4 F5 — Equivalence gate — **operational procedure**

Before any PRIMARY comparison:

1. Take `CONT-T1.current_semantics`.
2. Project `CONT-T2.accepted_trajectory` in frozen order → `projected_current`.
3. Also require `CONT-T2.current_semantics` **byte-identical** (canonical JSON) to `CONT-T1.current_semantics`.
4. Require `projected_current` canonical-JSON-equal to that same object on `CURRENT_SEMANTICS_FIELDS`.
5. Mismatch → `INVALID_ARM / EQUIVALENCE_FAIL`. Do not score PRIMARY as a trajectory effect.
6. On pass, still **deliver the full CONT-T2 package** (current + trajectory) to the CONT-T2 successor — never the projection alone (that was the historical E0-T T2 isolation failure).

Non-byte-identical “semantic equivalence” of current packages is **not selected**. v2 requires a shared canonical current object.

### 3.5 F6 — Genuine trajectory authenticity — **predicate**

A CONT-T2 trajectory is `AUTHENTIC` only if **all** hold:

1. Transitions are **experimenter-authored** and frozen with the fixture, not model-emitted (CAP-E1 remains HOLD).
2. Length ≥ 2 accepted transitions.
3. At least one intermediate `from_state` **≠** final `current_semantics`.
4. At least one genuine supersession (a previously accepted item is not currently true).
5. At least one accepted transition whose `from_state` cannot be reconstructed from the final snapshot alone by field-wise `SET`.
6. Folding the trajectory in order yields `current_semantics`.
7. The event list is **not** equal to `{SET field := current[field] for field in current}` (historical E0-T `prepare_transfer.py` construction). That construction is `FAKE_SET_FROM_FINAL_STATE` → `INVALID_ARM`.

If the predicate fails, CONT-T2 cannot receive trajectory credit. PRIMARY scores are inconclusive for B.

### 3.6 F7 — Historical-query leakage — **fail-closed map**

Every probe has exactly one tag:

`PRIMARY_RESUME` | `SECONDARY_HISTORY` | `DIAGNOSTIC`

| Tag | Allowed gold | Enters primary statistic? |
|-----|----------------|---------------------------|
| `PRIMARY_RESUME` | Currently-true constraint / blocker / valid resume point / next allowed action / honest UNKNOWN / no fabricated authorization | **Yes** |
| `SECONDARY_HISTORY` | Superseded state, from_state, change-set, as_of, “what happened earlier” | **No** |
| `DIAGNOSTIC` | Anything else pre-bound | **No** |

A probe whose gold is a superseded state, a from_state, or a change-set **cannot** be tagged PRIMARY_RESUME. If later re-tagged, the run is invalid.

WHY: if the rationale still **governs** the current process, it belongs on CONT-T1 (current rationale) and may be PRIMARY only as a current-constraint probe. If it is only about a past change, it is SECONDARY_HISTORY. This also blocks F10 T3-smuggling into PRIMARY.

### 3.7 F11 — Ledger envelope — **matched budget + per-fixture bound**

No global token multiplier is invented.

**Selected rule (v2):** **matched delivered budget.**

1. Serialize CONT-T2 as delivered to the reader. Measure `bytes_T2` and `tokens_T2` with the frozen tokenizer (tokenizer itself is Field 5, still MISSING).
2. CONT-T1 is the same `current_semantics` plus an inert `envelope_pad` object with **no** process semantics (fixed filler; not hints; not inverted trajectory).
3. Pad CONT-T1 until `tokens_T1_delivered == tokens_T2_delivered` (and bytes within the same tokenizer accounting). If padding cannot match without exceeding the frozen context reserve → `ENVELOPE_EXCEEDED`, pair invalid.
4. Each fixture declares `n_transitions` and `n_transitions_max`. If `len(accepted_trajectory) > n_transitions_max` → `ENVELOPE_EXCEEDED`.
5. Overflow is a protocol invalid, not a silent extra-context win.

Until Field 5 names the tokenizer, this rule is **FROZEN as procedure** and **PARTIAL as executable**.

### 3.8 F14 — Absolute adequacy — **arm-independent HARD FAIL**

```text
CONT-T1 ≡ CONT-T2 (current fields)  ≠  either arm is adequate
relative non-inferiority            ≠  CONT-T1 sufficient
```

HARD FAIL (pre-bound, not averaged, not compensated by the other arm):

| Atom | Fail if |
|------|---------|
| `HF_FABRICATED_AUTH` | Successor asserts authorization / permission the package does not grant |
| `HF_CONSTRAINT` | Successor violates a currently-true constraint in `current_semantics` |
| `HF_LOST_UNKNOWN` | Package marks UNKNOWN and successor treats it as known |
| `HF_INVALID_RESUME_POINT` | Successor continues a superseded goal / closed task as current |
| `HF_SIBLING_LEAK` | Output uses the other arm’s package or evaluator metadata |

An arm is **ADEQUATE** on a fixture only if: no HARD FAIL **and** every PRIMARY_RESUME probe meets its pre-bound ResumeAdequacy atoms.

A T1 win still means only: **this bounded T1 was adequate on these frozen fixtures for this reader.**

---

## 4. CURRENT_SEMANTICS vs TRAJECTORY_ONLY

**Status: FROZEN as field *names* for v2; schema JSON / hashes MISSING (no fixtures).**

`CURRENT_SEMANTICS_FIELDS` (must live on CONT-T1 when `current=true`):

- `active_goal`
- `task_position`
- `constraints[]` (currently in force)
- `accepted_decisions[]` (currently in force)
- `rejected_alternatives[]` (currently rejected)
- `unresolved_items[]`
- `contested_claims[]`
- `current_rationale` (governs now; not a past-change essay)
- `unknown_operations[]`
- `artifact_refs[]`
- `process_position`

`TRAJECTORY_ONLY_FIELDS` (CONT-T2 only; CONT-T1 forbidden):

- `accepted_trajectory[]` (`from_state`, `to_state`, `type`, `seq`, `accepted_at`, `supersedes`)
- superseded snapshots that are not currently true
- change-sets / as_of slices
- transition-only acceptance metadata
- ordered path whose intermediate nodes are not current

---

## 5. Ten-field v2 matrix

No fixtures are constructed in this pass.

| # | Field | v2 status | What v2 binds | What remains |
|---|-------|-----------|---------------|--------------|
| 1 | Primary confirmatory surface | **PARTIAL** | PRIMARY = resume-now only; probe tags; information-sufficiency rule; claim = B not A | Exact probe templates / action space per fixture |
| 2 | Frozen fixture set | **MISSING** | **Admission criteria only** (below). No IDs, no content, no hashes | Construction is a later owner-authorized pass |
| 3 | Queries per fixture | **PARTIAL** | Tag law (F7); PRIMARY cannot require T1-forbidden facts | Wording, gold, count |
| 4 | Equivalence check | **PARTIAL** | Procedure §3.4; canonical JSON; deliver trajectory on CONT-T2 | Executable evaluator + schema hash |
| 5 | Reader / model freeze | **MISSING** | Discipline: one reader; prompt symmetry; single-model ⇒ non-generalizing | Provider, model id, temp/seed, tokenizer, prompt hashes |
| 6 | Semantic rubric | **PARTIAL** | Separate ResumeAdequacy / history / cost tables; no NetValue invented; no token-overlap | Match spec / precedence table |
| 7 | Reviewer procedure | **PARTIAL** | Arm-blind scoring of **outputs**; LLM judge not primary for deterministic/HARD FAIL fields | Roster, IAA rule |
| 8 | Complexity / cost | **PARTIAL** | Report injection / storage / generation / verification / runtime separately; no invented NetValue | Run-manifest hooks |
| 9 | Ledger envelope | **PARTIAL** | Matched-budget + per-fixture `n_transitions_max`; overflow fail-closed | Tokenizer (Field 5); concrete `n` per fixture |
| 10 | Absolute adequacy | **PARTIAL** | HARD FAIL atoms §3.8; equivalence ≠ adequacy | Per-fixture ResumeAdequacy checklists |

**FROZEN science fields: 0 / 10.**  
Identifiability *decision* is FROZEN. That is not a field freeze.

**SOURCE_CONFLICT:** none new. Residual hygiene (lab pointer still uses bare T1/T2; Continuum `research_sequence` still lists historical E0-T) is unchanged and out of this pass.

### 5.1 Fixture admission criteria (not fixtures)

A future fixture is admissible only if it declares, before content lock:

1. `current_semantics` filled for every CURRENT_SEMANTICS field that is current.
2. `accepted_trajectory` that passes the F6 predicate (so fake SET-from-final-state is impossible).
3. At least one PRIMARY_RESUME probe whose gold is determined by `current_semantics` alone.
4. At least one SECONDARY_HISTORY probe (so C can be measured without contaminating B).
5. Explicit `primary_solvable_from_T1: true` on every PRIMARY probe.
6. `n_transitions` and `n_transitions_max`.
7. Content **not** copied as-is from historical E0-T transfer scenarios (those have no genuine CONT-T2 trajectory).
8. PILOT vs EVIDENCE partition named before evidence.

Do **not** build those fixtures in this commit.

---

## 6. Outcome rows (B only)

Map PRIMARY results **after** validity gates. Do not invent a weighted continuity score.

| Row | Meaning (claim B) |
|-----|-------------------|
| B-T1 | CONT-T1 ADEQUATE; CONT-T2 adds no material PRIMARY utilization benefit after cost |
| B-T2 | CONT-T2 material PRIMARY utilization benefit; still ≠ A, ≠ event sourcing, ≠ no-better-T1 |
| B-TIE-ADEQ | Both ADEQUATE, no material PRIMARY delta |
| B-TIE-FAIL | Both fail absolute bar — **not** a T1-sufficiency result |
| C-ONLY | SECONDARY_HISTORY delta only → claim C, not B |
| INVALID | Any §3 gate failed → inconclusive |

Historical program Cases A–D must not be used as aliases for claim A.

---

## 7. Decision

```text
IDENTIFIABILITY_A          = NOT_TESTABLE
IDENTIFIABILITY_B          = PROTOCOL_RESOLVED (pending owner accept)
IDENTIFIABILITY_C          = SECONDARY_ONLY
FROZEN_FIELDS              = 0 / 10
FINAL_PREREG_REVIEW        = NOT_READY
EXPERIMENT_AUTHORIZATION   = NOT_AUTHORIZED
```

Ready for **owner review of this v2 candidate**, especially §1 (do you accept B as the surviving claim?).

Not ready for fixture construction until that accept.  
Not ready for execution in any case from this file.

### Owner choices (not execution GO)

1. Accept §1: v2 tests **B** only; A is refused. Then a later pass may construct fixtures under §5.1.
2. Reject bounded-T1: **no** identifiable PRIMARY experiment; CONT-E0T stops as a continuity-value test.
3. Defer / stop the track.

---

## 8. Stopping rule

This commit is docs-only on `research/cont-e0t-prereg-v2`.  
Do not merge. Do not open a PR. Do not run CONT-E0T.  
Do not edit sealed Author / RedTeam / Integrity commits.  
Do not start FM-17 / CAP-E1 / ORNT-E1-CONFIRM from this file.
