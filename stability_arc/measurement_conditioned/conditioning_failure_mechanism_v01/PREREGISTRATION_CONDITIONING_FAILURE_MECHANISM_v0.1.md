# Prospective conditioning spectral-abscissa failure-mechanism test v0.1

**Status:** FROZEN BEFORE EXECUTION
**Lineage:** `FAIL_GENERALIZED_H2` -> post-hoc perturbative derivation -> fresh prospective test

## Purpose

The broad structural stress phase permanently falsified generalized H2: same-record conditioning does not monotonically improve the mean-square spectral abscissa across the full tested measured-qubit family.

Post-hoc analysis localized most counterexamples near the low-kappa branch of the deterministic active repeated-root geometry and derived a weak-measurement perturbative sign/magnitude formula. Those observations are discovery evidence only.

This phase prospectively tests that derived mechanism on a new seed and fresh fixtures. No fixture or threshold is chosen from the outcomes of this phase.

## Exact active drift notation

For the measured-qubit active `(x,z)` quotient define

`a = gamma/2 + kappa`,
`delta = gamma-a = gamma/2-kappa`,
`q = eta*kappa`.

The physical deterministic active drift is

`A_phys = [[-a, omega],[-omega,-gamma]]`.

The same-record deterministic correction is

`DeltaA = [[0, 2*q*z*x],[0,-2*q*(1-z^2)]]`.

The multiplicative-noise active matrix is common to both channels:

`B = [[-sqrt(2q)*z,-sqrt(2q)*x],[0,-2*sqrt(2q)*z]]`.

## Frozen perturbative prediction

On the low-kappa overdamped branch

`delta>0`,
`D = delta^2 - 4*omega^2 > 0`,

the slow deterministic active eigenvalue is

`lambda_s = -(a+gamma)/2 + sqrt(D)/2`.

Differentiation of the same-record drift at `q=0` gives

`S = -(1-z^2) + ((1-z^2)*delta - 2*omega*x*z)/sqrt(D)`.

For the leading deterministic second-moment mode the registered weak-measurement prediction is

`(alpha_rec-alpha_phys)/q -> 2*S`

as `q -> 0`, where `alpha=max Re eig(G)` for the symmetric second-moment generator.

This is the mechanism under test.

## Fresh balanced fixture generator

Use exactly NumPy `default_rng(seed=2026082903)`.

Generate candidate base fixtures in order with:

- `log10(gamma) ~ Uniform(-1,0.5)`;
- `r_k = kappa/gamma ~ Uniform(0.02,0.35)`;
- `delta = gamma*(0.5-r_k)`;
- repeated-root ratio `rho = 2*omega/delta ~ Uniform(0.20,0.80)`;
- therefore `omega = rho*delta/2`;
- draw a standard-normal 3D direction and normalize it;
- draw state radius `r ~ Uniform(0.20,0.95)` and set the Bloch vector to `r*direction`.

Compute `S` from these **input parameters only**, before any same-record outcome is evaluated.

Accept candidates in generation order until there are exactly:

- 64 fixtures with `S >= +0.10`, labeled `P001...P064`;
- 64 fixtures with `S <= -0.10`, labeled `N001...N064`.

Candidates with `|S|<0.10` are preserved in the generator count but are not admitted to the balanced mechanism panel because their first-order sign is intentionally near zero. This is selection on the frozen analytic predictor, not on an observed response.

Abort with `GENERATOR_HOLD` if either group is not filled within 100000 candidates. No outcome-based replacement is allowed.

## Measurement-strength ladder

For every accepted base fixture run exactly

`eta in {1e-3, 1e-4, 1e-5}`

with the same `gamma,kappa,omega` and Bloch state.

Thus `q=eta*kappa` approaches zero while the deterministic active repeated-root geometry remains fixed.

## Independent reconstruction

At every eta level independently reconstruct the full Hilbert-space physical and same-record tangent matrices and the stochastic tangent matrix, recover the conditioning-dark factor, and form the exact 2D active quotient.

Admission requires:

- positive density matrix;
- one-dimensional dark factor and two-dimensional active quotient;
- dark/invariance/intertwining residuals `<=5e-10`;
- direct symmetric second-moment generator agrees with the Kronecker/duplication lift to `<=5e-12`.

Any refused accepted fixture makes the phase `QUOTIENT_HOLD`; no replacement occurs.

## Registered outputs

For each accepted base fixture and eta level record

- `alpha_phys`;
- `alpha_rec`;
- `delta_alpha`;
- `slope = delta_alpha/q`;
- registered predictor `2*S`;
- absolute slope residual `|slope-2*S|`;
- sign agreement.

The physical and same-record channels remain separately recorded.

## Prospective hypotheses

### P1 sign mechanism

At the finest registered level `eta=1e-5`, every accepted fixture must satisfy

`sign(delta_alpha) = sign(S)`.

Because accepted fixtures have `|S|>=0.10`, no zero-sign ambiguity is licensed.

One sign mismatch makes P1 fail.

### P2 first-order magnitude

At `eta=1e-5`, every accepted fixture must satisfy

`|delta_alpha/q - 2*S| <= 0.01`.

One violation makes P2 fail.

### P3 asymptotic convergence

For each sign group separately, the median absolute slope residual must decrease strictly along

`eta=1e-3 -> 1e-4 -> 1e-5`.

The finest-level median residual for each sign group must also be `<=1e-3`.

## Frozen gates

- **F0 deterministic generation:** the base panel regenerates byte-equivalently in-process and contains exactly 64 positive-S plus 64 negative-S fixtures.
- **F1 geometry admission:** all 128 accepted fixtures pass quotient admission at all three eta levels.
- **F2 implementation consistency:** every active second-moment generator passes the direct-vs-Kronecker lift gate.
- **F3 P1 sign mechanism:** all 128 finest-level signs agree with the preregistered `S` sign.
- **F4 P2 magnitude:** all 128 finest-level slope residuals are `<=0.01`.
- **F5 P3 convergence:** both sign groups have strictly decreasing median residuals across the three eta levels and finest medians `<=1e-3`.

Overall status:

- `PASS_PROSPECTIVE_FAILURE_MECHANISM` if F0-F5 pass;
- `FAIL_PROSPECTIVE_FAILURE_MECHANISM` if F0-F2 pass and any of F3-F5 fail;
- `GENERATOR_HOLD` or `QUOTIENT_HOLD` as defined above;
- `AUDIT_FAILURE` for other implementation/provenance failures.

## Interpretation firewall

A PASS would prospectively validate the weak-measurement perturbative mechanism only in the registered low-kappa overdamped panel away from the repeated-root singularity.

It would explain why conditioning can make the spectral abscissa less negative even while stability is retained. It would not restore generalized H2.

A PASS would not establish:

- universal class monotonicity;
- a stochastic scalar chi;
- localization, collapse, or measurement-quality prediction;
- that the repeated-root coordinate alone determines the sign.

A FAIL remains a failure and becomes the next mechanism-boundary investigation target.
