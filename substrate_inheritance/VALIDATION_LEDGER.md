# Substrate Inheritance Computational Validation Ledger

Status: active computational-method evidence record. This ledger does not contain a real-system inheritance result.

## Evidence classes

The records below are classified as software, mathematical, synthetic ground-truth, ensemble-discriminability, identifiability, robustness, embedding-depth, non-normal-carrier, electronic-channel, or ingestion-boundary evidence. None may be promoted to physical substrate-inheritance evidence merely because a validation passes.

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

- maximum relative error: approximately `1.38e-9` in the current full-suite run;
- mean relative error: approximately `4.97e-10`;
- the result remains at numerical-validation precision far below any physical interpretation.

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

- maximum residuals remained at approximately `1e-15` to `2e-15` numerical scale in the current suite.

Interpretation: the implemented embedding observable is representation-invariant to numerical precision under the tested coordinate transformations.

### Near-degenerate carrier robustness

A two-mode sector with eigenvalue gap approximately `1e-8` was subjected to perturbations with Frobenius norm `1e-4` and compared with a separated sector having gap `0.7`.

Near-degenerate sector:

- mean individual-mode assignment score: approximately `0.82506`;
- 5th percentile individual-mode assignment score: approximately `0.53924`;
- mean minimum principal-angle cosine of the two-dimensional subspace: approximately `0.999999999893`;
- 5th percentile minimum subspace cosine: approximately `0.999999999747`.

Separated sector:

- mean individual-mode assignment score remained essentially `1.0`.

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
- depth 16: approximately machine scale.

Direct matrix inversion and recursive surface-Green-function evaluation agreed at zero or machine-scale residual throughout the tested depths.

A coupling-strength sweep showed that stronger substrate hopping required more retained substrate depth for equivalent convergence. This is a property of the specified synthetic chain, not a physical inheritance length for Cu or any other material.

Interpretation: the machinery can ask how the child embedding response converges as progressively more parent substrate degrees of freedom are retained and can validate that convergence against an independent analytic semi-infinite result.

Status: PASS as synthetic embedding-depth validation only.

## V7: Carrier-discriminability strength sweep

The planted parent-to-child carrier relation was progressively randomized while the parent and null scalar eigenvalue spectra remained identical. The purpose was to map the failure boundary of the correspondence statistic rather than test only easy positive examples.

Configuration:

- dimension 5;
- 256 trials per synthetic strength;
- angle scales from `0.0` through `1.8` radians;
- no physical threshold was fitted or inferred.

Results:

- maximum threshold-free AUC: `1.0`;
- minimum threshold-free AUC: approximately `0.911835`;
- maximum mean planted-minus-null score gap: approximately `0.463865`;
- minimum mean score gap: approximately `0.191899`;
- at angle scale `0.0`, planted mean score was `1.0` and AUC was `1.0`;
- at `0.35`, planted mean score was approximately `0.83641` and AUC approximately `0.98473`;
- at `0.55`, planted mean score was approximately `0.75646` and AUC approximately `0.93237`;
- at `1.2`, planted mean score was approximately `0.73821` and AUC approximately `0.91183`.

Interpretation: the modal-correspondence statistic loses discriminability as the planted carrier relation weakens. It is therefore not treated as a magic or universally decisive inheritance score. The synthetic strength parameter is not a physical inheritance coordinate and supplies no physical cutoff.

Status: PASS as synthetic failure-boundary validation only.

## V8: Non-normal and biorthogonal carrier validation

This layer tests a major failure mode of ordinary eigenvector comparison. In a non-normal generator, distinct right eigenvectors can become nearly parallel, while meaningful spectral coordinates require left/right or invariant-projector geometry and explicit conditioning.

For a three-mode triangular family:

- shear `0.0`: right-eigenvector condition number `1.0`, maximum off-diagonal right-vector overlap `0.0`;
- shear `1.0`: condition number approximately `3.77667`, off-diagonal overlap `0.5`;
- shear `3.0`: condition number approximately `20.5441`, off-diagonal overlap `0.9`;
- shear `10.0`: condition number approximately `213.770`, off-diagonal overlap approximately `0.990099`;
- shear `30.0`: condition number approximately `1925.741`, off-diagonal overlap approximately `0.998890`.

For the near-defective two-dimensional family `[[1,1],[epsilon,1]]`, the condition number rose from approximately `3.16228` at `epsilon=1e-1` to approximately `10000` at `epsilon=1e-8` while the eigenvalue gap collapsed from approximately `0.632456` to `0.0002`.

A common invertible similarity transformation changed the scale-invariant biorthogonal parent-child correspondence only at machine scale.

Interpretation: right eigenvectors alone are insufficient for non-normal inheritance claims. Future non-normal physical records must retain left and right carriers or equivalent invariant projectors/subspaces plus conditioning. Near defectiveness, an algebraically normalized mode is not automatically a robust physical carrier.

Status: PASS as synthetic non-normal method validation only.

## V9: Separate electronic substrate-inheritance channel

The electronic branch uses a block Hamiltonian and retarded Green-function reduction rather than importing mechanical damping language.

Across the synthetic validation:

