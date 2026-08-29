# Stochastic dark/active compatibility and quotient-closure audit v0.1 result

**Status:** PASS
**Scope:** STOCHASTIC_QUOTIENT_CLOSURE_ONLY
**Canonical run:** `33255726584`
**Execution commit:** `2394f836902bddc934eda3fae1cd31e71a7c27d9`

## Frozen source identities

- preregistration SHA-256: `cd201a8279860dbf14708c7c744fdc8fa59487b4f8bf52b2546fcf078ab6e40a`
- code SHA-256: `3a8b969d656d9035050fe66073dc1bf3ae9735906b7432a7211b3e671a135164`
- workflow SHA-256: `e67708350d88f3b141205a38d36af8133a0e12c1ec6a1f13755509a502d5bdef`
- upstream active-quotient result SHA-256: `ee7a58632fd68e29e15c89d3c7e0e4ed4a809fbfca9e92f6aa9f8e586f42ccd8`

## Evidence artifact

- artifact ID: `9715736382`
- artifact ZIP SHA-256: `2572a5197475e6d586663b4607f4ce5ff087a302fead240ccb7b39900674d360`
- result JSON SHA-256: `985f21fdd278c44503045716eb124b6a9906202b642da3775e8bd623dbdfc21e`
- stdout SHA-256: `f270150f0ca3c2ca3a7ab4e27e1b253af551d0d6c1c7f329347d3d2dc313b855`
- environment lock SHA-256: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- source-identity record SHA-256: `b2694e20899d13b3f6b2a95fa2c8ab44787a0b239ea055135fb4ac8b7abbd429`

The artifact manifest independently verified all recorded files before upload.

## Frozen gate results

All preregistered S0-S7 gates passed.

- **S0 source/state validity:** PASS. Minimum fresh density-matrix eigenvalue `0.29179337186342985`; maximum imaginary matrix entry `0.0`.
- **S1 independent deterministic dark reconstruction:** PASS. Maximum residual `2.642330798607873e-16`.
- **S2 stochastic compatibility:** PASS. Maximum `B D` leakage outside the independently reconstructed deterministic dark subspace was `2.900837493222097e-17`.
- **S3 quotient intertwining:** PASS. Maximum residual across `L A=A_A L` and `L B=B_A L` was `2.669225551699129e-16`.
- **S4 complement/basis covariance:** PASS. Maximum matrix and characteristic-polynomial residuals were each `2.220446049250313e-16` under the frozen non-orthogonal complement shear plus active-basis change.
- **S5 direct trajectory quotient closure:** PASS. Maximum projected full-vs-quotient Euler-Maruyama state residual was `5.551115123125783e-17`, including distinct dark lifts of the same active state.
- **S6 second-moment generator/direct covariance closure:** PASS. Maximum moment-generator intertwining residual `2.72301505788164e-16`; maximum projected full-vs-quotient covariance residual `5.551115123125783e-17`.
- **S7 refusal behavior / scalar firewall:** PASS. All six refusal controls returned exactly the preregistered states.

## Exact licensed consequence

For every admitted fresh quantum fixture, the same independently reconstructed one-dimensional deterministic conditioning-dark subspace `D` satisfied both

`A D subset D`

and

`B D subset D`.

Therefore the full local multiplicative-noise SDE

`d r = A r dt + B r dW`

descends exactly to the same two-dimensional quotient used by the deterministic active-sector analysis:

`d q = A_A q dt + B_A q dW`.

Equivalently, with quotient map `L`,

`L A = A_A L`,

`L B = B_A L`,

and at second-moment level

`(L tensor L) K(A,B) = K(A_A,B_A) (L tensor L)`.

This is stronger than deterministic factorization alone: active stochastic evolution is independent of which representative is chosen along the dark fiber.

The result does **not** imply that the dark coordinate is noise-free. `B` may act nontrivially inside `D`; the licensed statement is quotient closure, not stochastic silence.

## Fresh deterministic-scalar metadata

The already-licensed deterministic active-quotient coordinate was recorded only as metadata:

- SQ1: physical `0.2796412975644207`; record-conditioned `0.3691335201738627`;
- SQ2: physical `0.26163798988867515`; record-conditioned `0.3203100921721253`;
- SQ3: physical `0.3324963170859862`; record-conditioned `0.46397186484897024`.

No directionality or localization interpretation is promoted from these values.

For every admitted stochastic quotient, the registered status remains

`STOCHASTIC_PAIR_NOT_COMPRESSED`.

No noise-aware scalar is licensed.

## Refusal controls

The audit preserved the required failure boundaries exactly:

- RQ1: `REFUSE_STOCHASTIC_LEAKAGE`
- RQ2: `REFUSE_QUOTIENT_DIMENSION`
- RQ3: `REFUSE_NO_DARK_FACTOR`
- RQ4: `REFUSE_CROSS_SECTOR_DEGENERACY`
- RQ5: `REFUSE_DEFECTIVE_ACTIVE_SECTOR`
- RQ6: `REFUSE_COORDINATE_FAILURE`

A deterministic `chi_active` is therefore not sufficient to license stochastic quotient use when `B` leaks across the dark/active split.

## Interpretation firewall

This PASS establishes exact stochastic quotient closure for the admitted local tangent controls. It does not establish localization prediction, collapse, measurement-quality optimization, a stochastic analogue of `chi`, or a preferred value near `chi=1`.

The next justified question is the stability geometry of the exact 2D stochastic quotient itself. Because second moments evolve under a real 3x3 generator, any noise-aware stability criterion must be derived from that operator or its coordinate invariants rather than fitted to historical localization outcomes.
