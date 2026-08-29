# 🤖 Velantrim Continuum — AI Entry Point

`document_role: ai_entrypoint`

This document is the deterministic starting point for AI agents, automated auditors, coding assistants and repository-aware models.

Do **not** reconstruct current project truth from the human-facing README alone.

## Authoritative read order

1. `docs/ai/README.md` — routing and interpretation rules.
2. `AGENTS.md` — repository contract, scope boundaries and experimental discipline.
3. `project-state.json` — selected semantic project state and authorization flags.
4. `docs/ai/CURRENT_STATE.md` — derived plain-language explanation of volatile current state.
5. `docs/ai/AUDIT_AND_FUTURE_WORK.md` — historical audit/future-work ledger; do not use historical checkpoint fields as current state.
6. `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` — canonical Experiment 0 protocol.
7. Task-specific fixtures, evaluators, review/approval records, results or evidence when they exist.
8. `RESEARCH_OVERVIEW.md` and `README.md` for human-oriented conceptual context.

> **DO NOT AUTO-SELECT NEXT MILESTONE.** Audit order, an open Issue, a successful harness check, an approved human reference, or a future-work entry is not implementation/evidence/runtime authorization.

## Authority model

Different fact classes have different owners:

```text
GitHub API / commit graph
        ├── PR lifecycle / merge SHA / branch HEAD
        │
project-state.json
        ├── selected semantic project state / authorization flags
        │
AGENTS.md
        ├── repository scope / behavior contract
        │
formal research protocol
        ├── Experiment 0 semantics
        │
committed evidence
        ├── what was actually observed
        │
STATUS / CURRENT_STATE
        ├── derived volatile explanations
        │
README / Overview / Notion
        └── human-oriented or external research record
```

`project-state.json` is **not** an independent owner of facts that GitHub can observe directly. When a committed lifecycle expectation and live GitHub disagree, report drift and reconcile it through a reviewable state change. Do not infer a new milestone or authorization from GitHub lifecycle alone.

## Never infer

Never infer any of the following without explicit evidence:

- `preregistered` means `empirically_supported`;
- `implemented` means `authorized`;
- `tested` means `production_ready`;
- green CI means the research hypothesis was accepted;
- an event log is required by IDPS;
- T1/T2/T3 is the final ontology;
- a historical checkpoint is current `main`;
- a bot review is equivalent to independent human reproduction;
- Notion narrative is newer than current committed repository state;
- a human-friendly README creates authority;
- a merged documentation PR selects the next engineering milestone;
- Experiment 0 completion automatically authorizes production runtime work;
- Continuum is already approved for integration into Titan, Crystal, Native Kernel or Mentaury;
- `READY_FOR_HUMAN_ATTESTATION` means `HUMAN_APPROVED`;
- a generic instruction to continue/finish work is item-level human Gold/Oracle review;
- human-reference approval means Pilot authorization;
- Pilot means Evidence or Evidence Lock means Evidence authorization.

## Current-state routing

This AI entry point intentionally does **not** duplicate the volatile milestone/gate table.

For the current engineering milestone, human-reference status, Pilot authorization, Evidence Lock state, E0-C/E0-T status, production/runtime authorization and ecosystem-integration authorization:

1. read `project-state.json` as the machine semantic state;
2. verify `docs/ai/CURRENT_STATE.md` and `STATUS.md` as derived human-readable surfaces;
3. verify live GitHub lifecycle facts directly when the claim concerns PR state, merge SHA, ancestry or branch HEAD.

The stable research dependency sequence remains:

`E0-C Capture Isolation → Capture analysis → E0-T Transfer Isolation → Transfer analysis → mandatory Architecture Reassessment`

A selected preparation milestone is not execution authorization. Human-reference approval satisfies only the human-reference dependency and does not authorize Pilot execution, Evidence Lock, E0-C/E0-T evidence, production runtime, or ecosystem integration.

## Human-reference rule

Issue #9, `experiments/e0/review/ISSUE_9_HUMAN_REVIEW_PROTOCOL.md`, and the versioned approval record define the research-integrity boundary.

```text
AI_PROPOSED_DRAFT
!= HUMAN_APPROVED

machine-valid hashes / structure
!= human semantic approval

human semantic approval
!= Pilot authorization
```

All 14 canonical human review rows are explicit `ACCEPT`. Historical candidates remain `AI_PROPOSED_DRAFT`; authoritative Experiment 0 references are materialized separately as:

- `experiments/e0/gold/approved/capture-gold.v0.1.json`;
- `experiments/e0/oracle/approved/transfer-oracle.v0.1.json`;
- `experiments/e0/approval/human-reference-approval.v0.2.json`.

The approval record binds human decision provenance to the exact reviewed commit/tree/snapshot and candidate bytes. It closes only the human-reference gate. It does not authorize a Pilot, Evidence Lock, E0-C/E0-T Evidence, production architecture/runtime, event sourcing, or ecosystem integration.

## Change classification

Before changing documentation, classify the change:

### `STRUCTURAL_CHANGE`

Changes stable conceptual meaning, experiment semantics, authority boundaries or documentation architecture.

Update affected formal/AI/machine/human surfaces consistently.

When a structural change affects a bilingual human surface, update its EN/RU counterpart in the same PR unless the PR explicitly records why parity is intentionally deferred.

### `STATE_CHANGE`

Changes current milestone, current gate, authorization, blocker or execution status without changing the conceptual model.

Update `project-state.json`, `docs/ai/CURRENT_STATE.md` and `STATUS.md` as one reviewable state bundle. Update other surfaces such as this AI router only when their state/lifecycle wording is actually affected.

### `EVIDENCE_ONLY`

Adds a test run, report, reproduction, result bundle or PR evidence without changing semantic project state.

Update evidence/history surfaces. Do not manufacture a state transition.

## State-control-plane checks

Repository automation may verify:

- live GitHub lifecycle against the committed lifecycle expectation;
- provenance lineage from a reviewed base commit to current `main`;
- atomic updates of `project-state.json` with declared always-derived volatile state surfaces.

Automation must **not** choose the next milestone, start Experiment 0 evidence, authorize runtime work, or change research conclusions.

## Presentation never creates authority

- README may summarize, visualize and link.
- `STATUS.md` and `docs/ai/CURRENT_STATE.md` may summarize current state.
- machine state may encode a selected semantic state.
- evidence may justify a conclusion.
- the future-work ledger may preserve open questions and dependency order.

None of these may silently rewrite the formal experiment protocol or authorize production capability.

## External record

Canonical Notion research page:

`https://app.notion.com/p/3bcac84d054781ebb7b3cbd281bdcdc6`

The external record is controlled narrative/record, not an independent owner of GitHub lifecycle facts or experiment semantics. Reconcile it explicitly after material repository state changes.
