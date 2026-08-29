# Stochastic second-moment lift audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

The closed joint-channel v0.2 representation has the local Itô form

`d r = A r dt + B r dW`

for each channel, with distinct deterministic drifts `A_phys` and `A_rec` and a shared fully normalized stochastic matrix `B` under the registered single-observable convention.

Drift eigenvalues alone do not contain the full stability information of a multiplicative-noise linear SDE. This audit tests the exact second-moment/covariance lift before any localization or measurement-performance outcome is consulted.

It reads no E16-E27 localization error, no historical localization score, and no GFSA v0.7 external-candidate response.

## Frozen Itô derivation

For

`P = E[r r^T]`,

Itô multiplication gives

`dP/dt = A P + P A^T + B P B^T`.

Define

`G_{A,B}(P) = A P + P A^T + B P B^T`.

Use **column-major vectorization** `vec_F`, i.e. matrix columns are stacked in order. Under this convention,

`vec_F(G(P)) = K(A,B) vec_F(P)`

with

`K(A,B) = I tensor A + A tensor I + B tensor B`.

The physical and record-conditioned full-space moment operators are

`K_phys = K(A_phys,B)`

and

`K_rec = K(A_rec,B)`.

Because the two registered channels share `B`,

`DeltaK = K_rec-K_phys = I tensor DeltaA + DeltaA tensor I`.

This identity is specific to the currently registered shared-noise-amplitude convention and is not asserted universally.

## Symmetric covariance subspace

Physical second moments satisfy `P=P^T`. Use the fixed orthonormal Frobenius basis

- `S1=E11`
- `S2=E22`
- `S3=E33`
- `S4=(E12+E21)/sqrt(2)`
- `S5=(E13+E31)/sqrt(2)`
- `S6=(E23+E32)/sqrt(2)`.

Let `U` be the 9x6 matrix whose columns are `vec_F(Sj)`. The registered symmetric-subspace operator is

`K_sym = U^T K U`.

The licensed moment representation, if this audit passes, is the ordered tuple

`M = (K_phys_sym, K_rec_sym, DeltaK_sym, K_joint_sym)`

where

- `DeltaK_sym = K_rec_sym-K_phys_sym`;
- `K_joint_sym = diag(K_phys_sym,K_rec_sym)`.

No scalar compression of these 6x6 or 12x12 objects is licensed in v0.1.

## Fresh fixtures

Use three parameter/base-state fixtures not used in joint-channel v0.1 or v0.2:

1. `eta=0.68, gamma=0.19, kappa=0.13, omega=0.91, base=(0.21,0.09,-0.24)`
2. `eta=0.77, gamma=0.43, kappa=0.21, omega=1.07, base=(-0.16,-0.28,0.19)`
3. `eta=0.59, gamma=0.31, kappa=0.09, omega=0.73, base=(0.08,-0.11,0.36)`

For each fixture use the already-closed conventions:

- `x=sigma_z/2`;
- `H=omega sigma_y/2`;
- amplitude-damping collapse amplitude `sqrt(gamma)`;
- unconditional measurement term `2 kappa D[x]`;
- `A_phys` reconstructed from the Liouvillian action;
- `B=sqrt(2 eta kappa) D(H_x)[rho]`;
- `A_rec=A_phys-4 eta kappa h m^T`.

These fixtures are representation controls only and are not localization tests.

## Frozen covariance controls

Use both positive-definite covariance matrices:

`P1 = diag(0.7,0.4,0.2)`

and

`P2 = [[0.6,0.08,-0.04],[0.08,0.5,0.06],[-0.04,0.06,0.4]]`.

For deterministic ensemble propagation, factor each `P=L L^T` by Cholesky and use six sigma points

`r_{i,+}=+sqrt(3) L e_i`, `r_{i,-}=-sqrt(3) L e_i`,

each with weight `1/6`.

This ensemble has exactly zero mean and covariance `P` up to numerical roundoff.

## Independent one-step covariance check

For each channel and covariance control, use Euler-Maruyama tangent maps

`r' = (I + A dt + B dW) r`

with two equally weighted noise nodes `dW=+sqrt(dt)` and `dW=-sqrt(dt)`.

Freeze

- `dt_coarse=1e-3`
- `dt_fine=5e-4`.

From direct sigma-point/noise-node propagation compute

`D(dt) = (P_next(dt)-P)/dt`.

For this map,

`D(dt)=G(P)+A P A^T dt`.

