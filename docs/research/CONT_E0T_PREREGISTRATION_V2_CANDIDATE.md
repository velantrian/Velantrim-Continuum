# CONT-E0T Preregistration V2.2 Candidate

**Document role:** `CONT-E0T_PREREGISTRATION_V2_CANDIDATE`  
**Revision:** v2.2 (bounded correction after owner-accepted v2.1 reconciliation)  
**Parent candidate:** `163ab9a27e90eb08bc3d8d2349e1f171cb8c54cf`  
**Reconciliation accepted:** `16ee0a874299b124d7f2e399f61ccd54b7178620`  
**BASELINE SHA:** `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`  
**Repository:** `velantrian/Velantrim-Continuum`  
**Branch:** `research/cont-e0t-prereg-v22`  
**Status:** **CANDIDATE for owner review** — not a freeze, not Pilot execution, not Evidence, not architecture

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
FINAL_PREREG_REVIEW      = NOT_READY
NO READER / NO MODEL RUN / NO PAID RUN / NO MERGE / NO PR
```

Kept from owner review: Claim B; D2 PRIMARY←T1; D6 structural PASS only; D7 PILOT ≠ Evidence; D9 no `envelope_pad`; Integrity process PASS.

---

## 0. Correction resolutions

### F6.5 — distinct SET-from-final check (implemented, not weakened)

`semantic_atoms(state)` = nonempty scalar texts + list items `(field, id, text, status)`.

**F6.3** (unchanged, still required): some `audit_snapshots_validator_only[].from_state` is not canonical-JSON-equal to final `current_semantics`.

**F6.5** (new, distinct): some audit `from_state` has `semantic_atoms(from_state) ⊈ semantic_atoms(current)`.

That is the claimed property: the intermediate snapshot is **not** a field-wise SET / subset of the final snapshot.

A `from_state` that is `!= current` but whose atoms are all on the final snapshot (empty lists, dropped current items, empty start) **fails F6.5** and **passes F6.3**. The validator ships an internal self-check of that pair.

Validator stdout is `PACKAGE_STRUCTURAL_PASS`, not `PASS`. Still not science.

### D3 — thin trajectory (no snapshot replay, no T1 pad)

Reader CONT-T2 receives `current_semantics` + `thin_trajectory[]`.

Each event is `{seq, changes:[{field, id, from, to}]}` only.

Forbidden on `thin_trajectory`: `from_state`, `to_state`, `type`, `supersedes`, `accepted_at`, `provenance`, `envelope_pad`.

Full snapshots live only in `audit_snapshots_validator_only` (not a reader treatment).

No CONT-T1 padding. Token equality still not required. Field 9 stays PARTIAL. Residual T2 size is the **path deltas**, not three recopied states.

Measured reader JSON bytes (no pad): FX-01 T1 1166 / T2 3284; FX-02 T1 1185 / T2 3434. Previous v2.1 full-snapshot T2 was ~5.4× / ~4.7×.

### D4 — provenance is not a Claim B treatment

`provenance_validator_only` = `{seq, type, accepted_at, supersedes}` per event.

Claim B reader packages:

| Arm | Delivered |
|-----|-----------|
| CONT-T1 | `current_semantics` only |
| CONT-T2 | same `current_semantics` + `thin_trajectory` |

Neither arm receives provenance. Trajectory path and provenance commentary are not fused in the reader comparison.

### D8 — FX01-S1

CONT-T1 `r-friday.text` is now `Friday production deploy` (no clock).

S1 gold remains `Friday 16:00`, which lives on the trajectory/audit path only.

Validator fail-closes if any SECONDARY gold (normalized) is a substring of CONT-T1 JSON.

### PILOT_ONLY

FX-01 / FX-02 stay `partition: PILOT` and `claim_b_role: PILOT_SHAKEDOWN_NOT_DISCRIMINATOR`.  
EVIDENCE remains `[]`. Not promoted.

---

## 1. Identifiability (unchanged)

A = NOT_TESTABLE. B = owner-accepted working claim. C = SECONDARY_HISTORY only.

---

## 2. PILOT package (shakedown only)

| Fixture | file SHA-256 | role |
|---------|--------------|------|
| CONT-E0T-FX-01 | `e552d5a883d9c8a433254a6379e84ef9bdd78ed3a7fe40ea882e251215802ce9` | PILOT_ONLY |
| CONT-E0T-FX-02 | `e993f2dfa1d1bdc9a5af800dc2c6dfbb119684b8c26563af7e9e137bf82984b8` | PILOT_ONLY |

Prompt SHA-256: `5d3e946be3c0830a37575c59aa24636b2952a83384cb8ce813e604bb2362a067`  
Validator: `python3 docs/research/cont_e0t_v2/validate_cont_e0t_v2_package.py` → `PACKAGE_STRUCTURAL_PASS` at write time.

---

## 3. Proposed Claim B discriminator candidates (not Evidence)

`docs/research/cont_e0t_v2/candidates/` — **not** in the PILOT manifest, **not** Evidence.

| ID | Sketch | Why not PILOT ceiling |
|----|--------|------------------------|
| `CONT-E0T-FX-B-CAND-01` | Eight current constraints; HOLD-12 forbids all outbound email; `c-draft-mail` still present | `process_position` does not restate the gold. PRIMARY still T1-solvable (`c-hold-mail` + UNKNOWN). Thin last change only adds the hold. |
| `CONT-E0T-FX-B-CAND-02` | Three similar UNKNOWN identifiers on V-19 | `process_position` does not say UNKNOWN. PRIMARY asks DUNS / forbids API write. Gold on T1. |

Do **not** construct an Evidence partition from these until another bounded review of the corrected protocol.

---

## 4. Ten-field matrix (v2.2)

| # | Field | Status | Bound now | Open |
|---|-------|--------|-----------|------|
| 1 | Primary confirmatory surface | **FROZEN_CANDIDATE** | Unit=PRIMARY pair; B rule S≥3 ∧ I=0 | See `CONT_E0T_FIELDS_1_4_RUN_INTEGRITY.md` |
| 2 | Fixture set | **FROZEN_CANDIDATE** | Design N=4, 2 families; EVIDENCE objects empty | Authoring not started |
| 3 | Queries | **FROZEN_CANDIDATE** | 1 PRIMARY; compose ≥4; no gold leak | |
| 4 | Equivalence | **FROZEN_CANDIDATE** | E4.1–E4.10 executable checks | |
| 5 | Reader / model | **FROZEN_CANDIDATE** | `deepseek-flash` = DeepSeek-V4.1-Flash; identity cleared; wrapper pins unchanged | Weights not immutably pinned; alias mutable |
| 6 | Rubric | **FROZEN_CANDIDATE** | PRIMARY PASS/PARTIAL/FAIL; HARD FAIL separate; no lexical-only | See `CONT_E0T_PRE_EVIDENCE_RULES.md` |
| 7 | Reviewers | **FROZEN_CANDIDATE** | Arm-blind X/Y; A/B + adjudicator; fail-closed | `ROSTER_PERSONS_UNFILLED` |
| 8 | Cost | **FROZEN_CANDIDATE** | usage tokens, bytes, n_transitions, latency optional | No gain-per-token |
| 9 | Envelope | **FROZEN_CANDIDATE** | n∈[2,4]; ID_REFS_ONLY; no pad/provenance; id-sort T1 | |
| 10 | Absolute adequacy | **FROZEN_CANDIDATE** | PASS ∧ no HF; both-inadequate excluded | Tie = both adequate |

**FROZEN science fields: 0 / 10.**

---

## 5. Decision

```text
F6.5                     = DISTINCT_CHECK (atoms ⊈ final)
D3                       = THIN_TRAJECTORY (no snapshot replay, no pad)
D4                       = PROVENANCE_VALIDATOR_ONLY
D8                       = FX01-S1 clock not on T1
FX-01/FX-02              = PILOT_ONLY
EVIDENCE                 = []
FROZEN_FIELDS            = 0 / 10
FIELD_5                  = FROZEN_CANDIDATE
FIELD_5_MODEL_IDENTITY   = CLEARED
SNAPSHOT_PINNED          = NO
READY_TO_AUTHOR_EVIDENCE = YES
FINAL_PREREG_REVIEW      = NOT_READY
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
```

STOP for owner review. No reader. No Evidence promotion. No merge. No PR.
