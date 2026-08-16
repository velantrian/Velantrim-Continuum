# 🌎 Velantrim Continuum / IDPS — Audit & Future Work Ledger

**Repository:** `velantrian/Velantrim-Continuum`  
**Default branch:** `main`  
**Role:** documentation / audit / governance only  
**Last live reconciliation:** 2026-08-17  
**Audited checkpoint:** `main@1469865e61cb94b0d10da450cd635cb71cad1330`  
**Semantic project-state owner:** `project-state.json`  
**Experiment 0 semantic owner:** `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`  
**Human-reference gate:** Issue #9 + `experiments/e0/review/ISSUE_9_HUMAN_REVIEW_PROTOCOL.md`  
**Notion mirror:** `🌎 Velantrim Continuum — IDPS Research 🪎`

> **DO NOT AUTO-SELECT NEXT MILESTONE.**
>
> A future-work item, priority, experiment sequence, open Issue, successful harness test, AI recommendation, or research result does **not** authorize implementation, evidence execution, production architecture, runtime, or ecosystem integration.

Before future implementation/evidence work:

```text
resolve live main / PRs / Issues / exact CI
→ read project-state.json + CURRENT_STATE
→ read canonical preregistration / owning protocol
→ reconcile this ledger
→ verify current authorization / human gates
→ select ONE bounded scope only if explicitly admitted
→ only then execute it
```

If no scope is proven appropriate: **STOP WITH AUDIT REPORT.**

---

## 1. Fresh live checkpoint — 2026-08-17

Live audit established:

```text
main                                      1469865e61cb94b0d10da450cd635cb71cad1330
signature                                 VERIFIED / valid
open PRs                                  0
open Issues                               Issue #9 only
selected workstream                       EXPERIMENT_0_EVALUATION_CONTRACT_AND_HARNESS_READINESS
workstream status                         ACTIVE
preregistration hardening                 DONE
schemas / fixtures                        DONE
bounded deterministic evaluator/harness   IMPLEMENTED
human-review engineering preparation      READY_FOR_HUMAN_ATTESTATION
Capture Gold candidate                    AI_PROPOSED_DRAFT
Transfer Oracle candidate                 AI_PROPOSED_DRAFT
HUMAN_APPROVED                            NO
Pilot                                     NOT RUN
Evidence readiness                        false
Evidence Lock                             NONE
E0-C evidence                             NOT STARTED
E0-T evidence                             NOT STARTED
Architecture Reassessment                 NOT REACHED
production architecture                   NOT FROZEN
production runtime                        NOT AUTHORIZED
ecosystem integration                     NOT AUTHORIZED
event sourcing required                   false
state tiers canonical                     false
```

The broad machine-state field still records the harness-readiness workstream as active / implementation in progress. Repository evidence under that workstream has advanced to the human-attestation gate. This is not permission to promote the candidates or run Pilot/Evidence.

### Human-reference integrity boundary

Current candidates remain explicitly non-authoritative:

- `experiments/e0/gold/candidates/capture-gold.ai-proposed.json` → `AI_PROPOSED_DRAFT`;
- `experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json` → `AI_PROPOSED_DRAFT`.

The review protocol is `READY_FOR_HUMAN_ATTESTATION`, but every item-level decision is still `PENDING`. A generic instruction such as `continue`, `finish it`, an AI pre-review, green CI, or a machine-valid attestation structure **does not prove human semantic approval**.

### Current exact evidence anchors

- `main@1469865e61cb94b0d10da450cd635cb71cad1330`
- State control plane run `31969581292` — SUCCESS
- Experiment 0 harness run `31969581298` — SUCCESS
- Issue #9 — OPEN
- candidate Gold blob `adb873741f663c53a8b2cd0459139e1ce9b13520`
- candidate Oracle blob `3e9b79ccc48408e4857de19415c6d7a1e6ccf588`
- review protocol blob `28f7e94945361e2bef1ce58fbade8a24012c1f0e`

