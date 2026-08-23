# OD-PILOT-01 — Owner Decision Packet

> **Status:** `PREPARED — OWNER PREPARATION DECISION PENDING`  
> **Preparation gate ID:** `OD-PILOT-01-PREP`  
> **Decision:** whether to authorize **preparation of one future bounded `PILOT — NOT EVIDENCE` package only** under the controls merged by PR #29.  
> **Prepared from authoritative merged main:** `fc5fa1b16f5dda04fe2fe34d0c66f09856c33d2f`  
> **PR #29 independently reviewed head:** `78ca9d95132878b70dc7286de5e136736812866b`  
> **Important:** this preparation packet does **not** adopt `OD-PILOT-01`, does not authorize any Pilot execution, does not create canonical activation B, and does not create Evidence authority.

## 1. Decision in plain language

The control plane needed to construct and verify a bounded Pilot package is merged. The owner must now decide only whether to permit the next **preparation** phase.

There are two valid outcomes:

- `GO — PREPARE BOUNDED PILOT PACKAGE`: authorize preparation of one exact bounded candidate package under the rules below. This does **not** adopt `OD-PILOT-01` and does **not** authorize any Pilot execution.
- `NO-GO / DEFER`: leave canonical state unchanged and do not prepare or execute a real Pilot.

A later, separate and durable owner-adoption gate is required before `OD-PILOT-01` may become `ADOPTED`. No execution authority is created by this packet or by a preparation GO.

No other state should be inferred from this document.

## 2. Current authority state

Until separate owner adoption and a subsequently reviewed canonical activation transition:

- `experiment_0_pilot_status = NOT_AUTHORIZED`;
- `experiment_0_pilot_authorization = null`;
- `OD-PILOT-01` remains `DRAFT — NOT ADOPTED`;
- Human Reference remains `HUMAN_REFERENCE_APPROVED` with `14 / 14 ACCEPT`;
- merged PR #29 controls remain unchanged;
- Evidence Lock remains `NOT_CREATED`;
- E0-C Evidence remains `NOT_AUTHORIZED / NOT_RUN`;
- E0-T Evidence remains `NOT_AUTHORIZED / NOT_RUN`;
- production runtime remains `NOT_AUTHORIZED`;
- production architecture remains `NOT_FROZEN`;
- ecosystem integration remains `NOT_AUTHORIZED`;
- event sourcing remains `NOT_REQUIRED`.

`PR #29 merged ≠ preparation GO ≠ OD-PILOT-01 adoption ≠ package authorization ≠ Pilot execution ≠ Evidence Lock ≠ Evidence authorization ≠ production authorization`.

## 3. What PR #29 established

The merged controls provide a machine-verifiable construction rule for a future authorization:

1. package commit **A** contains the immutable Pilot manifest;
2. A is created before its commit/tree identity is needed by canonical activation authority, avoiding self-reference;
3. activation commit **B** must be the single direct child of A;
4. A→B may change only declared bounded governance paths;
5. manifest bytes are proven as an exact regular `100644` Git blob in A;
6. canonical authority is proven as exact regular `100644 project-state.json` Git blob in B;
7. symlink, executable mode, submodule, missing blob, external mutable authority, or working-tree/blob mismatch fail closed;
8. strict worktree checks and Python bytecode suppression protect the pre-spawn control path;
9. the official executor records A/tree(A) and actual B/tree(B) in reservation/result receipts;
10. `UNCONTROLLED_LOCAL_ADVISORY` is the only supported execution posture; it is explicitly not a sandbox.

Independent fifth review reported `APPROVE / READY TO MERGE`, with P1-R5/P1-R6/P1-R7 closed and 106/106 independent tests passing.

This packet does not reinterpret or weaken those controls.

## 4. Scope of a possible preparation GO

A preparation GO is deliberately narrow.

### Allowed

- select and pin the exact scope for one bounded candidate Pilot package;
- prepare exact candidate manifest/request/configuration material;
- use only Pilot-designated fixtures/scenarios;
- bind the approved human-reference artifacts required by the selected Pilot arm;
- use an exact provider/model/version/settings configuration;
- use one exact request byte sequence/hash;
- pin an explicit tool policy;
- use one exact adapter command and repository-relative cwd;
- use a minimal environment allowlist and credential profile reference without storing secrets;
- pin explicit timeout, output cap, max runs and budget;
- prepare package A only through the separate adoption/construction sequence in Section 6.

### Forbidden

