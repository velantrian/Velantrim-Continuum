# Owner Decision — ограниченный запуск `PILOT — NOT EVIDENCE`

> **Статус документа:** `DRAFT — NOT ADOPTED`  
> **Decision ID:** `OD-PILOT-01`  
> **Версия:** `0.6-draft`  
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
11. Future owner authorization использует **constructible two-commit Git binding без self-reference**:
    - **package commit A** содержит immutable Pilot manifest по canonical repository path;
    - manifest **не содержит SHA или tree собственного commit A** и не содержит будущий activation HEAD;
    - после создания A вычисляются `A`, `tree(A)` и SHA-256 exact manifest bytes;
    - **activation commit B** обязан быть единственным direct child A;
    - только B материализует canonical `experiment_0_pilot_status = AUTHORIZED_BOUNDED_PILOT` и package authorization record;
    - canonical record в B связывает exact `manifest_path`, exact `manifest_sha256`, `authorization_base_commit = A`, `authorization_base_tree = tree(A)`, `activation_policy = DIRECT_CHILD_ONLY` и bounded `activation_paths`;
    - manifest path не входит в activation paths и не может меняться между A и B;
    - diff `A..B` разрешён только для явно объявленных bounded governance paths, являющихся subset: `project-state.json`, `STATUS.md`, `docs/ai/CURRENT_STATE.md`, `docs/research/OD_PILOT_01_DRAFT.md`;
    - `project-state.json` обязательно должен быть изменён B;
    - любой code/protocol/fixture/reference/evaluator/prompt/run-config/manifest drift между A и B fail-closed запрещён.
12. Preflight дополнительно доказывает, что manifest уже существовал в A как regular non-executable Git blob (`100644`) и его bytes в A имеют exact canonical SHA-256.
13. Фактический activation `HEAD=B` и `tree(B)` не находятся внутри manifest. Они вычисляются после проверки direct-child transition и записываются в Pilot reservation/result receipt вместе с A/tree(A).
14. Generic `AUTHORIZED_BOUNDED_PILOT` без exact canonical package binding fail-closed отклоняется.

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
- `activation_policy = DIRECT_CHILD_ONLY`;
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

Manifest **не содержит** `execution_head_commit`, `execution_tree`, `authorization_base_commit` или `authorization_base_tree`: такие поля создают или возвращают self-referential identity coupling и fail-closed запрещены.

Manifest necessary but not sufficient authority. Только будущий canonical activation record в отдельном B hash-bind exact manifest blob from A и A/tree(A).

## 5. Future canonical authorization record

Future activation commit B должен материализовать record следующей формы:

```json
{
  "status": "AUTHORIZED_BOUNDED_PILOT_PACKAGE",
  "authorization_id": "<unique ID>",
  "manifest_path": "experiments/e0/pilot/packages/<package>.json",
  "manifest_sha256": "<exact lowercase SHA-256 of manifest bytes in A>",
  "authorization_base_commit": "<package commit A>",
  "authorization_base_tree": "<tree(A)>",
  "activation_policy": "DIRECT_CHILD_ONLY",
  "activation_paths": [
    "project-state.json"
  ]
}
```

`activation_paths` могут включать только реально необходимые governance mirrors из bounded allowlist. Manifest никогда не является activation path.

## 6. Official execution path

Только:

`python scripts/e0/execute_pilot.py --manifest <manifest> --request <request>`

`run_adapter.py` остаётся internal-only.

До spawn executor проверяет:

1. strict-clean worktree;
2. canonical Pilot status + exact manifest path/SHA binding;
3. exact A/tree(A) из canonical authorization record;
4. manifest существует в A как `100644 blob` и его bytes в A соответствуют canonical SHA-256;
5. current activation HEAD имеет ровно одного parent и этот parent равен A;
6. diff `A..B` не содержит ничего кроме declared bounded activation paths;
7. `project-state.json` действительно изменён в B;
8. human-reference approval validator;
9. повторный strict-clean worktree после child validator;
10. exact request bytes SHA-256;
11. ещё один strict-clean worktree непосредственно перед output reservation и перед adapter spawn.

