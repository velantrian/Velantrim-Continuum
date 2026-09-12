# CONT-E0T Blind Redteam Review

**BASELINE SHA:** `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`  
**Repo:** `velantrian/Velantrim-Continuum`  
**Branch:** `research/cont-e0t-redteam`  
**Reviewer role:** CONT-REDTEAM (blind independent attacker)  
**Protocol under attack:** CONT-E0T as currently framed (owner decision + program route + frozen Continuum baseline)  
**Author candidate:** not read  
**Experiment execution:** none  
**Architecture promotion:** none  

This review answers one question only:

> Can CONT-E0T as currently framed distinguish **CONT-T1 sufficient-for-bounded-resume** from **CONT-T2 independent history value**?

It does **not** design a preferred architecture, rewrite historical E0-T, or author a successor protocol.

---

## 0. Blindness, sources, and authority

### 0.1 Blindness

This review was written without opening:

- the Author worktree, branch, artifact, chat, or reasoning;
- `CONT_E0T_PREREGISTRATION_CANDIDATE.md` if it exists anywhere;
- sibling role outputs.

HEAD at start of this review: `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5` (exact owner-frozen baseline).

### 0.2 Sources used

**Frozen Continuum at the baseline SHA (read-only):**

- `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md`
- `STATUS.md`, `docs/ai/CURRENT_STATE.md`, `docs/ai/README.md`, `docs/research/README.md`
- `RESEARCH_OVERVIEW.md`, `README.md`, `AGENTS.md`, `project-state.json`
- historical E0-T construction needed to attack the named failure mode (final-state SET events): `scripts/e0/prepare_transfer.py`, `experiments/e0/oracle/approved/transfer-oracle.v0.1.json`, `experiments/e0/fixtures/transfer/scenarios.json`

**Program framing (not Continuum main, not Author):**

- owner decision delivered to this role (CONT-E0T is a **new** successor protocol; do not rewrite historical E0-T; use `CONT-T1` / `CONT-T2`; Graphiti_fractal_lab is pointer-only);
- `velantrian/Graphiti_fractal_lab` `docs/research/CROSS_PROJECT_RESEARCH_RESUME_2026-09-12.md` Program Route v0.1, CONT-E0T section and the listed 10 preregistration fields.

### 0.3 Authority conflict (recorded, not resolved here)

| Surface | What it currently says |
|---|---|
| Continuum baseline SHA | Canonical protocol is historical Experiment 0 (`E0-C` then `E0-T` T0–T4). `T1` = canonical current state. `T2` = event log → deterministic projection of the **same** Oracle State. |
| Owner decision | CONT-E0T is a **new** Continuum successor protocol. Historical `IDPS_EXPERIMENT_0_PREREGISTRATION.md` is read-only. Arms are `CONT-T1` / `CONT-T2`, not bare `T1`/`T2`. |
| Graphiti program route | Defines CONT-E0T question and the 10-field freeze list, but still writes bare `T1`/`T2`. Declared pointer-only. |

This is **SOURCE-CONFLICT**. Continuum SHA `78a73ed` does not contain a CONT-E0T protocol. The 10 fields live on a pointer surface that the owner said is not canonical. Historical E0-T identifiers collide with CONT-E0T arms unless the CONT- prefix is enforced in every freeze field.

---

## 1. Verdict

**NO. Not as currently framed.**

CONT-E0T *points at* the right contrast (competent current state vs genuine accepted trajectory). It does **not** yet operationally isolate:

1. `CONT-T1` sufficient for bounded resume, versus
2. `CONT-T2` independent **history** value, versus
3. representation / token / rationale / presentation advantage, versus
4. historical-query skill (THEN / supersession / “what changed”).

Until the blocking findings below are closed in a freeze — not by architecture invention — a CONT-T2 win, a CONT-T1 win, or a tie would all remain scientifically ambiguous.

**Severity of the overall identifiability failure: BLOCKING | INFERENCE** built on SOURCE-SUPPORTED arm definitions and the historical E0-T construction.

---

## 2. Finding index

