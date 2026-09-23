# Off-Main Branch Lifecycle Registry

> **Status:** NON-CANONICAL HYGIENE INDEX  
> **Snapshot date:** 2026-09-23  
> **Audit comparison baseline:** `main@78a73edf02cfa7e91fe6745b0f925fd5e0e05bc5`  
> **Coverage:** all 46 off-main branches visible during the audit/remediation snapshot before PR #59 merged.  
> **Post-remediation state:** PR #59 merged to `main@90ec316335184077869dcfb65b8a3af3248ad60c`; PR #60 then merged to `main@e53971609fb54a025ad2cc924acd4a79e2e9f018`. Both remediation branches were auto-deleted after merge.  
> **Current branch count after both merges:** 44 off-main branches remain.  
> **PR #60 provenance:** its remediation branch was rebuilt directly on merged #59 before final CI, so the final checks validated the combined #59 + #60 tree.

## Boundary

This registry is descriptive hygiene metadata only.

- branch != Canon
- branch != Evidence
- branch != adopted architecture
- branch != runtime authorization
- ahead-of-main != merge recommendation
- diverged != obsolete
- fully absorbed != automatic deletion authorization

Deletion, merge, promotion, or canonicalization still require the relevant project gate.

## Audit remediation branches

These branches were created by the 2026-09-23 bounded audit remediation. Both are complete and no longer exist as live branch refs.

| Branch | PR | Lifecycle |
| --- | ---: | --- |
| `fix/pilot-authority-contract-completion-20260923` | #59 | MERGED — branch auto-deleted after merge |
| `chore/hygiene-audit-followup-20260923` | #60 | MERGED — branch auto-deleted after merge |

## Fully absorbed by `main`

Re-compared on 2026-09-23. Each has `ahead_by = 0`, so no branch-only commit needs preservation for content completeness.

They are **safe-delete candidates after final owner/tooling safety check**, not automatic deletion authorizations.

| Branch | Ahead | Behind | Classification |
| --- | ---: | ---: | --- |
| `docs/human-ai-machine-architecture-v1` | 0 | 213 | FULLY_ABSORBED_BY_MAIN |
| `docs/state-reconcile-after-e0-v0-3` | 0 | 125 | FULLY_ABSORBED_BY_MAIN |
| `fix/e0-matcher-assignment-v0-3` | 0 | 130 | FULLY_ABSORBED_BY_MAIN |
| `fix/f01-state-control-plane` | 0 | 201 | FULLY_ABSORBED_BY_MAIN |
| `research/experiment-0-foundation` | 0 | 222 | FULLY_ABSORBED_BY_MAIN |

## Diverged historical branches

These 26 branches contain commits not present on `main` **and** are behind `main`. Branch age/name is not sufficient evidence to decide whether the unique commits are obsolete, superseded, or intentionally historical.

Until separately reconciled, classify them as `UNTRIAGED_DIVERGED_HISTORY`.

