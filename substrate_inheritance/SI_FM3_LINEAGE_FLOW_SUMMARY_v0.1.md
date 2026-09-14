# SI FM3 Lineage-Flow Function/Limit Map Summary v0.1

**Date:** 2026-09-13  
**Plan:** `SI_FM3_LINEAGE_FLOW_PLAN_v0.1.json`  
**Program map:** `SI_FUNCTION_LIMIT_MAP_PLAN_v0.1.json`  
**Epistemic status:** P0-D descriptive/structural synthetic Function/Limit mapping only  
**Physical inheritance claim:** false  
**Physical threshold frozen:** false  
**Atlas target used for selection:** false

## Purpose

FM3 maps how carrier persistence, splitting/mixing, reconvergence, and identifiability behave across repeated same-spectrum transformations when transformation strength, spectral crowding, and perturbation magnitude vary.

The map also stress-tests the program's existing row-normalized multi-generation `relative lineage flow` representation against a direct start-to-final carrier comparison. This is important because a convenient flow summary must not be allowed to overwrite carrier geometry that the full representation still preserves.

## Frozen construction

The unperturbed synthetic family used a real symmetric three-mode operator with eigenvalues

`[1.0, 1.0 + spectral_gap, 3.0]`.

The exact carrier bases followed:

- generation 0: identity;
- generation 1: `R13(theta)`;
- generation 2: `R23(theta) @ R13(theta)`;
- generation 3: identity reconvergence reference.

Thus the scalar spectrum is identical at every generation, while carrier geometry changes and then returns exactly to the starting basis.

The full frozen grid retained:

- 5 transformation strengths;
- 5 spectral gaps;
- 5 perturbation magnitudes;
- 32 fixed perturbation seeds per parameter case;
- 125 parameter cases;
- 4,000 seed-expanded evaluations.

No post-result threshold, seed selection, Atlas target, chi coordinate, or promotion rule was introduced.

## Validation provenance

Dedicated workflow:

- GitHub Actions run: `34756644076`;
- head used for the dedicated FM3 execution: `91f879ee06b8d1afd3f4bff715a75e1086092332`;
- dedicated FM3 tests: `6 passed`;
- workflow conclusion: `success`.

Artifact:

- name: `substrate-inheritance-fm3-lineage-flow-v01`;
- artifact ID: `10317572637`;
- artifact SHA-256: `21e4c21b318cd86cc1ed83ecf05d242ebc26d705f7c1b270fec8ac2c5e320049`.

Generated result SHA-256:

`e59179fc993a9354ca1531f0c8ac673c78df0c96dc193c4e2ce81505a912e9a5`.

These identifiers establish computational provenance only. They do not promote the result beyond P0-D.

## Primary result: direct reconvergence survives, sequential normalized flow does not

By construction, the exact final carrier basis returns to the initial basis. Direct generation-0 to generation-3 carrier correspondence therefore reconverged exactly to identity:

- maximum exact direct reconvergence error from identity: `0.0`.

However, sequential row-normalized relative-flow propagation generally did **not** return to the same direct end-to-end state.

Exact unperturbed sequential-flow versus direct-carrier L1 discrepancy across the frozen landscape:

- minimum: `0.0`;
- median: approximately `0.4398612`;
- maximum: approximately `1.25`.

By transformation strength, the exact discrepancy was approximately:

| theta (rad) | exact sequential-flow vs direct L1 |
|---:|---:|
| 0.0000 | 0.0000 |
| 0.1500 | 0.08831 |
| 0.3500 | 0.43986 |
| 0.6000 | 1.00892 |
| 0.7854 | 1.25000 |

The perturbed-ensemble median landscape retained the same broad pattern, with overall median approximately `0.4398612` and maximum approximately `1.25`.

### Interpretation

This is a method-limit result.

`relative lineage flow` is useful as a descriptive summary of local splitting/mixing and descendant weight propagation, but row normalization and repeated weight propagation discard information needed to reconstruct exact multi-generation carrier geometry.

