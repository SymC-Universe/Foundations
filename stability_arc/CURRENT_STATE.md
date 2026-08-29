# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`

Frozen hypotheses, thresholds, failures, HOLDs, exclusions, and interpretation firewalls remain controlling. Failed or insufficient phases are not repaired by post-outcome retuning.

## GFSA v0.7.2

Package validation, C18, OBS18, OBS19, external-interface licensing, and observable-only EP firewall remain closed PASS.

External numerical admission remains quarantined because the authentic frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered. External candidate response values remain sealed.

## Measurement-conditioned representation currently licensed

1. same-noise physical and same-record inference tangent generators remain distinct;
2. their deterministic difference is a low-rank conditioning bridge;
3. admitted sigma_z measured-qubit controls possess an exact conditioning-dark factor and exact 2D stochastic active quotient;
4. deterministic `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` is licensed separately per channel only under its deterministic 2D admissibility rules;
5. the stochastic pair `(A_A,B_A)` remains uncompressed;
6. symmetric second moments evolve under a real 3x3 generator `G`;
7. complete mean-square asymptotic stability requires `c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`;
8. required stochastic report remains `MEAN_SQUARE_INVARIANTS_REQUIRED`.

No stochastic scalar chi is licensed.

## Preserved failures and HOLDs

- joint representation v0.1: permanent mathematical/specification FAIL;
- generalized spectral-abscissa H2: permanent FAIL with 441 counterexamples;
- c3 displacement-map v0.1: permanent binary64 D3 numerical-oracle FAIL, with structural gates retained;
- H6 c3-only full-class sufficiency: permanent scientific/model-boundary FAIL;
- H7 c1-corrected broad-frame test: `SELECTION_HOLD`, not PASS/FAIL;
- H8 high-radius existence threshold: FAIL; H8 sufficiency: INSUFFICIENT, not PASS.

Later successes do not erase these records.

## H4/H5 real class-crossing lineage

H4 run `33257117162`: `PASS_TARGETED_CROSSING_H4`.

- 100000 fresh target-region inputs;
- 52435 robust physical STABLE cases frozen before record reveal;
- 50 robust physical STABLE -> record UNSTABLE crossings;
- 50/50 independently reconstructed.

H5 run `33263959965`: `PASS_PROSPECTIVE_C3_GATE_H5`.

- new 100000-case seed;
- 52944 robust physical STABLE cases frozen before reveal;
- 54 robust crossings;
- 54/54 independently reconstructed;
- zero mechanism counterexamples;
- every record failure used the c3 gate while the other three normalized Routh-Hurwitz margins remained positive.

## Exact c3/c1 boundary lineage

Run `33257258056`: `PASS_C3_BOUNDARY_DERIVATION`. Physical and record `c3=0` surfaces are exact quadratics in frequency and satisfy `c3=-det(G)`.

Displacement-map v0.1 run `33264098911` remains `DISPLACEMENT_MAP_FAILURE`: 16 root-adjacent binary64 determinant comparisons exceeded the frozen `2e-10` oracle gate, with zero sign/interval disagreements.

High-precision remediation run `33264252192`: `PASS_D3_HIGH_PRECISION_REMEDIATION` under the unchanged gate. 24830 non-boundary probes, zero 80-digit failures, maximum error about `4.96e-74`.

Exact c1 run `33266715420`: `PASS_C1_GATE_DERIVATION`:

`c1_phys = 9*gamma/2 + 3*kappa - 14*q*z^2`,

`c1_record = 9*gamma/2 + 3*kappa + 6*q - 20*q*z^2`,

so

`c1_record-c1_phys = 6*q*(1-z^2) >= 0`

for physical states.

## H6 c3-only full-class sufficiency: PERMANENT FAIL

Run `33266630910`, seed `2026082909`, 250000 fresh broad candidates.

Stage A froze 512 c3-only `I_destab` and 512 `I_stab` cases before full reveal.

- `I_destab`: 0/512 full crossings;
- `I_stab`: 512/512 full crossings in the frozen panel;
- every false `I_destab` case was already physically blocked by `m1`;
- 506 also failed physical `m2`;
- 6 also failed physical `mh`.

Conclusion: c3 displacement is a real boundary coordinate but not a sufficient complete stability-class coordinate across the broad frame.

## H7 broad c1-corrected test: SELECTION_HOLD

Run `33266791185`, seed `2026082912`, 500000 fresh candidates with Bloch radius restricted to `r<0.98`.

Stage A could use only c3 plus exact physical c1. It found:

