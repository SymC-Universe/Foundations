# Fresh targeted mean-square class-crossing test v0.1

**Status:** FROZEN BEFORE EXECUTION
**Lineage:** bounded H3 PASS -> post-hoc exploratory crossing lead -> fresh prospective existence test

## Purpose

The adversarial H3 phase passed on its preregistered 512-case panel selected from 50000 fresh candidates by smallest physical-only distance to the mean-square stability boundary. That result remains valid for that panel.

After H3 closed, a separate exploratory search produced a post-hoc lead suggesting that STABLE -> UNSTABLE crossings may occur in a different part of the same measured-qubit family, characterized by large `kappa/gamma` and `omega/gamma`, moderate efficiency, near-measurement-axis states, and `x*z<0`.

That exploratory lead is not evidence. This phase prospectively tests the existence of such a crossing using a new seed and a frozen target-region generator.

## Registered hypothesis H4

Within the frozen fresh target-region panel, there exists at least one input whose physical active quotient is robustly mean-square `STABLE` and whose same-record active quotient is robustly mean-square `UNSTABLE`.

A robust crossing requires

`alpha_phys / R < -1e-6`

and

`alpha_rec / R > +1e-6`,

where

`R = gamma + kappa + omega + eta*kappa`

and `alpha=max Re eig(G)` for the real 3x3 symmetric second-moment generator.

If no independently reconstructed robust crossing is found, H4 is `FAIL_TARGETED_CROSSING_H4`.

This is an existence test. One verified fresh crossing is sufficient to pass H4.

## Fresh target-region generator

Use exactly NumPy `default_rng(seed=2026082905)`.

Generate exactly 100000 input candidates `XC000001...XC100000`.

Fix

`gamma = 1`.

Draw independently:

- `log10(kappa/gamma) ~ Uniform(log10(3), log10(100))`;
- `log10(omega/gamma) ~ Uniform(log10(3), log10(100))`;
- `eta ~ Uniform(0.05,0.25)`;
- choose `sign_z` uniformly from `{-1,+1}`;
- `|z| ~ Uniform(0.90,0.999)`;
- `f_x ~ Uniform(0.20,0.99)`;
- set `z=sign_z*|z|`;
- set `x=-sign_z*f_x*sqrt(1-z^2)`;
- set `y=0`.

Thus every generated state satisfies `x*z<0` and `x^2+z^2<1` by construction.

No candidate is replaced or regenerated because of any physical or same-record outcome.

The previously exposed exploratory candidate is not part of this seed-generated panel and cannot be counted.

## Two-stage freeze-before-view architecture

### Stage A: physical channel only

For every generated input construct only the physical active matrices

`a=gamma/2+kappa`,
`q=eta*kappa`,

`A_phys=[[-a,omega],[-omega,-gamma]]`,

`B=[[-sqrt(2q)*z,-sqrt(2q)*x],[0,-2*sqrt(2q)*z]]`.

Construct `G_phys` and calculate `alpha_phys`.

A candidate enters the frozen Stage-A eligible set if

`alpha_phys/R < -1e-6`.

Write, before any same-record matrix is constructed:

- generator seed and candidate-input SHA-256;
- all eligible candidate IDs;
- each eligible candidate's physical normalized alpha;
- canonical Stage-A selection SHA-256.

Stage A receives `SELECTION_HOLD` if fewer than 10000 physical robustly stable candidates are available.

### Stage B: same-record reveal

Only after the Stage-A bytes and SHA-256 are written may the same-record correction be constructed for the frozen eligible IDs.

Use

`DeltaA=[[0,2*q*z*x],[0,-2*q*(1-z^2)]]`

and

`A_rec=A_phys+DeltaA`.

Compute `G_rec` and `alpha_rec` for every Stage-A eligible candidate.

Record every candidate with

`alpha_rec/R > +1e-6`

as an analytic robust class-crossing candidate.

The Stage-A eligible set is immutable during Stage B.

## Independent full-Hilbert reconstruction

Every analytic robust crossing candidate must then be reconstructed independently from the two-level Hilbert-space operators:

- measured operator `sigma_z/2`;
- Hamiltonian `omega sigma_y/2`;
- amplitude damping `sqrt(gamma)`;
- unconditional measurement backaction `2 kappa D[x]`;
- same-noise stochastic tangent amplitude `sqrt(2 eta kappa)`;
- same-record deterministic conditioning correction.

For each crossing require:

- positive density matrix;
- one-dimensional conditioning-dark factor;
- two-dimensional active quotient;
- dark/invariance/intertwining residuals `<=5e-9`;
- reconstructed physical and record active matrices agree with the Stage-A/Stage-B analytic matrices `<=5e-9`;
- direct symmetric moment lift agrees with Kronecker/duplication lift `<=5e-11`;
- independently reconstructed normalized physical alpha remains `<-1e-6`;
- independently reconstructed normalized record alpha remains `>+1e-6`.

If analytic crossing candidates exist but none survive independent reconstruction, phase status is `RECONSTRUCTION_HOLD`, not H4 PASS.

## Frozen negative/positive controls

The pipeline must include:

- a stable no-conditioning control with `eta=0`, for which physical and record channels are identical;
- the independent synthetic rank-one STABLE -> UNSTABLE control used in the preceding H3 audit, demonstrating the classifier can report a crossing.

These controls do not enter H4.

## Frozen gates

- **X0 generator determinism:** all 100000 input candidates regenerate byte-equivalently in-process.
- **X1 Stage-A freeze:** at least 10000 robust physical STABLE candidates, with Stage-A bytes and digest written before Stage B.
- **X2 analytic reveal:** Stage B evaluates exactly the frozen Stage-A eligible IDs without replacement or mutation.
- **X3 reconstruction:** every analytic robust crossing is preserved; at least one must pass independent full-Hilbert reconstruction for H4 to pass.
- **X4 controls:** eta-zero identity and independent synthetic crossing controls pass.
- **X5 H4 existence:** at least one independently reconstructed fresh robust physical STABLE -> record UNSTABLE crossing exists.

Overall status:

- `PASS_TARGETED_CROSSING_H4` if X0-X5 pass;
- `FAIL_TARGETED_CROSSING_H4` if X0-X2 and X4 pass but no analytic robust crossing exists;
- `RECONSTRUCTION_HOLD` if analytic crossings exist but none independently reconstruct;
- `SELECTION_HOLD` if X1 fails;
- `AUDIT_FAILURE` for other failures.

## Interpretation firewall

A H4 PASS would prospectively establish that mean-square stability-class preservation is not universal even within this exact measured-qubit family. It would not erase the bounded H3 PASS, which concerned a different frozen selection strategy and panel.

A H4 PASS would create a new class-crossing failure region requiring mechanistic investigation.

A H4 FAIL would mean the post-hoc exploratory lead did not prospectively reproduce under this frozen target generator; the original exploratory hit would remain non-confirmatory.

Neither outcome licenses a stochastic scalar chi, localization/collapse claims, or transfer to other measurement/dissipation geometries.
