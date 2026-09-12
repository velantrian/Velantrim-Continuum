# CONT-E0T v22 CAND-03 S1 repair RedTeam

**Reviewed commit:** `d2d9cf5d342a9f5f594cf652ad23eab50af48e73`  
**Worktree:** `/workspace/cont-e0t/v22-cand-rt-s1`  
**Branch:** `research/cont-e0t-v22-cand-redteam-s1`  
**Scope:** repaired CAND-03 S1 only. Not a new conceptual round.  
**Not done:** candidate-JSON edits; model; Evidence; PR.

Checks performed:

- CAND-04 file SHA-256 `a83e22c0377f491fad465a9a2993979560a4c6060e95c085b20d7a2b4340cb9e` — **match** (7182 bytes).
- C3-P1 object vs `f3d7fb9038377e5070b9554a8942f5ae43e5a46d` — **byte-identical**.
- CAND-03 `current_semantics` / `thin_trajectory` **did** change (HOLD-pine + reorder). Noted; S1 is the attack target.

New S1: “Which hold ids were already current when `c-hold-ash` became current?”  
Gold: `c-hold-elm, c-hold-oak.`  
Pine added in the same seq2 step as ash, so “all holds except ash” is not the gold.

---

## Gate

```text
READY_FOR_FIELD_5 = NOT_READY_FOR_FIELD_5
```

S1 gold is still recoverable from T1 list position. The unique-semantic and “all-but-ash” holes are closed. List-order is not.

---

## Index

| ID | Issue | Severity |
|----|-------|----------|
| S1 | CAND-04 byte-identical to required SHA | PASS |
| S2 | C3-P1 unchanged vs f3d7fb9; still T1-sufficient 6-way compose | PASS |
| S3 | S1 gold = {elm, oak} ≠ all-holds-except-ash (pine same step) | PASS |
| S4 | S1 gold ≠ unique outbound / email-binding hold (that is ash) | PASS |
| S5 | S1 not in rationale / process_position / rejected / one current row | PASS |
| S6 | After-ash suffix on unresolved + unknown is exactly {elm, oak} | **BLOCKING** |
| S7 | After-ash suffix on constraint-holds is {oak, elm} = gold set | **BLOCKING** |
| S8 | IDs / rationale / rejected do not encode the before-set | PASS |
| S9 | T1/trajectory also changed (pine); not probe-only | MINOR |
| S10 | Score S1 as a set, not a string order | MINOR |

---

## PRIMARY (required confirm) — PASS

C3-P1 wording, gold, `must_compose`, `resume_atoms`, `primary_solvable_from_T1` match f3d7fb9 exactly.

Still on T1: `d-pack`, `c-ops-list`, `c-email-outbound`, `c-hold-ash`, `c-prec`, `u-ash`, `c-mail-ok`. Pine (SMS) is a distractor, not a missing PRIMARY fact. Composition still required. Information-sufficient from T1. Claim B PRIMARY shape intact.

`composition_keys_for_primary` unchanged.

---

## S1 attacks

### Unique semantic matching — PASS (S3, S4)

Four current holds:

| id | text | seq |
|----|------|-----|
| c-hold-elm | Slack | 1 |
| c-hold-oak | public blog | 1 |
| c-hold-ash | all outbound | 2 |
| c-hold-pine | SMS | 2 |

“All holds except ash” = {elm, oak, pine} ≠ gold. Pine blocks that heuristic.  
“The unique hold that binds email / outbound” = ash ≠ gold. The old bar-8 leak is closed.  
No T1 sentence says elm+oak were earlier than ash. Channel meanings (Slack / blog / SMS / outbound) do not entail a before-set.

### Rationale / process_position / rejected / current flags — PASS (S5, S8)

- `current_rationale`: keep facts separate; do not invent clearance. No order.
- `process_position`: section 3/5; no channel action. No hold names.
- Rejected: `r-ext-tool`, `r-sms`. SMS touches pine, not “elm and oak were already current.”
- All four holds `current: true`. No timestamps. IDs do not encode time (alpha: ash, elm, oak, pine — gold is not “ids before ash”).

### List position / ordering artifacts — BLOCKING (S6, S7)

Hold order on T1:

| Array | Order | After `ash` |
|-------|-------|-------------|
| `constraints` holds | pine, **ash**, oak, elm | **oak, elm** |
| `unresolved_items` | pine, **ash**, elm, oak | **elm, oak** |
| `unknown_operations` | pine, **ash**, elm, oak | **elm, oak** |

`why_not_on_T1` says list order is “pine, ash, oak, elm — not the gold set.”  
Set-wise, **holds after ash = {elm, oak} = gold**.  
On unresolved and unknown, the suffix is **elm, oak in gold’s written order**.

Heuristic “ids after `c-hold-ash` / `u-ash` / `op-ash`” recovers S1 from T1 with no trajectory. Position is evidence. Same bar that blocked the previous CAND-03 S1.

Thin path still *has* the true answer (seq1: elm, oak; seq2: ash+pine). That is the intended T2 channel. It does not excuse a T1 list-suffix leak.

---

## CAND-04 — PASS

File bytes hash-equal to `a83e22c0…4340cb9e`. Not re-opened.

---

## Recommended Labs action

1. **Do not** start Field 5 / model run.
2. Rebuild CAND-03 arrays so the gold before-set is **not** any suffix/prefix/middle slice around `ash` on constraints, unresolved, **or** unknown. Example direction: interleave pine/ash/elm/oak so after-ash ≠ {elm, oak} and before-ash ≠ {elm, oak}.
3. Re-check set-equality, not only the printed “elm, oak” order (S10).
4. Keep C3-P1 frozen vs f3d7fb9; keep CAND-04 untouched.

```text
NOT_READY_FOR_FIELD_5
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
CANDIDATE ≠ PILOT ≠ EVIDENCE
```

STOP. Docs-only. No experiment. No merge. No architecture.
