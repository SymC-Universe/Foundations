# pyFBS Current-Metadata Measured SVT/LM-FBS Result v0.4

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** stability_inheritance/PYFBS_CURRENT_METADATA_SVT_LMFBS_PROTOCOL_v0.4.md
**Successful workflow run:** 36516521576
**Mechanical no-data retry:** v0.4a runner only
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**Disposition:** NATIVE_FRAMEWORK_EQUIVALENT
**Architecture evidence role:** ARCHITECTURE_SUPPORTING_NATIVE_HIERARCHICAL_TRANSFORMATION
**Novelty role:** NATIVE_FRAMEWORK_EQUIVALENT
**P1 eligibility:** NO

## Provenance and target seal

The scientific protocol was frozen before Y_A was downloaded.

The first execution attempt failed at import before any source download, so it did not expose A, B, or AB and did not alter the frozen scientific protocol. The v0.4a retry changed only dependency installation.

Verified source identities:

- Y_A.p:
  3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4
- Y_B.p:
  2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12
- Y_AB.p:
  197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7
- decoupling_example_SVT.xlsx:
  a8fd8d0e42a85b0bd0837b9b54bf235ab2d489114e1b9c680f7a42184a59dd08

The current official metadata produced the documented transformed shapes:
- B: 801 x 6 x 6
- AB: 801 x 12 x 12
- recovered A: 801 x 6 x 6.

## Frozen primary result

Primary support:
- all 800 strictly positive common frequency bins;
- 2.5 Hz through 2000 Hz.

Normalized complex Frobenius errors:

| Representation | Error |
|---|---:|
| Native SVT/LM-FBS recovered A | 1.2031285 |
| No-decoupling AB A-side baseline | 1.2533293 |
| Deterministic wrong reduced-coordinate map | 1.2063877 |

Relative improvement of native decoupling versus the no-decoupling baseline:

**4.0054%**

Frozen primary disposition:

**NATIVE_FRAMEWORK_EQUIVALENT**

The native measured component/assembly transformation moves the A-side assembly response closer to the independently measured free-A reference than leaving B coupled.

## Frequency-resolved behavior

- DEC error < BASE error at 80.25% of positive-frequency bins.
- DEC error < SHUFFLED error at 49.625% of bins.

Per-frequency normalized errors:

| Diagnostic | Median | 90th percentile |
|---|---:|---:|
| DEC | 0.75957 | 1.53157 |
| BASE | 1.20738 | 3.89218 |
| SHUFFLED | 0.87403 | 1.99737 |

The decoupled result therefore shows broad improvement relative to the no-decoupling baseline, even though the global normalized error remains greater than 1.

## Conditioning

Condition number of the 6 x 6 native interface matrix across positive frequencies:

- median: 380.80
- p90: 3822.27
- maximum: 22321.79
- nonfinite count: 0.

All scored output arrays were finite.

The high and strongly varying condition numbers are a material Limit Map feature and caution against interpreting global recovery error as a clean, uniformly resolved transformation.

## Correspondence-specificity diagnostic

The predeclared deterministic reduced-coordinate swap gave:

- E_DEC = 1.20313
- E_SHUFFLED = 1.20639.

By the frozen scalar diagnostic rule this is:

**MAPPING_SPECIFICITY_SUPPORTED**

However:
- the global difference is small;
- DEC beats SHUFFLED in only 49.625% of positive-frequency bins;
- the reduced SVT coordinates are not guaranteed one-to-one physical carrier axes.

Therefore this diagnostic is weak and cannot support a carrier-specific inheritance claim.

## Architecture interpretation

This is an important measured architectural piece because it contains:

1. independently measured component B;
2. independently measured assembled system AB;
3. an explicit native correspondence/transformation fixed from B and AB;
4. an independently measured A target sealed through transformation qualification;
5. a native operation that partially recovers A from the assembly/component pair.

This provides direct measured evidence that component-level and assembly-level response objects are related through an operational hierarchical transformation.

The correct dual classification is:

- **architecture evidence:** ARCHITECTURE_SUPPORTING_NATIVE_HIERARCHICAL_TRANSFORMATION
- **novelty / added value:** NATIVE_FRAMEWORK_EQUIVALENT

The native pyFBS/SVT/LM-FBS framework is sufficient to explain the measured relation. Stability Inheritance does not own this mechanism.

## Function Map additions

- MEASURED_COMPONENT_ASSEMBLY_RELATION_OPERATIONAL_UNDER_NATIVE_TRANSFORMATION
- INDEPENDENT_COMPONENT_TARGET_PARTIALLY_RECOVERABLE_FROM_ASSEMBLY_PLUS_COMPONENT
- NATIVE_HIERARCHICAL_TRANSFORMATION_IMPROVES_OVER_NO_DECOUPLING

## Limit Map additions

- ABSOLUTE_RECOVERY_ERROR_REMAINS_LARGE
- INTERFACE_TRANSFORMATION_IS_STRONGLY_FREQUENCY_CONDITIONED
- REDUCED_COORDINATE_MAPPING_SPECIFICITY_WEAK
- NATIVE_FRAMEWORK_EQUIVALENCE_DOES_NOT_ESTABLISH_SI_ADDED_VALUE

## Claim ceiling

No physical project chi is admitted.

The native FRF matrices are not automatically renamed capital Chi.

The assembly/recovered objects are not automatically equated with Chi_arc.

No carrier-resolved inheritance claim is promoted.

No new substructuring mechanism is claimed.

The result strengthens the integrated Stability Architecture case by establishing a measured hierarchical transformation piece under established native theory.
