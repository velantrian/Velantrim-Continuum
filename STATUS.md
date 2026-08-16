# 📊 Velantrim Continuum — Current Status

**Project:** 🌎 Velantrim Continuum 🪎  
**Technical name:** IDPS — Inference-Decoupled Process Substrate  
**Status:** Research / Pre-implementation

## Current position

| Area | State |
|---|---|
| Research foundation | ✅ Merged |
| Documentation Architecture v1 | ✅ PR #2 merged |
| Selected milestone | ✅ `EXPERIMENT_0_EVALUATION_CONTRACT_AND_HARNESS_READINESS` |
| Preregistration hardening | ✅ PR #5 merged |
| Experimental data contracts / fixtures | ✅ PR #6 merged |
| Experiment 0 harness | 🔄 Implementation started |
| Deterministic evaluator | 🔄 Implemented in current harness work |
| Human-authored Gold / Oracle | ⛔ Approval required; AI candidates are non-authoritative |
| Harness-validation pilot | ⛔ Not run; blocked on human reference approval |
| Evidence readiness | ❌ False |
| Evidence lock | ❌ None |
| E0-C Capture Isolation evidence | ❌ Not started |
| E0-T Transfer Isolation evidence | ❌ Not started |
| Architecture Reassessment | ❌ Not reached |
| Production architecture | ❌ Not frozen |
| Production runtime | ❌ Not authorized |
| Ecosystem integration | ❌ Not authorized |

## Current bounded sequence

```text
✅ milestone selection
        ↓
✅ preregistration hardening
        ↓
✅ schemas + F1–F8 fixtures + transfer scenarios
        ↓
🔄 deterministic evaluator + minimal harness
        ↓
⛔ human experimenter approval of Gold / Oracle
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

The repository contains AI-proposed candidate Capture Gold and Transfer Oracle solely as review material. They are explicitly non-authoritative and must not be used as Experiment 0 truth until a human experimenter reviews and approves a versioned reference artifact.

The harness/evidence-lock machinery is designed to fail closed while this status is not `HUMAN_APPROVED`.

## Current authority boundary

- GitHub owns observable lifecycle facts such as PR state, merge SHA and branch HEAD.
- [`project-state.json`](project-state.json) owns semantic project state and authorization flags.
- [`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md) owns Experiment 0 semantics.
- This file and [`docs/ai/CURRENT_STATE.md`](docs/ai/CURRENT_STATE.md) are derived explanations.

## Boundary

Harness implementation does **not** mean E0-C or E0-T evidence has begun. No production architecture, runtime, event-sourcing requirement, state-tier canon or ecosystem integration is authorized.
