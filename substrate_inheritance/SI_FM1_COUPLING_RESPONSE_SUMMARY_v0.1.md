# SI FM1 Coupling-Response Function/Limit Map Summary v0.1

**Date:** 2026-09-13  
**Plan:** `SI_FM1_COUPLING_RESPONSE_PLAN_v0.1.json`  
**Program map:** `SI_FUNCTION_LIMIT_MAP_PLAN_v0.1.json`  
**Epistemic status:** P0-D descriptive/structural synthetic Function/Limit mapping only  
**Physical inheritance claim:** false  
**Physical threshold frozen:** false  
**Atlas target used for selection:** false

## Purpose

FM1 asks how carrier correspondence, substrate participation, embedded response, intervention sensitivity, and coupling specificity vary across an ordinary synthetic range of coupling strength and carrier-geometry mismatch while the clean substrate spectrum is held fixed.

The map is deliberately broader than a failure-boundary scan. It records both the supported interior and the regions where simple carrier matching becomes weaker or potentially misleading.

## Execution

The frozen map retained all combinations of:

- 6 carrier-geometry angles;
- 6 coupling strengths;
- 36 total synthetic cases.

No master score, system scalar, physical inheritance cutoff, Atlas target, or post-result parameter deletion was introduced.

The corresponding GitHub Actions validation run was `34699663974`, head `8a8d46fc148345abe77a9c139d55dc2ef7d90164`. The validation suite completed with `149 passed`.

FM1 artifact:

- name: `substrate-inheritance-fm1-coupling-response-v01`;
- artifact ID: `10300106281`;
- artifact digest: `sha256:f34d2dfa48a22d70b6b8cf14d63a13fc0f0321843bfb65fcdf0a257f738586db`.

These identifiers establish computational provenance. They do not promote the result beyond P0-D.

## Global Function/Limit landscape

Across the complete 36-case surface:

### Carrier assignment mean overlap

- maximum: `1.0`;
- median: approximately `0.91595`;
- minimum: approximately `0.66575`.

### Substrate participation

- maximum: `1.0`;
- median: approximately `0.99434`;
- minimum: approximately `0.75006`.

### Carrier-overlap advantage over frequency-only assignment

- maximum: approximately `0.22066`;
- median: `0`;
- minimum: `0`.

### Coupling-rewire relative response-curve change

- maximum: approximately `1.7724`;
- median: approximately `1.08783`;
- minimum: `0`.

### Embedded response-curve norm

- maximum: approximately `2.30577`;
- median: approximately `0.06078`;
- minimum: `0`.

### Frequency-only assignment carrier overlap

- maximum: `1.0`;
- median: approximately `0.91595`;
- minimum: approximately `0.46595`.

### Frequency-only total absolute frequency error

- maximum: approximately `0.33687`;
- median: approximately `0.08909`.

### Intervention derivative magnitude

- maximum: approximately `13.42087`;
- median: approximately `0.01784`;
- minimum: `0`.

### Numerical conditioning

Maximum substrate dynamic-stiffness condition number over the map was approximately `25.3768`.

## Zero-coupling control

At coupling strength `g = 0`:

- embedded response contribution = `0`;
- coupling-rewire response change = `0`;
- intervention derivative = `0`;
- substrate participation remains approximately `1` in the constructed clean-substrate carrier comparison.

This is an important semantic control: the analysis does not manufacture embedding influence when the parent-child coupling is removed.

## Coupling-strength Function Map

Representative medians by coupling strength:

| coupling `g` | embedded response norm | coupling-rewire relative change | intervention derivative magnitude |
|---:|---:|---:|---:|
| 0.00 | 0 | 0 | 0 |
| 0.05 | ~0.00325 | ~1.13966 | ~0.00130 |
| 0.15 | ~0.02538 | ~1.23513 | ~0.01331 |
| 0.35 | ~0.11370 | ~1.32743 | ~0.09702 |
| 0.70 | ~0.40319 | ~1.22557 | ~0.75426 |
| 1.20 | ~1.93203 | ~1.08031 | ~10.7414 |

Within this synthetic family, stronger coupling increases the magnitude of the embedded response and intervention sensitivity strongly. The coupling-rewire response remains substantial over nonzero coupling, showing that response is not fixed by the clean substrate spectrum or coupling magnitude alone.

The rewire statistic is not interpreted as a universal monotonic law because it does not increase monotonically over the entire grid.

## Carrier-geometry Function/Limit Map

Median carrier-overlap assignment score by carrier-geometry angle:

| angle | median carrier overlap |
|---:|---:|
| 0.00 | ~0.99993 |
| 0.08 | ~0.99471 |
| 0.20 | ~0.97012 |
| 0.40 | ~0.88890 |
| 0.70 | ~0.69881 |
| 1.00 | ~0.69468 |

Carrier correspondence weakens as the planted carrier geometry is rotated away from the reference relation.

At angle `1.00`, carrier-resolved assignment retained a median advantage of approximately `0.21678` over frequency-only assignment. This is a concrete synthetic example in which small/favorable frequency matching is insufficient to identify the correct carrier relation.

No numerical carrier-overlap value from this map is promoted into a physical inheritance threshold.

## What FM1 establishes at P0-D

For this synthetic generator:

1. Holding the clean substrate spectrum fixed does not fix the embedded child response.
2. Parent-child coupling magnitude changes realized embedded response and intervention sensitivity.
3. Rewiring the coupling can change the response strongly without changing the parent spectrum.
4. Carrier geometry matters independently of scalar spectral similarity.
5. Frequency-only matching can become materially misleading as carrier geometry diverges.
6. The functioning interior contains graded changes in participation, response, specificity, and correspondence rather than a single pass/fail boundary.
7. No single scalar in the current map captures these quantities jointly without additional derivation.

This supports continued relational and carrier-resolved investigation. It does **not** establish physical substrate inheritance, a universal coupling law, a universal threshold, or a system chi.

## Limits and negative information retained

- The map is synthetic and construction-specific.
- The clean substrate spectrum was deliberately fixed; real materials may reorganize the parent operator itself.
- Carrier-overlap decline is gradual in this grid and no physical cutoff is inferred.
- Coupling-rewire sensitivity is non-monotonic over the full coupling range.
- Response magnitude, intervention sensitivity, participation, and carrier correspondence are not interchangeable quantities.
- Atlas placement played no role in parameter or metric selection.

## Balance disposition

**Function Map:** represented by the ordinary coupling/geometry response surface and continuous carrier/response changes.

**Limit Map:** represented by progressive carrier ambiguity, increasing mismatch between frequency-only and carrier-resolved assignment, and conditioning/representation diagnostics.

Neither side erases the other.

## Next step

Under the already-frozen `SI_FUNCTION_LIMIT_MAP_PLAN_v0.1.json` execution order, the next P0-D investigation is:

`FM3_LINEAGE_FLOW_LANDSCAPE`

FM3 will map persistence, splitting, mixing, reconvergence, extinction, dominant-margin behavior, entropy/effective-child-count structure, subspace preservation, and nonidentifiability across transformation strength, spectral crowding, and uncertainty magnitude. Relative flow remains descriptive and is not a probability, inheritance percentage, causal fraction, or promotion score.
