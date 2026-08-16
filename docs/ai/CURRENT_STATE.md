# 🤖 Current State — Velantrim Continuum

`document_role: volatile_ai_state_explanation`

This file explains the current volatile project state in plain technical language. Selected semantic machine-readable values live in [`project-state.json`](../../project-state.json). Observable GitHub lifecycle facts must be verified against GitHub rather than inferred from this derived explanation.

## Current checkpoint

- Project: Velantrim Continuum / IDPS Research.
- Status: Research / Pre-implementation.
- Research foundation: merged via PR #1.
- Foundation merge commit: `e14cf46f96724dda933ce647b46f72fc4866dc7c`.
- Human / AI / Machine Documentation Architecture v1: completed via PR #2.
- Documentation PR #2: **MERGED**.
- PR #2 merge commit: `533cc6abcf59d20f7a273098f043784c95421711`.
- Next bounded engineering milestone: **`EXPERIMENT_0_EVALUATION_CONTRACT_AND_HARNESS_READINESS` selected**.
- Current workstream: **active**, bounded to preregistration hardening, experiment contracts, deterministic evaluation, minimal harness, non-evidence pilot validation and evidence lock.
- Experiment 0 harness: not started.
- E0-C evidence: not started.
- E0-T evidence: not started.
- Evidence runs: none.
- Production architecture: not frozen.
- Production runtime: not authorized.
- Ecosystem integration: not authorized.
- Event sourcing: not required.
- State tiers: not canonical.

## Current bounded work order

1. Keep the completed Documentation Architecture v1 checkpoint reconciled with live GitHub lifecycle facts.
2. Harden the Experiment 0 preregistration before evidence.
3. Define bounded experimental state / fixture / Gold / Oracle / manifest / evaluation contracts.
4. Materialize F1–F8 fixtures and human-authored Gold without model self-Gold.
5. Implement deterministic evaluator and separate HARD FAIL evaluation.
6. Implement only the minimal E0-C / E0-T harness required by Experiment 0.
7. Run harness-validation pilot explicitly labeled **PILOT — NOT EVIDENCE**.
8. Fix pilot defects before lock; version any material protocol change.
9. Freeze protocol/schema/fixtures/Gold/Oracle/evaluator/run-config hashes and mark evidence readiness.
10. **STOP.** Do not start E0-C evidence unless separately authorized.
11. After separately authorized E0-C evidence and Capture analysis, run E0-T evidence.
12. Perform mandatory Architecture Reassessment before any production architecture decision.

## Current non-claims

Do not claim that:

- the Experiment 0 harness has started merely because this milestone is selected;
- E0-C or E0-T evidence has started;
- a complex IDPS runtime has been justified;
- `state.json` has been proven sufficient or insufficient;
- event sourcing is required;
- state tiers are canonical;
- Capture Assurance has been validated;
- model replacement continuity has been validated;
- stale-successor handling has been tested;
- Continuum is production-ready;
- any ecosystem integration has been authorized.

## Authority and freshness rule

Use the fact owner appropriate to the question:

- GitHub lifecycle facts (`PR state`, `merge SHA`, branch `HEAD`) → verify live GitHub.
- Selected semantic project state and authorization flags → `project-state.json`.
- Experiment semantics → formal preregistration.
- This file and `STATUS.md` → derived explanations.

If a GitHub fact and committed semantic/derived state disagree, treat the disagreement as state drift. Do not silently infer a newer milestone or authorization. Reconcile the repository through a reviewable `STATE_CHANGE`.
