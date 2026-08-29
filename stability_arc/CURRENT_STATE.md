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

## Latest verified closed state

GFSA v0.7.2 executable package validation: PASS.
C18 calibration validity: PASS.
OBS18 interface admissibility: PASS.
OBS19 blind holdout: PASS.
External interface status: LICENSED_FOR_EXTERNAL_NUMERICAL_ADMISSION.
Observable-only EP firewall: PASS.
Conditional measurement-tangent derivation audit v0.1: PASS under frozen T0-T4 gates.

The licensed GFSA observable output remains limited to a finite-band visible modal pole-proximity interval across the permitted surrogate equivalence class, or `NONIDENTIFIABLE`. No hidden-generator order/rationality, mechanical chi, or observable-only exceptional-point claim is licensed.

The measurement-conditioned derivation PASS closes only the registered differential identities and exact 2x2 second-order reduction. It does not establish that a tangent spectrum predicts localization, that a scalar chi exists for a general conditional generator, or that chi=1 is optimal under measurement.

## Current work-cycle milestone

The conditional measurement-tangent derivation audit was frozen before execution and run in GitHub Actions.

Initial run `33231598000` failed mechanically during `actions/setup-python@v5` because pip caching was requested in a repository with no `requirements.txt` or `pyproject.toml`. No T0-T4 scientific gate executed. The failed run and artifact were retained as evidence.

The smallest non-scientific repair removed only the inappropriate cache request. No equation, fixture, tolerance, dependency version, gate, or decision rule changed. Repair commit: `3cc3c498f62a2f6a03b9b0fe8d7fb3ea1225cdd2`.

Corrected run `33231627696` completed SUCCESS. Frozen source identities were preserved before execution:

- preregistration SHA-256 `0dc7cf7f1538a5e591e1df48f80de3bb370796aabfbac01728e584577b514938`
- audit-code SHA-256 `c8e95b5e865fd467f4c7aca8783b0346f8d1ab283db1e23265922193590281ac`

All gates passed:

- T0 trace/tangent validity: PASS; largest listed trace residual `6.938893903907228e-18`.
- T1 same-noise finite-difference gate: PASS; maximum fine-epsilon error `1.7007870458309456e-09` versus frozen `1e-7` limit, with improvement at smaller epsilon for every fixture.
- T2 same-record finite-difference gate: PASS; maximum fine-epsilon error `1.7064751790239328e-09`, with improvement at smaller epsilon for every fixture.
- T3 exact second-order reduction: PASS; maximum absolute reduction error `0.0`.
- T4 refusal controls: PASS; both registered invalid/unstable controls returned `REFUSE`.

Successful artifact ID `9708659316`, ZIP SHA-256 `7b650e93e518a468da674a4422828988ef0ae4ede97ab54023d21e41f4abf962`.

The exact frozen v0.7 external-candidate contract remains unrecovered. The missing rule set has not been reconstructed from gate names, historical summaries, remembered thresholds, or candidate outcomes.

## Active frontiers

### A. Measurement-conditioned quantum-position branch

The differential tangent equations and exact second-order reduction are now mechanically and numerically closed under v0.1. Next safe work is representation/reproducibility development that does not use prior localization outcomes as fitting targets. Before any localization holdout, freeze a response-relevant mode-pairing / tangent-spectrum representation with explicit scalar-refusal rules and an unconditional measurement-dressed Liouvillian control.

### B. GFSA v0.7 external admission

Recover and bind the exact frozen v0.7 external-candidate admission contract before inspecting candidate response values, then stage the reproducible external-admission runner around the already-validated v0.7.2 observer interface.

## Anti-circularity state

External candidate search remains metadata-only. No candidate numerical response values may be inspected, plotted, summarized, filtered by outcome, or numerically scored until the frozen v0.7 contract is recovered, persisted, hashed, and bound to the runner.

The measurement-conditioned derivation audit used fixed analytic identities, fixtures, tolerances, and refusal controls frozen before execution. It did not read prior localization errors or external-candidate outcomes. Its PASS may justify continuing the derivation program but may not be counted as evidence that the representation predicts localization.

## Failure-signal state

Failures are retained as evidence and must be classified/investigated rather than discarded.

The run `33231598000` failure is classified **MECHANICAL / CI CONFIGURATION**. It revealed a workflow portability defect: setup-python cache mode implicitly depended on a package-manifest file that the repository does not use. Because the failure occurred before dependency installation and before execution of the audit code, it carries no T0-T4 scientific signal. The exact failed state and artifact remain preserved.

The historical Phase 3Y/3Z record remains the canonical scientific example: Y2 stayed failed, its pattern motivated a bounded post-hoc refinement, and only the separately frozen Phase 3Z fresh-holdout result earned narrower prospective support.

## Current blockers

- **PROVENANCE / EXECUTION:** exact frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered into the canonical repository.
- **HISTORICAL REPRODUCIBILITY:** QuTiP independent-engine comparison remains pending unless executed output is recovered or the preserved notebook/source is recovered and run in an independently archived environment.
- **HISTORICAL SCIENTIFIC:** Phase 4A remains PENDING/INCOMPLETE and would require a new complete preregistered package if scientifically restarted.

None of these blockers prevents continued outcome-free work on the measurement-conditioned representation.

## Queue

### COMPLETED THIS CYCLE

1. Launched frozen conditional tangent derivation audit v0.1.
2. Preserved initial mechanical CI failure and its artifact.
3. Diagnosed exact cause without altering frozen science.
4. Applied minimal cache-only workflow repair.
5. Reran the unchanged scientific audit.
6. Closed T0-T4 as PASS.
7. Preserved source hashes, environment, result hashes, workflow IDs, artifact ID, and artifact digest.
8. Persisted the result and failure analysis in the repository.
9. Preserved GFSA external-candidate quarantine throughout.

### ACTIVE

- Develop and freeze the next outcome-free measurement-conditioned stability representation: unconditional measurement-dressed Liouvillian control, response-relevant mode pairing, modal damping/stability spectrum, exact second-order reduction, and explicit scalar-refusal conditions.
- Continue exact-source recovery for the v0.7 external-admission contract using only sources capable of authenticating the frozen chronology and bytes.

### BLOCKED

- External numerical admission/scoring: blocked on exact v0.7 contract recovery.
- Historical QuTiP independent-engine comparison: blocked on recovery/execution of the preserved independent-engine source/output.
- Historical Phase 4A: remains PENDING/INCOMPLETE.

### NEXT

1. Freeze the next representation-level audit before running it.
2. Test only mathematical consistency, mode-pairing invariance/refusal behavior, unconditional-control reduction, and second-order recovery; do not use historical localization outcomes as a target.
3. Investigate any PASS, FAIL, HOLD, or NONIDENTIFIABLE result under the failure-signal protocol.
4. Only after representation closure, design a separately preregistered prospective localization/interface test on untouched systems.
5. Independently, if the authentic v0.7 external contract is recovered, hash and bind it before any candidate response inspection.

## User action

None currently required.
