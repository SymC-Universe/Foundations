# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`

Frozen hypotheses, thresholds, failures, HOLDs, exclusions, source identities, and interpretation firewalls remain controlling. Failures may motivate only separately frozen fresh tests. Physical same-noise and same-record inference channels remain separately recoverable in all joint analyses.

## GFSA v0.7.2

Package validation, C18, OBS18, OBS19, external-interface licensing, and observable-only EP firewall remain closed PASS.

External numerical admission remains quarantined because the authentic frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered. External candidate response values remain sealed.

Historical QuTiP notebook reproduction remains open because the authentic original source has not been recovered. Expected SHA-256: `be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Historical Phase 4A remains PENDING/INCOMPLETE.

## Current measurement-conditioned architecture

Where the maximal conditioning-dark factor is exactly one-dimensional, the full stochastic tangent SDE admits an exact two-dimensional active quotient. The stochastic quotient remains a matrix pair `(A_A,B_A)` and is not compressed to a scalar.

Mean-square stability is governed by the real 3x3 symmetric second-moment generator `G`. With

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`,

strict mean-square asymptotic stability requires

`c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`.

Required stochastic report remains `MEAN_SQUARE_INVARIANTS_REQUIRED`.

## Important preserved failures / non-closures

- joint representation v0.1: permanent mathematical/specification FAIL;
- generalized spectral-abscissa H2: permanent FAIL with 441 counterexamples;
- c3 displacement v0.1: permanent binary64 numerical-oracle D3 FAIL, later high-precision remediation PASS under unchanged tolerance;
- H6 c3-only full-class sufficiency: permanent scientific FAIL;
- H7 c1-corrected broad-frame test: `SELECTION_HOLD`;
- H8 high-radius existence threshold: FAIL; H8F sufficiency: INSUFFICIENT;
- dephasing-augmented structural transfer parent v0.1 run `33267651929`: permanent `AUDIT_IMPLEMENTATION_FAILURE`, not rewritten as PASS.

## Sigma-z crossing lineage

H4 run `33257117162`: fresh targeted class-crossing PASS, 50/50 independently reconstructed physical STABLE -> record UNSTABLE crossings.

H5 run `33263959965`: fresh prospective c3-gate mechanism PASS, 54/54 independently reconstructed crossings and zero mechanism counterexamples.

H9 run `33267026845`: bounded near-pure orientation PASS. In the frozen R4 shell, 33 fresh `x*z<0` c1+c3-admissible cases and 0 matched `x*z>0` cases were found; all 33/33 frozen eligible cases were full STABLE -> UNSTABLE crossings. This is not a universal orientation law.

Exact orientation algebra run `33267107733` proved that orientation sign enters c3 affinely while c1 is orientation-sign independent in the sigma-z representation.

## General planar measurement family

Run `33267236939`: fixed 45-degree measurement-axis stochastic quotient PASS; generic out-of-plane axis correctly refused a 1D dark factor.

Run `33267394149`: `PASS_PLANAR_MEASUREMENT_DARK_BOUNDARY`.

For `n(theta)=(sin(theta),0,cos(theta))`,

`Delta_obs=omega-(gamma/4)sin(2theta)`.

`kappa` cancels exactly. Away from `Delta_obs=0`, the maximal dark factor is exactly `span(e_y)` and the stochastic tangent descends to the 2D quotient. At exact `Delta_obs=0`, dark dimension becomes 2 and the required state is `REFUSE_QUOTIENT_DIMENSION`.

Run `33267544870`: `PASS_PLANAR_QUOTIENT_INVARIANTS`.

In measurement-aligned quotient coordinates `u=n dot (x,z)`, `v=m dot (x,z)`, define

`q=eta*kappa`,
`p=gamma*(1+cos(theta)^2)/2`,
`d=kappa+gamma*(1+sin(theta)^2)/2`,
`h=gamma*sin(2theta)/4`.

Exact canonical matrices:

`A_phys=[[-p,h-omega],[h+omega,-d]]`

`B=-sqrt(2q)*[[2u,0],[v,u]]`

`A_record=A_phys+[[-2q(1-u^2),0],[2quv,0]]`.

The complete separate physical/record `(c1,c2,c3)` triples are exact functions of this canonical quotient. In particular

`c1_phys=3*(p+d)-14*q*u^2`,

`c1_record=3*(p+d)+6*q-20*q*u^2`,

`c1_record-c1_phys=6*q*(1-u^2)`.

## Pure-dephasing transfer: COMPOSITE CLOSED