### Global revalidation triggers

Re-audit relevant entries when any of these changes:

- newer `main` changes `project-state.json`, preregistration, review candidates, evaluator/harness, approval gate, evidence lock or experiment fixtures;
- Issue #9 closes/reopens or gains a valid item-level human attestation;
- candidate or approved Gold/Oracle hashes change;
- Pilot is run or corrected;
- evidence lock is created/replaced;
- E0-C/E0-T authorization or evidence status changes;
- mandatory Architecture Reassessment is reached;
- runtime/integration/authority flags change.

---

# 2. Durable future-work / audit queue

## IDPS-FW-001 — Human Gold / Oracle attestation gate

**State:** `BLOCKED / HUMAN_ACTION_REQUIRED`  
**Priority:** P0 research-integrity gate  
**Suggested audit sequence:** 1  
**Implementation authorized:** NO — no new engineering before human semantic decision unless correcting a reviewed candidate  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** Issue #9; readiness PRs #10–#12 historical  
**Last verified:** 2026-08-17  
**Evidence anchor:** Issue #9; review protocol; candidate Gold/Oracle at audited main  
**Revalidation trigger:** item-level human decision; candidate hash/content change; approved artifacts appear.

### Question
Has a human experimenter actually reviewed F1, F2 pre/post, F3, F4, F5 pre/post, F6, F7, F8 pre/post, T-PILOT-01, T-EVIDENCE-01 and T-EVIDENCE-02 and recorded `ACCEPT / REVISE / REJECT`?

### Why it matters
The system under evaluation must not create or approve its own truth reference.

### Current evidence
No. Issue #9 remains open, all checklist decisions remain pending, and both reference candidates still say `AI_PROPOSED_DRAFT`.

### Alternative explanations
A human may later approve or request revisions; machine hash/structure validation alone cannot establish that semantic act.

### Files / components to inspect
Issue #9, review protocol, candidate Gold/Oracle, approval record/approved directories if they later appear, approval validator/workflow.

### Required audit
Verify item-level decision record, reviewer role/provenance, exact candidate hashes, exact approved artifact hashes, and absence of unresolved semantic revisions.

### Required experiment / reproduction
None before valid human approval.

### Preconditions
Actual human semantic review.

### Non-goals
Do not infer approval from generic chat commands, AI pre-review, ownership of GitHub account, CI success, or a syntactically valid attestation.

### Authority boundaries
Machine gate verifies structure/binding; it does not prove human authorship or semantic approval.

### Falsification / closure condition
This gate is not closed while any review row is pending/revise/reject or authoritative approved artifacts are absent/unbound.

### Exit criteria
Valid item-level human attestation + versioned `HUMAN_APPROVED` Gold/Oracle + exact binding validation through a bounded reviewable PR.

### Possible outcomes
`ACCEPT_AND_MATERIALIZE`, `REVISE_AND_REVIEW_AGAIN`, `REJECT`, `BLOCKED_HUMAN_ACTION_REQUIRED`.

---

## IDPS-FW-002 — Harness-validation Pilot

**State:** `BLOCKED / NOT_RUN`  
**Priority:** P1  
**Suggested audit sequence:** 2  
**Implementation authorized:** NO until IDPS-FW-001 closes  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** Issue #9  
**Last verified:** 2026-08-17  
**Evidence anchor:** `project-state.json`; Issue #9; review protocol  
**Revalidation trigger:** valid approved Gold/Oracle; real provider/model adapter availability; Pilot run.

### Question
Does the real model/provider-neutral harness behave correctly on pilot fixtures when evaluated against human-approved references?

### Why it matters
Synthetic/unit tests prove machinery behavior, not a real Experiment 0 Pilot.

### Current evidence
Pilot has not run and is intentionally blocked on human reference approval.

### Alternative explanations
A model adapter may be unavailable; pilot may reveal evaluator/harness defects; no defect may appear.

