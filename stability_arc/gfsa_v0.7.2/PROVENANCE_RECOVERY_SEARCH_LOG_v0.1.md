# GFSA v0.7 external-admission provenance recovery search log v0.1

Date: 2026-08-29
Branch: `agent/stability-arc-gfsa-v072`
Status: `PROVENANCE_HOLD`

## Purpose

Record the durable search for the exact frozen v0.7 external-candidate admission contract without inspecting external candidate numerical response values and without reconstructing scientific rules from memory.

This is a provenance/recovery artifact only. It does not alter any scientific setting, threshold, scoring rule, uncertainty rule, bandwidth rule, interpretation, or conclusion.

## Sources searched in this recovery cycle

1. Canonical GitHub branch `SymC-Universe/Foundations@agent/stability-arc-gfsa-v072`:
   - repository tree under `stability_arc/`;
   - GFSA v0.7.2 staging tree;
   - Git commit/search history available to the connected GitHub integration;
   - current provenance-guard workflow and guard files.
2. Durable File Library searches using combinations of the known external-gate names and v0.7/GFSA terminology, including:
   - external candidate admission / external numerical admission;
   - file provenance;
   - channel mapping;
   - numerical quality;
   - uncertainty;
   - bandwidth;
   - metadata-only candidate search;
   - no candidate response values inspected.
3. Recovered GFSA v0.7.2 interface documents already preserved from the supplied package:
   - `PREREGISTRATION_EQUIVALENCE_BRIDGE_v0.7.2.md`;
   - `INTERFACE_LICENSE_v0.7.2.md`;
   - `INTERFACE_BRIDGE_REPORT_v0.7.2.md`;
   - `REPRODUCIBILITY_GUIDE_v0.7.2.md`.
4. Historical Stability-Boundary / Stability-Arc provenance artifacts in File Library used only to reconstruct project chronology and failure-handling rules. These are not substitutes for the missing v0.7 external contract.

## Recovery result

### Exact v0.7 external-candidate contract

`NOT_RECOVERED`

No searched source produced an artifact that can be authenticated as the exact frozen v0.7 external-candidate admission preregistration/configuration. Therefore `CONTRACT_RECOVERED.json` must not be created and the pre-admission guard must remain closed.

### Candidate numerical response exposure

`NONE`

No external candidate response values were inspected, plotted, summarized, filtered by outcome, or scored during this recovery cycle.

### Constraints independently recovered from v0.7.2 continuity documents

The v0.7.2 interface record establishes only the following external-admission boundary facts for recovery purposes:

- the v0.7 external search remained metadata-only at the v0.7.2 freeze;
- no candidate response values had been inspected at that freeze;
- the validated v0.7.2 observable interface is separate from external numerical admission;
- an external candidate must independently pass the frozen v0.7 gates named as file provenance, channel mapping, numerical quality, uncertainty, and bandwidth;
- these gate names do not reveal their exact thresholds, algorithms, schemas, or decision logic and therefore are insufficient to reconstruct the contract.

No threshold or missing rule is inferred from these facts.

## Historical continuity recovered during the search

Historical recovery records were found that materially improve project continuity without opening the external gate:

- the Stability-Boundary v0.9 provenance guide explicitly requires a failed criterion to remain failed; a failure may generate a new mathematical target but cannot confirm it, and any new target must be frozen before an untouched prospective reference is generated;
- the same guide records the independent QuTiP notebook as prepared but externally unexecuted, and Phase 4A as PENDING/INCOMPLETE with no accepted final claim because key original source/results were not byte-preserved;
- later recovery ledgers preserve the Phase 3Y Y2 failure rather than rewriting it, and separate the subsequent Phase 3Z fresh-holdout refinement as new prospective evidence.

These records are continuity evidence and failure-signal precedent. They do not authorize any missing v0.7 external-admission rule.

## CI / fail-closed state

The repository provenance guard remains deliberately fail-closed. The expected state while the exact contract is absent is `PROVENANCE_HOLD`; this state is a successful enforcement result, not a scientific failure.

## Exact remaining recovery targets

The following durable inputs can legitimately resolve the provenance hold:

1. the original v0.7 external-candidate preregistration/configuration/source artifact(s), with authentic chronology/hash evidence;
2. a v0.7 or v0.7.1 package/repository snapshot containing those files;
3. a Git bundle/history that contains the original files and predates candidate numerical outcome inspection;
4. the full previously supplied GFSA archive if it contains an authenticated parent-package pointer to the v0.7 external contract;
5. a historical manifest or execution record that identifies the exact load-bearing contract files and hashes, followed by recovery of those exact bytes.

The authoritative candidate-source package is also required before execution, but only metadata permitted by the recovered historical contract may be inspected before the contract gate opens.

## Stop condition

Do not advance from provenance recovery to numerical external admission until all of the following hold simultaneously:

1. exact contract bytes are recovered;
2. chronology/provenance is authenticated;
3. load-bearing files are SHA-256 recorded and verified;
4. every frozen gate and its exact decision logic is represented without reconstruction from outcomes;
5. `candidate_values_inspected` remains false through the freeze record;
6. the independent pre-admission guard returns `READY_FOR_FROZEN_EXTERNAL_ADMISSION`.

Until then, the scientifically correct state is `PROVENANCE_HOLD`.
