# Owner Decision — ограниченный запуск `PILOT — NOT EVIDENCE`

> **Статус документа:** `DRAFT — NOT ADOPTED`  
> **Decision ID:** `OD-PILOT-01`  
> **Версия:** `0.2-draft`  
> **Authority:** repository owner only

## 1. Решение

Этот документ описывает условия, при которых владелец **может отдельно авторизовать один ограниченный Experiment 0 Pilot** с обязательной маркировкой:

`PILOT — NOT EVIDENCE`

Само наличие этого файла, его merge, CI, AI review или preflight **не являются Owner GO**.

## 2. Preconditions

Pilot остаётся `NOT_AUTHORIZED`, пока одновременно не выполнены все условия:

1. PR #28 merged; authoritative human-approved Gold / Oracle находятся на execution head.
2. `validate_human_reference_approval.py` проходит на exact execution head.
3. Historical candidates остаются `AI_PROPOSED_DRAFT`; run использует только approved versioned reference artifacts.
4. Experiment 0 contract gate и relevant tests проходят на exact execution head.
5. **Execution worktree clean:** `git status --porcelain` пуст; `HEAD` равен `execution_head_commit` из manifest; нет локальных изменений в approved references, fixtures, protocol, evaluator, prompts/templates или run config.
6. Выбраны только Pilot fixtures/scenarios. Evidence IDs запрещены.
7. Владелец явно задаёт provider/model identifier/settings, adapter command, limits, output destination и credentials profile/scope. **Секретные значения и API keys в manifest не записываются.**
8. Выбран execution posture.
9. Evidence Lock остаётся `NOT_CREATED`.
10. **Отдельный owner-authorization state change** материализует в canonical `project-state.json` значение `experiment_0_pilot_status = AUTHORIZED_BOUNDED_PILOT`, не меняя Evidence/production authority. До такого reviewable state transition caller-supplied manifest не может авторизовать Pilot.
11. Preconditions перепроверены непосредственно перед запуском.

## 3. Execution posture

### A. `UNCONTROLLED_LOCAL_ADVISORY`

Допустим только для diagnostic Pilot без необратимых действий.

Обязательная честная маркировка:

- `isolation_enforcement = NOT_ENFORCED`
- `network_isolation = NOT_ENFORCED`
- `filesystem_isolation = NOT_ENFORCED`
- `process_isolation = NOT_ENFORCED`

Ограничения network/tools/credentials в этом posture являются **owner/executor obligations**, а не sandbox guarantees.

Запрещены purchases, deploy, publication, deletion, production writes и любые необратимые side effects.

### B. `ISOLATED_RUNNER_CONTRACT`

Разрешён только после отдельного approved isolation contract/implementation. Этот документ не создаёт sandbox и не утверждает, что он существует.

## 4. Required Pilot manifest

До запуска нужен immutable-by-convention manifest минимум с:

- `run_type = PILOT`;
- `label = PILOT — NOT EVIDENCE`;
- `owner_decision_id = OD-PILOT-01`;
- `owner_decision_status = ADOPTED`;
- exact execution commit/tree;
- human approval record path/hash;
- approved Gold/Oracle path/hash;
- exact Pilot fixture/scenario IDs;
- protocol/schema/fixture/evaluator/run-config hashes;
- provider/model/settings;
- credential profile/scope **without secret values**;
- execution posture;
- timeout/output-size/max-runs/budget limits;
- output destination;
- `evidence_lock = {status: NOT_CREATED, sha256: null}`.

The manifest is necessary but **not sufficient authority**. Preflight also requires the canonical project-state authorization described above.

## 5. Stop rules

Stop immediately if:

- approval validation fails;
- canonical Pilot authorization state is absent or inconsistent;
- worktree or bound artifact drift is detected;
- an Evidence fixture/scenario is requested;
- adapter exceeds timeout or output cap;
- adapter returns malformed JSON or non-zero exit;
- unknown adapter behavior or unapproved side effect appears;
- production credentials or irreversible external writes are observed;
- a semantic change to protocol/fixture/Gold/Oracle is required.

Any semantic correction goes through a separate bounded PR. Pilot outputs remain Pilot-only.

## 6. Non-authorizations

Adoption of OD-PILOT-01 does **not** authorize or create:

- Evidence Lock;
- E0-C Evidence;
- E0-T Evidence;
- scientific architecture conclusions;
- production runtime/architecture;
- event sourcing requirement;
- ecosystem integration.

`Human Reference Approved ≠ Pilot Evidence ≠ Evidence Lock ≠ Evidence Authorization ≠ Production Authorization`.

## 7. Owner adoption record

Until this block is explicitly completed by the repository owner **and** a separate reviewable canonical state change records the bounded authorization, status remains `DRAFT — NOT ADOPTED` / `Pilot NOT_AUTHORIZED`.

```text
I, <GitHub login>, adopt OD-PILOT-01 v0.2.

Authorized bounded Pilot package:
- exact execution head: <SHA>;
- execution tree: <SHA>;
- fixtures/scenarios: <PILOT-only IDs>;
- approved reference paths/hashes: <paths + SHA-256>;
- provider/model/settings: <details>;
- credential profile/scope: <reference only; no secrets>;
- adapter command: <exact command>;
- timeout/output cap/max runs/budget: <limits>;
- execution posture: <A/B>;
- output destination: <location>;
- incident contact: <identity>.

Pilot remains `PILOT — NOT EVIDENCE`.
Evidence Lock remains `NOT_CREATED`.
E0-C/E0-T Evidence and production authority remain NOT_AUTHORIZED.

UTC timestamp: <YYYY-MM-DDTHH:MM:SSZ>
```
