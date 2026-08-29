# Joint-channel representation audit v0.1 failure-signal report

**Frozen audit status:** FAIL
**Workflow run:** `33234191815`
**Head commit:** `eca8b7dfe958665ba1e32689c7d006e8ee51a402`
**Artifact:** `9709402456`
**Artifact ZIP SHA-256:** `f95209cf3ae0480722e0391224e78ba663136387c141891bbc47f614e05f6f98`

## Classification

**MATHEMATICAL SPECIFICATION / NORMALIZATION ERROR, with two additional representation-audit weaknesses found during failure investigation before any v0.2 execution.**

This is not a CI failure. It does not overturn the earlier v0.1 conditional-tangent finite-difference derivation, but it prevents the new joint-channel representation from being considered closed.

## Exact failed gate

Only `R0` failed numerically in the frozen run.

- frozen v0.1 R0 error: `0.4099999999999999`
- frozen R0 gate: `5e-13`
- `R1`: PASS, max centered-finite-difference error `4.5008885507513696e-11`
- `R2`: PASS, conditioning-difference residual `5.551115123125783e-17`, numerical rank `1`
- `R3`: PASS, joint characteristic-polynomial residual `7.105427357601002e-15`
- `R4`: PASS, coordinate-change invariants within floating-point residuals
- `R5`: PASS, exact 2x2 recovery and all scalar-refusal controls

Overall v0.1 remains **FAIL** and is not retroactively repaired.

## What R0 revealed

The preregistration asserted that the unconditional measurement term `2 kappa D[x]`, with `x=sigma_z/2`, contributes `-2 kappa` to the Bloch-x and Bloch-y tangent rates. Direct operator algebra shows that this is wrong.

Because

`D[x](rho) = x rho x - 1/2 {x^2,rho}`

and `x=sigma_z/2`, one has

`D[x](rho) = 1/4 (sigma_z rho sigma_z - rho)`.

Therefore

`2 kappa D[x](rho) = (kappa/2) (sigma_z rho sigma_z - rho)`.

On either `sigma_x/2` or `sigma_y/2`, conjugation by `sigma_z` changes the sign, so the parenthesis contributes minus twice that basis element. The net Bloch-coordinate rate is therefore `-kappa`, not `-2 kappa`.

For the frozen v0.1 values,

`gamma/2 + kappa = 0.23/2 + 0.41 = 0.525`,

which exactly matches the reconstructed physical drift entries `A_phys[0,0]=A_phys[1,1]=-0.525`.

The incorrect preregistered expression used `gamma/2 + 2 kappa = 0.935`; its discrepancy from the reconstructed rate is exactly `0.41 = kappa`, explaining the failed R0 residual.

## Additional latent issue 1: diffusion normalization

During adversarial review of the failed v0.1 package, a second normalization problem was found in the reported diffusion matrix `B`.

The registered tangent equation is

`d(delta rho) = L(delta rho) dt + sqrt(2 eta kappa) deltaH_x dW`

for the same-noise channel, with the same stochastic coefficient in the same-record channel. Therefore, if the Bloch-coordinate representation is written as

`d r = A r dt + B r dW`,

then the matrix `B` must include the prefactor `sqrt(2 eta kappa)`.

The v0.1 implementation stored only the Bloch matrix of `deltaH_x`, omitting that prefactor, while labeling the result as the full SDE diffusion matrix `B`. Its R1 finite-difference test compared the unscaled derivative of `H_x` against the same unscaled matrix, so R1 could pass without detecting the representational omission.

This does **not** alter the earlier derivation identity itself. It means the newly introduced matrix representation in v0.1 mislabeled an unscaled derivative operator as the full stochastic diffusion matrix.

## Additional latent issue 2: R2 self-certification

The v0.1 R2 implementation formed

`Delta_expected = -4 eta kappa h m^T`

then defined

`A_rec = A_phys + Delta_expected`

and finally checked

`A_rec-A_phys` against `Delta_expected`.

That comparison is algebraically guaranteed by construction and therefore is not an independent verification of the same-record drift representation. The rank-one result is still a valid property of the constructed update, but the v0.1 R2 PASS cannot by itself establish that the full nonlinear same-record map has that local drift.

A corrective audit must reconstruct `A_rec` independently from the full same-record map while holding detector records fixed, then compare that independently obtained drift against the analytic conditioning formula.

## Signal interpretation

The v0.1 failure and latent review findings expose a broader hazard: coefficients in stochastic/Lindblad equations cannot be promoted into Stability Arc coordinates by visual inspection, and an audit cannot certify a formula using an object defined from that same formula.

This constrains future measurement work in three ways:

1. damping rates must be derived from the generator action in the chosen operator normalization, not inferred from the coefficient written in front of a dissipator;
2. stochastic tangent matrices must include their full noise amplitude before any spectrum, norm, cross-channel comparison, or candidate scalar is interpreted;
3. joint-channel identities require an independent reconstruction route, not construction-then-comparison to the same expression.

## Next justified action

A new version may test the corrected algebraic control

`A_control = [[-(gamma/2+kappa),0,omega],[0,-(gamma/2+kappa),0],[-omega,0,-gamma]]`

and the correctly normalized diffusion matrix

`B = sqrt(2 eta kappa) * D(H_x)[rho]`

using fresh parameter/base-state fixtures chosen before execution. It must independently recover same-noise and same-record local drifts/diffusions from the full nonlinear maps using fixed `+/-dW` detector increments, rather than defining `A_rec` from the formula being tested.

The v0.1 failure and all latent weaknesses must remain preserved and may not be counted as support for the corrected formulas. Fresh v0.2 fixtures are required for corrective evidence.