| ID | Finding | Severity | Source class |
|---|---|---|---|
| F1 | Identifiability collapse: under competent, final-state-equivalent CONT-T1, no frozen probe class can credit CONT-T2 for *resume* without impoverishing CONT-T1, scoring a historical query, or smuggling rationale | BLOCKING | INFERENCE |
| F2 | Namespace collision: Continuum `T1`/`T2` ≠ CONT-E0T `CONT-T1`/`CONT-T2`; program route still uses bare `T1`/`T2` | MAJOR | SOURCE-CONFLICT |
| F3 | Impoverished CONT-T1 is named as forbidden, not operationally excluded | BLOCKING | SOURCE-SUPPORTED |
| F4 | Disguised-T2 CONT-T1 (trajectory smuggled into “state”) is named as forbidden, not operationally excluded | BLOCKING | SOURCE-SUPPORTED |
| F5 | Final-state information equivalence is a slogan; no check, schema, or fail-closed procedure | BLOCKING | SOURCE-SUPPORTED |
| F6 | Synthetic / fake trajectory: historical E0-T `T2` is SET-events from the final Oracle; CONT-T2 “genuine accepted trajectory” is not specified | BLOCKING | SOURCE-SUPPORTED |
| F7 | Historical-query leakage into the primary outcome (THEN / WHY / supersession scored as resume) | BLOCKING | SOURCE-SUPPORTED |
| F8 | History-value vs continuity-value vs representation-value lacks a frozen classifier | MAJOR | SOURCE-SUPPORTED |
| F9 | Rationale / provenance / presentation / token confounds (including ORNT-E1-PILOT open threats) | MAJOR | SOURCE-SUPPORTED |
| F10 | CONT-T2 can smuggle E0-T `T3` reconstructive-manifest value | MAJOR | SOURCE-SUPPORTED |
| F11 | Ledger envelope missing → CONT-T2 can win by bytes/tokens | BLOCKING | SOURCE-SUPPORTED |
| F12 | Model freeze missing → any result is model-dependent | MAJOR | SOURCE-SUPPORTED |
| F13 | Reviewer procedure missing → unblinded qualitative scoring can prefer richer-looking CONT-T2 | MAJOR | INFERENCE |
| F14 | Absolute adequacy missing: `CONT-T1 ≈ CONT-T2` ≠ CONT-T1 sufficient for bounded resume | BLOCKING | SOURCE-SUPPORTED |
| F15 | Fixture construction bias: no CONT-E0T fixtures; reusing E0-T or ORNT fixtures would predetermine the answer | MAJOR | SOURCE-SUPPORTED |
| F16 | Protocol / evidence-lock / deviation rules not instantiated for CONT-E0T | MINOR | SOURCE-SUPPORTED |
| F17 | Token-overlap proxy from ORNT-E1-PILOT must not become CONT-E0T primary | MINOR | SOURCE-SUPPORTED |
| F18 | Oracle-authored accepted transitions ≠ captured transitions (CAP-E1 is HOLD) | NON-BLOCKING | SOURCE-SUPPORTED |
| F19 | Continuum still sequences E0-T as the next transfer experiment | NON-BLOCKING | SOURCE-CONFLICT |
| F20 | Split canonical store (Continuum vs Graphiti pointer) for the 10 fields | MAJOR | SOURCE-CONFLICT |

---

## 3. Findings

### F1 — Identifiability collapse (BLOCKING | INFERENCE)

**Target claims**

- **CONT-T1-sufficient-for-bounded-resume:** a competent current-state package is enough for the preregistered resume probes.
- **CONT-T2-independent-history-value:** genuine accepted transition trajectory adds *resume* value that is not reducible to that current-state package.

**Framing constraints (SOURCE-SUPPORTED)**

Program route requires CONT-T2 to carry the **same final-state information as CONT-T1 plus** genuine accepted history, and forbids building T2 by serializing the final snapshot into fake SET events. Historical E0-T already stores, inside the *current* Oracle, the dimensions a successor needs for ordinary continuation: goal, task position, constraint, accepted decision, rejected alternative, unresolved question, contested claim, rationale, committed/UNKNOWN operations, artifact reference, mid-task revision (`IDPS_EXPERIMENT_0_PREREGISTRATION.md` §15; approved `transfer-oracle.v0.1.json`).

**Attack**

