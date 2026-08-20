# 🤖 Current State — Velantrim Continuum

`document_role: volatile_ai_state_explanation`

Selected semantic machine-readable values live in [`project-state.json`](../../project-state.json). Observable GitHub lifecycle facts must be verified live.

## Current checkpoint

- Project: Velantrim Continuum / IDPS Research.
- Status: Research / Pre-implementation.
- Current semantic gate: `EXPERIMENT_0_HUMAN_REFERENCE_REVIEW_GATE`.
- Experiment 0 harness: **implemented pre-Pilot**.
- Capture correspondence measurement law: **`e0-correspondence-v0.3`**.
- PR #24 removed the order-dependent greedy assignment rule and replaced it with global maximum-cardinality / maximum-score one-to-one assignment with fail-closed acceptance only for forced pairs.
- PR #23 closed the narrow B-01 same-byte Git tree-entry bypass on the selected review head by binding Git mode/blob identity as well as bytes.
- Human Review snapshot: **v0.4**, selected from reviewed commit `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`.
- Human semantic decisions: **0 / 14**.
- Candidate Capture Gold and Transfer Oracle: **AI_PROPOSED_DRAFT — non-authoritative**.
- Harness-validation Pilot: **not run**.
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

1. Keep the v0.3 Capture correspondence law and its permutation invariants stable unless a separately reviewed measurement-law change is required.
2. Complete the explicit 14-row human review in Issue #9. Each row requires `ACCEPT`, `REVISE`, or `REJECT`; generic continuation language is not a semantic decision.
3. If any row is revised/rejected, change only affected review material and select a fresh reviewed baseline/snapshot for affected review scope.
4. Only after all required human decisions and a bounded human-approval change may the human-reference gate close.
5. Pilot remains a separate authorization boundary: Human approval does not itself authorize `PILOT — NOT EVIDENCE`.
6. After a separately authorized Pilot: fix Pilot defects; if locked semantics change, version/review before lock.
7. Evidence Lock may be created only after its own readiness conditions are met; it is currently `NOT_CREATED`.
8. **STOP.** E0-C Evidence requires separate authorization.
9. Later: E0-C Evidence → Capture analysis → E0-T Evidence → Transfer analysis → mandatory Architecture Reassessment.

## Review binding checkpoint

The current selected review checkpoint is:

- reviewed commit: `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`;
- reviewed tree: `03be5376d592ec9c12299627a6ec0507548363b8`;
- snapshot version: `0.4`;
- snapshot SHA-256: `e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4`;
- bound review/control paths: `7`;
- human decisions recorded: `0 / 14`.

The matcher v0.3 remediation does not touch those seven snapshot paths. It therefore does not itself alter Gold/Oracle semantics, create human approval, authorize Pilot, or create Evidence Lock.

## Critical non-claims

Do not claim that:

- unit/regression tests are an Experiment 0 Pilot;
- green CI is scientific validity;
- B-01 technical binding closure is human semantic approval;
- candidate Gold/Oracle are human-authored or authoritative;
- the selected snapshot is an approval record;
- human approval would automatically authorize Pilot;
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
- This file / [`STATUS.md`](../../STATUS.md) → derived explanations.

Any disagreement is state drift and must be reconciled through a reviewable state change.