The distinct dissipation family adds pure-dephasing jump `sqrt(gamma_phi/2)*sigma_z` to amplitude damping.

Define transverse rate

`a=gamma/2+gamma_phi`

and longitudinal rate

`b=gamma`.

The exact structural target is

`Delta_phi=omega-(b-a)sin(theta)cos(theta)`

`=omega-(gamma/2-gamma_phi)sin(theta)cos(theta)`.

The canonical quotient retains the same algebraic form with

`p=a sin(theta)^2+b cos(theta)^2`,
`d=kappa+a cos(theta)^2+b sin(theta)^2`,
`h=(b-a)sin(theta)cos(theta)`.

### Parent v0.1

Run `33267651929`, commit `a70d52eefad4f1a7fade43eda8833297f900fa58`.

Permanent classification: `AUDIT_IMPLEMENTATION_FAILURE / VARIABLE_NAME_COLLISION`.

D0, D1, D2, D4, D5, D6, D7 passed. D5 passed all 256 fresh fixtures with maximum canonical-matrix error `8.881784197001252e-16`, maximum invariant-coefficient error `1.8818280267396403e-14`, and maximum second-moment intertwining error `1.7763568394002505e-15`. Both exact shifted-boundary refusals and the generic out-of-plane refusal passed.

D3 was falsely reported FAIL because the Python boolean name `D3` was later overwritten by the generic-axis empty dark-space NumPy array. This exact failure is preserved in
`stability_arc/measurement_conditioned/dephasing_augmented_v01/FAILURE_SIGNAL_REPORT_v0.1.md`.

### Independent v0.1.1 remediation

Run `33267776394`, commit `faed26482ab622dcbfd617fb1bc92feba8260783`.

Status: `PASS_D3_IDENTIFIER_REMEDIATION`.

All M0-M5 gates passed. All twelve physical/stochastic/same-record canonical-map residuals simplified exactly to zero using distinct non-reused identifiers. The parent is not rewritten.

Canonical remediation result:
`stability_arc/measurement_conditioned/dephasing_augmented_v011/D3_IDENTIFIER_REMEDIATION_RESULT_v0.1.1.md`.

The dephasing-augmented structural transfer is therefore **composite-closed only through the explicit parent-failure + remediation lineage**.

## ACTIVE: fresh dephasing-family crossing transfer

Live run: `33268037434`
Workflow: `Stability Arc dephasing crossing transfer v0.1`
Execution commit: `b2f27ace91e7c6ffb70bbf1211e7de66e5fc3669`

Preregistration:
`stability_arc/measurement_conditioned/dephasing_crossing_v01/PREREGISTRATION_DEPHASING_CROSSING_TRANSFER_v0.1.md`.

Fresh seed `2026082920` generates exactly 1,200,000 new dephasing-augmented planar inputs, 300000 in each of four equal-allocation radial strata:

- S1 `[0.05,0.50)`;
- S2 `[0.50,0.90)`;
- S3 `[0.90,0.98)`;
- S4 `[0.98,0.9999)`.

The panel spans all planar measurement angles and broad positive `gamma`, `gamma_phi`, `kappa`, `eta`, and `omega`. It is not targeted to any old sigma-z crossing pocket.

### Stage A firewall

Before full reveal, the code may use only:

- structural `Delta_phi`;
- exact dephasing canonical `c1_phys/c1_record`;
- exact dephasing canonical `c3_phys/c3_record`.

No second-moment matrix `G`, c2, final Hurwitz margin, eigenvalue, or full stability class may enter selection.

It freezes and hashes up to 128 cases in each class:

- `D_C13`: physical c1 positive, physical c3 positive, record c3 negative;
- `S_C13`: record c1 positive, physical c3 negative, record c3 positive.

At least 16 cases are required to score each direction.

### Stage B

Only after Stage-A bytes and SHA-256 verify, every frozen case is independently reconstructed from the full Hilbert-space amplitude-damping + pure-dephasing + planar-measurement generator. Hidden `m2` and `mh` are then revealed.

Registered hypotheses are scored separately:

- H10D: every scored `D_C13` is full physical STABLE -> record UNSTABLE;
- H10S: every scored `S_C13` is full physical UNSTABLE -> record STABLE.

A single robust counterexample fails its direction and is preserved. Hidden `m2`/`mh` blockers may explain failure but may not be added to H10 after outcome exposure.

## Current blockers

- GFSA external numerical admission: authentic frozen v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the active H10 dephasing crossing test.

## User action

None currently required.
