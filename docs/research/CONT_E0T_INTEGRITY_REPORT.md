# CONT-E0T Integrity Report

**Report role:** CONT-INTEGRITY (reproducibility and state-integrity only)  
**Repository:** `velantrian/Velantrim-Continuum`  
**Integrity branch:** `research/cont-e0t-integrity`  
**Integrity worktree:** `/workspace/cont-e0t/integrity`  
**Report date:** 2026-09-12 (Europe/Berlin)

This report does **not** decide whether CONT-T1 or CONT-T2 is scientifically correct. It does **not** rewrite sealed Author or RedTeam files. It records process and state integrity only.

---

## 0. Sealed inputs named by this report

| Role | Branch | Commit SHA | Artifact path | Artifact blob |
|---|---|---|---|---|
| Frozen baseline (`origin/main` tip at lock) | `main` | `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5` | — | — |
| Author | `research/cont-e0t-prereg-author` | `4a026c1ef7844cc95873d6155b311c2853346fe8` | `docs/research/CONT_E0T_PREREGISTRATION_CANDIDATE.md` | `44a6a13bfd516d7a1d4b3fc5c99bc2369b8e5d41` |
| RedTeam | `research/cont-e0t-redteam` | `1069ee39c8ad53251964ebd00c6ee3dfbdf21bac` | `docs/research/CONT_E0T_BLIND_REDTEAM_REVIEW.md` | `041d4038a164d6845da44e0087c6d2c65033c0ae` |

Historical E0-T preregistration blob (unchanged in baseline, Author, and RedTeam trees):

`docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md` = `82a11e13e44fc44e86e3327a2a7a69509571118c`

Author commit time: `2026-09-12T14:54:15Z` (16:54:15 Berlin).  
RedTeam commit time: `2026-09-12T14:55:40Z` (16:55:40 Berlin).  
Both commits have **exactly one parent**: baseline `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`.

Integrity inspected those commits via `git show` / `diff-tree` from the integrity worktree. Sealed files were not edited.

---

## 1. Checklist (state integrity)

| Check | Verdict | Evidence |
|---|---|---|
| Same baseline SHA used by all | **PASS** | Author parent, RedTeam parent, and Phase 1 lock HEAD are all `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`. Both artifacts print that SHA as **BASELINE SHA**. |
| No silent source-file changes outside authorized `docs/research` new files | **PASS** | `git diff-tree` vs baseline: Author adds only `docs/research/CONT_E0T_PREREGISTRATION_CANDIDATE.md` (+389 / −0). RedTeam adds only `docs/research/CONT_E0T_BLIND_REDTEAM_REVIEW.md` (+420 / −0). No other path in either commit. |
| Worktrees / branches cleanly separated | **PASS** | Distinct branches and worktrees: `research/cont-e0t-prereg-author`, `research/cont-e0t-redteam`, `research/cont-e0t-integrity`. Neither sealed commit is an ancestor of the other. Integrity HEAD at report write is still the baseline (this report is the first integrity commit). |
| No experiment / paid model run | **PASS** | Both commits are docs-only markdown. No result, receipt, usage, or run-log files. Author status is candidate-only and states it is not experiment execution or a paid model run. RedTeam header: experiment execution none. No score / cost / API-run markers in either artifact. |
| Old synthetic `event_projection` not treated as genuine accepted trajectory | **PASS** | Author Field 2 / Field 4: a CONT-T2 package that is only a serialization of the final snapshot (synthetic `SET_*` / fake SET-from-final-state) is **protocol-invalid** for trajectory credit. RedTeam F5/F6: historical `event_projection` SET-from-Oracle is the non-isolating construction and is **not** specified as CONT-T2 genuine accepted trajectory. Neither sealed artifact presents historical `event_projection` output as a genuine accepted trajectory. |
| Every artifact names its input source SHA | **PASS** | Author names `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5` (header + Field-status SOURCE CONFLICT line). RedTeam names the same full SHA (header + blindness HEAD) and short `78a73ed` in source-conflict notes. No other input commit SHAs appear. This report names baseline, Author, and RedTeam SHAs above. |
| No Author / reviewer cross-contamination before blind commits | **PASS** | Separate paths; neither tree contains the other artifact. Author commit does not mention RedTeam SHA, RedTeam filename, or RedTeam-unique headings. RedTeam header: **Author candidate: not read**. RedTeam mentions `CONT_E0T_PREREGISTRATION_CANDIDATE.md` only in the “was not opened” list (protocol filename), and does **not** cite Author SHA `4a026c1…` or Author-unique section titles / body strings. Commit times differ by 85 seconds (Author first). Sealed files were not rewritten after unblind. |
| No architecture / runtime promotion | **PASS** | Author: not architecture authority; stopping rule forbids architecture promotion. RedTeam: architecture promotion none; non-claims forbid architecture / organ / storage / runtime. This report promotes none. |
| No rewrite of historical E0-T prereg | **PASS** | `IDPS_EXPERIMENT_0_PREREGISTRATION.md` blob identical in baseline, Author commit, and RedTeam commit (`82a11e13e44fc44e86e3327a2a7a69509571118c`). Neither `diff-tree` touches that path. |

---

## 2. Phase 1 lock (restated)

Recorded before unblind:

- Worktrees present: `/workspace/cont-e0t/author`, `/workspace/cont-e0t/redteam`, `/workspace/cont-e0t/integrity`
- All three HEADs were `78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`
- Historical prereg unmodified vs baseline
- No experiment results; no paid model run
- Integrity did not open sibling scientific drafts during Phase 1

---

## 3. What this report does not do

- Does not judge scientific adequacy of CONT-T1 vs CONT-T2, the Author candidate, or the RedTeam findings.
- Does not merge, open a PR, change `project-state.json`, or authorize Pilot / Evidence / execution.
- Does not edit Author or RedTeam sealed files after unblind.

---

## 4. Integrity verdict

**INTEGRITY: PASS**

All listed state-integrity checks pass. Authorized outputs are two new `docs/research` files on separate branches, both parented at the locked baseline SHA, with no source rewrite, no historical E0-T prereg rewrite, no experiment or paid-model run, and no detected pre-commit cross-contamination.

🛑 STOP after this docs-only integrity commit. No experiment. No architecture promotion. No scientific T1/T2 decision.
