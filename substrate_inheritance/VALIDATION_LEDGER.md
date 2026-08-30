# Substrate Inheritance Computational Validation Ledger

Status: active computational-method evidence record. This ledger does not contain a real-system inheritance result.

## Evidence classes

The records below are classified as software, mathematical, synthetic ground-truth, ensemble-discriminability, identifiability, robustness, or embedding-depth evidence. None may be promoted to physical substrate-inheritance evidence merely because a validation passes.

## V1: Base mathematical and software validation

The engine validates:

- exact Schur-complement block elimination;
- mass-normalized modal overlap machinery;
- subspace comparison machinery;
- finite-difference parent-to-child transfer maps;
- eigenvalue-preserving modal scrambles;
- finite harmonic-bath recurrence;
- evidence labels that prevent influence-only results from being promoted to inheritance.

A representative synthetic run returned an exact Schur identity residual of 0.0 and retained late-time finite-bath recurrence rather than treating the finite mode set as irreversible friction.

Status: PASS as software/mathematical validation only.

## V2: Ten-case adversarial ground-truth battery

The battery contains ten constructed cases with known intended interpretation:

1. no coupling;
2. influence only;
3. conditional scalar mapping;
4. modal inheritance with changed scalar values;
5. equal-eigenvalue frequency false friend;
6. mode splitting;
7. degenerate-subspace basis rotation;
8. coupling rewiring;
9. finite-bath recurrence;
10. full prospective synthetic inheritance.

Key observations:

- zero coupling produced zero substrate self-energy and was not labeled influence;
- the influence-only case produced a nonzero transfer map but was labeled `SUBSTRATE_INFLUENCE`, not inheritance;
- the conditional scalar case predicted the synthetic child scalar exactly but remained `CONDITIONAL_INHERITANCE` because intervention and specificity were absent;
- the modal-inheritance case preserved the known carrier map with zero mapping residual even though the scalar values were deliberately changed;
- the frequency-false-friend case preserved eigenvalues to machine precision while producing a strongly non-identity modal-overlap structure;
- the split-mode case had 0.5 individual-vector overlap with each child vector but principal-angle cosine 1.0 for the containing child subspace;
- the degenerate-subspace case rotated the basis while retaining principal-angle cosines `[1.0, 1.0]`;
- the coupling-rewire case changed the scalar self-energy by approximately `0.0165012` despite preserving the substrate operator;
- the finite-bath case retained late recurrence with maximum late absolute kernel approximately `0.947656`;
- the full prospective synthetic case had zero Schur prediction error, a nonzero intervention transfer, and a nonzero eigenvalue-preserving scramble specificity gap.

Status: PASS as synthetic ground-truth validation only.

## V3: Same-spectrum modal ensemble and coupling-specificity ensemble

A seeded 256-trial ensemble was run in dimension 5.

### Same-spectrum modal null

The null preserves the parent eigenvalue spectrum while randomizing carrier geometry.

- maximum numerical difference between parent and null spectra: approximately `7.11e-15`;
- planted carrier-map mean assignment score: approximately `0.94981`;
- planted median assignment score: approximately `0.95614`;
- same-spectrum scrambled mean assignment score: approximately `0.53907`;
- same-spectrum scrambled median assignment score: approximately `0.53225`;
- threshold-free pairwise AUC probability: `1.0` for this specified synthetic generator.

Interpretation: under this synthetic generator, carrier-resolved information cleanly distinguishes the planted map from scalar-spectrum equivalence. The result does not establish a physical acceptance threshold and does not imply that real systems will have the same separation.

### Coupling rewiring

The parent substrate operator is held fixed while the child-coupling assignment is rewired.

- mean relative self-energy change: approximately `0.22004`;
- median relative self-energy change: approximately `0.20734`;
- 5th to 95th percentile range: approximately `0.02431` to `0.46536`;
- fraction nonzero above machine-scale criterion: `0.99609375`, or 255/256 trials.

Interpretation: in the specified synthetic ensemble, conglomerated response depends on the coupling architecture and is not determined by substrate spectrum alone.

### Intervention derivative cross-check

The numerical finite-difference parent-to-child transfer map was compared with an analytic derivative for a diagonal synthetic substrate.

- maximum relative error: approximately `1.12e-9`;
- mean relative error: approximately `4.17e-10`;
- 95th percentile relative error: approximately `7.70e-10`.

Interpretation: the implemented numerical intervention map reproduces the analytic result to substantially better precision than needed for the current synthetic validation.

Status: PASS as synthetic ensemble/method validation only.

## V4: Single-response identifiability challenge

Distinct substrate-to-child coupling geometries were scaled to produce the same scalar substrate self-energy at one synthetic probe frequency and then compared at a second frequency.

Configuration:

- 256 seeded trials;
- dimension 5;
- match frequency `0.4`;
- second probe frequency `0.9`.

Results:

