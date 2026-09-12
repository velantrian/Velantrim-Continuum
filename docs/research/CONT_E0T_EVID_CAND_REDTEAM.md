# CONT-E0T Evidence-candidate RedTeam

**Role:** CONT-REDTEAM (blind independent attacker)  
**Authorization:** one bounded Evidence-candidate review. **Not** experiment GO.  
**Sealed bytes only.** Author worktree / branch / artifact / chat / reasoning not read.  
**No** model / reader / DeepSeek call. **No** Author-file edit. **No** replacement pool.

Protocol (read-only): commit `fa61b22f7e898159d708e0ac0d768fdf76eced22`  
`CONT_E0T_FIELDS_1_4_RUN_INTEGRITY.md`, `CONT_E0T_PRE_EVIDENCE_RULES.md`, `CONT_E0T_FIELD5_READER_CONTRACT.md`, `T1_LIST_ORDER.md`.

```text
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
EVIDENCE                 = []
FINAL_PREREG_REVIEW      = NOT_READY
NO READER / NO MODEL
```

---

## Verdicts (exact)

| Fixture | SHA-256 (verified) | Family | Verdict |
|---------|--------------------|--------|---------|
| EVID-01 | `72585647e0edcacbd03bd42d7ad49f406a7ef0e9201fb5b444e3cedf23380227` | FAM-HOLD-CLASS | **PASS** |
| EVID-02 | `f41976dc3c7e8bf20d926e84e04e89789312055dd7b2e117be1fbe3251bab1c6` | FAM-MEMBER-CHANNEL | **PASS** |
| EVID-03 | `e2d1416938bd3016929e4c12cfd9c51b1d3d7f7c93ec1e3091361d6adf8d1621` | FAM-HOLD-CLASS | **PASS** |
| EVID-04 | `bf49323db90a21ad7884ba20564f0506f9a274348c8414f7344e17fc6042c8f0` | FAM-MEMBER-CHANNEL | **PASS** |

```text
EVID-01 PASS
EVID-02 PASS
EVID-03 PASS
EVID-04 PASS
```

`CORRECT_BEFORE_EVIDENCE` was not used: T1 already determines PRIMARY (required by Field 3 / E4.9 / construction rule 3). That is test (1) holding, not a ceiling or restatement fail. `BLOCKING` was not used: no bar below fails closed.

---

## Bar index (all four)

| # | Test | E1 | E2 | E3 | E4 | Class |
|---|------|----|----|----|----|-------|
| 1 | PRIMARY semantically solvable from T1 alone | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |
| 2 | T1 not impoverished | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |
| 3 | no direct/semantic answer leakage | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |
| 4 | no temporal leakage via IDs / list position | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |
| 5 | thin does not restate current/gold | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |
| 6 | trajectory is path/time only | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |
| 7 | no unique shortcut faking ≥4-way compose | PASS | PASS | PASS | PASS | INFERENCE |
| 8 | UNKNOWN + precedence genuinely required | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |
| 9 | not trivial ceiling | PASS | PASS | PASS | PASS | INFERENCE |
| 10 | E4.1–E4.10 | PASS | PASS | PASS | PASS | SOURCE-SUPPORTED |

---

## Independent T1 solves (test 1)

Done from `current_semantics` + probe wording only. Trajectory / gold / `t1_solvability_proof` were not required.

**EVID-01.** Pack → vendor workspace (`d-inv`); workspace via Slack (`c-via-slack`); Slack is outbound (`c-slack-out`); HOLD-kelp on outbound (`c-hold-kelp`); class hold outranks member permission (`c-prec`) so `c-fin-ok` does not win; kelp clearance UNKNOWN (`u-kelp`). **No.**

**EVID-02.** Runbook (`d-book`); public docs site is a published surface (`c-docs-pub`); published surfaces are public (`c-class-pub`); HOLD-nori on public (`c-hold-nori`); `c-prec` so `c-docs-ok` does not win; nori clearance UNKNOWN (`u-nori`). **No.**

**EVID-03.** Bulletin → field crew (`d-bull`); crew via SMS (`c-via-sms`); SMS is outbound (`c-sms-out`); HOLD-quartz on outbound (`c-hold-quartz`); `c-prec` so `c-sms-ok` does not win; quartz clearance UNKNOWN (`u-quartz`). **No.**

**EVID-04.** Outage note (`d-note`); ticket comment is a customer-visible thread (`c-tkt-ext`); those threads are external (`c-class-ext`); HOLD-cedar on external (`c-hold-cedar`); `c-prec` so `c-tkt-ok` does not win; cedar clearance UNKNOWN (`u-cedar`). **No.**

