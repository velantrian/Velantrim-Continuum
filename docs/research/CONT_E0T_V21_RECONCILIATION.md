# CONT-E0T v2.1 Labs Reconciliation

**Labs coordinator artifact.** Not a vote. Not a freeze. Not experiment authorization.  
**Reviewed candidate:** `163ab9a27e90eb08bc3d8d2349e1f171cb8c54cf`  
**Branch:** `research/cont-e0t-v21-reconciliation`  
**Repository:** `velantrian/Velantrim-Continuum`

Allowed row labels (this file only): `KEEP` | `CORRECT_BEFORE_FREEZE` | `PILOT_ONLY` | `BLOCKING`

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
FINAL_PREREG_REVIEW      = NOT_READY
FROZEN_FIELDS            = 0 / 10
PILOT ≠ EVIDENCE
validator PASS ≠ science
```

Sealed delta inputs (do not rewrite):

| Role | Artifact | Commit | Parent |
|------|----------|--------|--------|
| CONT-REDTEAM | `docs/research/CONT_E0T_V21_REDTEAM_DELTA.md` | `aec263c7cd37a8d5f1750aef0c015a981ced181d` | `163ab9a` |
| CONT-INTEGRITY | `docs/research/CONT_E0T_V21_INTEGRITY_DELTA.md` | `f198f0358c3f0bc0656a5c7c95d1219befa9a39c` | `163ab9a` |

Owner: Claim B remains accepted. v2.1 remains a **CANDIDATE**. This pass does not select a reader, construct Evidence fixtures, merge, or open a PR.

---

## 1. Shared process facts (Integrity)

Integrity **PASS with PROCESS NOTE**. Labs verified the SHA and parent.

KEEP as process:

- `docs/research` scope only vs `8c0da8b` and vs `78a73ed`
- FX-01 / FX-02 / prompt SHA-256 match disk + manifest
- EVIDENCE `[]`; validator fail-closes if nonempty
- validator script exit 0 (`PASS`)
- no paid run; no PR/merge
- sealed v1 Author `4a026c1` / RedTeam `1069ee3` / Integrity `35d935e` untouched
- historical E0-T prereg blob unchanged (`82a11e13e44fc44e86e3327a2a7a69509571118c`)

Integrity process note and RedTeam D5 name the **same gap**: stated F6 clause 5 is not a distinct executable check.

---

## 2. Reconciliation matrix

| ID | Topic | RedTeam | Integrity | Labs label | Why |
|----|-------|---------|-----------|------------|-----|
| D5 / F6.5 | “not reconstructable from final snapshot by field-wise SET” | BLOCKING | PROCESS NOTE (same fact) | **BLOCKING** | Code repeats `from_state != current`. Do not treat F6.5 / strong authenticity as shown. Either implement a distinct SET-reconstruction check or rewrite §3.5 so prose ≤ code. Until then, authenticity is **not freezeable**. |
| D1 | FX-01/FX-02 ceiling | MAJOR | (no science call) | **PILOT_ONLY** | PRIMARY gold restates `current_semantics`. Fine for wiring/shakedown. Not Claim B discriminators. Do not promote. |
| D2 | PRIMARY solvable from CONT-T1 | PASS | — | **KEEP** | Required for Claim B; actually true on all seven PRIMARY probes. |
| D2b | T1 `current_rationale` says “supersedes” | MINOR | — | **PILOT_ONLY** | Residual F4 surface; also raises the ceiling. Correct if these fixtures are ever reused past shakedown. |
| D3 | T2 ~5× bytes + full snapshot copies + type labels | MAJOR | — | **CORRECT_BEFORE_FREEZE** | Pad withdrawal did not remove unmatched T2 bulk / re-delivered current snapshots. A PRIMARY T2 delta on these packages is unidentified (presentation / bytes / labels vs utilization). |
| D4 | Provenance fused with trajectory | MAJOR | — | **CORRECT_BEFORE_FREEZE** | §2 names `+ provenance` but fixtures have no `provenance` object; `type` / `accepted_at` / `supersedes` ride inside events and are T2-only. Split payloads before any freeze that will read a T2 PRIMARY delta as Claim B. |
| D6 | Validator PASS semantics | PASS | PASS (script only) | **KEEP** | PACKAGE/STRUCTURAL only. Not science, not Evidence, not F6.5. |
| D6b | stdout `PASS` over-brief | MINOR | notes unused `canonical_json_sha256` | **PILOT_ONLY** | Later rename to `PACKAGE_STRUCTURAL_PASS` if the script is kept. |
| D7 | PILOT vs Evidence | PASS | PASS empty EVIDENCE | **KEEP** / **PILOT_ONLY** | Label is correct. **Do not promote.** Two explicit fixtures cannot support generalization. |
| D8 | FX01-S1 gold on T1 `rejected_alternatives` | MAJOR | — | **CORRECT_BEFORE_FREEZE** | Contaminates Claim C / C-ONLY on FX-01. FX01-S2 / FX02-S* are cleaner. |
| D9 | `envelope_pad` withdrawn | PASS | — | **KEEP** | Do not restore pad. Token equality remains not required. |
| D10 | HARD FAIL atoms vs match spec | MINOR | — | **PILOT_ONLY** | Atoms exist; matcher / `HF_SIBLING_LEAK` fixture binding still open. Correct before freeze, not blocking for shakedown docs. |
| D11 | Prompt names arm / ledger / absent history | MINOR | — | **PILOT_ONLY** | Shared file is good; prohibition still primes the baseline. |
| D12 | No chain / canonical-hash checks | MINOR | same unused hash field | **PILOT_ONLY** | Coverage gaps; fixtures happen to chain. |

Labs does **not** majority-vote D5 down. Integrity’s “not a science call” does not cancel RedTeam’s BLOCKING on over-claiming the validator.

---

## 3. What v2.1 is allowed to be

| Allowed now | Forbidden now |
|-------------|----------------|
| Claim B remains the working claim (owner) | Treating v2.1 as frozen protocol |
| PILOT package skeleton / infrastructure shakedown | Promoting FX-01/FX-02 to Evidence |
| KEEP items above | Reading validator `PASS` as authenticity or Claim B |
| Field 9 stays PARTIAL, no pad | Selecting/running a reader |
| | Constructing Evidence fixtures |
| | Merge / PR |

---

## 4. Before any freeze (not this commit)

Must close, in a later owner-authorized pass — **not done here**:

1. **BLOCKING:** F6.5 — distinct SET-from-final reconstruction check, or prose downgrade.
2. **CORRECT_BEFORE_FREEZE:** provenance / trajectory payload split (D4).
3. **CORRECT_BEFORE_FREEZE:** T2 delivery that does not re-embed full current snapshots as the only trajectory form (D3), or an explicit residual-confound statement that forbids Claim B attribution on these packages.
4. **CORRECT_BEFORE_FREEZE:** FX01-S1 gold must not sit on CONT-T1 (D8).
5. Discriminating Claim B fixtures (if a freeze is still wanted) — **new objects**, not a promotion of FX-01/FX-02.

This reconciliation does **not** edit `163ab9a` science files.

---

## 5. Decision

```text
CANDIDATE                = 163ab9a (unchanged)
IDENTIFIABILITY_B        = OWNER_ACCEPTED (unchanged)
BLOCKING                 = F6.5 over-claim
CORRECT_BEFORE_FREEZE    = D3, D4, D8
PILOT_ONLY               = FX-01, FX-02, D1, D2b, D10, D11, D12
KEEP                     = D2, D6, D7 labels, D9 no-pad, Integrity process PASS
FINAL_PREREG_REVIEW      = NOT_READY
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
```

STOP for owner review. No reader. No Evidence. No merge. No PR.
