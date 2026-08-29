# Stability Arc / GFSA closure reconciliation v0.1

Date: 2026-08-29
Status: ACTIVE PROJECT-CONTROL RECORD
Branch: `agent/stability-arc-gfsa-v072`

This record reconciles the older Stability-Boundary measurement/substrate investigation queue with the current Generator-First Stability Architecture v0.7.2 lane. It does not alter a historical claim, preregistration, threshold, interpretation, or scientific outcome.

## 1. Current v0.7.2 closure

A clean extraction of the supplied v0.7.2 package has been independently revalidated. Its package validator passes, C18 passes, OBS18 passes, OBS19 passes, the observable-only EP firewall passes, and the documented OBS18/OBS19 rescoring commands regenerate byte-identical result files. Exact archive/file hashes and regenerated-result hashes are preserved in `SOURCE_PACKAGE_PROVENANCE_v0.1.md`.

This establishes only the reproducibility and internal closure claimed by v0.7.2. It licenses the interface for external numerical admission **subject to the already-frozen v0.7 external-candidate contract**. It does not authorize reconstruction of that missing contract from memory or from candidate outcomes.

## 2. Historical items that remain historical rather than silently rewritten

### QuTiP independent-engine cross-check

Historical status remains **PENDING** unless a later archived execution artifact is recovered. The v0.9 provenance record preserved the independent QuTiP notebook but did not preserve an executed independent-engine comparison. v0.7.2 package closure does not retroactively convert that historical pending item into a pass.

### Phase 4A continuous-measurement backaction

Historical status remains **PENDING/INCOMPLETE; no final scientific claim accepted**. Five execution-transcript script recoveries were preserved historically, while the original common model module, original monolithic driver, and transient result tables were not recovered byte-for-byte. If this scientific axis is revisited, it must begin under a new complete preregistered source/results package rather than treating the incomplete historical branch as a completed baseline.

### CL011 and related Phase 3D provenance

CL011 remains recorded at its historical evidentiary status: **PROSPECTIVELY SUPPORTED** for the H1 crossover-bracket prediction, with 6/6 fresh symmetric holdouts within the frozen tolerance in the preserved claim ledger. That status is not promoted further here.

The transient retrospective source `phase3d_retrospective_fast.py` was not preserved byte-identically in the historical package, and the machine-readable pre-reference H2 pole-class artifact was not preserved. Those gaps remain explicit. In particular, the broader pole-class statement associated with CL012 remains **NOT CLAIMED**; no present reconstruction may backfill prospective chronology.

### v1.0 pre-move provenance gaps

The historical v1.0 pre-move audit found that the then-current phase-delta package lacked substantial scientific source/data and several final result artifacts, including critical reconstruction material for later substrate/interface phases. Those absences remain provenance debt unless exact artifacts are recovered. They are not treated as evidence against the reported science, but they cannot be silently marked closed merely because the current GFSA package is healthy.

## 3. Current active execution gate

The highest-priority unresolved item in the current lane is recovery of the **exact frozen v0.7 external-candidate admission contract**.

External candidate numerical response values remain sealed. Before any inspection or scoring, the recovered contract must unambiguously point to the already-frozen rules for:

1. file provenance;
2. channel mapping;
3. numerical quality;
4. uncertainty handling;
5. bandwidth / observation window;
6. observer or surrogate-order rules;
7. PASS / FAIL / NONIDENTIFIABLE decision logic;
8. exclusions and stop conditions.

The recovered contract, referenced files, code/configuration, and candidate inputs must be hashed before outcome inspection. `code/pre_admission_guard_v01.py` enforces this as a fail-closed mechanical gate.

## 4. Anti-circularity consequence

The current state is therefore:

- **not** a scientific failure;
- **not** permission to improvise the missing external rules;
- **not** permission to inspect a candidate first and decide afterward which rule appears reasonable;
- **not** permission to use historical validation/holdout outcomes to retune a rule and count the same evidence again as prospective.

Until the exact v0.7 contract is recovered, the correct machine state for external admission is `PROVENANCE_HOLD`.

## 5. Queue

### COMPLETED

- v0.7.2 clean-extract package validation.
- Independent byte-identical OBS18/OBS19 rescoring.
- Source/archive hash capsule committed.
- Anti-circularity execution guard committed.
- Fail-closed pre-admission provenance checker committed.
- Historical open-item statuses reconciled without retroactive promotion.

### ACTIVE

- Search repository/history and preserved project artifacts for the exact frozen v0.7 external-candidate contract and its referenced code/configuration.
- Preserve candidate values from inspection during that search.

### BLOCKED

- External numerical admission/scoring: blocked on exact v0.7 contract recovery.
- Historical QuTiP independent-engine comparison: pending unless executed output is recovered or the preserved notebook is run under an independently archived environment.
- Historical Phase 4A: incomplete; requires a new preregistered package if restarted.

### NEXT AFTER CONTRACT RECOVERY

1. Hash and record the recovered contract and every referenced scientific input before viewing candidate responses.
2. Populate the recovery record consumed by `pre_admission_guard_v01.py`.
3. Require the guard to emit `READY_FOR_FROZEN_EXTERNAL_ADMISSION` without changing any scientific rule.
4. Only then execute the frozen external admission and archive raw inputs, outputs, environment, decision record, and hashes.
5. Preserve PASS, FAIL, and NONIDENTIFIABLE exactly as produced; no outcome-dependent retuning.
