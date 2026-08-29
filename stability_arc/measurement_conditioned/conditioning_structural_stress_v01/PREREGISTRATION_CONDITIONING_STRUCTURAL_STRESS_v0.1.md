# Conditioning structural monotonicity stress audit v0.1

**Status:** FROZEN BEFORE EXECUTION
**Lineage:** PASS_PROSPECTIVE_H1 in a bounded 24-fixture sample -> broader structural/adversarial test

## Purpose

The prior prospective phase supported, within its preregistered parameter box, the statement that same-record conditioning did not worsen the mean-square spectral abscissa on 24/24 fresh admitted fixtures.

That result is not a universal theorem and is not reused as fresh evidence here.

This phase asks two harder questions:

1. does the exact measured-qubit algebra imply a simple low-rank/nonpositive conditioning correction at the mean-square-generator level?
2. does the observed directionality survive a deliberately much broader, boundary-seeking parameter domain?

A single admitted counterexample to the broadened directionality claim is scientifically meaningful and makes the generalized hypothesis fail.

No localization, collapse, measurement-quality, GFSA external-candidate, or historical Stability Arc outcome may be used by this phase.

## Exact model family

Measured qubit with

- measured operator `x_op=sigma_z/2`;
- Hamiltonian `H=omega sigma_y/2`;
- amplitude-damping collapse amplitude `sqrt(gamma)`;
- unconditional measurement backaction `2 kappa D[x_op]`;
- efficiency `eta`.

Let Bloch coordinates be `(x,y,z)` and define

`q = eta*kappa`,
`a = gamma/2 + kappa`,
`s = sqrt(2q)`.

For the exact deterministic conditioning-dark factor, the active quotient is the `(x,z)` plane whenever the frozen quotient-admission rules accept it.

## Frozen structural identities

The active physical drift is registered as

`A_phys = [[-a, omega],[-omega,-gamma]]`.

The active multiplicative tangent matrix is

`B = [[-s*z,-s*x],[0,-2*s*z]]`.

The same-record correction is

`DeltaA = A_rec-A_phys = [[0,2*q*z*x],[0,-2*q*(1-z^2)]]`.

For symmetric second-moment coordinates `m=(p11,p12,p22)^T`, let `G(A,B)` satisfy

`dm/dt = G(A,B)m`.

The registered exact correction is

`DeltaG = G(A_rec,B)-G(A_phys,B)`

with

`DeltaG = [[0,4*q*x*z,0],
           [0,-2*q*(1-z^2),2*q*x*z],
           [0,0,-4*q*(1-z^2)]]`.

Therefore its registered characteristic polynomial is

`lambda * (lambda + 2*q*(1-z^2)) * (lambda + 4*q*(1-z^2))`.

For physical Bloch states `|z|<1`, `eta>=0`, and `kappa>=0`, the correction's own eigenvalues are nonpositive.

This statement concerns `DeltaG` itself. It does **not** by itself imply monotonicity of the spectral abscissa of `G_phys + DeltaG`, because the full generators may be nonnormal.

## Structural hypothesis S0

Independent full Hilbert-space reconstruction and independent second-moment lifting must reproduce all registered active formulas above to absolute tolerance `2e-10` on every admitted numerical fixture.

Additionally, a fixed symbolic check using SymPy must simplify the direct algebraic `DeltaG` to the registered formula and its characteristic polynomial to the registered factorization exactly.

A failure of S0 is an `AUDIT_FAILURE`, not a directional result.

## Generalized prospective hypothesis H2

For **every admitted fixture in the frozen broad stress set**,

`alpha_rec <= alpha_phys + 1e-9`,

where `alpha=max Re eig(G)`.

A single admitted case with

`alpha_rec > alpha_phys + 1e-9`

makes H2 `FAIL_GENERALIZED_H2`.

No majority rule, quantile rule, outlier deletion, or retuning is permitted.

## Frozen broad stress generator

Use exactly NumPy `default_rng(seed=2026082902)`.

Generate 4096 candidates, IDs `BS0001` through `BS4096`, with no post-outcome replacement.

For every candidate draw:

- `eta ~ Uniform(0.001,0.999)`;
- `log10(gamma) ~ Uniform(-4,0.5)`;
- `log10(kappa) ~ Uniform(-4,0.5)`;
- `log10(omega) ~ Uniform(-3,0.7)`.

Thus the dynamical range spans approximately:

- `gamma: 1e-4 ... 3.1623`;
- `kappa: 1e-4 ... 3.1623`;
- `omega: 1e-3 ... 5.0119`.

Bloch state generation is frozen by candidate parity:

- odd candidate IDs: draw a 3D standard-normal direction, normalize it, and choose radius `r=0.95*u^(1/3)` with `u~Uniform(0,1)`;
- even candidate IDs: draw/normalize a 3D standard-normal direction and choose radius `r~Uniform(0.90,0.999)`.

