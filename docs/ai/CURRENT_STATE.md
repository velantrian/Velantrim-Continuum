# 🤖 Current State — Velantrim Continuum

`document_role: volatile_ai_state_explanation`

Selected semantic machine-readable values live in [`project-state.json`](../../project-state.json). Observable GitHub lifecycle facts must be verified live.

## Current checkpoint

- Project: Velantrim Continuum / IDPS Research.
- Status: Research / Pre-implementation.
- Current semantic position: **human-reference review completed; STOP pending separate owner selection of any next engineering milestone**.
- Experiment 0 harness: **implemented pre-Pilot**.
- Capture correspondence measurement law: **`e0-correspondence-v0.3`**.
- PR #24 removed the order-dependent greedy assignment rule and replaced it with global maximum-cardinality / maximum-score one-to-one assignment with fail-closed acceptance only for forced pairs.
- PR #23 closed the narrow B-01 same-byte Git tree-entry bypass on the selected review head by binding Git mode/blob identity as well as bytes.
- Human Review snapshot: **v0.4**, selected from reviewed commit `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`.
- Human semantic decisions: **14 / 14 ACCEPT** in Issue #9.
- Historical candidate Capture Gold and Transfer Oracle: **AI_PROPOSED_DRAFT — preserved as non-authoritative history**.
- Versioned Capture Gold and Transfer Oracle: **HUMAN_APPROVED**.
- Approval provenance: `experiments/e0/approval/human-reference-approval.v0.2.json`.
- Harness-validation Pilot: **not run and not authorized by this approval**.
- Evidence readiness: **false**.
- Evidence Lock: **not created**.
- E0-C evidence: **not started**.
- E0-T evidence: **not started**.
- Production architecture: **not frozen**.
- Production runtime: **not authorized**.
- Ecosystem integration: **not authorized**.
- Event sourcing: **not required**.
- State hypotheses: **not canonical**.

## Current bounded work order

1. Preserve the v0.3 Capture correspondence law and its permutation invariants unless a separately reviewed measurement-law change is required.
2. Treat Issue #9 human semantic review as complete: exactly 14 canonical rows are `ACCEPT`.
3. Use only the versioned approved Gold / Oracle as authoritative human references; preserve the AI-proposed candidates unchanged as review history.
4. **STOP.** This human-reference approval does not select or authorize a Pilot.
5. A `PILOT — NOT EVIDENCE` run requires a separate owner decision and must remain explicitly labelled non-evidence.
6. After a separately authorized Pilot: fix Pilot defects; if locked semantics change, version/review before lock.
7. Evidence Lock may be created only after its own readiness conditions are met; it is currently `NOT_CREATED`.
8. **STOP.** E0-C Evidence requires separate authorization.
9. Later: E0-C Evidence → Capture analysis → E0-T Evidence → Transfer analysis → mandatory Architecture Reassessment.

## Review binding checkpoint

The approved human-reference checkpoint is bound to:

- reviewed commit: `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`;
- reviewed tree: `03be5376d592ec9c12299627a6ec0507548363b8`;
- snapshot version: `0.4`;
- snapshot SHA-256: `e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4`;
- bound review/control paths: `7`;
- human decisions: `14 / 14 ACCEPT`;
- approved Capture Gold: `experiments/e0/gold/approved/capture-gold.v0.1.json`;
- approved Transfer Oracle: `experiments/e0/oracle/approved/transfer-oracle.v0.1.json`.

No bound review/control path changed between the selected baseline and the approval base. The approval validator independently checks reviewed commit/tree identity, current mode/blob identity, exact bytes, candidate/approved SHA-256 bindings, the 14 decision namespace, and continued absence of Evidence Lock.

## Critical non-claims

Do not claim that:

- unit/regression tests are an Experiment 0 Pilot;
- green CI is scientific validity;
- B-01 technical binding closure is human semantic approval;
- historical AI-proposed candidates became authoritative in place;
- human approval authorizes Pilot;
- human approval creates Evidence Lock;
- harness implementation means E0-C or E0-T Evidence has started;
- `state.json` is proven sufficient or insufficient;
- event sourcing is required;
- a production IDPS runtime is justified;
- Continuum is production-ready.

## Authority and freshness rule

- GitHub lifecycle facts → verify live GitHub.
- Semantic project state / authorization flags → [`project-state.json`](../../project-state.json).
- Experiment semantics → canonical preregistration.
- Capture association measurement semantics → [`E0_CORRESPONDENCE_LAW_V0_3.md`](../research/E0_CORRESPONDENCE_LAW_V0_3.md).
- Human-reference approval facts → `experiments/e0/approval/human-reference-approval.v0.2.json` plus Issue #9.
- This file / [`STATUS.md`](../../STATUS.md) → derived explanations.

Any disagreement is state drift and must be reconciled through a reviewable state change.
