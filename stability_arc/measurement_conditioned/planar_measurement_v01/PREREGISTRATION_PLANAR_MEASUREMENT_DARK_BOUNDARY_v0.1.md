# Planar measurement-axis dark-boundary derivation v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** GENERAL_PLANAR_MEASUREMENT_STRUCTURE

## Purpose

The fixed 45-degree x-z measurement-axis transfer passed on 128 fresh fixtures, while a generic 3D measurement-axis control correctly refused the 2D quotient. This phase asks for the exact structural boundary across the entire x-z measurement plane.

No localization, collapse, measurement-quality, sigma_z orientation-crossing outcome, or external GFSA candidate may enter this derivation.

## Model

Let

`n(theta)=(sin(theta),0,cos(theta))`

and

`X_theta = (sin(theta)*sigma_x + cos(theta)*sigma_z)/2`.

Keep

`H=omega*sigma_y/2`,

amplitude damping `sqrt(gamma)*sigma_-`,

unconditional measurement backaction `2*kappa*D[X_theta]`,

and measurement efficiency `eta`.

Use Bloch tangent coordinates `(x,y,z)`.

## Registered exact physical tangent target

The independently derived physical Bloch tangent matrix must be

`A_phys = [[-gamma/2-kappa*cos(theta)^2, 0, omega+kappa*sin(theta)*cos(theta)],
           [0, -gamma/2-kappa, 0],
           [-omega+kappa*sin(theta)*cos(theta), 0, -gamma-kappa*sin(theta)^2]]`.

The measurement functional is proportional to

`V^T=(sin(theta),0,cos(theta))`.

Therefore the y-axis vector `e_y=(0,1,0)^T` is measurement-dark.

## Registered observability boundary

Restrict the physical observability matrix to the x-z plane. The determinant of the first two observability rows must reduce exactly to

`Delta_obs = omega - (gamma/2)*sin(theta)*cos(theta)`

or equivalently

`Delta_obs = omega - (gamma/4)*sin(2*theta)`.

The measurement-backaction strength kappa cancels from this rank condition.

Registered classification:

- if `Delta_obs != 0`, physical observability rank is 2, the maximal dark factor is exactly `D=span(e_y)`, and quotient dimension is 2;
- if `Delta_obs = 0`, physical observability rank drops to 1, dark dimension becomes 2, and the 2D quotient must return `REFUSE_QUOTIENT_DIMENSION`.

The exact analytic condition, not an SVD threshold fitted to examples, controls this classification.

## Registered stochastic invariance target

For a physical Bloch base state `r`, let `mu=n dot r` and `q=eta*kappa`.

The same-noise stochastic tangent matrix must satisfy

`B e_y = -sqrt(2*q)*mu*e_y`.

The same-record deterministic correction has the rank-one form `U V^T`, so

`(A_rec-A_phys)e_y=0`.

Thus away from the exact observability boundary, the exact one-dimensional dark line must be invariant under `A_phys`, `A_rec`, and `B`, and the full stochastic tangent SDE must descend to the 2D quotient.

## Frozen symbolic gates

- **P0 physical matrix derivation:** independently derive the Bloch tangent matrix from the Hilbert-space Liouvillian and recover the registered A entries exactly.
- **P1 observability determinant:** derive the x-z observability determinant and simplify it exactly to `omega-(gamma/2)sin(theta)cos(theta)` with complete kappa cancellation.
- **P2 dark-line identities:** prove symbolically `V^T e_y=0` and `A_phys e_y=-(gamma/2+kappa)e_y`.
- **P3 stochastic dark-line identity:** independently derive the stochastic tangent Jacobian and prove `B e_y=-sqrt(2*eta*kappa)*(n dot r)e_y`.
- **P4 same-record invariance:** prove the rank-one conditioning correction annihilates `e_y`.

## Fresh numerical gates

Use NumPy `default_rng(seed=2026082917)` to generate exactly 256 fresh generic planar-axis fixtures:

- `theta ~ Uniform(-pi,pi)`;
- `gamma ~ LogUniform(0.1,2.0)`;
- `kappa ~ LogUniform(0.05,2.0)`;
- `eta ~ Uniform(0.05,0.95)`;
- `omega ~ Uniform(0.05,3.0)`;
- Bloch radius `r ~ Uniform(0.05,0.85)` with isotropic direction.

No fixture is replaced because of `Delta_obs` or any rank result.

For every fixture whose normalized `|Delta_obs|/(gamma+omega) > 1e-8`, require:

- Hilbert-space reconstructed dark dimension exactly 1;
- dark line overlaps `e_y` with absolute overlap >=`1-1e-10`;
- A_phys/A_rec/B dark-invariance residuals <=`5e-10`;
- deterministic and stochastic quotient intertwining <=`5e-10`;
- second-moment intertwining <=`5e-9`.

Any generated fixture inside the frozen `1e-8` numerical neighborhood is retained and reported as `NEAR_EXACT_BOUNDARY`, not replaced or used to tune a threshold.

- **P5 fresh generic-planar audit:** all non-near-boundary fixtures satisfy the registered one-dimensional stochastic quotient architecture.

## Exact boundary controls

Use three preregistered exact boundary controls:

1. `theta=pi/4, gamma=1, omega=1/4`;
2. `theta=pi/6, gamma=2, omega=sqrt(3)/4`;
3. `theta=3*pi/4, gamma=1, omega=-1/4` as an algebraic signed-frequency control only.

For controls 1 and 2 use positive physical omega and require physical observability rank 1, dark dimension 2, and exact refusal `REFUSE_QUOTIENT_DIMENSION`.

Control 3 is not a physical-frequency fixture and is used only to verify the signed algebraic boundary identity.

Use fixed `kappa=0.3`, `eta=0.7`, and Bloch vector `(0.2,0.1,-0.3)` for the two physical boundary controls.

- **P6 exact-boundary refusal:** both physical exact-boundary controls return dark dimension 2 and `REFUSE_QUOTIENT_DIMENSION`; the signed algebraic control satisfies the exact determinant identity.

## Generic out-of-plane refusal control

Retain the fixed axis

`n=(1,1,1)/sqrt(3)`

with `gamma=0.3,kappa=0.2,eta=0.7,omega=1.1` and Bloch vector `(0.2,0.1,-0.3)`.

- **P7 out-of-plane refusal:** physical observability rank is 3 and status is `REFUSE_NO_1D_DARK_FACTOR`.

## Decision rule

`PASS_PLANAR_MEASUREMENT_DARK_BOUNDARY` only if P0-P7 pass.

A symbolic mismatch is `DERIVATION_FAILURE`. A fresh generic fixture contradicting the registered structure is `FAIL_PLANAR_ARCHITECTURE`. Boundary controls failing their refusal are `BOUNDARY_REFUSAL_FAILURE`.

## Interpretation firewall

A PASS licenses an exact structural boundary for the existence of the 2D stochastic quotient across this x-z measurement-plane family. It does not imply that the c1/c3 mean-square boundary geometry is angle-independent, does not license a stochastic scalar, and does not transfer any localization/collapse claim.
