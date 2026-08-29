# Conditioning structural monotonicity stress v0.1 result

**Status:** FAIL_GENERALIZED_H2
**Classification:** SCIENTIFIC / MODEL-BOUNDARY SIGNAL
**Canonical run:** `33256389876`
**Execution commit:** `ba9d07b10e5828867c720f213d488146cb999ff0`

The workflow conclusion is `failure` because the preregistered generalized directional hypothesis H2 failed. The audit infrastructure itself passed its structural, admission, reconstruction, and adversarial-control gates.

## Frozen source identities

- preregistration SHA-256: `574ae43887cf136ff647befefc539775e872810206a206f09accdc638a40132d`
- pre-execution clarification SHA-256: `aa7a9ccbeb5b894b052ab79055cd9bbdef0abdfbece7ab44c367ad5e99885582`
- audit-code SHA-256: `a528291c4155d76b308a4a45bc646ace118558d7c875e0b97ad0296e69456a7b`
- workflow SHA-256: `73106dbdf78e668659aab5c25c04458bbe3712b59cfd2da2b607a88d204bd792`
- upstream directionality-result SHA-256: `add09191d9e590f6e09a643e8b4b7f9f3b989691c65273299954c7e62fca73f1`

The 16-case corner-panel ambiguity was resolved and separately recorded before implementation/execution. No outcome was available when that clarification was made.

## Preserved execution evidence

- artifact ID: `9715934331`
- artifact ZIP SHA-256: `a14675b7957776cb552f94a14b1345361b6b0a018ee4466a82594e05978323eb`
- result JSON SHA-256: `792b5f6eb2e17a7ebc6abedf2164045e87ca5e1421c6ac89371258062410cc9c`
- stdout SHA-256: `cc088f8d96abe5a5b0800cf3fdec20e1a298185ce1799dd194e168643748dbf6`
- environment-lock SHA-256: `62ea3a489c49d310850bc59b6c846cb0659bc975b25e9f2ae77ea57d96e15445`
- source-identity SHA-256: `a107b0a772ac71b71a8842040f5569f133b158d30d1a4848e7ac6147eae6313f`
- SHA256 manifest SHA-256: `e1438353ba6acbb6b8ee98c714c7c2d2b961327ea7d10502fb3e312519950de5`

The workflow independently verified the result-file manifest before artifact upload.

## Preregistered gate results

- **S0 exact structural identity: PASS.** Symbolic `DeltaG` identity and characteristic factorization passed; maximum numerical structural residual `3.552713678800501e-15`.
- **S1 generator determinism: PASS.** Exactly 4096 seeded stress fixtures regenerated under seed `2026082902`.
- **S2 broad admission: PASS.** `4096/4096` seeded fixtures and `16/16` explicit corners were admitted with no replacement.
- **S3 mean-square audit: PASS.** Maximum direct-vs-Kronecker lift error `0.0`; registered classifier consistency passed.
- **S4 adversarial comparator: PASS.** The fixed stabilizing rank-one control had `delta_alpha=-0.4`; the destabilizing control had `delta_alpha=+0.8` and became `UNSTABLE`.
- **S5 generalized H2: FAIL.** `441` admitted cases violated `alpha_rec <= alpha_phys + 1e-9`.

Therefore the preregistered phase status is permanently:

`FAIL_GENERALIZED_H2`.

No threshold, fixture, parameter range, or directional definition is changed to rescue H2.

## What the failure means directly

The bounded prior result, 24/24 fresh fixtures with `alpha_rec <= alpha_phys`, was genuine prospective support **inside that earlier registered sample**. This broader stress test demonstrates that the direction does not generalize across the much wider measured-qubit parameter space.

Of 4112 total admitted broad-plus-corner cases:

- `3146`: physical `STABLE` -> record `STABLE`;
- `584`: physical `UNSTABLE` -> record `STABLE`;
- `382`: physical `UNSTABLE` -> record `UNSTABLE`;
- `0`: physical `STABLE` -> record `UNSTABLE`.

Among the 441 H2 counterexamples:

- `440` were `STABLE -> STABLE`;
- `1`, `CORNER16`, was `UNSTABLE -> UNSTABLE`.

Thus almost every H2 failure in this stress set means that the same-record channel had a **less negative spectral abscissa while remaining mean-square stable**, not that conditioning destroyed stability.

The largest positive displacement was `+0.1442412611137911` at `CORNER16`; the most negative displacement was `-8.983357849986982` at `BS3262`.

## Stability metric split exposed by the failure

For all 440 stable H2 counterexamples, every registered cubic Routh-Hurwitz margin

`(c1, c2, c3, c1*c2-c3)`

