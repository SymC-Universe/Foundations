# Joint-channel conditional-stability representation audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Scope

This is an outcome-free mathematical representation audit. It does not read or score any historical localization outcome, E16-E27 position error, GFSA v0.7 external-candidate response, or measurement-performance holdout.

The same-noise physical tangent and same-record inference tangent remain separate auditable objects. This audit additionally constructs their joint/comparative representation without averaging, fitting, or collapsing them into one scalar.

## Frozen model

Use exactly the two-level fixture already registered in the conditional tangent derivation audit v0.1:

- `eta = 0.73`
- `kappa = 0.41`
- `omega = 1.17`
- `gamma = 0.23`
- `x = sigma_z/2`
- `H = omega sigma_y/2`
- amplitude-damping collapse amplitude `sqrt(gamma)`
- unconditional measurement term `2 kappa D[x]`
- base Bloch vector `(0.20,-0.25,0.30)`

Use the traceless-Hermitian Bloch basis `E=(sigma_x/2,sigma_y/2,sigma_z/2)`.

For a tangent coordinate vector `r`, write `delta rho = sum_j r_j E_j`.

The same-noise tangent is represented by the pair `(A_phys,B)`:

`d r = A_phys r dt + B r dW`.

The same-record tangent is represented by `(A_rec,B)`:

`d r = A_rec r dt + B r dW`,

with the registered conditioning drift correction

`A_rec - A_phys = -4 eta kappa h m^T`,

where `h` is the Bloch-coordinate vector of `H_x(rho)` and `m_j = Tr(x E_j)`.

The joint representation is the ordered tuple

`C = (A_phys, A_rec, DeltaA, B, A_joint)`,

where `DeltaA=A_rec-A_phys` and `A_joint=diag(A_phys,A_rec)`.

No element of this tuple may be replaced by an average or outcome-selected weighted combination inside v0.1.

## Analytic unconditional control

For this frozen convention, the unconditional measurement-dressed physical drift in the Bloch basis must equal

`A_control = [[-(gamma/2+2 kappa), 0, omega], [0, -(gamma/2+2 kappa), 0], [-omega, 0, -gamma]]`.

This is a control identity only. It is not a localization claim.

## Frozen gates

### R0 unconditional-control reconstruction

Construct `A_phys` independently by applying the Liouvillian to each Bloch basis element. PASS requires maximum absolute matrix-entry error versus `A_control` <= `5e-13`.

### R1 diffusion-tangent reconstruction

Construct `B` from the analytic first variation `delta H_x`. Independently reconstruct each column using a centered finite difference of the nonlinear `H_x(rho)` map with `epsilon=1e-6`. PASS requires maximum absolute entry error <= `5e-10`.

### R2 conditioning-difference identity

Construct `A_rec` from the registered same-record tangent and verify

`DeltaA = A_rec-A_phys = -4 eta kappa h m^T`.

PASS requires maximum absolute entry residual <= `5e-13`. The singular values of `DeltaA` must also have numerical rank <=1 using absolute tolerance `1e-12`.

### R3 joint characteristic-polynomial identity

Construct `A_joint=diag(A_phys,A_rec)`. PASS requires

`poly(A_joint) = convolution(poly(A_phys),poly(A_rec))`

with maximum absolute coefficient residual <= `5e-10`.

This verifies that the joint representation retains both spectra rather than manufacturing a new averaged spectrum.

### R4 fixed coordinate-change invariance

Apply the same fixed orthogonal Bloch-coordinate rotation

`Q = Rz(0.37) Ry(-0.52) Rx(0.29)`

to all channel matrices by similarity. PASS requires, for each of `A_phys`, `A_rec`, and `DeltaA`, maximum characteristic-polynomial coefficient change <= `5e-10`; Frobenius norms of `DeltaA` and `B` must be invariant to <= `5e-13`.

### R5 exact second-order recovery and scalar refusal

The only scalar extraction licensed in v0.1 is from an explicitly supplied real 2x2 block `A` satisfying `tr(A)<0` and `det(A)>0`:

`chi_block = -tr(A)/(2 sqrt(det(A)))`.

For oscillator blocks `[[0,1/m],[-m Omega^2,-Gamma]]`, verify exact recovery of `Gamma/(2 Omega)` for `(m,Omega,Gamma)=(1,1,0.6),(2.3,0.7,1.4),(0.4,2.1,5.0)` to `1e-14`.

The extractor must REFUSE wrong-shape matrices, materially complex 2x2 matrices, `tr>=0`, or `det<=0`.

**Important:** neither the full 3x3 `A_phys` nor full 3x3 `A_rec` may be compressed to a scalar in v0.1. Their output is `FULL_MATRIX_REQUIRED` unless a separately preregistered invariant-subspace extraction rule is later established.

## Decision rule

Overall PASS requires `R0 & R1 & R2 & R3 & R4 & R5`.

A failed gate remains failed. No fixture, coefficient, tolerance, basis rotation, scalar-admission rule, or analytic identity may be changed inside v0.1 after execution. A replacement requires a new version that preserves this result.

## Interpretation firewall

A PASS licenses only the ordered joint representation `C`, the exact rank-one conditioning-drift identity for the frozen model, coordinate-invariant matrix diagnostics, and conservative scalar refusal. It does not establish that any channel or combination predicts localization, that a unique scalar chi exists for a conditional quantum generator, that chi=1 is optimal, or that the conditioning correction is universally rank one outside the registered single-observable normalized-filter convention.
