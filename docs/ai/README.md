# 🤖 Velantrim Continuum — AI Entry Point

`document_role: ai_entrypoint`

This document is the deterministic starting point for AI agents, automated auditors, coding assistants and repository-aware models.

Do **not** reconstruct current project truth from the human-facing README alone.

## Authoritative read order

1. `docs/ai/README.md` — routing and interpretation rules.
2. `AGENTS.md` — repository contract, scope boundaries and experimental discipline.
3. `project-state.json` — selected semantic project state and authorization flags.
4. `docs/ai/CURRENT_STATE.md` — derived plain-language explanation of volatile current state.
5. `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` — canonical Experiment 0 protocol.
6. Task-specific fixtures, evaluators, results or evidence when they exist.
7. `RESEARCH_OVERVIEW.md` and `README.md` for human-oriented conceptual context.

## Authority model

Different fact classes have different owners:

```text
GitHub API / commit graph
        ├── PR lifecycle / merge SHA / branch HEAD
        │
project-state.json
        ├── selected semantic project state / authorization flags
        │
AGENTS.md
        ├── repository scope / behavior contract
        │
formal research protocol
        ├── Experiment 0 semantics
        │
committed evidence
        ├── what was actually observed
        │
STATUS / CURRENT_STATE
        ├── derived volatile explanations
        │
README / Overview / Notion
        └── human-oriented or external research record
```

`project-state.json` is **not** an independent owner of facts that GitHub can observe directly. When a committed lifecycle expectation and live GitHub disagree, report drift and reconcile it through a reviewable state change. Do not infer a new milestone or authorization from GitHub lifecycle alone.

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
- a merged documentation PR selects the next engineering milestone;
- Experiment 0 completion automatically authorizes production runtime work;
- Continuum is already approved for integration into Titan, Crystal, Native Kernel or Mentaury.

## Current canonical sequence

```text
Research foundation         ✅ merged
Documentation architecture  ✅ PR #2 merged
Next bounded milestone      ⏳ explicit selection pending
Experiment 0 harness        ❌ not started
E0-C evidence               ❌ not started
E0-T evidence               ❌ not started
Architecture Reassessment   ❌ not reached
Production architecture     ❌ not frozen
Production runtime          ❌ not authorized
```

The research sequence remains:

`E0-C Capture Isolation → E0-T Transfer Isolation → mandatory Architecture Reassessment`

That sequence does not itself authorize the next engineering milestone.

## Change classification

Before changing documentation, classify the change:

### `STRUCTURAL_CHANGE`

Changes stable conceptual meaning, experiment semantics, authority boundaries or documentation architecture.

Update affected formal/AI/machine/human surfaces consistently.

When a structural change affects a bilingual human surface, update its EN/RU counterpart in the same PR unless the PR explicitly records why parity is intentionally deferred.

### `STATE_CHANGE`

Changes current milestone, current gate, authorization, blocker or execution status without changing the conceptual model.

Update `project-state.json`, `docs/ai/CURRENT_STATE.md` and `STATUS.md` as one reviewable state bundle. Update other surfaces such as this AI router only when their state/lifecycle wording is actually affected.

### `EVIDENCE_ONLY`

Adds a test run, report, reproduction, result bundle or PR evidence without changing semantic project state.

Update evidence/history surfaces. Do not manufacture a state transition.

## State-control-plane checks

Repository automation may verify:

- live GitHub lifecycle against the committed lifecycle expectation;
- provenance lineage from a reviewed base commit to current `main`;
- atomic updates of `project-state.json` with declared always-derived volatile state surfaces.

Automation must **not** choose the next milestone, start Experiment 0, authorize runtime work, or change research conclusions.

## Presentation never creates authority

- README may summarize, visualize and link.
- `STATUS.md` and `docs/ai/CURRENT_STATE.md` may summarize current state.
- machine state may encode a selected semantic state.
- evidence may justify a conclusion.

None of these may silently rewrite the formal experiment protocol or authorize production capability.

## External record

Canonical Notion research page:

`https://app.notion.com/p/3bcac84d054781ebb7b3cbd281bdcdc6`

The external record is controlled narrative/record, not an independent owner of GitHub lifecycle facts or experiment semantics. Reconcile it explicitly after material repository state changes.
