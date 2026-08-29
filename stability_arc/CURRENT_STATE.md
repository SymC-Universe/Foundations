# Stability Arc current state

Last updated: 2026-08-29
Canonical repository: `SymC-Universe/Foundations`
Canonical working branch: `agent/stability-arc-gfsa-v072`

## Active controls

- `stability_arc/gfsa_v0.7.2/ANTI_CIRCULARITY_GUARD_v0.1.md`
- `stability_arc/CONTINUITY_AND_FAILURE_SIGNAL_PROTOCOL_v0.1.md`
- `stability_arc/HISTORICAL_FAILURE_SIGNAL_RECOVERY_v0.1.md`
- `stability_arc/gfsa_v0.7.2/PROVENANCE_RECOVERY_SEARCH_LOG_v0.1.md`
- `stability_arc/gfsa_v0.7.2/external_admission/v0.7/RECOVERY_TARGETS_v0.1.json`

Frozen science, preregistrations, thresholds, exclusions, failure records, and interpretation firewalls remain controlling. FAIL, HOLD, null, NONIDENTIFIABLE, and REFUSE are admissible evidence and may not be repaired by retuning against outcomes.

## GFSA v0.7.2 closed state

- executable package validation: PASS;
- C18 calibration validity: PASS;
- OBS18 interface admissibility: PASS;
- OBS19 blind holdout: PASS;
- external interface: `LICENSED_FOR_EXTERNAL_NUMERICAL_ADMISSION`;
- observable-only EP firewall: PASS.

The GFSA external numerical-admission lane remains quarantined because the exact authentic frozen v0.7 external-candidate contract and authoritative candidate-source package have not been recovered. Candidate response values must not be inspected, plotted, summarized, filtered, or scored until that contract is recovered, persisted, hashed, chronology-authenticated, and bound.

## Measurement-conditioned lineage

### Preserved failures

- joint-channel representation v0.1, run `33234191815`: **FAIL**, permanently preserved. It exposed an incorrect measurement-dissipator normalization, missing stochastic amplitude, and partial self-certification.
- generalized conditioning spectral-abscissa H2, run `33256389876`: **FAIL_GENERALIZED_H2**, permanently preserved and described below.

Failures are not superseded by later corrective or narrower PASS results.

### Closed constructive phases

1. conditional tangent derivation v0.1: PASS;
2. corrective joint-channel representation v0.2: PASS;
3. stochastic second-moment lift v0.1: PASS;
4. information-rank secular bridge v0.1: PASS;
5. secular continuation / mode correspondence v0.1: PASS_WITH_ALL_FRESH_PATHS_ADMISSIBLE;
6. conditioning-dark / active-sector factorization v0.1: PASS;
7. deterministic active-quotient scalar admissibility v0.1: PASS;
8. stochastic dark/active compatibility v0.1: PASS;
9. mean-square stability geometry v0.1: PASS;
10. bounded prospective conditioning directionality H1 v0.1: PASS_PROSPECTIVE_H1 on 24/24 fresh registered fixtures.

The physical same-noise and same-record inference channels remain separately auditable throughout. Joint/conglomerate analysis is licensed only when the channel identities remain recoverable.

## Current licensed representation hierarchy

For an admitted measured-qubit control:

1. separate local tangent generators are retained as `A_phys` and `A_rec`;
2. conditioning enters the deterministic drift by a low-rank bridge `DeltaA=A_rec-A_phys`;
3. the maximal conditioning-dark factor is reconstructed outcome-free from the physical generator and measurement functional;
4. on admitted controls, the full local multiplicative-noise SDE descends exactly to a 2D active quotient
   `dq = A_A q dt + B_A q dW`;
5. deterministic `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` is licensed separately for physical and record channels only when the deterministic 2D scalar-admissibility conditions pass;
6. the stochastic pair `(A_A,B_A)` is **not** compressed to a scalar;
7. its symmetric second moment is governed by a real 3x3 generator `G(A_A,B_A)` with coordinate-invariant cubic coefficients `(c1,c2,c3)`;
8. strict mean-square asymptotic stability uses the cubic Routh-Hurwitz conditions
   `c1>0`, `c2>0`, `c3>0`, `c1*c2>c3`.

Required stochastic reporting state remains:

`MEAN_SQUARE_INVARIANTS_REQUIRED`.

## Mean-square geometry result

Canonical run `33256099802`: PASS.
Canonical result:
`stability_arc/measurement_conditioned/mean_square_geometry_v01/MEAN_SQUARE_STABILITY_GEOMETRY_RESULT_v0.1.md`

The noiseless oscillator controls separated two different notions of boundary:

- `chi=0.5`: mean-square STABLE;
- `chi=1`: mean-square STABLE;
- `chi=1.5`: mean-square STABLE;
- `Gamma=0`: mean-square BOUNDARY.

Therefore deterministic critical damping at `chi=1` is a repeated-root/damping-morphology boundary, not the mean-square asymptotic-stability boundary. The two coordinates answer different questions and may not be conflated.

## Bounded prospective H1 result

Canonical run `33256215609`: `PASS_PROSPECTIVE_H1`.
Canonical result:
`stability_arc/measurement_conditioned/conditioning_directionality_v01/CONDITIONING_MEAN_SQUARE_DIRECTIONALITY_RESULT_v0.1.md`

The preregistered 24-fixture sample had 24/24 admitted fixtures satisfying

`alpha_rec <= alpha_phys + 1e-10`,

where `alpha=max Re eig(G)`.

This remains valid as a bounded prospective result inside that exact registered sample. It was never licensed as universal.

## Generalized H2 stress failure