If CONT-T1 is actually competent *and* final-state-equivalent, then any probe whose correct answer is determined by *currently holding* facts is solvable from CONT-T1. A CONT-T2 win on that probe is then one of:

1. CONT-T1 omitted a current field (impoverished CONT-T1, F3);
2. the probe asked about the past (historical-query leakage, F7);
3. CONT-T2 carried extra rationale/narrative/tokens/format (F9, F10, F11);
4. CONT-T2 was not genuine trajectory (F6).

There is **no frozen probe class** in the current framing that is simultaneously:

- a bounded **resume** task (next allowed action, constraint application, valid resume point, honest UNKNOWN);
- not recoverable from a competent current-state package;
- not a THEN / “what changed” / supersession quiz;
- not a rationale-manifest task (historical E0-T `T3`).

Without that class, CONT-E0T cannot distinguish “CONT-T1 sufficient” from “CONT-T2 has independent history value.” Case C in the program route (“T2 helps only history”) is conceptually correct and currently unenforceable, because the primary surface is not frozen (Field 1 PARTIAL).

This is not an argument that trajectory never matters. It is an argument that **the framed experiment cannot tell**. Durability, crash recovery, audit, concurrency, and freshness are explicitly later / out-of-scope in historical E0 (`§28`, RA-8). Importing them into CONT-E0T “resume” would change the question.

**What would close it (protocol, not architecture):** a preregistered, fail-closed map `{probe_id → {PRIMARY_RESUME | SECONDARY_HISTORY | DIAGNOSTIC}}` plus an explicit statement that no PRIMARY_RESUME probe is allowed to require a fact that a competent CONT-T1 is forbidden to hold.

---

### F2 — Namespace collision (MAJOR | SOURCE-CONFLICT)

Frozen Continuum reserves `T0`–`T4` exclusively for E0-T transfer arms (`§4.1`). Historical meanings:

| ID | Historical E0-T |
|---|---|
| T1 | Canonical current state (`state.json`) |
| T2 | Event log → deterministic **projection of the same Oracle** |
| T3 | Projection + reconstructive manifest |

CONT-E0T (owner + program) uses:

| ID | CONT-E0T framing |
|---|---|
| CONT-T1 | Versioned maintained current state; **no** full accepted trajectory |
| CONT-T2 | Same final-state information **plus** genuine accepted transition history |

The program route still labels arms `T1`/`T2`. Any implementer reading Continuum first will rebuild historical `event_projection()` SET-logs and will **not** test independent history value. Owner already required the CONT- prefix; the pointer document was not updated. Bare `T1`/`T2` in a CONT-E0T freeze is a protocol defect.

---

### F3 — Impoverished CONT-T1 (BLOCKING | SOURCE-SUPPORTED)

Historical E0-T: T1 “is the primary boring baseline and must be implemented competently”; T0 “must not be deliberately weakened into a strawman” (`§16`). Program route lists CONT-T1 contents (goals, constraints, blockers, accepted decisions, open questions, provenance refs, process position) but does **not** freeze:

- a minimum field set / schema;
- a competence bar against the E0 Oracle dimensions;
- a check that every currently-true probe-relevant fact in the fixture gold is present on CONT-T1.

If CONT-T1 drops rejected alternatives, UNKNOWN operations, contested claims, or provenance that remain currently relevant, CONT-T2 will “win” by carrying current-state inside events. That is not history value. It is a strawman baseline.

**Minimum exclusion:** CONT-T1 may omit *only* fields that are preregistered as trajectory-only (ordering of superseded states, from_state snapshots that are not currently true, acceptance metadata of past transitions). It may not omit currently-true process facts.

---

### F4 — Disguised-T2 CONT-T1 (BLOCKING | SOURCE-SUPPORTED)

Program: CONT-T1 has “No full accepted transition trajectory.” Not operational.

A `state.json` that contains an ordered `accepted_transitions[]` with `from_state`, `to_state`, supersession, timestamps, and acceptance is CONT-T2 under a current-state filename. So is a current-state object that embeds enough event IDs / hashes / “how we got here” narrative to reconstruct the path.

**Minimum exclusion (examples, not an ontology):** CONT-T1 may hold *current* accepted decision D and *current* rejected alternative R. It may not hold the ordered path `S0→S1→S2` that produced D, nor superseded state snapshots, unless those snapshots are still currently true (in which case they belong in current state, not history).

