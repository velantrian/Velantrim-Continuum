# 📊 Velantrim Continuum — Current Status

**Project:** 🌎 Velantrim Continuum 🪎  
**Technical name:** IDPS — Inference-Decoupled Process Substrate  
**Status:** Research / Pre-implementation

## Current position

| Area | State |
|---|---|
| Research foundation | ✅ Merged |
| Foundation PR | ✅ #1 merged |
| Foundation merge SHA | `e14cf46f96724dda933ce647b46f72fc4866dc7c` |
| Documentation Architecture v1 | ✅ PR #2 merged |
| Documentation PR #2 merge SHA | `533cc6abcf59d20f7a273098f043784c95421711` |
| Next bounded engineering milestone | ✅ `EXPERIMENT_0_EVALUATION_CONTRACT_AND_HARNESS_READINESS` selected |
| Current workstream | 🔄 Active — evaluation contract / harness readiness only |
| Experiment 0 harness | ❌ Not started |
| E0-C Capture Isolation | ❌ Not started |
| E0-T Transfer Isolation | ❌ Not started |
| Architecture Reassessment | ❌ Not reached |
| Production architecture | ❌ Not frozen |
| Production runtime | ❌ Not authorized |
| Ecosystem integration | ❌ Not authorized |

## Current research sequence

```text
Documentation Architecture v1
        ↓
✅ PR #2 merged
        ↓
✅ next bounded milestone explicitly selected
        ↓
EXPERIMENT_0_EVALUATION_CONTRACT_AND_HARNESS_READINESS
        ↓
preregistration hardening
        ↓
experimental data contracts + evaluator + minimal harness
        ↓
PILOT — NOT EVIDENCE
        ↓
evidence lock
        ↓
🛑 STOP
        ↓
only when separately authorized:
E0-C Capture Isolation evidence
        ↓
Capture analysis
        ↓
E0-T Transfer Isolation evidence
        ↓
Transfer analysis
        ↓
🛑 Architecture Reassessment
```

## Current authority boundary

- GitHub owns observable GitHub lifecycle facts such as PR state, merge SHA and branch HEAD.
- [`project-state.json`](project-state.json) owns selected semantic project state and authorization flags.
- The formal Experiment 0 preregistration owns experiment semantics.
- This file and [`docs/ai/CURRENT_STATE.md`](docs/ai/CURRENT_STATE.md) are derived explanations and must be reconciled with semantic state.

## Current canonical sources

- AI entrypoint: [`docs/ai/README.md`](docs/ai/README.md)
- AI contract: [`AGENTS.md`](AGENTS.md)
- Semantic machine state: [`project-state.json`](project-state.json)
- AI current-state explanation: [`docs/ai/CURRENT_STATE.md`](docs/ai/CURRENT_STATE.md)
- Formal Experiment 0 protocol: [`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md)
- Deep human overview: [`RESEARCH_OVERVIEW.md`](RESEARCH_OVERVIEW.md)

## Boundary

Selecting `EXPERIMENT_0_EVALUATION_CONTRACT_AND_HARNESS_READINESS` authorizes only the bounded preparation needed to make Experiment 0 executable, reproducible and falsifiable: preregistration hardening, experimental data contracts, deterministic evaluation, minimal harness implementation, non-evidence pilot validation and evidence lock.

It does **not** start the Experiment 0 harness by itself, start E0-C or E0-T evidence, freeze production architecture, authorize production runtime, require event sourcing, make state tiers canonical, or authorize ecosystem integration.