This deliberately mixes interior states with near-boundary physical states.

No candidate is regenerated because of its scientific outcome. A numerically inadmissible quotient is preserved as `REFUSE_QUOTIENT`.

## Frozen explicit corner panel

In addition to the 4096 seeded cases, test these 16 deterministic physical-state corners. Use all combinations of:

- `eta in {0.001,0.999}`;
- `(gamma,kappa,omega)` in {
  `(1e-4,3.0,1e-3)`,
  `(3.0,1e-4,1e-3)`,
  `(1e-4,1e-4,5.0)`,
  `(3.0,3.0,5.0)`
  };
- state choice alternating by combination index between `(x,y,z)=(0.04,0,0.998)` and `(0.04,0,-0.998)`.

The state norm is below 1. These corner cases are not replaceable.

## Quotient admission and numerical reconstruction

Use the same fail-closed rules as the preceding phases:

- positive density matrix;
- deterministic physical observability dark space reconstructed from `[V^T;V^T A;V^T A^2]`;
- exactly one-dimensional dark factor and two-dimensional active quotient;
- measurement-dark, `A_phys`, `A_rec`, and `B` dark-invariance residuals `<=5e-9`;
- quotient intertwining residuals `<=5e-9`;
- direct symmetric second-moment lift agrees with the Kronecker/duplication construction to `<=5e-11`.

The looser-than-previous reconstruction tolerances are frozen here because this stress set spans more than four orders of magnitude and includes near-boundary states. They may not be changed after execution.

If fewer than 4000 of 4096 seeded fixtures are admitted, status is `STRESS_ADMISSION_HOLD`. Refused fixtures are not replaced.

All 16 explicit corner controls must be admitted; otherwise status is `CORNER_ADMISSION_HOLD`.

## Frozen directional and diagnostic outputs

For each admitted case record separately:

- `alpha_phys`;
- `alpha_rec`;
- `delta_alpha=alpha_rec-alpha_phys`;
- physical and same-record Routh-Hurwitz classes and invariant triples;
- `DeltaA` and `DeltaG` ranks;
- structural-formula residuals;
- physical parameters and Bloch state.

If H2 fails, preserve **all** counterexample IDs and full parameter records. Do not alter the phase to rescue the claim.

For diagnostic ranking only, report:

- largest positive `delta_alpha`, if any;
- least-negative `delta_alpha` otherwise;
- most-negative `delta_alpha`;
- cases nearest the physical or same-record mean-square boundary.

Those diagnostics do not change H2.

## Frozen adversarial algorithm controls

The comparator must again prove that it can report either direction using:

`A0=[[-0.3,1],[-1,-0.3]]`, `B0=0.2 I2`.

- stabilizing rank-one update: `DeltaA=[[-0.4,0],[0,0]]`, require `delta_alpha<0`;
- destabilizing rank-one update: `DeltaA=[[0.8,0],[0,0]]`, require `delta_alpha>0` and updated mean-square class `UNSTABLE`.

## Frozen gates

- **S0 exact structural identity:** symbolic identities factor exactly and numerical full-reconstruction residuals are within the registered limits.
- **S1 generator determinism:** the 4096 seeded fixtures regenerate byte-equivalent numeric arrays in-process.
- **S2 broad admission:** at least 4000/4096 seeded cases admitted without replacement and all 16 corner cases admitted.
- **S3 mean-square audit:** all admitted channels pass direct-vs-Kronecker lift and Routh-Hurwitz-vs-spectral consistency.
- **S4 adversarial comparator:** both stabilizing and destabilizing controls return the expected direction, and the destabilizing control becomes `UNSTABLE`.
- **S5 generalized H2:** every admitted broad/corner fixture satisfies `alpha_rec <= alpha_phys + 1e-9`.

Phase status:

- `PASS_GENERALIZED_H2_STRESS` if S0-S5 pass;
- `FAIL_GENERALIZED_H2` if S0-S4 pass but S5 fails;
- `STRESS_ADMISSION_HOLD` or `CORNER_ADMISSION_HOLD` for the corresponding S2 condition;
- `AUDIT_FAILURE` for any other failed gate.

## Interpretation firewall

A H2 PASS would be strong computational evidence across the specified broad measured-qubit family but would still not be a mathematical proof of universal monotonicity.

A H2 FAIL would be a valuable boundary signal identifying where the bounded 24-fixture result stops generalizing.

Neither outcome licenses:

- localization/collapse prediction;
- a stochastic scalar chi;
- channel averaging;
- extension to different Hamiltonian axes, measurement operators, dissipation structures, Hilbert-space dimensions, or nonlinear measurement models without fresh work.
