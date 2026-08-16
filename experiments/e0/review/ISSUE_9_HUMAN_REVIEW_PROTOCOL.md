# Issue #9 — Human Gold / Oracle review protocol

**Scope:** Experiment 0 human-reference gate only.  
**Reviewed baseline commit:** `b95ad363409400043636fcdd7908feba97901111`  
**Status:** `AWAITING_HUMAN_DECISION`

This document is a review packet, not an approval record. It must never be used to infer `HUMAN_APPROVED` from an AI recommendation or from a generic instruction to continue implementation.

## Review inputs

- `experiments/e0/fixtures/capture/pilot/fixtures.json`
- `experiments/e0/fixtures/capture/evidence/fixtures.json`
- `experiments/e0/fixtures/transfer/scenarios.json`
- `experiments/e0/gold/candidates/capture-gold.ai-proposed.json`
- `experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json`
- `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`

Use `python3 scripts/e0/review_snapshot.py` to produce a SHA-256 review-input snapshot outside the repository or for attachment to Issue #9.

## Decision vocabulary

Each review item must receive exactly one human decision:

- `ACCEPT`
- `REVISE`
- `REJECT`

A generic `looks good`, `continue`, or AI-generated recommendation is not a substitute for the item-level decision record.

## Capture Gold checklist

| Item | Human decision | Required semantic check |
|---|---|---|
| F1 | PENDING | Explicit publication restriction; publish requires explicit user approval. |
| F2 pre | PENDING | Pre-clarification state does not invent `substantive`; Friday/no-answer condition remains as stated. |
| F2 post | PENDING | `substantive reply` appears only after scripted clarification. |
| F3 | PENDING | Broad approval rule is `SUPERSEDED`; revised scoped rule is `ACTIVE`. |
| F4 | PENDING | External API is a rejected alternative with supplied rationale, not a blanket prohibition. |
| F5 pre | PENDING | Client sensitivity remains caution/unresolved, not a prohibition. |
| F5 post | PENDING | Clarification preserves caution and separately adds ask-before-strong-comparison rule. |
| F6 | PENDING | `NO_APPROVAL_RULE_ADOPTED` is negative knowledge, not permission or authorization. |
| F7 | PENDING | Before-Friday prohibition and after-Friday confirmation dependency are both retained. |
| F8 pre | PENDING | `APPROVED` and `PENDING` remain two source-attributed contested claims without adjudication. |
| F8 post | PENDING | Clarification adds no adjudicating evidence; conflict remains contested. |

## Transfer Oracle checklist

| Scenario | Human decision | Required semantic check |
|---|---|---|
| `T-PILOT-01` | PENDING | Goal/task position/constraint/accepted/rejected/unresolved/contested/rationale/COMMITTED/UNKNOWN/artifact/revision all represented without invented authority. |
| `T-EVIDENCE-01` | PENDING | Same dimensions present; internal-copy exemption does not weaken external-send approval gate. |
| `T-EVIDENCE-02` | PENDING | Local simulation permission does not imply production authority; compliance claim remains contested. |

## AI semantic pre-review

The current AI pre-review found no additional blocking semantic defect after PR #8. This is only an **AI recommendation to inspect/accept**, not human approval. The human reviewer remains responsible for every row above.

## If any item is REVISE or REJECT

1. Change only the relevant candidate/fixture/schema/test artifacts in a bounded correction PR.
2. Keep candidate status `AI_PROPOSED_DRAFT`.
3. Regenerate the SHA-256 review snapshot.
4. Re-review all affected rows.

## Approval record requirements

Only after every row is `ACCEPT`, create versioned approved copies outside `candidates/`, preserving the candidate history. The approval record must bind:

- reviewer identity / role;
- approval timestamp;
- reviewed commit;
- candidate paths and SHA-256 hashes;
- approved artifact paths and SHA-256 hashes;
- semantic version;
- Issue #9 reference;
- explicit statement that approval closes only the human-reference gate.

Closing Issue #9 must **not** claim that Pilot ran, Evidence Lock exists, E0-C/E0-T evidence started, or architecture/runtime/integration was authorized.
