# Substrate Inheritance Computational Validation Ledger

Status: active computational-method evidence record. This ledger does not contain a real-system inheritance result.

## Evidence classes

The records below are classified as software, mathematical, synthetic ground-truth, ensemble-discriminability, or identifiability evidence. None may be promoted to physical substrate-inheritance evidence merely because a validation passes.

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

GitHub Actions run `33290141338` executed the battery successfully as part of commit `58b3feb9976ee6b4783a4e04fc2c19e740871981`.

Key observations from that run:

- zero coupling produced zero substrate self-energy and was not labeled influence;
- the influence-only case produced a nonzero transfer map but was labeled `SUBSTRATE_INFLUENCE`, not inheritance;
- the conditional scalar case predicted the synthetic child scalar exactly but remained `CONDITIONAL_INHERITANCE` because intervention and specificity were absent;
- the modal-inheritance case preserved the known carrier map with zero mapping residual even though the scalar values were deliberately changed;
- the frequency-false-friend case preserved eigenvalues to approximately `4.44e-16` while producing a strongly non-identity modal-overlap structure;
- the split-mode case had only 0.5 individual-vector overlap with each child vector but principal-angle cosine 1.0 for the containing child subspace;
- the degenerate-subspace case rotated the basis while retaining principal-angle cosines `[1.0, 1.0]`;
- the coupling-rewire case changed the scalar self-energy by approximately `0.01650` despite preserving the substrate operator;
- the finite-bath case retained late recurrence with maximum late absolute kernel approximately `0.94766`;
- the full prospective synthetic case had zero Schur prediction error, a nonzero intervention transfer, and a nonzero eigenvalue-preserving scramble specificity gap.

Status: PASS as synthetic ground-truth validation only.

## V3: Same-spectrum modal ensemble and coupling-specificity ensemble

GitHub Actions run `33290141338` also executed 256-trial seeded ensembles in dimension 5.

### Same-spectrum modal null

The null preserves the parent eigenvalue spectrum while randomizing carrier geometry.

- maximum numerical difference between parent and null spectra: approximately `6.22e-15`;
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
- fraction nonzero above machine-scale criterion: `0.99609375` or 255/256 trials.

Interpretation: in the specified synthetic ensemble, conglomerated response depends on the coupling architecture and is not determined by substrate spectrum alone.

### Intervention derivative cross-check

The numerical finite-difference parent-to-child transfer map was compared with an analytic derivative for a diagonal synthetic substrate.

- maximum relative error: approximately `1.38e-9`;
- mean relative error: approximately `4.97e-10`;
- 95th percentile relative error: approximately `9.30e-10`.

Interpretation: the implemented numerical intervention map reproduces the analytic result to substantially better than the precision needed for the current synthetic validation.

Status: PASS as synthetic ensemble/method validation only.

## Provenance for V1-V3

- workflow: `.github/workflows/substrate-inheritance.yml`;
- successful run: `33290141338`;
- successful job: `99200237146`;
- test count in that run: 26 passed;
- uploaded artifact: `substrate-inheritance-synthetic-validation`;
- artifact ID: `9725698262`;
- uploaded artifact ZIP SHA-256: `8a4f1417e6ea7d27eeabd057f0eaaddf51bdf9e5ca2fa4fde4393d74e656d822`;
- physical thresholds frozen: false;
- real-system evidence: false.

## V4: Single-response identifiability challenge

Status: active validation layer added after V3.

Purpose: construct distinct substrate-to-child coupling geometries that produce exactly the same scalar substrate self-energy at one synthetic probe frequency, then test whether a second frequency separates them.

This directly attacks the inference that one matched scalar response could identify inheritance. If the construction succeeds, the correct conclusion is that one scalar response may demonstrate influence but is insufficient to uniquely identify conglomerative inheritance.

The numerical result is not entered here until the corresponding GitHub Actions execution passes.

## Physical evidence boundary

At the time of this ledger entry:

- no physical inheritance threshold has been frozen;
- no real-system substrate-inheritance result has been established;
- Na/Cu remains development-only and its planned active-region Hessian artifact is not yet present at the checked Chemistry branch head;
- CO/Cu remains upstream of the inheritance analysis while its frozen surface audit closes;
- H/Ru remains a contrast/limit protocol without an admitted Foundations inheritance input record.

The next transition from synthetic validation to physical development evidence requires a provenance-complete parent governing object, child governing object, shared-degree-of-freedom mapping, modal/subspace representation, and a correspondence rule frozen before the target inheritance result is inspected.
