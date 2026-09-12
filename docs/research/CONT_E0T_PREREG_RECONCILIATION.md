# CONT-E0T Preregistration Reconciliation

**Labs coordinator artifact.** Not a vote. Not experiment authorization.  
**BASELINE SHA:** `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`  
**Repository:** `velantrian/Velantrim-Continuum`  
**This branch:** `research/cont-e0t-prereg-reconciliation`

Sealed inputs (do not rewrite):

| Role | Artifact | Commit |
|------|----------|--------|
| CONT-AUTHOR | `docs/research/CONT_E0T_PREREGISTRATION_CANDIDATE.md` | `4a026c1ef7844cc95873d6155b311c2853346fe8` |
| CONT-REDTEAM | `docs/research/CONT_E0T_BLIND_REDTEAM_REVIEW.md` | `1069ee39c8ad53251964ebd00c6ee3dfbdf21bac` |
| CONT-INTEGRITY | `docs/research/CONT_E0T_INTEGRITY_REPORT.md` | `35d935e78fd87a584a73fd520d09f9b2465d8ad0` |

```text
MODEL OUTPUT ≠ STATE AUTHORITY
TWO MODELS AGREEING ≠ TRUTH
REVIEWER VERDICT ≠ OWNER AUTHORIZATION
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
```

Historical `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` was not modified on either sealed branch (same blob as baseline).

---

## 1. Unblind condition

Both sealed commits exist and are parented on the exact baseline. Cross-file contamination check:

- RedTeam tree does **not** contain the Author candidate file.
- Author tree does **not** contain the RedTeam review file.
- Historical E0-T prereg SHA-256 identical on baseline, Author HEAD, and RedTeam HEAD.

Labs did **not** send Author text to RedTeam before RedTeam commit.

---

## 2. Shared agreements (AGREE)

These are **not** a freeze. They are shared directions.

| Item | Author | RedTeam | Labs |
|------|--------|---------|------|
| CONT-E0T ≠ historical E0-T | yes | yes | AGREE |
| Do not rewrite E0-T T0–T4 | yes | yes | AGREE |
| Use CONT-T1 / CONT-T2, not bare T1/T2 | yes | yes (F2) | AGREE |
| CONT-T1 must be competent, not impoverished | direction | F3 BLOCKING until operational | AGREE on direction; **not operational** |
| CONT-T1 must not be disguised CONT-T2 | direction | F4 BLOCKING until operational | AGREE on direction; **not operational** |
| CONT-T2 must not be SET-from-final-state | direction | F6 BLOCKING; only executable historical builder is that construction | AGREE on direction; **not operational** |
| Historical/THEN queries off PRIMARY | direction | F7 BLOCKING until tagged | AGREE on direction; **not operational** |
| Equivalence ≠ adequacy | direction | F14 BLOCKING until absolute bar | AGREE on direction; **not operational** |
| No NetValue collapse | yes | yes | AGREE |
| No invented 100%/0%/0% gates | yes | implied | AGREE |
| Structured comparison + blind semantic equivalence | **PROPOSED, not selected** | not selected as law | AGREE: remains PROPOSED |
| Fixtures / exact queries / model IDs / envelope schema | MISSING or unbound | MISSING | AGREE: unbound |
| Execution / architecture | none | none | AGREE: not authorized |

---

## 3. Reconciliation matrix (10 fields)

Allowed field statuses for the **current combined state** (not “basically done”):

`FROZEN` | `PARTIAL` | `MISSING` | `SOURCE_CONFLICT`