Every `must_compose` id is present on T1 with the cited text. Dummy trajectory holds (`c-hold-lichen` / `laver` / `pebble` / `alder`) are absent from T1, as required.

T1 lists are schema-complete (`id` + `text` + `current` on every list item; all four scalars present). Binding atoms are not withheld. Not impoverished.

---

## Leakage / time / thin (tests 3–6)

- Full gold sentence is not a substring of T1 JSON or of `thin_trajectory`.
- `current_rationale` / `process_position` do not state the May/No or the UNKNOWN resolution.
- Thin is `ID_REFS_ONLY`: `{seq, changes:[{op,field,id}]}` only; `op ∈ {ADD,SET,REMOVE}`; no `from`/`to`/gold prose.
- IDs do not encode time (false-positive: `c-hold-*` contains the letters `old`; not a clock).
- T1 lists are `CANONICAL_ID_ASC_NON_TEMPORAL`. Binding hold is not a last-item leak (E1 kelp 3/7; E2 nori 5/7; E3 quartz 2/7; E4 cedar 2/7).
- Titles name the binding hold; titles are not in the Field 5 reader object.

---

## E4.1–E4.10 (test 10)

| ID | Result |
|----|--------|
| E4.1 | One `current_semantics` object; reader T1/T2 would share it byte-identical |
| E4.2 | Keys = frozen CURRENT_SEMANTICS lists + four scalars; no smuggled trajectory / pad / provenance inside `current_semantics` |
| E4.3 | Schema-complete; not impoverished |
| E4.4 | Thin `ID_REFS_ONLY` |
| E4.5 | No current-answer text on thin |
| E4.6 | `provenance_validator_only` / `audit_snapshots_validator_only` are validator-only keys on the sealed object, not reader-package keys |
| E4.7 | Every T1 list id-asc |
| E4.8 | `n_transitions = 2`; last audit `to_state` equals current (order-normalized); no `envelope_pad` |
| E4.9 | All `must_compose` ids on T1; independent solve above |
| E4.10 | No SECONDARY probe |

`partition` is `EVIDENCE_CANDIDATE_UNSEALED`. `copied_from_cand_03_04` / `copied_from_e0t_transfer` are false. Objects are new scenarios (invoice/Slack, runbook/docs, bulletin/SMS, outage/ticket), not CAND-03/04 bytes.

---

## Compose / UNKNOWN / ceiling (tests 7–9)

Each gold binds ≥4 current relations including one precedence and one UNKNOWN. A decoy member permission quotes the probe action; distractor holds (fax/phone, intranet/newsletter, radio/pager, social/status-page) do not cover the asked channel. “Any UNKNOWN → No” or “first/middle hold” does not recover the gold *compose* (wrong `must_compose` ids ⇒ not `PRIMARY_PASS`).

Ceiling: the decoy is a Yes-trap, not a one-look No. Isolated Field 5 calls have no cross-fixture memory.

---

## Residuals (not gate-fail)

| ID | Note | Severity | Class |
|----|------|----------|-------|
| R1 | T2 seq2 uniquely ADDs the binding hold. Recency salience can aid T2 without adding PRIMARY facts. Protocol allows path/time on thin. | MINOR | INFERENCE |
| R2 | Among the three current holds, gold is the id-sorted middle on E1–E3 and the first on E4 (I7-class naming coincidence). Protocol forbids reading T1 order as time. | MINOR | INFERENCE |
| R3 | `d-*` content inventories and probe-named channels are weak compose members. Authorization still needs class / hold / precedence / UNKNOWN (≥4). | MINOR | INFERENCE |
| R4 | May/No is reachable from class-hold + UNKNOWN without *stating* precedence. `PRIMARY_PASS` still requires the gold compose, including `c-prec`. | MINOR | INFERENCE |
| R5 | Four objects share one stencil (Field 2: two families × two). Not a per-fixture bar fail. | MINOR | SOURCE-SUPPORTED |

R1 is a Claim B identifiability residue (salience ≠ history value). It does not fail a listed construction bar. Do not treat PASS as experiment GO or as `T2_SUPERIOR` predicted.

---

## Gate

```text
EVID-01 = PASS
EVID-02 = PASS
EVID-03 = PASS
EVID-04 = PASS
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
NO REPLACEMENT POOL
```

STOP. Docs-only. No model. No merge. No PR. No architecture.
