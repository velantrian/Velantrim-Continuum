# CONT-E0T v2.1 Redteam Delta

**Reviewed commit:** `163ab9a27e90eb08bc3d8d2349e1f171cb8c54cf`  
**Worktree:** `/workspace/cont-e0t/v21-redteam`  
**Branch:** `research/cont-e0t-v21-redteam-delta`  
**Role:** CONT-REDTEAM delta (not a new conceptual round; not the v1 blind attack)  
**v2.1 status under review:** CANDIDATE (owner accepted Claim B only). Not a freeze. Not experiment authorization.  
**Not read:** `/workspace/cont-e0t/v21-integrity`; Author v1 (not used to rewrite science).  
**Not done:** model run, paid run, merge, PR, edits to v2.1 scientific files.

Scope is the new material at `163ab9a` only:

- `docs/research/CONT_E0T_PREREGISTRATION_V2_CANDIDATE.md` (v2.1)
- `docs/research/cont_e0t_v2/fixtures/CONT_E0T_FX_01.json`
- `docs/research/cont_e0t_v2/fixtures/CONT_E0T_FX_02.json`
- `docs/research/cont_e0t_v2/fixtures/manifest.json`
- `docs/research/cont_e0t_v2/reader_prompt_v2.txt`
- `docs/research/cont_e0t_v2/validate_cont_e0t_v2_package.py`

Severity vocabulary for this delta: **BLOCKING | MAJOR | MINOR | PASS** only.

Package validator was run as structure audit (no reader, no model): stdout `PASS`, exit 0. That result is **not** used as science (see D6).

---

## Verdict (delta)

v2.1 is a coherent **PILOT package skeleton** for Claim B: partitions are labeled, PRIMARY probes are T1-solvable, pad is withdrawn, hashes match, EVIDENCE is empty.

It does **not** yet operationalize Claim B as a discriminating test. FX-01/FX-02 are explicit copy-from-`current_semantics` items. CONT-T2 is not a compact trajectory add-on: it re-delivers full state snapshots plus fused provenance, at ~5× T1 bytes. F6 prose item 5 is **not** what the validator checks.

**Do not freeze. Do not promote PILOT to Evidence. Do not read validator `PASS` as authenticity of the strong F6 predicate or as Claim B evidence.**

---

## Index

| ID | Issue | Severity |
|----|-------|----------|
| D1 | FX-01/FX-02 ceiling: too explicit to discriminate Claim B | MAJOR |
| D2 | Every PRIMARY probe is solvable from CONT-T1 without historical facts | PASS |
| D2b | `current_rationale` carries supersession narrative inside CONT-T1 | MINOR |
| D3 | Any PRIMARY CONT-T2 win still confounded (snapshots / bytes / type labels) | MAJOR |
| D4 | Provenance fused with trajectory; no `provenance` object | MAJOR |
| D5 | F6 validator: item 5 ≡ item 3 (`from_state != current`); stronger claim not checked | BLOCKING |
| D6 | Validator `PASS` = package/structural only | PASS |
| D6b | stdout `PASS` is easy to over-read | MINOR |
| D7 | Fixtures are PILOT shakedown only; EVIDENCE empty | PASS |
| D8 | FX01-S1 gold recoverable from T1 `rejected_alternatives` | MAJOR |
| D9 | Field 9 `envelope_pad` withdrawn | PASS |
| D10 | HARD FAIL atoms exist; match spec and `HF_SIBLING_LEAK` fixture binding still open | MINOR |
| D11 | Prompt mentions arm / ledger / absent history | MINOR |
| D12 | Validator does not check chain `to_state[i]==from_state[i+1]` or `canonical_json_sha256` | MINOR |

---

## D1 — Ceiling / non-discrimination of Claim B — MAJOR

Claim B (owner-accepted): practical utilization benefit of bounded genuine trajectory for a **fallible** reader beyond the **same** bounded CONT-T1.

FX-01/FX-02 PRIMARY gold is almost a restatement of `current_semantics`:

| Probe | Gold (abbrev.) | Already written on CONT-T1 |
|-------|----------------|----------------------------|
| FX01-P1 | staging dry-run only; no prod | `d-staging`, `c-staging-ok`, `process_position` |
| FX01-P2 | no Friday prod until Monday 09:00 | `c-freeze`, `r-friday` |
| FX01-P3 | tag UNKNOWN | `unknown_operations[op-tag-check]`, `u-tag` |
| FX01-P4 | mid-task after freeze; staging only | `task_position`, `process_position` |
| FX02-P1 | read-only export; no write; no PII | `c-read-only`, `c-pii`, `process_position` |
| FX02-P2 | write not granted | `r-write`, `c-read-only` |
| FX02-P3 | LGL-884 UNKNOWN | `op-lgl-884`, `u-legal` |

A reader that copies `process_position` + `constraints` + `unknown_operations` satisfies PRIMARY. There is little room for the fallibility Claim B needs. Expected honest PILOT outcome if a model is ever run: **B-TIE-ADEQ**, which does not exercise utilization-of-trajectory.

