# Stochastic dark/active compatibility and quotient-closure audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

The closed deterministic lineage has established, without consulting localization outcomes, a maximal conditioning-dark subspace `D` for the physical drift `A_phys`, an exact common characteristic factor shared by `A_phys` and `A_rec`, and an admissible deterministic scalar `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` only when the remaining active quotient is real, identifiable, asymptotically stable, and exactly two-dimensional.

The local tangent dynamics are nevertheless stochastic:

`d r = A r dt + B r dW`.

This audit asks whether the same deterministic dark factor is also compatible with the multiplicative-noise matrix `B`, so that the full linear Itô SDE descends exactly to the same two-dimensional quotient. It does **not** test localization, collapse, measurement quality, or any historical outcome.

No localization result, E16-E27 error, historical preferred chi, or GFSA external-candidate response may be read by this audit.

## Frozen construction

For the registered physical generator `A_phys`, measurement functional `V^T`, and state-dependent stochastic tangent matrix `B`, reconstruct the deterministic maximal dark subspace outcome-free as

`D = ker(O)`,

where

`O = [V^T; V^T A_phys; ...; V^T A_phys^(n-1)]`.

Use SVD with fixed null threshold `1e-10`. `D` must first pass the already-established deterministic invariance check

`A_phys D subset D`.

Stochastic compatibility additionally requires

`B D subset D`.

Only if both conditions hold does the quotient map `L` annihilating `D` define exact quotient matrices satisfying

`L A = A_A L`,

`L B = B_A L`.

The same `D`, `L`, and `B_A` are used for the physical and record-conditioned channels because the registered convention has a shared `B` and `A_rec=A_phys+UV^T` with `V^T D=0`.

For an orthonormal decomposition `T=[D,C]`, take the canonical quotient map `L=C^T`. For a non-orthogonal complement/basis change

`C_s = D S + C R`,

with frozen

`R=[[1.2,0.3],[-0.2,0.9]]`

and, for one-dimensional `D`,

`S=[[0.4,-0.35]]`,

construct `T_s=[D,C_s]` and define `L_s` as the lower two rows of `T_s^{-1}`. The transformed quotient matrices must obey

`A_A,s = R^(-1) A_A R`,

`B_A,s = R^(-1) B_A R`.

No Frobenius-norm invariance under non-orthogonal similarity is assumed.

## Frozen fresh quantum controls

Use three parameter/base-state fixtures not used by the preceding active-quotient audit:

1. `SQ1: eta=0.66, gamma=0.27, kappa=0.16, omega=0.97, base=(0.14,-0.23,0.18)`
2. `SQ2: eta=0.74, gamma=0.35, kappa=0.12, omega=1.19, base=(-0.22,0.17,-0.31)`
3. `SQ3: eta=0.58, gamma=0.21, kappa=0.24, omega=0.79, base=(0.29,0.08,0.12)`

Use the already-closed convention:

- `x=sigma_z/2`;
- `H=omega sigma_y/2`;
- amplitude-damping collapse amplitude `sqrt(gamma)`;
- unconditional measurement term `2 kappa D[x]`;
- `A_phys` reconstructed from the Liouvillian action;
- `B=sqrt(2 eta kappa) D(H_x)[rho]`;
- `A_rec=A_phys-4 eta kappa h m^T`.

These are representation controls only.

## Frozen direct-propagation controls

For each admitted quantum fixture and each channel use quotient initial vectors

`q1=(0.31,-0.22)` and `q2=(-0.17,0.28)`.

For each quotient vector use dark lifts `alpha in {-0.73,0.41}` so that

`r=C q + D alpha`.

Use Euler-Maruyama maps

`r'=(I+A dt+B dW)r`

with

- `dt=1e-4`;
- `dW/sqrt(dt) in {0.47,-0.63}`.

Projected full propagation must equal

`q'=(I+A_A dt+B_A dW)q`

independently of the dark lift.

For direct covariance propagation, in `[D,C]` coordinates use

`Pfull1=[[0.55,0.09,-0.05],[0.09,0.42,0.04],[-0.05,0.04,0.31]]`

and

`Pfull2=[[0.70,-0.06,0.08],[-0.06,0.36,-0.03],[0.08,-0.03,0.48]]`.

Transform each to the physical basis by `T P T^T`. Use `dt_cov=7e-4` with equally weighted noise nodes `dW=+sqrt(dt_cov)` and `-sqrt(dt_cov)`. Compare the quotient covariance obtained by projecting the full propagated covariance against propagation by the quotient matrices alone.

## Frozen second-moment closure

For column-major vectorization define

`K(A,B)=I tensor A + A tensor I + B tensor B`.

Let

`J=L tensor L`.

Exact quotient closure requires

`J K(A,B) = K(A_A,B_A) J`.

This intertwining must hold separately for `A_phys` and `A_rec`.

