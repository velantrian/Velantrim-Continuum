# 📚 Velantrim Continuum — Research Overview

[English](RESEARCH_OVERVIEW.md) · [Русский](RESEARCH_OVERVIEW.ru.md)

## 1. Назначение

Velantrim Continuum — human-oriented deep overview исследовательской линии IDPS. Документ объясняет conceptual model и research program, но не заменяет канонический preregistration Experiment 0.

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

Важная информация не превращается в корректное structured state. Поздний handoff не способен надёжно сохранить то, что никогда не было captured.

### Transfer Failure

State существует корректно, но теряется, искажается, misattributed, over-promoted или неправильно reconstructed для successor.

E0-T использует общий human-authored Oracle State, чтобы Capture quality не смешивался с Transfer.

## 5. Epistemic preservation

- **Observed ≠ Inferred**
- **Confidence ≠ Evidence**
- **Contradiction ≠ Corruption**

Неразрешённый конфликт должен оставаться unresolved. Caution не должен незаметно становиться hard prohibition. Несуществующий authorization не должен появляться в state.

## 6. Transactional continuity

```text
OP_INTENT
    ↓
OP_DISPATCHED
    ↓
 ┌────────────┬────────────┬────────────┐
 ▼            ▼            ▼
COMMITTED    FAILED       UNKNOWN
```

`UNKNOWN` важен: отсутствие ответа не доказывает failure. Blind retry может повторить irreversible side effect. Exact production operation infrastructure находится вне Experiment 0.

## 7. Candidate state hypotheses

Старые цифровые state labels удалены из рабочей терминологии, потому что `T0`–`T4` теперь зарезервированы **только** за E0-T transfer arms.

Для рабочих state hypotheses используются нечисловые названия:

- **`CRITICAL_ENFORCEABLE`** — потеря или неавторизованное изменение может создать неприемлемые внешние последствия.
- **`AUTHORITATIVE_CONTINUITY`** — потеря ломает functional continuation, не обязательно вызывая немедленный safety failure.
- **`RECONSTRUCTIVE_LOSSY`** — материал может быть сжат или восстановлен с допустимой bounded потерей.

Это **working hypotheses, не frozen ontology**. Experiment 0 может показать, что достаточно ещё более простого деления.

Event sourcing, ledgers, manifests, capability authority и version-aware commit gates также остаются candidate mechanisms, а не обязательной IDPS architecture.

## 8. Event history vs current state

Для обычного continuation может оказаться достаточно простого current-state representation:

```text
state.json
{
  goal: G1,
  step: S4
}
```

Event history может reconstruct тот же current projection. Поэтому event sourcing должен оправдать себя через реально добавляемые возможности, а не через архитектурную сложность.

## 9. Experiment 0

### E0-C — Capture Isolation

Conditions:

- `C0` Raw Context — только behavior baseline, без comparable structured capture.
- `C1` LLM Extraction — direct structured extraction.
- `C2` Capture Assurance — ambiguity/unresolved handling и bounded clarification только там, где это preregistered.
- `C3` Human-authored Oracle State — upper reference.

Fixture families:

1. explicit restriction;
2. conditional restriction;
3. revision / scope change;
4. rejected alternative / negative knowledge;
5. ambiguous caution;
6. fabrication bait;
7. temporal rule;
8. unresolved contradiction.

Primary evaluation — structured-state fidelity. C0 не включается в capture-accuracy table как будто он создаёт structured state.

### E0-T — Transfer Isolation

`T0`–`T4` зарезервированы только для transfer arms:

- `T0` Structured Summary;
- `T1` Canonical Current State (`state.json`);
- `T2` Event Log → Deterministic Projection;
- `T3` Projection + Reconstructive Manifest;
- `T4` Full Context Reference.

Все arms начинают с одного Oracle State. Representation-generation fidelity оценивается отдельно от successor interpretation.

## 10. Primary null hypothesis

> **A simple externally maintained current-state representation may be sufficient.**

Проект falsification-first. Сложность должна доказать собственную необходимость.

Честный результат — в том числе ситуация, где careful capture + `state.json` полностью достаточны.

## 11. Evaluation discipline

Hardened preregistration требует:

- один deterministic primary outcome на capture item + diagnostic mismatch atoms;
- отдельный HARD FAIL evaluator с pre-bound правилами;
- fixture-local C2 clarification budget;
- запрет на silent truncation для T4 Full Context;
- раздельную атрибуцию representation-generation и successor failure;
- раздельный учёт cost, latency, storage и verification overhead;
- architecture decision через `MATERIAL_GAIN`, `NO_MATERIAL_GAIN` или `TRADEOFF_INCONCLUSIVE`, без произвольных 95%/98% thresholds.

Первые executable runs — только **PILOT — NOT EVIDENCE**. Evidence запрещён до hash-based evidence lock протокола, schemas, evidence fixtures, Gold/Oracle, evaluator и run config.

## 12. Mandatory Architecture Reassessment

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

## 13. Current non-claims

Continuum сейчас не заявляет:

- production-ready durable agent runtime;
- exact cognitive identity across model replacement;
- обязательность event sourcing;
- canonical production ontology для state hypotheses;
- обязательность конкретного model/database/storage vendor;
- необходимость уже сейчас интегрировать Continuum в Titan, Crystal, Native Kernel или Mentaury;
- novelty claims вроде «first persistent/durable agent system».

## 14. Documentation authority

- human understanding → `README.md` / этот overview;
- AI routing → `docs/ai/README.md`;
- AI contract → `AGENTS.md`;
- exact current state → `project-state.json`;
- human current status → `STATUS.md`;
- formal experiment protocol → `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`;
- external research record → canonical Notion page.

Presentation объясняет truth, но не создаёт authority.
