# OpenClaw Continuity Candidate v0.1

Status: EXPERIMENT CANDIDATE ONLY
Date: 2026-08-24

## Purpose

OpenClaw provides useful operational patterns for long-lived sessions and detached work, but Continuum treats them only as candidates to compare against simpler continuity hypotheses.

This document does not adopt them as Continuum truth, does not authorize OD-PILOT-01, Package A/B, Pilot, Evidence Lock, E0-C/E0-T, or production.

## Candidate mechanisms

The following may be represented as experimental variants:

- durable session/transcript ledger;
- prompt-only pruning that does not rewrite persisted history;
- compaction summary plus recent tail;
- pre-compaction durable memory flush;
- detached background-task ledger separate from scheduler;
- per-session writer ownership to prevent stale/superseded runs from committing;
- lifecycle hooks that record transitions without becoming authority.

## Critical negative lesson

OpenClaw gateway events are not inherently a replayable evidence log. Continuum MUST NOT equate transient event delivery with continuity proof.

`event observed != durable continuity evidence`

`summary persisted != original state preserved`

`session resumed != process continuity proven`

`task record != scheduler != permission`

## Proposed experiment mapping

Future E0-compatible candidates may compare:

A. minimal `state.json` baseline;
B. append-only event/session ledger;
C. full transcript/state transfer;
D. compacted summary + retained recent tail;
E. summary + explicit pre-compaction durable memory flush;
F. task-ledger + session-writer ownership metadata.

Any comparison must preserve the existing separation between capture failure and transfer failure.

## Required measurements

If these candidates become authorized experiments, measure at minimum:

- information retained/lost;
- declared vs undeclared loss;
- reproducibility/replayability;
- stale-writer collision behavior;
- transfer success independent of capture quality;
- ability to detect that continuity has failed rather than silently fabricate it;
- complexity cost relative to the `state.json` null hypothesis.

## Boundary

OpenClaw is an implementation specimen, not the answer to Continuum. A more complex mechanism wins only if experiments falsify the simpler alternative on the dimensions Continuum actually cares about.
