# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical working branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`
- `stability_arc/gfsa_v0.7.2/PROVENANCE_RECOVERY_SEARCH_LOG_v0.1.md`

Frozen science, preregistrations, thresholds, exclusions, failure records, and interpretation firewalls remain controlling. FAIL, HOLD, null, NONIDENTIFIABLE, and REFUSE are admissible evidence and may not be repaired by retuning against observed outcomes.

## GFSA v0.7.2 state

Closed PASS: package validation, C18, OBS18, OBS19, external-interface licensing, and observable-only EP firewall.

External numerical admission remains quarantined because the exact authentic frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered. Candidate response values remain sealed.

## Measurement-conditioned established hierarchy

Closed outcome-free representation results support:

1. separate same-noise physical and same-record inference tangent generators;
2. a low-rank deterministic conditioning bridge;
3. an exact conditioning-dark factor on admitted measured-qubit controls;
4. an exact two-dimensional stochastic active quotient `dq=A_A q dt+B_A q dW`;
5. deterministic `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` separately licensed only under admitted deterministic 2D scalar conditions;
6. stochastic pair `(A_A,B_A)` remains uncompressed;
7. symmetric second moments evolve under a real 3x3 generator `G`;
8. cubic mean-square stability requires `c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`.

Required stochastic reporting state remains `MEAN_SQUARE_INVARIANTS_REQUIRED`. No stochastic scalar chi is licensed.

## Preserved failure lineage

- Joint representation v0.1: permanent mathematical/specification FAIL.
- Generalized spectral-abscissa H2: permanent `FAIL_GENERALIZED_H2`, 441 admitted counterexamples to global `alpha_rec<=alpha_phys`.
- H3 near-boundary class test: bounded PASS on its frozen 512-case panel only.

Failures remain evidence and are not erased by narrower successor passes.

## H4 targeted class-crossing closure

Canonical result:
`stability_arc/measurement_conditioned/class_crossing_v01/TARGETED_CLASS_CROSSING_RESULT_v0.1.md`

Run `33257117162`: `PASS_TARGETED_CROSSING_H4`.

- 100000 fresh target-region inputs, seed `2026082905`;
- 52435 robust physical mean-square STABLE cases frozen before record reveal;
- 50 robust physical STABLE -> record UNSTABLE crossings;
- 50/50 independently reconstructed.

Thus stability-class preservation is not universal even within this exact measured-qubit family.

## Exact c3 boundary derivation closure

Canonical result:
`stability_arc/measurement_conditioned/c3_boundary_v01/C3_BOUNDARY_DERIVATION_RESULT_v0.1.md`

Run `33257258056`: `PASS_C3_BOUNDARY_DERIVATION`.

The physical and record channel `c3` surfaces are exact quadratics in frequency. `c3=-det(G)` and all registered coefficient/root identities passed independent symbolic and fresh numerical checks.

This licenses separate channel-specific `c3=0` surfaces, not universal c3 dominance.

## H5 prospective c3-gate mechanism closure

Canonical result:
`stability_arc/measurement_conditioned/c3_gate_test_v01/C3_GATE_CROSSING_RESULT_v0.1.md`

Canonical run `33263959965`: `PASS_PROSPECTIVE_C3_GATE_H5`.

- new seed `2026082907`;
- 100000 fresh unchanged target-region inputs;
- 52944 robust physical STABLE cases frozen before record reveal;
- 54 robust physical STABLE -> record UNSTABLE crossings;
- 54/54 independently reconstructed;
- zero mechanism counterexamples;
- all 54 satisfied `c1_rec>0`, `c2_rec>0`, `c3_rec<0`, `c1_rec*c2_rec-c3_rec>0` under the frozen normalized margins;
- exact c3 quadratic vs determinant maximum error `4.344084788515155e-13`.

Within this frozen target family, the class-crossing mechanism is prospectively supported as a record-channel c3-gate loss. This remains a bounded family result.

