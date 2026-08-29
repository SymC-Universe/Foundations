# Fresh targeted mean-square class-crossing v0.1 result

**Status:** PASS_TARGETED_CROSSING_H4
**Scope:** FRESH_TARGETED_CLASS_CROSSING_EXISTENCE_TEST
**Canonical run:** `33257117162`
**Execution commit:** `c09a6eface73b7d696b767e43bac78b1ef9af8bc`

## Lineage and evidentiary status

The preceding H3 phase remains a valid bounded prospective PASS on its frozen 512-case near-boundary panel.

Only after H3 closed did an exploratory equation-level search suggest rare STABLE -> UNSTABLE crossings elsewhere in the same measured-qubit family. That post-hoc lead was recorded separately and was not counted as evidence.

This H4 phase used a new seed, a frozen target-region generator, and a two-stage physical-only freeze before same-record reveal.

## Frozen source identities

- preregistration SHA-256: `7bd82b0e079d673dc7a19e83b80ceef4f1a0f38c7129ccbb57c01b1636ef708b`
- audit-code SHA-256: `10f333cb0d25448ef58f2d2dfa98a2f48ae9c274f8297704bbe56f941ffca3b5`
- workflow SHA-256: `d903881af405cce103b8b8eba28a5b45479ce3eaaa685eb1ef78bd0a378633f4`
- exploratory-lead SHA-256: `7d194f4a7af2228a2ffbfe45b729c93b6cd3b67ef8b61ddcf82663385b80c94e`
- bounded H3 result SHA-256: `3b48510393fc2fe8ad05da18905ab03152ae4c48a0a76bb953a94f9f208c091a`

## Preserved evidence

- artifact ID: `9716142827`
- artifact ZIP SHA-256: `6a781a83c83293e5b4103f23829094f044af1b265bc588f5051cf65ded33e549`
- candidate-input SHA-256: `86a7d9d95d0af3c9536ac7af9069a74da0c278bf51fdea6b50b1e502e25652a4`
- Stage-A frozen selection SHA-256: `6d782fe36fd1aee26f5c4a26c486c44430757b7fae95307ac7cb897160468600`
- result JSON SHA-256: `2db4215570b7cf8c2acbd448eaa62f4a910ca793fbe882783e27675326990c38`
- stdout SHA-256: `d5ab2dcc1a60e6f4a44184a77819c5f11c1770d0632bf6008d8f53c68d31e2b1`
- environment-lock SHA-256: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- source-identity SHA-256: `1d75bc7413576e4aab501fddc229ed49522e6111ff8c736a5a6fe707218b36f7`
- evidence-manifest SHA-256: `d6b564e36e11890822cb40d176a60596918e8170719d223b78c75181de1f6e58`

The workflow independently verified the Stage-A digest and full evidence manifest before artifact upload.

## Two-stage prospective execution

### Stage A: physical channel only

Exactly 100000 fresh inputs were generated from seed `2026082905` under the frozen target-region distribution.

No same-record drift was constructed during Stage A.

A total of `52435` candidates satisfied the preregistered robust physical mean-square stability condition

`alpha_phys/R < -1e-6`.

Their IDs and physical normalized spectral abscissae were frozen to bytes and hashed before Stage B.

### Stage B: same-record reveal

The same-record channel was then constructed for exactly the frozen 52435 Stage-A cases.

The frozen robust crossing rule was

`alpha_rec/R > +1e-6`.

Stage B produced exactly `50` analytic robust STABLE -> UNSTABLE crossing candidates.

All `50/50` were independently reconstructed from full two-level Hilbert-space operators and all 50 retained the robust class crossing.

No crossing was replaced, removed, or selected post-outcome.

## Frozen gate results

- **X0 generator determinism: PASS.** Input hash reproduced exactly.
- **X1 Stage-A freeze: PASS.** 52435 robust physical STABLE cases frozen before record reveal.
- **X2 analytic reveal: PASS.** 52435 frozen cases evaluated; 50 robust analytic crossings.
- **X3 independent reconstruction: PASS.** `50/50` analytic crossings independently verified.
- **X4 controls: PASS.** `eta=0` physical/record identity held; independent synthetic classifier control returned STABLE -> UNSTABLE.
- **X5 H4 existence: PASS.** At least one fresh independently reconstructed robust crossing existed; in fact there were 50.

Overall status:

`PASS_TARGETED_CROSSING_H4`.

## Example fresh crossing

The first preregistered-seed crossing was `XC002679`:

- `gamma=1`;
- `kappa=7.13390807096159`;
- `omega=5.531011477185077`;
- `eta=0.1436084182509635`;
- `x=+0.16060572259621236`;
- `z=-0.9850913026355294`;
- physical `alpha/R=-0.0030143664972786042`;
- record `alpha/R=+0.014695040970220617`.

Thus the crossing is well outside the frozen `1e-6` numerical ambiguity zone on both sides.

## Scientific conclusion

Mean-square stability-class preservation is **not universal even within this exact measured-qubit family**.

The earlier H3 PASS remains valid but must be stated narrowly:

> In the frozen H3 panel of 512 cases selected from 50000 candidates by smallest physical-only distance to the mean-square boundary, all 512 remained stable under same-record conditioning.

H4 now establishes a different bounded fact:

> In a fresh, preregistered high-`kappa/gamma`, high-`omega/gamma`, near-measurement-axis, `x*z<0` target region, robust physical STABLE -> record UNSTABLE crossings exist.

Those two results are compatible because the selection regimes are different.

## Post-outcome failure-signal observation

This subsection is exploratory relative to H4 and must not be treated as a preregistered mechanism claim.

Across all 50 fresh verified crossings, the record-channel cubic Routh-Hurwitz failure occurred through the constant polynomial coefficient `c3` becoming negative. In the same 50 cases:

- record `c1` remained positive;
- record `c2` remained positive;
- record `c1*c2-c3` remained positive;
- record `c3 < 0` in `50/50` cases.

The crossing sample had approximately:

- `kappa/gamma`: 3.77 to 89.99, median 24.57;
- `omega/gamma`: 3.03 to 75.18, median 17.27;
- `eta`: 0.0571 to 0.2137, median 0.1279;
- `|z|`: 0.9050 to 0.9990, median 0.9776;
- `x*z<0` by frozen construction.

This identifies `c3=0` as the immediate next mechanism-boundary candidate. It is a post-outcome observation and requires a new derivation/fresh test before promotion.

## Consequence for the joint/conglomerate picture

The physical and same-record channels cannot be ordered globally by either spectral decay rate or stability class.

The joint structure instead contains multiple distinct phenomena:

1. regions where conditioning increases decay rate;
2. regions where conditioning decreases decay rate without changing class;
3. regions where conditioning stabilizes a physically unstable quotient;
4. now, prospectively confirmed regions where conditioning destabilizes a physically stable quotient.

A useful conglomerate representation therefore must retain channel identity, the full mean-square invariant triple, and the direction of the conditioning bridge. A universal scalar average would erase scientifically real distinctions.

## Next justified frontier

Investigate the fresh class-crossing failure signal at the exact `c3=0` boundary:

- derive the physical and same-record `c3` expressions from the active stochastic quotient;
- determine which terms permit the same-record determinant coefficient to change sign while the other three Routh-Hurwitz inequalities remain positive;
- formulate a fresh outcome-free boundary coordinate or sufficient-condition map only if the algebra warrants it;
- test any learned crossing criterion on a new seed before promotion.

No universal class-monotonicity theorem is now licensed.
