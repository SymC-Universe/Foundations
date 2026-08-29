# Evidence and Failure Ledger v1.0

**Science freeze anchor:** `5a1c0d3a579f0251374544973c1ff53194bba722`

This ledger is intentionally mixed. Positive results, failures, holds, insufficiencies, numerical limitations, and implementation errors are all part of the evidentiary record.

| Phase | Canonical result | Status | Evidentiary meaning |
|---|---|---|---|
| Conditional tangent v0.1 | `measurement_conditioned/CONDITIONAL_TANGENT_DERIVATION_AUDIT_RESULT_v0.1.md` | PASS | Same-noise physical and same-record inference tangents independently validated; exact second-order recovery. |
| Joint representation v0.1 | `representation_v01/FAILURE_SIGNAL_REPORT_v0.1.md` | PERMANENT FAIL | Wrong control damping factor, missing stochastic prefactor, and partial self-certification exposed. |
| Joint representation v0.2 | `representation_v02/JOINT_CHANNEL_REPRESENTATION_AUDIT_RESULT_v0.2.md` | PASS | Corrected separate-plus-joint representation; rank-one conditioning difference; no spectral averaging. |
| Active quotient scalar | `active_quotient_scalar_v01/ACTIVE_QUOTIENT_SCALAR_ADMISSIBILITY_RESULT_v0.1.md` | PASS | Legitimate 2D deterministic quotient carries invariant `chi_active`; full generators and stochastic term remain uncompressed. |
| Stochastic dark/active | `stochastic_dark_active_v01/STOCHASTIC_DARK_ACTIVE_QUOTIENT_RESULT_v0.1.md` | PASS | Both A and B preserve dark factor for admitted fixtures; exact 2D stochastic quotient. |
| Mean-square geometry | `mean_square_geometry_v01/MEAN_SQUARE_STABILITY_GEOMETRY_RESULT_v0.1.md` | PASS | 3D second-moment generator and full cubic Routh-Hurwitz classifier established. |
| Directionality bounded precursor | `conditioning_directionality_v01/CONDITIONING_MEAN_SQUARE_DIRECTIONALITY_RESULT_v0.1.md` | BOUNDED PASS | Supported a narrower registered sample only; later broad generalization failed. |
| Generalized H2 stress | `conditioning_structural_stress_v01/CONDITIONING_STRUCTURAL_STRESS_RESULT_v0.1.md` | `FAIL_GENERALIZED_H2` | 441 counterexamples reject universal monotonic spectral-abscissa improvement. |
| H2 mechanism successor | `conditioning_failure_mechanism_v01/CONDITIONING_FAILURE_MECHANISM_RESULT_v0.1.md` | PROSPECTIVE PASS | Fresh weak-measurement mechanism test supported the narrower failure mechanism; does not rescue generalized H2. |
| H3 class monotonicity | `class_monotonicity_v01/CLASS_MONOTONICITY_ADVERSARIAL_RESULT_v0.1.md` | BOUNDED PASS | No crossing in frozen 512-case near-boundary panel; bounded result only. |
| H4 class crossing | `class_crossing_v01/TARGETED_CLASS_CROSSING_RESULT_v0.1.md` | PASS | 50/50 fresh physical-STABLE to record-UNSTABLE crossings independently reconstructed; universal class preservation falsified. |
| c3 boundary derivation | `c3_boundary_v01/C3_BOUNDARY_DERIVATION_RESULT_v0.1.md` | PASS | Exact channel-specific c3 boundary quadratics derived. |
| c3 displacement v0.1 | `c3_displacement_v01/FAILURE_SIGNAL_REPORT_v0.1.md` | PERMANENT NUMERICAL FAIL | 16 root-adjacent binary64 determinant-oracle failures; no sign/interval mismatches. |
| c3 displacement v0.2 | `c3_displacement_v02/C3_DISPLACEMENT_D3_HIGH_PRECISION_REMEDIATION_RESULT_v0.2.md` | PASS REMEDIATION | 80-digit oracle passed unchanged gate; original v0.1 remains failed. |
| H5 prospective c3 gate | `c3_gate_test_v01/C3_GATE_CROSSING_RESULT_v0.1.md` | PASS | 54/54 fresh crossings; zero registered c3-pattern counterexamples. |
| H6 c3 full-class map | `c3_map_full_class_v01/C3_MAP_FULL_CLASS_VALIDATION_RESULT_v0.1.md` | PERMANENT SCIENTIFIC FAIL | c3 alone insufficient; 512 I_destab predictions already physically failed through c1. |
| c1 derivation | `c1_gate_v01/C1_GATE_DERIVATION_RESULT_v0.1.md` | PASS | Exact c1 relation and nonnegative same-record displacement derived. |
| H7 c1-corrected map | `c1_corrected_map_v01/C1_CORRECTED_MAP_TEST_RESULT_v0.1.md` | `SELECTION_HOLD` | Broad support frame produced no robust target cases; not a scientific pass/fail. |
| H8 state geometry | `state_geometry_v01/STATE_GEOMETRY_ADMISSIBILITY_RESULT_v0.1.md` | H8E FAIL / H8L PASS / H8F INSUFFICIENT | High-radius concentration exposed; only two fresh eligible cases, both correct but below minimum. |
| H9 near-pure orientation | `near_pure_orientation_v01/NEAR_PURE_ORIENTATION_RESULT_v0.1.md` | BOUNDED PASS | 33 eligible NEG orientation cases, 0 POS; 33/33 crossings. Not universal. |
| Orientation algebra | `orientation_algebra_v01/ORIENTATION_C3_DECOMPOSITION_RESULT_v0.1.md` | PASS | Orientation sign enters c3 affinely; c1 sign-independent in registered sigma-z representation. |
| Rotated measurement | `rotated_measurement_v01/ROTATED_MEASUREMENT_ARCHITECTURE_RESULT_v0.1.md` | PASS | 45-degree axis transfers architecture; generic out-of-plane control correctly refuses 1D dark factor. |
| Planar dark boundary | `planar_measurement_v01/PLANAR_MEASUREMENT_DARK_BOUNDARY_RESULT_v0.1.md` | PASS | Exact `Delta_obs` boundary and quotient-dimension refusal. |
| Planar invariants | `planar_invariants_v01/PLANAR_QUOTIENT_INVARIANTS_RESULT_v0.1.md` | PASS | Exact general-planar A, B, A_record and separate invariant triples. |
| Dephasing parent | `dephasing_augmented_v01/FAILURE_SIGNAL_REPORT_v0.1.md` | PERMANENT IMPLEMENTATION FAIL | Boolean `D3` overwritten by array. Other registered structural gates passed. |
| Dephasing remediation | `dephasing_augmented_v011/D3_IDENTIFIER_REMEDIATION_RESULT_v0.1.1.md` | PASS REMEDIATION | Independent symbolic D3 remediation; parent not rewritten. |
| H10 dephasing transfer | `dephasing_crossing_v01/DEPHASING_CROSSING_TRANSFER_RESULT_v0.1.md` | H10S PASS / H10D SELECTION HOLD | Stabilizing side 128/128; destabilizing broad panel only 2 cases, below minimum. |
| H11 availability | `dephasing_d_availability_v01/DEPHASING_D_AVAILABILITY_RESULT_v0.1.md` | READY FOR BLIND REVEAL | 10M fresh cases, 69 eligible, first 64 frozen before hidden stability. Not scientific confirmation itself. |
| H11 reveal | `dephasing_d_reveal_v01/DEPHASING_D_BLIND_REVEAL_RESULT_v0.1.md` | PASS | 64/64 immutable fresh cases crossed STABLE to UNSTABLE; zero counterexamples/holds. |
| H12 Stage A | `dephasing_d_replication_v01/DEPHASING_D_REPLICATION_STAGEA_RESULT_v0.1.md` | READY FOR BLIND REVEAL | Independent untouched seed, 10M fresh cases, 71 eligible, first 64 frozen. |
| H12 reveal | `dephasing_d_replication_reveal_v01/DEPHASING_D_REPLICATION_BLIND_REVEAL_RESULT_v0.1.md` | `PASS_H12D_REPLICATION` | 64/64 independent replication; zero counterexamples, boundaries, reconstruction failures, or hidden m2/mh blockers. |

## Failure lessons carried forward

### Joint representation v0.1

A representation can fail even if later corrected. A wrong damping coefficient, missing stochastic prefactor, or self-certifying gate is sufficient to invalidate an audit. The corrective v0.2 exists beside, not in place of, the failed v0.1.

### Generalized H2

"More stable" is not a single total ordering. Decay-rate spectral abscissa and Routh-Hurwitz margins can move in opposite directions while both systems remain stable.

### c3 displacement numerical failure

Near a boundary, the numerical oracle can fail before the analytic structure does. The fix was a new high-precision oracle under the same tolerance, not a relaxed tolerance.

### H6

A correct boundary component is not necessarily a sufficient classifier. Full stability required the complete margin set.

### H7/H8

Absence of enough admissible cases is a selection or design result, not evidence for the hypothesis.

### Dephasing parent implementation failure

Mechanical failures remain part of reproducibility lineage even when an independently frozen remediation closes the intended identity.

## Permanent rule

No entry in this ledger may be relabeled retrospectively to improve the narrative.
