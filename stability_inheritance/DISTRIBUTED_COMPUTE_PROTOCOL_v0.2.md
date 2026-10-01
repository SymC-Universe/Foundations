# Stability Inheritance Distributed Compute Protocol v0.2

**Date:** 2026-10-01  
**Governance:** SymC General Operations Manual v1.1 + mandatory Continuity Hardening Addendum  
**Supersedes:** DISTRIBUTED_COMPUTE_PROTOCOL_v0.1.md  
**Scope:** execution orchestration only  
**Scientific authority:** unchanged  
**Status:** ACTIVE INFRASTRUCTURE BASELINE

## Purpose

Long Stability Inheritance calculations may run concurrently across Victus, Popstop, GitHub-hosted runners, and Kaggle only when execution identity remains unambiguous.

Parallelism is an execution optimization. It does not create scientific authority, relax frozen designs, convert exploratory work into confirmation, or permit duplicate-evidence inflation.

The controlling rule is:

> More simultaneous computation is allowed only when every active task has a unique scientific identity, execution slot, checkpoint lineage, output namespace, and stopping condition.

## Slot model

Each executor has named slots. A task occupies one slot, even if its runtime spawns several child processes.

- Victus: `VICTUS_HEAVY_1` and conditional `VICTUS_LIGHT_1`.
- Popstop: `POPSTOP_HEAVY_1` and conditional `POPSTOP_LIGHT_1`.
- GitHub: `GITHUB_HOSTED_A` through `GITHUB_HOSTED_D`.
- Kaggle: `KAGGLE_CPU_A`; GPU remains disabled unless the scientific task is GPU-native.

Two active tasks may never occupy the same slot. Two slots may never share the same active output/checkpoint namespace.

## Local machines

Each local machine may run one HEAVY task plus one LIGHT task when resource admission passes.

A LIGHT task is not admitted merely because CPU cores are idle. Available physical RAM and committed-memory pressure are first-class gates.

Current default admission:
- HEAVY launch requires >= 2.5 GB available physical RAM;
- LIGHT launch requires >= 1.2 GB available physical RAM;
- no new local launch when committed memory is >= 85%.

These thresholds prevent pagefile thrash. Resource limits may delay a launch but may never simplify or retune the science.

## GitHub-hosted runners

Use standard Linux runners for checked-in or reproducibly acquired computations.

Default SI allocation is **four simultaneous distinct GitHub task slots**.

A standard hosted job has a six-hour execution ceiling. SI scientific execution must therefore stop by 300 minutes per segment, reserving margin for checkpoint serialization, artifact upload, and continuity persistence. The 300-minute segment target is an infrastructure safety margin, not a universal scientific checkpoint cadence; task-level checkpoint/progress cadence remains workload-specific under GOM v1.1 Sections 27 and 31.

A task longer than one segment may continue only if the task has a scientifically neutral exact-resume checkpoint. Successor segments must preserve:
- model, solver, precision, tolerance, source/input identity, seed contract, and frozen configuration;
- exact checkpoint lineage;
- one task identity across segments.

A successor segment is continuation, not an independent replication.

If exact resume is unavailable, route the task to Kaggle or a local long-lived slot instead of restarting inside GitHub.

## Kaggle

Kaggle is the preferred external pool for memory-heavy jobs that fit within one notebook execution window.

Default CPU-lane planning envelope:
- 4 CPU cores;
- approximately 30 GB RAM;
- 12-hour platform session;
- target <= 11 hours scientific execution so checkpoint/output persistence completes before shutdown.

Kaggle remains dormant until a scientific task is actually assigned and authentication is configured. Lack of Kaggle authentication alone is not a continuity fault.

Every Kaggle output must return to the canonical SI lineage with:
- task ID;
- notebook/version identity;
- source/input hashes;
- output/checkpoint hashes;
- terminal disposition.

## Backend parity and execution-mode changes

Moving an already-defined task between local CPU, GitHub, Kaggle, GPU, alternate precision, alternate solver/runtime, MPI rank count, or another execution mode that could change numerical behavior requires representative production-equivalent parity qualification under GOM v1.1 Section 25.3 before decisive production use.

Executor choice may change logistics. It may not silently change the scientific method, precision, solver, stochastic contract, or result semantics. A parity check may be omitted only when the change is demonstrably transport-only and cannot alter the numerical object; the reason is recorded.

## Required task identity

Every task must record:
1. task ID;
2. scientific lane and evidence class;
3. protocol/frozen question;
4. code/ref identity;
5. source/input identity;
6. executor slot;
7. resource class;
8. unique output root;
9. unique checkpoint root;
10. frozen stop condition;
11. next already-authorized action;
12. duplicate-suppression identity.

The scheduler may choose **where** an already-authorized task runs. It may not choose **what science** exists.

## States

Allowed execution states:
- PLANNED
- READY
- ACTIVE_COMPUTE
- ADVANCED_CHECKPOINT
- COMPLETE
- MECHANICAL_BLOCK
- SCIENTIFIC_GATE
- RESOURCE_HOLD
- USER_ACTION_REQUIRED

IDLE is not a valid state for authorized unfinished work.

## Monitoring

The distributed registry is the authoritative execution map.

Monitoring is condition-driven, not conversational polling. One SI compute watcher is authoritative. Duplicate or stale SI watchers must remain disabled.

Human attention is requested only when:
- a task completes;
- a task fails or blocks;
- advancement is stale beyond the workload-specific progress expectation derived from pilot/provider/native behavior; use approximately 90 minutes only as a fallback when no better expectation exists;
- an expected checkpoint/output is missing;
- an authorized task is held by resources;
- a scientific gate or new user action is reached.

Healthy unchanged jobs produce no notification.

## Duplicate and evidence firewall

The same scientific task may not be launched simultaneously on multiple pools merely to finish sooner. Independent replicas require an explicit frozen replica design and remain subject to evidence-family accounting.

Multiple OS processes belonging to one sampler/task count as one scientific task.

## Failure handling

Every failure is preserved and classified as infrastructure, implementation, resource, data/provenance, numerical, model, or scientific behavior.

Mechanical recovery resumes the newest valid same-chain checkpoint. If recovery would change solver, threshold, model, source, feature definition, comparator, precision, or other frozen science, stop at SCIENTIFIC_GATE.

## Interpretation ceiling

This protocol changes execution topology only. It does not alter lowercase \(\chi\), capital \(\Chi\), \(\Chi_{\rm arc}\), evidence classes, native-model comparators, novelty gates, frozen thresholds, or promotion rules.