Appropriate as **wiring/shakedown** objects (tags, hashes, HARD FAIL strings). **Not** appropriate as Claim B discriminators or as a freeze set.

Candidate already says `primary_solvable_from_T1: true` and that these cannot test claim A. It still labels `claim_under_test: "B"`. That label is aspirational for this pair.

---

## D2 — PRIMARY solvable from CONT-T1 — PASS

Checked probe-by-probe against `current_semantics` only (no `accepted_trajectory`).

All seven PRIMARY probes have currently-true gold in CONT-T1. None requires `from_state`, `seq`, or a superseded id. Tags `PRIMARY_RESUME` + `primary_solvable_from_T1: true` match the T1 bytes.

This is required for Claim B and is actually done.

### D2b — T1 rationale is a change-set in prose — MINOR

FX-01 `current_rationale`: “The freeze **supersedes** the Friday production window.”

F4 forbids change-sets on CONT-T1. The validator only forbids keys `accepted_trajectory` / `envelope_pad` on `current_semantics`, not supersession language in `current_rationale`. Residual F4 surface. Does not make PRIMARY unsolvable from T1; it makes T1 *easier* (another ceiling contributor).

---

## D3 — PRIMARY CONT-T2 advantage still confounded — MAJOR

Measured delivered size (JSON of `current_semantics` vs `current_semantics`+`accepted_trajectory`):

| Fixture | CONT-T1 bytes | CONT-T2 bytes | ratio |
|---------|--------------:|--------------:|------:|
| FX-01 | 1230 | 6671 | 5.42 |
| FX-02 | 1227 | 5815 | 4.74 |

CONT-T2 is not “same current object plus a thin event list.” Each event carries a **full** `from_state`/`to_state`. Last `to_state` is byte-identical to `current_semantics`. The reader sees current facts again, plus intermediate snapshots, plus type labels (`SUPERSEDE_CONSTRAINT`, `ACCEPT_AND_REJECT`).

A PRIMARY T2 win on these packages would be unidentified among:

- extra copies of current semantics (redundancy / presentation);
- ~5× tokens/bytes (Field 8/9 residual);
- event `type` / `supersedes` hints;
- actual trajectory utilization (the Claim B quantity).

Pad withdrawal (D9) correctly refused fake T1 filler. It did **not** remove the unmatched T2 bulk confound.

---

## D4 — Provenance treatment-confounded with trajectory — MAJOR

v2.1 §2: `CONT-T2 = byte-identical current_semantics + accepted_trajectory[] + provenance`.

Fixture JSON has **no** `provenance` object (`"provenance" in fx == False`). Provenance lives **inside** trajectory events: `type`, `seq`, `accepted_at`, `supersedes`.

Those fields are a second treatment, delivered only to CONT-T2. `type: "SUPERSEDE_CONSTRAINT"` plus `supersedes: ["c-weekday","d-friday"]` is not the state path; it is a labeled history commentary. It cannot be partialled out from trajectory on these packages.

**Bounded correction required before freeze** (protocol split, not an architecture):

1. Name three payloads: `current_semantics` | `accepted_trajectory` (path: `seq`,`from_state`,`to_state`) | `provenance` (`type`,`accepted_at`,`supersedes`, owner if any).
2. Reader packages for Claim B PRIMARY must not mix (2) and (3) if a T2-PRIMARY delta will be read as trajectory utilization.
3. Either omit `provenance` from both reader arms (keep it validator-only), or give currently-true provenance refs to **both** arms.
4. Do not freeze while (2) also re-embeds full current snapshots (D3).

Until that split exists, do not interpret a PRIMARY T2 delta as Claim B.

---

## D5 — F6 validator ≠ F6 prose — BLOCKING

Candidate §3.5 AUTHENTIC iff (among other items):

3. at least one `from_state` ≠ final `current_semantics`;
5. at least one `from_state` not reconstructable from the final snapshot by field-wise `SET`.

`validate_cont_e0t_v2_package.py` implements **the same predicate twice**:

```text
any(canon(from_state) != canon(current_semantics))
```

once as “no from_state distinct from final current”, again as “from_state reconstructable from final only.”

That is **not** a field-wise SET reconstruction test. `from_state != current` is passed by:

- empty / “not started” snapshots (FX-02 seq 1);
- current-minus-one-field subsets;
- any object that is not canonical-JSON-equal to final, including ones whose values are all present on the final snapshot.

What PASS **does** certify here: length 2–max; some `supersedes` nonempty; last `to_state` == current; not every `to_state` == current; not the literal `{seq,op,field,value}` / `op==SET` shape.

What PASS **does not** certify: §3.5 item 5; “from_state cannot be reconstructed from the final snapshot alone.”

These two fixtures *happen* to contain intermediate text absent from final (`c-weekday` / “Production deploys allowed on weekdays” on FX-01 seq 1–2). That is **not** what the code checks. Do not upgrade F6 to closed on the basis of this PASS.

