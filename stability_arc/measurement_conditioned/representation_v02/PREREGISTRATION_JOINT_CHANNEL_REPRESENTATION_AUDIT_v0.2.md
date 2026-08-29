# Joint-channel conditional-stability representation audit v0.2

**Status:** FROZEN BEFORE EXECUTION
**Lineage:** corrective successor to preserved v0.1 FAIL

## Why v0.2 exists

Audit v0.1 failed R0 because its preregistered analytic control treated the coefficient `2 kappa D[sigma_z/2]` as though it produced transverse Bloch damping `2 kappa`. Operator algebra shows the correct transverse Bloch damping is `kappa` because the measured operator includes the factor `1/2`.

Adversarial review of the failed v0.1 package also found two additional weaknesses before any v0.2 execution:

1. the reported diffusion matrix `B` omitted the required SDE prefactor `sqrt(2 eta kappa)`;
2. the v0.1 conditioning-difference check constructed `A_rec` from the same formula it then checked, so that gate was not sufficiently independent.

These issues are preserved in the v0.1 failure record. The v0.1 result remains failed. No v0.1 threshold, output, or interpretation is rewritten.

## Representation convention

At a fixed instantaneous base state `rho`, use the traceless-Hermitian Bloch basis

`E=(sigma_x/2,sigma_y/2,sigma_z/2)`

and write `delta rho = sum_j r_j E_j`.

The same-noise local tangent is represented by

`d r = A_phys r dt + B r dW`,

and the same-record local tangent by

`d r = A_rec r dt + B r dW`.

The correctly normalized diffusion matrix is

`B = sqrt(2 eta kappa) * B_H`,

where `B_H` is the Bloch-coordinate Jacobian of `H_x(rho)`.

The same-record conditioning drift difference is

`DeltaA = A_rec-A_phys = -4 eta kappa h m^T`,

where `h` is the Bloch-coordinate vector of `H_x(rho)` and `m_j=Tr(x E_j)`.

The ordered joint object is

`C=(A_phys,A_rec,DeltaA,B,A_joint)`

with `A_joint=diag(A_phys,A_rec)`.

This is an instantaneous local stochastic-tangent representation. It is not called a global generator, and no single scalar is implied.

## Corrected unconditional-control identity

For `x=sigma_z/2`,

`2 kappa D[x](rho)=(kappa/2)(sigma_z rho sigma_z-rho)`.

Therefore

`A_control = [[-(gamma/2+kappa),0,omega],[0,-(gamma/2+kappa),0],[-omega,0,-gamma]]`.

## Fresh fixtures

All corrected identities must be tested on the following three parameter/base-state fixtures, none of which appeared in v0.1:

1. `eta=0.64, gamma=0.11, kappa=0.17, omega=0.83, base=(0.12,-0.18,0.27)`
2. `eta=0.81, gamma=0.37, kappa=0.29, omega=1.31, base=(-0.31,0.22,-0.14)`
3. `eta=0.55, gamma=0.52, kappa=0.07, omega=0.61, base=(0.05,0.33,0.41)`

All base Bloch vectors lie strictly inside the Bloch ball. For every fixture use `x=sigma_z/2`, `H=omega sigma_y/2`, amplitude-damping collapse amplitude `sqrt(gamma)`, and unconditional measurement term `2 kappa D[x]`.

No parameter was selected from a v0.2 outcome.

## Independent full-map decomposition fixture

To avoid self-certification, v0.2 must independently recover local drift and diffusion matrices from the full nonlinear one-step maps, not only from the analytic tangent formulas.

Freeze:

- `dt = 1e-3`
- normalized innovation magnitude `z = 0.43`
- `dW = z sqrt(dt)` and `-dW`
- centered state perturbation `epsilon = 1e-5`

For same-noise maps, construct centered state Jacobians `J_noise+` and `J_noise-` at `+dW` and `-dW`.

Recover

`A_phys_FD = ((J_noise+ + J_noise-)/2 - I)/dt`

and

`B_noise_FD = (J_noise+ - J_noise-)/(2 dW)`.

For same-record maps, hold the base detector records

`dY+ = sqrt(8 eta kappa) mu(rho) dt + dW`