| # | Field | Author | RedTeam | Class | Labs synthesis | Resolution type |
|---|-------|--------|---------|-------|----------------|-----------------|
| 1 | Primary confirmatory surface | PARTIAL (resume-now; exact probes missing) | PARTIAL; F1 identifiability collapse BLOCKING | **CONFLICT** on *whether the framed primary can isolate history-value at all* | Direction (resume-now only) is shared. RedTeam F1 is the scientific blocker: if CONT-T1 is competent and equivalent, a PRIMARY resume win for CONT-T2 is unidentified (impoverished T1 / historical query / extra rationale-tokens / fake trajectory). Author did not freeze a probe class that escapes that collapse. | methodological + owner-policy: must define fail-closed `{probe → PRIMARY_RESUME \| SECONDARY_HISTORY \| DIAGNOSTIC}` and forbid PRIMARY probes that require facts CONT-T1 may not hold |
| 2 | Frozen fixture set | MISSING | MISSING (F15 MAJOR) | **AGREE** | No IDs, hashes, or content. Must not reuse E0-T transfer scenarios as-is. | empirical construction (later); **owner** must authorize a fixture campaign |
| 3 | Frozen queries per fixture | MISSING (dual-class rule PARTIAL) | PARTIAL (need per-query tags) | **AGREE** | Dual-class rule is prose only. No wording/gold. | empirical + methodological |
| 4 | Operational equivalence check | PARTIAL; executable evaluator MISSING | PARTIAL + SOURCE CONFLICT; F5 BLOCKING | **CONFLICT** (severity, plus RedTeam SOURCE CONFLICT on namespace/store) | Shared invert-the-old-T2 idea: project CONT-T2 → current object; match CONT-T1; fail closed; still *deliver* trajectory on CONT-T2. Not executable. RedTeam SOURCE CONFLICT is about Continuum vs pointer store / bare T1T2 — owner already chose Continuum + CONT- prefix; remaining conflict is “no Continuum freeze fields yet,” which this candidate begins to close as *candidate*, not freeze. | methodological |
| 5 | Reader/model freeze | PARTIAL (discipline only) | MISSING | **AUTHOR_ONLY** vs **REDTEAM_ONLY** label difference | Same substance: no model/prompt hashes. Author calls it PARTIAL (inherited E0 discipline). RedTeam calls MISSING (nothing CONT-pinned). Combined: **MISSING** for a lock. | owner-policy when/if a later freeze names one non-generalizing reader |
| 6 | Semantic rubric | PARTIAL (E0-like labels; no match spec) | PARTIAL | **AGREE** | Vocabulary sketch ≠ frozen ResumeAdequacy procedure. Token-overlap must not be imported (F17). | methodological |
| 7 | Reviewer procedure | PARTIAL sketch | MISSING | same as #5 | Arm-blind scoring of *outputs* is sketched, not bound. Combined: **MISSING** for lock. | methodological |
| 8 | Complexity/cost accounting | PARTIAL (channels named) | PARTIAL | **AGREE** | Structure reusable; no CONT run-manifest. Do not invent NetValue. | methodological |
| 9 | CONT-T2 ledger envelope | PARTIAL (logical sections; no bounds) | MISSING; F11 BLOCKING | **CONFLICT** on status label | Author named sections; RedTeam requires max transitions **and/or** max injection budget vs CONT-T1, overflow fail-closed. Without a numeric/matched envelope, token confound remains. Combined: **PARTIAL** direction, **MISSING** bound. Labs matrix status: **MISSING**. | methodological |
| 10 | Absolute adequacy boundary | PARTIAL (equivalence ≠ adequacy; no checklist) | PARTIAL; F14 BLOCKING | **AGREE** on diagnosis | Relative non-inferiority cannot conclude “CONT-T1 sufficient.” Need an arm-independent HARD FAIL / ResumeAdequacy bar. Not written as atoms. | owner-policy (how strict) + methodological |

**FROZEN fields: 0 / 10.**

---

## 4. RedTeam findings vs Author (not a vote)

| ID | Severity | vs Author | Class |
|----|----------|-----------|-------|
| F1 identifiability collapse | BLOCKING | Author primary surface is resume-now but does not answer F1 | **REDTEAM_ONLY** as explicit collapse argument; Labs: **UNRESOLVED / BLOCKING** |
| F2 namespace | MAJOR | Author already uses CONT-T1/CONT-T2 | **AGREE** closed in Author candidate; pointer-lab resume still bare T1/T2 (out of this repo) |
| F3 impoverished CONT-T1 | BLOCKING | named, not operational | **AGREE** gap |
| F4 disguised-T2 CONT-T1 | BLOCKING | named, not operational | **AGREE** gap |
| F5 equivalence not operational | BLOCKING | named, not executable | **AGREE** gap |
| F6 fake SET trajectory | BLOCKING | named invalid; no authenticity predicate/schema | **AGREE** gap; RedTeam predicate is **PROPOSAL** |
| F7 historical leakage | BLOCKING | dual-class named; no query tags | **AGREE** gap |
| F8 advantage classifier | MAJOR | qualitative A–D mentioned | **AGREE** gap |
| F9–F11 confounds / envelope | MAJOR/BLOCKING | costs named; envelope unbound | **AGREE** gap |
| F10 T3-smuggling | MAJOR | not explicitly split | **REDTEAM_ONLY** extra; Labs: accept as MAJOR hygiene |
| F12 model | MAJOR | PARTIAL vs MISSING | **AGREE** unbound |
| F13 reviewer | MAJOR | sketch vs MISSING | **AGREE** unbound |
| F14 absolute adequacy | BLOCKING | named, no atoms | **AGREE** gap |
| F15 fixture bias | MAJOR | MISSING | **AGREE** |
| F16 lock/deviations | MINOR | stop rule only | **AGREE** not needed for this docs step |
| F17 token-overlap | MINOR | Author refused invented thresholds | **AGREE** |
| F18 CAP ≠ CONT | NON-BLOCKING | implicit | **AGREE**; explicit non-claim should stay |
| F19 Continuum still sequences E0-T | NON-BLOCKING | owner: new doc, no rewrite | **OWNER_DECISION_REQUIRED** later pointer only |
| F20 split store | MAJOR | Author wrote on Continuum | **mostly closed** by this workflow; lab pointer still exists |