## Frozen refusal controls

The audit must refuse rather than manufacture stochastic quotient closure in the following preregistered cases.

### RQ1 stochastic leakage

Use a stable real 3x3 synthetic control with a one-dimensional deterministic dark factor but choose `B` so that `B D` has a nonzero active component. Required status: `REFUSE_STOCHASTIC_LEAKAGE`.

### RQ2 wrong quotient dimension

Use a synthetic 4x4 control whose reconstructed deterministic dark factor leaves a three-dimensional quotient. Required status: `REFUSE_QUOTIENT_DIMENSION`.

### RQ3 no identifiable dark factor

Use a synthetic control with full observability under `V^T`, so `dim D=0`. Required status: `REFUSE_NO_DARK_FACTOR`.

### RQ4 cross-sector degeneracy

Use an otherwise compatible synthetic control whose dark eigenvalue coincides with an active eigenvalue. Required status: `REFUSE_CROSS_SECTOR_DEGENERACY`.

### RQ5 defective active sector

Use an otherwise compatible control with a defective 2x2 active quotient. Required status: `REFUSE_DEFECTIVE_ACTIVE_SECTOR`.

### RQ6 coordinate failure

Use a deliberately singular active-basis transform. Required status: `REFUSE_COORDINATE_FAILURE`.

No refusal control may fall back to a scalar or quotient claim.

## Frozen gates

### S0 source/state validity

For every quantum fixture require a positive density matrix and finite real `A_phys`, `A_rec`, and `B`.

PASS requires minimum density eigenvalue `>0` and maximum imaginary matrix entry `<=1e-12`.

### S1 independent deterministic dark reconstruction

Reconstruct `D` from the observability matrix using only `A_phys` and `V^T`.

PASS requires `dim D=1`, `dim quotient=2`, orthonormality residual `<=5e-12`, `||V^T D||_max<=5e-12`, and deterministic invariance residual `||(I-DD^T)A_phys D||_max<=5e-12`.

### S2 stochastic compatibility

PASS requires

`||(I-DD^T) B D||_max <=5e-12`

for every fresh quantum fixture. Failure returns `REFUSE_STOCHASTIC_LEAKAGE` for that fixture and no stochastic quotient is licensed.

### S3 quotient intertwining

For both physical and record-conditioned channels verify

`L A = A_A L`

and

`L B = B_A L`.

PASS requires maximum absolute residual `<=5e-12`.

### S4 complement/basis covariance

Using the frozen non-orthogonal complement shear plus active-basis change, verify transformed quotient matrices against

`R^(-1) A_A R`

and

`R^(-1) B_A R`.

Also verify characteristic-polynomial invariance of `A_A` and `B_A`.

PASS requires maximum matrix residual `<=5e-11` and maximum characteristic-polynomial coefficient residual `<=5e-11`.

### S5 direct trajectory quotient closure

For every registered `q`, dark lift, noise node, fixture, and channel, compare projected full Euler-Maruyama propagation with quotient propagation.

PASS requires maximum absolute state residual `<=2e-12`.

### S6 second-moment generator and direct covariance closure

For every fixture and channel verify

`(L tensor L) K(A,B) = K(A_A,B_A) (L tensor L)`

with maximum absolute residual `<=5e-11`.

For both frozen covariance controls, compare projected full two-node Euler-Maruyama covariance propagation with quotient covariance propagation. PASS requires maximum absolute covariance residual `<=5e-12`.

### S7 refusal behavior and deterministic-scalar firewall

All RQ1-RQ6 controls must return exactly their preregistered refusal statuses.

For admitted quantum controls the already-licensed deterministic `chi_active` may be reported as metadata, separately for physical and record-conditioned `A_A`, but the stochastic pair `(A_A,B_A)` must return

`STOCHASTIC_PAIR_NOT_COMPRESSED`.

No noise-aware scalar is licensed in v0.1.

## Decision rule

Overall PASS requires `S0 & S1 & S2 & S3 & S4 & S5 & S6 & S7`.

Any failed gate remains failed. After first execution, no fixture, matrix convention, null threshold, timestep, noise node, covariance control, transform, tolerance, refusal rule, or interpretation may be changed inside v0.1. A scientifically motivated correction requires a new version with the v0.1 result preserved.

## Interpretation firewall

A PASS would establish only that, for the admitted controls, the already-reconstructed deterministic conditioning-dark factor is also invariant under the registered multiplicative stochastic tangent matrix and therefore defines an exact two-dimensional stochastic quotient.

A PASS would **not** establish that the dark sector is noise-free, that `chi_active` captures stochastic stability, that any noise-aware scalar exists, that chi=1 predicts localization, or that measurement performance is optimized anywhere.

The dark coordinate may itself remain stochastic. The only licensed statement is quotient closure: active projected dynamics do not depend on which representative is chosen along the dark fiber.
