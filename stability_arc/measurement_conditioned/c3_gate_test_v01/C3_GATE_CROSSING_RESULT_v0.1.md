# Prospective c3-gate class-crossing test v0.1 result

**Status:** PASS_PROSPECTIVE_C3_GATE_H5
**Scope:** FRESH_MECHANISM_TEST
**Canonical run:** `33263959965`
**Execution commit:** `ea27b9be79df3a88ce426551328c024eefce579e`

## Frozen source identities

- preregistration SHA-256: `2c7c853ac0eb23c611e3dfcd9f04648a083e2f37094026fca911610a319c6564`
- audit-code SHA-256: `41cf22bfebd62f2f3d2d5fb160594b84f55d55bffdf20607cc4ae1e59e60358b`
- workflow SHA-256: `8f7aae18ff49ded0a5fed973494044b008e20d375c1255ada29b53c3b3062112`
- c3 derivation result SHA-256: `40e2c96b37a382d59d11edae5e57ae350405a22f3eff35cda899adc7441a1ebc`
- upstream H4 result SHA-256: `50a65476b7dc7d982a8dbaccd2633384a0b5b988c37f02ca1eaf13aa81a135ff`

## Preserved evidence

- artifact ID: `9718065233`
- artifact ZIP SHA-256: `bbb525b48a9a64713a2050e8d6cd8c197adebd42ad4fe6eb72322225056048cb`
- artifact size: 6025386 bytes
- candidate-input SHA-256: `baf2e2e422bc65432438fe6784c194072c7c47b348063c67662dfbd2c88f7ec9`
- Stage-A frozen selection SHA-256: `e3c5c17ff1c9267f46b412e5ec87952ca6365a4473b14d271e3e8c7beca2fe6c`
- runner environment: Python 3.12.14, NumPy 2.1.3

The workflow independently verified all evidence files before artifact upload.

## Two-stage execution

H5 used new seed `2026082907` and the unchanged pre-H4 target-region generator.

### Stage A: physical only

Exactly 100000 fresh candidate inputs were generated.

Only the physical channel was constructed. `52944` candidates satisfied the frozen robust physical mean-square stability condition

`alpha_phys/R < -1e-6`.

Their IDs and physical normalized spectral abscissae were frozen and SHA-256 hashed before any record-channel construction.

### Stage B: record reveal

The record channel was then constructed for exactly the immutable 52944 Stage-A cases.

Exactly `54` robust physical STABLE -> record UNSTABLE crossings were found using the frozen condition

`alpha_rec/R > +1e-6`.

All `54/54` analytic crossings independently reconstructed from the full two-level Hilbert-space model.

No crossing was dropped, replaced, or selected by its Routh-Hurwitz pattern.

## Frozen gate results

All Y0-Y6 gates passed.

- **Y0 input determinism:** PASS; fresh candidate input hash reproduced exactly.
- **Y1 Stage-A freeze:** PASS; 52944 robust physical STABLE cases, frozen before record reveal.
- **Y2 reveal integrity:** PASS; record channel evaluated exactly the frozen Stage-A set; 54 robust crossings.
- **Y3 independent reconstruction:** PASS; 54/54 crossings reconstructed.
- **Y4 exact c3 identity:** PASS; maximum relative-or-absolute exact-quadratic versus determinant error `4.344084788515155e-13`, below frozen `2e-10` gate.
- **Y5 prospective mechanism pattern:** PASS; zero counterexamples. Every reconstructed crossing satisfied the frozen normalized sign pattern `m1_rec>1e-9`, `m2_rec>1e-9`, `m3_rec<-1e-9`, `mh_rec>1e-9`. The preregistered minimum of 20 crossings for population-level promotion was exceeded.
- **Y6 controls:** PASS; eta-zero identity, c3-only unstable control, multi-gate rejection control, and exact c3 boundary control all behaved as registered.

Overall status:

`PASS_PROSPECTIVE_C3_GATE_H5`.

## Scientific consequence

The earlier H4 observation that all 50 fresh target-region crossings had a negative record `c3` with the other three cubic Routh-Hurwitz margins positive has now reproduced prospectively on a new seed.

In H5, all 54 independently reconstructed robust crossings again had

`c1_rec > 0`,

`c2_rec > 0`,

`c3_rec < 0`,

`c1_rec*c2_rec-c3_rec > 0`.

Within this frozen high-kappa/high-omega, near-measurement-axis, `x*z<0` target family, the supported class-crossing mechanism is therefore a **record-channel c3-gate loss** rather than a simultaneous multi-gate failure.

This does not make `c3` a universal failure gate. H5 is bounded to the registered target family.

## Joint-channel interpretation

The physical and same-record channels remain separate objects. The result supports studying the displacement between their separate `c3=0` boundary surfaces, but not averaging those boundaries or collapsing the stochastic geometry to a single scalar.

The next justified step is to derive a boundary-displacement representation and test whether c3-surface displacement has prospective predictive value for true full Routh-Hurwitz class crossings on another untouched seed, with all non-c3 margins retained as mandatory admissibility information.

## Interpretation firewall

This PASS does not license:

- universal c3 dominance outside the frozen target family;
- a stochastic scalar chi;
- localization, collapse, or measurement-quality prediction;
- erasure of H2 FAIL, H3 bounded PASS, or H4/H5 selection boundaries.
