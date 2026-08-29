# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`

Frozen hypotheses, thresholds, failure records, exclusions, and interpretation firewalls remain controlling. FAIL, HOLD, NONIDENTIFIABLE, REFUSE, and selection failure are evidence and may not be repaired by post-outcome retuning.

## GFSA v0.7.2

Package validation, C18, OBS18, OBS19, interface licensing, and observable-only EP firewall remain closed PASS.

External numerical admission remains quarantined because the authentic frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered. External candidate response values remain sealed.

## Measurement-conditioned representation

The currently licensed hierarchy is:

1. separate same-noise physical and same-record inference tangent generators;
2. a low-rank deterministic conditioning bridge;
3. an exact conditioning-dark factor for admitted measured-qubit controls;
4. an exact 2D stochastic active quotient `dq=A_A q dt+B_A q dW`;
5. deterministic `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` separately licensed only under its deterministic 2D admissibility conditions;
6. stochastic pair `(A_A,B_A)` remains uncompressed;
7. symmetric second moments evolve under a real 3x3 generator `G`;
8. complete mean-square asymptotic stability requires `c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`.

Required stochastic report remains `MEAN_SQUARE_INVARIANTS_REQUIRED`. No stochastic scalar chi is licensed.

## Preserved failure lineage

- joint representation v0.1: permanent mathematical/specification FAIL;
- generalized spectral-abscissa H2: permanent FAIL with 441 admitted counterexamples;
- c3 displacement-map v0.1: permanent numerical-oracle D3 FAIL despite structural D0/D1/D2/D4/D5 PASS;
- H6 c3-only full-class sufficiency: permanent scientific/model-boundary FAIL;
- H7 c1-corrected broad-frame test: `SELECTION_HOLD`, not PASS or FAIL.

Later phases do not erase these records.

## H4 and H5 targeted crossing lineage

H4 run `33257117162`: `PASS_TARGETED_CROSSING_H4`.

- 100000 fresh target-region inputs;
- 52435 physical robust STABLE cases frozen before record reveal;
- 50 robust physical STABLE -> record UNSTABLE crossings;
- 50/50 independently reconstructed.

H5 run `33263959965`: `PASS_PROSPECTIVE_C3_GATE_H5`.

- new 100000-case seed;
- 52944 physical robust STABLE cases frozen before record reveal;
- 54 robust crossings;
- 54/54 independently reconstructed;
- zero mechanism counterexamples;
- all 54 record-channel failures occurred with positive `c1`, positive `c2`, negative `c3`, and positive `c1*c2-c3` under the frozen normalized margins.

Thus real class crossings exist in the registered near-axis target family and prospectively cross through the record c3 gate in that family.

## Exact c3 geometry and numerical-oracle lineage

Run `33257258056`: `PASS_C3_BOUNDARY_DERIVATION`. Separate physical and record `c3=0` surfaces are exact quadratics in frequency and satisfy `c3=-det(G)`.

Displacement-map v0.1 run `33264098911` remains `DISPLACEMENT_MAP_FAILURE`: D3 binary64 determinant comparison failed on 16 deliberately root-adjacent probes, maximum error `3.973577272775586e-09` against the frozen `2e-10` gate, while all signs/interval labels remained correct.

High-precision remediation v0.2 run `33264252192` is `PASS_D3_HIGH_PRECISION_REMEDIATION` under the unchanged gate:

- 24830 non-boundary probes;
- 0 high-precision failures;
- maximum error about `4.96e-74` at 80 decimal digits;
- 0 sign disagreements.

Canonical v0.2 result:
`stability_arc/measurement_conditioned/c3_displacement_v02/C3_DISPLACEMENT_D3_HIGH_PRECISION_REMEDIATION_RESULT_v0.2.md`.

The c3 displacement representation is supported only through this explicit composite lineage. v0.1 is never rewritten as PASS.

## H6 c3-only full-class sufficiency: PERMANENT FAIL

Run `33266630910`, fresh seed `2026082909`, 250000 broad candidates.

Stage A used c3 only and froze 512 robust `I_destab` plus 512 robust `I_stab` cases before full mean-square reveal.

Result:

