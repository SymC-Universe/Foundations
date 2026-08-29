# Joint-channel conditional-stability representation audit v0.2 result

**Status:** PASS
**Scope:** CORRECTIVE_REPRESENTATION_AUDIT_ONLY
**Canonical workflow run:** `33234401976`
**Canonical execution commit:** `1840750ce94ad5f3a62d9199ab14c9aee81dfe68`

## Lineage

v0.2 is the corrective successor to the preserved v0.1 **FAIL** in run `33234191815`. The v0.1 failure is not erased or relabeled.

Failure investigation identified three issues that v0.2 had to address prospectively:

1. the v0.1 unconditional-control formula used transverse measurement damping `2*kappa` for `2*kappa D[sigma_z/2]`; the correct Bloch damping is `kappa`;
2. the v0.1 matrix labeled `B` omitted the SDE prefactor `sqrt(2 eta kappa)`;
3. the v0.1 conditioning-difference gate partly self-certified because `A_rec` was constructed from the same formula being checked.

The v0.2 preregistration froze the corrected identities, three fresh parameter/base-state fixtures, and an independent full-nonlinear-map finite-difference reconstruction before execution.

## Frozen source identities used by the canonical run

- preregistration SHA-256: `31dca30a5817bbdad8cdd1665c3e21ab86881a7d3a37b3bdae4f4e5350742517`
- audit-code SHA-256: `065b881c10ebe45159867cbf7b57000f00ee8c221a50f4f4b4789511bdfbc5f2`
- execution-workflow SHA-256: `cf1bc5d393ee14f13b470f470471a153225c2891ad18cd389c6f4b88948fa4e2`
- preserved v0.1 failure-report SHA-256 at execution: `7c1b89190fbc334195d638e1e2120a4153a14969c2c60a9f59394ab831e3dcdc`

Environment: Python `3.12.14`, NumPy `2.1.3`, Ubuntu 24.04 hosted runner.

## Frozen corrective results

All v0.2 gates passed.

### R0 corrected unconditional-control reconstruction: PASS

Across the three fresh fixtures, maximum absolute matrix-entry error was

`1.1102230246251565e-16`

against the frozen gate `5e-13`.

This supports the corrected identity for `x=sigma_z/2`:

`A_control = [[-(gamma/2+kappa),0,omega],[0,-(gamma/2+kappa),0],[-omega,0,-gamma]]`.

### R1 fully normalized diffusion reconstruction: PASS

The analytic full stochastic diffusion matrix

`B = sqrt(2 eta kappa) * D(H_x)[rho]`

was compared independently with matrices recovered from the full nonlinear same-noise and same-record one-step maps.

Maximum errors across fresh fixtures:

- analytic `B` vs same-noise finite-difference reconstruction: `3.209545684779158e-10`
- analytic `B` vs same-record finite-difference reconstruction: `1.168363461534483e-10`
- same-noise vs same-record finite-difference `B`: `2.0411822232446752e-10`

Frozen gate: `2e-6`.

### R2 independent same-record drift / conditioning difference: PASS

The physical and record-conditioned drifts were independently reconstructed from full nonlinear maps using fixed `+/-dW` records rather than defining the test object from the formula under test.

Maximum errors:

- `A_phys_FD` vs analytic `A_phys`: `3.1673200728832285e-09`
- `A_rec_FD` vs analytic `A_rec`: `2.632416729042575e-09`

Frozen drift gate: `2e-6`.

The conditioning-difference identity

`DeltaA = -4 eta kappa h m^T`

had maximum residual `5.551115123125783e-17`, and `DeltaA` had numerical rank `1` for all three fresh fixtures under the frozen `1e-12` rank tolerance.

### R3 joint characteristic-polynomial identity: PASS

For `A_joint = diag(A_phys,A_rec)`, the maximum residual between the joint characteristic polynomial and the product of the two channel characteristic polynomials was

`3.552713678800501e-15`

against the frozen `5e-10` gate.

This verifies that the joint representation retains both channel spectra rather than replacing them with an averaged spectrum.

### R4 common-coordinate invariance: PASS

Under the fixed common Bloch rotation `Q=Rz(0.37) Ry(-0.52) Rx(0.29)`:

- maximum characteristic-polynomial coefficient change: `3.1086244689504383e-15`
- maximum `DeltaA` Frobenius-norm change: `0.0`
- maximum fully normalized `B` Frobenius-norm change: `5.551115123125783e-17`

All are within the frozen gates.

### R5 exact second-order recovery and scalar refusal: PASS

The explicit real stable 2x2 extractor recovered `Gamma/(2 Omega)` exactly for all three registered oscillator controls, including the registered `chi=1.0` case.

It refused:

- wrong-shape 3x3 input;
- materially complex 2x2 input;
- nonpositive determinant;
- nonnegative-trace/unstable input.

The full 3x3 `A_phys` and `A_rec` remain explicitly `FULL_MATRIX_REQUIRED`. v0.2 does not license scalar compression of either channel.

## Structural result of the conglomerate representation

The same-noise and same-record channels are now simultaneously represented without conflation:

`C = (A_phys, A_rec, DeltaA, B, A_joint)`.

For the registered single-observable convention they share the same fully normalized stochastic tangent matrix `B`, while measurement conditioning changes the deterministic local drift through the rank-one update `DeltaA`.

This means the joint description contains information that neither channel alone records: it identifies exactly which part of local perturbation dynamics is introduced by conditioning on the measurement record while preserving the physical and inference channels independently.

The three fresh fixtures also showed nonzero commutators between `A_phys` and `A_rec`, so the conditioning update generally changes more than eigenvalue magnitudes; the two drift operators are not simply interchangeable rescalings in these fixtures. This is a representation-level observation only.

## Preserved evidence

Artifact ID: `9709462702`
Artifact ZIP SHA-256: `0ae0bf6cb694aacada0ad54427d3d56ae694868e5179702ef7d12159e4f56be9`
Artifact size: 8490 bytes
Artifact retention expiry: 2026-11-27

Internal artifact SHA-256 values:

- `environment_lock.txt`: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- `joint_channel_representation_audit_v02.json`: `b29255c8957e252437476ecebf44df0ecf3cf383a4271060525069c8127c1116`
- `stdout.txt`: `b29255c8957e252437476ecebf44df0ecf3cf383a4271060525069c8127c1116`
- `source_identity.txt`: `b2ce772678d66faaf61dfdbf0264465c89bd241a40562929beb9a21e7ca0e841`

The artifact manifest independently verified all hashed files as `OK`.

After the canonical execution, the workflow path filter was narrowed at commit `5ca907f8bc8c381a4d4343f8690b3b0ac0ed01d9` so result/provenance documentation changes do not trigger redundant scientific reruns. This changed orchestration only, not the executed v0.2 science.

## Interpretation firewall

This PASS licenses the corrected instantaneous separate-plus-joint stochastic tangent representation and its registered algebraic/reconstruction checks only.

It does **not** establish that any drift spectrum, joint spectrum, conditioning difference, or scalar predicts localization. It does not establish a universal scalar chi for conditional quantum dynamics and does not establish an optimum at `chi=1`.

The next justified representation question is whether stochastic perturbation stability should be evaluated at the moment/covariance level, where the common diffusion matrix `B` contributes explicitly, rather than from drift spectra alone. That question requires its own preregistered audit before any localization outcomes are consulted.
