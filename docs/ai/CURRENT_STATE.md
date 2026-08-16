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
- Next bounded engineering milestone: **not selected**.
- Experiment 0 harness: not started.
- Evidence runs: none.
- Production architecture: not frozen.
- Production runtime: not authorized.
- Ecosystem integration: not authorized.

## Current research order

1. Keep the completed Documentation Architecture v1 checkpoint reconciled with live GitHub lifecycle facts.
2. Select the next bounded engineering milestone explicitly.
3. Only when explicitly authorized, build the bounded Experiment 0 evaluation/harness work required by the preregistration.
4. Run E0-C Capture Isolation first.
5. Analyze Capture before E0-T.
6. Run E0-T Transfer Isolation second.
7. Perform mandatory Architecture Reassessment.
8. Only then decide whether additional IDPS architecture is justified.

## Current non-claims

Do not claim that:

- a complex IDPS runtime has been justified;
- `state.json` has been proven sufficient or insufficient;
- event sourcing is required;
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