- any Pilot execution;
- Evidence fixture/scenario IDs or Evidence wording;
- Evidence Lock creation;
- E0-C or E0-T Evidence execution;
- purchases, deployment, publication, deletion, production writes or irreversible external side effects;
- claims of sandbox/network/filesystem/process isolation;
- production credentials or unnecessary write-capable credentials;
- model aliases such as `latest` when an exact model/version can be pinned;
- changing protocol, Gold/Oracle, evaluator, prompts, fixtures, run config or manifest between A and B;
- treating Pilot output as scientific Evidence or production authorization.

A preparation GO does **not** permit `scripts/e0/execute_pilot.py` to run.

## 5. Values that must be pinned before package A exists

The following are deliberately **not guessed** in this packet. They must be chosen and verified before package A is committed:

- owner GitHub login;
- exact Pilot fixture/scenario IDs;
- whether the bounded Pilot is Capture-only or includes an explicitly allowed Pilot Transfer scenario;
- exact authorized request JSON bytes and SHA-256;
- provider;
- exact model identifier/version;
- model settings, including temperature/seed where supported;
- **tool policy**, exactly one of:
  - `NO_TOOLS`, or
  - an exact minimal tool allowlist, or
  - explicit `N/A` only when the selected adapter/provider exposes no tool surface;
- exact adapter command;
- adapter cwd;
- environment allowlist;
- credential profile/scope reference, with no secret values committed;
- timeout;
- maximum output bytes;
- max runs;
- monetary/token budget and manual stop owner/contact;
- any allowed network dependency required by the chosen provider;
- exact relevant protocol/prompt/template/run-configuration identities where they influence the selected Pilot execution.

### Required human-reference bindings

Every candidate package must bind the exact Human Reference approval artifact and the approved reference artifact(s) required by the selected arm.

- **Capture Pilot:** exact approved Capture Gold path + SHA-256 are mandatory.
- **Transfer Pilot:** exact approved Transfer Oracle path + SHA-256 are mandatory. A Transfer Pilot must not be accepted merely because some unrelated approved reference is present.
- If a package legitimately exercises both bounded Pilot arms, both exact approved references are mandatory.

This is a package-construction requirement even if a lower-level validator currently checks only that `approved_references` is non-empty.

The current manifest template defaults to timeout `120s`, max output `1,048,576 bytes`, max runs `1`, but those defaults become authoritative only if the owner explicitly accepts them in the exact package.

## 6. Required decision / package / activation sequence

No stage may silently imply the next stage.

### Phase 0 — preparation decision

1. owner chooses `GO — PREPARE BOUNDED PILOT PACKAGE` or `NO-GO / DEFER` under preparation gate `OD-PILOT-01-PREP`;
2. a GO permits package preparation only and leaves `OD-PILOT-01 = DRAFT — NOT ADOPTED` and Pilot `NOT_AUTHORIZED`.

### Phase 1 — pin exact candidate package contents

3. re-read current merged `main` immediately before preparation;
4. validate Human Reference approval and Experiment 0 contracts/tests;
5. choose and record every value in Section 5, including arm-specific Gold/Oracle bindings and explicit tool policy;
6. construct the exact candidate manifest/request/configuration bytes and verify all hashes.

### Phase 2 — separate owner adoption gate

7. before a manifest may truthfully carry `owner_decision_status = ADOPTED`, obtain a **separate explicit durable owner adoption of `OD-PILOT-01`** for the exact pinned candidate package intent;
8. that adoption record must be distinct from `OD-PILOT-01-PREP`, record owner identity, UTC timestamp, exact manifest SHA-256 and the pinned scope/configuration, and explicitly state that adoption alone still does not authorize execution;
9. because package commit A does not yet exist at the instant of pre-commit adoption, A/tree(A) are not self-referential manifest fields; their immutable identity is established after A is committed and later bound by canonical activation B under the PR #29 controls.

If the authoritative OD-PILOT-01 adoption template is not consistent with this constructible ordering at the time of real adoption, stop and reconcile that documentation before proceeding. This packet itself does not adopt or rewrite OD-PILOT-01.

### Phase 3 — construct and independently review package A

10. only after the separate adoption gate, commit the immutable adopted manifest as package commit **A** while canonical Pilot state remains `NOT_AUTHORIZED`;
11. compute A, tree(A), and exact manifest SHA-256 from committed bytes;
12. **independently review package A before activation B exists**, checking the exact committed manifest, selected Pilot-only IDs, arm-specific Human Reference bindings, request hash, provider/model/settings, explicit tool policy, credentials scope, command/cwd/env, limits, budget and side-effect prohibition;
13. if A review is not `APPROVE`, do not create B; prepare a new/revised package instead.

