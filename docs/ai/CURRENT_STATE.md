# 🤖 Current State — Velantrim Continuum

`document_role: volatile_ai_state_explanation`

Selected semantic machine-readable values live in [`project-state.json`](../../project-state.json). Observable GitHub lifecycle facts must be verified live.

## Current checkpoint

- Project: Velantrim Continuum / IDPS Research.
- Status: Research / Pre-implementation.
- Selected workstream: `EXPERIMENT_0_EVALUATION_CONTRACT_AND_HARNESS_READINESS`.
- Preregistration hardening: merged via PR #5.
- Experiment 0 data contracts / F1–F8 fixture materialization: merged via PR #6.
- Experiment 0 harness implementation: **started**.
- Deterministic capture evaluator / HARD FAIL evaluator / provider-neutral adapter runner / transfer representation preparation / evidence-lock validation: current implementation scope.
- Candidate Capture Gold and Transfer Oracle: **AI_PROPOSED_DRAFT — non-authoritative**.
- Human-authored Gold / Oracle approval: **required before pilot**.
- Harness-validation pilot: **not run**.
- Evidence readiness: **false**.
- Evidence lock: none.
- E0-C evidence: not started.
- E0-T evidence: not started.
- Production architecture: not frozen.
- Production runtime: not authorized.
- Ecosystem integration: not authorized.
- Event sourcing: not required.
- State hypotheses: not canonical.

## Current bounded work order

1. Complete deterministic evaluator / minimal harness implementation and offline tests.
2. Keep model/provider execution behind the provider-neutral adapter boundary.
3. Require human experimenter review/approval of candidate Gold and Oracle; do not self-promote AI proposals into truth.
4. Only after human approval, run `PILOT — NOT EVIDENCE` against pilot fixtures.
5. Fix pilot defects; if semantics change, version the draft before lock.
6. Freeze protocol/schema/evidence fixtures/Gold/Oracle/evaluator/run-config/prompts/randomization by hash.
7. Mark evidence readiness only if the lock validates and human reference status is `HUMAN_APPROVED`.
8. **STOP.** E0-C evidence requires a separate authorization.
9. Later: E0-C evidence → Capture analysis → E0-T evidence → Transfer analysis → mandatory Architecture Reassessment.

## Critical non-claims

Do not claim that:

- synthetic/unit tests are an Experiment 0 pilot;
- candidate Gold/Oracle are human-authored;
- harness implementation means evidence execution has started;
- E0-C or E0-T has started;
- `state.json` is proven sufficient or insufficient;
- event sourcing is required;
- a production IDPS runtime is justified;
- Continuum is production-ready.

## Authority and freshness rule

- GitHub lifecycle facts → verify live GitHub.
- Semantic project state / authorization flags → `project-state.json`.
- Experiment semantics → canonical preregistration.
- This file / `STATUS.md` → derived explanations.

Any disagreement is state drift and must be reconciled through a reviewable state change.
