# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical working branch: `agent/stability-arc-gfsa-v072`

## Control documents

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`
- `stability_arc/gfsa_v0.7.2/PROVENANCE_RECOVERY_SEARCH_LOG_v0.1.md`
- `stability_arc/gfsa_v0.7.2/external_admission/v0.7/RECOVERY_TARGETS_v0.1.json`
- `stability_arc/measurement_conditioned/PREREGISTRATION_CONDITIONAL_TANGENT_DERIVATION_AUDIT_v0.1.md`
- `stability_arc/measurement_conditioned/CONDITIONAL_TANGENT_DERIVATION_AUDIT_RESULT_v0.1.md`
- `stability_arc/qutip_runtime/QUTIP_RUNTIME_ADMISSION_RESULT_v0.1.md`

## Latest verified closed state

GFSA v0.7.2 executable package validation: PASS.
C18 calibration validity: PASS.
OBS18 interface admissibility: PASS.
OBS19 blind holdout: PASS.
External interface status: LICENSED_FOR_EXTERNAL_NUMERICAL_ADMISSION.
Observable-only EP firewall: PASS.
Conditional measurement-tangent derivation audit v0.1: PASS under frozen T0-T4 gates.
QuTiP 5.3.1 runtime admission v0.1: RUNTIME_ADMITTED under frozen Q0-Q3 gates.

The licensed GFSA observable output remains limited to a finite-band visible modal pole-proximity interval across the permitted surrogate equivalence class, or `NONIDENTIFIABLE`. No hidden-generator order/rationality, mechanical chi, or observable-only exceptional-point claim is licensed.

The measurement-conditioned derivation PASS closes only the registered differential identities and exact 2x2 second-order reduction. It does not establish that a tangent spectrum predicts localization, that a scalar chi exists for a general conditional generator, or that chi=1 is optimal under measurement.

The QuTiP runtime admission establishes only that an independently archived pinned QuTiP 5.3.1 runtime is operational and passes its frozen analytic/runtime integrity gates. It does not reproduce the historical v0.6 QuTiP notebook, which remains a separate provenance/reproducibility target.

## Current work-cycle milestone

### Conditional tangent derivation

Initial run `33231598000` failed mechanically during `actions/setup-python@v5` because pip caching was requested in a repository with no `requirements.txt` or `pyproject.toml`. No T0-T4 scientific gate executed. The failed run and artifact were retained as evidence.

The smallest non-scientific repair removed only the inappropriate cache request. No equation, fixture, tolerance, dependency version, gate, or decision rule changed. Repair commit: `3cc3c498f62a2f6a03b9b0fe8d7fb3ea1225cdd2`.

Corrected run `33231627696` completed SUCCESS. Frozen source identities were preserved before execution:

- preregistration SHA-256 `0dc7cf7f1538a5e591e1df48f80de3bb370796aabfbac01728e584577b514938`
- audit-code SHA-256 `c8e95b5e865fd467f4c7aca8783b0346f8d1ab283db1e23265922193590281ac`

All T0-T4 gates passed. Successful artifact ID `9708659316`, ZIP SHA-256 `7b650e93e518a468da674a4422828988ef0ae4ede97ab54023d21e41f4abf962`.

### QuTiP runtime admission

Run `33231741394` at head commit `aeb141066fa9e21ad58b341da8c02ab01644ae3a` completed SUCCESS.

Frozen source identities:

- preregistration SHA-256 `0b5a9d09dce1fd1555deeed3f2b85ae8d764b7a14235c39a66d3a2a7051a5412`
- runtime-code SHA-256 `74e17512b324e2ad07262f632c61ce59edf28deb2390cbe217381d8c99edfb3a`
- workflow SHA-256 `ff220dd5c99c84ae9557b9f4b8ad082215ce08c9e3148c92e67b29e91820d2b4`

Q0-Q3 passed. The analytic dephasing test maximum absolute error was `1.5216428117525993e-10` under the frozen `1e-7` gate. Trace and Hermiticity errors were `0.0`, minimum density eigenvalue was `0.0`, and the evidence manifest verified cleanly.

Final status: `RUNTIME_ADMITTED / HISTORICAL_NOTEBOOK_CROSSCHECK_STILL_PENDING`.

Artifact ID `9708692674`, ZIP SHA-256 `ccea56a1929ca10832e56c34e31cb4bbe27f2b1d95e64a942f85e3d884446dd1`.

The exact frozen v0.7 external-candidate contract remains unrecovered. The missing rule set has not been reconstructed from gate names, historical summaries, remembered thresholds, or candidate outcomes.

## Active frontiers

### A. Measurement-conditioned quantum-position branch

The same-noise physical tangent and same-record inference tangent remain distinct, separately auditable objects. The next representation phase must also investigate whether useful structure emerges from their relationship without conflating them.

Before any localization holdout, freeze a representation-level protocol that preserves at minimum:

- the same-noise physical tangent spectrum;
- the same-record inference tangent spectrum;
- their conditioning difference as a separately labeled comparative object;
- fixed, outcome-free rules for any cross-spectrum mode matching;
- eigenvalue displacement and mode/eigenvector overlap where mathematically defined;
- separate scalar stability coordinates only where each channel independently supports them;
- comparative quantities such as scalar displacement only where matched modes make that operation legitimate;
- a joint/augmented representation that retains both channel identities;
- explicit refusal to compress the joint representation to a single scalar unless independently justified by the mathematics;
- an unconditional measurement-dressed Liouvillian control;
- exact second-order recovery and scalar-refusal controls.

No historical localization outcome may be used to select a combination, weighting, mode pairing, threshold, scalar compression, or preferred representation.

### B. QuTiP independent-engine closure

The QuTiP 5.3.1 runtime is now admitted for future preregistered independent work. The historical notebook cross-check remains open because the original notebook bytes/source with expected SHA-256 `be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82` have not yet been recovered into the canonical repository. Runtime admission must not be misreported as historical reproduction.

### C. GFSA v0.7 external admission

Recover and bind the exact frozen v0.7 external-candidate admission contract before inspecting candidate response values, then stage the reproducible external-admission runner around the already-validated v0.7.2 observer interface.

## Anti-circularity state

External candidate search remains metadata-only. No candidate numerical response values may be inspected, plotted, summarized, filtered by outcome, or numerically scored until the frozen v0.7 contract is recovered, persisted, hashed, and bound to the runner.

The measurement-conditioned derivation and future joint-channel representation must be frozen without consulting historical localization outcomes. Same-noise and same-record channels may be studied jointly, but every constituent channel must remain separately recoverable and no combined scalar may be invented because it happens to align with a desired boundary.

The QuTiP runtime-admission gates were frozen before execution and used an analytic control, not prior Stability Arc outcomes.

## Failure-signal state

Failures are retained as evidence and must be classified/investigated rather than discarded.

Run `33231598000` is classified **MECHANICAL / CI CONFIGURATION**. It revealed a workflow portability defect before any scientific gate executed. The failed state and artifact remain preserved.

The historical Phase 3Y/3Z record remains the canonical scientific example: Y2 stayed failed, its pattern motivated a bounded post-hoc refinement, and only the separately frozen Phase 3Z fresh-holdout result earned narrower prospective support.

## Current blockers

- **PROVENANCE / EXECUTION:** exact frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered into the canonical repository.
- **HISTORICAL REPRODUCIBILITY:** original v0.6 QuTiP cross-check notebook/source remains unrecovered; the newly admitted runtime does not substitute for it.
- **HISTORICAL SCIENTIFIC:** Phase 4A remains PENDING/INCOMPLETE and would require a new complete preregistered package if scientifically restarted.

None of these blockers prevents continued outcome-free work on the measurement-conditioned representation.

## Queue

### COMPLETED THIS CYCLE

1. Closed conditional tangent derivation audit v0.1 as PASS under frozen T0-T4 gates.
2. Preserved and investigated its initial mechanical CI failure.
3. Admitted a pinned QuTiP 5.3.1 runtime under frozen Q0-Q3 gates.
4. Preserved runtime provenance, environment, exact source hashes, artifact ID, and artifact digest.
5. Kept historical QuTiP reproduction explicitly open rather than conflating runtime admission with reproduction.
6. Preserved GFSA external-candidate quarantine throughout.
7. Added the joint-channel requirement: same-noise and same-record dynamics remain separate controls while their relationship is also investigated prospectively and without outcome-driven compression.

### ACTIVE

- Prepare and freeze the next outcome-free measurement-conditioned representation audit, including separate and joint/comparative channel structure, unconditional measurement-dressed control, mode-pairing/refusal logic, and second-order recovery.
- Continue exact-source recovery for the historical QuTiP notebook/source and the v0.7 external-admission contract using only sources capable of authenticating chronology and bytes.

### BLOCKED

- External numerical admission/scoring: blocked on exact v0.7 contract recovery.
- Historical QuTiP independent-engine reproduction: blocked on recovery of the preserved source/notebook or exact equivalent archived source.
- Historical Phase 4A: remains PENDING/INCOMPLETE.

### NEXT

1. Freeze the representation-level protocol before any new outcome-bearing execution.
2. Audit separate physical and inference spectra plus their comparative/joint structure without consulting localization outcomes.
3. Preserve REFUSE/NONIDENTIFIABLE as legitimate outcomes and investigate all failures/HOLDs.
4. Only after representation closure, design a separately preregistered prospective localization/interface test on untouched systems.
5. Independently, if the authentic v0.7 external contract or historical QuTiP notebook is recovered, hash and bind it before scientific execution.

## User action

None currently required.
