# CONT-E0T v2.1 Integrity Delta

**Report role:** CONT-INTEGRITY (process / state only)  
**Repository:** `velantrian/Velantrim-Continuum`  
**Integrity branch:** `research/cont-e0t-v21-integrity-delta`  
**Integrity worktree:** `/workspace/cont-e0t/v21-integrity`  
**Report date:** 2026-09-12 (Europe/Berlin)

This report does **not** decide CONT-T1 vs CONT-T2 science. It does **not** edit v2.1 science files. It does **not** authorize a freeze, experiment, merge, or PR.

Owner framing recorded here as given: commit `163ab9a27e90eb08bc3d8d2349e1f171cb8c54cf` is a **CANDIDATE**, not a freeze, not experiment authorization.

The v2.1-redteam worktree was **not** opened.

---

## 0. Inputs named by this report

| Object | SHA |
|---|---|
| Frozen Continuum baseline | `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5` |
| v2.1 candidate parent | `8c0da8b34c702cbc5446c971238fa32227db1a56` |
| v2.1 candidate under review | `163ab9a27e90eb08bc3d8d2349e1f171cb8c54cf` |
| Sealed v1 Author | `4a026c1ef7844cc95873d6155b311c2853346fe8` |
| Sealed v1 RedTeam | `1069ee39c8ad53251964ebd00c6ee3dfbdf21bac` |
| Sealed v1 Integrity | `35d935e78fd87a584a73fd520d09f9b2465d8ad0` |

`163ab9a` subject: `docs(research): CONT-E0T v2.1 PILOT fixtures; withdraw envelope_pad`  
Commit time: `2026-09-12T15:18:41Z` (17:18:41 Berlin). Single parent `8c0da8b`. Not a merge.

Lineage `78a73ed..163ab9a` is two docs commits only (`8c0da8b`, then `163ab9a`).

---

## 1. Path scope

`git diff --name-status 8c0da8b 163ab9a`:

| Status | Path |
|---|---|
| M | `docs/research/CONT_E0T_PREREGISTRATION_V2_CANDIDATE.md` |
| A | `docs/research/cont_e0t_v2/fixtures/CONT_E0T_FX_01.json` |
| A | `docs/research/cont_e0t_v2/fixtures/CONT_E0T_FX_02.json` |
| A | `docs/research/cont_e0t_v2/fixtures/manifest.json` |
| A | `docs/research/cont_e0t_v2/reader_prompt_v2.txt` |
| A | `docs/research/cont_e0t_v2/validate_cont_e0t_v2_package.py` |

`git diff --name-status 78a73ed 163ab9a`: the same six paths (all `A` vs baseline, except the candidate markdown is also new vs baseline). Parent `8c0da8b` vs baseline adds only `docs/research/CONT_E0T_PREREGISTRATION_V2_CANDIDATE.md`.

**No path outside `docs/research`.** **PASS**

---

## 2. Hashes and manifest

On-disk SHA-256 (raw file bytes) vs Labs-named values and vs `fixtures/manifest.json`:

| Item | Expected | On disk | Manifest |
|---|---|---|---|
| FX-01 `CONT_E0T_FX_01.json` | `48be07139b3106a4701e38417b31557fb833b703df2aafc5700a0cfa422dd07d` | match | `file_sha256` match |
| FX-02 `CONT_E0T_FX_02.json` | `cdbe362463a077972932a8feba1f753c214b3abfd57269717ca205def890f340` | match | `file_sha256` match |
| Reader prompt `reader_prompt_v2.txt` | `73668419a2135e293ef3902a7a974012454ace61cc16ca14fa858f741bfb5db3` | match | `reader_prompt_sha256` match |

Manifest consistency:

- `partition.PILOT` = `CONT-E0T-FX-01`, `CONT-E0T-FX-02`
- `partition.EVIDENCE` = `[]`
- each row `n_transitions` = `3` (= on-disk `n_transitions` and `len(accepted_trajectory)`)
- `n_transitions_max` = `4`
- `copied_from_e0t_transfer` = `false` (manifest and both fixtures)
- both fixtures `partition` = `PILOT`

Independent recompute of manifest `canonical_json_sha256` matches both files. The validator script does **not** check that field (see §5).

**PASS**

---

## 3. Validator run

