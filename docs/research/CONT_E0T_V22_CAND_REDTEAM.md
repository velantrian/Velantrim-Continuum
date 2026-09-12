# CONT-E0T v22 Claim-B candidate RedTeam

**Reviewed commit:** `f3d7fb9038377e5070b9554a8942f5ae43e5a46d`  
**Worktree:** `/workspace/cont-e0t/v22-cand-rt`  
**Branch:** `research/cont-e0t-v22-cand-redteam`  
**Role:** independent RedTeam of Labs-authored discriminator candidates  
**Not:** a new conceptual round; Field-5 model freeze; Evidence; PILOT promotion; candidate-JSON edits; a model run  

Reviewed:

- `docs/research/cont_e0t_v2/candidates/CONT_E0T_FX_B_CAND_03.json`
- `docs/research/cont_e0t_v2/candidates/CONT_E0T_FX_B_CAND_04.json`

CAND-01/02 are SUPERSEDED (README). Used only as contrast. Not re-litigated as live objects.

Thin form on 03/04: `ID_REFS_ONLY` (`op` / `field` / `id`; no `from_state` / `to_state` text).

Owner bars: fail any → **BLOCKING**.

---

## Gate

```text
READY_FOR_FIELD_5 = NOT_READY_FOR_FIELD_5
```

CAND-03 fails bar 5 (list-order) and bar 8 (SECONDARY semantically derivable from T1). CAND-04 clears the eight bars with residuals. The pair is not Field-5-ready. Do not freeze. Do not run a model.

---

## Owner bars

| # | Bar | CAND-03 | CAND-04 |
|---|-----|---------|---------|
| 1 | CONT-T1 fully competent for PRIMARY; not impoverished | PASS | PASS |
| 2 | PRIMARY gold is *not* a verbatim restatement of rationale / process_position / one constraint / one UNKNOWN / one rejected | PASS | PASS |
| 3 | PRIMARY requires composition across multiple currently-true T1 facts | PASS | PASS |
| 4 | PRIMARY still information-sufficient from T1 | PASS | PASS |
| 5 | List order must not make SECONDARY gold solvable from T1 | **BLOCKING** | PASS |
| 6 | thin_trajectory must not re-deliver the final current answer as extra text | PASS | PASS |
| 7 | A T2 PRIMARY delta attributable only to ordered ID-path (Claim B), not duplicated current facts / provenance / gold hints / extra authorization | PASS | PASS |
| 8 | SECONDARY gold not semantically derivable from T1 without trajectory | **BLOCKING** | PASS |

Contrast (not scored as live): CAND-01 PRIMARY gold was HOLD-12 + UNKNOWN (bar 2 fail / ceiling). CAND-02 PRIMARY was one UNKNOWN / one rejected; S1 “which UNKNOWN first” was list-order (bar 5). 03/04 fixed the PRIMARY ceiling. 03 re-imported a SECONDARY leak.

---

## Issues

| ID | Issue | Severity |
|----|-------|----------|
| R1 | CAND-03 S1 list-order: `u-ash` / `op-ash` are last | BLOCKING |
| R2 | CAND-03 S1 semantically derivable: ash is the unique hold that conflicts with email permission | BLOCKING |
| R3 | CAND-04 S1 list-order: rye is middle in constraints, unresolved, and unknown | PASS |
| R4 | CAND-04 S1 not uniquely derivable from “pack membership” alone | PASS |
| R5 | PRIMARY 6-way compose; gold ≠ one T1 sentence | PASS |
| R6 | All PRIMARY `must_compose` ids are currently-true on T1 | PASS |
| R7 | Thin path is ID_REFS_ONLY; no gold / “No. Compose…” text | PASS |
| R8 | T2 PRIMARY delta: no extra auth, no provenance types, no gold in package | PASS |
| R9 | Seq2 is a 3-id spotlight on the PRIMARY keystone hold | MINOR |
| R10 | Seq1 is still a near-complete ID catalog of current T1 (CAND-01 contrast) | MINOR |
| R11 | CAND-04 `k-chart4` contested vs PRIMARY “chart 4” | MINOR |
| R12 | 03/04 are isomorphic templates (same leak class will correlate) | MINOR |
| R13 | Score PRIMARY as `must_compose`, not Yes/No | MINOR |

---

## Bar 1 — T1 competence — PASS / PASS

C3-P1 `must_compose`: `d-pack`, `c-ops-list`, `c-email-outbound`, `c-hold-ash`, `c-prec`, `u-ash`. All present as current T1 rows. Decoy `c-mail-ok` is also current (needed so precedence has a member-permission to lose).

C4-P1 `must_compose`: `d-brief`, `c-portal`, `c-class-ext`, `c-hold-rye`, `c-prec`, `u-rye`. All current. Decoy `c-pub-ok` (internal wiki, not portal) is current.

No PRIMARY fact lives only on the thin path. Not impoverished.

---

## Bar 2 — gold not a one-field restatement — PASS / PASS

`current_rationale` on both: keep class / channel / precedence / ticket separate; do not invent clearance.  
`process_position`: “no channel/distribution action is named here.”

PRIMARY gold is a six-step compose ending in UNKNOWN clearance. That is not a copy of rationale, process_position, a single constraint, a single UNKNOWN, or a rejected alternative.

Contrast CAND-01 gold (“No outbound email… HOLD-12… UNKNOWN”) *was* that restatement. Fixed on 03/04.

---

## Bar 3 — composition required — PASS / PASS

`must_compose` is six currently-true ids. A single-row lookup does not yield the gold chain. This is the actual Claim B PRIMARY shape: fallible utilization of a competent T1.

---

