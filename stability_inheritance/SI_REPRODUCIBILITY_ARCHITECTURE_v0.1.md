# Stability Inheritance Reproducibility Architecture v0.1

**Date:** 2026-09-30
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum
**Status:** PROGRAM SCAFFOLD / NO SCIENTIFIC PROMOTION
**Scope:** Stability Inheritance representation-qualification and inheritance-qualification lanes

## Purpose

Define the minimum durable evidence chain required for an SI result to be reproducible, auditable, restartable, and interpretable without depending on chat state.

This scaffold does not prescribe one estimator across domains. Domain-native models remain primary. It prescribes the provenance and adjudication structure around those models.

## Canonical evidence chain

Every substantive SI task should be reconstructible through the following chain:

\[
\text{source identity}
\rightarrow
\text{frozen question/protocol}
\rightarrow
\text{implementation identity}
\rightarrow
\text{execution identity}
\rightarrow
\text{raw result}
\rightarrow
\text{adjudicated disposition}
\rightarrow
\text{Function/Limit map}
\rightarrow
\text{claim ceiling}.
\]

No downstream item may silently overwrite an upstream item.

## 1. Source identity contract

Before outcome exposure, record as available:

- source name and native repository/archive identity;
- DOI / record ID / release tag / dataset version;
- exact file names;
- byte size;
- SHA-256 or authoritative upstream checksum;
- access date;
- source role: baseline, target, adversary, comparator, calibration, holdout;
- protected/sealed status;
- whether any source was previously inspected in an outcome-bearing way.

For large external files that should not live in GitHub, store the receipt and hash, not the data body.

### DESI example

The DESI SI lane binds:
- four baseline posterior chain SHA-256 identities;
- four base_mu_sigma posterior chain SHA-256 identities;
- official DESI release paths;
- local transport receipts;
- exact model-only coordinates excluded from the representation test.

## 2. Frozen protocol contract

Each protocol must state before scoring:

- scientific question;
- evidence class and promotion eligibility;
- admitted native representations;
- refused/not-yet-admitted project representations;
- features/coordinates and exclusions;
- train/test or source-level split rule;
- comparators and negative controls;
- decision rules;
- failure/indeterminate states;
- claim ceiling;
- explicit protected next stage.

Post-result repairs may fix implementation or transport only if the scientific design is unchanged and the repair is separately recorded.

## 3. Implementation identity contract

For every executed analyzer:

- canonical repository path;
- Git commit containing the executed implementation;
- SHA-256 of the exact local file used;
- language/runtime version;
- key dependency versions;
- deterministic seeds where randomness is used;
- exact command-line arguments;
- explicit statement of whether code differs from the frozen protocol.

If a remote-tool wrapper or serialization layer is used to transfer code, syntax verification is mandatory before execution.

## 4. Execution identity contract

Record:

- execution host;
- process/workflow/run ID;
- start and finish timestamps;
- source commit;
- environment identity when material;
- CPU/GPU distinction if material;
- active versus queued versus completed state;
- restart/checkpoint identity for long runs.

A monitoring process, workflow timer, or queued job is never reported as active scientific computation.

## 5. Raw-result preservation

Machine-readable output should be persisted before prose interpretation when feasible.

Minimum fields:

- protocol identifier;
- source identities;
- implementation identity;
- sample counts / effective sample sizes;
- primary metrics;
- fold/replicate metrics;
- all frozen decision diagnostics;
- warning/failure telemetry;
- raw disposition;
- output SHA-256.

If a result is numerically provisional, preserve it with that status rather than replacing it after repair.

## 6. Numerical-validity layer

Numerical validity is separate from scientific outcome.

Required checks may include:
- convergence;
- finite outputs;
- rank/conditioning diagnostics;
- exact/approximate implementation equivalence guards;
- sensitivity to source-chain/replicate split;
- solver termination status;
- memory/resource failure classification.

A numerical failure cannot authorize:
- row thinning;
- feature deletion;
- lower precision;
- threshold relaxation;
- solver-family change;
- evidence substitution;
unless separately frozen as a scientific or methodological decision.

## 7. Adjudication record

The prose result record must identify:

- raw disposition;
- whether all numerical validity gates passed;
- Function Map additions;
- Limit Map additions;
- native prior-art/native-model explanation;
- whether project \(\chi\), \(\Chi\), or \(\Chi_{\mathrm{arc}}\) is admitted, refused, or not identified;
- promotion debt;
- P1 eligibility;
- exact scientific ceiling;
- exact next authorized action.

