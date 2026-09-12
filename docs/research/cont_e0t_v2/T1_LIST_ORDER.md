# T1 list order (discriminator fixtures)

**Status:** frozen as protocol rule for Claim-B discriminator candidates, before any reader execution.  
**Not:** experiment authorization. Not Evidence.

```text
T1 LIST ORDER IS NON-TEMPORAL AND NON-SEMANTIC.
```

For every list-valued `CURRENT_SEMANTICS` field on CONT-T1 in a discriminator fixture:

- serialize in **deterministic canonical order**;
- canonical key = stable `id` ascending (Unicode code-point / UTF-8 byte order);
- do **not** preserve insertion, transition, or chronological order;
- do **not** hand-shuffle until a secondary gold disappears;
- do **not** use random order unless a later revision freezes a seed and procedure.

`thin_trajectory` (and only that object in the Claim B reader T2 package) carries temporal order.

CAND-03 is serialized under this rule.  
CAND-04 bytes are **frozen this pass** (already PASS); do not rewrite it here. A later pass may re-serialize CAND-04 under the same rule without changing probes.