- `I_destab + positive c1_phys`: 0;
- `I_stab`: 90161.

The preregistered minimum was not met, so no H7D/H7S scientific score is licensed.

Audit reconciliation showed an old H4 crossing would satisfy the exact H7 c1+c3 selector but has `r≈0.99810`, outside H7 support. This motivated a new fresh domain test rather than more draws from the same truncated frame.

## H8 state-geometry audit

Run `33266926497`, seed `2026082913`, 400000 fresh candidates in four radial shells crossed with `x*z` NEG/POS.

All G0-G5 mechanical/reconstruction gates passed.

Eligible c1+c3 destabilizing counts:

- R1 `[0.90,0.95)`: NEG 0, POS 0;
- R2 `[0.95,0.98)`: NEG 0, POS 0;
- R3 `[0.98,0.995)`: NEG 0, POS 0;
- R4 `[0.995,0.9999)`: NEG 2, POS 0.

Registered outcomes:

- H8E high-radius >=20 existence: FAIL;
- H8L low-radius absence: PASS;
- H8F: `INSUFFICIENT_H8F` because only two cases existed. Both 2/2 were full crossings but cannot be promoted.

Canonical result:
`stability_arc/measurement_conditioned/state_geometry_v01/STATE_GEOMETRY_ADMISSIBILITY_RESULT_v0.1.md`.

## H9 near-pure orientation test: PASS

Run `33267026845`, seed `2026082914`.

Exactly 1,000,000 fresh R4 states were generated:

- 500000 `x*z<0`;
- 500000 `x*z>0`.

Stage A used only exact c1+c3 before full reveal.

Eligible counts:

- NEG: 33;
- POS: 0.

All N0-N5 audit gates passed. Maximum c1/c3 reconstruction error `1.080649077427649e-13`.

Registered outcomes:

- H9N negative-orientation existence: PASS;
- H9P matched positive-orientation absence: PASS;
- H9F c1+c3 full-class sufficiency: PASS, 33/33 physical STABLE -> record UNSTABLE, zero m2/mh blockers and zero boundary cases.

This is bounded near-pure evidence, not a universal orientation law.

Canonical result:
`stability_arc/measurement_conditioned/near_pure_orientation_v01/NEAR_PURE_ORIENTATION_RESULT_v0.1.md`.

## Exact orientation algebra: PASS

Run `33267107733`: `PASS_ORIENTATION_C3_DECOMPOSITION`.

For fixed magnitudes with `x=s*a`, `z=b`, `s=+/-1`:

`c3_phys(s)=E_phys+s*M_phys`,

`M_phys=16*a*b*q*omega*(gamma+kappa-3*q*b^2)`,

`c3_record(s)=E_record+s*M_record`,

`M_record=4*a*b*q*omega*(7*gamma+6*kappa+8*q-30*q*b^2)`.

Thus orientation reversal changes each c3 exactly by `2*M`, while c1 is exactly orientation-sign independent. At `q=0`, both c1 and c3 are orientation invariant.

All symbolic gates and 512 fresh two-sign classifier controls passed with zero label mismatches.

Canonical result:
`stability_arc/measurement_conditioned/orientation_algebra_v01/ORIENTATION_C3_DECOMPOSITION_RESULT_v0.1.md`.

## ACTIVE: independent rotated-measurement geometry

Live run: `33267236939`
Execution commit: `db02b49ed7167f61632af4e85b05e78151fcbccb`

Preregistration:
`stability_arc/measurement_conditioned/rotated_measurement_v01/PREREGISTRATION_ROTATED_MEASUREMENT_ARCHITECTURE_v0.1.md`.

The measured observable is changed from `sigma_z/2` to

`X45=(sigma_x+sigma_z)/(2*sqrt(2))`,

while the Hamiltonian and amplitude-damping axes remain unchanged.

The fresh 128-fixture phase asks whether the separate tangent channels, rank-one bridge, one-dimensional conditioning-dark factor, exact 2D stochastic quotient, second-moment closure, and coordinate covariance survive this distinct measurement geometry.

A fixed generic 3D measurement-axis control must return `REFUSE_NO_1D_DARK_FACTOR` rather than forcing a quotient.

No sigma_z c1/c3 orientation result is assumed to transfer.

## Historical blockers

- GFSA external numerical admission: authentic v0.7 contract/source package absent;
- historical QuTiP notebook reproduction: authentic source absent, expected SHA-256 `be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the active rotated-measurement architecture test.

## User action

None currently required.