Therefore:

`sequential normalized flow disagreement != physical lineage loss`

when a direct carrier/subspace calculation demonstrates reconvergence.

The current flow object must remain explicitly descriptive. It is not a conserved lineage state, probability, causal fraction, inheritance percentage, or promotion score.

## Identifiability landscape

Across all 125 perturbation-envelope cases:

- direct generation-0 to generation-3 parent-0 interval-identifiable fraction: `0.8`;
- fraction of parameter cases in which **all** transition rows remained interval-identifiable: `0.632`.

Direct start-to-final carrier identity remained interval-identifiable for every tested spectral gap at perturbation magnitudes:

- `0`;
- `1e-4`;
- `1e-3`.

At relative perturbation `1e-2`, direct parent-0 identity became nonidentifiable for the two most crowded gaps:

- `0.01`;
- `0.03`.

At relative perturbation `0.05`, it also became nonidentifiable at gap `0.1`, while gaps `0.3` and `1.0` remained identifiable in this frozen ensemble.

These perturbation envelopes are descriptive seeded minimum/maximum ranges, not confidence intervals and not physical noise calibration.

## Splitting and transformation-strength behavior

At `theta = pi/4`, the first exact transition gives an equal `0.5 / 0.5` carrier split for the affected parent carrier. The dominant-lineage routine correctly refuses a unique descendant rather than breaking the exact tie arbitrarily.

Across increasing transformation strength, individual transition identifiability degrades and the descriptive sequential-flow discrepancy increases. This is a Function/Limit landscape, not evidence for a universal angular cutoff.

## Crowded-subspace behavior

The map retains a two-dimensional low-eigenvalue subspace diagnostic separately from individual carrier identity.

In crowded/perturbed regimes, individual carrier identification can become ambiguous while the corresponding two-dimensional subspace remains substantially better preserved.

This reinforces the existing SI rule:

`individual carrier nonidentifiability != subspace loss`.

A future physical lineage analysis must therefore retain projector/subspace geometry wherever crowding or near-degeneracy makes individual vectors unstable.

## Extinction disposition

This FM3 construction is full-rank and same-spectrum by design. It does not create a true extinction channel.

Result:

`extinction_status = NOT_PRESENT_IN_FULL_RANK_SAME_SPECTRUM_CONSTRUCTION`.

No synthetic zeroing rule was added after inspection merely to make extinction appear. A separate construction would be required to study genuine loss/extinction.

## What FM3 establishes at P0-D

For this declared synthetic family:

1. Same scalar spectrum does not determine carrier lineage geometry.
2. Exact ties can and should produce a nonidentifiable descendant rather than an arbitrary winner.
3. Individual carrier identity can degrade while a containing subspace remains better preserved.
4. Direct end-to-end carrier correspondence can recover exact reconvergence that sequential normalized-flow summaries lose.
5. Therefore lineage must remain a layered object: local transition correspondence, uncertainty/identifiability, subspace geometry, and direct higher-generation comparison cannot be collapsed into one normalized flow vector without information loss.

None of these results establishes physical substrate inheritance or a universal cross-scale lineage law.

## Balance disposition

**Function Map:** continuous splitting/mixing, dominant-fraction, entropy/effective-child-count, and relative-flow behavior across ordinary transformation strengths.

**Limit Map:** exact ties, perturbation-driven nonidentifiability, crowded-subspace versus individual-carrier divergence, and demonstrated loss of end-to-end information under sequential normalized-flow reduction.

The negative method result is retained as part of the target rather than repaired away.

## Next step

Under the frozen `SI_FUNCTION_LIMIT_MAP_PLAN_v0.1.json` execution order, the next investigation is:

`FM2_EMBEDDING_DEPTH_LANDSCAPE`.

FM2 is a synthetic reduction-depth problem. It will map the amount of parent substrate needed to reproduce an analytic semi-infinite embedded response across coupling and probe conditions. Any reported effective depth is a numerical/model-reduction depth for the declared task, not a physical inheritance length.
