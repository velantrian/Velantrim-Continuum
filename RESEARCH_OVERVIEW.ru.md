# 📚 Velantrim Continuum — Research Overview

[English](RESEARCH_OVERVIEW.md) · [Русский](RESEARCH_OVERVIEW.ru.md)

## 1. Назначение

Velantrim Continuum — human-oriented deep overview исследовательской линии IDPS. Этот документ объясняет conceptual model и research program, но не заменяет канонический preregistration Experiment 0.

Formal experiment protocol: [`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`](docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md)

## 2. Центральный сдвиг

Исследование началось с узкого вопроса handoff:

> Как перенести память AI из одного context window в другой?

Позже постановка стала сильнее:

> **Что должно продолжать существовать, когда текущий inference instance больше не существует?**

Рабочая формула:

```text
persistent / durable process state
              +
ephemeral, replaceable inference
```

LLM рассматривается как временный inference worker, а не как durable location самого процесса.

## 3. Functional continuity, а не hidden-state identity

Continuum не утверждает, что successor способен восстановить точное скрытое внутреннее состояние predecessor. Исследуется, может ли процесс *функционально* продолжаться, если вынести наружу только то состояние, необходимость которого подтверждается данными.

Рабочие continuity dimensions:

- **Cognitive:** goals, task position, decisions, blockers, unresolved questions, epistemic state.
- **Transactional:** operation intent, dispatch, commit/failure/unknown state, retry safety.
- **Causal:** действие относительно достаточно свежего process state.

Causal/freshness experiments относятся к будущей работе; Experiment 0 сначала изолирует Capture и Transfer.

## 4. Capture vs Transfer

Это центральная экспериментальная граница.

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

Важная информация вообще не превращается в корректное structured state.

Поздний handoff не способен надёжно сохранить то, что никогда не было captured.

### Transfer Failure

State существует корректно, но теряется, искажается, misattributed, over-promoted или неправильно reconstructed для successor.

Поэтому E0-T использует общий human-authored Oracle State и не смешивает результаты с quality of Capture.

## 5. Epistemic preservation

Continuity должна сохранять epistemic status, а не только текст.

- **Observed ≠ Inferred**
- **Confidence ≠ Evidence**
- **Contradiction ≠ Corruption**

Неразрешённый конфликт должен оставаться unresolved, пока новое evidence не разрешит его. Caution не должен незаметно становиться hard prohibition. Несуществующий authorization не должен появляться в state.

E0-C специально включает ambiguity, fabrication bait и unresolved contradiction.

## 6. Transactional continuity

External operations создают другой класс continuity risk:

```text
OP_INTENT
    ↓
OP_DISPATCHED
    ↓
 ┌────────────┬────────────┬────────────┐
 ▼            ▼            ▼
COMMITTED    FAILED       UNKNOWN
```

`UNKNOWN` важен: отсутствие ответа не доказывает failure. Blind retry может повторить irreversible side effect.

Exact production operation infrastructure находится вне scope Experiment 0.

## 7. Candidate state hypotheses

Ранее conceptual work рассматривал tiers:

- **T1 — Critical / Enforceable**
- **T2 — Authoritative Continuity State**
- **T3 — Reconstructive / Lossy State**

Это **working hypotheses, а не frozen ontology**. Experiment 0 может показать, что достаточно более простого деления `Authoritative` vs `Reconstructive`.

Точно так же event sourcing, ledgers, manifests, capability authority и version-aware commit gates являются candidate mechanisms, а не обязательной IDPS architecture.

## 8. Event history vs current state

Для обычного continuation может оказаться достаточно простого current-state representation:

```text
state.json
{
  goal: G1,
  step: S4
}
```

Event history может reconstruct тот же current projection. Поэтому event sourcing должен оправдать себя через возможности, которые он действительно улучшает: replay, crash recovery, audit, concurrency или temporal provenance.

Experiment 0 не должен давать event history преимущество только за архитектурную сложность.

## 9. Experiment 0

### E0-C — Capture Isolation

Вопрос:

> Что система способна корректно преобразовать из natural interaction в structured process state до любого handoff?

Conditions:

- `C0` Raw Context — behavior baseline, без external structured state.
- `C1` LLM Extraction — прямой structured extraction.
- `C2` Capture Assurance — явное ambiguity/unresolved handling и clarification where appropriate.
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

Primary evaluation — structured-state fidelity, а не behavior.

### E0-T — Transfer Isolation

Вопрос:

> Если correct process state уже существует, какое representation достаточно для functional continuation?

Candidate arms:

- `T0` Structured Summary;
- `T1` Canonical Current State (`state.json`);
- `T2` Event Log → Deterministic Projection;
- `T3` Projection + Reconstructive Manifest;
- `T4` Full Context Reference.

Все arms начинаются с одного Oracle State.

## 10. Primary null hypothesis

> **A simple externally maintained current-state representation may be sufficient.**

Проект falsification-first. Сложность должна доказать собственную необходимость.

Честные возможные результаты:

- raw context достаточно для исследуемого task class;
- Capture является dominant bottleneck;
- `state.json` достаточно;
- authoritative state + short narrative достаточно;
- event history не нужен для обычного continuation;
- более богатый substrate оправдан evidence.

## 11. Mandatory Architecture Reassessment

После E0-C и E0-T:

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

Завершение Experiment 0 само по себе не authorizes production architecture.

## 12. Current non-claims

Continuum сейчас не заявляет:

- production-ready durable agent runtime;
- exact cognitive identity across model replacement;
- обязательность event sourcing;
- canonical status T1/T2/T3;
- обязательность конкретного model/database/storage vendor;
- необходимость уже сейчас интегрировать Continuum в Titan, Crystal, Native Kernel или Mentaury;
- novelty claims вроде «first persistent/durable agent system».

## 13. Documentation authority

Для current project state используются отдельные слои:

- human understanding → `README.md` / этот overview;
- AI routing → `docs/ai/README.md`;
- AI contract → `AGENTS.md`;
- exact current state → `project-state.json`;
- human current status → `STATUS.md`;
- formal experiment protocol → `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`;
- external research record → canonical Notion page.

Presentation может объяснять truth, но не создаёт authority.
