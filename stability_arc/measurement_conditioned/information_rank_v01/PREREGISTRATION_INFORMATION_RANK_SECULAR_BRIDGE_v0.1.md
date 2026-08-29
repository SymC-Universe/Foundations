# Information-rank secular bridge audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

The closed same-noise / same-record tangent relation has, for one scalar continuously measured record under the registered convention,

`A_rec = A_phys + DeltaA`

with

`DeltaA = -4 eta kappa h m^T`,

where `h` is the tangent-space coordinate vector of `H_x(rho)` and `m^T delta r = delta mu` is the scalar measurement functional. The closed joint-channel v0.2 audit observed rank one on three fresh fixtures, and the closed moment-lift v0.1 audit established the corresponding stochastic covariance generators without licensing a scalar compression.

This audit asks a different, outcome-free structural question:

> Does the dimension of the measurement record bound the dimension of the direct conditioning update, and therefore reduce the **comparative** spectral relation between the physical and record-conditioned generators to a low-dimensional secular object without collapsing either generator itself?

No localization outcome, E16-E27 score, GFSA external-candidate response, preferred chi value, or retrospective mode choice may be read or used.

## Frozen algebraic statement

For tangent dimension `n` and `m` scalar measurement records, write the record-conditioning drift correction as

`DeltaA = U V^T = sum_j u_j v_j^T`,

where each scalar record contributes one outer product. Therefore

`rank(DeltaA) = r <= m`.

For `A_rec = A_phys + U V^T`, define `M(z)=z I-A_phys`.

The global polynomial identity is

`det(z I-A_rec) = det(M(z)) -` the appropriate rank-one adjugate term for `m=1`,

and, away from singular `M(z)`, the general matrix determinant lemma gives

`det(z I-A_rec) / det(z I-A_phys) = det(I_m - V^T M(z)^(-1) U)`.

For `m=1`, the comparative secular factor is the scalar

`g(z) = 1 - v^T (z I-A_phys)^(-1) u`.

This scalar is a **comparative secular factor only**. It is not a scalar state coordinate, not a replacement for either full generator, and not a licensed chi.

## Frozen second-moment consequence

Under the already-closed shared stochastic-amplitude convention, the physical and record-conditioned moment generators differ only through the drift correction:

`DeltaK = I tensor DeltaA + DeltaA tensor I`.

If `rank(DeltaA)=r`, then on the full `n^2` vectorized second-moment space the image of `DeltaK` is contained in

`(R^n tensor range(DeltaA)) + (range(DeltaA) tensor R^n)`,

so

`rank(DeltaK) <= 2 n r - r^2`.

On the symmetric covariance space, the image is contained in the symmetric matrices having at least one index in `range(DeltaA)`, so

`rank(DeltaK_sym) <= r(2 n-r+1)/2`.

For one effective scalar record (`r=1`), these become

- full second-moment update rank `<= 2n-1`;
- symmetric covariance update rank `<= n`.

These are upper bounds, not claims that equality must hold.

## Fresh quantum fixtures

Use three parameter/base-state fixtures not used in joint-channel v0.1, joint-channel v0.2, or moment-lift v0.1:

1. `eta=0.72, gamma=0.27, kappa=0.16, omega=1.19, base=(0.14,-0.07,0.31)`
2. `eta=0.61, gamma=0.36, kappa=0.24, omega=0.88, base=(-0.23,0.17,0.12)`
3. `eta=0.83, gamma=0.15, kappa=0.11, omega=1.43, base=(0.06,0.26,-0.29)`

Use the already-closed conventions:

- `x=sigma_z/2`;
- `H=omega sigma_y/2`;
- amplitude-damping collapse amplitude `sqrt(gamma)`;
- unconditional measurement term `2 kappa D[x]`;
- same-noise and same-record tangent maps exactly as closed previously.

For independent full-map reconstruction freeze

- `dt=7e-4`;
- normalized innovation coefficient `dW/sqrt(dt)=0.41`;
- centered finite-difference epsilon `8e-6`.

These values are fixed before execution and are not selected from outcomes.

## Frozen algebraic multi-record controls

These are representation controls, not physical localization systems.

### C1: n=4, m=2

`A = [[-0.4,1.0,0,0],[-1.0,-0.4,0.2,0],[0,-0.2,-0.7,0.5],[0,0,-0.5,-0.7]]`

`U = [[0.3,-0.2],[0.1,0.4],[-0.25,0.15],[0.2,0.05]]`

`V = [[0.5,0.1],[-0.2,0.35],[0.3,-0.25],[0.15,0.4]]`

### C2: n=5, m=3

`A = [[-0.5,0.8,0,0,0],[-0.8,-0.5,0.15,0,0],[0,-0.15,-0.65,0.45,0],[0,0,-0.45,-0.65,0.2],[0,0,0,-0.2,-0.9]]`

