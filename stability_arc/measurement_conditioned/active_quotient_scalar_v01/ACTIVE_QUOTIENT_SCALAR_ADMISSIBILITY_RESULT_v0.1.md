# Active-quotient scalar admissibility audit v0.1 result

**Status:** PASS
**Scope:** deterministic active quotient only

## Frozen contract and pre-execution amendment

The base preregistration was frozen before execution:

`stability_arc/measurement_conditioned/active_quotient_scalar_v01/PREREGISTRATION_ACTIVE_QUOTIENT_SCALAR_ADMISSIBILITY_AUDIT_v0.1.md`

SHA-256:
`9afc75864f704d9a9f1310e102a58ca36b5ce24ed6cb45ad4f3361e2f1f07eda`

Before any execution, adversarial review identified one coverage omission: the standing control required explicit refusal when no nontrivial conditioning-dark factor is identifiable. The separately frozen pre-execution amendment added only RQ8 and changed A6 from RQ1-RQ7 to RQ1-RQ8:

`stability_arc/measurement_conditioned/active_quotient_scalar_v01/PREEXECUTION_AMENDMENT_v0.1a.md`

SHA-256:
`486b2d5e0bc08ba95432529dd2e9f5c3d2fbe571e12bf17d3a2853e06452f790`

No numerical audit result had been observed before that amendment.

Frozen code SHA-256:
`c87c3387072dc5ea45269411bdd787f97783064992473be8b962456c5859c84a`

## Canonical first execution

Workflow run: `33252642667`
Execution commit: `e6833f60cb6591dc00b6be9e6403a6e5ed48b867`
Conclusion: **SUCCESS / PASS**
Python: 3.12.14
NumPy: 2.1.3

Artifact ID: `9714831463`
Artifact ZIP SHA-256:
`9aa92ed8d0a8f851b06c4723d161a350049fb9fbc453d64a3106af2d39e77c6c`

Result JSON SHA-256:
`66ef426d61d0e1a850a4abe1a7fcfe09bccd88d6f870b0a4b0fb2024c406fa34`

A redundant orchestration-only launch-marker push produced run `33252664549`. It also completed SUCCESS and reproduced the **identical result JSON SHA-256** `66ef426d61d0e1a850a4abe1a7fcfe09bccd88d6f870b0a4b0fb2024c406fa34`. Its artifact ID is `9714837159`, artifact ZIP SHA-256 `6255fd00701bc16f9b571350fc1f09661701abbfb2a1ffd6c2512f2c129765ae`. The first execution remains canonical.

## Frozen gate results

All gates A0-A7 passed.

### A0 dark reconstruction and quotient dimension: PASS

Across all three fresh quantum fixtures:

- independently reconstructed dark dimension = 1;
- active quotient dimension = 2;
- maximum `|V^T D|` residual = `1.1102230246251565e-16`;
- maximum physical dark-invariance residual = `1.7541523789077474e-16`;
- maximum record dark-preservation residual = `2.596211245986523e-17`.

### A1 real stable quotient admissibility: PASS

Both physical and record-conditioned active quotients were independently admitted as real 2x2 asymptotically stable blocks for every fresh fixture.

### A2 coordinate/complement invariance: PASS

Under the frozen active basis change and the independent complement-shear plus basis change:

- maximum trace residual = `2.220446049250313e-16`;
- maximum determinant residual = `2.220446049250313e-16`;
- maximum scalar residual = `1.1102230246251565e-16`.

All are far below the frozen `5e-12` gate.

### A3 characteristic-factor consistency: PASS

The degree-2 active characteristic factor obtained by polynomial division of the full characteristic polynomial by the independently reconstructed dark factor agreed with the quotient representation to maximum residual

`6.661338147750939e-16`

versus the frozen `2e-10` gate.

### A4 canonical 2x2 inheritance: PASS

All three fresh oscillator controls recovered

`chi = Gamma/(2 Omega)`

with maximum absolute error

`1.1102230246251565e-16`

versus the frozen `1e-13` gate.

### A5 separate-channel preservation: PASS

The admitted active-quotient coordinates were recorded separately:

- AQ1: `chi_active_phys = 0.25202432454547247`, `chi_active_rec = 0.3352225058179115`;
- AQ2: `chi_active_phys = 0.3181045051401759`, `chi_active_rec = 0.40837538880643054`;
- AQ3: `chi_active_phys = 0.32615439934795415`, `chi_active_rec = 0.3871758850234289`.

The fact that the record-conditioned value exceeded the physical value in all three fresh fixtures is **observation only**. It was not a preregistered directional claim and is not promoted as evidence of movement toward or away from any preferred value.

### A6 refusal behavior: PASS

Every preregistered refusal control returned exactly the required status:

- RQ1 -> `REFUSE_QUOTIENT_DIMENSION`;
- RQ2 -> `REFUSE_NOT_ASYMPTOTICALLY_STABLE`;
- RQ3 -> `REFUSE_NONPOSITIVE_DETERMINANT`;
- RQ4 -> `REFUSE_DEGENERATE_SECTOR_ATTRIBUTION`;
- RQ5 -> `REFUSE_DEFECTIVE_ACTIVE_SECTOR`;
- RQ6 -> `REFUSE_COORDINATE_FAILURE`;
- RQ7 -> `REFUSE_NONREAL_QUOTIENT`;
- RQ8 -> `REFUSE_NONIDENTIFIABLE_DARK_FACTOR`.

No fallback scalar was produced.

### A7 full-generator and stochastic firewall: PASS

For every fresh quantum fixture:

- full 3x3 physical generator -> `FULL_MATRIX_REQUIRED`;
- full 3x3 record-conditioned generator -> `FULL_MATRIX_REQUIRED`;
- multiplicative stochastic term -> `STOCHASTIC_TERM_NOT_COMPRESSED`.

## Licensed conclusion

The audit licenses the following narrow mathematical statement:

> When the independently reconstructed conditioning-dark factor leaves an identifiable, real, asymptotically stable two-dimensional deterministic active quotient, `chi_active=-tr(A_A)/(2 sqrt(det(A_A)))` is a basis- and complement-invariant Stability Arc coordinate on that quotient, separately for the physical and record-conditioned deterministic drifts.

This is the first licensed scalar coordinate in the measurement-conditioned branch that does **not** compress the full three-dimensional generator.

## Interpretation firewall

This PASS does not establish a scalar for the full generator, does not compress the multiplicative stochastic term, does not privilege either physical or record-conditioned channel, does not license averaging the two scalars, and does not show that chi=1 predicts localization, measurement quality, collapse, or an optimum.

A critical remaining question is whether the exact conditioning-dark factor is also invariant under the shared stochastic tangent matrix `B`. If not, stochastic dynamics can leak between the dark and active sectors even though the deterministic drift factorizes. Therefore the next safe frontier is an outcome-free **stochastic dark/active compatibility and quotient-closure audit** before any localization claim is attempted.