- maximum self-energy mismatch at the matched frequency: approximately `1.67e-16`;
- mean mismatch at the matched frequency: approximately `3.37e-17`;
- median absolute coupling-direction cosine: approximately `0.30763`;
- mean absolute coupling-direction cosine: approximately `0.34741`;
- 5th to 95th percentile coupling-direction cosine: approximately `0.03492` to `0.75918`;
- median relative response difference at the second frequency: approximately `0.03263`;
- mean relative response difference at the second frequency: approximately `0.04378`;
- 5th to 95th percentile second-frequency difference: approximately `0.00306` to `0.11937`;
- all 256 pairs separated above machine-scale criterion at the second frequency.

Interpretation: one scalar child response can be perfectly matched by substantially different parent-to-child coupling geometries. A single scalar response may demonstrate influence, but it does not uniquely identify conglomerative inheritance.

Status: PASS as synthetic identifiability validation only.

## V5: Coordinate and degeneracy robustness

### Coordinate invariance

Across 256 seeded trials, the substrate self-energy was recomputed after consistent orthogonal basis changes and invertible coordinate scalings.

- maximum orthogonal-basis residual: approximately `1.78e-15`;
- mean orthogonal-basis residual: approximately `2.03e-16`;
- maximum coordinate-scaling residual: approximately `1.78e-15`;
- mean coordinate-scaling residual: approximately `1.34e-16`.

Interpretation: the implemented embedding observable is representation-invariant to numerical precision under the tested coordinate transformations.

### Near-degenerate carrier robustness

A two-mode sector with eigenvalue gap approximately `1e-8` was subjected to perturbations with Frobenius norm `1e-4` and compared with a separated sector having gap `0.7`.

Near-degenerate sector:

- mean individual-mode assignment score: approximately `0.82506`;
- 5th percentile individual-mode assignment score: approximately `0.53924`;
- mean minimum principal-angle cosine of the two-dimensional subspace: approximately `0.999999999893`;
- 5th percentile minimum subspace cosine: approximately `0.999999999747`.

Separated sector:

- mean individual-mode assignment score: approximately `0.999999999222`;
- 5th percentile individual-mode assignment score: approximately `0.999999997420`.

Interpretation: near-degenerate individual eigenvectors can rotate strongly under perturbations far smaller than the overall spectral scale while the physical subspace remains essentially unchanged. This validates the frozen rule that crowded or degenerate sectors must be compared as subspaces instead of forcing one-to-one vector identity.

Status: PASS as synthetic robustness validation only.

## V6: Synthetic substrate-depth embedding validation

A finite uniform nearest-neighbor substrate chain was compared with its analytic semi-infinite surface Green function. The complex probe frequency contains an explicit imaginary regularizer for the resolvent and is not interpreted as physical damping.

Reference configuration:

- onsite stiffness `4.0`;
- substrate hopping `0.8`;
- child coupling `0.6`;
- probe frequency `0.7 + 0.15 i`;
- semi-infinite self-energy real part approximately `0.107248931361`;
- semi-infinite self-energy imaginary part approximately `0.00714727299806`.

Relative finite-depth error:

- depth 1: approximately `5.3999e-2`;
- depth 2: approximately `3.0717e-3`;
- depth 4: approximately `9.9971e-6`;
- depth 8: approximately `1.0593e-10`;
- depth 16: approximately `1.41e-16`.

Direct matrix inversion and recursive surface-Green-function evaluation agreed at zero or machine-scale residual throughout the tested depths.

A coupling-strength sweep showed that stronger substrate hopping required more retained substrate depth for equivalent convergence. This is a property of the specified synthetic chain, not a physical inheritance length for Cu or any other material.

Interpretation: the machinery can ask how the child embedding response converges as progressively more parent substrate degrees of freedom are retained and can validate that convergence against an independent analytic semi-infinite result.

Status: PASS as synthetic embedding-depth validation only.

## Current provenance

Latest closed validation run containing V1-V6:

- workflow: `.github/workflows/substrate-inheritance.yml`;
- GitHub Actions run: `33290269457`;
- commit: `d76e2317817d91911c104ad8dcd23bba29b8fae1`;
- job: `99200574195`;
- conclusion: `success`;
- adversarial/unit tests: `36 passed`;
- uploaded artifact: `substrate-inheritance-synthetic-validation`;
- artifact ID: `9725736036`;
- uploaded artifact ZIP SHA-256: `8adc5e7135a824f8f3f726e8abd2ba60dbc64aacfae86a4db992ae9449e0343d`;
- physical thresholds frozen: false;
- real-system evidence: false.

## Physical evidence boundary

At the time of this ledger entry:

- no physical inheritance threshold has been frozen;
- no real-system substrate-inheritance result has been established;
- Na/Cu remains development-only and its planned active-region Hessian artifact is not yet present at the checked Chemistry branch head;
- CO/Cu remains upstream of the inheritance analysis while its frozen surface audit closes;
- H/Ru remains a contrast/limit protocol without an admitted Foundations inheritance input record.

The next transition from synthetic validation to physical development evidence requires a provenance-complete parent governing object, child governing object, shared-degree-of-freedom mapping, modal/subspace representation, and a correspondence rule frozen before the target inheritance result is inspected.
