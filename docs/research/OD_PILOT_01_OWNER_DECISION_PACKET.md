# OD-PILOT-01 — Owner Decision Packet

> **Status:** `PREPARED — OWNER DECISION PENDING`  
> **Decision:** whether to authorize preparation/execution of one bounded `PILOT — NOT EVIDENCE` package under the controls merged by PR #29.  
> **Prepared from authoritative merged main:** `fc5fa1b16f5dda04fe2fe34d0c66f09856c33d2f`  
> **PR #29 independently reviewed head:** `78ca9d95132878b70dc7286de5e136736812866b`  
> **Important:** this packet does **not** adopt OD-PILOT-01, does not create package A or activation B, and does not run Pilot.

## 1. Decision in plain language

The control plane needed to construct and verify a bounded Pilot package is merged. The owner must now decide whether to cross the next authority boundary.

There are two valid outcomes:

- `GO — PREPARE BOUNDED PILOT PACKAGE`: authorize a separate, exact package-construction workflow. This is not yet execution authority until the exact package A and direct-child activation B are materialized and reviewed under the merged controls.
- `NO-GO / DEFER`: leave canonical state unchanged and do not prepare or execute a real Pilot.

No other state should be inferred from this document.

## 2. Current authority state

Until an explicit owner decision and subsequent canonical activation transition:

- `experiment_0_pilot_status = NOT_AUTHORIZED`;
- `experiment_0_pilot_authorization = null`;
- OD-PILOT-01 remains `DRAFT — NOT ADOPTED`;
- Evidence Lock remains `NOT_CREATED`;
- E0-C Evidence remains `NOT_AUTHORIZED / NOT_RUN`;
- E0-T Evidence remains `NOT_AUTHORIZED / NOT_RUN`;
- production runtime remains `NOT_AUTHORIZED`;
- production architecture remains `NOT_FROZEN`;
- ecosystem integration remains `NOT_AUTHORIZED`.

`PR #29 merged ≠ Owner GO ≠ package authorization ≠ Pilot ≠ Evidence Lock ≠ Evidence authorization ≠ production authorization`.

## 3. What PR #29 established

The merged controls provide a machine-verifiable construction rule for a future authorization:

1. package commit **A** contains the immutable Pilot manifest;
2. A is created before its commit/tree identity is needed by canonical authority, avoiding self-reference;
3. activation commit **B** must be the single direct child of A;
4. A→B may change only declared bounded governance paths;
5. manifest bytes are proven as an exact regular `100644` Git blob in A;
6. canonical authority is proven as exact regular `100644 project-state.json` Git blob in B;
7. symlink, executable mode, submodule, missing blob, external mutable authority, or working-tree/blob mismatch fail closed;
8. strict worktree checks and Python bytecode suppression protect the pre-spawn control path;
9. the official executor records A/tree(A) and actual B/tree(B) in reservation/result receipts;
10. `UNCONTROLLED_LOCAL_ADVISORY` is the only supported execution posture; it is explicitly not a sandbox.

Independent fifth review reported `APPROVE / READY TO MERGE`, with P1-R5/P1-R6/P1-R7 closed and 106/106 independent tests passing.

## 4. Scope of a possible GO

A GO should be deliberately narrow:

### Allowed

- prepare exactly one bounded Pilot package;
- use only Pilot-designated fixtures/scenarios;
- use the approved human-reference bindings;
- use an exact provider/model/version/settings configuration;
- use one exact request byte sequence/hash;
- use one exact adapter command and repository-relative cwd;
- use a minimal environment allowlist and credential profile reference without storing secrets;
- enforce explicit timeout, output cap, max runs and budget;
- write only to `.velantrim-continuum-pilot-runs` under the merged output containment rules;
- run only through `scripts/e0/execute_pilot.py` after the separately reviewed A→B authorization transition.

### Forbidden

- Evidence fixture/scenario IDs or Evidence wording;
- Evidence Lock creation;
- E0-C or E0-T Evidence execution;
- purchases, deployment, publication, deletion, production writes or irreversible external side effects;
- claims of sandbox/network/filesystem/process isolation;
- production credentials or unnecessary write-capable credentials;
- model aliases such as `latest` when an exact model/version can be pinned;
- changing protocol, Gold/Oracle, evaluator, prompts, fixtures, run config or manifest between A and B;
- treating Pilot output as scientific Evidence or production authorization.

