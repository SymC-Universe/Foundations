# Dephasing-augmented planar transfer audit v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** DISTINCT_DISSIPATION_GEOMETRY_TRANSFER_TEST

## Purpose

The planar measurement family is closed for amplitude damping alone. This phase changes the dissipative generator by adding independent Markovian pure dephasing while retaining planar continuous measurement.

The new Lindblad generator contains

- amplitude damping jump `sqrt(gamma)*sigma_-`;
- pure-dephasing jump `sqrt(gamma_phi/2)*sigma_z`;
- Hamiltonian `omega*sigma_y/2`;
- measurement backaction `2*kappa*D[X_theta]`, where `X_theta=(sin(theta)sigma_x+cos(theta)sigma_z)/2`.

No prior crossing outcome is used. The question is whether the dark/active quotient and canonical mean-square architecture transfer under a genuinely changed dissipation geometry.

## Dissipative rates

Define

`a = gamma/2 + gamma_phi`

as the transverse dissipative tangent rate and

`b = gamma`

as the longitudinal dissipative tangent rate before measurement backaction.

## Registered exact full tangent target

The physical Bloch tangent must be

`A_phys = [[-a-kappa*cos(theta)^2, 0, omega+kappa*sin(theta)*cos(theta)],
           [0, -a-kappa, 0],
           [-omega+kappa*sin(theta)*cos(theta), 0, -b-kappa*sin(theta)^2]]`.

The measurement functional remains proportional to

`V^T=(sin(theta),0,cos(theta))`.

## Registered observability boundary

The exact x-z observability determinant must reduce to

`Delta_phi = omega-(b-a)*sin(theta)*cos(theta)`

or

`Delta_phi = omega-(gamma/2-gamma_phi)*sin(theta)*cos(theta)`.

Equivalently

`Delta_phi = omega-(gamma/4-gamma_phi/2)*sin(2*theta)`.

The measurement strength kappa must cancel exactly.

Registered architecture:

- `Delta_phi != 0`: maximal dark factor exactly `span(e_y)`, quotient dimension 2;
- `Delta_phi = 0`: dark dimension 2 and mandatory `REFUSE_QUOTIENT_DIMENSION`.

## Registered canonical quotient map

In measurement-aligned in-plane coordinates

`u=n dot (x,z)`, `v=m dot (x,z)`,

with `m=(cos(theta),-sin(theta))`, define

`p = a*sin(theta)^2 + b*cos(theta)^2`,

`d = kappa + a*cos(theta)^2 + b*sin(theta)^2`,

`h = (b-a)*sin(theta)*cos(theta)`.

The admitted quotient must reduce exactly to the already-closed canonical form

`A_p=[[-p,h-omega],[h+omega,-d]]`,

`B=-sqrt(2q)*[[2u,0],[v,u]]`,

`A_r=A_p+[[-2q(1-u^2),0],[2quv,0]]`,

where `q=eta*kappa`.

Thus the full mean-square characteristic triple may transfer only if this exact parameter map is independently verified.

## Frozen symbolic gates

- **D0 Hilbert-space tangent derivation:** independently derive the full Bloch tangent from both dissipators plus measurement and recover the registered matrix exactly.
- **D1 exact observability boundary:** derive and simplify the planar rank determinant exactly to `Delta_phi`, including exact kappa cancellation.
- **D2 exact dark/stochastic identities:** prove `V^T e_y=0`, `A_phys e_y=-(a+kappa)e_y`, same-record correction annihilates `e_y`, and `B e_y=-sqrt(2eta kappa)*(n dot r)e_y`.
- **D3 canonical quotient map:** transform the independently derived full x-z tangent and stochastic Jacobian into `(u,v)` coordinates and recover the registered `A_p,A_r,B` with the new `(p,d,h)` map exactly.
- **D4 amplitude-damping reduction:** set `gamma_phi=0` and recover exactly the preceding planar observability boundary and planar canonical parameter map.

## Fresh transfer audit

Use NumPy `default_rng(seed=2026082919)` to generate exactly 256 fresh fixtures:

- `theta ~ Uniform(-pi,pi)`;
- `gamma ~ LogUniform(0.1,2.0)`;
- `gamma_phi ~ LogUniform(0.001,2.0)`;
- `kappa ~ LogUniform(0.05,2.0)`;
- `eta ~ Uniform(0.05,0.95)`;
- `omega ~ Uniform(0.05,3.0)`;
- Bloch radius `r ~ Uniform(0.05,0.85)` with isotropic direction.

No fixture may be replaced because of the observability determinant or any stability result.

Fixtures with normalized `|Delta_phi|/(a+b+omega)<=1e-8` are retained as `NEAR_BOUNDARY` and excluded only from admitted-quotient scoring.

For every other fixture require:

- Hilbert-space dark dimension exactly 1 and overlap with `e_y` >=`1-1e-10`;
- A_phys/A_rec/B dark invariance <=`5e-10`;
- full-to-canonical quotient matrices <=`2e-9`;
- all six physical/record mean-square characteristic coefficients agree with the already-closed canonical `(p,d,h,q,u,v)` coefficient functions to `2e-8`;
- second-moment quotient intertwining <=`5e-9`.

- **D5 fresh dephasing-augmented transfer:** all scored fresh fixtures pass.

## Exact shifted-boundary controls

Use fixed `kappa=0.3`, `eta=0.7`, Bloch vector `(0.2,0.1,-0.3)`.

- **Bphi1:** `theta=pi/4`, `gamma=1`, `gamma_phi=0.1`, `omega=0.2`.
- **Bphi2:** `theta=-pi/4`, `gamma=1`, `gamma_phi=0.8`, `omega=0.15`.

Both have positive physical frequency and exact `Delta_phi=0` under different signs of `(b-a)`. Both must have dark dimension 2 and return `REFUSE_QUOTIENT_DIMENSION`.

- **D6 shifted-boundary refusal:** both controls refuse exactly.

## Out-of-plane control

With the same two dissipators, use `X3=(sigma_x+sigma_y+sigma_z)/(2sqrt(3))`, parameters `gamma=0.3`, `gamma_phi=0.4`, `kappa=0.2`, `eta=0.7`, `omega=1.1`, base `(0.2,0.1,-0.3)`.

- **D7 generic-axis refusal:** observability rank 3 and status `REFUSE_NO_1D_DARK_FACTOR`.

## Decision rule

`PASS_DEPHASING_AUGMENTED_PLANAR_TRANSFER` only if D0-D7 pass.

A symbolic mismatch is `DERIVATION_FAILURE`; a fresh structural/invariant contradiction is `FAIL_DISSIPATION_TRANSFER`; an exact-boundary refusal failure is `BOUNDARY_REFUSAL_FAILURE`.

## Interpretation firewall

A PASS establishes transfer only to this amplitude-damping-plus-pure-dephasing family. It does not establish universal Lindblad transfer, does not preserve any sigma_z crossing region automatically, and does not license a stochastic scalar or localization/collapse claim.
