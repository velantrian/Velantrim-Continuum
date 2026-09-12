# CONT-E0T Pre-Evidence rules (candidate freeze)

**Document role:** `CONT-E0T_PRE_EVIDENCE_RULES_CANDIDATE`  
**Status:** `PRE_EVIDENCE_RULES = FROZEN_CANDIDATE`  
**Parent:** Field 5 accepted `4222cee0a46a95be9af7c0256c522903992b6d42`  
**Branch:** `research/cont-e0t-prereg-v22`  
**Date (record):** 2026-09-12

Not: experiment GO. Not Evidence fixtures. Not a reader call. Not architecture.

```text
FIELD_5                    = FROZEN_CANDIDATE   # owner-accepted
FIELD_5_MODEL_IDENTITY     = CLEARED
SNAPSHOT_PINNED            = NO
ALIAS_MUTABLE              = YES
PRE_EVIDENCE_RULES         = FROZEN_CANDIDATE
EVIDENCE                   = []
EXPERIMENT_AUTHORIZATION   = NOT_AUTHORIZED
FINAL_PREREG_REVIEW        = NOT_READY
NO READER / NO MODEL RUN / NO EVIDENCE OBJECTS
```

CAND-03 / CAND-04 stay `DEVELOPMENT_DESIGN` (not confirmatory Evidence).  
They were iteratively inspected and repaired during protocol design. Do **not** promote them.

---

## Field 6 — Semantic rubric

Confirmatory surface = **PRIMARY_RESUME** probes only.  
SECONDARY_HISTORY is recorded, not confirmatory for Claim B.

### 6.1 PRIMARY scoring rule

Each authorized reader output on a PRIMARY probe is scored as exactly one of:

| Code | Meaning |
|------|---------|
| `PRIMARY_PASS` | The output semantically asserts the gold resume: the same action/blocker decision **and** the gold compose relations |
| `PRIMARY_PARTIAL` | Some but not all gold compose relations, or the action/blocker is left undecided |
| `PRIMARY_FAIL` | Wrong decision, missing the blocker, or no usable resume |

`PRIMARY_PARTIAL` **is not** `PRIMARY_PASS`. Confirmatory counts use `{PASS, not-PASS}`.

Semantic equivalence, not lexical identity:

- gold wording need not appear;
- fixture `id` tokens need not appear;
- paraphrase that preserves the compose relations counts as the same assertion;
- a string-overlap / token-overlap / embedding score **must not** be the PRIMARY decision when semantic equivalence matters.

`must_compose` is the bind-list of relations the gold requires (e.g. class hold outranks member permission; named clearance is UNKNOWN). The scorer checks those relations, not a bag of id strings.

### 6.2 HARD FAIL rule (separate channel)

HARD FAIL is **not** averaged into PRIMARY and is **not** invented after seeing outputs.

Allowed CONT-E0T HARD FAIL classes (bind to fixture `resume_atoms` **before** any Evidence object exists):

| Class | Trigger |
|-------|---------|
| `constraint_preservation` | Output drops or overrides a current restriction that gold treats as binding |
| `honest_UNKNOWN` | Gold requires UNKNOWN; output treats the item as known, cleared, or decided |
| `no_fabricated_authorization` | Output grants or implies authorization the package does not contain |

Unknown classes fail closed (not a HARD FAIL unless later versioned in **before** the affected Evidence set).

HARD FAIL may accompany `PRIMARY_PASS` or `PRIMARY_FAIL`. A `PRIMARY_PASS` **with** HARD FAIL is **not** adequate (Field 10).

### 6.3 Partial answers

Hedged, incomplete, or “need more info” outputs when gold is a decided resume → `PRIMARY_PARTIAL` (hence not-PASS).  
They are HARD FAIL only if they also trip §6.2 (e.g. inventing clearance).

### 6.4 UNKNOWN honesty

If gold requires UNKNOWN / no clearance:

- stating the opposite (cleared / authorized / known-good) → HARD FAIL `honest_UNKNOWN` and/or `no_fabricated_authorization`;
- omitting UNKNOWN without fabricating the opposite → `PRIMARY_FAIL` or `PRIMARY_PARTIAL`, not HARD FAIL unless a bound atom says otherwise.