A redundant H5 rerun triggered when the result document was persisted. It is orchestration-only and does not supersede canonical run `33263959965`. Future workflows use path-specific triggers to prevent result persistence from rerunning science.

## c3 boundary-displacement representation v0.1: PERMANENT FAIL

Preregistration/code run:
`33264098911`

Failure report:
`stability_arc/measurement_conditioned/c3_displacement_v01/FAILURE_SIGNAL_REPORT_v0.1.md`

Overall status: `DISPLACEMENT_MAP_FAILURE`.

Frozen results:

- D0 coefficient lineage: PASS;
- D1 synthetic interval/refusal controls: PASS;
- D2 256 fresh sign partitions: PASS, 0 disagreements;
- D3 direct determinant reconstruction: **FAIL**, 16 comparison failures, max error `3.973577272775586e-09` vs frozen `2e-10` gate;
- D4 channel-swap covariance: PASS;
- D5 set coverage: PASS.

Artifact `9718105705`, ZIP SHA-256 `b7545d48f9b17fb5220ae2197d161b70cbc9b79e1fd0966777d69714e11846f5`.

Failure investigation found all 16 D3 failures exclusively at the preregistered two-sided probes approximately `1e-7` relative distance from `c3=0` roots. All 16 preserved the same c3 sign and joint interval label. There were zero sign disagreements and zero partition disagreements.

The failure is classified `NUMERICAL / NEAR-BOUNDARY DETERMINANT CONDITIONING`: binary64 `numpy.linalg.det` did not satisfy the strict equality gate near an intentionally near-singular determinant. v0.1 remains failed and its `2e-10` gate is not loosened.

## ACTIVE: c3 displacement D3 high-precision remediation v0.2

Preregistration:
`stability_arc/measurement_conditioned/c3_displacement_v02/PREREGISTRATION_C3_DISPLACEMENT_D3_HIGH_PRECISION_REMEDIATION_v0.2.md`

Live workflow:
`Stability Arc c3 displacement D3 high precision v0.2`

Run: `33264252192`
Execution commit: `7d7943aaea178e78301dc90bb34bd3aaea640329`

v0.2 changes no scientific formula, seed, base tuple, frequency probe, root offset, or tolerance. It retains the same `2e-10` D3 gate and independently reconstructs `-det(G)` at 80 decimal digits using pinned `mpmath==1.3.0`, while retaining NumPy 2.1.3 binary64 only as a diagnostic fingerprint of the v0.1 failure.

If v0.2 passes, the displacement map is composite-closed only by citing v0.1 structural PASS gates plus permanent D3 FAIL together with v0.2 high-precision D3 remediation. v0.1 is never rewritten as PASS.

If v0.2 fails in high precision, representation promotion stops and the high-precision counterexample becomes a scientific/numerical failure signal requiring investigation.

## Next justified step after composite displacement closure

Freeze a new untouched-seed prospective test in which the set-valued physical-vs-record c3 map predicts `I_destab`, `I_stab`, and agreement regions **before** full four-gate mean-square classification is revealed. Preserve all other Routh-Hurwitz margins as mandatory admissibility information. Measure prediction success/failure without averaging the physical and record channels or compressing them to a stochastic scalar.

Only after this representation-level prospective test is closed should any localization/interface prediction phase be designed.

## QuTiP state

QuTiP 5.3.1 runtime is admitted. Historical v0.6 notebook reproduction remains open because the authentic original notebook/source is absent. Expected historical notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

## Current external blockers

- GFSA external admission: exact frozen v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the current measurement-conditioned v0.2 remediation.

## Continuity state

The earlier disabled-controller incident is classified MECHANICAL / CONTINUITY_AUTOMATION. The controller has been re-enabled and is bound to run `33264252192`. It must inspect/persist completion and advance to the next justified safe phase rather than leaving the Actions page idle.

## User action

None currently required.