Command: `python3 docs/research/cont_e0t_v2/validate_cont_e0t_v2_package.py`  
Working tree: `/workspace/cont-e0t/v21-integrity` at `163ab9a`

```text
PASS
fixtures CONT-E0T-FX-01, CONT-E0T-FX-02
claim B; no envelope_pad; no model run
```

Exit code `0`. **PASS** (script result only; see §5 for predicate coverage)

---

## 4. Other process checks

| Check | Verdict | Evidence |
|---|---|---|
| No model calls / no paid run | **PASS** | Validator imports only stdlib (`hashlib`, `json`, `sys`, `pathlib`). No HTTP, no vendor SDKs. Candidate header: no experiment / no paid run. `163ab9a` adds no run logs or receipts. |
| No PR / merge | **PASS** | `163ab9a` has one parent. Message says no PR. This delta does not open a PR or merge. |
| EVIDENCE partition empty | **PASS** | Manifest `EVIDENCE: []`. Validator fail-closes if that list is nonempty. Fixture files are PILOT only. |
| Sealed v1 commits untouched | **PASS** | Objects `4a026c1…`, `1069ee3…`, `35d935e…` still resolve to the original commit SHAs and messages. v1 Author / RedTeam / Integrity worktree HEADs still those SHAs. `163ab9a` is **not** a descendant of those commits and does not rewrite their trees. |
| No historical E0-T rewrite | **PASS** | `docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` blob `82a11e13e44fc44e86e3327a2a7a69509571118c` in baseline, `8c0da8b`, and `163ab9a`. |

---

## 5. Process note: stated F6 vs what the validator enforces

Candidate §3.5 (`AUTHENTIC` iff all hold) names seven clauses. The validator is cited there as the checker. Integrity compared the **stated list** to the **code**, not the scientific merit of F6.

| Stated §3.5 clause | What the code does |
|---|---|
| 1. Experimenter-authored, not model-emitted | Checks `authorship == EXPERIMENTER_AUTHORED`. Does not inspect git history or generation provenance. |
| 2. `len(accepted_trajectory) >= 2` and `<= n_transitions_max` | Enforced via `n`/`nmax` integers, `n <= nmax`, `len(traj) == n`, `len(traj) >= 2`. |
| 3. At least one `from_state` ≠ final `current_semantics` | Enforced (`canon(from_state) != canon(current)`). |
| 4. At least one nonempty `supersedes` | Enforced (`any(ev.get("supersedes"))`). |
| 5. At least one `from_state` **not reconstructable from the final snapshot by field-wise `SET`** | **Not independently enforced.** Lines 79–81 use the **same** test as clause 3 (some `from_state` canonically ≠ final current). Comment claims field-wise SET non-reconstructability; the body does not build a SET-from-final expansion or compare field values to that construction. |
| 6. Last `to_state` equals `current_semantics` | Enforced. |
| 7. Not historical E0-T `{SET field := current[field]}` | Partial. Rejects `op == "SET"` or key set exactly `{seq, op, field, value}`, and rejects “every `to_state` == final current”. Comment on the latter says it also requires every `from_state` == current; the `if` does not test `from_state`. Does not synthesize the historical SET-from-final event list and diff against `accepted_trajectory`. |

Duplicate: the clause-3 test is executed twice (lines 75–76 and 79–81). The second is labeled as clause 5.

Also not checked by the validator, though present in the manifest: `canonical_json_sha256` (on-disk values do match; recorded here only).

This is a **process coverage gap** between the written authenticity predicate and the executable checker. It is **not** a CONT-T1 vs CONT-T2 scientific verdict, and it does **not** authorize rewriting the candidate.

---

## 6. Verdict

**INTEGRITY DELTA: PASS with PROCESS NOTE**

All requested state checks pass: `docs/research` scope only; named file SHA-256s match; manifest PILOT/EVIDENCE/`n_transitions` consistent; validator script **PASS**; no paid run; no PR/merge; EVIDENCE empty; sealed v1 SHAs intact; historical E0-T prereg blob unchanged.

Process note (not a science call): stated F6 clause 5 (“cannot be reconstructed from the final snapshot by field-wise SET”) is not implemented as a distinct check. The executable test is clause 3 repeated.

`163ab9a` remains a **candidate**. Not a freeze. `EXPERIMENT_AUTHORIZATION` is not granted by this report.

🛑 STOP. No science edit. No experiment. No merge. No PR. No T1/T2 decision.
