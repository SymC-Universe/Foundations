# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`

Frozen hypotheses, thresholds, failures, HOLDs, exclusions, and interpretation firewalls remain controlling. Failure signals are preserved and may motivate only separately frozen fresh tests.

## GFSA v0.7.2

Package validation, C18, OBS18, OBS19, external-interface licensing, and observable-only EP firewall remain closed PASS.

External numerical admission remains quarantined because the authentic frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered. External candidate response values remain sealed.

## Measurement-conditioned licensed hierarchy

1. Same-noise physical and same-record inference tangents remain separately recoverable.
2. Their deterministic difference is a low-rank conditioning bridge.
3. Where the maximal conditioning-dark factor is exactly one-dimensional, the full stochastic tangent SDE can descend to an exact two-dimensional active quotient.
4. Deterministic `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` is licensed separately per channel only under the deterministic 2D admissibility rules.
5. The stochastic pair `(A_A,B_A)` remains uncompressed.
6. Symmetric second moments evolve under a real 3x3 generator `G`.
7. Mean-square asymptotic stability requires `c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`.
8. Required stochastic reporting remains `MEAN_SQUARE_INVARIANTS_REQUIRED`.

No stochastic scalar chi is licensed.

## Preserved failures / HOLDs

- joint representation v0.1: permanent mathematical/specification FAIL;
- generalized spectral-abscissa H2: permanent FAIL with 441 counterexamples;
- c3 displacement v0.1: permanent binary64 D3 numerical-oracle FAIL, with structural passes retained;
- H6 c3-only full-class sufficiency: permanent scientific/model-boundary FAIL;
- H7 c1-corrected broad frame: `SELECTION_HOLD`;
- H8 high-radius >=20 existence: FAIL; H8F: INSUFFICIENT.

Later closures do not erase these records.

## Sigma-z crossing and mechanism lineage

H4 run `33257117162`: `PASS_TARGETED_CROSSING_H4`.
- 100000 fresh target-region cases;
- 52435 robust physical STABLE cases frozen before record reveal;
- 50 robust STABLE -> UNSTABLE crossings;
- 50/50 independently reconstructed.

H5 run `33263959965`: `PASS_PROSPECTIVE_C3_GATE_H5`.
- new 100000-case seed;
- 52944 physical robust STABLE cases frozen before reveal;
- 54 robust crossings;
- 54/54 independently reconstructed;
- zero c3-mechanism counterexamples.

Exact sigma-z c3 and c1 derivations remain closed PASS. The c3 high-precision remediation passed under the unchanged tolerance while the binary64 predecessor failure remains permanent.

## H6-H9 state-domain sequence

H6 run `33266630910`: permanent `FAIL_C3_MAP_FULL_CLASS_H6`.
- c3-only `I_destab`: 0/512 full crossings;
- c3-only `I_stab`: 512/512 in the bounded panel;
- every false `I_destab` case was already physically blocked by `m1`.

Exact c1 derivation run `33266715420`: PASS.

`c1_phys=9*gamma/2+3*kappa-14*q*z^2`

`c1_record=9*gamma/2+3*kappa+6*q-20*q*z^2`

`c1_record-c1_phys=6*q*(1-z^2)>=0` for physical states.

H7 run `33266791185`: `SELECTION_HOLD`. Its `r<0.98` broad frame contained zero corrected destabilizing c1+c3 cases.

H8 run `33266926497`: R1-R3 contained zero eligible cases; R4 `[0.995,0.9999)` contained two NEG and zero POS. H8E failed its >=20 minimum; H8F remained insufficient.

H9 run `33267026845`: bounded near-pure PASS.
- 500000 fresh R4 `x*z<0` states and 500000 matched `x*z>0` states;
- eligible NEG: 33; POS: 0;
- all 33/33 frozen eligible NEG cases were full physical STABLE -> record UNSTABLE crossings;
- zero `m2`/`mh` blockers and zero boundary cases.

This is not a universal orientation law.

## Exact orientation decomposition

Run `33267107733`: `PASS_ORIENTATION_C3_DECOMPOSITION`.

For `x=s*a`, `z=b`, `s=+/-1` at fixed magnitudes:

`c3_phys(s)=E_phys+s*M_phys`

with `M_phys=16*a*b*q*omega*(gamma+kappa-3*q*b^2)`, and

`c3_record(s)=E_record+s*M_record`

