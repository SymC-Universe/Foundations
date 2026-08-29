# Stability Arc historical failure-signal recovery v0.1

Date: 2026-08-29
Branch: `agent/stability-arc-gfsa-v072`
Status: `CONTINUITY_RECOVERY_RECORD`

## Purpose

Persist historically important failure-handling and unresolved-branch state recovered from durable File Library artifacts so future work does not depend on conversational memory.

This record is documentary/provenance only. It changes no historical result, preregistration, threshold, interpretation, or conclusion. The source artifacts remain authoritative; this file is a continuity index of their recovered content.

## Durable source artifacts consulted

1. `V1_RECOVERY_LEDGER(3).xlsx` (recovered File Library artifact; eight-tab recovery ledger).
2. `Stability-Boundary_Quantum_Measurement_Reproducibility_Guide_v0.9.docx`, frozen 12 August 2026.

If either source is later committed byte-for-byte to the canonical repository, replace this documentary pointer with exact repository path plus SHA-256. Do not claim byte identity from this summary alone.

## Failure-handling rule recovered from v0.9

The v0.9 guide defines the required scientific sequence:

1. freeze the question/model/metrics/gates before the target outcome;
2. execute and apply the frozen decision rule;
3. preserve a failed criterion as failed;
4. permit that failure to generate a new mathematical hypothesis, but not to confirm it;
5. freeze the new target/prediction before an untouched reference;
6. promote only if the fresh prospective test survives, with domain limits retained.

The guide explicitly describes failures as model-selection evidence rather than disposable negative outcomes.

## Phase 3Y -> Phase 3Z failure signal

The recovered v1 ledger records a concrete example of the rule above.

### Phase 3Y

- Y0 basis gate: PASS.
- Y1 absolute-accuracy gate: PASS.
- Y2 relative-superiority gate: FAIL.
- Y2 observed pointwise improvements: 11/16.
- Frozen Y2 requirement: at least 14/16 plus all registered geometry means improving.
- Scientific consequence: the strong conjunctive Y1+Y2 claim remained failed. It was not threshold-repaired.

The ledger labels the subsequent analysis of this failure as `POSTHOC_DISCOVERY_PRESERVED`: it may motivate a follow-up but cannot itself count as prospective support.

### Phase 3Z

A fresh prospective refinement was then run on new E12-E15 holdouts rather than reusing Phase 3Y as confirmation.

- Z0: PASS.
- Z1: PASS, aggregate interface RMSE 0.01159635190932108 under the frozen absolute-accuracy rule.
- Z2: PASS, 8/8 registered higher-damping channels at chi in {1.0, 1.4} improved.
- Low-damping outcomes were retained descriptively and explicitly were not used to rescue Z2.

Scientific consequence: only the narrower damping-activated boundary refinement earned fresh prospective support. The original broader Phase 3Y superiority claim remains failed.

This is the canonical template for treating a failure as signal without circularity: investigate the pattern, bound the new interpretation, freeze a new test, and require fresh evidence.

## Runtime-continuity failure also preserved

The recovered ledger records that transient raw prediction/reference files were lost after result freeze during the Phase 3Y/3Z continuity sequence. Exact execution records and reproduction code were recovered, but regenerated curves are not to be claimed byte-identical to lost transient raw files.

This is a provenance/continuity failure, not a scientific pass/fail result. The correct response is preservation of the distinction between execution-time identity and later regeneration.

## QuTiP independent-engine state

The v0.9 guide identifies the preserved notebook:

`history/v0.6_source/notebooks/Stability_Measurement_v0.6_QuTiP_Crosscheck.ipynb`

Historical state:

- notebook prepared and pinned for an independent solver stack;
- intended target QuTiP release: 5.3.1;
- local runtime could not install/run QuTiP;
- independent-engine comparison remained pending;
- an eventual run must archive the executed notebook, environment/package versions, raw outputs, comparison tables, and disagreements;
- conflicting engines must be diagnosed rather than averaged.

No later GFSA package pass retroactively changes this historical status.

## Phase 4A state

The v0.9 guide preserves five exact transcript-recovered Phase 4A scripts but records the original common model module, original monolithic scan driver, and transient result CSVs as not byte-recovered.

Historical state remains:

`PENDING/INCOMPLETE; NO FINAL SCIENTIFIC CLAIM ACCEPTED`

A future restart of this axis requires a new complete preregistered package. The incomplete historical branch cannot be promoted by reconstruction after the fact.

## Current relation to GFSA v0.7.2

These recovered historical states do not block the already-validated GFSA v0.7.2 internal interface closure. They do constrain what historical evidence can be claimed and how future failures must be handled.

The current external-admission frontier remains separately blocked on exact recovery of the frozen v0.7 external-candidate contract. No candidate numerical response values were inspected while producing this record.
