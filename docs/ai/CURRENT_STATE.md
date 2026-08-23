# 🤖 Current State — Velantrim Continuum

`document_role: volatile_ai_state_explanation`

Selected semantic machine-readable values live in [`project-state.json`](../../project-state.json). Observable GitHub lifecycle facts must be verified live.

## Current checkpoint

- Project: Velantrim Continuum / IDPS Research.
- Status: Research / Pre-implementation.
- Human-reference gate: **`CLOSED`** by a bounded human-reference approval.
- Experiment 0 harness: **implemented pre-Pilot**.
- Capture correspondence measurement law: **`e0-correspondence-v0.3`**.
- PR #24 removed the order-dependent greedy assignment rule and replaced it with global maximum-cardinality / maximum-score one-to-one assignment with fail-closed acceptance only for forced pairs.
- PR #23 closed the narrow B-01 same-byte Git tree-entry bypass on the selected review head by binding Git mode/blob identity as well as bytes.
- Human Review snapshot: **v0.4**, selected from reviewed commit `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`.
- Human semantic decisions: **14 / 14 ACCEPT**.
- Historical Capture Gold and Transfer Oracle candidates: **AI_PROPOSED_DRAFT — preserved and non-authoritative**.
- Approved Capture Gold: **`experiments/e0/gold/approved/capture-gold.v0.1.json` — HUMAN_APPROVED**.
- Approved Transfer Oracle: **`experiments/e0/oracle/approved/transfer-oracle.v0.1.json` — HUMAN_APPROVED**.
- Approval provenance: **`experiments/e0/approval/human-reference-approval.v0.2.json`**.
- Harness-validation Pilot: **NOT_AUTHORIZED / not run**.
- Canonical Pilot package authorization: **`null` — no exact manifest path/SHA is authorized**.
- Evidence readiness: **false**.
- Evidence Lock: **not created**.
- E0-C evidence: **not started / not authorized**.
- E0-T evidence: **not started / not authorized**.
- Production architecture: **not frozen**.
- Production runtime: **not authorized**.
- Ecosystem integration: **not authorized**.
- Event sourcing: **not required**.
- State hypotheses: **not canonical**.

## Current bounded work order

1. Keep the v0.3 Capture correspondence law and its permutation invariants stable unless a separately reviewed measurement-law change is required.
2. Preserve the human-approved v0.1 Capture Gold and Transfer Oracle plus the v0.2 approval provenance as the authoritative Experiment 0 human reference.
3. Keep the historical candidate artifacts unchanged as `AI_PROPOSED_DRAFT`; approval does not rewrite their history.
4. **STOP at the Pilot authorization boundary.** Human-reference approval does not itself authorize `PILOT — NOT EVIDENCE`.
5. A future bounded Pilot requires a separate owner GO, canonical `experiment_0_pilot_status = AUTHORIZED_BOUNDED_PILOT`, and a canonical constructible package/activation binding: immutable manifest blob in package commit A; direct-child activation commit B; exact manifest path/SHA plus A/tree(A); bounded activation paths; and canonical authority bytes materialized as B's regular non-executable `100644` `project-state.json` Git blob. The current authorization slot remains `null`.
6. Only after those separate reviewable changes may a Pilot run occur, and every Pilot output must remain explicitly labelled `PILOT — NOT EVIDENCE`.
7. After a separately authorized Pilot: fix Pilot defects; if locked semantics change, version/review before lock.
8. Evidence Lock may be created only after its own readiness conditions are met; it is currently `NOT_CREATED`.
9. **STOP.** E0-C Evidence requires separate authorization.
10. Later: E0-C Evidence → Capture analysis → E0-T Evidence → Transfer analysis → mandatory Architecture Reassessment.

## Review and approval binding checkpoint

The selected reviewed checkpoint remains:

- reviewed commit: `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`;
- reviewed tree: `03be5376d592ec9c12299627a6ec0507548363b8`;
- snapshot version: `0.4`;
- snapshot SHA-256: `e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4`;
- bound review/control paths: `7`;
- human decisions recorded: `14 / 14 ACCEPT`.

The approval record additionally binds every reviewed path's Git mode, Git blob SHA and SHA-256, and records candidate → approved hashes. The approval-head validator independently re-reads the reviewed commit and fails closed on byte, blob, mode or symlink drift.

## Critical non-claims

Do not claim that:

- human-reference approval authorizes Pilot;
- existence of the canonical Pilot package-authorization field authorizes Pilot;
- unit/regression tests are an Experiment 0 Pilot;
- green CI is scientific validity;
- approved Gold / Oracle are Evidence;
- Evidence Lock exists;
- E0-C or E0-T Evidence has started;
- `state.json` is proven sufficient or insufficient;
- event sourcing is required;
- a production IDPS runtime is justified;
- production architecture is frozen;
- Continuum is approved for ecosystem integration;
- Continuum is production-ready.

## Authority and freshness rule

- GitHub lifecycle facts → verify live GitHub.
- Semantic project state / authorization flags → [`project-state.json`](../../project-state.json).
- A future Pilot authorization must bind canonical Pilot status to the exact constructible A→B package/activation chain: manifest blob in A, exact manifest path/SHA and A/tree(A), direct-child B with bounded activation paths, and canonical authority committed as B's exact `100644` `project-state.json` blob; none of those elements can substitute for the others.
- Experiment semantics → canonical preregistration.
- Human reference approval → `experiments/e0/approval/human-reference-approval.v0.2.json` plus the exact Issue #9 human decision record.
- Capture association measurement semantics → [`E0_CORRESPONDENCE_LAW_V0_3.md`](../research/E0_CORRESPONDENCE_LAW_V0_3.md).
- This file / [`STATUS.md`](../../STATUS.md) → derived explanations.

Any disagreement is state drift and must be reconciled through a reviewable state change.
