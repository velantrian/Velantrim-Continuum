# Claim B fixture candidates (not Evidence, not PILOT)

| ID | Status |
|----|--------|
| CONT-E0T-FX-B-CAND-01 | SUPERSEDED (ceiling / seq1 replay) |
| CONT-E0T-FX-B-CAND-02 | SUPERSEDED (ceiling / list-order leak) |
| CONT-E0T-FX-B-CAND-03 | ACTIVE; T1 lists CANONICAL_ID_ASC; PRIMARY unchanged |
| CONT-E0T-FX-B-CAND-04 | ACCEPTED viable candidate; not Evidence |

- Not in `fixtures/manifest.json`
- `partition: CANDIDATE_NOT_EVIDENCE`
- `thin_trajectory_form: ID_REFS_ONLY` — no current-state `to` text
- Do **not** promote to Evidence

See `T1_LIST_ORDER.md`: T1 list order is non-temporal / non-semantic.

**Partition:** `DEVELOPMENT_DESIGN`. Do **not** promote CAND-03/CAND-04 to confirmatory Evidence. Future Evidence must be new objects after `CONT_E0T_PRE_EVIDENCE_RULES.md`.
