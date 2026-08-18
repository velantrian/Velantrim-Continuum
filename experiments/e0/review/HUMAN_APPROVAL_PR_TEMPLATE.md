# 👤 Human Gold / Oracle approval PR template

Use this only after the human reviewer has independently inspected the exact Issue #9 inputs and all review decisions are `ACCEPT`. This template does not itself constitute human approval.

## Human Review Attestation — Issue #9

- **Issue:** Closes #9
- **Review status:** `HUMAN_APPROVED`
- **Review scope:** Gold / Oracle approval for future `PILOT — NOT EVIDENCE` only
- **Reviewed repository commit:** `<40-character SHA>`
- **Reviewed at (UTC):** `<YYYY-MM-DDTHH:MM:SSZ>`
- **Human reviewer:** `<name>`
- **Reviewer role / authority:** `<role>`

The reviewer should state that they independently reviewed the exact candidate artifacts and fixture/scenario semantics and approve only the versioned artifacts and exact SHA-256 bindings in the PR.

## Required human decisions

Record an `ACCEPT` plus a non-empty human note for **each of the 14 canonical human review rows** below. Machine-only assertions must not be inserted into this namespace.

| Decision ID | Meaning |
|---|---|
| `F1` | explicit restriction |
| `F2_PRE` | pre-clarification semantics |
| `F2_POST` | post-clarification semantics |
| `F3` | superseded + active rule |
| `F4` | rejected alternative / rationale |
| `F5_PRE` | caution remains unresolved before clarification |
| `F5_POST` | post-clarification semantics, including variant-specific F5-E1/F5-E2 meaning |
| `F6` | `NO_APPROVAL_RULE_ADOPTED` |
| `F7` | temporal / confirmation gate |
| `F8_PRE` | contested source-attributed claims before clarification |
| `F8_POST` | clarification adds no adjudication; conflict remains contested |
| `T-PILOT-01` | pilot Transfer Oracle |
| `T-EVIDENCE-01` | held-out Oracle review only |
| `T-EVIDENCE-02` | held-out Oracle review only |

`open_semantic_revisions` must be empty.

> **Boundary:** machine assertions may independently deny package readiness/admissibility, but they must never rewrite, substitute, or impersonate one of the 14 human semantic decisions above.

## Candidate → approved bindings

Approved files must be versioned copies outside `candidates/`:

- `experiments/e0/gold/approved/capture-gold.v0.1.json`
- `experiments/e0/oracle/approved/transfer-oracle.v0.1.json`

Historical candidate inputs must remain `AI_PROPOSED_DRAFT`.

Approval provenance record:

`experiments/e0/approval/human-reference-approval.v0.1.json`

The record must bind exact candidate and approved SHA-256 values and include the reviewed commit, canonical Issue #9 URL, reviewer identity/role, timestamp, all 14 human decisions, and:

```json
"evidence_lock": {"status": "NOT_CREATED", "sha256": null}
```

## Verification

```text
python scripts/e0/validate_human_reference_approval.py \
  --repo-root . \
  --approval experiments/e0/approval/human-reference-approval.v0.1.json \
  --issue-number 9
```

Expected machine result after a legitimate approval PR has materialized all required artifacts:

`HUMAN_REFERENCE_APPROVAL_BINDINGS_VALID`

Important: this machine result validates attestation structure and exact repository bindings that the validator actually checks. It **does not prove that a human actually performed or understood the review**; the human act remains an external governance fact that must be explicitly recorded by the reviewer.

## Boundary

This PR must not:

- run a Pilot;
- create an Evidence Lock;
- set `EVIDENCE_READY`;
- authorize E0-C or E0-T Evidence;
- freeze production architecture;
- authorize runtime, event sourcing, or ecosystem integration.

After merge, the next permitted experimental action is **not selected by this template**. A separate owner-authorized Pilot-only step is still required before any pilot execution, and all pilot outputs must remain labelled `PILOT — NOT EVIDENCE`.