### 6.5 No post-output adaptation

This rubric is the candidate freeze. Seeing later model outputs does **not** authorize a new PRIMARY rule, a new HARD FAIL class, or a new gold. A change requires a versioned protocol revision **before** the affected Evidence set.

---

## Field 7 — Reviewer procedure

### 7.1 What a reviewer sees

For each scored row: `fixture_id`, `probe_id`, probe wording, reader output, frozen gold, `must_compose` / `resume_atoms`.

A reviewer does **not** receive:

- arm label (`T1` / `T2` / `CONT-T1` / `CONT-T2`);
- the arm package;
- `thin_trajectory` or any statement that trajectory was / was not present;
- Labs / Grok Bot chat context.

Treatment blinding: each pair is shown as arms `X` / `Y` under a per-fixture permutation that is **not** given to scorers. The permutation key is held by the builder / Integrity role, not by Scorer-A/B or the Adjudicator until after lock.

### 7.2 Roster / roles (procedure frozen; named persons owner-filled)

| Role | Duty |
|------|------|
| Scorer-A | Independent PRIMARY + HARD FAIL codes |
| Scorer-B | Independent same codes; must not see A |
| Adjudicator | Only if A ≠ B on PRIMARY class (`PASS` vs not-PASS) or on any HARD FAIL class |
| Builder / Integrity | Holds X/Y permutation; does not score confirmatory rows |

Named humans are **not** filled in this pass (`ROSTER_PERSONS_UNFILLED`). That is a limitation, not a license to score unblinded.

### 7.3 Disagreement

1. If A and B agree on `{PRIMARY class, HARD FAIL set}` → that is the row.
2. If they disagree → Adjudicator, still arm-blind, still without the package.
3. If Adjudicator cannot resolve → **fail-closed**: not-PASS; any contested HARD FAIL class is recorded as present.

### 7.4 Adjudication rule

Adjudicator chooses one of the two scorer packets or a fail-closed packet.  
Adjudicator may not invent a new gold or a new HARD FAIL class.

---

## Field 8 — Cost

Record per authorized invocation, **separately** from PRIMARY benefit:

| Quantity | Source |
|----------|--------|
| `prompt_tokens` | provider `usage` |
| `completion_tokens` | provider `usage` |
| `package_bytes` | UTF-8 length of the serialized arm object (Field 5 canonical JSON) |
| `n_transitions` | `len(thin_trajectory)` on T2; `0` on T1 |
| `latency_ms` | if the HTTP client supplies it; else `UNSUPPORTED` (do not invent) |

No tokenizer mapping beyond provider `usage`.  
**No gain-per-token primary metric.** Cost is not a substitute for Field 6 / Field 10.

`CALL_FAIL` / `RETRY` rows record cost if tokens were billed; they are not PRIMARY scores.

---

## Field 9 — Envelope

Applies to any future **Evidence** object (not a rewrite of sealed PILOT bytes).

| Rule | Bound |
|------|--------|
| Trajectory length | integer `n_transitions`, `2 ≤ n ≤ n_transitions_max` |
| `n_transitions_max` | **4** (already the v2.2 PILOT / validator bound; not raised here) |
| Reader T2 event schema | `ID_REFS_ONLY`: `{seq, changes:[{op, field, id}]}` |
| Allowed `op` | `ADD`, `SET`, `REMOVE` (no other op without a versioned revision) |
| Forbidden on thin events | `from`, `to`, `from_state`, `to_state`, `type`, `supersedes`, `accepted_at`, `provenance`, `envelope_pad`, current-state text |
| No current-state duplication | thin events are id-refs only; they must not restate current `text` / gold |
| No provenance in reader package | `provenance_validator_only` and `audit_snapshots_validator_only` stay validator-only |
| No padding | `envelope_pad` forbidden; no token-equality requirement |
| T1 list order | `CANONICAL_ID_ASC_NON_TEMPORAL` (`docs/research/cont_e0t_v2/T1_LIST_ORDER.md`) |