Use the preregistered Richardson combination

`D_R = 2 D(dt_fine) - D(dt_coarse)`

because `dt_fine=dt_coarse/2`; it removes the first-order-in-dt remainder without fitting any parameter.

## Frozen gates

### M0 vectorization convention

For every fresh fixture, both channels, and every matrix unit `Eij`, verify

`K vec_F(Eij) = vec_F(G(Eij))`.

PASS requires maximum absolute residual <= `5e-13`.

This gate prevents silent row-major/column-major or Kronecker-order mistakes.

### M1 symmetric-subspace closure and projection

For every fresh fixture and both channels:

1. `G(Sj)` must be symmetric for every registered symmetric basis element `Sj`, with maximum antisymmetry entry <= `5e-13`;
2. the directly constructed 6x6 Frobenius-coordinate operator must agree with `U^T K U` to maximum absolute entry residual <= `5e-13`.

### M2 independent covariance-propagation reconstruction

For `P1` and `P2`, every fresh fixture, and both channels:

- compare `D_R` from direct sigma-point/noise-node propagation with `G(P)`;
- compare `vec_F(D_R)` with `K vec_F(P)`.

PASS requires maximum absolute matrix/vector residual <= `2e-9`.

The raw fine-step error `||D(dt_fine)-G(P)||_max` must not exceed the corresponding coarse-step error; otherwise M2 fails even if Richardson happens to pass.

### M3 comparative moment identity

For every fresh fixture verify

`DeltaK = I tensor DeltaA + DeltaA tensor I`

with maximum absolute entry residual <= `5e-13`.

Also verify

`DeltaK_sym = U^T DeltaK U = K_rec_sym-K_phys_sym`

with maximum absolute residual <= `5e-13`.

### M4 common-coordinate covariance

Use the same fixed orthogonal rotation

`Q=Rz(0.37) Ry(-0.52) Rx(0.29)`.

Transform

`A' = Q^T A Q`, `B'=Q^T B Q`.

For column-major covariance vectorization define

`S = Q^T tensor Q^T`.

Construct `K'` directly from `(A',B')` and verify

`K' = S K S^{-1}`

with maximum absolute entry residual <= `5e-12` for both channels and all fresh fixtures.

For the 6D symmetric representation, construct the induced orthogonal matrix

`R_ij = <S_i, Q^T S_j Q>_F`

and verify

`K_sym' = R K_sym R^T`

or its algebraically equivalent coordinate-convention form, provided that form is fixed in code before execution. The implementation must record which orientation is used and verify `R` orthogonality <= `5e-13`. Maximum similarity residual must be <= `5e-12`.

### M5 joint identity preservation

Construct

`K_joint_sym = diag(K_phys_sym,K_rec_sym)`.

PASS requires exact block recovery to `5e-13` and all off-diagonal channel blocks to have maximum absolute magnitude <= `5e-13`.

The joint representation may contain comparative metadata, but no averaging or outcome-weighted mixing is permitted.

### M6 scalar-refusal and noiseless inheritance control

All 6x6 moment operators and the 12x12 joint moment operator must return

`FULL_MOMENT_OPERATOR_REQUIRED`

under the v0.1 scalar policy.

As a lineage control only, for the registered real stable 2x2 oscillator blocks with `B=0`, verify that the full 4x4 moment-lift eigenvalue multiset equals the pairwise sums of the underlying 2x2 drift eigenvalues to matching tolerance `1e-10` using an outcome-independent minimum-cost matching over the four values.

This check establishes the known noiseless spectral inheritance of the lift. It does **not** license applying the original scalar `chi` formula directly to `K`.

## Decision rule

Overall PASS requires `M0 & M1 & M2 & M3 & M4 & M5 & M6`.

Any failed gate remains failed. No fixture, covariance control, timestep, sigma-point rule, vectorization convention, threshold, rotation, scalar policy, or interpretation may be changed inside v0.1 after execution. A scientifically motivated correction requires a new version with the v0.1 result preserved.

## Interpretation firewall

A PASS would establish only that the second-moment lift is mathematically and numerically consistent with the already-closed local stochastic tangent representation.

It would **not** establish that moment stability predicts localization, that a particular moment eigenvalue is physically privileged, that a scalar chi exists for the lifted system, or that chi=1 is an optimum under measurement.

No localization outcome may be used to choose a moment norm, spectral statistic, channel weighting, mode pairing, threshold, or scalar reduction in this phase.
