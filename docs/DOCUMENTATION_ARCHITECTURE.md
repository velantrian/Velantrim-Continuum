# 📚 Velantrim Continuum — Documentation Architecture v1

> **Scope:** documentation structure and presentation only.  
> **Non-authority:** this document does not change Experiment 0 semantics, project authorization, runtime scope, Pilot, Evidence Lock, or Evidence status.

## 🎯 Purpose

Continuum documentation is intentionally split into several representations of the **same project truth**.

```text
                       🧬 CONTINUUM PROJECT TRUTH
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
          👤 HUMAN VIEW      🤖 AI / AGENT     ⚙ MACHINE STATE
          README /           docs/ai/           project-state.json
          OVERVIEW           AGENTS.md
                │
                └─────────────────┬─────────────────┘
                                  ▼
                           🔬 EVIDENCE / HISTORY
```

Different views may use different presentation styles, but they must not create different truths.

## 👤 Human view

Primary surfaces:

- `README.md` / `README.ru.md` — short landing page and stable mental model;
- `RESEARCH_OVERVIEW.md` / `RESEARCH_OVERVIEW.ru.md` — deeper conceptual explanation;
- `docs/APPLICABILITY.md` / `docs/APPLICABILITY.ru.md` — practical significance, applicability, and boundaries;
- `STATUS.md` — compact current-state explanation.

Human documentation may use:

- short narrative explanations;
- examples;
- diagrams;
- mindmaps;
- emojis as visual grammar;
- comparison tables;
- reading paths.

It must not manufacture authorization or override formal protocols.

## 🤖 AI / agent view

Primary surfaces:

- `docs/ai/README.md` — deterministic AI entry point and routing rules;
- `AGENTS.md` — repository working contract;
- `docs/ai/CURRENT_STATE.md` — volatile state explanation;
- `docs/ai/AUDIT_AND_FUTURE_WORK.md` — durable audit/future-work ledger;
- task-specific protocols, contracts, fixtures, and evidence.

AI-facing documentation should prefer:

- exact vocabulary;
- authoritative read order;
- explicit invariants;
- forbidden inferences;
- exact scope boundaries;
- machine-checkable references where available.

Decorative narrative must never be required to recover an authorization or protocol rule.

## ⚙ Machine-readable state

Primary surface:

- `project-state.json`

Machine state exists to encode selected structured project-state facts. It is not an independent owner of facts that GitHub or formal protocols own directly.

Machine-readable state must not be treated as proof of:

- human understanding;
- research truth;
- scientific validity;
- deployment readiness.

## 🔬 Evidence, protocols, and history

Primary surfaces include:

- `docs/research/**` — formal research protocol and research artifacts;
- `experiments/**` — fixtures, candidates, evaluators, results, locks, and experiment records where authorized;
- audit/future-work records;
- Git history and GitHub lifecycle facts.

Evidence/history must remain distinguishable from current human explanation and from machine state.

## 🧭 Stable truth vs volatile state

Stable conceptual material belongs in README/Overview/Applicability.

Volatile facts belong in dedicated state surfaces.

```text
STABLE
├── purpose
├── research question
├── conceptual boundaries
├── non-conflation principles
└── documentation architecture

VOLATILE
├── current HEAD / PR lifecycle
├── current owner-decision phase
├── current gate
├── authorization flags
├── Pilot / Evidence state
└── blockers
```

A stable human landing page should not become a chronological SHA ledger.

## 🎨 Emoji visual grammar

When emojis are used, they should behave as lightweight semantic types rather than decoration:

| Emoji | Meaning |
|---|---|
| 🧬 | Continuum / continuity / project identity |
| 👤 | human decision / human view |
| 🤖 | AI / agent |
| ⚙ | machine / deterministic mechanism |
| 🔬 | research |
| 🧪 | experiment |
| 📚 | state / knowledge / documentation |
| 🔎 | provenance / inspection |
| ⚖ | conflict / uncertainty |
| 🛡 | authority / safety boundary |
| 🔒 | lock / frozen input |
| 🚦 | authorization / gate |
| ✅ | confirmed or available |
| 🟡 | unresolved / incomplete / research |
| 🔴 | blocked / critical issue |
| 📜 | history / record |
| 🌍 | applicability / external context |

## 🧠 Visualizations have distinct jobs

Avoid several diagrams that say the same thing.

Recommended roles:

- **Mindmap** → concepts and relationships;
- **Flow diagram** → movement through Capture → State → Transfer → Successor;
- **Project tree** → documentation and component navigation;
- **Status table** → implemented / research / unavailable;
- **Comparison table** → differences in research emphasis.

Visualization should reduce cognitive load, not multiply representations without purpose.

## 🆚 Comparison discipline

Competitor or adjacent-system comparisons must follow these rules:

1. No unsupported superiority claims.
2. Compare **research emphasis and capabilities**, not prestige.
3. Product-specific claims must be dated and source-backed because external systems evolve.
4. Category-level comparisons may be used when the intent is conceptual orientation.
5. A comparison never changes Continuum's research evidence or architecture authority.

Preferred framing:

> **How Continuum differs in research emphasis**

Not:

> **Why Continuum is better than X**

## 🌍 Applicability discipline

Every applicability document must preserve:

```text
Potential applicability
        ≠
Validated applicability
        ≠
Deployment authorization
```

Examples from medicine, law, finance, defense, or other high-stakes domains are conceptual applicability examples only unless separately validated and authorized.

## 🏛 GitHub and Notion roles

### GitHub

GitHub is the canonical versioned technical/research record for:

- repository documentation;
- formal protocols;
- machine state;
- experiment artifacts;
- approval/decision records when committed;
- code and tests;
- Git lifecycle facts.

### Notion

Notion is a curated human knowledge/navigation layer for:

- project explanation;
- conceptual onboarding;
- applicability;
- diagrams and narrative;
- external research record.

Notion must not become an independent owner of volatile GitHub lifecycle or Experiment 0 semantics.

## 🔄 Consistency rule

Different documentation surfaces may summarize the same truth differently, but they may not contradict one another.

```text
same truth
   ├── human explanation
   ├── AI routing
   ├── machine representation
   └── evidence / historical record
```

When a structural change affects a bilingual human surface, EN/RU parity should be updated in the same bounded change unless an explicit reason for deferral is recorded.

## 🚫 Non-goals

Documentation Architecture v1 does not:

- authorize implementation work outside this docs-only scope;
- select OD-09;
- alter OD-01…OD-08;
- approve Candidate Gold/Oracle;
- authorize Pilot or Evidence;
- freeze production architecture;
- select storage/database/event sourcing;
- authorize ecosystem integration.

## 🧬 Core rule

> **Presentation summarizes truth. It does not create authority.**