The adjudication record must never silently convert a native representation into project notation.

## 8. Function / Limit ledger

Every result should add zero or more explicit Function and Limit entries.

### Function entry schema

- identifier;
- domain;
- task;
- representation level;
- evidence class;
- source result;
- native comparator;
- condition under which the function holds;
- promotion status.

### Limit entry schema

- identifier;
- domain;
- failed/insufficient representation or mapping;
- condition where failure occurs;
- whether failure is scientific, measurement, estimation, transport, implementation, or numerical;
- source result;
- whether it is local or program-wide.

Rare/local failures remain visible but do not override majority behavior unless the scientific question concerns the failure boundary itself.

## 9. Cross-domain synthesis rule

Cross-domain recurrence may motivate a new question but cannot promote a universal law by accumulation alone.

A cross-domain synthesis must preserve:
- domain-native mechanisms;
- different evidence classes;
- different representation admissions;
- negative and redundant cases;
- native-framework equivalence;
- local outliers and reversals;
- promotion debt.

The synthesis should ask what discrimination architecture generalizes, not whether all systems share one hidden variable.

## 10. Failure provenance

All failures are retained with root-cause class:

- SCIENTIFIC_RESULT
- DATA_IDENTITY_OR_ACCESS
- TRANSPORT
- IMPLEMENTATION
- RESOURCE_ALLOCATION
- NUMERICAL_CONVERGENCE
- REPRESENTATION_NONIDENTIFIABILITY
- CONTINUITY_OR_ORCHESTRATION

A repaired failure remains in lineage. Successful recovery appends rather than erases.

## 11. Directory convention

Recommended canonical layout:

- protocols / qualification documents in stability_inheritance/
- analyzers in stability_inheritance/
- durable prose result records in stability_inheritance/
- machine-readable results under stability_inheritance/results/<task>/
- source receipts under task-specific receipt/provenance files
- CONTINUITY_STATE.json for live machine-readable continuity
- COMPUTE_CONVEYOR_QUEUE_v0.1.json for execution lineage
- WORKING_INVESTIGATION.md for chronological scientific record
- cross-domain matrices and Function/Limit ledgers as versioned synthesis artifacts

Large externally hosted raw data remain external when stable checksums and retrieval identity are sufficient.

## 12. Reproduction tiers

### Tier R0 — provenance-only
A reader can identify the exact source, protocol, code, and result but may not possess the source data.

### Tier R1 — deterministic rerun
A reader with the source data can execute the exact analyzer and reproduce the machine-readable result.

### Tier R2 — independent implementation
A separately implemented calculation reproduces the disposition under the same frozen scientific design.

### Tier R3 — independent evidence
A distinct dataset/system prospectively tests the same declared relation.

R3 is evidence expansion, not merely stronger software reproducibility.

## 13. Current DESI SI reproduction path

The DESI lane currently demonstrates the intended structure:

1. official release chains with per-file SHA-256 receipts;
2. shared-coordinate protocol + pre-result validation amendment;
3. exact analyzer identity;
4. full-chain execution on Popstop;
5. raw JSON + SHA-256;
6. prose adjudication;
7. tracer decomposition protocol frozen after Result 1;
8. Result 2 with LOSC, single-tracer, and leave-one-tracer controls;
9. cross-block protocol frozen before interaction scoring;
10. memory repairs preserving scientific design;
11. provisional v0.1c retained when convergence warnings appear;
12. convergence-validity audit frozen before final disposition exposure;
13. three-result adjudication map frozen before the convergence-qualified result.

This sequence is reproducibility machinery, not itself evidence for SI.

## 14. Minimum release packet for an SI paper

A public SI paper should eventually ship:

- main manuscript;
- supplementary information;
- reproducibility guide;
- protocol/preregistration packet;
- exact analysis code;
- environment specification;
- source manifest with hashes and retrieval instructions;
- machine-readable result tables;
- Function/Limit map;
- failure ledger;
- figure-generation scripts and figure source tables;
- README with one-command or staged reproduction where technically practical.

## Stop condition

This scaffold is operational guidance. It does not alter the current DESI execution or authorize new evidence. Any change that affects the scientific question still requires the normal GOM gate.