with `M_record=4*a*b*q*omega*(7*gamma+6*kappa+8*q-30*q*b^2)`.

Thus orientation reversal changes each c3 by exactly `2*M`; c1 is exactly orientation-sign independent.

## Rotated and general planar measurement transfer

Run `33267236939`: `PASS_ROTATED_AXIS_STOCHASTIC_QUOTIENT` for fixed `X45=(sigma_x+sigma_z)/(2sqrt(2))` on 128 fresh fixtures. The generic 3D measurement-axis control returned `REFUSE_NO_1D_DARK_FACTOR`.

Run `33267394149`: `PASS_PLANAR_MEASUREMENT_DARK_BOUNDARY`.

For any planar measurement axis `n(theta)=(sin(theta),0,cos(theta))`, the exact observability boundary is

`Delta_obs=omega-(gamma/4)*sin(2theta)`.

`kappa` cancels exactly. Away from `Delta_obs=0`, the maximal dark factor is exactly `span(e_y)` and the full stochastic tangent descends to the 2D quotient. At exact `Delta_obs=0`, dark dimension becomes 2 and the required state is `REFUSE_QUOTIENT_DIMENSION`. Generic out-of-plane measurement retains `REFUSE_NO_1D_DARK_FACTOR`.

Canonical result:
`stability_arc/measurement_conditioned/planar_measurement_v01/PLANAR_MEASUREMENT_DARK_BOUNDARY_RESULT_v0.1.md`.

## General planar mean-square invariants

Run `33267544870`: `PASS_PLANAR_QUOTIENT_INVARIANTS`.

In measurement-aligned quotient coordinates `u=n dot (x,z)`, `v=m dot (x,z)` define

`q=eta*kappa`,
`p=gamma*(1+cos(theta)^2)/2`,
`d=kappa+gamma*(1+sin(theta)^2)/2`,
`h=gamma*sin(2theta)/4`.

Exact quotient matrices:

`A_phys=[[-p,h-omega],[h+omega,-d]]`

`B=-sqrt(2q)*[[2u,0],[v,u]]`

`A_record=A_phys+[[-2q(1-u^2),0],[2quv,0]]`.

The complete separate physical/record `(c1,c2,c3)` triples are exact functions of this canonical quotient. In particular

`c1_phys=3*(p+d)-14*q*u^2`

`c1_record=3*(p+d)+6*q-20*q*u^2`

and `Delta_c1=6*q*(1-u^2)`.

Exact `theta=0` reduction recovers the sigma-z c1/c3 formulas. Fresh X45 and general-planar Hilbert reconstructions passed.

Canonical result:
`stability_arc/measurement_conditioned/planar_invariants_v01/PLANAR_QUOTIENT_INVARIANTS_RESULT_v0.1.md`.

## ACTIVE: distinct dissipation geometry

Live run: `33267651929`
Execution commit: `a70d52eefad4f1a7fade43eda8833297f900fa58`
Workflow: `Stability Arc dephasing augmented planar transfer v0.1`

Preregistration:
`stability_arc/measurement_conditioned/dephasing_augmented_v01/PREREGISTRATION_DEPHASING_AUGMENTED_PLANAR_TRANSFER_v0.1.md`.

This phase adds independent pure dephasing jump `sqrt(gamma_phi/2)*sigma_z` to amplitude damping.

Define transverse rate `a=gamma/2+gamma_phi` and longitudinal rate `b=gamma`. The frozen target observability boundary is

`Delta_phi=omega-(b-a)*sin(theta)*cos(theta)`

`=omega-(gamma/2-gamma_phi)*sin(theta)*cos(theta)`.

The target canonical quotient is the same algebraic family with

`p=a*sin(theta)^2+b*cos(theta)^2`,
`d=kappa+a*cos(theta)^2+b*sin(theta)^2`,
`h=(b-a)*sin(theta)*cos(theta)`.

The run tests exact symbolic transfer, 256 fresh dephasing-augmented fixtures, two exact shifted-boundary refusals with positive frequency, amplitude-damping reduction, complete mean-square invariant transfer, and generic out-of-plane refusal.

No prior crossing region is assumed to transfer.

## Historical blockers

- GFSA external numerical admission: authentic frozen v0.7 contract/source package absent;
- historical QuTiP notebook reproduction: authentic source absent, expected SHA-256 `be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the active dissipation-transfer test.

## User action

None currently required.