Chain continuity `to_state[i] == from_state[i+1]` holds on both fixtures by inspection; the validator does not check it (D12).

---

## D6 — Validator PASS semantics — PASS

Docstring: “Not a reader. Not an experiment. No model calls.”  
Candidate §3.5: “package only; no reader.”  
§5: EVIDENCE partition empty.  
stdout includes “no model run.”

**PASS = PACKAGE/STRUCTURAL PASS only.** Not science, not Evidence, not Claim B, not F6.5.

### D6b — MINOR

Bare stdout `PASS` is still over-brief. A later human can quote it as experimental success. Rename in a later revision to `PACKAGE_STRUCTURAL_PASS` (do not treat this delta as that patch).

---

## D7 — PILOT vs Evidence — PASS

- `partition: PILOT` on both fixtures; manifest `EVIDENCE: []`; validator fails if EVIDENCE is nonempty.
- Candidate: “Not ready for Evidence fixtures.” `EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED`. `FROZEN_FIELDS = 0 / 10`.
- `copied_from_e0t_transfer: false` (not historical E0-T scenarios).

**Do not promote this PILOT pair to Evidence or generalization.** Two explicit fixtures cannot support reader-general Claim B even after a clean shakedown.

---

## D8 — SECONDARY_HISTORY leak on FX01-S1 — MAJOR

FX01-S1 gold: “Friday 16:00.”  
CONT-T1 `rejected_alternatives[r-friday].text`: “Ship production Friday 16:00”.  
`Friday 16:00` is in the T1 JSON.

`primary_solvable_from_T1: false` is therefore **false as science** even if the wording says “previously accepted.” A T1 reader can emit the gold without trajectory. That contaminates the Claim C / C-ONLY channel on FX-01.

FX01-S2 gold (`c-weekday`) is **not** on T1 — that secondary is cleaner.  
FX02-S1 (`Read+write; not yet decided`) is **not** on T1.  
FX02-S2 needs order — T1-insufficient, OK.

---

## D9 — `envelope_pad` withdrawn — PASS

Owner/v2.1: do not pad CONT-T1 to force token equality. Validator forbids `envelope_pad`. Matches the v1 pad-is-itself-a-confound objection.

Residual unmatched T2 bulk remains (D3). Candidate Field 9 stays PARTIAL; this delta does not re-open pad as required.

---

## D10 — HARD FAIL / ResumeAdequacy — MINOR

§3.8 atoms are named. Both fixtures bind HF_FABRICATED_AUTH / HF_CONSTRAINT / HF_LOST_UNKNOWN / HF_INVALID_RESUME_POINT to concrete actions.

Still open (candidate Field 6/10): match specification / inter-rater rule. `HF_SIBLING_LEAK` is in §3.8 and **not** in either fixture `hard_fail_bindings`. ADEQUATE := no HARD FAIL and all PRIMARY `resume_atoms` — no executable matcher in this package (correct for no-run; not a freeze).

---

## D11 — Prompt — MINOR

Same file for both arms (`reader_prompt_v2.txt`, SHA matches manifest). Good.

Text still names “another arm”, “missing ledger”, and “that history is absent.” That is the pattern “do not tell the baseline it lacks X,” encoded as a prohibition that **informs** the baseline. Shared text ≠ unprimed text. Fine for PILOT shakedown; not freeze-grade prompt symmetry.

---

## D12 — Validator coverage gaps — MINOR

Not checked, though fixtures currently satisfy some of them:

- event chain `canon(to_state[i]) == canon(from_state[i+1])`;
- `seq` consecutive from 1;
- manifest `canonical_json_sha256` (file SHA is checked; canonical SHA is recorded and unused);
- presence/absence of a `provenance` object (D4);
- distinct F6.5 predicate (D5).

---

## Answers to the seven tests

1. **Claim B exercise vs ceiling?** Ceiling. FX-01/FX-02 do not discriminate Claim B. **MAJOR.** Shakedown-only.
2. **PRIMARY solvable from CONT-T1 without history?** **PASS** for all PRIMARY probes.
3. **PRIMARY T2 advantage confounded?** **Yes — MAJOR** (snapshot copies, bytes, type labels).
4. **Provenance confounded with trajectory?** **Yes — MAJOR.** Bounded correction (D4) required before freeze.
5. **F6 validator vs “not reconstructable from final snapshot”?** Code checks `from_state != current` twice. **BLOCKING** to treat F6.5 / strong authenticity as shown.
6. **Validator PASS = package/structural only?** **PASS** (D6). Not science, not evidence.
7. **Shakedown vs Evidence?** **PASS** as labeled PILOT. **Do not promote to Evidence.**

---

## Freeze / authorization (unchanged)

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
FINAL_PREREG_REVIEW      = NOT_READY
FROZEN_FIELDS            = 0 / 10
PILOT ≠ EVIDENCE
validator PASS ≠ science
```

STOP. Docs-only delta. No experiment. No merge. No architecture.
