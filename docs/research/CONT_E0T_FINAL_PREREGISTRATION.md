# CONT-E0T Final preregistration freeze

**Gate:** `READY_FOR_OWNER_GO`  
**Not:** experiment execution. `EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED` until a **separate** explicit owner GO.

```text
READY_FOR_OWNER_GO           = YES
EXPERIMENT_AUTHORIZATION     = NOT_AUTHORIZED
FINAL_PREREG_REVIEW          = FROZEN_PENDING_OWNER_GO
NO READER / NO SCORING / NO OUTPUTS
```

No Evidence candidate bytes were rewritten. No replacement. No extra fixture.

---

## 1. Frozen Evidence set (exact hashes)

Official confirmatory manifest: `docs/research/cont_e0t_v2/EVIDENCE_MANIFEST.json`

PILOT `fixtures/manifest.json` `EVIDENCE` remains `[]` (PILOT validator fail-closes otherwise). That is not an empty confirmatory set.

| Slot | Fixture id | Family | SHA-256 |
|------|------------|--------|---------|
| EVID-01 | CONT-E0T-EVID-01 | FAM-HOLD-CLASS | `72585647e0edcacbd03bd42d7ad49f406a7ef0e9201fb5b444e3cedf23380227` |
| EVID-02 | CONT-E0T-EVID-02 | FAM-MEMBER-CHANNEL | `f41976dc3c7e8bf20d926e84e04e89789312055dd7b2e117be1fbe3251bab1c6` |
| EVID-03 | CONT-E0T-EVID-03 | FAM-HOLD-CLASS | `e2d1416938bd3016929e4c12cfd9c51b1d3d7f7c93ec1e3091361d6adf8d1621` |
| EVID-04 | CONT-E0T-EVID-04 | FAM-MEMBER-CHANNEL | `bf49323db90a21ad7884ba20564f0506f9a274348c8414f7344e17fc6042c8f0` |

File bytes match the RedTeam-reviewed sealed copies. `partition` *inside* each JSON stays `EVIDENCE_CANDIDATE_UNSEALED` so the hash does not move.

---

## 2. Immutable protocol map

| Item | Pin |
|------|-----|
| Fields 1–4 | commit `fa61b22f7e898159d708e0ac0d768fdf76eced22` · file SHA `7151bb0c5aea664bc4d2290cf775e054a6426a17be9bcbb0465f3077daf5c804` (`CONT_E0T_FIELDS_1_4_RUN_INTEGRITY.md`) |
| Fields 6–10 | commit `305eb4f8e520702ffc5d1425299d5a75438e60e2` · file SHA `d8ca7896ab40341b3d1f6e46f111212a0f7b7d8b02a7d39d853055f22bc43b5e` (`CONT_E0T_PRE_EVIDENCE_RULES.md`) |
| Field 5 contract | commit `4222cee0a46a95be9af7c0256c522903992b6d42` · file SHA `3158c53ca98d250df4d8a3036adbd2bbcbbd294a6853a52cd410358182a33c8e` |
| Field 5 source reconciliation | commit `4222cee0a46a95be9af7c0256c522903992b6d42` · file SHA `23574d1c602639f77a7f0a3c4f178c4bf02e659ca268529e7c8de8c64c2ed6e1` |
| Run-order | SHA-256 `4ed48f6c793d1fc0fa1f6ae0311f541ef4422dfdd0c81fcadf81a41f2cbf82bd` |
| Reader prompt | SHA-256 `966400916b79e7025ed22c325e7d858e08ff2e89c0cc024606d7eb429878a349` |
| Decision rule | Field 1 in the Fields 1–4 pin: `B_SUPPORTED_BOUNDED` iff 4 complete ∧ `S≥3` ∧ `I=0` |
| Rubric | Field 6 in the 6–10 pin |

Changing any scientific rule after this freeze invalidates the affected preregistered run.

---

## 3. Reviewer roster (filled)

These are **Grok Bot agents**, not humans. Isolation is **procedural** (separate chats, blinded materials, no packages / arm labels / permutation). This is **not** hard physical independence.

| Role | Identity | Isolation |
|------|----------|-----------|
| Scorer-A | CONT-SCORER-A `c8a8b7ad-2533-405f-bc7f-3e828cee1466` | Arm-blind; no Scorer-B; no permutation |
| Scorer-B | CONT-SCORER-B `5f3fc376-abb1-4f21-b78d-2b2eaf7d5ff7` | Arm-blind; no Scorer-A; no permutation |
| Adjudicator | CONT-ADJUDICATOR `7c9f1d4a-e8f4-4ea5-9076-b5cae8e26b28` | Arm-blind until scoring lock |
| Builder / Integrity (X/Y permutation holder) | CONT-INTEGRITY `50310e45-f60c-4c7a-aa24-c4ea66a08727` | Does not score confirmatory rows |

Labs / CONT-AUTHOR / CONT-REDTEAM are **not** scorers (construction or prior unblind).

`ROSTER_PERSONS_UNFILLED` is **cleared**.

---

## 4. Interpretation lock (before any output)

**A. Claim B** is practical utilization / representation benefit of the *same* competent current state plus a bounded genuine trajectory, for the frozen replaceable reader (`deepseek-flash` / DeepSeek-V4.1-Flash).

It is **not**: semantic necessity of history; proof of event sourcing; proof that trajectory is universally required; proof that no better T1 exists.

**B. R1** remains documented: trajectory recency/path salience may be one mechanism of any observed T2 benefit. Permitted under Claim B. A T2 win must **not** later be reinterpreted as proof that temporal order itself, rather than the complete T2 package, caused the gain.

**C.** `PRIMARY_PASS` requires the frozen `must_compose` relations. The experiment measures frozen resume adequacy including reconstruction/justification completeness, not merely the binary May/No action.

---

## 5. Integrity checklist (this pass)

| Check | Result |
|-------|--------|
| Evidence manifest has exactly 4 frozen hashes | YES (`EVIDENCE_MANIFEST.json`) |
| Candidate bytes unchanged vs RedTeam | YES (re-hashed) |
| Field 5 prompt unchanged | YES `96640091…878a349` |
| Reader contract unchanged since 4222cee | YES `3158c53c…a33c8e` |
| Run-order unchanged | YES `4ed48f6c…f82bd` |
| Decision rule unchanged | YES (Fields 1–4 pin) |
| Rubric unchanged | YES (Fields 6–10 pin) |
| DeepSeek completions / fixture calls this freeze | **NONE** |
| Model outputs exist | **NONE** |
| Reviewer roster filled | YES (agents above) |
| Mutable-alias limitation explicit | YES: `SNAPSHOT_PINNED=NO`, `ALIAS_MUTABLE=YES` |

---

## Ten-field status

All ten are **protocol-frozen** as the pins above. Still **0 / 10 science-complete** in the sense that no confirmatory outputs exist.

```text
READY_FOR_OWNER_GO           = YES
EXPERIMENT_AUTHORIZATION     = NOT_AUTHORIZED
SNAPSHOT_PINNED              = NO
ALIAS_MUTABLE                = YES
```

STOP. No reader. No scoring. No merge. No PR.
