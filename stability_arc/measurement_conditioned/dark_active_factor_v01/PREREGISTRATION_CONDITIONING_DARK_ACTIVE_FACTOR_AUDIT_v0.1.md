# Conditioning-dark / active-sector factorization audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

The closed measurement-conditioned lineage establishes the local comparative generator

`A_rec = A_phys + DeltaA`, with `DeltaA = U V^T` and `rank(DeltaA) <= m` for `m` scalar record channels.

This audit tests an exact algebraic consequence without consulting localization outcomes: an instantaneous conditioning-null direction (`V^T x = 0`) is not automatically a dynamically dark mode. A genuinely conditioning-dark subspace must also be invariant under `A_phys`.

No historical localization score, E16-E27 position error, GFSA v0.7 external-candidate response, or prior continuation outcome is used to choose a subspace, basis, threshold, dimension, or preferred mode.

## Frozen definitions

For an `n x n` physical drift `A` and `n x m` bridge matrix `V`, define the finite observability stack

`O = [V^T; V^T A; ...; V^T A^(n-1)]`.

Define

`D = ker(O)`.

By construction, `D` is the maximal `A`-invariant subspace contained in `ker(V^T)` in finite dimension. It is the registered **conditioning-dark subspace**.

The larger instantaneous nullspace

`N0 = ker(V^T)`

is called the **instantaneous conditioning-null space**. It may be used as a full dark factor only if it is `A`-invariant.

Let `Q=[Q_D,Q_A]` be an orthogonal basis with `Q_D` spanning `D` and `Q_A` its orthogonal complement. In that basis,

`A_tilde = Q^T A Q`

and

`Arec_tilde = Q^T A_rec Q`.

Because `D` is invariant and `V^T Q_D=0`, both matrices must have zero lower-left dark-to-active block and exactly the same dark block. Therefore their characteristic polynomials share the global factor

`p_D(z) = det(z I_D - A_D)`

without any resolvent division or pole exclusion.

The bottom-right blocks define the quotient/active operators `A_A` and `Arec_A`. All eigenvalue motion induced by conditioning must be contained in these quotient factors. This does not imply that every active-sector eigenvalue must move.

## Quantum controls

Use three fresh parameter/base-state fixtures not used by the previous measurement-conditioned audits:

1. `QF1: eta=0.71, gamma=0.27, kappa=0.16, omega=0.88, base=(0.14,0.26,-0.19)`
2. `QF2: eta=0.63, gamma=0.35, kappa=0.12, omega=1.19, base=(-0.22,0.17,0.31)`
3. `QF3: eta=0.82, gamma=0.21, kappa=0.24, omega=0.67, base=(0.29,-0.13,0.08)`

Use the already-closed convention `x=sigma_z/2`, `H=omega sigma_y/2`, amplitude damping `sqrt(gamma)`, unconditional measurement term `2 kappa D[x]`, and

`DeltaA = -4 eta kappa h m^T`.

For these scalar-record controls use `U=-4 eta kappa h` and `V=m` as column vectors.

## Synthetic controls

### S1 full-kernel invariant dark factor

`A = blockdiag(diag(-0.4,-0.9), [[-0.7,1.2],[-1.2,-0.7]])`.

Use two record directions `V=[e3,e4]` and a fixed nonzero `U` with columns `(0.2,-0.1,0.3,0.4)^T` and `(-0.15,0.25,-0.2,0.35)^T`.

Expected: `ker(V^T)` is invariant and equals `D` with dimension 2.

### S2 instantaneous nullspace larger than the invariant dark space

`A=[[-0.4,0,1.0],[0,-0.6,0],[-1.0,0,-0.8]]`, `V=e3`, `U=(0.3,-0.2,0.25)^T`.

Expected: `ker(V^T)` is not invariant and must return `REFUSE_FULL_KERNEL_FACTOR`; the maximal invariant `D` remains one-dimensional.

### S3 no nontrivial conditioning-dark subspace

`A=[[-0.5,1.0],[-1.0,-0.5]]`, `V=e1`, `U=(0.2,0.3)^T`.

Expected: `dim(D)=0`, status `NO_NONTRIVIAL_DARK_FACTOR`; the full operator is the active quotient.

## Refusal controls

### R1 cross-sector degeneracy

`A=diag(-0.5,-0.8,-0.5)`, `V=e3`, `U=(0.2,-0.1,0.3)^T`.

The algebraic dark factor remains valid, but a dark eigenvalue coincides with an active eigenvalue. Mode-level sector attribution must return `REFUSE_DEGENERATE_SECTOR_ATTRIBUTION`.

### R2 defective active quotient

`A=blockdiag([-0.4], [[-1,1],[0,-1]])`, `V=[e2,e3]`, and fixed `U` columns `(0.1,0.2,-0.1)^T`, `(-0.2,0.15,0.25)^T`.

The algebraic dark factor remains valid, but the active quotient is defective. Mode-level active correspondence must return `REFUSE_DEFECTIVE_ACTIVE_SECTOR`.

Refusal does not invalidate an exact polynomial factorization that independently passes its algebraic gates.

## Frozen numerical conventions

