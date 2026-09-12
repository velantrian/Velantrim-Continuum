# CONT-E0T v22 id-order RedTeam

**Reviewed commit:** `bc48a15148d6b7d2f1a9863214cf8a5c734ae10d`  
**Worktree:** `/workspace/cont-e0t/v22-cand-rt-id`  
**Branch:** `research/cont-e0t-v22-cand-redteam-idorder`  
**Scope:** protocol rule `T1_LIST_ORDER.md` + CAND-03 reserialize. Not a new conceptual round.  
**Not done:** science-JSON edits; model; Evidence; PR.

Rule under test (`docs/research/cont_e0t_v2/T1_LIST_ORDER.md`):

```text
T1 LIST ORDER IS NON-TEMPORAL AND NON-SEMANTIC.
```

Canonical = stable `id` ascending. No hand-shuffle. No random. `thin_trajectory` is the only temporal carrier.

---

## Gate

```text
READY_FOR_FIELD_5
```

Named S1 attacks are closed on CAND-03. C3-P1 unchanged and still T1-sufficient compose. CAND-04 bytes frozen and match. Residuals below are not bar fails. **Field 5 ≠ execution ≠ Evidence.**

---

## Index

| ID | Check | Severity |
|----|-------|----------|
| I1 | After-ash suffix ≠ {elm, oak} on constraints / unresolved / unknown | PASS |
| I2 | S1 not unique-semantic / not all-holds-except-ash | PASS |
| I3 | C3-P1 byte-identical to f3d7fb9; 6-way T1 compose intact | PASS |
| I4 | CAND-04 SHA-256 `a83e22c0…4340cb9e` | PASS |
| I5 | CAND-03 T1 lists are id-sorted; thin_trajectory remains the time carrier | PASS |
| I6 | `why_not_on_T1` still describes the old shuffle (`pine, ash, oak, elm`) | MINOR |
| I7 | Id-sort + these four names makes gold the interior hold pair | MINOR |
| I8 | CAND-04 not yet under the new serialize rule (exempt this pass) | MINOR |

---

## 1. List position — PASS (I1)

CAND-03 T1 hold / ticket order after canonical sort:

| Array | Order | After ash | = {elm, oak}? |
|-------|-------|-----------|----------------|
| constraints holds | ash, elm, oak, pine | elm, oak, **pine** | **no** |
| unresolved | ash, elm, oak, pine | elm, oak, **pine** | **no** |
| unknown | ash, elm, oak, pine | elm, oak, **pine** | **no** |

Before-ash on holds is empty. After-ash is the previous gold **plus pine**. The suffix leak that blocked `97cb14a` is gone.

All list-valued `current_semantics` fields checked (`constraints`, `accepted_decisions`, `rejected_alternatives`, `unresolved_items`, `unknown_operations`, `contested_claims`, `artifact_refs`) are `id` ascending.

---

## 2. Semantic / set membership — PASS (I2)

Four current holds: elm=Slack, oak=blog, ash=all outbound, pine=SMS.

- “All holds except ash” = {elm, oak, pine} ≠ gold.
- “Unique hold that binds email/outbound” = ash ≠ gold.
- Rationale / process_position / rejected (`r-sms` only touches pine) do not name a before-set.
- All four `current: true`. IDs do not encode time.

No unique T1 semantic that selects {elm, oak} as “already current when ash became current.”

---

## 3. PRIMARY — PASS (I3)

C3-P1 object equals f3d7fb9. `must_compose` still all present on T1. Pine remains a distractor. Composition still required. Claim B PRIMARY shape intact.

---

## 4. CAND-04 — PASS (I4)

File SHA-256 `a83e22c0377f491fad465a9a2993979560a4c6060e95c085b20d7a2b4340cb9e`. Untouched this pass, as required.

---

## 5. Only temporal carrier — PASS (I5)

CAND-03 `t1_list_order: CANONICAL_ID_ASC_NON_TEMPORAL`.  
`thin_trajectory` seq1 = {elm, oak, …}; seq2 = {ash, pine, …}. That path, not T1 array order, is the S1 clock.

---

## Residuals (not gate-fail)

**I6 MINOR.** S1 `why_not_on_T1` still says list order is `pine, ash, oak, elm`. That sentence is false after reserialize. Evaluator-only (should not enter the reader package). Fix in a docs touch; do not re-shuffle T1 to make the comment true.

**I7 MINOR.** Under id-sort the four hold ids are `ash, elm, oak, pine`. Gold is the **interior pair**. “Not first, not last” would recover S1. That is a naming coincidence, not the after-ash suffix, and the protocol now forbids reading T1 order as time. Do not treat as BLOCKING. If a later revision renames holds, avoid gold = a trivial slice of the sorted id list.

**I8 MINOR.** Rule text: CAND-04 bytes frozen this pass; later pass may re-serialize 04 without changing probes. Pair is temporarily mixed (03 canonical, 04 as-authored). Acceptable for Field-5 *discussion*; do not silently treat 04 list order as temporal.

---

## Recommended Labs action

Field 5 (reader/model identity) may be specified next. Still:

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
CANDIDATE ≠ PILOT ≠ EVIDENCE
READY_FOR_FIELD_5 ≠ GO
```

Optional hygiene before a freeze packet: refresh CAND-03 `why_not_on_T1`; later, re-serialize CAND-04 under the same id-asc rule without touching its probes.

STOP. Docs-only. No experiment. No merge. No architecture.
