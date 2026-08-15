# 🔬 Research Index

Velantrim Continuum is currently a research-first repository. Research artifacts are intentionally separated from human landing pages, AI routing, volatile status and machine-readable project state.

## Current canonical artifact

- [`IDPS_EXPERIMENT_0_PREREGISTRATION.md`](IDPS_EXPERIMENT_0_PREREGISTRATION.md) — canonical Experiment 0 protocol: E0-C Capture Isolation first, E0-T Transfer Isolation second, followed by mandatory Architecture Reassessment.

## Research-facing navigation

- Human deep overview: [`../../RESEARCH_OVERVIEW.md`](../../RESEARCH_OVERVIEW.md)
- AI entrypoint: [`../ai/README.md`](../ai/README.md)
- Machine current state: [`../../project-state.json`](../../project-state.json)
- Human current status: [`../../STATUS.md`](../../STATUS.md)

## Current status

```text
Conceptual decomposition   ✅ complete enough to test
Research foundation        ✅ merged
Documentation architecture 🟡 current proposed change
Production architecture    ⛔ not frozen
Experiment 0 harness       ❌ not started
E0-C Capture Isolation     → future first evidence stage
E0-T Transfer Isolation    → future second evidence stage
Architecture Reassessment  → mandatory stop gate
```

## Boundary

`docs/research/**` stores research protocols, future experiment artifacts and evidence-oriented material. It does not automatically define production architecture or authorize runtime capability.

The status block above is a point-in-time snapshot, not the canonical source. It can go stale — always defer to [`project-state.json`](../../project-state.json) / [`STATUS.md`](../../STATUS.md) for current milestone/gate state.

No production runtime or ecosystem integration should be added merely because candidate mechanisms have been discussed.
