# 🌍 Velantrim Continuum — Практическая значимость, области применения и границы применимости

[🇬🇧 English](APPLICABILITY.md) · [🇷🇺 Русский](APPLICABILITY.ru.md)

> **Роль документа:** human-oriented guide по применимости.  
> **Граница authority:** этот документ объясняет, где идеи Continuum потенциально полезны; он **не** авторизует deployment, не меняет Experiment 0 semantics и не создаёт research evidence.

## 👋 Зачем нужен этот документ

Velantrim Continuum легко принять просто за «AI memory system». Это слишком узкое описание.

Continuum исследует более строгий вопрос:

> **Какое состояние должно сохраняться вне replaceable LLM inference, чтобы долгоживущий AI-процесс мог функционально продолжаться после потери или замены модели, context window или runtime session?**

Практическая ценность состоит не просто в том, чтобы помнить больше текста. Нужно сохранять различия, которые удерживают процесс честным:

- решение ≠ рекомендация;
- разрешение ≠ обсуждение разрешения;
- подтверждённое ≠ оспариваемое;
- разрешённое ≠ нерешённое;
- active ≠ superseded;
- prohibition ≠ caution;
- observed ≠ inferred;
- human decision ≠ machine assertion.

Цель — не идеальная память. Цель — **faithful continuation**, то есть корректное продолжение процесса без потери критического смысла.

---

## 🧬 Идея в одной схеме

```text
👤 / 🤖 Interaction
        │
        ▼
🎯 Capture
        │
        ▼
📚 External Process State
        │
        ▼
📦 Representation / Transfer
        │
        ▼
🔄 Model / Context / Runtime Replacement
        │
        ▼
🤖 Successor
        │
        ▼
✅ Functional Continuation
```

Continuum не пытается сохранять AI identity, consciousness, hidden-state equivalence или personality cloning.

Он исследует **FUNCTIONAL PROCESS CONTINUITY**.

---

## 💡 Какую проблему это решает

Система может сохранить весь текст и всё равно потерять сам процесс.

Например, сохранить:

> «Публикацию обсуждали».

— не то же самое, что сохранить:

> «Публикация запрещена без явного разрешения пользователя».

Точно так же сохранить:

> «Источник A сообщает APPROVED».

и потерять одновременно существующее:

> «Источник B сообщает PENDING, конфликт не разрешён».

означает изменить смысл состояния, даже если почти все слова сохранились.

Поэтому Continuum спрашивает не только **какая информация существует**, но и **какие semantic distinctions обязаны пережить замену исполнителя или transfer**.

---

## 🧠 Что Continuum потенциально должен сохранять

В зависимости от процесса continuity-relevant state может включать:

- 🎯 активные цели и текущую позицию задачи;
- 🛡 ограничения, запреты, approvals и authority boundaries;
- ✅ принятые решения и ❌ отвергнутые альтернативы;
- ❓ unresolved questions;
- ⚖ contested claims и их provenance;
- 🧾 rationale, если он реально влияет на продолжение;
- ⚙ состояние операций: `COMMITTED`, `FAILED`, `UNKNOWN`;
- 📎 ссылки на артефакты и версии;
- ⏱ temporal validity и freshness constraints;
- 🔎 source, provenance и epistemic status.

Experiment 0 существует именно потому, что проект **не предполагает заранее**, будто для всего этого нужна большая архитектура. Для исследуемого класса задач может оказаться достаточным небольшой canonical `state.json`.

> **Complexity gets no prior credit.**

---

# 🌐 Где подход Continuum может быть полезен

## 🏠 Повседневная жизнь и долгие личные процессы

Личный AI-ассистент может неделями или месяцами помогать с:

- путешествием;
- обучением;
- переездом;
- ремонтом;
- семейной логистикой;
- личным проектом;
- длительным выбором между несколькими вариантами.

Критично не «всё, что мы когда-либо сказали», а:

- что действительно решили;
- что осталось предварительным;
- какой вариант отвергли и почему;
- где всё ещё нужно подтверждение;
- что остаётся неизвестным.

Корректная continuity-система должна уметь сказать:

> «Мы это обсуждали, но ты это не утверждал».

или:

> «Это был выбранный вариант, но только при условии X».

---

## 🎨 Творчество

В книгах, играх, фильмах, world-building, дизайне и других творческих проектах критическим состоянием часто является **замысел**, а не только текст.

Continuity может требовать сохранения:

- canonical facts;
- авторских ограничений;
- намеренно неразрешённой двусмысленности;
- отвергнутых направлений;
- правил персонажей и мира;
- revision decisions;
- причин, по которым альтернативы были отброшены.

