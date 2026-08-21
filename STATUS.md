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
| Human Gold / Oracle decisions | ✅ `14 / 14` — explicit `ACCEPT` recorded in Issue #9 |
| Historical Gold / Oracle candidates | ⚠️ `AI_PROPOSED_DRAFT` — preserved as non-authoritative history |
| Authoritative Gold / Oracle | ✅ `HUMAN_APPROVED` — versioned approved artifacts materialized |
| Harness-validation Pilot | ⛔ Not run; **NOT AUTHORIZED** by human-reference approval |
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
✅ 14-row human Gold / Oracle review — 14/14 ACCEPT
        ↓
✅ versioned HUMAN_APPROVED Gold / Oracle + approval provenance
        ↓
🛑 STOP — next engineering milestone is not selected by this approval
        ↓
only after a separate owner authorization:
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

Permutation regressions are part of the harness tests. This is a measurement-correctness remediation, not runtime authorization.

## Human reference integrity gate

Issue #9 records exactly 14 canonical human semantic decisions, all `ACCEPT`. The authoritative references are materialized separately from historical AI-proposed candidates:

- approved Capture Gold: `experiments/e0/gold/approved/capture-gold.v0.1.json`;
- approved Transfer Oracle: `experiments/e0/oracle/approved/transfer-oracle.v0.1.json`;
- approval provenance: `experiments/e0/approval/human-reference-approval.v0.2.json`.

The selected review baseline remains:

- reviewed commit: `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`;
- reviewed tree: `03be5376d592ec9c12299627a6ec0507548363b8`;
- snapshot version: `0.4`;
- snapshot SHA-256: `e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4`;
- bound paths: exactly 7;
- human decisions: `14 / 14 ACCEPT`.

No bound review/control path changed between the reviewed baseline and the approval base. Historical candidate artifacts remain `AI_PROPOSED_DRAFT` and byte-bound to the reviewed snapshot.

## Current authority boundary

- GitHub owns observable lifecycle facts such as PR state, merge SHA, and branch HEAD.
- [`project-state.json`](project-state.json) owns selected semantic project state and authorization flags.
- [`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md) owns Experiment 0 semantics.
- [`docs/research/E0_CORRESPONDENCE_LAW_V0_3.md`](docs/research/E0_CORRESPONDENCE_LAW_V0_3.md) owns the current Capture association measurement law.
- The human-reference approval record proves the recorded approval/bindings; it does not grant execution authority.
- This file and [`docs/ai/CURRENT_STATE.md`](docs/ai/CURRENT_STATE.md) are derived explanations.

## Boundary

`CI green ≠ scientific validity · technical binding ≠ human approval · human approval ≠ Pilot authorization · Pilot ≠ Evidence · research ≠ production runtime.`
