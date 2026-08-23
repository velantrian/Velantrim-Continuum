# OD-PILOT-01-PREP — Owner Preparation Decision

> **Status:** `GO — PREPARE BOUNDED PILOT PACKAGE`  
> **Preparation gate ID:** `OD-PILOT-01-PREP`  
> **Target future decision:** `OD-PILOT-01`  
> **Pilot label:** `PILOT — NOT EVIDENCE`  
> **Execution posture:** `UNCONTROLLED_LOCAL_ADVISORY`  
> **Owner:** `velantrian`  
> **Owner decision source:** explicit repository-owner instruction in the active Continuum workflow  
> **UTC recorded-at timestamp:** `2026-08-23T21:07:00Z`  
> **Authoritative main at decision:** `6bd61c17229d75792d1a6d510c197142d8a7b322`  
> **Authoritative main tree:** `15772f4e1c9f81b47e6494f7d786ded53f9ed946`

## Decision

I authorize **preparation of one exact bounded candidate Pilot package** under the controls merged by PR #29 and the preparation/adoption procedure merged by PR #33.

This preparation decision:

- does **not** adopt `OD-PILOT-01`;
- does **not** authorize any Pilot execution;
- does **not** authorize `scripts/e0/execute_pilot.py` to run;
- does **not** create package A;
- does **not** create activation B;
- does **not** create Evidence Lock;
- does **not** authorize E0-C or E0-T Evidence;
- does **not** authorize production runtime or freeze production architecture.

## Allowed next work

The preparation phase may:

1. re-read authoritative `main` and validate current Human Reference / Experiment 0 controls;
2. select and pin one exact Pilot-only fixture/scenario scope;
3. bind exact approved Capture Gold and/or Transfer Oracle as required by the selected arm;
4. construct exact candidate request bytes and SHA-256;
5. pin exact provider/model/version/settings;
6. pin explicit tool policy;
7. pin exact adapter command, repository-relative cwd, environment allowlist and credential profile/scope reference without secret values;
8. pin timeout, output cap, max runs, budget, network dependency and manual stop owner/contact;
9. prepare exact candidate manifest/request/configuration material for a later **separate** `OD-PILOT-01` adoption gate.

## Required stop boundary

Preparation must stop before package A if any mandatory package value cannot be derived or explicitly selected without guessing.

Before package A may exist with `owner_decision_status = ADOPTED`, a separate durable owner adoption of `OD-PILOT-01` for the exact pinned candidate package intent is required.

After that separate adoption:

`A → independent review A → B → independent review B/A→B → execution eligibility`

No stage silently authorizes the next stage.

## Current authority remains unchanged

- Human Reference = `HUMAN_REFERENCE_APPROVED / 14 of 14 ACCEPT`;
- `experiment_0_pilot_status = NOT_AUTHORIZED`;
- `experiment_0_pilot_authorization = null`;
- `OD-PILOT-01 = DRAFT — NOT ADOPTED`;
- Evidence Lock = `NOT_CREATED`;
- E0-C/E0-T Evidence = `NOT_AUTHORIZED / NOT_RUN`;
- production runtime = `NOT_AUTHORIZED`;
- architecture = `NOT_FROZEN`;
- ecosystem integration = `NOT_AUTHORIZED`;
- event sourcing = `NOT_REQUIRED`.

`PREP GO ≠ OD-PILOT-01 adoption ≠ package A approval ≠ activation B authorization ≠ Pilot execution ≠ Evidence ≠ Production Authorization`.