| Branch | Ahead | Behind | Classification |
| --- | ---: | ---: | --- |
| `agent/cognitive-os-relations` | 1 | 142 | UNTRIAGED_DIVERGED_HISTORY |
| `approval/issue-9-human-reference-v0.2` | 1 | 123 | UNTRIAGED_DIVERGED_HISTORY |
| `chore/governance-ci-hardening-20260829` | 5 | 55 | UNTRIAGED_DIVERGED_HISTORY |
| `chore/reconcile-pilot-preparation-state-20260824` | 3 | 61 | UNTRIAGED_DIVERGED_HISTORY |
| `claude/documentation-analysis-owkx58` | 1 | 110 | UNTRIAGED_DIVERGED_HISTORY |
| `claude/velantrim-continuum-pr1-audit-w1f06n` | 1 | 217 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/cognitive-ai-research-map-2026-08-22` | 1 | 111 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/documentation-architecture-v1` | 5 | 142 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/eiti-current-research-transfer` | 1 | 124 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/openclaw-continuity-candidate-v0.1` | 1 | 61 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/smart-context-handoff-bridge-v0-1` | 2 | 112 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/smart-context-handoff-mapping` | 1 | 112 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/smart-context-index-sync` | 1 | 111 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/substrate-neutral-projection` | 1 | 61 | UNTRIAGED_DIVERGED_HISTORY |
| `docs/truth-cleanup-20260829` | 4 | 54 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-correspondence-law-v02` | 4 | 140 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-current-tree-identity-binding` | 5 | 135 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-evidence-lock-path-containment` | 2 | 138 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-hard-fail-law-v02` | 4 | 139 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-json-schema-enforcement` | 4 | 137 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-reference-approval-conformance` | 9 | 142 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-review-protocol-binding` | 4 | 136 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-review-tree-binding` | 11 | 141 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-schema-contract-alignment-20260829` | 5 | 54 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/e0-transfer-representation-order-20260829` | 6 | 54 | UNTRIAGED_DIVERGED_HISTORY |
| `fix/pilot-instrumentation-hygiene-20260829` | 4 | 53 | UNTRIAGED_DIVERGED_HISTORY |

## Unique-ahead research branches

At the audit baseline above, these 13 branches had unique commits with `behind_by = 0`. After PR #59 advanced `main`, their live ahead/behind relation may mechanically become diverged; the table preserves the bounded audit snapshot rather than pretending to be a continuously refreshed authority surface.

Their lifecycle is intentionally **not inferred** from branch names. Until a durable decision says otherwise, treat them as `UNTRIAGED_RESEARCH_LINEAGE`, except where an explicit durable state is already known.

| Branch | Ahead | Behind | Current lifecycle note |
| --- | ---: | ---: | --- |
| `research/cont-e0t-integrity` | 1 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-prereg-author` | 1 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-prereg-reconciliation` | 2 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-prereg-v2` | 2 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-prereg-v22` | 14 | 0 | FROZEN PREREG INPUT / unique off-main history; no merge inference |
| `research/cont-e0t-redteam` | 2 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-v21-integrity-delta` | 3 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-v21-reconciliation` | 3 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-v21-redteam-delta` | 3 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-v22-cand-redteam` | 5 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-v22-cand-redteam-idorder` | 7 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/cont-e0t-v22-cand-redteam-s1` | 6 | 0 | UNTRIAGED_RESEARCH_LINEAGE |
| `research/e0b-capture-input-20260923` | 1 | 0 | OPEN DRAFT PR #58; cross-project input; NOT CANON / NOT MERGE-AUTHORIZED |

## CONT-E0T reproducibility boundary

Closed Issue #57 records a reported completed CONT-E0T run whose original raw reproducibility package was not recovered from checked durable surfaces.

The durable boundary remains:

- run reported complete / result recorded;
- raw run evidence not recovered from checked durable surfaces;
- scoring reproducibility not attempted from originals;
- reproducibility package not sealed;
- Claim B support underdetermined;
- no rerun or reconstruction implied by this registry.

Therefore unique CONT-E0T branches must not be collapsed into `main`, deleted as “obsolete”, or promoted as Evidence merely because later lineage exists.

## Open research issue

Issue #38 remains `STILL_NEEDED / DEFERRED` after 2026-09-23 hygiene triage. No durable result or concrete successor artifact was found that proves the exact plain-vs-hash-bound successor-handoff comparison was completed or superseded.

## Maintenance rule

When an off-main branch receives a durable lifecycle decision, record one of:

- `ACTIVE`
- `FROZEN`
- `SUPERSEDED_BY:<ref>`
- `HISTORICAL_KEEP`
- `FULLY_ABSORBED_BY_MAIN`
- `DELETE_APPROVED`

Do not infer lifecycle from age, branch name, lack of an open PR, or ahead/behind counts alone.
