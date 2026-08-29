# Prospective c3 displacement-map full-class validation v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** FRESH_PROSPECTIVE_MAP_SUFFICIENCY_TEST

## Purpose

The exact channel-specific `c3` quadratics and set-valued displacement map are now available through an explicit composite lineage. This phase tests a stronger question that has not yet been answered:

> Is c3 sign displacement alone sufficient to predict the complete four-gate mean-square stability-class displacement on fresh measured-qubit cases?

This is deliberately adversarial. A single robust counterexample falsifies sufficiency. A failure does not invalidate the c3 boundary map; it means another Routh-Hurwitz margin is also required as an admissibility coordinate.

No H3, H4, H5, localization, collapse, measurement-quality, or GFSA external-candidate outcome may be used to select cases, thresholds, signs, or exclusions.

## Frozen fresh generator

Use exactly NumPy `default_rng(seed=2026082909)` and generate exactly `250000` candidates `MV000001...MV250000`.

Fix `gamma=1` and draw independently:

- `log10(kappa/gamma) ~ Uniform(log10(0.2), log10(100))`;
- `eta ~ Uniform(0.001,0.95)`;
- `r ~ Uniform(0.05,0.98)`;
- `theta ~ Uniform(0,2*pi)`;
- `log10(omega/gamma) ~ Uniform(-3,3)`.

Set

- `x=r*cos(theta)`;
- `z=r*sin(theta)`;
- `q=eta*kappa`.

No candidate may be replaced or regenerated because of any c3 or full-stability result.

## Stage A: c3 map only

Stage A may evaluate only the already-closed exact c3 quadratics

`c3_p(omega)` and `c3_r(omega)`.

For each channel define

`scale=max(1, |A| omega^2 + |B| omega + |C|)`

and normalized c3 sign coordinate

`s=c3/scale`.

Use frozen robust map-sign threshold

`MAP_TOL=1e-8`.

Classify:

- `I_destab` if `s_p > +MAP_TOL` and `s_r < -MAP_TOL`;
- `I_stab` if `s_p < -MAP_TOL` and `s_r > +MAP_TOL`;
- otherwise not selected for the sufficiency test.

Stage A must not construct any 2x2 drift/noise matrix, 3x3 second-moment generator, eigenvalue, or non-c3 Routh-Hurwitz coefficient.

Freeze the first `512` candidates in candidate-ID order from each map class. If either class has fewer than `128` candidates, return `SELECTION_HOLD`.

Before Stage B, write the selected IDs, complete input parameters, normalized c3 signs, generator seed, candidate-array SHA-256, and selection SHA-256 to `stageA_c3_map_selection.json`. Re-read the file and verify its digest before any full generator is constructed.

## Stage B: full mean-square reveal

For exactly the immutable Stage-A selections, independently construct the physical and same-record active matrices

`A_p=[[-(gamma/2+kappa),omega],[-omega,-gamma]]`,

`B=[[-sqrt(2q) z,-sqrt(2q) x],[0,-2 sqrt(2q) z]]`,

`A_r=A_p+[[0,2qzx],[0,-2q(1-z^2)]]`.

Construct the real symmetric second-moment generator from

`dP/dt=A P + P A^T + B P B^T`.

For

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`, define

`R=gamma+kappa+omega+q`

and normalized margins

`m1=c1/R`,
`m2=c2/R^2`,
`m3=c3/R^3`,
`mh=(c1*c2-c3)/R^3`.

Use frozen full-class threshold

`RH_TOL=1e-9`.

A channel is:

- `STABLE` iff all four margins are `> +RH_TOL`;
- `UNSTABLE` iff at least one margin is `< -RH_TOL`;
- `BOUNDARY` otherwise.

Stage B must independently verify direct-generator `c3=-det(G)` against the Stage-A exact c3 polynomial to relative-or-absolute tolerance `2e-10`. A mismatch is `RECONSTRUCTION_HOLD`.

## Registered H6 sufficiency hypothesis

For every robust Stage-A `I_destab` case:

`physical STABLE -> record UNSTABLE`.

For every robust Stage-A `I_stab` case:

`physical UNSTABLE -> record STABLE`.

A single robust full-class counterexample falsifies H6.

This is intentionally stronger than the current licensed statement. The map is allowed to fail this test.

## Failure decomposition

If H6 fails, preserve every counterexample. Without changing H6, report which non-c3 margins block the predicted class:

- physical `m1`, `m2`, or `mh` for failed `I_destab` predictions;
- record `m1`, `m2`, or `mh` for failed `I_stab` predictions;
- multiple blockers when applicable.

These decompositions are hypothesis-generation only for a successor phase and may not rescue H6.

## Frozen gates

- **V0 generator determinism:** exact regeneration of the 250000 candidate-array SHA-256.
- **V1 Stage-A freeze:** at least 128 candidates in each map class; first 512 by ID frozen before Stage B; selection digest verifies exactly.
- **V2 map replay:** every selected case independently re-evaluates to its frozen c3 map class using only the exact quadratic.
- **V3 full-generator reconstruction:** direct `c3=-det(G)` agrees with the frozen exact c3 value within `2e-10` for both channels on every selected case.
- **V4 full-class robustness:** no selected channel is `BOUNDARY` under `RH_TOL`; otherwise `BOUNDARY_HOLD`.
- **V5 H6 sufficiency:** zero full-class counterexamples in both classes.
- **V6 controls:** fixed eta-zero physical/record identity control and fixed synthetic cubic classifier controls pass.

## Decision rule

- `PASS_C3_MAP_FULL_CLASS_H6` only if V0-V6 pass and both map classes contain at least 128 frozen cases;
- `FAIL_C3_MAP_FULL_CLASS_H6` if V0-V3 and V6 pass, no selected channel is boundary, and at least one full-class counterexample exists;
- `BOUNDARY_HOLD` if any selected case is numerically boundary-classed under the frozen full-class threshold;
- `SELECTION_HOLD` if either map class has fewer than 128 fresh candidates;
- `RECONSTRUCTION_HOLD` if direct c3 reconstruction fails;
- `AUDIT_FAILURE` for other mechanical/audit failures.

## Interpretation firewall

A PASS would establish c3 displacement as a sufficient full-class predictor only within this exact fresh sampling frame and measured-qubit model. It would not prove universality or license a stochastic scalar.

A FAIL would be scientifically useful: the exact c3 map would remain valid as a boundary coordinate, while the preserved counterexamples would identify which additional Routh-Hurwitz margins are required to form a complete joint stability map.

Physical and same-record channels remain separately recoverable throughout.
