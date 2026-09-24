# D01C Non-Normal Linear Domain Map Readout v0.1

**Date:** 2026-09-22  
**Status:** P0-D / P0-Q WITHIN-DOMAIN READOUT  
**Authority:** SymC General Operations Manual v0.8.3  
**Scientific freeze:** commit `b8bf36c2776e2d788cdbf7a5f33e4254d1cb5f9b`  
**Execution commit:** `9818612abae93e460af7ab45281fd9a5e4ae68e7`  
**Execution archive:** `results/D01C_ARCHIVAL_RECORD_v0.1.json`  
**Claim ceiling:** synthetic/mathematical linear-dynamics evidence only

## 1. Question

D01C asked whether a fixed asymptotically stable spectrum is sufficient to determine finite-time response and robustness when carrier geometry becomes non-normal, and whether a broader Chi interpretation adds anything beyond established nonmodal/state-space analysis.

No master chi was searched, fitted, or emitted.

## 2. Frozen construction

Each family used

`A(theta) = V(theta) diag(lambda1,lambda2) V(theta)^-1`

with normalized right carriers

`v1=[1,0]^T`

and

`v2=[cos(theta),sin(theta)]^T`.

Two spectra were frozen before output:

- N1: `[-1,-2]`;
- N2: `[-0.25,-2]`.

The carrier angle was swept from 90 degrees to 0.5 degrees while the spectrum remained fixed.

The exact generator has upper-triangular form

`A = [[lambda1, (lambda2-lambda1) cot(theta)], [0,lambda2]]`.

Thus D01C changes carrier non-orthogonality without changing the eigenvalue set.

## 3. Execution integrity

GitHub Actions run `35809467796` completed successfully.

- frozen cases: 26/26;
- maximum eigenvalue-preservation residual: `2.220446049250313e-16`;
- no master scalar emitted;
- regression/scientific guards passed;
- one reviewer artifact was produced;
- reproduction entrypoint: `python chi_architecture/reproduce.py d01c`.

## 4. Function Map

### N1: fixed spectrum [-1,-2]

The normal case at 90 degrees has maximum operator state gain 1.0.

At 0.5 degrees, with the same eigenvalues, the maximum operator state gain is

`28.6524936441728`.

The scanned complex stability radius falls from 1.0 in the normal case to

`0.01745041361890063`.

The resolvent peak increases by approximately 56.31 above the normal-family baseline.

### N2: fixed spectrum [-0.25,-2]

The normal case again has maximum operator state gain 1.0.

At 0.5 degrees, with the same eigenvalues, the maximum operator state gain is

`74.5003623740674`.

The scanned complex stability radius falls from 0.25 in the normal case to

`0.002493264858180868`.

The resolvent peak increases by approximately 397.08 above the normal-family baseline.

Therefore the frozen eigenvalue set is not sufficient to determine finite-time amplification or perturbation robustness within either construction.

The official within-construction status is:

`REFUTED_WITHIN_FROZEN_CONSTRUCTION`

for eigenvalue-only sufficiency.

## 5. Limit Map and exact standard-theory threshold

For the upper-triangular generator

`A=[[lambda1,b],[0,lambda2]]`

with

`b=(lambda2-lambda1) cot(theta)`,

the numerical abscissa is the largest eigenvalue of

`(A+A^T)/2`.

Because the trace is negative in both frozen families, the numerical abscissa becomes positive when

`b^2 > 4 lambda1 lambda2`

where both eigenvalues are negative and their product is positive.

Equivalently,

`|cot(theta)| > 2 sqrt(lambda1 lambda2) / |lambda2-lambda1|`.

This gives exact carrier-angle boundaries:

- N1: `theta < 19.4712206345 degrees`;
- N2: `theta < 51.0575587310 degrees`.

The first frozen points with positive numerical abscissa were 15 degrees for N1 and 45 degrees for N2, exactly consistent with those analytic thresholds.

This agreement is a standard nonmodal/state-space result. It is not new SymC mathematics.

## 6. Perturbation orientation matters

The first coordinate perturbation is aligned with the first right carrier in this construction and does not expose the large non-normal amplification.

The second coordinate perturbation increasingly excites the non-orthogonal carrier combination and approaches the worst-case operator gain as theta becomes small.

Thus even when the spectrum is fixed, realized response depends on how a perturbation projects into the carrier geometry.

This supplies a clean example of:

`ASYMPTOTIC SPECTRAL PLACEMENT != FINITE-TIME REALIZED RESPONSE`.

## 7. Standard-toolkit comparator verdict

D01C deliberately included the strongest relevant native comparators:

- full state-transition operator;
- numerical abscissa;
- eigenvector conditioning and carrier angle;
- resolvent norm;
- unstructured stability radius.

These established quantities explain the observed synthetic behavior without a new SymC dynamical variable.

The correct added-value verdict is therefore:

`STANDARD_NONMODAL_TOOLKIT_SUFFICIENT_FOR_D01C`.

D01C does **not** support:

- a new non-normal chi;
- a new transient-growth law;
- a new resolvent quantity;
- a new pseudospectral quantity;
- a claim that Chi quantitatively outperforms established nonmodal analysis.

## 8. What D01C contributes to the Chi program

The useful result is representational and architectural rather than a new equation.

A scalar or spectrum can remain perfectly valid for its native asymptotic question while becoming insufficient for a different question about finite-time response or robustness.

The D01 sequence now gives three distinct cases:

1. **D01A:** a scalar chi is exact and highly compressive for normalized SDOF response.
2. **D01B:** local chi can survive, transform, or lose exact modal scalarization after coupling.
3. **D01C:** the entire eigenvalue set can remain fixed while finite-time behavior and robustness change strongly through carrier geometry.

This supports the GOM rule that broader Chi should retain only the additional native structure required by the declared question.

It does not establish that Chi is a new physical agent or a universal coordinate.

## 9. Relation to stability inheritance

D01C strengthens one requirement for any future inheritance claim:

`NUMERICAL OR SPECTRAL SIMILARITY != CARRIER-RESOLVED INHERITANCE`.

If an inherited stability claim concerns realized response, the carrier/subspace or transformation pathway must be preserved strongly enough to support that response.

However, D01C itself contains no physical substrate and therefore is not physical substrate-inheritance evidence.

## 10. Literature and novelty boundary

The behavior mapped here is established nonmodal science.

Relevant prior art includes:

- Trefethen et al., Science 261 (1993), DOI 10.1126/science.261.5121.578;
- Trefethen, SIAM Review 39 (1997), DOI 10.1137/S0036144595295284;
- Schmid, Annual Review of Fluid Mechanics 39 (2007), DOI 10.1146/annurev.fluid.38.050304.092139;
- Jovanovic, Annual Review of Fluid Mechanics 53 (2021), DOI 10.1146/annurev-fluid-010719-060244.

The residual SymC contribution, if any, must come from prospective cross-level interpretation, inheritance/refusal rules, or physical prediction beyond these established tools.

## 11. Next experiment rule

Do not spend the next cycle adding another toy non-normal matrix family merely to reproduce the same established phenomenon.

The next high-information experiment should move to a domain-native physical or empirical system where all three can be independently grounded:

1. a local or spectral stability coordinate;
2. carrier/coupling/system organization;
3. perturbation or recovery behavior.

The test must be frozen before the decisive outcome is inspected and must compare against the strongest native domain toolkit.

That is the point at which the Chi architecture can either earn physical added value or be narrowed again.