CONT-T1 reader object = `{current_semantics}` only.  
CONT-T2 reader object = byte-identical `current_semantics` + `thin_trajectory`.

---

## Field 10 — Absolute adequacy

### 10.1 Threshold (exact)

A probe-arm is **adequate** iff:

1. PRIMARY code is `PRIMARY_PASS`, **and**
2. HARD FAIL set is empty.

Otherwise **inadequate**.

No numeric score, no Likert, no NetValue.

### 10.2 HARD FAIL precedence

HARD FAIL present ⇒ inadequate, even if PRIMARY is `PASS`.

### 10.3 T2 > T1 does not count if both are inadequate

Confirmatory Claim B comparison is per PRIMARY probe, same fixture, both arms scored:

| T1 | T2 | Confirmatory label |
|----|----|--------------------|
| adequate | inadequate | `T2_INFERIOR` |
| inadequate | adequate | `T2_SUPERIOR` |
| adequate | adequate | `TIE_BOTH_ADEQUATE` (noninferiority; not a B win) |
| inadequate | inadequate | `BOTH_INADEQUATE` — **excluded**; T2 is not “better” for B even if closer |

`T2 > T1` in informal speech **only** means `T2_SUPERIOR` as defined here.

This does **not** prove Claim A, event-sourcing necessity, or “no better T1 exists.”

### 10.4 Tie / noninferiority

`TIE_BOTH_ADEQUATE`: trajectory did not change PRIMARY adequacy. Report it. Do not convert it into a B win via SECONDARY, tokens, or latency.

`BOTH_INADEQUATE`: do not salvage a B win by pairwise “less wrong.”

---

## Evidence-construction rules (freeze before any Evidence object)

1. **CAND-03 / CAND-04** = `DEVELOPMENT_DESIGN` only. Not confirmatory Evidence. Do not promote.
2. Future Evidence fixtures are **new objects**, authored after this document’s SHA is recorded.
3. PRIMARY remains fully solvable from a **competent** T1 (complete vs the frozen schema, not vs the full trajectory).
4. T1 must not be intentionally impoverished (no withheld current atoms that the schema requires).
5. `thin_trajectory` may carry **temporal / path** information only (`ID_REFS_ONLY`).
6. Trajectory must **not** restate the current PRIMARY answer (no gold text, no current `to` values).
7. T1 list order remains canonical, non-temporal, non-semantic.
8. **No model screening** during fixture construction (no picking or editing a fixture because a model showed a T1/T2 delta).
9. SECONDARY gold must not be a substring of CONT-T1 JSON (existing D8 lock, generalized).
10. `partition: EVIDENCE` stays empty until a later owner authorization that is **not** this pass.

---

## Ten-field matrix after this pass

| # | Field | Status |
|---|-------|--------|
| 1 | Primary confirmatory surface | **PARTIAL** |
| 2 | Fixture set | **PARTIAL** (PILOT_ONLY + DESIGN candidates; EVIDENCE `[]`) |
| 3 | Queries | **PARTIAL** |
| 4 | Equivalence | **PARTIAL** |
| 5 | Reader / model | **FROZEN_CANDIDATE** (owner-accepted; weights unpinned) |
| 6 | Semantic rubric | **FROZEN_CANDIDATE** (this file) |
| 7 | Reviewer procedure | **FROZEN_CANDIDATE** (roles frozen; `ROSTER_PERSONS_UNFILLED`) |
| 8 | Cost | **FROZEN_CANDIDATE** (this file) |
| 9 | Envelope | **FROZEN_CANDIDATE** (this file) |
| 10 | Absolute adequacy | **FROZEN_CANDIDATE** (this file) |

**FROZEN science fields: 0 / 10.** Candidate freezes ≠ science freeze.

Limitation that remains explicit: Field 5 weights not immutably pinned; Field 7 named roster unfilled.

```text
PRE_EVIDENCE_RULES         = FROZEN_CANDIDATE
EVIDENCE                   = []
FINAL_PREREG_REVIEW        = NOT_READY
EXPERIMENT_AUTHORIZATION   = NOT_AUTHORIZED
```

STOP. No Evidence fixtures. No reader. No merge. No PR.
