# Adversarial mean-square stability-class monotonicity test v0.1

**Status:** FROZEN BEFORE EXECUTION
**Lineage:** generalized H2 FAIL -> post-hoc observation of zero STABLE-to-UNSTABLE crossings -> new prospective adversarial test

## Purpose

The broad generalized H2 stress phase proved that same-record conditioning does not monotonically improve the mean-square spectral abscissa. In that exposed stress set, however, no physical mean-square STABLE case became UNSTABLE under same-record conditioning, while many physical UNSTABLE cases became STABLE.

That class-level pattern was not preregistered and is not established.

This phase prospectively attacks the narrower class-monotonicity candidate by selecting fresh physical-channel cases deliberately closest to the mean-square stability boundary **before any same-record outcome is computed**.

## Registered hypothesis H3

For every admitted selected fixture whose physical active quotient is mean-square `STABLE`, the same-record active quotient remains mean-square `STABLE`.

One selected fixture classified physical `STABLE` and record `BOUNDARY` or `UNSTABLE` makes H3

`FAIL_CLASS_MONOTONICITY`.

No majority rule, quantile rescue, case deletion, threshold relaxation, or outcome-based replacement is allowed.

## Two-stage freeze-before-view architecture

The run must execute in two logically separate stages.

### Stage A: physical-only candidate ranking

Generate candidates and compute only the physical-channel active quotient and physical mean-square generator. The same-record drift, same-record mean-square generator, and same-record spectral abscissa must not be constructed during Stage A.

Select the 512 eligible physical cases nearest the physical mean-square stability boundary by the registered normalized distance below.

Write the selected candidate IDs, full input parameters, physical spectral data, and a SHA-256 digest of the canonical selection JSON **before Stage B begins**.

### Stage B: same-record reveal

Only after the Stage-A selection is frozen in bytes may the same-record channel be constructed for the selected 512 cases.

The selection is immutable during Stage B.

## Fresh candidate generator

Use exactly NumPy `default_rng(seed=2026082904)`.

Generate exactly 50000 candidate inputs `CM00001...CM50000` with:

- `eta ~ Uniform(1e-4,0.9999)`;
- `log10(gamma) ~ Uniform(-5,1)`;
- `log10(kappa) ~ Uniform(-5,1)`;
- `log10(omega) ~ Uniform(-5,1)`;
- draw a normalized 3D standard-normal direction.

State radius:

- odd candidate IDs: `r=0.98*u^(1/3)`, `u~Uniform(0,1)`;
- even candidate IDs: `r~Uniform(0.95,0.9999)`.

Set the Bloch vector to `r*direction`.

No candidate is regenerated because of any physical or same-record result.

## Physical-only active representation used for ranking

Use the exact measured-qubit active `(x,z)` quotient formulas already independently closed upstream:

`a=gamma/2+kappa`,
`q=eta*kappa`,

`A_phys=[[-a,omega],[-omega,-gamma]]`,

`B=[[-sqrt(2q)*z,-sqrt(2q)*x],[0,-2*sqrt(2q)*z]]`.

Construct the physical real 3x3 symmetric second-moment generator `G_phys` independently by direct symmetric-basis action.

Let

`alpha_phys=max Re eig(G_phys)`

and define the strictly positive natural rate scale

`R=gamma+kappa+omega+q`.

Define normalized physical boundary distance

`d_phys=-alpha_phys/R`.

A Stage-A candidate is eligible if:

- physical spectral class is `STABLE` under normalized tolerance `alpha_phys/R < -1e-9`;
- `d_phys >= 1e-7` to exclude numerically indistinguishable boundary cases;
- base density matrix is positive.

Select exactly the 512 eligible candidates with smallest `d_phys`; tie-break by candidate numeric ID.

Stage A receives `SELECTION_HOLD` if fewer than 512 eligible cases exist or if the farthest selected case has `d_phys>0.05`.

## Independent Stage-B reconstruction

For every selected case, independently reconstruct from Hilbert-space operators:

- `A_phys`;
- `A_rec`;
- common stochastic tangent matrix `B`;
- measurement functional;
- conditioning-dark space;
- exact 2D active quotient for both channels.

Before evaluating H3, require:

- positive density matrix;
- one-dimensional conditioning-dark factor and two-dimensional quotient;
- dark/invariance/intertwining residuals `<=5e-9`;
- independently reconstructed physical active `A` and `B` agree with the Stage-A analytic matrices up to active-basis similarity/invariant checks;
- direct symmetric moment lift agrees with Kronecker/duplication lift `<=5e-11`;
- physical Stage-B class remains `STABLE` and normalized physical alpha agrees with Stage A to `<=1e-8`.

Any selected fixture failing reconstruction makes the phase `RECONSTRUCTION_HOLD`. No replacement occurs.

## Record-channel classification

For each selected case compute

`alpha_rec=max Re eig(G_rec)`

using the same natural scale `R` and normalized tolerance:

- `STABLE` if `alpha_rec/R < -1e-9`;
- `BOUNDARY` if `|alpha_rec/R|<=1e-9`;
- `UNSTABLE` if `alpha_rec/R > 1e-9`.

H3 requires all 512 selected cases to remain `STABLE`.

Record exact crossing IDs and full input/physical/record data for any violation.

## Adversarial classifier control

The pipeline must prove it can detect a STABLE-to-UNSTABLE transition independently of the measured-qubit family.

Use

`A0=[[-0.3,1],[-1,-0.3]]`, `B0=0.2 I2`

as a stable base and apply rank-one update

`DeltaA=[[0.8,0],[0,0]]`.

Require base mean-square `STABLE`, updated mean-square `UNSTABLE`.

This control does not enter H3.

## Frozen gates

- **C0 generator determinism:** all 50000 input candidates regenerate byte-equivalently in-process.
- **C1 physical-only selection:** Stage A produces exactly 512 frozen selected cases, selection digest is written before Stage B, and maximum selected `d_phys<=0.05`.
- **C2 reconstruction:** all 512 selected cases pass independent Hilbert-space/quotient reconstruction with no replacement.
- **C3 physical replay:** Stage-B physical classes remain STABLE and normalized alphas agree with Stage A `<=1e-8`.
- **C4 adversarial control:** the independent control detects STABLE -> UNSTABLE.
- **C5 H3 class monotonicity:** all 512 selected measured-qubit cases remain record STABLE.

Overall status:

- `PASS_ADVERSARIAL_CLASS_MONOTONICITY` if C0-C5 pass;
- `FAIL_CLASS_MONOTONICITY` if C0-C4 pass and C5 fails;
- `SELECTION_HOLD` or `RECONSTRUCTION_HOLD` as defined above;
- `AUDIT_FAILURE` for other failures.

## Interpretation firewall

A PASS would provide strong prospective adversarial evidence that same-record conditioning preserves mean-square stability class in this exact measured-qubit family, even for fresh physical cases selected as close as possible to the boundary from 50000 candidates.

A PASS is not a proof and does not establish the claim for different measurement operators, Hamiltonian axes, dissipators, Hilbert-space dimensions, or nonlinear measurement models.

A FAIL is a major scientific boundary signal and must be preserved. It would identify an explicit stable physical system that conditioning makes mean-square unstable.

Neither outcome licenses a stochastic scalar chi or localization/collapse interpretation.
