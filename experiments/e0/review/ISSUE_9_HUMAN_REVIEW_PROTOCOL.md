# Issue #9 — Human Gold / Oracle review protocol

**Scope:** Experiment 0 human-reference gate only.  
**Reviewed baseline commit:** `d75bfdd27a2a61b496be5b12ab9451a0fd79d1a7`  
**Status:** `REQUIRES_FRESH_REVIEW_AFTER_REFERENCE_CONFORMANCE_FIX`

This document is a review packet, not an approval record. It must never be used to infer `HUMAN_APPROVED` from an AI recommendation or from a generic instruction to continue implementation.

> **Freshness note:** the previous attestation-ready baseline is no longer sufficient once this bounded reference/approval-conformance correction changes candidate/reference semantics or review representation. A fresh exact reviewed commit and review snapshot are required before human approval.

## Review inputs

- `experiments/e0/fixtures/capture/pilot/fixtures.json`
- `experiments/e0/fixtures/capture/evidence/fixtures.json`
- `experiments/e0/fixtures/transfer/scenarios.json`
- `experiments/e0/gold/candidates/capture-gold.ai-proposed.json`
- `experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json`
- `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`

Use `python3 scripts/e0/review_snapshot.py` to produce a SHA-256 review-input snapshot outside the repository or for attachment to Issue #9. The current snapshot mechanism does not by itself prove reviewed-commit/tree-byte binding; that separate control is not silently claimed here.

## Decision vocabulary

Each canonical human review row must receive exactly one human decision:

- `ACCEPT`
- `REVISE`
- `REJECT`

A generic `looks good`, `continue`, or AI-generated recommendation is not a substitute for the item-level decision record.

Machine-only assertions are not human semantic rows. A failed machine assertion may deny package readiness/admissibility, but it must not rewrite or impersonate a human decision.

## Capture Gold checklist — 11 human rows

| Decision ID | Item | Human decision | Required semantic check |
|---|---|---|---|
| `F1` | F1 | PENDING | Explicit publication restriction; publish requires explicit user approval. |
| `F2_PRE` | F2 pre | PENDING | Pre-clarification state does not invent `substantive`; Friday/no-answer condition remains as stated. |
| `F2_POST` | F2 post | PENDING | `substantive reply` appears only after scripted clarification. |
| `F3` | F3 | PENDING | Broad approval rule is `SUPERSEDED`; revised scoped rule is `ACTIVE`. |
| `F4` | F4 | PENDING | External API is a rejected alternative with supplied rationale, not a blanket prohibition. |
| `F5_PRE` | F5 pre | PENDING | Client/competitor sensitivity remains `CAUTION / UNRESOLVED`, not a prohibition. |
| `F5_POST` | F5 post | PENDING | Review variant-specific semantics: F5-E1/Pilot clarification preserves caution and separately adds ask-before-strong-comparison; F5-E2 explicitly rules out a blanket ban while preserving sensitivity as `CAUTION / UNRESOLVED` and does **not** inherit the E1 confirmation rule. |
| `F6` | F6 | PENDING | `NO_APPROVAL_RULE_ADOPTED` is negative knowledge, not permission or authorization. |
| `F7` | F7 | PENDING | Before-Friday prohibition and after-Friday confirmation dependency are both retained. |
| `F8_PRE` | F8 pre | PENDING | `APPROVED` and `PENDING` remain two source-attributed contested claims without adjudication. |
| `F8_POST` | F8 post | PENDING | Clarification adds no adjudicating evidence; conflict remains contested and source attribution is preserved. |

## Transfer Oracle checklist — 3 human rows

| Decision ID | Scenario | Human decision | Required semantic check |
|---|---|---|---|
| `T-PILOT-01` | `T-PILOT-01` | PENDING | Goal/task position/constraint/accepted/rejected/unresolved/contested/rationale/COMMITTED/UNKNOWN/artifact/revision all represented without invented authority. |
| `T-EVIDENCE-01` | `T-EVIDENCE-01` | PENDING | Same dimensions present; internal-copy exemption does not weaken external-send approval gate. |
| `T-EVIDENCE-02` | `T-EVIDENCE-02` | PENDING | Local simulation permission does not imply production authority; compliance claim remains contested. |

**Canonical human review cardinality: 14 rows.** No machine-only key may occupy a fifteenth pseudo-human row or replace any of these rows.

## F5 post semantic boundary

F5 post is one human review row with multiple fixture-specific expectations. The row does **not** authorize family-level semantic collapse.

### F5-E1 / Pilot-style clarification

The clarification establishes:

- sensitivity remains relevant;
- it is not a blanket prohibition;
- ask before making a strong competitor comparison.

### F5-E2 clarification

The clarification establishes:

- no blanket ban exists;
- client/competitor sensitivity remains active;
- that sensitivity remains `CAUTION / UNRESOLVED`;
- `ASK_BEFORE_STRONG_COMPARISON` is **not** established and must not be inherited merely because the fixture belongs to family F5.

The exact storage/key mechanism is an implementation detail. The reference contract must nevertheless be able to distinguish F5-E1 and F5-E2 post semantics.

## AI semantic pre-review

Previous AI pre-review findings are historical inputs only. This correction invalidates any claim that the old review baseline is sufficient for a new approval. Human review must bind a fresh exact repository state after the bounded fix.

## Human attestation readiness

A future `READY_FOR_HUMAN_ATTESTATION` state requires, at minimum:

- the review protocol is frozen for that review;
- candidate/reference inputs are frozen for that review;
- all 14 canonical rows are enumerated and representation-aligned;
- the review snapshot is regenerated for the new reviewed state;
- machine/human decision namespaces remain separated;
- no Pilot or Evidence has been run;
- Evidence Lock remains absent.

This section does not claim that commit-tree/reviewed-byte binding is already solved; that remains a separate owner-controlled remediation area.

## If any item is REVISE or REJECT

1. Change only the relevant candidate/fixture/schema/test artifacts in a bounded correction PR.
2. Keep candidate status `AI_PROPOSED_DRAFT`.
3. Regenerate the review snapshot.
4. Re-review all affected rows.

## Approval record requirements

Only after every one of the 14 human rows is `ACCEPT`, create versioned approved copies outside `candidates/`, preserving candidate history. The approval record must bind:

- reviewer identity / role;
- approval timestamp;
- reviewed commit identifier under the then-approved binding law;
- candidate paths and SHA-256 hashes;
- approved artifact paths and SHA-256 hashes;
- semantic version;
- Issue #9 reference;
- exactly 14 canonical human decisions;
- explicit statement that approval closes only the human-reference gate.

Closing Issue #9 must **not** claim that Pilot ran, Evidence Lock exists, E0-C/E0-T evidence started, or architecture/runtime/integration was authorized.