### Files / components to inspect
Pilot fixtures, approved references, adapter runner, run manifest, evaluator outputs.

### Required audit / experiment
Run pilot fixtures only, label every result `PILOT — NOT EVIDENCE`, record model/adapter/config/prompts/provenance and pre/post clarification artifacts.

### Preconditions
Valid human references and a legitimate executable model/provider adapter.

### Non-goals
No evidence claims, held-out evidence consumption, architecture selection, or production runtime.

### Authority boundaries
Pilot success does not authorize E0-C/E0-T evidence.

### Falsification / closure condition
If only fake/replay/synthetic adapters are used, a real Pilot claim is invalid.

### Exit criteria
Pilot completed and bounded defects corrected or explicitly recorded.

### Possible outcomes
`PILOT_PASS`, `PILOT_DEFECT_FOUND`, `PILOT_BLOCKED_NO_MODEL_ADAPTER`.

---

## IDPS-FW-003 — Evidence Lock

**State:** `DEFERRED / NOT_CREATED`  
**Priority:** P1  
**Suggested audit sequence:** 3  
**Implementation authorized:** NO until valid human refs + Pilot + allowed corrections  
**Runtime capability change:** NO  
**Authority impact:** experiment-governance only after later lock  
**Last verified:** 2026-08-17  
**Evidence anchor:** `project-state.json`: lock SHA `null`; lock validator; Issue #9  
**Revalidation trigger:** Pilot completion/correction; reference/schema/evaluator/config changes; lock creation.

### Question
Are all evidence-critical artifacts stable enough to hash-lock reproducibly?

### Why it matters
Locking before Pilot/corrections would freeze known-unstable experiment machinery or create false evidence readiness.

### Required audit
Bind exact paths + SHA-256 for protocol/schema/evidence fixtures/human-approved references/evaluator/run config/prompts/randomization and approval provenance.

### Preconditions
IDPS-FW-001 and Pilot closure; no open allowed corrections.

### Non-goals
Evidence Lock is not evidence execution authorization.

### Exit criteria
Valid lock committed/verified and semantic project state reconciled, then **STOP**.

### Possible outcomes
`LOCK_READY`, `LOCK_NOT_READY`, `REQUIRES_CORRECTION`.

---

## IDPS-FW-004 — E0-C Capture Isolation evidence

**State:** `NOT_AUTHORIZED / NOT_STARTED`  
**Priority:** P1 research  
**Suggested audit sequence:** 4  
**Implementation authorized:** NO by this ledger  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Last verified:** 2026-08-17  
**Evidence anchor:** `project-state.json`; preregistration  
**Revalidation trigger:** valid Evidence Lock + separate E0-C authorization.

### Question
Under preregistered conditions, how accurately can natural interaction be captured into structured process state?

### Required experiment
Only after a separate authorization, execute E0-C exactly against locked references/configuration and preserve per-family outcomes + separate HARD FAIL.

### Non-goals
Do not infer transfer sufficiency from capture results or change production architecture.

### Exit criteria
Locked E0-C evidence generated, integrity-checked, then analyzed separately.

---

## IDPS-FW-005 — Capture analysis

**State:** `DEFERRED / NOT_REACHED`  
**Priority:** P1  
**Suggested audit sequence:** 5  
**Implementation authorized:** NO until E0-C evidence exists  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Revalidation trigger:** completed locked E0-C evidence.

### Question
Which failures are true capture failures, which are clarification-policy effects, and what state dimensions are reliably externalizable?

### Why it matters
Transfer interpretation is contaminated if capture failure is not isolated first.

### Required audit
Analyze primary outcomes, mismatch atoms, HARD FAILs, C1/C2 clarification cost and family-specific error structure without collapsing into one score.

### Exit criteria
Explicit Capture analysis precedes E0-T evidence interpretation.

---

## IDPS-FW-006 — E0-T Transfer Isolation evidence