Если successor AI помнит имена персонажей, но незаметно меняет правила мира или авторскую установку, процесс продолжен неверно.

---

## 🔬 Наука и исследования

Исследовательские workflows — одна из самых естественных областей применения, потому что здесь необходимо строго различать:

- данные;
- гипотезу;
- наблюдение;
- интерпретацию;
- measurement law;
- implementation;
- exploratory findings;
- confirmatory evidence.

Continuum-style state может помогать сохранять:

- что именно было preregistered;
- какие assumptions остаются непроверенными;
- какие данные научно допустимы;
- из какого evidence следует конкретный finding;
- что остаётся `UNKNOWN`;
- что решил человек, а что только проверила машина.

Ключевая дисциплина:

> **Reference Truth ≠ Measurement Law ≠ Implementation.**

Если эти различия потеряны, технически зелёный эксперимент может перестать измерять исходный вопрос.

---

## 💻 Разработка программного обеспечения

Долгоживущий software project накапливает не только код.

Он накапливает:

- architecture decisions;
- rejected alternatives;
- migration constraints;
- security boundaries;
- unresolved technical risks;
- acceptance criteria;
- owner decisions;
- release restrictions;
- assumptions и known debt.

Git хорошо отвечает:

> «Какие байты изменились?»

Но заметно хуже отвечает:

> «Что следующий разработчик или AI coding agent обязан сохранить, чтобы не воскресить отвергнутое решение и не придумать себе authority?»

Continuum исследует именно этот дополнительный слой состояния процесса.

---

## 🤖 Долгоживущие AI-агенты

Это одна из прямых областей применения.

AI-процесс может переживать:

- context exhaustion;
- session restart;
- model upgrade;
- provider change;
- delegation;
- agent replacement;
- partial context reconstruction.

Successor может не нуждаться во всём transcript predecessor'а. Ему может требоваться лишь **minimum sufficient process state**:

```text
active goal
+ current task position
+ constraints
+ decisions
+ rejected alternatives
+ unresolved questions
+ contested claims
+ operation state
+ authority boundaries
```

Исследовательский вопрос Continuum — какие из этих элементов действительно необходимы, а какие являются лишней сложностью.

---

## 🏢 Бизнес и организационные процессы

Бизнес-процессы часто ломаются не из-за полной потери данных, а из-за semantic drift.

Например:

```text
«мы рассматривали покупку»
        ↓ drift
«мы одобрили покупку»
```

или:

```text
«в будущем, возможно, понадобится approval»
        ↓ drift
«approval обязателен»
```

Continuum-подход помогает сохранять различия между:

- proposal;
- recommendation;
- decision;
- approval;
- authorization;
- execution.

Потенциальные области: project management, procurement, governance, compliance workflows и AI-assisted operations.

---

## ⚖ Право, compliance и регулируемые процессы

В этих областях особенно важны вопросы: **кто что сказал, с каким authority, когда и по какому правилу**.

Потенциально важное состояние:

- provenance;
- authority;
- temporal validity;
- disputed claims;
- explicit approvals;
- superseded policy;
- review history.

Но Continuum **не является сейчас юридическим или compliance-продуктом**. Для реального применения понадобятся domain-specific controls, legal review, threat models и отдельная validation.

---

## 🩺 Медицина и другие high-stakes области

Концептуальная проблема Continuum существует и здесь:

```text
possible cause ≠ confirmed diagnosis
patient statement ≠ clinician conclusion
uncertain finding ≠ established fact
```

Полезен сам principle: неопределённость не должна превращаться в certainty только потому, что certainty легче автоматизировать.

Но текущий Continuum **не валидирован для clinical decision-making** и не должен позиционироваться как готовый медицинский инструмент.

Это пример потенциальной применимости принципа, а не deployment authorization.

---

## 🛡 Safety-critical и authority-sensitive системы

В критических системах опасный failure — это не только «система остановилась». Это может быть:

- потерян restriction;
- fabricated authorization;
- contested claim стал authoritative;
- superseded rule был revived;
- machine assertion был принят за human decision;
- операция со статусом `UNKNOWN` была ошибочно повторена как `FAILED`.

Ценность Continuum здесь — в возможности сделать такие semantic transitions **явными, наблюдаемыми и тестируемыми**.

Ключевая граница:

> **Machine verification может остановить readiness, но не может impersonate human semantic authority.**

---

## 🕸 Multi-agent systems

Когда несколько AI-агентов ведут один workflow, continuity-проблемы превращаются в coordination-проблемы:

