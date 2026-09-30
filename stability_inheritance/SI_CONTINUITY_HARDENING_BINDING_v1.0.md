# Stability Inheritance Continuity Hardening Binding v1.0

**Date:** 2026-09-29  
**Authority:** SymC General Operations Manual v1.0 + mandatory program-wide Continuity Hardening Addendum  
**Scope:** execution continuity only  
**Scientific authority:** unchanged

This binding applies the current program-wide continuity rules to the Stability Inheritance lane. It does not authorize new hypotheses, new scientific claims, outcome-driven retuning, holdout exposure, or autonomous reinterpretation.

## Canonical advancement

Progress counts only when the authoritative Stability Inheritance lane itself advances into durable canonical lineage. Monitoring, documentation-only churn, CI activity, controller activity, unrelated repository work, repeated polling, or repeated unchanged retries do not reset the SI liveness clock.

Each active SI lane must carry its own:
- execution state;
- checkpoint history;
- liveness clock;
- next exact authorized action;
- execution ceiling;
- scientific gate, external block, or user-action block when present.

## Permitted states

- `ACTIVE_COMPUTE`
- `ADVANCED_CHECKPOINT`
- `SCIENTIFIC_GATE`
- `EXTERNAL_BLOCK`
- `USER_ACTION_REQUIRED`

`IDLE` is not a valid state while authorized unfinished work remains.

`USER_ACTION_REQUIRED` is distinct from `SCIENTIFIC_GATE`. It is permitted only when a concrete external/manual action is required and must identify:
1. the blocked stage;
2. the exact reason;
3. the exact user action;
4. the resume checkpoint;
5. what will execute immediately after that action.

## Dual durable records

`stability_inheritance/CONTINUITY_STATE.json` and root `WORKING_INVESTIGATION.md` must agree on the active lane, current stage, latest valid checkpoint, stopping condition, and next authorized action.

If they conflict, repository science/protocol provenance and `WORKING_INVESTIGATION.md` govern until the machine-readable record is reconciled.

## Checkpoint identity and exact resume

A valid checkpoint must identify enough of the frozen chain to prove what actually ran, including relevant:
- source/input identities and hashes when available;
- protocol/config identity;
- code/ref identity;
- manifests or archive identities;
- result/output identity and hash;
- workflow/run/artifact identity;
- restart state.

Resume from the newest valid checkpoint in the same frozen scientific chain. Do not recompute completed valid work because a monitor, controller, conversation, runner, or polling layer failed.

## Duplicate suppression

A completed computation may be skipped as a duplicate only when the scientific input/configuration identity is demonstrably unchanged. Similar labels, timestamps, filenames, or task names are not sufficient proof.

## Protected evidence

Masked, sealed, holdout, embargoed, staged, or otherwise protected outcomes retain their original boundary during recovery. Mechanical recovery may inspect only metadata already permitted by the frozen protocol.

Resource exhaustion, runner limits, or transport problems do not authorize scientific simplification.

## False-liveness detection

The independent continuity sentinel must detect:
- controller failure;
- orphaned or stale runs;
- empty queues while authorized work remains;
- stale queue/run identifiers;
- queue entries still marked READY after valid completion;
- repeated identical retries;
- missing checkpoint persistence;
- monitoring without substantive execution;
- support activity that falsely resets SI liveness.

The default stagnation threshold is approximately 90 minutes without genuine SI advancement and without a documented legitimate stop.

Recovery may restore already-granted execution authority. It may not create scientific authority.

## Five-question durable-state test

At every substantive checkpoint, recovery, gate, or block, answer exactly:

1. **What scientific lane are we advancing?**
2. **What is actually running or what durable checkpoint was just completed?**
3. **What is the next already-authorized action?**
4. **What prevents that action from happening immediately, if anything?**
5. **Does crossing that boundary require mechanical execution or a new scientific decision?**

If these questions cannot be answered from durable state, continuity is not adequately specified.

## Current ERIES execution ceiling

Current lane: `ERIES_EUROPROTEAS_CROSS_SUBSTRATE`.

The active execution ceiling is:
1. preserve the completed metadata-only source qualification;
2. complete archive-layout qualification without opening member bodies or numeric responses;
3. automatically repair transport-only failures that leave the frozen archive-layout question unchanged;
4. persist the newest valid checkpoint and suppress duplicate reruns;
5. stop at `SCIENTIFIC_GATE` if construction of a matched hierarchy requires a new scientific correspondence/channel/test decision not already frozen.

No response scoring, chi admission, Chi admission, Chi_arc reconstruction, or cross-substrate scientific claim is authorized by this continuity binding.
