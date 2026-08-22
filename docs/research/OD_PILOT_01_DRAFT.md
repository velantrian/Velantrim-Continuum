# Owner Decision — ограниченный запуск `PILOT — NOT EVIDENCE`

> **Статус документа:** `DRAFT — NOT ADOPTED`  
> **Decision ID:** `OD-PILOT-01`  
> **Версия:** `0.5-draft`  
> **Authority:** repository owner only

## 1. Решение

Этот документ описывает условия, при которых владелец **может отдельно авторизовать один ограниченный Experiment 0 Pilot** с обязательной маркировкой:

`PILOT — NOT EVIDENCE`

Само наличие этого файла, его merge, CI, AI review или preflight **не являются Owner GO**.

## 2. Preconditions

Pilot остаётся `NOT_AUTHORIZED`, пока одновременно не выполнены все условия:

1. PR #28 merged; authoritative human-approved Gold / Oracle сохранены.
2. `validate_human_reference_approval.py` проходит на runtime head.
3. Historical candidates остаются `AI_PROPOSED_DRAFT`.
4. Experiment 0 contracts/tests проходят.
5. Worktree остаётся strict-clean до adapter spawn.
6. Выбраны только Pilot fixtures/scenarios; Evidence IDs запрещены.
7. Владелец задаёт provider/model/settings, exact adapter command, repository-relative cwd, environment allowlist, limits и credential profile/scope без секретных значений.
8. Exact request bytes связаны SHA-256 в manifest.
9. Поддерживаемый posture: только `UNCONTROLLED_LOCAL_ADVISORY`.
10. Evidence Lock остаётся `NOT_CREATED`.
11. Future owner authorization использует **non-circular two-stage Git binding**:
    - manifest фиксирует `authorization_base_commit` и `authorization_base_tree` — последний pre-authorization baseline;
    - canonical `project-state.json` фиксирует exact `manifest_path`, `manifest_sha256`, тот же base commit/tree и `AUTHORIZED_BOUNDED_PILOT`;
    - текущий runtime `HEAD` обязан быть base или его descendant;
    - diff `authorization_base_commit..HEAD` разрешён только для bounded authorization-transition paths: exact manifest, `project-state.json`, `STATUS.md`, `docs/ai/CURRENT_STATE.md`, `docs/research/OD_PILOT_01_DRAFT.md`;
    - любой runtime/protocol/fixture/reference/code drift в этом переходе fail-closed запрещён.
12. Фактический runtime HEAD/tree не находятся внутри hash-bound manifest, чтобы исключить self-referential fixed-point. Они вычисляются после проверки transition и записываются в Pilot reservation/result receipt.
13. Generic `AUTHORIZED_BOUNDED_PILOT` без exact package binding fail-closed отклоняется.

Текущий canonical state остаётся:

- `experiment_0_pilot_status = NOT_AUTHORIZED`;
- `experiment_0_pilot_authorization = null`.

То есть этот PR **не авторизует Pilot**.

## 3. Execution posture

### Поддерживается: `UNCONTROLLED_LOCAL_ADVISORY`

- `isolation_enforcement = NOT_ENFORCED`
- `network_isolation = NOT_ENFORCED`
- `filesystem_isolation = NOT_ENFORCED`
- `process_isolation = NOT_ENFORCED`

Это diagnostic Pilot без production sandbox claims. Purchases, deploy, publication, deletion, production writes и необратимые side effects запрещены.

### Не поддерживается: `ISOLATED_RUNNER_CONTRACT`

Preflight fail-closed отклоняет этот posture до отдельной реальной реализации/контракта.

## 4. Required Pilot manifest

Manifest минимум содержит:

- `run_type = PILOT`;
- `label = PILOT — NOT EVIDENCE`;
- `owner_decision_id = OD-PILOT-01`;
- `owner_decision_status = ADOPTED`;
- exact `authorization_base_commit`;
- exact `authorization_base_tree`;
- human approval path/hash;
- approved Gold/Oracle path/hash;
- Pilot-only IDs;
- exact request SHA-256;
- provider/model/settings;
- credential profile/scope без secret values;
- exact adapter command;
- repository-relative adapter cwd;
- environment allowlist;
- limits;
- `output_destination = .velantrim-continuum-pilot-runs`;
- `evidence_lock = {status: NOT_CREATED, sha256: null}`.