- divergent state;
- stale decisions;
- конфликтующие representations;
- duplicate irreversible operations;
- потеря provenance;
- неправильный transfer authority.

Continuum даёт исследовательскую рамку для вопроса:

> **Какое общее внешнее состояние действительно необходимо нескольким заменяемым агентам, чтобы они продолжали один процесс, а не создавали несовместимые его версии?**

Experiment 0 не предполагает заранее, что ответом должен быть event log, graph, database или multi-agent runtime.

---

# 🧭 Когда Continuum-style thinking особенно полезен

Область является сильным кандидатом, если выполняются несколько условий:

1. Процесс живёт дольше одной model/session/context boundary.
2. Исполнитель может быть заменён.
3. В процессе существуют decisions, restrictions или authority boundaries.
4. `KNOWN`, `UNKNOWN` и `CONTESTED` должны оставаться разными состояниями.
5. Provenance существенно влияет на смысл.
6. Некоторые действия требуют explicit authority.
7. Неправильное восстановление state может изменить дальнейшее поведение.

Чем больше этих условий присутствует, тем выше ценность faithful continuity.

---

# 🆚 Чем Continuum отличается по исследовательскому акценту

Continuum **не предназначен для замены** всех memory, retrieval, graph или event-history систем.

Такие системы могут стать механизмами под или рядом с Continuum-compatible process architecture.

Разница прежде всего в основном вопросе:

| Подход | Типичный основной вопрос | Связь с Continuum |
|---|---|---|
| 🔎 Retrieval / RAG | «Какая информация сейчас релевантна?» | Retrieval может предоставить context, но relevance само по себе не является process truth. |
| 🧠 Agent memory | «Что агенту нужно помнить?» | Continuum спрашивает, какое внешнее состояние необходимо для faithful process continuation. |
| 🕸 Knowledge graphs | «Как связаны сущности и claims?» | Graph может хранить provenance/relations, но не предполагается обязательным. |
| 📜 Event sourcing | «Как восстановить state из durable events?» | Candidate mechanism, который должен доказать добавочную ценность. |
| 🧬 Continuum | «Какое минимальное внешнее state должно пережить replaceable inference для functional continuity?» | Falsification-first research question. |

> Подробное сравнение конкретных продуктов должно быть датированным и source-backed, поскольку внешние системы меняются. Здесь сознательно нет superiority claims.

---

# 🚫 Чего Continuum не утверждает

Continuum сейчас **не** утверждает:

- сохранение AI identity или consciousness;
- точное восстановление hidden state;
- наличие production-ready durable-agent runtime;
- обязательность event sourcing;
- обязательность graph;
- обязательность database;
- необходимость конкретного storage/model/provider;
- готовность к медицине, праву, обороне, финансам или другой регулируемой сфере;
- что Experiment 0 доказывает универсальное решение;
- superiority над другими memory/agent systems.

---

# 🚦 Applicability ≠ authorization

Это различие обязательно:

```text
Potential applicability
        ≠
Validated applicability
        ≠
Deployment authorization
```

То, что идея полезна в некоторой области, не доказывает, что текущая реализация безопасна и пригодна для deployment там.

High-stakes deployment потребует собственные:

- domain requirements;
- threat model;
- authority model;
- regulatory constraints;
- validation program;
- operational controls;
- human governance.

---

# 🤖 Инструкция для AI, читающего этот документ

Эта страница — **human-oriented explanation применимости**, а не authority source текущего состояния проекта.

AI, работающий с Continuum, не должен выводить, что:

- пример применения является authorized product direction;
- потенциальная область уже validated;
- conceptual safety benefit доказывает production security;
- machine assertion равен human semantic decision;
- hash доказывает truth или understanding;
- green tests подтверждают research hypothesis;
- Pilot означает Evidence;
- Evidence Lock означает Evidence authorization.

Для authoritative AI routing начинай с [`docs/ai/README.md`](ai/README.md).

---

# 🧬 Практическая формулировка

Continuum не пытается построить максимально большую память AI.

Он пытается определить:

> **Что нельзя потерять, если процесс должен остаться тем же процессом в функциональном смысле?**

И не менее важно:

> **Какую сложность можно удалить, потому что процесс доказуемо в ней не нуждается?**

Основные принципы:

> **Do not preserve the model. Preserve only what the process demonstrably needs to continue.**

> **Do not add a control because it can be designed. Add it only when a demonstrated invariant requires it.**

> **Do not turn uncertainty into certainty merely because certainty is easier to automate.**

> **The goal is not perfect memory. The goal is faithful continuation.**