Without a field-level allow/deny list, Author and later implementers can move the entire contrast into naming.

---

### F5 — Final-state non-equivalence (BLOCKING | SOURCE-SUPPORTED)

Program: CONT-T2 = same final-state information as CONT-T1 plus history. Historical E0-T already had a *projection fidelity* check, but it checked that T2’s projection **equals the Oracle**, and then **delivered that projection to the successor** (`prepare_transfer.py` `event_projection`; `§16` “The successor receives a current projection representing the same Oracle State as T1”). That design *removes* independent trajectory from the successor channel.

CONT-E0T must invert the historical mistake:

1. project CONT-T2’s genuine trajectory to a current-state object;
2. require that projection to match CONT-T1 under a frozen equality (canonical JSON / field map);
3. **fail closed** on mismatch (do not interpret successor results);
4. still **deliver the trajectory (plus CONT-T1-equivalent current state)** to the CONT-T2 successor, not the projection alone.

None of (1)–(4) is frozen. Without them, a CONT-T2 win is unidentified extra current-state content.

---

### F6 — Synthetic / fake trajectory (BLOCKING | SOURCE-SUPPORTED)

Historical construction, baseline SHA, `scripts/e0/prepare_transfer.py`:

```text
events = [{seq, op: "SET", field, value} for field, value in canonical_final_state.items()]
```

That is exactly the construction the program forbids: “do not build T2 by serializing final state into fake SET events.” It is also the only executable transfer-arm builder in Continuum. CONT-T2 “genuine accepted trajectory” (`from_state`, `to_state`, type, owner/authority, provenance, acceptance, supersession, ordering, timestamp) has **no** fixture, schema, or authenticity predicate.

**Minimum authenticity predicate:**

- at least one intermediate `from_state` that is **not** equal to final state;
- at least one genuine supersession (a previously accepted item is no longer current);
- at least one accepted transition whose `from_state` cannot be reconstructed from the final snapshot alone by field-wise SET;
- experimenter-authored accepted transitions, frozen before evidence, not model-emitted (CAP-E1 is HOLD).

If this predicate is absent, CONT-T2 cannot in principle carry independent history value.

---

### F7 — Historical-query leakage into primary outcome (BLOCKING | SOURCE-SUPPORTED)

Program primary continuity surface: “correct current state, constraint preservation, blocker preservation, valid resume point, honest UNKNOWN.” Historical queries must be separate. Case C: if T2 is better only at “what was true before / what changed / what did we supersede?” that is HISTORY VALUE, not continuity value.

Query roles on the same program surface include NOW, THEN, WHY, REOPEN, UNKNOWN, NEXT. ORNT-E1-PILOT measured a large THEN packet delta (≈0.381 → ≈0.745) on a token-overlap proxy. If CONT-E0T primary scoring includes THEN/WHY/REOPEN, CONT-T2 wins by construction.

No frozen split `{query_id → CURRENT_RESUME vs HISTORICAL}` exists. Field 1 and Field 3 are therefore not executable.

**Fail-closed rule required:** a query whose gold answer is a superseded state, a from_state, or a change-set cannot contribute to the primary ResumeAdequacy statistic.

---

### F8 — History-value vs continuity-value (MAJOR | SOURCE-SUPPORTED)

The invariants are named:

```text
REPRESENTATION ADVANTAGE ≠ HISTORY ADVANTAGE ≠ CONTINUITY ADVANTAGE
EQUIVALENCE ≠ ADEQUACY
CURRENT STATE ≠ STATE TRAJECTORY
```

There is no frozen classifier from probe → advantage type, and no separate reporting tables. Outcome rows A–D exist as prose. A single composite “T2 better” claim would be an illicit collapse, which historical E0 already forbids (no weighted continuity score, `§19`–`§20`).

---

### F9 — Rationale / provenance / presentation / token confounds (MAJOR | SOURCE-SUPPORTED)

ORNT-E1-PILOT recorded OPEN threats: content advantage; selection/presentation advantage; token-overlap proxy bias; prompt asymmetry. Program route says not to tell a baseline “you do not receive X.”

CONT-E0T does not freeze:

