# Experiment 0 — Correspondence / Association Law v0.3

**Status:** proposed bounded measurement-law remediation for Experiment 0 Capture evaluation.  
**Implementation identifier:** `e0-correspondence-v0.3`  
**Fixture strategy key:** `deterministic_semantic_fields`

This document supersedes v0.2 for Capture association. It changes only the assignment law after pair eligibility/scoring; it does not change Gold / Oracle semantics, human approval, HARD FAIL semantics, Pilot authorization, Evidence authorization, or production architecture.

## Core eligibility rule

`item_id` is a signal, not proof of semantic correspondence.

A Gold/Actual pair is eligible only when:

1. `kind` is equal;
2. populated `origin` values do not conflict;
3. populated `authority` values do not conflict;
4. distinct symbolic/enum-like `value` constants do not conflict;
5. at least one semantic anchor overlaps across `entity`, `value`, `scope`, or `condition`;
6. the resulting pair score is at least `5`.

The v0.2 Unicode normalization and pair-scoring signals remain unchanged.

## Global one-to-one assignment

Association is solved over the complete eligible Gold × Actual graph, not greedily in list order.

The objective is lexicographic:

1. maximize the number of eligible one-to-one associations;
2. among maximum-cardinality assignments, maximize total semantic score.

This objective is part of the measurement law. It prevents an early Gold item from consuming an Actual item that is required for a globally better correspondence.

## Global ambiguity / fail-closed rule

An individual Gold → Actual pair is accepted only when that pair is present in **every** globally optimal assignment under the objective above.

Operationally, a candidate pair is forced when removing that pair makes the global optimum strictly worse. If another assignment with the same maximum cardinality and total score remains possible, the pair is ambiguous and is not accepted.

Consequences:

- Gold list order cannot decide correspondence;
- Actual list order cannot decide correspondence;
- a unique globally optimal assignment is fully accepted;
- pairs common to all globally optimal assignments may be accepted even when other parts of the graph remain ambiguous;
- ambiguous Gold items remain `MISSED`;
- Actual items not belonging to accepted forced pairs remain `FABRICATED` for evaluator accounting.

This is intentionally conservative. Global ambiguity is evidence that deterministic correspondence was not established.

## Required permutation invariant

For identical item contents, any permutation of Gold items and/or Actual items must preserve semantic evaluation after results are keyed by stable item identifiers.

A regression test must cover the former greedy failure shape where:

```text
          A1   A2
G1        13   10
G2        13   —
```

The globally optimal correspondence is `G1 → A2` and `G2 → A1` (cardinality 2, score 23), regardless of Gold or Actual ordering.

## Fixture contract

Capture fixtures continue to declare:

```json
{"match_spec":{"strategy":"deterministic_semantic_fields"}}
```

The strategy key is retained because v0.3 is a versioned refinement of the same bounded semantic-fields strategy. The exact measurement-law version is emitted separately.

## Result provenance

Every Capture evaluation result produced under this law must include:

```json
{
  "measurement_law_version": "e0-correspondence-v0.3",
  "match_strategy": "deterministic_semantic_fields"
}
```

## Non-goals

This law does not define or change:

- Capture Gold content;
- Transfer Oracle content;
- human semantic approval;
- HARD FAIL classes or trigger predicates;
- Evidence disposition;
- Pilot or Evidence authorization;
- production matching/retrieval architecture.

`Association ≠ semantic correctness · assignment ≠ authorization · green tests ≠ scientific validity.`
