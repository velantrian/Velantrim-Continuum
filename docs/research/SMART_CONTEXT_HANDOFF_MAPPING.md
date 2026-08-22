# 🧠 Smart Context / Handoff — Continuum Research Mapping

**Status:** `RESEARCH MAPPING · NON-CANONICAL APPLICATION NOTE · NOT EXPERIMENT 0 · NOT AUTHORIZATION`  
**Repository:** Velantrim Continuum  
**Related design host:** Velantrim Titan research / `Smart Context / Handoff v0.1`

## 1. Why this mapping exists

Smart Context / Handoff is a concrete application hypothesis for the broader Continuum question:

> What explicit durable state is sufficient for functional continuation after a replaceable inference/context instance disappears?

The application imagines a normal working AI plus a bounded read-side Context Observer that maintains candidate process state and can later generate a compact successor package.

This note records only the conceptual relationship. It does **not** import Titan implementation into Continuum, change Experiment 0, select a new milestone, or authorize ecosystem integration.

## 2. Application shape

```text
👤 Human ↔ 🤖 Working AI
                │
                │ observable interaction/events
                ▼
         🧩 Context Observer
                │
                ▼
          candidate Process State
                │
                ▼
       📦 SuccessorContextPack
                │
                ▼
       🤖 successor inference
                │
                ▼
      continuation evaluation
```

Candidate state may include:

- active goal and task position;
- explicit decisions and rejected/deferred paths;
- constraints and prohibitions;
- blockers and unresolved questions;
- relevant artifact/evidence references;
- last meaningful state transition;
- next bounded step;
- explicit unknown/contested state.

## 3. Mapping to Continuum failure decomposition

Smart Context must not collapse Capture and Transfer into one opaque “summary quality” score.

```text
Interaction
    │
    ▼
🎯 CAPTURE
    │  Was important process state represented correctly?
    ▼
Candidate durable state
    │
    ▼
📦 TRANSFER / HANDOFF
    │  Was captured state preserved without loss/distortion/revival?
    ▼
Successor
```

Examples:

- Observer never records an explicit “do not publish” restriction → **Capture Failure**.
- Restriction was recorded but omitted from the successor pack → **Transfer Failure**.
- Restriction survives correctly but successor reasons badly → **Reasoning Failure**, not handoff failure.
- Successor acts on a stale external PR state → potential **Causal/Freshness Failure**.
- Handoff silently grants action permission → **Authorization Failure**.

## 4. StateDelta as an application hypothesis

Smart Context proposes tracking meaningful transition:

```text
S(t-1) → S(t)
```

This is useful because continuation depends not only on a static description but on knowing what changed, what was superseded, and what remains open.

However, Continuum does not adopt `StateDelta` as a required substrate mechanism through this note. Experiment 0 must remain able to show that a simpler current-state representation is sufficient.

## 5. SuccessorContextPack mapping

A `SuccessorContextPack` is an application-level candidate transfer artifact. It is not automatically a new Experiment 0 transfer arm and does not modify T0–T4.

A future post-reassessment experiment could compare it against simpler baselines only if separately selected.

Candidate properties:

- minimal still-useful state;
- explicit provenance/source class where needed;
- preserved ambiguity and contested status;
- no hidden chain-of-thought requirement;
- obsolete/superseded material excluded or marked;
- external-state references revalidated before protected action;
- bounded size and deterministic/replayable serialization where practical.

## 6. Evaluation questions

A later explicitly authorized study could ask:

- Did the successor preserve the active goal?
- Did it preserve explicit prohibitions and constraints?
- Did it retain accepted/rejected decisions without inversion?
- Did it retain open loops and blockers?
- Did it preserve ambiguity instead of inventing resolution?
- Did it avoid reviving superseded state?
- Did it correctly distinguish user statement, evidence, external state and model inference?
- Did it continue the task correctly with less context than the raw transcript?
- Is a simple `state.json`-like baseline equally good or better?

No weighted single continuity score is introduced by this note.

## 7. Hard boundaries

```text
Smart Context mapping != Experiment 0 change
Context Observer != durable authority
observer summary != fact
handoff != Canon
context survival != identity continuity
second AI != independent human reviewer
successor package != action authorization
Titan research != Continuum ecosystem-integration approval
Pilot != Evidence
```

The Observer/handoff path must not mutate external systems, grant authority, or convert inferred state into confirmed state merely by being persistent.

## 8. Current Continuum state remains unchanged

This research mapping does not change any current state or gate:

- Human Reference remains approved/closed according to current owning state.
- Pilot remains separately owner-gated and is not authorized by this note.
- Evidence Lock is not created by this note.
- E0-C / E0-T Evidence are not started or authorized by this note.
- Experiment 0 protocol order remains unchanged.
- Production architecture/runtime remain unapproved.
- Ecosystem integration remains unapproved.

No `project-state.json`, `STATUS.md`, or `docs/ai/CURRENT_STATE.md` update is warranted because this document creates no state transition.

## 9. Return trigger

Return to this application mapping only after at least one of these occurs:

1. Experiment 0 and mandatory Architecture Reassessment provide evidence relevant to minimum sufficient continuation state; or
2. a separate owner decision explicitly authorizes a bounded Smart Context research experiment that does not contaminate Experiment 0; or
3. a concrete Titan shadow prototype needs a Continuum-defined falsifiable evaluation question without changing Continuum's current program.

Until then, this is preserved research context only.
