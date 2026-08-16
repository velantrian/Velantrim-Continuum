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

## Required decisions

Record an `ACCEPT` plus a non-empty human note for every machine-keyed decision below:

| Decision ID | Meaning |
|---|---|
| `F1` | explicit restriction |
| `F2_PRE` | pre-clarification semantics |
| `F2_POST` | post-clarification semantics |
| `F3` | superseded + active rule |
| `F4` | rejected alternative / rationale |
| `F5` | caution / confirmation semantics |
| `F6` | `NO_APPROVAL_RULE_ADOPTED` |
| `F7` | temporal / confirmation gate |
| `F8` | contested claims remain contested |
| `T-PILOT-01` | pilot Transfer Oracle |
| `T-EVIDENCE-01` | held-out Oracle review only |
| `T-EVIDENCE-02` | held-out Oracle review only |
| `AUTHORITY_AMBIGUITY_PROVENANCE` | cross-cutting authority/provenance check |

`open_semantic_revisions` must be empty.

## Candidate → approved bindings

Approved files must be versioned copies outside `candidates/`:

- `experiments/e0/gold/approved/capture-gold.v0.1.json`
- `experiments/e0/oracle/approved/transfer-oracle.v0.1.json`

Historical candidate inputs must remain `AI_PROPOSED_DRAFT`.

Approval provenance record:

`experiments/e0/approval/human-reference-approval.v0.1.json`

The record must bind exact candidate and approved SHA-256 values and include the reviewed commit, canonical Issue #9 URL, reviewer identity/role, timestamp, all decisions, and:

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

Important: this machine result validates attestation structure and exact repository bindings. It **does not prove that a human actually performed the review**; the human act is a governance fact that must be explicitly recorded by the reviewer.

## Boundary

This PR must not:

- run a Pilot;
- create an Evidence Lock;
- set `EVIDENCE_READY`;
- authorize E0-C or E0-T Evidence;
- freeze production architecture;
- authorize runtime, event sourcing, or ecosystem integration.

After merge, the next permitted experimental action is a separate Pilot-only issue/PR using approved references and pilot fixtures, with all outputs labelled `PILOT — NOT EVIDENCE`.
