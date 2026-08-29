# Planar measurement quotient-invariant derivation v0.1

**Status:** FROZEN BEFORE EXECUTION
**Scope:** OUTCOME_FREE_PLANAR_MEAN_SQUARE_DERIVATION

## Preconditions

The exact planar observability boundary is already closed:

`Delta_obs = omega-(gamma/4)*sin(2*theta)`.

This phase applies only where `Delta_obs != 0`, so the maximal dark factor is exactly one-dimensional and the admitted stochastic quotient is two-dimensional. Exact boundary points remain `REFUSE_QUOTIENT_DIMENSION`.

No localization, collapse, measurement-performance, H4/H5 crossing outcome, or GFSA external candidate may enter this derivation.

## Canonical measurement-aligned quotient coordinates

Let

`n=(sin(theta),cos(theta))`

be the measurement axis in the laboratory x-z plane and

`m=(cos(theta),-sin(theta))`

its orthogonal in-plane direction.

Define quotient coordinates

`u = n dot (x,z)`,

`v = m dot (x,z)`.

Define

`q=eta*kappa`,

`p = gamma*(1+cos(theta)^2)/2`,

`d = kappa + gamma*(1+sin(theta)^2)/2`,

`h = gamma*sin(2*theta)/4`.

Then `Delta_obs=omega-h`.

## Registered exact quotient matrices

The physical drift must reduce exactly to

`A_p = [[-p, h-omega],
        [h+omega, -d]]`.

The shared stochastic tangent matrix must reduce exactly to

`B = -sqrt(2*q)*[[2*u, 0],
                 [v, u]]`.

The same-record drift must reduce exactly to

`A_r = A_p + [[-2*q*(1-u^2), 0],
               [2*q*u*v,       0]]`.

These matrices are frozen derivation targets.

## Mean-square invariant construction

For each channel independently construct the real symmetric second-moment generator from

`dP/dt = A P + P A^T + B P B^T`

on basis `(P11,P12,P22)`.

Define

`det(lambda I-G)=lambda^3+c1 lambda^2+c2 lambda+c3`.

The phase must derive and preserve exact factored expressions for all six channel coefficients

`(c1_p,c2_p,c3_p,c1_r,c2_r,c3_r)`

from the registered quotient matrices. No coefficient may be fitted from numerical cases.

## Registered c1 targets

The exact derivation must recover

`c1_p = 3*(p+d)-14*q*u^2`

and

`c1_r = 3*(p+d)+6*q-20*q*u^2`.

Because `p+d=3*gamma/2+kappa`, equivalently

`c1_p = 9*gamma/2+3*kappa-14*q*u^2`,

`c1_r = 9*gamma/2+3*kappa+6*q-20*q*u^2`,

and

`c1_r-c1_p=6*q*(1-u^2)`.

Thus the previously derived sigma_z c1 displacement is promoted here only if it follows exactly after replacing the measured coordinate `z` by the general measured coordinate `u`.

## Frozen gates

- **Q0 quotient-matrix derivation:** starting from the closed full planar Bloch tangent and the fixed orthogonal `(n,m)` coordinate transform, independently derive `A_p`, `A_r`, and `B` and match the registered matrices exactly.
- **Q1 exact second-moment construction:** independently construct both 3x3 generators and their characteristic coefficients.
- **Q2 c1 identities:** recover the registered c1 formulas and exact displacement `6*q*(1-u^2)`.
- **Q3 sigma_z reduction:** at `theta=0`, with `u=z` and `v=x`, exact symbolic c3 for both channels must reduce to the previously closed sigma_z c3 quadratics from `C3_BOUNDARY_DERIVATION_RESULT_v0.1.md`. c1 must reduce to the previously closed sigma_z c1 formulas.
- **Q4 45-degree clean-room reconstruction:** use fresh seed `2026082918` and exactly 64 independent X45 fixtures; direct Hilbert-space quotient matrices and all six characteristic coefficients must match the canonical formulas to relative-or-absolute `2e-9`.
- **Q5 general-planar clean-room reconstruction:** using the same seed stream after Q4, generate exactly 128 additional fresh planar-axis fixtures with `theta~Uniform(-pi,pi)` and broad positive gamma/kappa/eta/omega plus physical states. Retain every fixture. Fixtures with normalized `|Delta_obs|/(gamma+omega)<=1e-8` are reported as `NEAR_BOUNDARY` and excluded only from 2D quotient scoring; all others must match canonical matrices and all six invariants to `2e-9`.
- **Q6 coordinate covariance:** for all scored Q4/Q5 fixtures, a fixed non-orthogonal active-coordinate change `R=[[1.2,0.3],[-0.2,0.9]]` must preserve both channel characteristic polynomials to `2e-8`.
- **Q7 boundary firewall:** the two positive-frequency exact planar boundary controls from the preceding phase must remain `REFUSE_QUOTIENT_DIMENSION` and may not be assigned c1/c2/c3 as an admitted maximal 2D quotient.

Overall status is `PASS_PLANAR_QUOTIENT_INVARIANTS` only if Q0-Q7 pass.

## Interpretation firewall

A PASS licenses exact angle-dependent planar quotient matrices and their complete mean-square invariant triples. It does not establish that the sigma_z near-pure orientation crossing region persists at other measurement angles, does not license an angle-averaged scalar, and does not establish localization, collapse, or measurement-quality behavior.

Physical and same-record channels remain separately recoverable.
