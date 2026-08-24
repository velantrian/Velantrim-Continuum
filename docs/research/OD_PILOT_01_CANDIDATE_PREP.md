# OD-PILOT-01 — Candidate Preparation Worksheet

> **Status:** `PREPARATION ONLY — NOT ADOPTED — NOT EXECUTABLE`  
> **Preparation gate:** `OD-PILOT-01-PREP = GO — PREPARE BOUNDED PILOT PACKAGE`  
> **Authoritative baseline:** `main@6bd61c17229d75792d1a6d510c197142d8a7b322`  
> **Pilot label:** `PILOT — NOT EVIDENCE`

This worksheet records the safest bounded candidate that can currently be derived from repository state without inventing provider/model/credential choices. It is **not package A** and is **not an OD-PILOT-01 adoption record**.

## 1. Candidate arm and fixture

Selected preparatory candidate:

- arm: `Capture Pilot only`;
- fixture set: `experiments/e0/fixtures/capture/pilot/fixtures.json`;
- fixture ID: `F1-P-A`;
- family: `F1`;
- clarification mode: `NONE`;
- interaction: `Do not publish the release note without my explicit approval.`;
- expected item ref: `f1_restriction`;
- hard-fail class: `LOST_CRITICAL_RESTRICTION`.

### Why F1-P-A

`F1-P-A` is the smallest repository-defined Pilot-only Capture fixture with no clarification turn and a direct critical-restriction invariant. Selecting it minimizes the first Pilot's moving parts and avoids Transfer-specific Oracle requirements.

No Evidence fixture/scenario is selected.

## 2. Human-reference bindings

Required for this Capture-only candidate:

- Human Reference approval path: `experiments/e0/approval/human-reference-approval.v0.2.json`;
- approved Capture Gold path: `experiments/e0/gold/approved/capture-gold.v0.1.json`;
- approved Capture Gold SHA-256: `9b806fdb44ff84ba0456d0dd480c328398915ca40f9de7f9e0232452678e2025`.

The exact Human Reference approval SHA-256 must still be recomputed/pinned from authoritative bytes before adoption/package A.

Transfer Oracle is `N/A` for this Capture-only candidate. If the scope changes to include any Transfer Pilot scenario, exact approved Transfer Oracle path + SHA-256 becomes mandatory and this worksheet must be revised before adoption.

## 3. Tool and side-effect policy

Preparatory selection:

- tool policy: `NO_TOOLS`;
- purchases: forbidden;
- deployment: forbidden;
- publication: forbidden;
- deletion: forbidden;
- production writes: forbidden;
- irreversible external side effects: forbidden;
- production credentials: forbidden;
- unnecessary write-capable credentials: forbidden.

Execution posture remains:

`UNCONTROLLED_LOCAL_ADVISORY`

with all isolation fields `NOT_ENFORCED`. This is not a sandbox.

## 4. Proposed bounded limits — not yet owner-adopted

Repository template defaults are retained as the current candidate proposal:

- timeout: `120 seconds`;
- max output: `1,048,576 bytes`;
- max runs: `1`;
- output destination: `.velantrim-continuum-pilot-runs`.

These values are **proposed, not yet adopted**. They become authoritative only inside the later exact owner adoption/package intent.

## 5. Values that remain unresolved and must NOT be guessed

The repository does not currently provide a canonical real Pilot provider/model/adapter configuration. The test suite contains only synthetic examples and must not be promoted into real Pilot authority.

The following remain intentionally `UNPINNED`:

- exact request JSON structure/bytes for the real adapter contract;
- exact request SHA-256;
- provider;
- exact model identifier/version;
- model settings;
- adapter command;
- adapter cwd if different from repository root;
- environment allowlist;
- credential profile reference;
- credential scope;
- allowed network dependency;
- monetary/token budget;
- manual stop contact details beyond repository-owner identity;
- exact Human Reference approval SHA-256.

Test-only values such as provider `example`, model `model-v1`, `pilot-minimal`, and the Python one-line synthetic adapter are **not valid production/Pilot selections** and are not adopted here.

## 6. Current stop boundary

Because mandatory provider/model/adapter/request/credential/budget values are still unpinned, preparation MUST stop before:

- OD-PILOT-01 adoption;
- package commit A;
- activation B;
- `scripts/e0/execute_pilot.py` execution.

The next safe action is to resolve the remaining exact candidate values, then present the complete content-bound package intent for the separate owner adoption gate.

## 7. Authority remains closed

- `experiment_0_pilot_status = NOT_AUTHORIZED`;
- `experiment_0_pilot_authorization = null`;
- `OD-PILOT-01 = DRAFT — NOT ADOPTED`;
- Evidence Lock = `NOT_CREATED`;
- E0-C/E0-T Evidence = `NOT_AUTHORIZED / NOT_RUN`;
- production runtime = `NOT_AUTHORIZED`.

`Candidate preparation ≠ OD adoption ≠ package A ≠ activation B ≠ Pilot execution ≠ Evidence ≠ Production Authorization`.
