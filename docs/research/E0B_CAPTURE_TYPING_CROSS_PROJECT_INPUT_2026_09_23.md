# E0-B Capture Typing — Cross-Project Research Input

STATUS:
CROSS-PROJECT RESEARCH INPUT
NOT CONTINUUM CANON
NOT PREREGISTRATION CHANGE
NOT IMPLEMENTATION
NOT PILOT AUTHORIZATION

Date: 2026-09-23

---

## AUTHORITY BOUNDARY

This document is cross-project research input.

It does not modify the receiving repository's Canon, runtime,
authorization state, architecture contract, implementation status,
preregistration or owner responsibilities.

Primary experiment evidence remains in:

velantrian/Eiti-Wizard-Lab
experiments/memory-governance-e0b/

RESEARCH INPUT != OWNER CANON
EXPERIMENT RESULT != ARCHITECTURE AUTHORIZATION
CROSS-PROJECT RELEVANCE != OWNERSHIP TRANSFER

---

## Primary evidence pointers

Repository: `velantrian/Eiti-Wizard-Lab`  
Branch: `exp/e0b-typing-reliability`  
Path: `experiments/memory-governance-e0b/`

Frozen artifacts:

- `HUMAN_SEGMENTATION_REFERENCE.json`  
  SHA-256: `2464ab24e1c6d6e25a6466380927dd0845f132cb58361bc7e48f6ce1ed5dbd2d`
- `HUMAN_SEGMENTATION_REFERENCE_FREEZE_RECEIPT.json`  
  SHA-256: `0d68cd4ae160a89049f9dcfcd38f2a7e35717c4ce25387e1ef5aafc258fce06c`

Human-answer fingerprint: `1cf0569676643cf920d7944cedc052c2710d8160d06cb06c78b1f93323e078b8`  
Verified live lab HEAD (`exp/e0b-typing-reliability`) after docs preserve: `8a8557706a5a73bf9d177052104129e5020aa88f`  
Historical post-freeze HEAD: `1f5ce9e2cd0117284f6ae6fb56847f50c0162487`  
Narrative companion: `experiments/memory-governance-e0b/RESEARCH_TRAJECTORY_AND_CURRENT_STATE.md`

Do not duplicate full primary evidence into this repository.


## Purpose

Relate E0-B to Continuum's existing Capture vs Transfer distinction.

Existing Continuum distinction:

- CAPTURE FAILURE: relevant state never becomes correct structured state.
- TRANSFER FAILURE: correct state exists but is distorted/lost during handoff.

E0-B probes a narrower upstream part of Capture:

NATURAL INTERACTION → SEMANTIC ACT / INTENT → TYPED REPRESENTATION

Key implication:

PERFECT TRANSFER CANNOT REPAIR A STATE THAT WAS CAPTURED INCORRECTLY

Or:

WRONG CAPTURE + PERFECT TRANSFER = PERFECTLY PRESERVED ERROR

## Explicit non-equivalence

- E0-B != CONTINUUM E0-C RESULT
- E0-B != IDPS EVIDENCE
- E0-B != CHANGE TO APPROVED CONTINUUM GOLD/ORACLE
- E0-B != PILOT AUTHORIZATION

This research input must **not** change Continuum's frozen Experiment 0 preregistration.

Do not modify `project-state.json`, `STATUS.md`, `IDPS_EXPERIMENT_0_PREREGISTRATION.md`, approved Capture Gold, approved Transfer Oracle, pilot authorization, or experiment activation state.

## Bounded current E0-B state (summary)

- FRESH_U0_COMPLETE = YES (N=30; 25 single-act / 5 two-act)
- Human captured count + intent wording only; exact textual boundaries not yet collected
- FREEZE_AUDIT_PASS_WITH_LIMITATION
- CURRENT_U0_SUFFICIENT_FOR_A0/A1/B = NO
- HUMAN_BOUNDARY_LAYER_REQUIRED_FIRST
- HUMAN_BOUNDARY_REFERENCE_U0b = NOT_CREATED
- GENERALIZATION_HUMAN_GOLD = NOT_CREATED
- A0 / A1 / B = NOT_RUN

No model-understanding accuracy result exists yet.

## Non-claims

Do not claim E0-B passed, Capture solved, Continuum Experiment 0 changed, approved Gold/Oracle changed, pilot authorization granted, or runtime activation authorized.


---

## 2026-09-27 methodology refinement — capture, transfer, continuation

Status: `RESEARCH METHOD REFINEMENT · NO RETROACTIVE VERDICT CHANGE · NO NEW EXPERIMENT ID · PILOT NOT AUTHORIZED`

The latest cross-project review sharpens the Continuum/TCE distinction into three independent questions:

1. **STATE EXTRACTION** — did capture correctly represent the source conversation?
2. **STATE TRANSFER** — did snapshot / interruption / restore preserve that captured state?
3. **CONTINUATION UTILITY** — did the restored state support correct continuation?

These must not be collapsed.

`GOOD CONTINUATION ≠ CORRECT SNAPSHOT`

`GOOD RESUME ≠ CORRECT EXTRACTION`

`WRONG STATE + GOOD CONTINUATION ≠ SUCCESS`

### Self-confirming snapshot error

Important failure pattern:

`FALSE EXTRACTION → FALSE SNAPSHOT → RESTORED MODEL BEHAVES CONSISTENTLY WITH FALSE SNAPSHOT → FALSE PASS`

Working analytical label: **SELF-CONFIRMING SNAPSHOT ERROR**.

This is not a formal Continuum enum and does not rewrite historical verdicts.

Example class: if the source dialogue never establishes that the user rejected a path, the snapshot must not record that path as rejected. A restored model later refusing that path cannot be counted as continuity success merely because it follows the erroneous snapshot.

### Non-selection preservation

Continuity state must preserve:

- `OFFERED ≠ SELECTED`
- `UNSELECTED ≠ REJECTED`
- `UNUSED ≠ DEFERRED`
- `DISCUSSION ≠ COMMITMENT`

For an existing non-selection case, the reference shape should preserve:

- current goal only when source-supported;
- live alternatives;
- `USER SELECTION = NONE / NOT ESTABLISHED`;
- rejected options only when explicit;
- deferred options only when explicit;
- critical unknowns;
- resume point = continue from the open choice without choosing on behalf of the user.

When revisiting this case, score independently:

- **CAPTURE** — fidelity to the source conversation;
- **TRANSFER** — preservation across interruption/restore;
- **RESUMPTION** — correctness/usefulness of continuation.

### Human reference boundary

`TRANSCRIPT-SUPPORTED STATE ≠ RETROSPECTIVE USER SELF-REPORT`

Later self-report may be retained separately, but it does not prove the earlier text made the hidden state observable.

### Relationship to existing E0-C / E0-T

This refinement fits the existing Experiment 0 decomposition rather than creating a parallel experiment:

- E0-C remains the Capture question;
- E0-T remains the Transfer question from correct supplied/oracle state;
- continuation utility is a separate downstream outcome.

No new experiment ID, preregistration change, Gold/Oracle change, pilot authorization, or activation is implied.

### Program order

Current global bounded priority remains `E0-B Issue #8 → U0b provenance disposition`.

This Continuum/TCE refinement becomes the next bounded action when returning to the continuity line.

`PRIORITY ≠ DEPENDENCY`
