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
- Pilot preparation decision: **`GO — PREPARE BOUNDED PILOT PACKAGE`**, recorded by merged PR #34.
- Selected preparation candidate: **`F1-P-A / NO_TOOLS / UNCONTROLLED_LOCAL_ADVISORY`**.
- Mandatory real provider/model/adapter/request/credential/budget values: **UNRESOLVED / intentionally unpinned**.
- `OD-PILOT-01`: **NOT_ADOPTED**.
- Package A / activation B: **NOT_CREATED**.
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
4. PR #34 permits **bounded Pilot-package preparation only** for `F1-P-A / NO_TOOLS`; it does not adopt `OD-PILOT-01` and does not authorize Pilot.
5. Resolve and present the mandatory exact provider/model/adapter/request/credential/budget values for a separate `OD-PILOT-01` owner-adoption decision. Synthetic test values are not authority.
6. **STOP before package A / activation B / Pilot.** Current canonical state remains `experiment_0_pilot_status = NOT_AUTHORIZED` and `experiment_0_pilot_authorization = null`.
7. A future bounded Pilot requires a separate owner GO, canonical `experiment_0_pilot_status = AUTHORIZED_BOUNDED_PILOT`, and a canonical constructible package/activation binding: immutable manifest blob in package commit A; direct-child activation commit B; exact manifest path/SHA plus A/tree(A); bounded activation paths; and canonical authority bytes materialized as B's regular non-executable `100644` `project-state.json` Git blob.
8. Only after those separate reviewable changes may a Pilot run occur, and every Pilot output must remain explicitly labelled `PILOT — NOT EVIDENCE`.
9. After a separately authorized Pilot: fix Pilot defects; if locked semantics change, version/review before lock.
10. Evidence Lock may be created only after its own readiness conditions are met; it is currently `NOT_CREATED`.
11. **STOP.** E0-C Evidence requires separate authorization.
12. Later: E0-C Evidence → Capture analysis → E0-T Evidence → Transfer analysis → mandatory Architecture Reassessment.

## Review and approval binding checkpoint

The selected reviewed checkpoint remains:

- reviewed commit: `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`;
- reviewed tree: `03be5376d592ec9c12299627a6ec0507548363b8`;
- snapshot version: `0.4`;
- snapshot SHA-256: `e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4`;
- bound review/control paths: `7`;
- human decisions recorded: `14 / 14 ACCEPT`.

The approval record additionally binds every reviewed path's Git mode, Git blob SHA and SHA-256, and records candidate → approved hashes. The approval-head validator independently re-reads the reviewed commit and fails closed on byte, blob, mode or symlink drift.

## Pilot preparation boundary

Merged PR #34 records the owner's `OD-PILOT-01-PREP` decision to **GO — PREPARE BOUNDED PILOT PACKAGE**. It permits candidate preparation and documentation only.

```text
preparation GO != OD-PILOT-01 adoption
preparation GO != package A
preparation GO != activation B
preparation GO != Pilot authorization
Pilot != Evidence
```

The preparation decision cannot substitute for the later exact-value decision, package construction, activation binding, or canonical authorization state.

## Critical non-claims

Do not claim that:

- human-reference approval authorizes Pilot;
- PR #34 or its preparation GO adopts `OD-PILOT-01`;
- PR #34 creates package A or activation B;
- Pilot preparation authorizes Pilot execution;
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
- Pilot preparation authority is bounded to the merged PR #34 decision and does not override canonical `NOT_AUTHORIZED` Pilot state.
- A future Pilot authorization must bind canonical Pilot status to the exact constructible A→B package/activation chain: manifest blob in A, exact manifest path/SHA and A/tree(A), direct-child B with bounded activation paths, and canonical authority committed as B's exact `100644` `project-state.json` blob; none of those elements can substitute for the others.
- Experiment semantics → canonical preregistration.
- Human reference approval → `experiments/e0/approval/human-reference-approval.v0.2.json` plus the exact Issue #9 human decision record.
- Capture association measurement semantics → [`E0_CORRESPONDENCE_LAW_V0_3.md`](../research/E0_CORRESPONDENCE_LAW_V0_3.md).
- This file / [`STATUS.md`](../../STATUS.md) → derived explanations.

Any disagreement is state drift and must be reconciled through a reviewable state change.
