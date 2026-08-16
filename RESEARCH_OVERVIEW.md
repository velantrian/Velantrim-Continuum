# 📚 Velantrim Continuum — Research Overview

[English](RESEARCH_OVERVIEW.md) · [Русский](RESEARCH_OVERVIEW.ru.md)

## 1. Purpose

Velantrim Continuum is the human-oriented deep overview for the IDPS research line. It explains the conceptual model and research program without replacing the canonical Experiment 0 preregistration.

Formal experiment protocol: [`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md)

## 2. Central shift

The research started from a narrow handoff question:

> How do we transfer AI memory from one context window to another?

That framing was replaced by a stronger one:

> **What must continue to exist when the current inference instance no longer exists?**

Working formulation:

```text
persistent / durable process state
              +
ephemeral, replaceable inference
```

The LLM is treated as a temporary inference worker, not as the durable location of the process.

## 3. Functional continuity, not hidden-state identity

Continuum does not claim that a successor model can recover the exact hidden internal state of its predecessor. The research asks whether a process can continue *functionally* by externalizing only the state that evidence shows is necessary.

Potential continuity dimensions include:

- **Cognitive:** goals, task position, decisions, blockers, unresolved questions, epistemic state.
- **Transactional:** operation intent, dispatch, commit/failure/unknown state, retry safety.
- **Causal:** whether action is based on sufficiently current process state.

Causal/freshness experiments are later work; Experiment 0 isolates Capture and Transfer first.

## 4. Capture vs Transfer

This is the central experimental separation.

```text
Natural interaction
       │
       ▼
🎯 CAPTURE            ← E0-C
       │
       ▼
Structured State
       │
       ▼
📦 TRANSFER           ← E0-T
       │
       ▼
Successor
```

### Capture Failure

Important information never becomes correct structured state.

A later handoff cannot reliably preserve information that was never captured.

### Transfer Failure

The state exists correctly, but is lost, distorted, misattributed, over-promoted or reconstructed incorrectly for the successor.

E0-T therefore uses a common human-authored Oracle State so Capture quality cannot confound the comparison.

## 5. Epistemic preservation

Continuity must preserve epistemic status, not only text.

- **Observed ≠ Inferred**
- **Confidence ≠ Evidence**
- **Contradiction ≠ Corruption**

An unresolved conflict must remain unresolved unless new evidence resolves it. A caution must not silently become a hard prohibition. An absent authorization must not be fabricated.

The E0-C fixture families intentionally include ambiguity, fabrication bait and unresolved contradiction.

## 6. Transactional continuity

External operations create a different class of continuity risk:

```text
OP_INTENT
    ↓
OP_DISPATCHED
    ↓
 ┌────────────┬────────────┬────────────┐
 ▼            ▼            ▼
COMMITTED    FAILED       UNKNOWN
```

`UNKNOWN` matters because a lost response does not prove failure. Blind retry can duplicate an irreversible side effect.

Exact production operation infrastructure is outside Experiment 0.

## 7. Candidate state hypotheses

Earlier conceptual work considered three consequence-of-loss categories. The old numeric labels were removed because `T0`–`T4` are now reserved exclusively for E0-T transfer arms.

Use these non-numeric working names:

- **`CRITICAL_ENFORCEABLE`** — loss or unauthorized mutation may create unacceptable externally relevant consequences.
- **`AUTHORITATIVE_CONTINUITY`** — loss breaks functional continuation without necessarily causing an immediate external safety failure.
- **`RECONSTRUCTIVE_LOSSY`** — material may be compressed or regenerated with bounded quality loss.

These remain **working hypotheses, not a frozen ontology**. Experiment 0 may show that a simpler split is sufficient.

Similarly, event sourcing, ledgers, manifests, capability authority and version-aware commit gates are candidate mechanisms rather than required IDPS architecture.

## 8. Event history vs current state

A simple current-state representation may be enough for ordinary continuation:

```text
state.json
{
  goal: G1,
  step: S4
}
```

An event history can reconstruct the same current projection. Therefore event sourcing must justify itself on capabilities it uniquely improves, such as replay, crash recovery, audit, concurrency or temporal provenance.

Experiment 0 must not give event history automatic credit merely for being more complex.

## 9. Experiment 0

### E0-C — Capture Isolation

Question:

> What can the system correctly transform from natural interaction into structured process state before any handoff?

Conditions:

- `C0` Raw Context — behavior baseline, no external structured state.
- `C1` LLM Extraction — direct structured extraction.
- `C2` Capture Assurance — explicit ambiguity/unresolved handling and bounded clarification only where preregistered.
- `C3` Human-authored Oracle State — upper reference.

Initial fixture families:

1. explicit restriction;
2. conditional restriction;
3. revision / scope change;
4. rejected alternative / negative knowledge;
5. ambiguous caution;
6. fabrication bait;
7. temporal rule;
8. unresolved contradiction.

Primary evaluation is structured-state fidelity, not behavior. C0 remains behavior-only and is not scored as a structured capture arm.

### E0-T — Transfer Isolation

Question:

> If correct process state already exists, what representation is sufficient for functional continuation?

Transfer-arm identifiers are reserved exclusively for these experimental arms:

- `T0` Structured Summary;
- `T1` Canonical Current State (`state.json`);
- `T2` Event Log → Deterministic Projection;
- `T3` Projection + Reconstructive Manifest;
- `T4` Full Context Reference.

All arms begin from the same Oracle State. Representation-generation fidelity is evaluated separately from successor interpretation.

## 10. Primary null hypothesis

> **A simple externally maintained current-state representation may be sufficient.**

The project is falsification-first. Complexity has to earn its place.

Honest possible outcomes include:

- raw context is sufficient for the studied task class;
- Capture is the dominant bottleneck;
- `state.json` is sufficient;
- authoritative state + short narrative is sufficient;
- event history is unnecessary for ordinary continuation;
- a richer substrate is justified by evidence.

## 11. Evaluation discipline

Experiment 0 does not use one weighted Continuity Score.

The hardened preregistration requires:

- one deterministic primary outcome per evaluated capture item plus diagnostic mismatch atoms;
- separate HARD FAIL evaluation bound before evidence;
- fixture-local C2 clarification limits;
- no silent truncation of T4 Full Context;
- separate representation-generation and successor-attribution stages;
- separate cost, latency, storage and verification accounting;
- architecture-level `MATERIAL_GAIN`, `NO_MATERIAL_GAIN` or `TRADEOFF_INCONCLUSIVE` decisions instead of invented percentage thresholds.

The first executable runs are **PILOT — NOT EVIDENCE**. Evidence execution is forbidden until the protocol, schemas, evidence fixtures, Gold/Oracle, evaluator and run configuration are locked by hash.

## 12. Mandatory Architecture Reassessment

After E0-C and E0-T evidence:

```text
Evidence
   ↓
🛑 STOP
   ↓
Architecture Reassessment
   ├── simplify
   ├── redirect research
   └── justify next complexity
```

No production architecture is authorized automatically by completing Experiment 0.

## 13. Current non-claims

Continuum does not currently claim:

- a production-ready durable agent runtime;
- exact cognitive identity across model replacement;
- that event sourcing is required;
- that any state hypothesis is a canonical production ontology;
- that any particular model/database/storage vendor is required;
- that Continuum should already be integrated into Titan, Crystal, Native Kernel or Mentaury;
- novelty claims such as being the first persistent or durable agent system.

## 14. Documentation authority

For current project state, use the repository’s dedicated layers:

- human understanding → `README.md` / this overview;
- AI routing → `docs/ai/README.md`;
- AI contract → `AGENTS.md`;
- exact current state → `project-state.json`;
- human current status → `STATUS.md`;
- formal experiment protocol → `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`;
- external research record → canonical Notion page.

Presentation summarizes truth; it does not create authority.
