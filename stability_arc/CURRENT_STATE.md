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

## Measurement-conditioned architecture closed so far

Where the maximal conditioning-dark factor is exactly one-dimensional, the full stochastic tangent SDE admits an exact two-dimensional active quotient. The stochastic quotient remains a matrix pair `(A_A,B_A)` and is not compressed to a scalar.

Mean-square stability is governed by the real 3x3 symmetric second-moment generator `G`. With

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`,

strict mean-square asymptotic stability requires

`c1>0`, `c2>0`, `c3>0`, and `c1*c2>c3`.

Required stochastic report remains `MEAN_SQUARE_INVARIANTS_REQUIRED`.

The same-noise physical tangent and same-record inference tangent are kept separately auditable while joint/comparative structure is studied. No scalar compression is licensed merely from coexistence of the two channels.

## Important preserved failures / non-closures

- joint representation v0.1: permanent mathematical/specification FAIL;
- generalized spectral-abscissa H2: permanent FAIL with 441 counterexamples;
- c3 displacement v0.1: permanent binary64 numerical-oracle D3 FAIL; independent high-precision remediation later passed under the unchanged tolerance;
- H6 c3-only full-class sufficiency: permanent scientific FAIL;
- H7 c1-corrected broad-frame test: `SELECTION_HOLD`;
- H8 high-radius existence threshold: FAIL; H8F sufficiency: INSUFFICIENT;
- dephasing-augmented structural-transfer parent run `33267651929`: permanent `AUDIT_IMPLEMENTATION_FAILURE / VARIABLE_NAME_COLLISION`, not rewritten as PASS.

Every failure above remains part of the evidentiary record.

## Sigma-z and planar lineage

H4 run `33257117162`: fresh targeted class-crossing PASS, 50/50 independently reconstructed physical STABLE -> record UNSTABLE crossings.

H5 run `33263959965`: fresh prospective c3-gate mechanism PASS, 54/54 independently reconstructed crossings and zero mechanism counterexamples.

H9 run `33267026845`: bounded near-pure orientation PASS. In the frozen R4 shell, 33 fresh `x*z<0` c1+c3-admissible cases and 0 matched `x*z>0` cases were found; all 33/33 frozen eligible cases were full STABLE -> UNSTABLE crossings. This is not a universal orientation law.

Exact orientation algebra run `33267107733` proved that orientation sign enters c3 affinely while c1 is orientation-sign independent in the sigma-z representation.

Run `33267236939`: fixed 45-degree measurement-axis stochastic quotient PASS; generic out-of-plane axis correctly refused a 1D dark factor.

Run `33267394149`: `PASS_PLANAR_MEASUREMENT_DARK_BOUNDARY` with exact

`Delta_obs=omega-(gamma/4)sin(2theta)`.

Away from `Delta_obs=0`, the maximal dark factor is exactly `span(e_y)` and the stochastic tangent descends to the 2D quotient. At exact `Delta_obs=0`, dark dimension becomes 2 and the required state is `REFUSE_QUOTIENT_DIMENSION`.

Run `33267544870`: `PASS_PLANAR_QUOTIENT_INVARIANTS`, including the complete separate physical/record `(c1,c2,c3)` triples in measurement-aligned quotient coordinates.

## Pure-dephasing structural transfer: COMPOSITE CLOSED

The distinct dissipation family adds pure-dephasing jump `sqrt(gamma_phi/2)*sigma_z` to amplitude damping.

Define

`a=gamma/2+gamma_phi`,
`b=gamma`,

and

`Delta_phi=omega-(b-a)sin(theta)cos(theta)`.

The canonical quotient retains the same algebraic form with

`p=a sin(theta)^2+b cos(theta)^2`,
`d=kappa+a cos(theta)^2+b sin(theta)^2`,
`h=(b-a)sin(theta)cos(theta)`.

Parent run `33267651929` remains permanently classified `AUDIT_IMPLEMENTATION_FAILURE / VARIABLE_NAME_COLLISION`. Independent remediation run `33267776394` is `PASS_D3_IDENTIFIER_REMEDIATION`. The structural transfer is therefore composite-closed only through the explicit parent-failure + remediation lineage.

## Dephasing crossing transfer and replication

H10 run `33267893712`:

- all audit gates X0-X5 PASS;
- stabilizing direction H10S: `PASS_H10S`, 128/128 fresh frozen cases, zero counterexamples;
- destabilizing direction H10D: `SELECTION_HOLD_D`, because the broad 1.2M panel produced only 2 D-side eligible cases; both were correct but below the preregistered minimum 16.

H11 Stage-A run `33269021023` was a post-H10 availability recovery only, not confirmatory evidence. It generated exactly 10,000,000 fresh S3/S4 cases, found 69 D-side eligible cases, froze the first 64 before hidden full stability, and bound selection SHA-256
`f0f266117f5f86ee6cf9e86667a73f4412844c2555a4fa0c81250f40978d80dc`.

H11 blind reveal run `33269087712`: `PASS_H11D_BLIND_REVEAL`.

- immutable cases scored: 64
- physical STABLE -> same-record UNSTABLE: 64/64
- counterexamples: 0
- boundary cases: 0
- reconstruction failures: 0
- hidden physical m2/mh blockers: 0

H12 was the preregistered one-time same-family untouched-seed replication.

H12 Stage-A run `33269142763`:

- replication seed: `2026082922`
- fresh generated cases: `10,000,000`
- S3 eligible: 6
- S4 eligible: 65
- total eligible: 71
- frozen before reveal: first 64
- hidden full stability computed in Stage A: no
- selection SHA-256: `364ba6a18b5ea8b8cad7a164028013bf605db5a44f847bcc9e1d13dfacb46de5`
- status: `READY_FOR_BLIND_REVEAL_H12`

Canonical Stage-A result:
`stability_arc/measurement_conditioned/dephasing_d_replication_v01/DEPHASING_D_REPLICATION_STAGEA_RESULT_v0.1.md`.

H12 blind reveal run `33278587821`:

**Status: `PASS_H12D_REPLICATION`**

- immutable cases scored: 64
- physical STABLE -> same-record UNSTABLE: 64/64
- counterexamples: 0
- boundary cases: 0
- reconstruction failures: 0
- hidden physical m2 blockers: 0
- hidden physical mh blockers: 0
- maximum c1/c3 reconstruction error: `8.962889729849714e-14`
- maximum quotient-matrix error: `1.7763568394002505e-15`
- maximum moment-intertwining error: `1.7763568394002505e-15`
- reveal artifact: `9722269776`
- reveal artifact ZIP SHA-256: `4b13b336b9b9bfe21b23f5a18e03e470a8bb18e7b4faf69bd183fae49558ceef`

Canonical reveal result:
`stability_arc/measurement_conditioned/dephasing_d_replication_reveal_v01/DEPHASING_D_REPLICATION_BLIND_REVEAL_RESULT_v0.1.md`.

H11 and H12 therefore provide two separately frozen 64-case blind reveals with zero counterexamples in the bounded targeted dephasing D-side family. This does not license a universal destabilization law, universal radius/orientation rule, or scalar chi.

## ACTIVE FRONTIER: BRAINSTORMING / DECISION REQUIRED

The planned same-family compute sequence is complete. Further repeats of the same targeted dephasing family are not justified merely to increase sample size.

A repository search after H12 found no already-frozen independent successor based on a different generator/dissipation family. The next scientific calculation must therefore begin with an explicit design choice for a genuinely independent physical extension before any outcomes are generated.

Candidate design space may include a new dissipation/generator family, a measurement geometry that does not retain the current one-dimensional dark factor, or another independent physical realization. No candidate is frozen or promoted by this state file.

Until that choice is made, do not launch additional same-family outcome calculations.

## Current blockers

- GFSA external numerical admission: authentic frozen v0.7 contract/source package absent;
- historical QuTiP reproduction: authentic source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

These do not invalidate the closed H12 result but remain open project items.

## User action

Scientific design discussion is now required to choose the next genuinely independent measurement-conditioned test family. No repository/mechanical action is required from the user.
