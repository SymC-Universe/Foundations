# Joint-channel conditional-stability representation audit v0.2

**Status:** FROZEN BEFORE EXECUTION
**Lineage:** corrective successor to preserved v0.1 FAIL

## Why v0.2 exists

Audit v0.1 failed R0 because its preregistered analytic control treated the coefficient `2 kappa D[sigma_z/2]` as though it produced transverse Bloch damping `2 kappa`. Operator algebra shows the correct transverse Bloch damping is `kappa` because the measured operator includes the factor `1/2`.

The v0.1 result remains failed and is preserved in `representation_v01/FAILURE_SIGNAL_REPORT_v0.1.md`. No v0.1 threshold or result is rewritten.

## Corrected algebraic identity

For `x=sigma_z/2`,

`2 kappa D[x](rho) = (kappa/2)(sigma_z rho sigma_z-rho)`.

Therefore the unconditional measurement-dressed Bloch tangent control is

`A_control = [[-(gamma/2+kappa),0,omega],[0,-(gamma/2+kappa),0],[-omega,0,-gamma]]`.

## Fresh R0 fixtures

The corrected R0 identity must be tested on parameter triples not used in v0.1:

1. `(gamma,kappa,omega) = (0.11,0.17,0.83)`
2. `(gamma,kappa,omega) = (0.37,0.29,1.31)`
3. `(gamma,kappa,omega) = (0.52,0.07,0.61)`

For each fixture use `x=sigma_z/2`, `H=omega sigma_y/2`, amplitude-damping collapse amplitude `sqrt(gamma)`, and unconditional measurement term `2 kappa D[x]`.

PASS requires maximum absolute matrix-entry error between the basis-reconstructed Liouvillian tangent and the corrected analytic control <= `5e-13` for every fresh fixture.

The original v0.1 fixture `(gamma,kappa,omega)=(0.23,0.41,1.17)` may be recorded as a regression value but cannot serve as the fresh corrective evidence.

## Joint representation regression gates

The following use the original v0.1 two-level base state `(0.20,-0.25,0.30)` only as implementation regression checks. Their thresholds and definitions are unchanged from v0.1:

- **R1:** centered finite-difference reconstruction of diffusion tangent `B`, epsilon `1e-6`, max entry error <= `5e-10`.
- **R2:** `DeltaA=A_rec-A_phys=-4 eta kappa h m^T`, max entry residual <= `5e-13`, numerical rank <=1 at absolute tolerance `1e-12`.
- **R3:** `poly(diag(A_phys,A_rec)) = convolution(poly(A_phys),poly(A_rec))`, residual <= `5e-10`.
- **R4:** fixed common coordinate rotation `Q=Rz(0.37) Ry(-0.52) Rx(0.29)` preserves characteristic polynomials to `5e-10` and Frobenius norms of `DeltaA` and `B` to `5e-13`.
- **R5:** explicit real stable 2x2 block extraction `chi_block=-tr(A)/(2 sqrt(det(A)))` recovers the same three registered oscillator controls to `1e-14`; wrong-shape, materially complex, `tr>=0`, and `det<=0` inputs are REFUSED. Full 3x3 `A_phys` and `A_rec` remain `FULL_MATRIX_REQUIRED`.

## Decision rule

Overall v0.2 PASS requires fresh-corrective `R0` plus regression `R1-R5` all PASS.

No parameter, fixture, coefficient, threshold, rotation, scalar-admission rule, or equation may change inside v0.2 after execution.

## Anti-circularity firewall

This audit reads no historical localization outcome, no E16-E27 error, and no GFSA v0.7 external-candidate response. The corrected formula was derived from operator normalization after v0.1 failure and therefore is explicitly post-failure. Only the three fresh R0 parameter fixtures may provide new corrective evidence for that formula.

A v0.2 PASS would license only the corrected unconditional-control algebra plus the separate-and-joint matrix representation. It would not establish predictive value for localization, a universal scalar chi, or an optimum at chi=1.