**State:** `NOT_AUTHORIZED / NOT_STARTED`  
**Priority:** P1 research  
**Suggested audit sequence:** 6  
**Implementation authorized:** NO by this ledger  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Last verified:** 2026-08-17  
**Evidence anchor:** preregistration; transfer Oracle candidate currently non-authoritative  
**Revalidation trigger:** human-approved Oracle + lock + Capture analysis + separate E0-T authorization.

### Question
Given correct Oracle State, what representation is sufficient for a successor to continue functionally?

### Required experiment
Compare T0–T4 from the same Oracle State and keep representation generation separate from successor interpretation.

### Non-goals
Do not inject E0-C capture errors into transfer arms; T4 must not silently truncate.

### Exit criteria
Locked E0-T evidence under the preregistered same-Oracle design.

---

## IDPS-FW-007 — Minimal sufficient substrate

**State:** `RESEARCH_HYPOTHESIS / DEFERRED`  
**Priority:** P1 architecture question  
**Suggested audit sequence:** 7 — interpret only after Experiment 0 evidence  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Evidence anchor:** primary null hypothesis in `project-state.json` + preregistration  
**Revalidation trigger:** E0-C/E0-T analyses and Architecture Reassessment.

### Question
Is a carefully maintained current-state representation such as `state.json` sufficient, or does a more complex substrate deliver a material capability gain?

### Alternative explanations
Simple current state may win; event log may help only replay/audit/recovery; reconstructive manifest may help rationale; different tasks may create trade-offs.

### Required audit
Test simplest baseline before event sourcing, graph, database-heavy substrate or workflow engine. Use preregistered `MATERIAL_GAIN / NO_MATERIAL_GAIN / TRADEOFF_INCONCLUSIVE` logic rather than arbitrary threshold worship.

### Non-goals
No event-sourcing requirement or production datastore choice before reassessment.

### Exit criteria
Evidence-backed architecture conclusion at mandatory reassessment.

---

## IDPS-FW-008 — External side-effect state

**State:** `CANDIDATE / FUTURE_RESEARCH`  
**Priority:** P2  
**Suggested audit sequence:** 8  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** future transactional continuity only  
**Revalidation trigger:** post-Experiment-0 architecture decision or selected transactional-continuity experiment.

### Question
What durable operation state is necessary to continue safely across lost responses/restarts?

### Required invariant

```text
INTENT → DISPATCHED → COMMITTED | FAILED | UNKNOWN
```

`UNKNOWN` must remain first-class when blind retry can duplicate an irreversible effect.

### Non-goals
No transaction coordinator, effect runner or production side-effect authority now.

### Exit criteria
A future bounded experiment proves the minimum required operation-state contract.

---

## IDPS-FW-009 — Idempotency / replay / lost acknowledgement

**State:** `CANDIDATE / FUTURE_RESEARCH`  
**Priority:** P2  
**Suggested audit sequence:** 9  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Revalidation trigger:** transactional-continuity scope selection.

### Question
How do crash, restart, duplicate execution, partial effects, replay and lost acknowledgements affect process continuation?

### Required experiment
Only after a bounded failure model exists; distinguish application idempotency, effect identity, replay and ambiguous completion.

### Non-goals
No generic distributed systems framework by analogy.

### Exit criteria
Reproduced failure classes and bounded contract, or defer.

---

## IDPS-FW-010 — Process identity boundary

**State:** `PERMANENT_CONCEPTUAL_BOUNDARY / INVESTIGATE_LATER`  
**Priority:** P1  
**Suggested audit sequence:** 10  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE

### Core distinction

```text
functional process continuity
!= hidden cognitive-state identity
!= model identity
!= Mentaury personal/identity continuity
```

### Question
What identity, if any, must a long-lived process have beyond functional continuity identifiers and provenance?

### Non-goals
Do not claim reconstruction of destroyed hidden inference state or import Mentaury identity semantics automatically.

### Exit criteria
Only a later evidence-backed process-identity requirement may create a bounded architecture question.

---

## IDPS-FW-011 — Ownership / protected-transition authority