Manifest necessary but not sufficient authority. Canonical state отдельно hash-bind exact manifest и base identity.

## 5. Official execution path

Только:

`python scripts/e0/execute_pilot.py --manifest <manifest> --request <request>`

`run_adapter.py` остаётся internal-only.

До spawn executor проверяет:

1. canonical Pilot status + exact manifest path/SHA binding;
2. manifest base commit/tree = canonical base commit/tree;
3. current HEAD descendant relation к base;
4. diff base..HEAD содержит только authorization-transition allowlist paths;
5. strict-clean worktree;
6. human-reference approval validator;
7. повторный strict-clean worktree после child validator;
8. exact request bytes SHA-256.

Human-reference child запускается с `python -B` и `PYTHONDONTWRITEBYTECODE=1`, чтобы сам control path не создавал `__pycache__` drift.

Manifest/request должны быть regular non-symlink files. Request читается один раз; те же bytes хэшируются, парсятся, записываются и передаются adapter.

Фактические `runtime_head_commit` и `runtime_tree` вычисляются после preflight и фиксируются в reservation/result receipt вместе с base identity.

## 6. Output and process containment

Outputs:

`.velantrim-continuum-pilot-runs/<manifest-sha256>/attempt-NNN/`

Output root/package/attempt должны быть реальными directories, не symlink, и оставаться вне repository.

`max_runs` технически ограничивается atomic attempt reservation. Adapter работает в отдельной process group/session; timeout/output-cap/final cleanup завершают descendants. Это lifecycle containment, не sandbox.

## 7. Stop rules

Fail closed если:

- approval validation fails;
- canonical Pilot authorization отсутствует/не совпадает с package;
- base commit/tree не совпадают;
- runtime HEAD не descendant base;
- authorization transition затрагивает любой path вне bounded allowlist;
- worktree dirty до или после child validator;
- manifest/request symlink/non-regular;
- request hash mismatch;
- output path symlink/escape;
- Evidence ID requested;
- unsupported posture;
- timeout/output cap/nonzero/malformed adapter output;
- max_runs exhausted;
- semantic correction требуется для protocol/fixture/Gold/Oracle.

## 8. Non-authorizations

Даже будущая adoption OD-PILOT-01 не создаёт автоматически:

- Evidence Lock;
- E0-C Evidence;
- E0-T Evidence;
- scientific conclusions;
- production runtime/architecture;
- event sourcing requirement;
- ecosystem integration.

`Human Reference Approved ≠ Pilot ≠ Evidence ≠ Production Authorization`.

## 9. Owner adoption record

До отдельной explicit owner adoption + canonical authorization transition статус остаётся `DRAFT — NOT ADOPTED` / `Pilot NOT_AUTHORIZED`.

```text
I, <GitHub login>, adopt OD-PILOT-01 v0.5.

Authorized bounded Pilot package:
- authorization_id: <unique ID>;
- authorization_base_commit: <pre-authorization SHA>;
- authorization_base_tree: <tree SHA>;
- canonical manifest path: <repository-relative path under experiments/e0/pilot/>;
- canonical manifest SHA-256: <SHA-256>;
- fixtures/scenarios: <PILOT-only IDs>;
- request SHA-256: <SHA-256>;
- approved reference paths/hashes: <paths + SHA-256>;
- provider/model/settings: <details>;
- credential profile/scope: <reference only; no secrets>;
- adapter command/cwd/environment allowlist: <details>;
- timeout/output cap/max runs/budget: <limits>;
- execution posture: UNCONTROLLED_LOCAL_ADVISORY;
- output destination: .velantrim-continuum-pilot-runs.

Pilot remains PILOT — NOT EVIDENCE.
Evidence Lock remains NOT_CREATED.
E0-C/E0-T and production remain NOT_AUTHORIZED.

UTC timestamp: <YYYY-MM-DDTHH:MM:SSZ>
```
