# Experiment 0 — Correspondence / Association Law v0.2

> **HISTORICAL / SUPERSEDED.** This measurement law is retained for provenance and research history only. It is superseded by `E0_CORRESPONDENCE_LAW_V0_3.md` and must not be treated as the current correspondence law.

**Status:** superseded historical measurement law for Experiment 0 Capture evaluation.  
**Implementation identifier:** `e0-correspondence-v0.2`  
**Fixture strategy key:** `deterministic_semantic_fields`

This document specifies how an actual captured-state item may be associated with a human-reference item before mismatch classification. Association is part of the measurement law. It is not retrieval, architecture, or authorization.

## Core rule

`item_id` is a signal, not proof of semantic correspondence.

An association is eligible only when:

1. `kind` is equal;
2. populated `origin` values do not conflict;
3. populated `authority` values do not conflict;
4. distinct symbolic/enum-like `value` constants do not conflict;
5. at least one semantic anchor overlaps across `entity`, `value`, `scope`, or `condition`.

Therefore **same kind alone is insufficient**, and an exact `item_id` cannot bypass semantic/provenance incompatibility.

## Unicode normalization

Normalization uses Unicode NFKC + case-folding and retains Unicode alphanumeric characters plus `€` before tokenization.

The measurement law must not erase Cyrillic or other non-ASCII semantic anchors merely because they are not `[a-z0-9]`.

## Ranking

Only eligible candidates are scored.

Signals include:

- same kind — required base signal;
- exact `item_id` — additional signal only;
- matching origin / authority;
- matching lifecycle status;
- token overlap in value, entity, scope, and condition.

The minimum score is `5`; because kind contributes `4`, at least one additional semantic signal is necessary.

## Ambiguity

If two or more eligible candidates share the same highest score, the evaluator does **not** break the tie by list position or index.

The reference item remains `MISSED`, and the unmatched actual items remain available to be reported as `FABRICATED`.

This is intentionally conservative: ambiguity is evidence that deterministic correspondence was not established.

## Fixture contract

Capture fixtures declare:

```json
{"match_spec":{"strategy":"deterministic_semantic_fields"}}
```

The evaluator must consume and validate that field. An unknown strategy fails evaluation rather than silently falling back to another association law.

## Result provenance

Every Capture evaluation result produced under this law must include:

```json
{
  "measurement_law_version": "e0-correspondence-v0.2",
  "match_strategy": "deterministic_semantic_fields"
}
```

This makes measurement-law changes observable in stored results.

## Non-goals

This law does not define or change:

- Gold / Oracle semantics;
- human approval;
- HARD FAIL classes or trigger predicates;
- Evidence disposition;
- Pilot or Evidence authorization;
- production matching/retrieval architecture.

`Association ≠ semantic correctness · item_id ≠ correspondence proof · green tests ≠ scientific validity.`