**State:** `NEEDS_ARCHITECTURE_DECISION / DEFERRED`  
**Priority:** P1  
**Suggested audit sequence:** 11  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** potentially high, therefore deferred  
**Revalidation trigger:** mandatory Architecture Reassessment or earlier experiment-specific governance need.

### Question
Who owns durable process state, protected transitions, continuation rights and authorization?

### Current evidence
Only research/governance boundaries exist. Production authority architecture is intentionally not frozen.

### Non-goals
Do not freeze capability/authority architecture before Experiment 0 simply because it is plausible.

### Exit criteria
Explicit post-evidence architecture decision with owner/scope/non-goals.

---

## IDPS-FW-012 — Model independence / portability

**State:** `RESEARCH_HYPOTHESIS / DEFERRED`  
**Priority:** P2  
**Suggested audit sequence:** 12  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Revalidation trigger:** a separately designed portability comparison.

### Question
How portable is an externally represented process state across different model families/capability levels?

### Why it matters
Inference is intended to be replaceable, but absolute model independence is not yet proven and should not be manufactured as a requirement.

### Required experiment
Empirical cross-model comparison with fixed state/reference/task and explicit capability confounds.

### Non-goals
No claim that all models are interchangeable.

### Exit criteria
Empirical portability envelope or explicitly bounded limitation.

---

## IDPS-FW-013 — Mandatory Architecture Reassessment

**State:** `REQUIRED_GATE / NOT_REACHED`  
**Priority:** P0 architecture gate  
**Suggested audit sequence:** 13  
**Implementation authorized:** NO before gate  
**Runtime capability change:** NO  
**Authority impact:** future architecture selection only  
**Evidence anchor:** canonical research program  
**Revalidation trigger:** completed E0-C + Capture analysis + E0-T + Transfer analysis.

### Required sequence

```text
E0-C evidence
→ Capture analysis
→ E0-T evidence
→ Transfer analysis
→ ARCHITECTURE REASSESSMENT
```

### Question
Given the evidence, what is the minimum justified durable substrate and which previously plausible mechanisms are unnecessary?

### Required audit
Compare evidence against the primary null and candidate representations. Explicitly consider `state.json only`, event log, reconstructive manifest, workflow substrate, database/other mechanisms without preselecting a winner.

### Non-goals
No production architecture, runtime or ecosystem integration before this gate.

### Exit criteria
An explicit evidence-backed architecture decision or `MORE_RESEARCH`; only afterward may a production architecture milestone be considered under separate authorization.

---

# 3. Suggested future audit order — not implementation order

```text
1  Human attestation gate (#9)
2  Pilot — NOT EVIDENCE
3  Pilot corrections / Evidence Lock
4  separate GO for E0-C
5  E0-C evidence
6  Capture analysis
7  separate GO for E0-T
8  E0-T evidence
9  Transfer analysis
10 mandatory Architecture Reassessment
11 only then evaluate production architecture/runtime needs
```

This list is a dependency/audit map. It grants **zero automatic authorization**.

---

# 4. Safe continuation protocol

A future AI must preserve:

- `process != inference instance != context window != transcript`;
- capture failure and transfer failure remain isolated;
- ambiguity remains ambiguity;
- contested claims remain contested until adjudicated by an owner;
- `Observed != Inferred`, `Confidence != Evidence`;
- `UNKNOWN` external-operation state is not silently converted into `FAILED`;
- human reference approval cannot be self-issued by the evaluated AI;
- Pilot != Evidence;
- Evidence Lock != Evidence authorization;
- Experiment 0 != production-runtime authorization;
- cross-project similarity != authority inheritance.

For suspected defects:

```text
suspicion
→ reproduction
→ violated invariant
→ causal boundary
→ bounded owner
→ only then repair under separate authorization
```

No ledger entry authorizes E0-C/E0-T evidence, production architecture, runtime, event sourcing, model integration, or ecosystem integration.