- the full block-Hamiltonian and reduced adsorbate Green functions agree at approximately `1e-15` numerical scale;
- basis-transformed electronic self-energy curves agree at approximately `1e-14` numerical scale;
- in 256 same-spectrum electronic carrier scrambles, the substrate eigenvalue spectrum was preserved at machine scale while the median relative self-energy-curve change was approximately `0.98147`;
- all 256 same-spectrum electronic scrambles changed the interface response above machine scale.

The finite-system broadening parameter is explicitly a resolvent regularizer in this synthetic calculation and is not interpreted as mechanical damping.

Interpretation: in the tested synthetic electronic model, the same scalar energy spectrum does not determine the interface response. Orbital/carrier geometry and coupling matter strongly. Electronic self-energy and hybridization remain electronic-channel objects and are not renamed mechanical `gamma` or automatically added to a phononic damping constant.

Status: PASS as synthetic electronic-channel validation only.

## V10: Fail-closed real-system ingestion adapter validation

A separate real-system input contract and adapter were created before any admissible physical parent/child Hessian entered Foundations.

The active input contract is `REAL_SYSTEM_INPUT_SCHEMA_v0.2.json`. It supersedes v0.1 because a pre-ingestion review found that the first draft referred to a matrix-symmetry tolerance without making that tolerance mandatory. The correction was made before any physical record existed or was inspected.

The mechanical adapter refuses, among other conditions:

- incomplete or duplicate shared-coordinate mappings;
- mappings chosen after target-carrier inspection;
- mappings selected using target kinetics or chi;
- matrix or mass unit mismatch;
- invalid source-artifact hashes;
- matrix asymmetry beyond the declared numerical tolerance;
- nonpositive masses;
- schema or correspondence-protocol drift.

The adapter computes only provenance-preserving preprocessing:

- mass-weighted parent and child eigensystems;
- child-mode participation on the prospectively mapped substrate coordinates;
- directional parent-to-projected-child modal overlap;
- shared-coordinate mapping and source hashes.

It explicitly does **not** apply a physical inheritance threshold, assign an inheritance promotion label, compute damping, or compute chi.

The synthetic machine-readable adapter validation produced a 2-parent-mode by 3-child-mode directional overlap matrix and separate child substrate-participation weights. The separation is intentional: directional similarity and the amount of a child mode physically residing on the substrate are different quantities.

Representative synthetic adapter output:

- parent mass-weighted eigenvalues approximately `[0.239627, 0.418706]`;
- child mass-weighted eigenvalues approximately `[0.253455, 0.390568, 0.516810]`;
- child substrate-participation weights approximately `[0.994471, 0.719949, 0.285580]`;
- first parent directional overlaps approximately `[0.998304, 0.007675, 0.005918]`;
- second parent directional overlaps approximately `[0.001696, 0.992325, 0.994082]`.

These numbers describe a synthetic adapter-validation record only and are not evidence about Na/Cu, CO/Cu, H/Ru, or any physical system.

Status: PASS as ingestion-boundary/software validation only.

## Reference validation provenance

The fixed hardened reference for the V1-V10 method and ingestion-boundary suite is:

- workflow: `.github/workflows/substrate-inheritance.yml`;
- GitHub Actions run: `33292821080`;
- reference commit: `9a1f357e73a27e532c755649568dde8af0b229cd`;
- conclusion: `success`;
- adversarial/unit tests: `62 passed`;
- Python: `3.12.14`;
- runner family: Ubuntu `24.04`;
- dependency integrity: `pip check` reported no broken requirements;
- uploaded artifact: `substrate-inheritance-synthetic-validation`;
- artifact ID: `9726488007`;
- validation records uploaded: 10 plus `validation_environment.txt`;
- uploaded artifact ZIP SHA-256: `332e5c463c597015a5cbe832b84ce8843be4eef688c8f62ca2e3ef4df18b7635`;
- physical thresholds frozen: false;
- real-system evidence: false.

The dependency set is pinned in `requirements-validation.txt`, the realized runtime environment is archived with the reference artifact, and the external GitHub Actions are pinned by commit SHA. `VALIDATION_ENVIRONMENT.md` records the environment and the rule for future dependency or runner changes.

This is a fixed reproducibility milestone rather than a moving `latest run` pointer. Later successful CI executions are regression evidence unless a new reference milestone is explicitly designated.

`CORRESPONDENCE_PROTOCOL_v0.2.json` freezes the non-normal and electronic-channel safeguards before any real-system inheritance target reveal. `REAL_SYSTEM_INPUT_SCHEMA_v0.2.json` freezes the real mechanical input boundary before first physical ingestion. Neither document freezes a physical promotion threshold.

## Physical evidence boundary

At the time of this ledger entry:

- no physical inheritance threshold has been frozen;
- no real-system substrate-inheritance result has been established;
- Na/Cu remains development-only and its planned `na_cu001_ci/ACTIVE_REGION_HESSIAN.json` artifact was still absent at Chemistry branch head `b0c6c8bb74ee12445b77b7a43f7a12ebf099aaf4` when last checked;
- CO/Cu remains upstream of the inheritance analysis while its frozen surface-audit/recovery sequence closes;
- H/Ru remains a contrast/limit protocol without an admitted Foundations inheritance input record.

The computational method and fail-closed ingestion path are ready. The next transition from synthetic validation to physical development evidence requires an actual provenance-complete parent governing object, child governing object, shared-degree-of-freedom mapping, modal/subspace representation, and the correspondence rule frozen before the target inheritance result is inspected.
