# 🔬 Research Index

Velantrim Continuum is a research-first repository. Research artifacts are intentionally separated from human landing pages, AI routing, volatile status and machine-readable project state.

## Canonical Experiment 0 protocol

- [`IDPS_EXPERIMENT_0_PREREGISTRATION.md`](IDPS_EXPERIMENT_0_PREREGISTRATION.md) — canonical Experiment 0 protocol: E0-C Capture Isolation first, E0-T Transfer Isolation second, followed by mandatory Architecture Reassessment.

## Research-facing navigation

- Human deep overview: [`../../RESEARCH_OVERVIEW.md`](../../RESEARCH_OVERVIEW.md)
- AI entrypoint: [`../ai/README.md`](../ai/README.md)
- Machine current state: [`../../project-state.json`](../../project-state.json)
- Human current status: [`../../STATUS.md`](../../STATUS.md)
- [`SMART_CONTEXT_HANDOFF_APPLICATION_NOTE_V0_1.md`](SMART_CONTEXT_HANDOFF_APPLICATION_NOTE_V0_1.md) — application/research bridge mapping a bounded Context Observer, state deltas and successor handoff onto Continuum capture/transfer questions. It is **not** Experiment 0, a selected milestone, Pilot authorization, Evidence, or ecosystem integration authorization.

## Research program order

```text
E0-C Capture Isolation
        ↓
Capture analysis
        ↓
E0-T Transfer Isolation
        ↓
Transfer analysis
        ↓
🛑 Architecture Reassessment
```

This is the stable protocol order, not a statement that any stage is currently running. For current milestone, PR, gate or authorization state, use [`../../project-state.json`](../../project-state.json) and [`../../STATUS.md`](../../STATUS.md).

## Boundary

`docs/research/**` stores research protocols, experiment artifacts and evidence-oriented material. It does not automatically define production architecture or authorize runtime capability.

No production runtime or ecosystem integration should be added merely because candidate mechanisms have been discussed.

Application notes such as Smart Context/Handoff must preserve the current Experiment 0 dependency order and the null hypothesis that a simpler explicit current-state representation may be sufficient.