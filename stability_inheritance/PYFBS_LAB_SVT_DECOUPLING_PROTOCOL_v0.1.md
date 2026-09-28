# pyFBS Lab Measured SVT Decoupling P0-Q Protocol v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Status:** NEW POST-INVALID-TEST PROTOCOL / FROZEN BEFORE VALID TARGET SCORING  
**Evidence class:** PUBLIC_EXTERNAL_P0Q / P1 INELIGIBLE  
**Native method:** Singular Vector Transformation (SVT) + Lagrange-Multiplier Frequency-Based Substructuring (LM-FBS) decoupling  
**Empirical Stability Inheritance claim:** NONE

## Provenance and reason for new protocol

The preceding component-to-assembly protocol is permanently preserved as INVALID_TEST because `coupling_example.xlsx` did not match the measured `Y_A.p` dimensions.

A shape/metadata identity audit performed after that invalid test established, without scoring FRF values:

- Y_A raw FRF shape: 6 x 6 x 801;
- Y_B raw FRF shape: 21 x 21 x 801;
- Y_AB raw FRF shape: 27 x 27 x 801;
- `decoupling_example.xlsx` channel/impact counts: A=6/6, B=21/21, AB=27/27.

The official pyFBS measured SVT-decoupling example explicitly loads these three measured FRFs, applies an SVT basis extracted from B to B and AB, then uses LM-FBS to recover A and compares the result with independently measured A.

This new protocol does not erase or replace the invalid coupling protocol.

## Frozen source identities

| File | SHA-256 |
|---|---|
| Y_A.p | 3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4 |
| Y_B.p | 2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12 |
| Y_AB.p | 197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7 |
| decoupling_example.xlsx | 20d246430c163c5abd935d71f36a65b470fd3b0fff6243a81d1e2cc0099a04a9 |

Any mismatch aborts the test.

## Frozen native operation

Load the measured FRFs using the documented transpose:
- raw response x input x frequency;
- transformed to frequency x response x input.

Use metadata sheets:
- Channels_B / Impacts_B;
- Channels_AB / Impacts_AB.

Freeze the documented SVT construction:
- reduced dimension k = 6;
- SVT basis estimated from measured B;
- documented interval argument [1, 10];
- the same reduction spaces applied to B and AB.

Expected transformed dimensions under the documented example:
- B_SVT: 6 x 6 at each frequency;
- AB_SVT: 12 x 12 at each frequency.

Construct the decoupling block:
- AB_SVT in the first 12 x 12 block;
- minus B_SVT in the final 6 x 6 block.

Compatibility/equilibrium:
- six interface rows;
- AB interface = reduced indices 0:6;
- B interface = block indices 12:18;
- Bf = Bu.

Apply native LM-FBS decoupling exactly:

[
Y_{int}=B_uY^{AB|-B}B_f^T
]

[
Y_{dec}=Y^{AB|-B}
-Y^{AB|-B}B_f^TY_{int}^{+}B_uY^{AB|-B}.
]

Extract recovered A:
- indices 6:12 for both response and input.

Independently measured Y_A is the target reference and is not used to construct the SVT basis, transformation, or decoupling map.

## Frequency handling

Use every strictly positive common frequency bin.

No frequency cropping, post-result band selection, smoothing, modal fitting, or outlier removal is permitted in the primary analysis.

## Frozen primary metric

For recovered A (hat Y_A) and independently measured reference (Y_A):

[
E_{DEC}=
sqrt{
rac{sum_{f,i,j}|hat Y_{A,fij}-Y_{A,fij}|^2}
{sum_{f,i,j}|Y_{A,fij}|^2}
}.
]

## Frozen no-decoupling baseline

Before subtracting B, use the A-side external 6 x 6 block of the transformed AB representation as the no-decoupling baseline:

[
Y_{BASE}=Y_{AB,SVT}[:,6:12,6:12].
]

Score:

[
E_{BASE}=E(Y_{BASE},Y_A).
]

The baseline asks whether native decoupling improves recovery of independently measured A relative to leaving B's assembly influence in place.

## Frozen mapping-specificity diagnostic

Create a deterministic wrong correspondence by swapping the first two reduced B coordinates when forming the B side of the compatibility/equilibrium map while leaving AB unchanged.

Score:
- E_SHUFFLED.

This is only a diagnostic of correspondence sensitivity. Because SVT coordinates are reduced singular-vector coordinates rather than guaranteed physical axes, success of the native method does **not** require E_DEC < E_SHUFFLED.

Record:
- MAPPING_SPECIFICITY_SUPPORTED if E_DEC < E_SHUFFLED;
- MAPPING_SPECIFICITY_NOT_SHOWN otherwise.

Do not use this diagnostic to rescue or reject the primary native decoupling outcome.

## Secondary diagnostics

Compute:
- per-frequency normalized complex Frobenius errors for DEC, BASE, SHUFFLED;
- fraction of positive-frequency bins with DEC < BASE;
- fraction with DEC < SHUFFLED;
- median and 90th-percentile per-frequency errors;
- interface-matrix condition-number median, p90, and maximum;
- nonfinite output counts.

No secondary diagnostic may replace the frozen primary metric after inspection.

## Frozen primary outcome rule

### NATIVE_FRAMEWORK_EQUIVALENT

Assign if:
- all source hashes match;
- dimensions/frequencies match the frozen identity;
- documented SVT and LM-FBS produce finite output;
- E_DEC < E_BASE.

Meaning:
the measured assembly/component relation is operational through the established native decoupling framework. This is successful source/transform/independent-target P0-Q qualification and **not SI added value**.

### NATIVE_MODEL_NOT_QUALIFIED_FOR_THIS_IMPLEMENTATION

Assign if a valid finite native decoupling score exists but E_DEC >= E_BASE.

No rescue by changing k, [1,10], frequency band, reference channels, regularization, or metric.

### INVALID_TEST

Assign if source identity fails, documented API/data dimensions cannot execute, or no valid finite score can be produced.

### INDETERMINATE

Reserve for a valid score whose ordering against baseline is numerically unresolved under explicit numerical tolerance/conditioning evidence.

## Stability Architecture interpretation ceiling

- Y_A, Y_B, and Y_AB remain native measured FRF objects.
- chi is NOT ADMITTED.
- Chi is NOT FORCED merely because the objects are multivariate.
- Y_A reference is an independent target but is not automatically relabeled Chi_arc.
- successful native decoupling does not establish inheritance;
- native FBS remains the sufficient explanation for the tested source/target relation.

The SI-relevant result is only whether the workflow can preserve independent objects, correspondence, transformation, and target comparison on real measured hierarchical data without circularity.

## No-retuning rule

After valid target scoring begins, do not change:
- k=6;
- interval [1,10];
- source metadata;
- frequency domain;
- primary metric;
- baseline;
- extraction indices;
- pseudo-inverse route;
- outcome rule.

Any alternative is a new post-result P0-Q protocol.