## Bar 4 — still T1-sufficient — PASS / PASS

Every compose step is a current T1 fact. Trajectory is not required for PRIMARY. Required for Claim B; actually true here.

---

## Bar 5 — list order vs SECONDARY — BLOCKING on 03 / PASS on 04

### CAND-03 — BLOCKING (R1)

S1 gold: `c-hold-ash`.  
`why_not_on_T1` says constraint order is elm, ash, oak (ash middle) and IDs do not encode time.

Parallel arrays were not scrambled:

| Array | Order | ash position |
|-------|-------|----------------|
| `constraints` holds | elm, ash, oak | middle |
| `unresolved_items` | u-elm, u-oak, **u-ash** | **last** |
| `unknown_operations` | op-elm, op-oak, **op-ash** | **last** |

Seq2 ADDs `c-hold-ash`, `u-ash`, `op-ash`. On T1, the two ticket arrays **append** ash. Heuristic “the last UNKNOWN / last hold-ticket is newest” recovers S1 gold from T1 without `thin_trajectory`. Position is evidence. Bar 5 fail.

### CAND-04 — PASS (R3)

Holds flax, rye, maize. Rye is **middle** in `constraints`, `unresolved_items`, and `unknown_operations`. Seq2 rye is not an append-to-end leak. IDs do not encode time.

---

## Bar 6 — thin path does not re-deliver PRIMARY answer text — PASS / PASS

`thin_trajectory` entries are `{op, field, id}` only. No `from_state` / `to_state`. No “No. Compose:…” prose. PRIMARY answer text is not in the T2 add-on.

Ids in the path already exist as T1 row ids. That is an id echo, not a second copy of the gold sentence (R7).

---

## Bar 7 — T2 PRIMARY delta attribution — PASS / PASS

T2 add-on vs the v2.1 full-snapshot package:

- no event `type` / `SUPERSEDE_*` labels;
- no `accepted_at` / owner provenance block;
- no extra authorization rows;
- gold is not in the reader package;
- no current-state answer text on the path.

A PRIMARY T2 delta, if one ever appeared, would have to come from using the **ordered ID-path** (seq grouping / seq2) together with the same T1 bytes. That is Claim B’s intended quantity, not the v2.1 confounds.

Residuals (not bar fails):

- **R9 MINOR:** seq2 is exactly the three ids of the PRIMARY keystone hold (`c-hold-ash`+`u-ash`+`op-ash` / rye analog). Last-event salience can produce a bare “No” without walking `must_compose`. Ordered-path, but coarse scoring would mis-attribute. **R13:** score PRIMARY on the compose ids, not Yes/No.
- **R10 MINOR:** seq1 is still a near-complete ADD catalog of current T1 (CAND-01 “seq1 replay” shape). It does not print the PRIMARY sentence. Leave as hygiene if 03 is rebuilt.

---

## Bar 8 — SECONDARY semantically derivable from T1 — BLOCKING on 03 / PASS on 04

### CAND-03 — BLOCKING (R2)

S1: “Which hold id became current **after internal-email permission** was already current?”  
Gold: `c-hold-ash`.

T1, without time:

- `c-mail-ok`: internal drafts may be emailed;
- `c-email-outbound`: email is outbound;
- `c-hold-ash`: HOLD-ash applies to **all outbound**;
- `c-hold-elm`: Slack only;
- `c-hold-oak`: public blog only;
- `c-prec`: class hold outranks member permission.

Ash is the **unique** hold that conflicts with the named permission. Elm/oak do not apply to email. A reader who treats “the hold after email-permission” as “the hold that actually binds email” emits `c-hold-ash` with no trajectory.

That is semantic derivability, not a substring accident (`c-hold-ash` also appears as a current id, but the *selection among three holds* is what S1 tests). Bar 8 fail.

### CAND-04 — PASS (R4)

S1: “Which hold id became current **after the client pack membership** was already current?”  
Gold: `c-hold-rye`.

`d-brief` (pack includes charts 2, 4, 7) does not, by itself, pick among flax (press) / rye (external) / maize (social). Temporal order is not on T1.

Residual: PRIMARY’s portal→external→rye chain is on T1. A reader who **reinterprets** S1 as “which hold matters for the pack” can emit rye. That is a wording-discipline risk, not unique semantic entailment from “pack membership.” Not a bar-8 fail. Keep S1 wording strictly temporal; do not mention portal/external in S1.

---

## Other

**R11 MINOR (04):** `k-chart4` contests chart 4 vs 4b. C4-P1 asks “May chart 4 be published…”. Gold ignores the contest. A conservative T1 reader may answer UNKNOWN-which-chart. Bind it (contest does not block this probe) or drop the contest.

**R12 MINOR:** 03 and 04 are the same machine with swapped nouns. One leak class hits both if it exists. After 03 is rebuilt, keep 04’s middle-list discipline; do not clone 03’s append pattern onto 04.

---

## Recommended Labs action

1. **Do not** start Field 5 / reader freeze / model run.
2. Rebuild CAND-03 SECONDARY (or replace 03): scramble *all* arrays so the later hold is not last; make S1 gold **not** the unique hold that binds the permission named in the question (or drop the permission from the S1 wording).
3. Keep CAND-04 list-middle discipline; tighten S1 so it cannot be read as PRIMARY-lite.
4. If PRIMARY is ever scored, require `must_compose` ids (R13).
5. Re-review the rebuilt 03 (and 04 if touched) before any Field-5 discussion.

```text
NOT_READY_FOR_FIELD_5
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
CANDIDATE ≠ PILOT ≠ EVIDENCE
```

STOP. Docs-only. No experiment. No merge. No architecture.
