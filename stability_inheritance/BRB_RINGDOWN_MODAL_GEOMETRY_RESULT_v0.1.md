# Brake-Reuss Beam Ringdown Modal-Geometry Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** stability_inheritance/BRB_RINGDOWN_MODAL_GEOMETRY_PROTOCOL_v0.1.md
**Workflow run:** 36522955020
**Evidence class:** PUBLIC EXTERNAL MEASURED / KNOWN-TRUTH P0-Q
**Disposition:** AMPLITUDE_CONDITIONED_MODAL_GEOMETRY
**Architecture evidence role:** ARCHITECTURE_SUPPORTING_NATIVE_MODAL_REORGANIZATION
**Novelty role:** KNOWN_NATIVE_AMPLITUDE_DEPENDENT_MODE_SHAPE_NO_SI_NOVELTY
**P1 eligibility:** NO

## Source identity

Repository:
mattiacenedese/BRBtesting

Frozen source commit:
2d42d3a618206da58642674d3287ae34dfc7d5e5

ShakerRingdown.mat:
- Git blob: 739048b2b1c71839f773ff1aecf4880fda5d62ed
- SHA-256: a62c551e34cc45257257d4e683cc9406beec2cbc1c7270329658fd9033de2f4a
- source identity: PASS

The source-code audit independently established that the DIC record is the shaker-ringdown record, that DIC index 185 is nearest Accelerometer 3, and that the DIC data are filtered around the slowest mode. The repository code uses approximately 80 Hz for the first four cycles.

## Data identity after protocol freeze

- DIC time samples: 15,915
- DIC positions per upper/lower line: 206
- concatenated spatial coordinates: 412
- time start: 30.21705 s
- time end: 33.39985 s
- dt: 0.0002 s
- source reference position: 64.53664 cm
- detected absolute reference peaks: 510

This independently confirms that the DIC record begins essentially at the source-declared post-release interval.

## Frozen amplitude strata

Top and bottom thirds of detected peak amplitudes were used exactly as preregistered.

- HIGH peaks: 170
  - fit 85
  - test 85
- LOW peaks: 170
  - fit 85
  - test 85

Reference peak medians:
- HIGH: 0.086418 mm
- LOW: 0.012132 mm

No amplitude threshold was tuned.

## Dominant spatial-subspace adequacy

Rank-1 energy fraction:

- HIGH fit: 0.99995812
- HIGH test: 0.99995801
- LOW fit: 0.99994646
- LOW test: 0.99994607

Thus the declared ringdown response remains overwhelmingly one-dimensional in spatial geometry within both amplitude strata.

This is an important Function Map result. The amplitude dependence does not erase the dominant modal skeleton.

## Held-out spatial prediction

Median projection residuals:

| Held-out stratum | Own-amplitude basis | Opposite-amplitude basis | Own / opposite |
|---|---:|---:|---:|
| HIGH | E_HH = 0.0061595 | E_LH = 0.0167698 | R_H = 0.36730 |
| LOW | E_LL = 0.0065956 | E_HL = 0.0183698 | R_L = 0.35904 |

Each amplitude-conditioned basis represents its own held-out peaks substantially better than the opposite-amplitude basis.

## Repeatability-grounded geometry comparison

- HIGH within-stratum split-half MAC: 0.99999998998
- LOW within-stratum split-half MAC: 0.99999999365
- HIGH-vs-LOW cross-stratum MAC: 0.99972856879
- HIGH-vs-LOW principal angle: 0.944000 degrees

The high/low geometric difference is small in absolute angular terms, but it is substantially larger than the observed split-half geometric variation within either stratum.

The frozen disposition therefore is:

**AMPLITUDE_CONDITIONED_MODAL_GEOMETRY**

## Independent upper/lower-line diagnostics

The result is not created by concatenating the two DIC lines.

Upper line:
- E_HH 0.006872 vs E_LH 0.017446
- E_LL 0.006545 vs E_HL 0.019271
- within-HIGH MAC 0.999999988
- within-LOW MAC 0.999999992
- cross MAC 0.999700054

Lower line:
- E_HH 0.005510 vs E_LH 0.015496
- E_LL 0.006638 vs E_HL 0.016848
- within-HIGH MAC 0.999999992
- within-LOW MAC 0.999999995
- cross MAC 0.999773476

Both independently support the same direction.

## Stability Architecture interpretation

This result supports two statements simultaneously.

### Function

**DOMINANT_MODAL_SUBSPACE_PERSISTS_ACROSS_RINGDOWN**

The spatial response remains almost perfectly rank 1 across high and low response amplitudes. Most of the native modal organization is therefore stable.

### Limit

**EXACT_MODAL_VECTOR_INVARIANCE_REFUSED_AT_MEASUREMENT_PRECISION**

The high- and low-amplitude modal vectors are not identical at the repeatability scale available in this dataset. A small amplitude-conditioned deformation of the modal geometry is reproducible and improves held-out representation.

This is a better description than either extreme:
- "the mode shape is unchanged";
- "the mode shape is completely reorganized."

The evidence supports a stable modal skeleton with fine amplitude-conditioned geometry.

## Project notation

### chi

NOT ADMITTED by this analysis. No damping/recovery scalar was used.

### Chi

**ADMITTED_NATIVE_MODAL_SUBSPACE_FOR_DECLARED_TASK**

For this measured slow-mode ringdown, the one-dimensional native DIC spatial subspace is a scientifically licensed instance of the project modal/vector layer.

The result further shows that Chi is condition-dependent at fine resolution: HIGH and LOW amplitude representations differ measurably even though both occupy a strongly conserved one-dimensional modal family.

### Chi_arc

NOT IDENTIFIED by this test alone.

## Native comparator / novelty

The associated Part II paper already reports amplitude-dependent mode-shape reconstruction from DIC. The present result is therefore:

- architecture-supporting measured evidence: YES;
- raw-data independent protocol execution: YES;
- SI-specific novelty: NO;
- native experimental modal interpretation: SUFFICIENT.

Its value to Stability Architecture is integrative. It supplies a direct measured modal/vector constituent that can now be compared with scalar and higher-order architectural evidence without pretending the constituent itself was newly discovered.

## Next architecture question

Because the same ringdown also contains amplitude-dependent frequency and damping information, the next useful nonphysical question is whether a licensed local scalar damping coordinate tracks the measured Chi geometry continuously, partially, or not at all.

That scalar-modal relation must be frozen before scalar extraction and must carry post-result/P0-D status because the positive Chi geometry result is already known.