## 5. Values that must be pinned before package A exists

The following are deliberately **not guessed** in this packet. They must be chosen and verified before package A is committed:

- owner GitHub login;
- exact Pilot fixture/scenario IDs;
- whether the bounded Pilot includes Capture only or an explicitly allowed Pilot Transfer fixture;
- exact authorized request JSON bytes and SHA-256;
- provider;
- exact model identifier/version;
- model settings (including temperature/seed where supported);
- exact adapter command;
- adapter cwd;
- environment allowlist;
- credential profile/scope reference, with no secret values committed;
- timeout;
- maximum output bytes;
- max runs;
- monetary/token budget and manual stop owner/contact;
- any allowed network dependency required by the chosen provider.

The current manifest template defaults to timeout `120s`, max output `1,048,576 bytes`, max runs `1`, but those defaults become authoritative only if the owner explicitly accepts them in the exact package.

## 6. Required package-construction sequence after GO

A GO does not permit skipping these steps:

1. re-read current merged `main` immediately before construction;
2. validate human-reference approval and Experiment 0 contracts/tests;
3. choose and record every value in Section 5;
4. construct the exact manifest and request under the Pilot namespace;
5. verify all reference/request/config hashes;
6. commit the immutable manifest as package commit **A** while Pilot remains `NOT_AUTHORIZED`;
7. compute A, tree(A), and exact manifest SHA-256 from committed bytes;
8. prepare direct-child activation **B**, changing only declared governance activation paths and materializing the exact canonical package authorization in `project-state.json`;
9. independently review B and the A→B transition before any real execution;
10. only after that review and exact canonical authorization, run the official executor;
11. stop after the bounded Pilot and inspect outputs/corrections;
12. do not create Evidence Lock or begin Evidence without a later, separate owner decision.

If any pinned input changes after package A, abort and construct a new package/amendment rather than silently rebinding authority.

## 7. Security posture to acknowledge

The supported posture is:

`UNCONTROLLED_LOCAL_ADVISORY`

with:

- `isolation_enforcement = NOT_ENFORCED`;
- `network_isolation = NOT_ENFORCED`;
- `filesystem_isolation = NOT_ENFORCED`;
- `process_isolation = NOT_ENFORCED`.

Therefore the Pilot must be treated as a controlled diagnostic execution, not as a sandbox. Credential minimization, side-effect prohibition, exact command/cwd/env binding, limits and stop rules are part of the authorization package.

## 8. Separate governance note

Branch protection / required-check enforcement on `main` is a separate governance control and should not be confused with scientific validity or Pilot authority. If it remains disabled, that risk should be consciously accepted or hardened before Evidence-grade work. It does not itself authorize or invalidate the bounded Pilot package.

## 9. Owner decision record

Choose exactly one outcome.

### Option A — GO to prepare the bounded package

```text
OWNER DECISION: GO — PREPARE BOUNDED PILOT PACKAGE
Decision ID: OD-PILOT-01
Pilot label: PILOT — NOT EVIDENCE
Execution posture: UNCONTROLLED_LOCAL_ADVISORY

I authorize preparation of one exact bounded Pilot package under the controls merged by PR #29.

This decision does not by itself authorize arbitrary execution. The exact manifest/request/configuration must be materialized as package commit A, followed by a separately reviewed direct-child activation B with canonical package authorization before scripts/e0/execute_pilot.py may run.

Evidence Lock remains NOT_CREATED.
E0-C/E0-T Evidence remain NOT_AUTHORIZED / NOT_RUN.
Production runtime remains NOT_AUTHORIZED.

Owner: <GitHub login>
UTC timestamp: <timestamp>
```

### Option B — NO-GO / DEFER

```text
OWNER DECISION: NO-GO / DEFER
Decision ID: OD-PILOT-01

Do not prepare or execute a real Pilot package at this time.
Keep experiment_0_pilot_status = NOT_AUTHORIZED.
Keep experiment_0_pilot_authorization = null.
Keep Evidence Lock NOT_CREATED and E0-C/E0-T NOT_AUTHORIZED / NOT_RUN.

Owner: <GitHub login>
UTC timestamp: <timestamp>
```

## 10. Stop boundary

The next action after an owner GO is **package preparation**, not Pilot execution and not Evidence.

The next action after a NO-GO is **none** unless the owner later reopens the decision.
