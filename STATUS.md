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
| Human Gold / Oracle decisions | ✅ `14 / 14 ACCEPT` |
| Human-reference gate | ✅ `CLOSED` by bounded human-reference approval |
| Historical Gold / Oracle candidates | ⚠️ `AI_PROPOSED_DRAFT` — preserved, non-authoritative |
| Approved Capture Gold | ✅ `capture-gold.v0.1.json` — `HUMAN_APPROVED` |
| Approved Transfer Oracle | ✅ `transfer-oracle.v0.1.json` — `HUMAN_APPROVED` |
| Harness-validation Pilot | ⛔ `NOT_AUTHORIZED`; not run |
| Pilot package authorization | ⛔ `null`; no exact manifest path/SHA authorized |
| Evidence readiness | ❌ False |
| Evidence Lock | ❌ Not created |
| E0-C Capture Isolation evidence | ❌ Not started / not authorized |
| E0-T Transfer Isolation evidence | ❌ Not started / not authorized |
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
✅ 14 / 14 explicit human ACCEPT decisions
        ↓
✅ authoritative versioned Gold / Oracle + approval provenance
        ↓
🛑 separate owner authorization still required
        ↓
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

## Human reference integrity gate

Issue #9 records all 14 canonical human semantic decisions as explicit `ACCEPT`. The authoritative reference material is represented by distinct, versioned files outside `candidates/`:

- `experiments/e0/gold/approved/capture-gold.v0.1.json`;
- `experiments/e0/oracle/approved/transfer-oracle.v0.1.json`;
- `experiments/e0/approval/human-reference-approval.v0.2.json`.

The historical candidate files remain unchanged as `AI_PROPOSED_DRAFT`. Human approval materializes reference truth for Experiment 0; it does not create runtime authority.

The reviewed baseline remains:

- reviewed commit: `dbda5c364f5bc76eb033f90031ce03bf3f4f29e9`;
- reviewed tree: `03be5376d592ec9c12299627a6ec0507548363b8`;
- snapshot version: `0.4`;
- snapshot SHA-256: `e44650d54a4dd007a1c2039785f31ed5ab947877d5cd51000e01062b17016da4`;
- bound paths: exactly 7;
- human decisions: `14 / 14 ACCEPT`.

Later commits through the approval base do not modify those seven review-snapshot paths, so the approved reference remains bound to the exact reviewed Git tree entries and bytes.

## Current authority boundary

- GitHub owns observable lifecycle facts such as PR state, merge SHA, Issue state, and branch HEAD.
- [`project-state.json`](project-state.json) owns selected semantic project state and authorization flags. A future bounded Pilot requires both `experiment_0_pilot_status = AUTHORIZED_BOUNDED_PILOT` and an exact canonical manifest path/SHA package binding; the current package authorization slot is `null`.
- [`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md) owns Experiment 0 semantics.
- [`docs/research/E0_CORRESPONDENCE_LAW_V0_3.md`](docs/research/E0_CORRESPONDENCE_LAW_V0_3.md) owns the current Capture association measurement law.
- `human-reference-approval.v0.2.json` records explicit human-reference approval provenance and exact reviewed bindings.
- This file and [`docs/ai/CURRENT_STATE.md`](docs/ai/CURRENT_STATE.md) are derived explanations.

## Boundary

`Human reference approved ≠ Pilot authorized · Pilot package slot present ≠ Pilot authorized · Pilot ≠ Evidence · Evidence Lock ≠ Evidence authorization · CI green ≠ scientific validity · research ≠ production runtime.`