- SVD/nullspace rank tolerance: `1e-11` times the largest singular value, with absolute floor `1e-13`.
- invariance/annihilation/block residual gate: `1e-10` maximum absolute entry.
- characteristic-polynomial coefficient reconstruction gate: `2e-9` maximum absolute coefficient residual.
- spectral cross-sector degeneracy tolerance: `1e-8`.
- eigenvalue clustering tolerance for defectivity checks: `1e-8`.
- geometric-nullity SVD tolerance for defectivity checks: `1e-10` times the largest singular value, absolute floor `1e-12`.

No tolerance may be changed inside v0.1 after execution.

## Frozen gates

### F0 maximal invariant dark-space construction

For every quantum and synthetic control, construct `D=ker(O)` from the fixed observability stack. PASS requires

- `max|V^T Q_D| <= 1e-10` when `dim(D)>0`;
- `max|(I-Q_D Q_D^T) A Q_D| <= 1e-10`;
- `DeltaA Q_D` maximum absolute entry `<=1e-10`.

For `dim(D)=0`, these checks are vacuous and the status must explicitly record `NO_NONTRIVIAL_DARK_FACTOR`.

### F1 instantaneous-nullspace distinction

Construct `N0=ker(V^T)` independently.

If `N0` is not `A`-invariant to the frozen gate, the full-kernel interpretation must return exactly `REFUSE_FULL_KERNEL_FACTOR`; it may not be silently substituted for `D`.

S1 must admit the full kernel. S2 must refuse it. The three quantum controls are expected to be evaluated, not assumed; their returned status is preserved as evidence.

### F2 global common characteristic factor

For every control with `dim(D)>0`, build an orthogonal basis `Q=[Q_D,Q_A]` before any spectral inspection.

PASS requires

- lower-left block of both `Q^T A Q` and `Q^T A_rec Q` `<=1e-10`;
- dark blocks agree `<=1e-10`;
- `poly(A) = convolve(poly(A_D), poly(A_A))` within `2e-9` coefficient residual;
- `poly(A_rec) = convolve(poly(A_D), poly(Arec_A))` within `2e-9`.

This is the primary global-factor test and does not divide by `det(zI-A)`.

### F3 active-quotient bridge identity

With `U_A=Q_A^T U` and `V_A=Q_A^T V`, PASS requires

`Arec_A - A_A = U_A V_A^T`

within `1e-10` maximum absolute entry.

Also verify that the rank of the quotient update does not exceed `m` under the frozen SVD tolerance.

### F4 moved-spectrum completeness by polynomial accounting

For every control with a dark factor, remove only the explicitly constructed common polynomial factor `p_D` by using the already-extracted active blocks, not numerical polynomial division.

PASS requires that the active quotient characteristic polynomials reconstruct the full physical and record-conditioned characteristic polynomials under F2. Therefore every spectral change between the two full generators is contained in the active quotient.

No one-to-one eigenvalue pairing is required by this gate.

### F5 exact dark-mode preservation

For every basis vector in `D`, verify

`A_rec Q_D = A Q_D`

within `1e-10`.

If a simple dark eigenvalue is spectrally separated from the active quotient by more than `1e-8`, its common physical/record eigenvalue may be recorded as `IDENTIFIABLE_DARK_MODE`. Otherwise mode-level attribution must refuse even though the invariant factor remains exact.

### F6 refusal controls

R1 must return `REFUSE_DEGENERATE_SECTOR_ATTRIBUTION` for mode-level labeling while retaining any valid algebraic factorization.

R2 must return `REFUSE_DEFECTIVE_ACTIVE_SECTOR` for mode-level active correspondence while retaining any valid algebraic factorization.

Any implementation that forces a unique eigenmode correspondence in either control fails F6.

### F7 coordinate covariance

Apply the fixed orthogonal coordinate rotation

`Q0 = Rz(0.31) Ry(-0.47) Rx(0.22)`

to `A`, `A_rec`, `U`, and `V` for all three quantum controls. Reconstruct the maximal invariant dark subspace from the rotated inputs, rather than rotating the previously found basis.

PASS requires equal dark-space dimension and projector agreement after transforming back, with maximum absolute projector residual `<=2e-9`. The dark-factor polynomial coefficients must agree within `2e-9`.

## Decision rule

Overall PASS requires `F0 & F1 & F2 & F3 & F4 & F5 & F6 & F7`.

A REFUSE required by F1 or F6 is a successful outcome for that registered refusal gate, not a failure. An unexpected refusal, failed factorization, rank inconsistency, or coordinate-covariance failure remains evidence and must be investigated.

## Interpretation firewall

A PASS would establish an exact decomposition of the **comparative conditioning update** into a maximal dynamically dark invariant factor and an active quotient for the registered controls.

It would not establish that dark modes are immune to stochastic measurement noise, because the shared stochastic tangent matrix `B` and its `B tensor B` second-moment contribution remain. It would not establish localization prediction, a preferred physical mode, a universal dark-space dimension, a scalar chi for the active sector, or optimality at chi=1.

No localization outcome may be used to choose the dark subspace, active complement, basis, factor dimension, degeneracy tolerance, or any subsequent scalar reduction.