### Phase 4 — construct and review activation B

14. only after independent approval of A, prepare direct-child activation **B**;
15. B may change only declared governance activation paths and must materialize the exact canonical package authorization in `project-state.json`, binding A/tree(A), manifest path/SHA, `DIRECT_CHILD_ONLY` and bounded activation paths;
16. independently review B and the full A→B transition;
17. if B/A→B review is not `APPROVE`, do not execute.

### Phase 5 — execution eligibility

18. only after all preceding gates are satisfied and exact canonical authorization is valid may the official executor become eligible to run;
19. any actual run remains exactly one bounded `PILOT — NOT EVIDENCE` execution under the pinned package;
20. stop after the bounded Pilot and inspect outputs/corrections;
21. do not create Evidence Lock or begin Evidence without a later, separate owner decision.

If any pinned input changes after package A, abort and construct a new package rather than silently rebinding authority.

## 7. Security posture to acknowledge

The supported posture is:

`UNCONTROLLED_LOCAL_ADVISORY`

with:

- `isolation_enforcement = NOT_ENFORCED`;
- `network_isolation = NOT_ENFORCED`;
- `filesystem_isolation = NOT_ENFORCED`;
- `process_isolation = NOT_ENFORCED`.

Therefore the Pilot must be treated as a controlled diagnostic execution, not as a sandbox. Credential minimization, side-effect prohibition, exact command/cwd/env/tool-policy binding, limits and stop rules are part of the candidate package.

## 8. Separate governance note

Branch protection / required-check enforcement on `main` is a separate governance control and should not be confused with scientific validity or Pilot authority. If it remains disabled, that risk should be consciously accepted or hardened before Evidence-grade work. It does not itself authorize or invalidate the bounded Pilot package.

## 9. Preparation decision record

Choose exactly one outcome. These records use **Preparation gate ID `OD-PILOT-01-PREP`**, not the eventual adoption identity `OD-PILOT-01`.

### Option A — GO to prepare the bounded package

```text
OWNER PREPARATION DECISION: GO — PREPARE BOUNDED PILOT PACKAGE
Preparation gate ID: OD-PILOT-01-PREP
Target future decision: OD-PILOT-01
Pilot label: PILOT — NOT EVIDENCE
Execution posture: UNCONTROLLED_LOCAL_ADVISORY

I authorize preparation of one exact bounded candidate Pilot package under the controls merged by PR #29.

This preparation decision does not adopt OD-PILOT-01 and does not authorize any Pilot execution.
Before package A is committed with owner_decision_status = ADOPTED, a separate durable owner adoption of OD-PILOT-01 for the exact pinned candidate package intent is required.
Package A must then receive independent review before any direct-child activation B is constructed.
Activation B / A→B must receive a separate independent review before execution can become eligible.

Evidence Lock remains NOT_CREATED.
E0-C/E0-T Evidence remain NOT_AUTHORIZED / NOT_RUN.
Production runtime remains NOT_AUTHORIZED.

Owner: <GitHub login>
UTC timestamp: <timestamp>
```

### Option B — NO-GO / DEFER

```text
OWNER PREPARATION DECISION: NO-GO / DEFER
Preparation gate ID: OD-PILOT-01-PREP
Target future decision: OD-PILOT-01

Do not prepare or execute a real Pilot package at this time.
Keep OD-PILOT-01 DRAFT — NOT ADOPTED.
Keep experiment_0_pilot_status = NOT_AUTHORIZED.
Keep experiment_0_pilot_authorization = null.
Keep Human Reference HUMAN_REFERENCE_APPROVED with 14 / 14 ACCEPT.
Keep merged PR #29 controls unchanged.
Keep Evidence Lock NOT_CREATED and E0-C/E0-T NOT_AUTHORIZED / NOT_RUN.

Owner: <GitHub login>
UTC timestamp: <timestamp>
```

## 10. Stop boundary

The next action after a preparation GO is **pinning and preparing candidate package contents**, not Pilot execution and not Evidence.

The next authority transition after candidate contents are pinned is the **separate `OD-PILOT-01` owner-adoption gate**. It is not implicit in preparation GO.

Package A must be independently reviewed before B is constructed. B/A→B must be independently reviewed before any execution becomes eligible.

The next action after a NO-GO is **none** unless the owner later reopens the preparation decision.