Labs does **not** treat F1 as resolved because Author and RedTeam “both want resume-now.” F1 is exactly that resume-now + competent equivalent CONT-T1 leaves no isolating primary probe.

---

## 5. Special CONT-T1 / CONT-T2 check

| | Question | Established? |
|---|---------|--------------|
| A | Is CONT-T1 competent rather than intentionally impoverished? | **NO** — named, not operational (F3) |
| B | Does CONT-T1 preserve every current resume-relevant semantic consequence the fixture needs? | **NO** — no fixtures, no field list |
| C | Does CONT-T1 avoid embedding the full historical trajectory? | **NO** — no allow/deny list (F4) |
| D | Does CONT-T2 contain a genuine accepted trajectory rather than final-snapshot events? | **NO** — no schema/authenticity predicate (F6) |
| E | Are historical/audit questions separated from PRIMARY practical resume? | **NO** — rule in prose only (F7) |
| F | Can an apparent CONT-T2 gain be explained by more current info, rationale, provenance, tokens, formatting, or reader bias? | **YES, currently** — envelope/model/prompt/reviewer unbound (F9–F13) |

If any of A–E cannot be established: **NOT_READY.**

---

## 6. Labs process integrity

Verified by Labs before this file:

- Baseline `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`
- Author parent = baseline; RedTeam parent = baseline
- Docs-only one-file commits
- No E0-T prereg mutation
- No experiment / paid model run observed in these worktrees
- Procedural blindness: shared computer; no Author file in RedTeam tree

Formal Integrity report sealed after this file’s first commit (`6cfe219d5410e67f17878a60225e421f52f2331a`):

- SHA: `35d935e78fd87a584a73fd520d09f9b2465d8ad0`
- Parent: `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`
- Branch: `research/cont-e0t-integrity`
- Verdict: **INTEGRITY: PASS** (process / state only)
- Names Author `4a026c1ef7844cc95873d6155b311c2853346fe8` and RedTeam `1069ee39c8ad53251964ebd00c6ee3dfbdf21bac`
- Docs-only one-file add; sealed Author/RedTeam not rewritten

Integrity PASS does **not** freeze science fields and does **not** authorize the experiment.

---

## 7. Current 10-field matrix (Labs, this SHA)

| # | Field | Status |
|---|-------|--------|
| 1 | Primary confirmatory surface | **PARTIAL** |
| 2 | Frozen fixture set | **MISSING** |
| 3 | Frozen queries per fixture | **MISSING** |
| 4 | Operational equivalence check | **PARTIAL** |
| 5 | Reader/model freeze | **MISSING** |
| 6 | Semantic rubric | **PARTIAL** |
| 7 | Reviewer procedure | **MISSING** |
| 8 | Complexity/cost accounting | **PARTIAL** |
| 9 | T2 ledger envelope | **MISSING** |
| 10 | Absolute adequacy boundary | **PARTIAL** |

**SOURCE_CONFLICT:** none remaining on *owner repo choice* (Continuum + new protocol). Residual namespace/store notes are hygiene (lab pointer still uses bare T1/T2; Continuum `research_sequence` still lists historical E0-T). Those are **not** field-10 SOURCE_CONFLICT for CONT-E0T semantics.

---

## 8. Decision

Any required field is PARTIAL or MISSING →

```text
FINAL_PREREG_REVIEW = NOT_READY
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
```

This is **not** a claim that CONT-E0T is the wrong question. It is a claim that the freeze cannot yet isolate the contrast.

---

## 9. Owner decisions required (not execution GO)

1. Accept `NOT_READY` and authorize a **v2 preregistration freeze** that operationalizes F1/F3–F7/F11/F14 (probe map, field allow/deny, authenticity predicate, envelope bound, absolute HARD FAIL) — still no experiment.
2. Or stop / defer CONT-E0T.
3. Later, optional **pointer-only** line on historical E0-T index: “CONT-E0T is a follow-up protocol.” No rewrite.
4. Whether F1’s demanded PRIMARY_RESUME class is even constructible without impoverishing CONT-T1 — if owner believes it is not, CONT-E0T may be limited to **history-value** measurement (Case C by design), not continuity-value.

---

## 10. Next single action

**Owner review of this reconciliation.**  
Do **not** execute CONT-E0T.  
Do **not** merge these research branches without explicit Ruslan approval.

If owner wants progress: one v2 freeze document addressing the blocking operational gaps — not a new architecture, not a run.