- `I_destab` precision: `0/512`;
- `I_stab` precision: `512/512` in this bounded panel;
- 512 robust counterexamples to c3-only destabilizing sufficiency;
- every false `I_destab` prediction was already physically blocked by `m1`;
- 506 also failed physical `m2`;
- 6 also failed physical `mh`;
- no selected case was boundary-classed;
- c3 reconstruction remained clean.

Canonical result:
`stability_arc/measurement_conditioned/c3_map_full_class_v01/C3_MAP_FULL_CLASS_VALIDATION_RESULT_v0.1.md`.

Failure report:
`stability_arc/measurement_conditioned/c3_map_full_class_v01/FAILURE_SIGNAL_REPORT_v0.1.md`.

Conclusion: c3 displacement is a real boundary coordinate but is not sufficient by itself for complete mean-square class displacement in the broad sampling frame.

## Exact c1 gate derivation: PASS

Run `33266715420`: `PASS_C1_GATE_DERIVATION`.

Exact identities:

`c1_phys = 9*gamma/2 + 3*kappa - 14*q*z^2`,

`c1_record = 9*gamma/2 + 3*kappa + 6*q - 20*q*z^2`,

and therefore

`c1_record-c1_phys = 6*q*(1-z^2) >= 0`

for physical states.

Fresh 128-case clean-room and coordinate-covariance audits passed. Same-record conditioning can only move the first Hurwitz coefficient upward, or leave it unchanged at `q=0`, in this exact model.

Canonical result:
`stability_arc/measurement_conditioned/c1_gate_v01/C1_GATE_DERIVATION_RESULT_v0.1.md`.

## H7 c1-corrected broad-frame test: SELECTION_HOLD

Run `33266791185`, fresh seed `2026082912`, exactly 500000 broad candidates.

Stage A was allowed to know only c3 displacement plus exact physical c1. It required robust `I_destab` and `c1_phys/R>1e-8` before full reveal.

Available cases:

- corrected `I_destab_c1`: `0`;
- `I_stab`: `90161`.

The preregistration required at least 128 in both classes, so H7 returned `SELECTION_HOLD` before scientific Stage-B scoring. No H7D or H7S PASS/FAIL is licensed.

Canonical result:
`stability_arc/measurement_conditioned/c1_corrected_map_v01/C1_CORRECTED_MAP_TEST_RESULT_v0.1.md`.

Geometry reconciliation:
`stability_arc/measurement_conditioned/c1_corrected_map_v01/SELECTION_HOLD_GEOMETRY_RECONCILIATION_v0.1.md`.

Audit consistency shows the earlier H4 example `XC002679` strongly satisfies positive physical c1 plus the c3 destabilizing sign pattern, but has Bloch radius about `0.99810`; H7 sampled only `r<0.98`. Therefore the H7 empty selection is a sampling-domain signal, not a contradiction with H4/H5 and not an impossibility theorem.

## ACTIVE: state-geometry admissibility v0.1

Live run: `33266926497`
Execution commit: `b2a7c5312f32556b5047e5a62a1bfd8300505d82`

Preregistration:
`stability_arc/measurement_conditioned/state_geometry_v01/PREREGISTRATION_STATE_GEOMETRY_ADMISSIBILITY_v0.1.md`.

The fresh audit uses seed `2026082913`, exactly 400000 candidates, four radial shells straddling the old `r=0.98` cutoff, and both `x*z<0` and `x*z>0` strata.

Stage A may use only exact physical c1 and separate exact physical/record c3 coordinates. It freezes eligible selections before any c2, final Hurwitz margin, G eigenvalue, or full class is revealed.

Registered questions:

- H8E: do at least 20 corrected c1+c3 destabilizing candidates exist for `r>=0.98`?
- H8L: does the fresh `r<0.98` shell replication again contain zero such candidates?
- H8F: once eligible cases are frozen, are they all full physical STABLE -> record UNSTABLE crossings, or do unseen `m2`/`mh` blockers remain?

Failures remain evidence and may only motivate later fresh phases.

## QuTiP / historical closure

QuTiP 5.3.1 runtime is admitted. Authentic historical v0.6 notebook reproduction remains open because the original source has not been recovered. Expected notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Historical Phase 4A remains PENDING/INCOMPLETE.

## Current blockers

- GFSA external admission: authentic frozen v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic notebook absent;
- historical Phase 4A: incomplete.

None blocks the active state-geometry investigation.

## User action

None currently required.
