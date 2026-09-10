# Experiment 0 data contracts

This directory contains **Experiment-0-only** contracts and fixtures. It is not a production IDPS ontology or runtime package.

## Partitions

- `fixtures/capture/pilot/` — harness-validation wording; never architecture evidence.
- `fixtures/capture/evidence/` — held-out evidence wording; must not be used to tune the harness after evidence lock.
- `fixtures/transfer/scenarios.json` — one pilot and two evidence transfer scenarios.
- `gold/candidates/` — historical AI-proposed Capture Gold candidates; not authoritative references.
- `oracle/candidates/` — historical AI-proposed Transfer Oracle candidates; not authoritative references.
- `gold/approved/capture-gold.v0.1.json` — human-approved Capture Gold reference.
- `oracle/approved/transfer-oracle.v0.1.json` — human-approved Transfer Oracle reference.
- `approval/human-reference-approval.v0.2.json` — human approval record binding the approved references.
- `schema/` — bounded machine contracts for Experiment 0.

## Human Gold / Oracle gate

`AI_PROPOSED_DRAFT` is **not** authoritative Gold or Oracle.

Human Reference review is complete: the approved Capture Gold and Transfer Oracle are bound by `approval/human-reference-approval.v0.2.json` with `HUMAN_APPROVED` status. Candidate artifacts remain historical inputs and do not become authoritative merely because they exist.

Pilot preflight and Evidence Lock validation fail closed on their respective approved-reference and approval bindings. This prevents the evaluated AI system from creating or silently approving its own truth reference.

Human Reference approval does **not** adopt `OD-PILOT-01`, authorize Pilot execution, create an Evidence Lock, or authorize E0-C/E0-T Evidence.

## C2 pre/post clarification reference

If a scripted clarification materially adds information, the reference distinguishes:

- `items_by_family` — what is justified by the original visible interaction;
- `post_clarification_items_by_family` — what is justified after the preregistered clarification answer.

C1 must never be scored against information that only appears in a C2 clarification response. Pre- and post-clarification outputs are evaluated separately.

## Revision, negative knowledge and contested claims

- Revision fixtures preserve both superseded and currently active rules where needed to test lifecycle fidelity.
- Fabrication-bait fixtures may preserve supported negative knowledge such as `NO_APPROVAL_RULE_ADOPTED`; such a truthful negative item is not a fabricated authorization.
- Conflicting claims use an explicit `value` field for claim content. Lifecycle status describes the state item, not the truth value asserted by the source.

## Leakage boundary

The following are evaluator-only and must never be inserted into model prompts:

- `expected_item_refs`;
- `match_spec`;
- HARD FAIL bindings;
- Gold/Oracle content;
- outcome labels;
- evidence-lock metadata.

## Research boundary

These artifacts do not authorize E0-C/E0-T evidence, production runtime, event sourcing, state-tier canon, or ecosystem integration.
