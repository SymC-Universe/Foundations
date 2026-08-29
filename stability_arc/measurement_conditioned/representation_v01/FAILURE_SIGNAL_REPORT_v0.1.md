# Joint-channel representation audit v0.1 failure-signal report

**Frozen audit status:** FAIL
**Workflow run:** `33234191815`
**Head commit:** `eca8b7dfe958665ba1e32689c7d006e8ee51a402`
**Artifact:** `9709402456`
**Artifact ZIP SHA-256:** `f95209cf3ae0480722e0391224e78ba663136387c141891bbc47f614e05f6f98`

## Classification

**MATHEMATICAL SPECIFICATION / ANALYTIC CONTROL ERROR.**

This is not a CI failure and not a failure of the already-validated same-noise/same-record tangent identities. The frozen v0.1 analytic unconditional-control formula contained a factor-of-two error in the measurement-dephasing contribution.

## Exact failed gate

Only `R0` failed.

- frozen v0.1 R0 error: `0.4099999999999999`
- frozen R0 gate: `5e-13`
- `R1`: PASS, max centered-finite-difference error `4.5008885507513696e-11`
- `R2`: PASS, conditioning-difference residual `5.551115123125783e-17`, numerical rank `1`
- `R3`: PASS, joint characteristic-polynomial residual `7.105427357601002e-15`
- `R4`: PASS, coordinate-change invariants within floating-point residuals
- `R5`: PASS, exact 2x2 recovery and all scalar-refusal controls

Overall v0.1 remains **FAIL** and is not retroactively repaired.

## What the failure revealed

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

## Signal interpretation

This failure is useful because it exposed a normalization hazard in carrying Lindblad measurement coefficients into Bloch-coordinate damping rates. The factor multiplying `D[x]` cannot be read directly as the transverse Bloch damping rate when the measured operator itself contains a scale factor (`x=sigma_z/2`).

The failure therefore constrains future Stability Arc measurement work: damping coordinates must be derived from the actual generator action in the chosen operator normalization, not inferred from the coefficient written in front of a dissipator.

## Next justified action

A new version may test the corrected algebraic control

`A_control = [[-(gamma/2+kappa),0,omega],[0,-(gamma/2+kappa),0],[-omega,0,-gamma]]`

using fresh parameter fixtures chosen before execution. The v0.1 failure must remain preserved and may not be counted as support for the corrected formula. The other v0.1 gates may be retained as regression checks, but their previous PASS values are not new prospective evidence.
