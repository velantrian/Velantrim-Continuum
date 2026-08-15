# AGENTS.md — Velantrim Continuum Research Contract

## Repository identity

This repository is **Velantrim Continuum**, the standalone research surface for **IDPS — Inference-Decoupled Process Substrate**.

Human-facing name: **🌎 Velantrim Continuum 🪎**

Status: **Research / Pre-implementation**.

## Current objective

The current objective is not to implement a production runtime.

The current objective is to execute a falsification-first Experiment 0:

1. **E0-C — Capture Isolation**
2. **E0-T — Transfer Isolation**
3. **Mandatory Architecture Reassessment**

The canonical protocol is:

`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`

## Core research rule

> Do not preserve the model. Preserve only what the process demonstrably needs to continue.

And operationally:

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

Those systems may become references in later research only after Experiment 0 and Architecture Reassessment justify mapping or integration.

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

When working on Experiment 0:

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

## Current allowed work

Allowed before Experiment 0 evidence:

- research documentation;
- preregistration refinement before evidence lock;
- deterministic schemas/evaluators needed by the preregistered protocol;
- fixtures and human-authored Gold;
- bounded experiment harness;
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

If repository evidence and an older narrative conflict, prefer current committed evidence and explicitly reconcile the documentation rather than silently rewriting history.
