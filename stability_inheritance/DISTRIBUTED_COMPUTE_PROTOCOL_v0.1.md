# Stability Inheritance Distributed Compute Protocol v0.1

**Date:** 2026-10-01  
**Governance:** SymC General Operations Manual v1.0 + mandatory Continuity Hardening Addendum  
**Scope:** execution orchestration only  
**Scientific authority:** unchanged  
**Status:** ACTIVE INFRASTRUCTURE BASELINE

## Purpose

Long Stability Inheritance calculations may run concurrently across local computers, GitHub-hosted runners, and Kaggle only when execution identity remains unambiguous.

Parallelism is an execution optimization. It does not create scientific authority, relax frozen designs, convert exploratory work into confirmation, or permit duplicate evidence inflation.

The controlling rule is:

> More simultaneous computation is allowed only when every active task has a unique scientific identity, execution slot, checkpoint lineage, output namespace, and stopping condition.

## Compute pools

### Local machines

Local computers are preferred for jobs that require:
- large persistent source trees already present locally;
- exact checkpoint/resume continuity across many hours or days;
- software environments difficult to reconstruct remotely;
- source-local datasets that should not be retransferred.

Each physical machine has two conceptual slots:
- **HEAVY:** one memory-intensive or long checkpointed calculation;
- **LIGHT:** one low-memory auxiliary calculation, permitted only when live resource headroom is adequate.

A LIGHT slot may not be filled merely because CPU cores are idle. Memory pressure and pagefile pressure are first-class resource limits.

### GitHub-hosted runners

GitHub-hosted standard Linux runners are used for:
- clean-room reproducibility;
- source-locked computations with checked-in inputs or reproducible acquisition;
- independent numerical qualification;
- bounded segments of longer checkpointable jobs.

Default distributed SI allocation is two simultaneous GitHub-hosted slots.

A single GitHub-hosted segment must stop by 300 minutes of scientific execution, leaving margin below the platform job ceiling for checkpoint serialization, artifact upload, and continuity persistence.

A >300-minute scientific task may use consecutive GitHub segments only when the native method supports an exact scientifically neutral resume. Segmentation may not:
- change random seeds except where the frozen design explicitly defines continuation seeds;
- restart warmup/burn-in as new evidence;
- thin data;
- change precision;
- alter solver/tolerance/model;
- silently merge independent chains into one chain;
- discard failed segments.

If exact resume is unavailable, the task must be routed to a longer-lived pool instead.

### Kaggle

Kaggle is reserved primarily for:
- memory-heavy jobs that exceed local headroom;
- CPU/GPU jobs that can complete within one notebook execution window;
- isolated reproducible calculations with explicit input/output manifests.

Kaggle remains disabled until authentication is configured.

Kaggle output must be copied into the canonical SI evidence lineage with source, notebook/version, output, and checksum identity before it counts as a durable checkpoint.

## Resource admission classes

Each task must declare one of:

- `LIGHT`: expected peak working memory <= 512 MB and modest CPU;
- `MEDIUM`: expected peak memory <= 4 GB;
- `HEAVY`: expected peak memory > 4 GB or sustained high CPU;
- `HEAVY_CHECKPOINTED`: long-running heavy computation with a validated exact-resume state;
- `GPU`: GPU-native computation only; never request GPU merely for availability.

Local admission defaults:
- HEAVY requires >= 2.5 GB available physical RAM before launch;
- LIGHT requires >= 1.2 GB available physical RAM;
- no new local job launches if committed-memory pressure is >= 85%;
- resource thresholds may stop launch but may not simplify the science.

## Required task identity

Every distributed task must have:

1. `task_id`;
2. scientific lane;
3. evidence class;
4. protocol or source-locked question;
5. code path and code/ref identity;
6. source/input identity;
7. executor pool;
8. resource class;
9. unique output directory;
10. unique checkpoint directory when applicable;
11. frozen stop condition;
12. next already-authorized action;
13. duplication identity sufficient to suppress identical work.

No two active tasks may share an output or checkpoint directory.

## Required execution states

- `PLANNED`
- `READY`
- `ACTIVE_COMPUTE`
- `ADVANCED_CHECKPOINT`
- `COMPLETE`
- `MECHANICAL_BLOCK`
- `SCIENTIFIC_GATE`
- `RESOURCE_HOLD`
- `USER_ACTION_REQUIRED`

`IDLE` is not used for authorized unfinished work.

## Launch rule

A task may launch only when:
- its scientific design is already authorized;
- its task identity is complete;
- its executor is compatible with the resource class;
- no identical scientific input/configuration identity is already active or complete;
- its output and checkpoint namespaces are unique;
- the destination slot passes resource admission.

The scheduler may choose **where** an already-authorized task runs. It may not choose **what scientific task** should exist.

## Checkpoint and heartbeat rule

Every long task must persist:
- start manifest;
- latest valid checkpoint identity;
- last substantive advancement timestamp;
- process/run identity;
- output identity;
- completion/block disposition.

Heartbeat-only activity never resets the scientific liveness clock.

For local processes, process existence alone is not scientific advancement. For GitHub and Kaggle, workflow/session activity alone is not scientific advancement.

## Completion and failure rule

At completion, persist the exact result and checksum before releasing the slot.

At failure:
1. preserve the failure;
2. classify infrastructure/implementation/resource/model/data/scientific cause;
3. inspect whether it is isolated, reproducible, or systematic;
4. resume the newest valid checkpoint if the scientific chain is unchanged;
5. stop at a scientific gate if recovery would change the scientific design.

## Cross-pool duplication firewall

The same task must never be launched on Victus, Popstop, GitHub, and Kaggle merely to make it finish sooner unless the frozen design explicitly defines independent replicas.

Redundant execution for reproducibility must be labeled as a replica and counted according to evidence-family rules. It is not automatic independent evidence.

## Monitoring policy

The distributed registry is the authoritative execution map.

Routine monitoring should be event/condition driven rather than conversational polling. Human attention is required only when:
- a task completes;
- a task blocks or fails;
- a checkpoint becomes stale beyond the continuity threshold;
- a resource hold prevents an already-authorized launch;
- a scientific gate is reached;
- a user action is required.

No repeated status checking is scientifically useful when state has not changed.

## Current platform ceilings

- GitHub-hosted standard jobs: use <= 300 minutes scientific runtime per segment.
- Local long jobs: may exceed 10 hours when checkpointed and thermally/resource stable.
- Kaggle: reserve end-of-session time for persistence; target <= 11 hours of scientific execution per notebook run.
- Self-hosted GitHub runners are not activated in this public repository baseline because they require a separate security review.

## Interpretation ceiling

This protocol changes execution topology only.

It does not alter (chi), (Chi), (Chi_{\rm arc}), evidence classes, native-model comparators, novelty gates, frozen thresholds, or promotion rules.