increased from the physical channel to the same-record channel, even though the spectral abscissa became less negative.

Therefore this phase supplies a concrete warning against treating "more stable" as a one-dimensional ordering. In this family, spectral-abscissa decay rate and algebraic Hurwitz distance can move in opposite directions while both channels remain on the stable side of the boundary.

This is a scientific signal, not an inconsistency in the audit.

## Post-hoc boundary localization

Everything in this section is **EXPLORATORY / POST-HOC** and cannot count as prospective support.

Among the 439 seeded H2 counterexamples, all 439 satisfied

`omega + kappa < gamma/2`.

Equivalently, with

`a = gamma/2 + kappa`,
`delta = gamma-a = gamma/2-kappa`,

they all satisfied

`omega < delta`.

For the deterministic physical active block

`A_phys=[[-a,omega],[-omega,-gamma]]`,

the repeated-root condition on the low-kappa branch is

`delta = 2 omega`.

Thus every seeded H2 counterexample occurred inside a wedge extending from the overdamped side of that repeated-root boundary through only a limited distance onto the underdamped side. `421/439` seeded counterexamples had deterministic active `chi_active>1`; the remaining 18 lay close to the boundary on the `chi_active<=1` side, with the smallest observed counterexample value approximately `0.9743984479768725`.

This does **not** mean `chi_active` alone predicts the H2 failure. Many cases with `chi_active>1` did not fail H2. The repeated-root geometry is a boundary coordinate, not a sufficient classifier.

State orientation also mattered: `312/439` seeded counterexamples had `x*z<0`.

## Post-hoc perturbative mechanism

For the low-kappa branch `delta=gamma/2-kappa>0`, consider the weak-measurement limit `q=eta*kappa -> 0` while remaining on the deterministic overdamped side

`D = delta^2 - 4 omega^2 > 0`.

The slow deterministic eigenvalue of the active physical drift is

`lambda_s = -(a+gamma)/2 + sqrt(D)/2`.

The same-record drift correction is

`DeltaA = [[0, 2 q z x], [0, -2 q (1-z^2)]]`.

Differentiating the slow eigenvalue with respect to `q` at `q=0` gives the exploratory first-order coefficient

`S = -(1-z^2) + ((1-z^2)*delta - 2*omega*x*z)/sqrt(delta^2-4*omega^2)`.

For a deterministic second-moment mode, the leading first-order spectral-abscissa displacement is

`delta_alpha / q -> 2 S`.

Therefore weak conditioning can make the leading decay rate **less negative** when

`2*omega*x*z < (1-z^2)*(delta - sqrt(delta^2-4*omega^2))`.

This explains why `x*z<0` is strongly associated with the counterexamples: on this branch, negative `x*z` reduces the effective reversible coupling between the slower active coordinate and the faster-damped coordinate. Added direct damping and reduced stabilizing mixing can compete, so the dominant decay rate can slow even though the system remains stable.

As an exploratory consistency check on the already-exposed stress data, the sign of this first-order expression predicted `412/439` seeded H2 counterexamples. Across the full seeded stress set it had about `95.6%` precision and `93.8%` recall for H2 failure. Restricting to weak `q<1e-3` cases away from the repeated-root singular neighborhood (`D/delta^2>0.05`), there were 320 cases and the observed `delta_alpha/q` versus predicted `2S` correlation was approximately `0.99776`, with median absolute residual approximately `6.31e-5`.

These checks are mechanism discovery on the same failure data and are **not confirmatory evidence**. They justify a fresh prospective mechanism test only.

## New post-hoc hypothesis candidates

Two narrower hypotheses are licensed for future preregistration, not for current promotion:

1. **Perturbative sign mechanism:** in a fresh weak-measurement, low-kappa, overdamped active-quotient sample away from the repeated-root singularity, the sign and leading magnitude of `delta_alpha` are predicted by `2 q S` above.
2. **Class monotonicity candidate:** in this exact measured-qubit family, same-record conditioning may preserve or improve the mean-square stability **class** even though it does not monotonically improve spectral abscissa. The current stress set showed no `STABLE -> UNSTABLE` cases and 584 `UNSTABLE -> STABLE` cases. This was not preregistered and therefore requires fresh prospective testing or proof.

## Interpretation firewall

The failure rules out universal monotonic improvement of the spectral abscissa within the tested measured-qubit family.

It does not rule out:

- bounded regimes where spectral-abscissa improvement holds;
- structural stabilization of the Routh-Hurwitz class;
- a multicoordinate joint stability geometry;
- meaningful organization around the repeated-root boundary when combined with state orientation and measurement strength.

It does not license a new scalar, localization/collapse claim, or retrospective replacement of H2.