`U = [[0.2,-0.1,0.05],[0.15,0.25,-0.2],[-0.3,0.1,0.12],[0.05,-0.2,0.3],[0.18,0.07,-0.11]]`

`V = [[0.4,0.05,-0.12],[-0.1,0.3,0.2],[0.25,-0.2,0.15],[0.08,0.22,-0.3],[-0.18,0.1,0.27]]`

No control matrix may be replaced after execution.

## Frozen complex probes

For resolvent-form determinant-lemma checks use

- `z1 = 0.50 + 0.70 i`;
- `z2 = 0.90 + 1.20 i`;
- `z3 = 1.40 + 0.35 i`.

The implementation must also evaluate the global rank-one adjugate identity for the quantum fixtures at the physical eigenvalues, where the resolvent ratio is not licensed.

## Frozen gates

### I0 independent quantum conditioning reconstruction

For every fresh quantum fixture, independently reconstruct the deterministic Jacobians of the same-noise and same-record one-step maps by centered finite differences using both `+dW` and `-dW` and average away the stochastic term.

PASS requires:

- `max|A_phys_FD-A_phys| <= 2e-6`;
- `max|A_rec_FD-A_rec_formula| <= 2e-6`;
- `max|(A_rec_FD-A_phys_FD)-DeltaA_formula| <= 3e-6`;
- numerical `rank(DeltaA_formula) <= 1` at singular-value tolerance `1e-12`.

The formula being tested may not be used to construct the finite-difference Jacobians.

### I1 global rank-one characteristic-polynomial identity

For each fresh quantum fixture, write `DeltaA=u v^T` using the frozen physical factors

`u=-4 eta kappa h`, `v=m`.

For every coefficient probe and at each eigenvalue of `A_phys`, verify the globally valid identity

`det(z I-A_rec) = det(z I-A_phys) - v^T adj(z I-A_phys) u`.

The implementation must compute the adjugate independently by cofactors for the 3x3 quantum matrices, not by multiplying `det(M)` by an inverse.

PASS requires maximum absolute residual `<= 2e-10`.

### I2 resolvent secular factor

At each frozen complex probe, for every quantum fixture and both multi-record controls, verify

`det(z I-A_rec)/det(z I-A_phys) = det(I_m - V^T (zI-A_phys)^(-1) U)`

with absolute residual `<= 2e-10`.

If `sigma_min(zI-A_phys) <= 1e-8`, the resolvent form must return `REFUSE_NEAR_PHYSICAL_POLE` for that probe and may not be rescued by changing the probe. The global polynomial identity remains the fallback mathematical representation.

### I3 information-rank bound

For each quantum fixture and each multi-record control, let `r=rank(UV^T)` at tolerance `1e-12`.

PASS requires `r <= m`.

No lower-bound or equality claim is registered.

### I4 moment-update rank bounds

Construct

`DeltaK = I tensor DeltaA + DeltaA tensor I`

and its orthonormal symmetric-covariance projection.

PASS requires, at SVD tolerance `1e-10`,

- `rank(DeltaK) <= 2 n r-r^2`;
- `rank(DeltaK_sym) <= r(2 n-r+1)/2`.

For the quantum single-record fixtures this means full-space rank `<=5` and symmetric-space rank `<=3`.

### I5 coordinate invariance of the secular bridge

Use fixed orthogonal

`Q=Rz(0.31) Ry(-0.47) Rx(0.22)`

for the n=3 quantum fixtures. Transform

`A'=Q^T A Q`, `U'=Q^T U`, `V'=Q^T V`.

At all frozen complex probes verify that the secular factor

`det(I_m-V^T(zI-A)^(-1)U)`

is invariant to absolute residual `<=2e-11`.

### I6 interpretation/refusal firewall

The implementation must emit all of:

- `PHYSICAL_GENERATOR=FULL_MATRIX_REQUIRED`;
- `RECORD_GENERATOR=FULL_MATRIX_REQUIRED`;
- `MOMENT_GENERATOR=FULL_MOMENT_OPERATOR_REQUIRED`;
- `SECULAR_OBJECT=COMPARATIVE_ONLY`.

No `chi`, optimum, localization predictor, or mode correspondence may be produced by this audit.

## Decision rule

Overall PASS requires `I0 & I1 & I2 & I3 & I4 & I5 & I6`.

Every failed or refused item is preserved as evidence. No fixture, probe, tolerance, finite-difference setting, rank tolerance, rotation, factorization convention, or interpretation may be changed inside v0.1 after execution.

## Interpretation firewall

A PASS would establish a low-rank **comparative** bridge between same-noise physical stability and same-record inference stability under the registered local continuous-measurement convention. It would show that the number of scalar measurement records bounds the rank of the direct conditioning drift update, and that the comparative characteristic-polynomial relation can be expressed through an `m x m` secular determinant relative to the physical resolvent.

It would **not** establish that either generator is reducible to `m` dimensions, that a scalar chi exists, that individual modes can always be paired, that localization is predicted, or that chi=1 is special under measurement.
