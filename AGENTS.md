# AGENTS.md — Velantrim Continuum Research Contract

## Repository identity

This repository is **Velantrim Continuum**, the standalone research surface for **IDPS — Inference-Decoupled Process Substrate**.

Human-facing name: **🌎 Velantrim Continuum 🪎**

Status: **Research / Pre-implementation**.

## Mandatory AI start point

Before doing repository work, read in this order:

1. `docs/ai/README.md`
2. `AGENTS.md`
3. `project-state.json`
4. `docs/ai/CURRENT_STATE.md`
5. the task-specific formal protocol / evidence

Do not use the human-facing README as the sole source of current project truth.

## Current objective

The current research sequence is:

1. **E0-C — Capture Isolation**
2. **E0-T — Transfer Isolation**
3. **Mandatory Architecture Reassessment**

The canonical protocol is:

`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`

Documentation Architecture v1 is complete via PR #2. That merge did **not** select the next engineering milestone and did not authorize Experiment 0 execution. The next bounded engineering milestone must still be selected explicitly.

## Core research rule

> Do not preserve the model. Preserve only what the process demonstrably needs to continue.

Operationally:

> Measure Capture → Measure Transfer → Find minimum sufficient state → Reassess architecture.

## Primary null hypothesis

A simple externally maintained current-state representation, including a possible `state.json` baseline, may be sufficient.

Do not favor architectural complexity merely because a richer design has already been discussed.

## Hard scope boundary

Do **not** automatically import or implement architecture from:

- Velantrim Titan;
- Velantrim Crystal;
- Velantrim Native Kernel;
- Mentaury / Mentaury Soul;
- other Velantrim experimental projects.

Those systems may become references later only after Experiment 0 and Architecture Reassessment justify mapping or integration.

## Not frozen

Do not treat the following as settled architecture:

- T1/T2/T3 state tiers;
- event sourcing / ledger;
- reconstructive manifest;
- capability-based authority schema;
- storage backend;
- event alphabet;
- database technology;
- model count;
- role-to-model mapping;
- model provider;
- embeddings strategy;
- context-pressure thresholds;
- production FSM;
- ecosystem integration destination.

These are candidate mechanisms or future research questions.

## Experimental discipline

When Experiment 0 work is explicitly authorized:

- keep Capture and Transfer experimentally isolated;
- use human-authored Gold / Oracle State;
- preserve ambiguity and contested status conservatively;
- avoid LLM judges as the primary truth source for deterministic fields;
- do not invent numeric acceptance thresholds without evidence;
- do not collapse results into one weighted continuity score;
- record hard failures separately;
- keep probe forks independent to avoid contamination;
- version any protocol change that occurs after runs begin;
- invalidate and rerun affected comparisons if a preregistered protocol changes materially.

## Authority model

Authority is fact-class specific:

- **GitHub:** observable repository lifecycle facts such as PR state, merge SHA, commit ancestry and branch HEAD.
- **Machine semantic state:** `project-state.json` for selected milestone/state and authorization flags.
- **Formal research:** `docs/research/**` for experiment semantics and preregistered rules.
- **Derived status:** `STATUS.md` and `docs/ai/CURRENT_STATE.md`.
- **External research record:** canonical Notion page.

`project-state.json` does not override live GitHub facts, and GitHub lifecycle does not select semantic milestones or authorizations.

Presentation never creates authority.

## Documentation architecture

The repository separates one project truth into different representations:

- **Human:** `README.md`, `README.ru.md`, `RESEARCH_OVERVIEW*.md`;
- **AI:** `docs/ai/README.md`, this file, `docs/ai/CURRENT_STATE.md`;
- **Machine semantic state:** `project-state.json`;
- **Formal research:** `docs/research/**`;
- **Status:** `STATUS.md`;
- **Evidence/history:** future committed evidence, results, ADRs or checkpoints when they actually exist.

## Documentation change classification

Before changing documentation, classify the change:

### `STRUCTURAL_CHANGE`

Changes conceptual meaning, formal experiment semantics, authority boundaries, or the documentation architecture itself.

Reconcile affected formal, AI, machine and human surfaces.

When a structural change affects a bilingual human surface, update the paired EN/RU surface in the same PR unless parity is explicitly and reviewably deferred.

### `STATE_CHANGE`

Changes current milestone, gate, blocker or authorization without changing conceptual meaning.

Update the always-derived volatile state bundle together:

- `project-state.json`;
- `docs/ai/CURRENT_STATE.md`;
- `STATUS.md`.

Update `docs/ai/README.md` or other structural surfaces only when their wording is affected by the state transition.

### `EVIDENCE_ONLY`

Adds evidence without changing semantic state.

Do not manufacture a project-state transition merely because new evidence exists.

## State-control-plane invariant

Repository validation may independently check:

1. live GitHub lifecycle against committed lifecycle expectations;
2. provenance lineage — a reviewed base may be identical to or an ancestor of current `main`;
3. state-bundle integrity for primary and always-derived volatile state files.

A later README-only, translation-only or engineering-only commit is not a state failure merely because `main` advances.

Automation may detect inconsistency. It may not choose a milestone, start Experiment 0, authorize production runtime, or change an experimental conclusion.

## Canonical `never infer` rules

The canonical and complete `never infer` list is maintained in [`docs/ai/README.md`](docs/ai/README.md#never-infer).

Treat that list as part of this repository contract. Do not duplicate a second independently maintained copy here; if the rule set changes, update the AI router and any affected machine/formal surfaces consistently.

## Current allowed work

Allowed before Experiment 0 evidence:

- research documentation;
- preregistration refinement before evidence lock;
- deterministic schemas/evaluators needed by an explicitly selected bounded milestone;
- fixtures and human-authored Gold when that milestone is authorized;
- bounded experiment harness when explicitly authorized;
- reproducibility and cost instrumentation;
- tests for the experiment harness.

Not allowed merely by default:

- production agent runtime;
- production authority system;
- ecosystem-wide integration;
- claims that IDPS is a proven architecture;
- claims of novelty such as “first durable AI agent system”.

## Canonical external research record

Notion page:

https://app.notion.com/p/3bcac84d054781ebb7b3cbd281bdcdc6

If repository evidence and an older narrative conflict, prefer the fact owner appropriate to the claim, report the conflict, and reconcile documentation explicitly rather than silently rewriting history.