Human-reference child запускается с `python -B` и `PYTHONDONTWRITEBYTECODE=1`, чтобы control path не создавал `__pycache__` drift.

Manifest/request должны быть regular non-symlink files. Request читается один раз; те же bytes хэшируются, парсятся, записываются и передаются adapter.

Reservation/result receipt фиксируют:

- `authorization_base_commit = A`;
- `authorization_base_tree = tree(A)`;
- `activation_head_commit = B`;
- `activation_tree = tree(B)`.

Таким образом manifest не должен заранее знать commit, который материализует authorization.

## 7. Output and process containment

Outputs:

`.velantrim-continuum-pilot-runs/<manifest-sha256>/attempt-NNN/`

Output root/package/attempt должны быть реальными directories, не symlink, и оставаться вне repository.

`max_runs` технически ограничивается atomic attempt reservation. Adapter работает в отдельной process group/session; timeout/output-cap/final cleanup завершают descendants. Это lifecycle containment, не sandbox.

## 8. Stop rules

Fail closed если:

- approval validation fails;
- canonical Pilot authorization отсутствует/не совпадает с package;
- manifest path/SHA не совпадают;
- A/tree(A) invalid;
- manifest отсутствует в A, имеет неправильный Git mode/type или bytes/SHA mismatch;
- B не является direct child A;
- activation transition затрагивает любой path вне declared bounded allowlist;
- manifest изменён между A и B;
- worktree dirty до, после child validator или непосредственно перед execution steps;
- manifest/request symlink/non-regular;
- request hash mismatch;
- output path symlink/escape;
- Evidence ID requested;
- unsupported posture;
- timeout/output cap/nonzero/malformed adapter output;
- max_runs exhausted;
- semantic correction требуется для protocol/fixture/Gold/Oracle.

## 9. Non-authorizations

Даже будущая adoption OD-PILOT-01 не создаёт автоматически:

- Evidence Lock;
- E0-C Evidence;
- E0-T Evidence;
- scientific conclusions;
- production runtime/architecture;
- event sourcing requirement;
- ecosystem integration.

`Human Reference Approved ≠ Pilot ≠ Evidence ≠ Production Authorization`.

## 10. Owner adoption record

До отдельной explicit owner adoption + canonical activation transition статус остаётся `DRAFT — NOT ADOPTED` / `Pilot NOT_AUTHORIZED`.

```text
I, <GitHub login>, adopt OD-PILOT-01 v0.6.

Authorized bounded Pilot package:
- authorization_id: <unique ID>;
- package commit A: <SHA>;
- package tree: <tree(A)>;
- activation policy: DIRECT_CHILD_ONLY;
- activation paths: <bounded governance paths>;
- canonical manifest path: <repository-relative path under experiments/e0/pilot/>;
- canonical manifest SHA-256: <SHA-256 of exact manifest bytes in A>;
- fixtures/scenarios: <PILOT-only IDs>;
- request SHA-256: <SHA-256>;
- approved reference paths/hashes: <paths + SHA-256>;
- provider/model/settings: <details>;
- credential profile/scope: <reference only; no secrets>;
- adapter command/cwd/environment allowlist: <details>;
- timeout/output cap/max runs/budget: <limits>;
- execution posture: UNCONTROLLED_LOCAL_ADVISORY;
- output destination: .velantrim-continuum-pilot-runs.

Activation must be a separately reviewed direct child B of A and may only materialize canonical authorization/governance mirrors.

Pilot remains PILOT — NOT EVIDENCE.
Evidence Lock remains NOT_CREATED.
E0-C/E0-T and production remain NOT_AUTHORIZED.

UTC timestamp: <YYYY-MM-DDTHH:MM:SSZ>
```
