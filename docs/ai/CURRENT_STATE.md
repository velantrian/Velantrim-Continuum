# 🤖 Current State — Velantrim Continuum

`document_role: volatile_ai_state_explanation`

This file explains the current volatile project state in plain technical language. Exact machine-readable values live in [`project-state.json`](../../project-state.json).

## Current checkpoint

- Project: Velantrim Continuum / IDPS Research.
- Status: Research / Pre-implementation.
- Research foundation: merged via PR #1.
- Foundation merge commit: `e14cf46f96724dda933ce647b46f72fc4866dc7c`.
- Current documentation work: Human / AI / Machine Documentation Architecture v1.
- Current documentation PR: #2 — OPEN.
- Experiment 0 harness: not started.
- Evidence runs: none.
- Production architecture: not frozen.
- Production runtime: not authorized.
- Ecosystem integration: not authorized.

## Current research order

1. Review and close documentation PR #2.
2. Select the next bounded engineering milestone explicitly.
3. When authorized, build only the bounded Experiment 0 harness required by the preregistration.
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

## Freshness rule

When this file and `project-state.json` disagree, treat the disagreement as documentation drift. Do not silently infer the newer state. Verify live repository evidence and reconcile both surfaces.