- prompt symmetry (CONT-T1 must not be instructed that it “lacks history”);
- matched serialization (both arms structured, same key naming for shared current-state fields);
- provenance verbosity caps;
- tokenizer/byte accounting per arm.

A narrative ledger will beat a compact `state.json` on many models for reasons that are not trajectory-value. That confound is already enough to make a CONT-T2 win uninterpretable.

---

### F10 — Reconstructive-manifest / T3 smuggling (MAJOR | SOURCE-SUPPORTED)

Historical E0-T split T2 (events→projection) from T3 (projection + reconstructive manifest of rationale / unresolved / rejected / artifact). CONT-T2 as listed includes provenance and the program’s WHY = “transition/decision rationale.” If CONT-T2 packages rationale text that CONT-T1 also holds (Oracle `rationale` is a current-state field) *and* extra narrative, the contrast is T3-like reconstructive value, not independent history value.

**Required split:** current rationale that still governs the process belongs on CONT-T1. Transition-justification that is *only* about a past change belongs on secondary WHY/history metrics, not primary resume.

---

### F11 — Ledger-envelope advantage (BLOCKING | SOURCE-SUPPORTED)

Program Field 9 is explicitly missing: max transitions and/or max T2 token/byte budget. Historical E0-T §21 already requires separate injection/storage/generation/projection/verification/runtime accounting and forbids inventing missing telemetry.

Without an envelope, CONT-T2 can be arbitrarily larger. Token/context advantage is representation advantage, not history advantage. This alone blocks causal attribution of a CONT-T2 win.

---

### F12 — Model dependence (MAJOR | SOURCE-SUPPORTED)

Field 5 is missing. Continuum Pilot runtime values remain `UNRESOLVED`. Historical E0 lists model-family swap as **future**, not E0 (`§28`). ORNT-E1-PILOT used `gpt-5-mini` only. A single-model CONT-E0T result cannot support “history has independent resume value” versus “this model uses narrative / extra tokens better.”

Not blocking for a *pre-execution freeze* if the freeze names one model family and pre-declares non-generalization. Blocking for any architecture-level reading. This review treats architecture promotion as already forbidden, so severity is MAJOR for the scientific claim, not an invitation to run more models.

---

### F13 — Reviewer bias (MAJOR | INFERENCE)

Field 7 is missing. Historical E0: LLM judges must not be primary truth for deterministic fields (`§10`); HARD FAIL must be pre-bound (`§12`). If humans score successor resume quality while seeing which arm produced the package, richer CONT-T2 will be favored. Arm-blind scoring of successor **outputs** (not of packages) is not specified.

---

### F14 — Inadequate absolute adequacy (BLOCKING | SOURCE-SUPPORTED)

Program: `T1 ≈ T2 ≠ T1 is good enough in absolute terms`. Case A still defines sufficiency as non-inferiority **and** cheaper/simpler than CONT-T2. That is a relative rule. Both arms can fail constraint preservation, fabricate authorization, or lose UNKNOWN, and Case A could still fire if CONT-T1 fails equally and is cheaper.

Historical E0 §20 `MATERIAL_GAIN` is also relative, but HARD FAIL is a separate non-averaged channel. CONT-E0T names “unacceptable safety regression” in Case B and does not freeze HARD FAIL classes, predicates, or an absolute ResumeAdequacy bar independent of the other arm.

**Without an absolute bar, “CONT-T1 sufficient-for-bounded-resume” is not a possible experimental conclusion.** Only “not worse than CONT-T2 on this fixture set” is.

---

### F15 — Fixture construction bias (MAJOR | SOURCE-SUPPORTED)

No CONT-E0T fixture IDs, count, hashes, or content exist at the Continuum baseline. Historical transfer fixtures are **final Oracle snapshots plus a prose source_context**, not genuine trajectories. ORNT-E1-PILOT’s 8 fixtures are a different question; artifacts are not even in the lab repo as of the resume.

Two opposite biases are both available:

- write fixtures whose “resume” gold requires a superseded fact → CONT-T2 wins by construction;
- write fixtures with no trajectory-only information → CONT-T2 cannot show continuity value, only optional history value.

Either bias can be introduced after seeing model behavior unless fixtures are hashed before evidence (historical E0 §23–§25). Reusing E0-T scenarios would import the SET-event T2 failure into CONT-E0T.

