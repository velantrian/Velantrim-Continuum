# Experiment 0 data contracts

This directory contains **Experiment-0-only** contracts and fixtures. It is not a production IDPS ontology or runtime package.

## Partitions

- `fixtures/capture/pilot/` — harness-validation wording; never architecture evidence.
- `fixtures/capture/evidence/` — held-out evidence wording; must not be used to tune the harness after evidence lock.
- `fixtures/transfer/scenarios.json` — one pilot and two evidence transfer scenarios.
- `gold/candidates/` — proposed capture Gold awaiting human experimenter review.
- `oracle/candidates/` — proposed transfer Oracle awaiting human experimenter review.
- `schema/` — bounded machine contracts for Experiment 0.

## Human Gold / Oracle gate

`AI_PROPOSED_DRAFT` is **not** authoritative Gold or Oracle.

Before a pilot or evidence readiness can be declared, a human experimenter must review the candidate semantics, correct them if needed, and explicitly approve a versioned reference artifact. The harness/evidence-lock validators fail closed while approval status is not `HUMAN_APPROVED`.

This prevents the evaluated AI system from creating or silently approving its own truth reference.

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
