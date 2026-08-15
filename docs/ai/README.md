# 🤖 Velantrim Continuum — AI Entry Point

`document_role: ai_entrypoint`

This document is the deterministic starting point for AI agents, automated auditors, coding assistants and repository-aware models.

Do **not** reconstruct current project truth from the human-facing README alone.

## Authoritative read order

1. `docs/ai/README.md` — routing and interpretation rules.
2. `AGENTS.md` — repository contract, scope boundaries and experimental discipline.
3. `project-state.json` — machine-readable current project state.
4. `docs/ai/CURRENT_STATE.md` — human-readable explanation of volatile current state.
5. `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` — canonical Experiment 0 protocol.
6. Task-specific fixtures, evaluators, results or evidence when they exist.
7. `RESEARCH_OVERVIEW.md` and `README.md` for human-oriented conceptual context.

## Current authority model for documentation

```text
project-state.json
        │
        ├── exact volatile project state
        │
AGENTS.md
        ├── repository scope / behavior contract
        │
formal research protocol
        ├── experiment semantics
        │
committed evidence
        ├── what was actually observed
        │
README / Overview
        └── human-oriented explanation
```

If surfaces conflict, do not silently choose the most readable one. Identify the conflict, prefer the more task-authoritative committed source, and reconcile documentation explicitly.

## Never infer

Never infer any of the following without explicit evidence:

- `preregistered` means `empirically_supported`;
- `implemented` means `authorized`;
- `tested` means `production_ready`;
- green CI means the research hypothesis was accepted;
- an event log is required by IDPS;
- T1/T2/T3 is the final ontology;
- a historical checkpoint is current `main`;
- a bot review is equivalent to independent human reproduction;
- Notion narrative is newer than current committed repository state;
- a human-friendly README creates authority;
- Experiment 0 completion automatically authorizes production runtime work;
- Continuum is already approved for integration into Titan, Crystal, Native Kernel or Mentaury.

## Current canonical sequence

```text
Research foundation         ✅ merged
Documentation architecture  🟡 current proposed change
Experiment 0 harness        ❌ not started
E0-C evidence               ❌ not started
E0-T evidence               ❌ not started
Architecture Reassessment   ❌ not reached
Production architecture     ❌ not frozen
Production runtime          ❌ not authorized
```

The sequence after documentation work remains:

`E0-C Capture Isolation → E0-T Transfer Isolation → mandatory Architecture Reassessment`

## Change classification

Before changing documentation, classify the change:

### `STRUCTURAL_CHANGE`

Changes stable conceptual meaning, experiment semantics, authority boundaries or documentation architecture.

Update affected formal/AI/machine/human surfaces consistently.

### `STATE_CHANGE`

Changes current milestone, current gate, authorization, blocker or execution status without changing the conceptual model.

Update `project-state.json`, `docs/ai/CURRENT_STATE.md`, `STATUS.md`, and only the minimal human-facing status surface required.

### `EVIDENCE_ONLY`

Adds a test run, report, reproduction, result bundle or PR evidence without changing semantic project state.

Update evidence/history surfaces. Do not manufacture a state transition.

## Presentation never creates authority

- README may summarize, visualize and link.
- `STATUS.md` may summarize current state.
- machine state may encode a selected current state.
- evidence may justify a conclusion.

None of these may silently rewrite the formal experiment protocol or authorize production capability.

## External record

Canonical Notion research page:

`https://app.notion.com/p/3bcac84d054781ebb7b3cbd281bdcdc6`

Repository truth and external record should be reconciled when state changes materially.