---

### F16 — Protocol deviations / lock (MINOR | SOURCE-SUPPORTED)

Historical E0 has evidence lock, fail-closed execution, PILOT ≠ EVIDENCE, supersession, and invalidation-on-change (`§22`–`§24`). CONT-E0T has `executed: false`, `authorized: false`, and no protocol version, schema hashes, or deviation table. Not blocking for this docs-only review; blocking before any later GO.

---

### F17 — Token-overlap proxy (MINOR | SOURCE-SUPPORTED)

ORNT-E1-PILOT primary-ish diagnostic was token-overlap; proxy-bias is an OPEN THREAT. It must not be imported as CONT-E0T ResumeAdequacy. Semantic rubric Field 6 is the replacement and is not frozen.

---

### F18 — Oracle trajectory ≠ captured trajectory (NON-BLOCKING | SOURCE-SUPPORTED)

CAP-E1 is HOLD and must not be smuggled into CONT-E0T. Using experimenter-authored accepted transitions is legitimate transfer isolation (same logic as E0-T Oracle State). A later positive CONT-T2 result would not prove capture. The framing already implies this; it only needs an explicit non-claim in the freeze.

---

### F19 — Continuum still sequences historical E0-T next (NON-BLOCKING | SOURCE-CONFLICT)

`project-state.json` `research_sequence` remains `E0-C → E0-T → Architecture Reassessment`. Owner forbids rewriting that historical protocol and places CONT-E0T as a **new** successor document. This review does not update state surfaces. Future STATE_CHANGE is owner work. Contamination risk for agents who read Continuum first: they will implement E0-T T0–T4 instead of CONT-E0T.

---

### F20 — Split freeze store (MAJOR | SOURCE-CONFLICT)

Owner: canonical repo is Continuum; Graphiti_fractal_lab is pointer-only. The only currently written 10-field list lives in the pointer repo. Continuum SHA `78a73ed` has zero CONT-E0T freeze fields. Until the freeze lives on Continuum, “CONT-E0T as framed” has two owners. This review therefore classifies Continuum-side fields as MISSING even where Graphiti prose is PARTIAL.

---

## 4. Independent minimum 10-field freeze

Same 10 fields as Program Route v0.1 (`CROSS_PROJECT_RESEARCH_RESUME_2026-09-12.md` “Still missing before CONT-E0T execution”). This is **redteam’s required freeze for identifiability**, written without seeing any Author candidate. It is not an architecture.

Status column = how frozen **the current framing** is (owner + program route + Continuum baseline SHA). Not a grade of an unseen Author file.

