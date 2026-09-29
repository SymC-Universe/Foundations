# pyFBS Current-Metadata Measured SVT/LM-FBS Decoupling Protocol v0.4

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE Y_A TARGET DOWNLOAD / SCORING
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**P1 eligibility:** NO
**Architecture evidence role if successful:** ARCHITECTURE_SUPPORTING_NATIVE_HIERARCHICAL_TRANSFORMATION
**Novelty role:** NATIVE_FRAMEWORK_EQUIVALENT / no SI-specific mechanism claim

## Provenance

Earlier pyFBS measured routes failed before valid scoring because they used stale or incompatible metadata. Those failures remain preserved.

A current-official-notebook audit then identified the maintained SVT route:
- metadata: decoupling_example_SVT.xlsx;
- k = 6;
- grouping = [1,10];
- SVT basis estimated from measured B;
- same SVT applied to B and AB;
- 18 x 18 uncoupling block;
- recovered A extracted at reduced indices 6:12.

A pre-target v0.3 compatibility test used only B and AB and returned CURRENT_SVT_ROUTE_EXECUTABLE:
- B transformed shape = 801 x 6 x 6;
- AB transformed shape = 801 x 12 x 12;
- all transformed values finite;
- Y_A was not downloaded.

The v0.4 scoring protocol is frozen now, before Y_A is downloaded.

## Frozen source identities

Runtime source base:
https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/

Measured FRFs:
- Y_A.p expected SHA-256:
  3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4
- Y_B.p expected SHA-256:
  2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12
- Y_AB.p expected SHA-256:
  197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7

Current official SVT metadata:
- decoupling_example_SVT.xlsx SHA-256:
  a8fd8d0e42a85b0bd0837b9b54bf235ab2d489114e1b9c680f7a42184a59dd08

Package:
- pyFBS 1.0.6

Any source mismatch is INVALID_TEST.

## Frozen native transformation

Load all FRFs using the documented transpose:
- stored response x input x frequency;
- analysis frequency x response x input.

Read from decoupling_example_SVT.xlsx:
- Channels_B / Impacts_B;
- Channels_AB / Impacts_AB.

Construct the native SVT exactly:
- k = 6;
- grouping = [1,10];
- basis estimated from B;
- same transform applied to B and AB.

Expected:
- B_SVT = frequency x 6 x 6;
- AB_SVT = frequency x 12 x 12.

Construct the uncoupling block Y_AB_un as:
- AB_SVT in rows/cols 0:12;
- -B_SVT in rows/cols 12:18.

Construct compatibility/equilibrium matrices:
- Bu = Bf;
- Bu[:,0:6] = I;
- Bu[:,12:18] = -I;
- all other entries zero.

Apply LM-FBS decoupling:

Y_int = Bu Y_AB_un Bf^T

Y_dec = Y_AB_un
        - Y_AB_un Bf^T pinv(Y_int) Bu Y_AB_un

Extract:
- Y_A_hat = Y_dec[:,6:12,6:12].

Independent target:
- Y_A_ref = measured Y_A.p.

No Y_A value enters the SVT basis, correspondence map, decoupling transform, or extraction indices.

## Frozen frequency handling

Primary score uses all common strictly positive frequency bins.

Do not crop a frequency range after target access.

DC is excluded only because dynamic FRF normalization at zero frequency is not needed for this declared comparison.

No smoothing, modal fitting, outlier removal, or target-informed frequency weighting is allowed.

## Frozen primary metric

For prediction X and independent target Y_A_ref:

E(X) =
sqrt(
  sum_{f,i,j} |X_fij - Y_A_ref,fij|^2
  /
  sum_{f,i,j} |Y_A_ref,fij|^2
)

Primary native score:
- E_DEC = E(Y_A_hat).

Frozen no-decoupling baseline:
- Y_BASE = AB_SVT[:,6:12,6:12].
- E_BASE = E(Y_BASE).

The baseline asks whether removing the measured B component through the documented native transform moves the A-side assembly response closer to independently measured free A than leaving the assembly influence in place.

## Frozen primary dispositions

### NATIVE_FRAMEWORK_EQUIVALENT

Assign if:
- all hashes and dimensions pass;
- all native transforms and decoupling outputs are finite;
- E_DEC < E_BASE.

Architecture evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_HIERARCHICAL_TRANSFORMATION.

Meaning:
measured component B plus measured assembly AB, connected through the established native correspondence/transformation, recover independently measured component A better than the no-decoupling assembly-side baseline.

This is positive evidence toward the Stability Architecture reconstruction while the native pyFBS/LM-FBS framework remains the sufficient explanation.

### NATIVE_MODEL_NOT_QUALIFIED_FOR_THIS_IMPLEMENTATION

Assign if a valid finite native score exists but E_DEC >= E_BASE.

Do not rescue by changing k, metadata, grouping, frequency range, extraction indices, pseudo-inverse route, or metric.

### INVALID_TEST

Assign if any source identity, dimension, transform, frequency, or finite-value condition fails before a valid primary score exists.

### INDETERMINATE

Reserve for a valid finite result where E_DEC and E_BASE cannot be ordered beyond numerical precision.

## Frozen correspondence-specificity diagnostic

This is secondary and cannot change the primary disposition.

Create a deterministic wrong reduced-coordinate correspondence by swapping the first two B-side reduced interface coordinates in the negative block of Bu and Bf, leaving the AB side unchanged.

Compute:
- Y_A_shuffled;
- E_SHUFFLED.

Report:
- MAPPING_SPECIFICITY_SUPPORTED if E_DEC < E_SHUFFLED;
- MAPPING_SPECIFICITY_NOT_SHOWN otherwise.

Because SVT coordinates are reduced singular-vector coordinates rather than guaranteed one-to-one physical carrier axes, this diagnostic is not required for native-framework qualification and cannot be used to rescue the primary result.

## Frozen secondary diagnostics

Report:
- per-frequency normalized complex Frobenius error for DEC, BASE, SHUFFLED;
- fraction of positive-frequency bins where DEC < BASE;
- fraction where DEC < SHUFFLED;
- median and 90th-percentile per-frequency error for all three;
- median, p90, and maximum condition number of Y_int;
- nonfinite count;
- exact source hashes and transformed shapes.

No secondary diagnostic may replace the primary score.

## Stability Architecture interpretation ceiling

If successful, this is stronger architecture evidence than a generic nonlinear-vs-linear benchmark because it contains:
- independently measured lower-level/component object B;
- independently measured assembled object AB;
- explicit documented correspondence/transformation;
- independent A target that was sealed through transform qualification;
- native hierarchical recovery operation.

It still does not establish:
- SI-specific added value beyond the native framework;
- a universal inheritance law;
- a new physical carrier;
- a physical project chi;
- that native FRFs must be renamed capital Chi;
- that the recovered A or AB object uniquely equals Chi_arc.

The correct dual classification is:
- architecture evidence: potentially SUPPORTING;
- novelty/added-value: NATIVE_FRAMEWORK_EQUIVALENT if successful.

## No-retuning rule

After Y_A download begins, do not change:
- metadata file/hash;
- k;
- grouping;
- B-derived SVT;
- uncoupling block;
- Bu/Bf;
- extraction indices;
- positive-frequency support;
- primary metric;
- baseline;
- pseudo-inverse operation;
- primary disposition rule.
