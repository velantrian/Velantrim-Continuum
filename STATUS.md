# 📊 Velantrim Continuum — Current Status

**Project:** 🌎 Velantrim Continuum 🪎  
**Technical name:** IDPS — Inference-Decoupled Process Substrate  
**Status:** Research / Pre-implementation

## Current position

| Area | State |
|---|---|
| Research foundation | ✅ Merged |
| Experiment 0 contracts / fixtures | ✅ Implemented |
| Experiment 0 harness | ✅ Implemented pre-Pilot |
| Capture correspondence law | ✅ v0.3 — global order-independent assignment, PR #24 merged |
| B-01 review-input Git tree binding | ✅ Narrow bypass closed on reviewed head via PR #23 |
| Human Review snapshot | ✅ v0.4 selected from `dbda5c3…`; 7 bound paths |
| Human Gold / Oracle decisions | ⛔ `0 / 14` — explicit row decisions still required |
| Gold / Oracle candidates | ⚠️ `AI_PROPOSED_DRAFT` — non-authoritative |
| Harness-validation Pilot | ⛔ Not run; blocked on human reference approval |
| Evidence readiness | ❌ False |
| Evidence Lock | ❌ Not created |
| E0-C Capture Isolation evidence | ❌ Not started |
| E0-T Transfer Isolation evidence | ❌ Not started |
| Architecture Reassessment | ❌ Not reached |
| Production architecture | ❌ Not frozen |
| Production runtime | ❌ Not authorized |
| Ecosystem integration | ❌ Not authorized |

## Current bounded sequence

```text
✅ contracts + fixtures + harness
        ↓
✅ correspondence law v0.3 / order-dependence remediation
        ↓
✅ review-input binding / snapshot v0.4 selected
        ↓
⛔ 14-row human Gold / Oracle review (currently 0/14)
        ↓
only after all required human decisions and a bounded approval change:
PILOT — NOT EVIDENCE
        ↓
pilot fixes
        ↓
evidence lock
        ↓
🛑 STOP
        ↓
only when separately authorized:
E0-C evidence → Capture analysis → E0-T evidence → Transfer analysis
        ↓
🛑 Architecture Reassessment
```

## Capture correspondence remediation

The old sequential greedy association rule could produce a different Capture result when Gold items were reordered. PR #24 replaced it with `e0-correspondence-v0.3`:

1. build the complete eligible Gold × Actual association graph;
2. maximize one-to-one association cardinality;
3. among those assignments, maximize total semantic score;
4. accept only pairs forced in every globally optimal assignment;
5. leave global ambiguity fail-closed.

Permutation regressions are part of the harness tests. This is a measurement-correctness remediation, not human approval or runtime authorization.

## Human reference integrity gate

Issue #9 remains the active semantic gate. Exactly 14 human decision rows require one explicit `ACCEPT`, `REVISE`, or `REJECT` each. No generic continuation instruction, AI recommendation, passing test, hash, receipt, or CI result substitutes for those decisions.

The selected review baseline remains:

- reviewed commit: `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`;
- reviewed tree: `03be5376d592ec9c12299627a6ec0507548363b8`;
- snapshot version: `0.4`;
- snapshot SHA-256: `e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4`;
- bound paths: exactly 7;
- current human decisions: `0 / 14`.

PR #24 did not modify any of those seven review-snapshot paths, so the matcher remediation does not itself create a new human-reference snapshot or human decision.

## Current authority boundary

- GitHub owns observable lifecycle facts such as PR state, merge SHA, and branch HEAD.
- [`project-state.json`](project-state.json) owns selected semantic project state and authorization flags.
- [`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md) owns Experiment 0 semantics.
- [`docs/research/E0_CORRESPONDENCE_LAW_V0_3.md`](docs/research/E0_CORRESPONDENCE_LAW_V0_3.md) owns the current Capture association measurement law.
- This file and [`docs/ai/CURRENT_STATE.md`](docs/ai/CURRENT_STATE.md) are derived explanations.

## Boundary

`CI green ≠ scientific validity · technical binding ≠ human approval · human approval ≠ Pilot authorization · Pilot ≠ Evidence · research ≠ production runtime.`
