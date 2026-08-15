# 🌎 Velantrim Continuum 🪎

> **IDPS Research — Inference-Decoupled Process Substrate**  
> Research / Pre-implementation

Velantrim Continuum is a standalone research line investigating how a long-lived AI process can continue functioning when any particular LLM inference instance, context window, model family, or runtime session disappears or is replaced.

The central idea is deliberately simple:

> **Do not preserve the model. Preserve only what the process demonstrably needs to continue.**

This repository does **not** assume that a complex runtime is necessary. The primary null hypothesis is that a much simpler approach — potentially careful capture plus a canonical `state.json` — may already be sufficient.

---

## 🧬 Core model

```text
🤖 inference/context disappears
            ↓
📚 required process state remains
            ↓
🤖 new inference instance attaches
            ↓
▶ functional process continuation
```

The target is **functional continuity**, not literal reconstruction of hidden model cognition.

A replaceable inference instance may change, crash, reset, exhaust its context, or be swapped for another model while the long-lived process preserves only the externally represented state proven necessary for continuation.

## 🎯 Research question

What properties of a long-lived AI process must exist outside replaceable inference so that the process can continue correctly across context exhaustion, reset, crash, restart, or model replacement?

The program explicitly separates continuity failures into different mechanisms:

```text
Input / Environment
        │
        ▼
🎯 CAPTURE
        │
        ▼
📚 PROCESS STATE
        │
        ▼
📦 TRANSFER / RECONSTRUCTION
        │
        ▼
🤖 INFERENCE
        │
        ▼
🔐 AUTHORITY / POLICY
        │
        ▼
⚙ EXECUTION
        │
        ▼
🌍 WORLD

Parallel risk: ⏱ causal / freshness failure
```

This decomposition matters because a handoff can appear to fail for very different reasons: the state may never have been captured, it may have been lost during transfer, the successor may reason incorrectly, an authorization boundary may fail, or the successor may simply be stale.

## 🧠 Continuity dimensions

Continuity is currently studied across three working dimensions:

- **Cognitive continuity** — goals, task position, decisions, blockers, unresolved questions, epistemic state and relevant rationale.
- **Transactional continuity** — intent, dispatch, commit/failure/unknown state of external operations and protection against unsafe retries.
- **Causal continuity** — whether the inference instance acts against sufficiently current process state.

These are research dimensions, not a claim that the final architecture must expose exactly these abstractions.

## 🔬 Experiment 0

The next stage is intentionally experimental rather than architectural.

### E0-C — Capture Isolation

Question:

> What can the system correctly transform from natural interaction into structured process state before any handoff occurs?

Candidate conditions:

- `C0` — Raw Context
- `C1` — LLM Extraction
- `C2` — Capture Assurance
- `C3` — Human-authored Oracle State

Initial fixture families include explicit restrictions, conditional restrictions, revisions, rejected alternatives, ambiguous cautions, fabrication bait, temporal rules and unresolved contradictions.

### E0-T — Transfer Isolation

Question:

> If correct process state already exists, what representation is sufficient for a successor to continue functionally?

Candidate arms:

- `T0` — Structured Summary
- `T1` — Canonical Current State (`state.json`)
- `T2` — Event Log → Deterministic Projection
- `T3` — Projection + Reconstructive Manifest
- `T4` — Full Context Reference, where technically possible

All transfer arms must start from the **same human-authored Oracle State** so capture quality cannot confound transfer results.

## ⚔️ Primary null hypothesis

> **A simple externally maintained current-state representation may be sufficient.**

A result where `state.json` performs as well as a more complex mechanism is a **successful research outcome**. The project is falsification-first: complexity has to earn its place.

## 🛑 Mandatory reassessment gate

```text
E0-C
  ↓
Capture analysis
  ↓
E0-T
  ↓
Transfer analysis
  ↓
🛑 STOP
  ↓
🧠 Architecture Reassessment
```

Only after this gate should the project decide whether to:

- simplify to a small current-state representation;
- redirect toward Capture Assurance research;
- add reconstructive narrative;
- investigate durability/recovery mechanisms;
- justify event sourcing;
- or continue toward a fuller IDPS substrate.

## 🚫 Deliberately not frozen

The repository does **not** currently freeze:

- storage backend;
- event alphabet;
- database technology;
- authority schema;
- exact state tier ontology;
- model vendor or family;
- number of models;
- role-to-model mapping;
- context-pressure thresholds;
- embedding strategy;
- production FSM;
- long-horizon benchmark;
- integration destination inside the broader Velantrim ecosystem.

## 🧭 Ecosystem boundary

Velantrim Continuum is currently standalone research. It must not be automatically integrated into Titan, Crystal, Native Kernel, Mentaury, or other Velantrim projects before Experiment 0 and the subsequent Architecture Reassessment establish what is actually justified.

Related systems may be used as references later, but this repository is intentionally isolated so experimental failures can be attributed to Continuum hypotheses rather than to the complexity of another runtime.

## 📄 Canonical next artifact

The immediate research artifact is:

[`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md)

It locks the Experiment 0 protocol before evidence runs begin.

## 🔗 Research record

Canonical Notion research page: **🌎 Velantrim Continuum — IDPS Research 🪎**  
https://app.notion.com/p/3bcac84d054781ebb7b3cbd281bdcdc6

---

### 🧬 One-line formulation

**Measure Capture → Measure Transfer → Find minimum sufficient state → Reassess architecture.**