| # | Field | Redteam minimum freeze (identifiability) | Status |
|---|---|---|---|
| 1 | Primary confirmatory surface | Primary statistic = bounded **final-state resume** only: constraint preservation, blocker preservation, valid resume point, honest UNKNOWN, no fabricated authorization. Historical queries (THEN, superseded, change-set, as_of) are a **separate** table and cannot enter the primary statistic. ResumeAdequacy must be a named, deterministic-or-prebound procedure, not token-overlap. | **PARTIAL** |
| 2 | Fixture set | Count, IDs, partition (PILOT vs EVIDENCE), content, schema, hash/version frozen before evidence. No post-hoc edits. Must not reuse historical E0-T transfer scenarios as-is (they have no genuine trajectory). Each fixture must declare whether primary resume is solvable from competent current state. | **MISSING** |
| 3 | Queries per fixture | Number, role, exact wording, gold, and `{CURRENT_RESUME \| HISTORICAL \| DIAGNOSTIC}` tag per query. Fail closed if a HISTORICAL query is later moved into primary. WHY, if used, stays “transition/decision rationale” and is **not** primary unless preregistered as resume-necessary *and* still currently true (then it belongs on CONT-T1). | **PARTIAL** |
| 4 | Operational CONT-T1 / CONT-T2 final-state equivalence check | Canonical projection of CONT-T2 trajectory → current-state object; frozen field map; byte/canonical-JSON equality to CONT-T1; fail closed on mismatch; successor still receives trajectory on CONT-T2. Bare `T1`/`T2` identifiers forbidden in this field. | **PARTIAL** + **SOURCE CONFLICT** |
| 5 | Reader / model freeze | Provider, exact model identifier, temperature, seed, context limit, reserved tokens, prompt/template hashes, tokenizer. Prompt symmetry required. Single-model results pre-declared as non-generalizing. | **MISSING** |
| 6 | Semantic rubric frozen before outputs | Separate rubrics: ResumeAdequacy (primary) vs historical metrics (secondary) vs complexity (accounting). No post-output invention. No weighted NetValue unless weights are themselves preregistered (program default: do not invent one). Map to outcomes A/B/C/D with HARD FAIL as a separate channel. | **PARTIAL** |
| 7 | Reviewer procedure | Roles, arm-blind scoring of successor outputs, adjudication, IAA if human, LLM-judge not primary for deterministic/safety fields. | **MISSING** |
| 8 | Complexity accounting (separate) | Storage bytes, annotation cost, replay/projection cost, injected tokens/bytes, latency. Provenance `MEASURED \| ESTIMATED \| UNAVAILABLE`. No fake NetValue scalar. | **PARTIAL** |
| 9 | Ledger envelope | Max accepted transitions **and** max CONT-T2 injection tokens/bytes relative to CONT-T1 (or an explicit matched-budget rule). Overflow → `ENVELOPE_EXCEEDED`, not silent extra context. | **MISSING** |
| 10 | Equivalence ≠ adequacy | Absolute ResumeAdequacy / HARD FAIL bar that does **not** depend on the other arm. `CONT-T1 ≈ CONT-T2` cannot by itself justify “CONT-T1 sufficient-for-bounded-resume.” Pre-bind HARD FAIL classes (at least fabricated authorization, lost critical restriction, unsafe epistemic promotion). | **PARTIAL** |

### 4.1 Status counts (current framing)

| Status | Fields |
|---|---|
| FROZEN | none |
| PARTIAL | 1, 3, 6, 8, 10 |
| PARTIAL + SOURCE CONFLICT | 4 |
| MISSING | 2, 5, 7, 9 |
| SOURCE CONFLICT (also F2/F19/F20) | namespace + canonical store |

**Zero of ten fields are FROZEN.** That is sufficient to refuse execution. It is also sufficient to refuse the claim that the framed protocol can already distinguish the two scientific hypotheses.

---

## 5. Attack coverage checklist (Labs-requested vectors)

| Requested attack | Covered by |
|---|---|
| Impoverished CONT-T1 | F3 |
| Disguised-T2 CONT-T1 | F4 |
| Final-state non-equivalence | F5 |
| Rationale / provenance / presentation / token confounds | F9, F10, F11, F17 |
| History-value vs continuity-value | F1, F7, F8 |
| Historical-query leakage into primary outcome | F7 |
| Model dependence | F12 |
| Reviewer bias | F13 |
| Inadequate absolute adequacy | F14 |
| Synthetic / fake trajectory | F6 |
| Ledger-envelope advantage | F11 |
| Protocol deviations | F16 |
| Fixture construction bias | F15 |

---

## 6. Non-claims

This review does **not** claim:

- that event sourcing is required or forbidden;
- that CONT-T1 will win or CONT-T2 will win;
- that historical E0-T evidence exists (it does not; Pilot and E0-T evidence are not authorized);
- that ORNT-E1-PILOT proved or disproved history value;
- that Author’s unseen candidate is adequate or inadequate;
- any architecture, organ, storage backend, or runtime.

Negative later evidence would not prove history universally unnecessary. Positive later evidence would not prove event sourcing necessary. Those non-claims are already in the owner/program framing and remain in force.

---

## 7. Answer, restated

**Can CONT-E0T as currently framed distinguish CONT-T1 sufficient-for-bounded-resume from CONT-T2 independent history value?**

**No.** The question is well-aimed. The freeze is not. Under the framing’s own constraints (competent CONT-T1, final-state equivalence, no fake SET trajectory), a CONT-T2 primary-resume win is unidentified, and a CONT-T1 “sufficiency” win has no absolute bar. Historical E0-T’s executable `T2` is the exact non-isolating construction CONT-E0T must not repeat.

**STOP.** Docs-only. No experiment. No merge. No architecture promotion.