Canonical run: `33256389876`
Execution commit: `ba9d07b10e5828867c720f213d488146cb999ff0`
Canonical preserved result and failure analysis:
`stability_arc/measurement_conditioned/conditioning_structural_stress_v01/CONDITIONING_STRUCTURAL_STRESS_RESULT_v0.1.md`

Artifact ID: `9715934331`
Artifact ZIP SHA-256: `a14675b7957776cb552f94a14b1345361b6b0a018ee4466a82594e05978323eb`

Preregistered gates:

- S0 structural identity: PASS;
- S1 4096-case seeded generator determinism: PASS;
- S2 admission: PASS, `4096/4096` seeded plus `16/16` corners;
- S3 second-moment audit: PASS;
- S4 adversarial comparator: PASS;
- S5 generalized H2: **FAIL**, 441 counterexamples.

Permanent phase status:

`FAIL_GENERALIZED_H2`.

### Signal extracted without rescuing H2

Of 4112 admitted stress/corner cases:

- `3146` physical STABLE -> record STABLE;
- `584` physical UNSTABLE -> record STABLE;
- `382` physical UNSTABLE -> record UNSTABLE;
- `0` physical STABLE -> record UNSTABLE.

Among the 441 H2 counterexamples, 440 were STABLE -> STABLE and one was UNSTABLE -> UNSTABLE. Thus H2 usually failed because the spectral decay rate became less negative, not because mean-square stability was lost.

For all 440 stable H2 counterexamples, every cubic Routh-Hurwitz margin increased even while the spectral abscissa became less negative. This demonstrates that stability margin and decay-rate ordering are not one-dimensional in this stochastic joint representation.

### Post-hoc failure localization

The following is discovery only and does not count as confirmation.

All 439 seeded H2 counterexamples satisfied

`omega + kappa < gamma/2`.

On the low-kappa active branch, with

`delta = gamma/2-kappa`,

the deterministic repeated-root condition is

`delta = 2 omega`.

`421/439` seeded counterexamples were on the deterministic active `chi_active>1` side; the remaining 18 were close to the boundary on the opposite side. `312/439` had `x*z<0`.

A post-hoc weak-measurement perturbative derivation gives

`S = -(1-z^2) + ((1-z^2)*delta - 2*omega*x*z)/sqrt(delta^2-4*omega^2)`

and predicts

`(alpha_rec-alpha_phys)/q -> 2*S`, `q=eta*kappa`,

on the low-kappa overdamped branch away from the repeated-root singularity.

On the exposed stress data this post-hoc predictor localized most counterexamples, but those checks are discovery evidence only. They generated the next fresh preregistered test.

## ACTIVE: prospective failure-mechanism test v0.1

Live workflow:

- run `33256684197`;
- workflow `Stability Arc conditioning failure mechanism v0.1`;
- head commit `1574ca67fd37e7ded46a886b8056cbbfac9bce8f`.

Preregistration:
`stability_arc/measurement_conditioned/conditioning_failure_mechanism_v01/PREREGISTRATION_CONDITIONING_FAILURE_MECHANISM_v0.1.md`

This uses fresh seed `2026082903` and an outcome-free balanced panel of 64 analytic `S>=+0.10` fixtures plus 64 `S<=-0.10` fixtures, all safely on the low-kappa overdamped branch away from the repeated-root singularity. Each is evaluated at `eta={1e-3,1e-4,1e-5}`.

It prospectively tests:

1. sign of `alpha_rec-alpha_phys` against sign of `S`;
2. convergence of `(alpha_rec-alpha_phys)/q` to `2*S`;
3. first-order magnitude accuracy as `q -> 0`.

No parameter, acceptance rule, sign threshold, magnitude threshold, or eta level may change after outcome exposure. A failure becomes the next mechanism-boundary signal.

## Post-hoc class-monotonicity candidate

The H2 stress result observed no STABLE -> UNSTABLE transitions and 584 UNSTABLE -> STABLE transitions. This was not preregistered and is not promoted.

It may become a future fresh prospective hypothesis or symbolic proof target after the current failure-mechanism test. It may not be treated as established from the H2 stress data alone.

## QuTiP state

QuTiP 5.3.1 runtime admission remains `RUNTIME_ADMITTED`.

Historical v0.6 notebook reproduction remains open. Expected historical notebook SHA-256:
`be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

Runtime admission is not a substitute for authentic notebook recovery/reproduction.

## Anti-circularity state

- the 24/24 H1 support remains bounded to its original sample;
- generalized H2 remains failed despite the earlier H1 pass;
- all 441 H2 counterexamples are retained;
- the perturbative mechanism is explicitly post-hoc until the fresh run resolves it;
- same-noise and same-record channels remain separate inside all joint analysis;
- no stochastic scalar is licensed;
- no localization outcome has been used to choose the measurement-conditioned representations, failure wedge, or current mechanism panel;
- GFSA external candidate values remain sealed.

## Current blockers

- GFSA external numerical admission: exact frozen v0.7 contract/source package absent;
- historical QuTiP comparison: authentic original notebook/source absent;
- historical Phase 4A: PENDING/INCOMPLETE.

None blocks the active fresh failure-mechanism test.

## Queue

### COMPLETED

- stochastic active quotient closure;
- mean-square 3x3 invariant geometry;
- bounded 24-case prospective H1 PASS;
- broad 4112-case generalized H2 falsification;
- full preservation and post-hoc investigation of the H2 failure.

### ACTIVE

- run `33256684197`: prospective weak-measurement mechanism falsification/validation.

### NEXT

- if mechanism PASS: preserve it as a bounded mechanistic closure, then preregister an adversarial class-monotonicity test or attempt a symbolic sufficient-condition proof;
- if mechanism FAIL: retain the failure and investigate the mismatch region before any new hypothesis;
- independently continue authentic v0.7 contract and historical QuTiP-source recovery when durable source material becomes available.

## User action

None currently required.
