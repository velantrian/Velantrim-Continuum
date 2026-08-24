# Continuum — Substrate-Neutral Projection

**Status:** Documentation-only research projection. Not Pilot authorization, Evidence Lock, E0 evidence, architecture freeze, or production runtime authorization.

Continuum asks what durable process state must survive replaceable inference/context instances so that long-horizon work can continue without pretending that missing state is known.

Its durable meaning is not a particular JSON file, database, model, agent framework, programming language, or storage engine.

For a declared scope, preserve distinctions such as:

```text
process state != one model/context instance
checkpoint != proof of correctness
resume attempt != successful continuation
unknown != false
missing != resolved
partial continuation != complete continuation
state transport != authority transfer
successful mechanism != scientific validation
scientific evidence != production authorization
```

A future implementation may use a radically different persistence or inference substrate. It remains compatible only where required continuity state, uncertainty, ownership/authority, revision lineage, and declared loss remain representable and testable.

Cross-project orientation and conformance checklist live in `velantrian/velantrim`; owning Continuum research documents remain authoritative for Continuum-specific semantics.