and

`dY- = sqrt(8 eta kappa) mu(rho) dt - dW`

fixed while each perturbed candidate state constructs its own innovation. Build `J_record+` and `J_record-`, then recover

`A_rec_FD = ((J_record+ + J_record-)/2 - I)/dt`

and

`B_record_FD = (J_record+ - J_record-)/(2 dW)`.

These finite-difference matrices are the independent comparison route for R1 and R2.

## Frozen gates

### R0 corrected unconditional-control reconstruction

For every fresh fixture, reconstruct `A_phys` by applying the Liouvillian to the Bloch basis and compare with the corrected analytic `A_control` above.

PASS requires maximum absolute matrix-entry error <= `5e-13` for every fixture.

### R1 fully normalized diffusion reconstruction

For every fresh fixture, construct the analytic full diffusion matrix

`B = sqrt(2 eta kappa) * D(H_x)[rho]`.

Compare it independently against both `B_noise_FD` and `B_record_FD` recovered from the full nonlinear maps above.

PASS requires maximum absolute entry error <= `2e-6` for each comparison and maximum difference between `B_noise_FD` and `B_record_FD` <= `2e-6`.

### R2 independent same-record drift / conditioning-difference identity

For every fresh fixture, construct

`A_rec_formula = A_phys - 4 eta kappa h m^T`.

Compare it against independently recovered `A_rec_FD` from the full same-record map. Also compare `A_phys` against `A_phys_FD` from the full same-noise map.

PASS requires maximum absolute entry error <= `2e-6` for both drift comparisons.

For the analytic difference

`DeltaA = A_rec_formula-A_phys`,

PASS additionally requires agreement with `-4 eta kappa h m^T` to `5e-13` and numerical rank <=1 using absolute singular-value tolerance `1e-12`.

### R3 joint characteristic-polynomial identity

For every fresh fixture construct `A_joint=diag(A_phys,A_rec_formula)`.

PASS requires

`poly(A_joint)=convolution(poly(A_phys),poly(A_rec_formula))`

with maximum absolute coefficient residual <= `5e-10`.

### R4 fixed coordinate-change invariance

Apply the same fixed orthogonal rotation

`Q=Rz(0.37) Ry(-0.52) Rx(0.29)`

to all analytic representation matrices by similarity. For every fresh fixture PASS requires:

- characteristic-polynomial coefficient changes for `A_phys`, `A_rec_formula`, and `DeltaA` <= `5e-10`;
- Frobenius-norm changes for `DeltaA` and the fully normalized `B` <= `5e-13`.

### R5 exact second-order recovery and scalar refusal

The only scalar extraction licensed in v0.2 is from an explicitly supplied real 2x2 block `A` satisfying `tr(A)<0` and `det(A)>0`:

`chi_block=-tr(A)/(2 sqrt(det(A)))`.

Verify exact recovery of `Gamma/(2 Omega)` to `1e-14` for:

- `(m,Omega,Gamma)=(1,1,0.6)`
- `(2.3,0.7,1.4)`
- `(0.4,2.1,5.0)`

The extractor must REFUSE wrong-shape matrices, materially complex 2x2 matrices, `tr>=0`, or `det<=0`.

The full 3x3 `A_phys` and `A_rec_formula` from every fresh fixture remain `FULL_MATRIX_REQUIRED`. No invariant-subspace discovery or scalar compression is licensed here.

## Decision rule

Overall v0.2 PASS requires `R0 & R1 & R2 & R3 & R4 & R5` for the fresh fixtures and registered scalar controls.

No parameter, fixture, coefficient, threshold, rotation, scalar-admission rule, or equation may change inside v0.2 after execution.

## Anti-circularity firewall

This audit reads no historical localization outcome, no E16-E27 error, and no GFSA v0.7 external-candidate response. All corrections are explicitly post-v0.1-failure and were frozen before v0.2 execution. Only the three fresh v0.2 fixtures may provide new corrective evidence for those identities.

A v0.2 PASS would license only the corrected local separate-plus-joint matrix representation and its algebraic invariants. It would not establish predictive value for localization, a universal scalar chi, or an optimum at chi=1.
