# pyFBS Lab Measured Component-to-Assembly P0-Q Protocol v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Status:** FROZEN P0-Q EXTERNAL MEASURED QUALIFICATION BEFORE FRF SCORING  
**Dataset:** pyFBS academic lab testbench  
**Evidence class:** PUBLIC_EXTERNAL_P0Q / P1 INELIGIBLE  
**Physical Stability Inheritance claim:** NONE  
**Native comparator:** Lagrange-Multiplier Frequency-Based Substructuring (LM-FBS) with Virtual Point Transformation (VPT)

## Scientific purpose

Test whether the Stability Inheritance workflow can correctly represent a measured source-to-target assembly problem without claiming novelty over the established native method.

The test uses:
- independently measured subsystem A FRFs;
- independently measured subsystem B FRFs;
- a prospectively specified six-DOF interface/correspondence map;
- native LM-FBS to predict assembled response;
- independently measured assembled-system AB FRFs as the target.

This is the closest current nonphysical benchmark to the first four mechanistic SI gates:
1. independent source characterization;
2. explicit correspondence;
3. frozen transformation;
4. independent target prediction.

It does **not** provide a new physical intervention and does not satisfy the full six-gate inheritance ceiling.

## Frozen data identities

| File | SHA-256 |
|---|---|
| Y_A.p | 3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4 |
| Y_B.p | 2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12 |
| Y_AB.p | 197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7 |
| coupling_example.xlsx | 44df97fd4f97e2bcce122afd6578113c23e2820a32f957baaeb5b4c8a4162ad4 |

Any mismatch aborts scoring.

Raw files are downloaded from the official public pyFBS_data repository and are not redistributed in SymC artifacts.

## Frozen software route

- Python 3.12.x
- pyFBS 1.0.6
- numpy version resolved and recorded by the runner
- pandas/openpyxl versions resolved and recorded by the runner
- source metadata from coupling_example.xlsx
- no outcome-dependent channel selection or frequency-band selection

If pyFBS 1.0.6 API incompatibility blocks the documented operation, mechanical API repair is permitted only if it preserves the same VPT, six-DOF interface, LM-FBS transformation, target, and metrics. Such repair is logged before interpretation.

## Native objects and notation discipline

The measured FRF/admittance matrices are treated first as **native frequency-domain dynamic models**.

They are **not automatically relabeled**:
- as scalar chi;
- as modal/vector Chi;
- or as Chi_arc.

The benchmark first asks whether the native source-to-assembly relation is operational. Any later mapping into Stability Architecture notation requires separate admission.

Scalar chi is **NOT ADMITTED** by this protocol.

## Frozen preprocessing

Load the measured data using the documented pyFBS convention:

- each .p file contains a frequency vector and FRF array;
- transpose the FRF array to frequency x response x input ordering where necessary, following current pyFBS measured-data documentation;
- require the frequency vectors of A, B, and AB to be numerically identical within machine tolerance; otherwise stop as INVALID_DATA_ALIGNMENT;
- use every strictly positive common frequency bin in the dataset;
- no smoothing, modal fitting, frequency cropping, outlier removal, or amplitude reweighting.

Metadata sheets:
- Channels_A / Impacts_A
- Channels_B / Impacts_B
- Channels_AB / Impacts_AB
- VP_Channels
- VP_RefChannels

are used exactly to construct the native VPT/correspondence.

## Frozen VPT and interface map

Apply the documented virtual-point transformation independently to measured A and measured B using the same six generalized interface coordinates from VP_Channels / VP_RefChannels.

The coupling interface is six generalized DoFs:
- ux, uy, uz;
- rx, ry, rz.

After VPT, construct the block-diagonal uncoupled admittance:

[
Y^{A|B}=
\begin{bmatrix}
Y^A & 0\\
0 & Y^B
\end{bmatrix}.
]

Use the documented six-DoF LM-FBS mapping:
- A interface = local A indices 6:12;
- B interface = local B indices 0:6;
- equal-and-opposite compatibility/equilibrium signs.

The assembled native prediction is

[
hat Y^{AB}=Y^{A|B}
-Y^{A|B}B_f^T
(B_uY^{A|B}B_f^T)^+
B_uY^{A|B}.
]

Extract the predicted external/reference DoFs according to the documented coupling example:
- A external: local 0:6;
- B external: local 6:18;
- combined predicted reference has 18 response and 18 input DoFs.

The independently measured Y_AB is the target and may not enter VPT fitting or coupling construction.

## Frozen primary metric

Across all strictly positive common frequencies and all matched 18 x 18 target channels, compute normalized complex Frobenius error:

[
E(X,R)=
\sqrt{
\frac{\sum_{f,i,j}|X_{fij}-R_{fij}|^2}
{\sum_{f,i,j}|R_{fij}|^2}
}.
]

Primary native score:
- E_FBS = E(predicted LM-FBS assembly, measured AB).

## Frozen no-coupling baseline

Construct an external-only block-diagonal baseline from the uncoupled transformed source models:
- A external 0:6;
- B external 6:18;
- cross-substructure terms fixed to zero.

Score:
- E_UNCOUPLED = E(uncoupled external block baseline, measured AB).

This baseline is intentionally simple and is not the strongest native competitor. It asks whether the documented physical coupling operation adds explanatory value over leaving the independently measured components uncoupled.

## Frozen correspondence-specificity control

Create one deterministic wrong correspondence map by swapping x and y generalized interface coordinates on subsystem B while preserving:
- translation with translation;
- rotation with rotation;
- z and rz unchanged.

Permutation:
- [ux, uy, uz, rx, ry, rz] -> [uy, ux, uz, ry, rx, rz].

Run the otherwise identical LM-FBS construction with this wrong map.

Score:
- E_SHUFFLED = E(wrong-map assembly prediction, measured AB).

This is a **mapping-specificity control**, not a physical alternative-carrier intervention and cannot satisfy gate 6 by itself.

## Frozen secondary diagnostics

Compute:
- per-frequency normalized complex Frobenius error;
- fraction of positive-frequency bins where correct FBS error < uncoupled baseline error;
- fraction where correct FBS error < shuffled-map error;
- median and 90th percentile per-frequency error for all three routes;
- matrix dimensions, rank/conditioning diagnostics of the interface flexibility matrix;
- any numerical pseudo-inverse failure/nonfinite output count.

No frequency sub-band may be promoted after inspection to rescue the primary result. Frequency-local patterns may be recorded only as Limit Map/post-result observations.

## Frozen outcome rules

### NATIVE_FRAMEWORK_EQUIVALENT

Assign if:
- all source hashes match;
- data/frequency alignment is valid;
- correct-map LM-FBS produces finite output;
- E_FBS < E_UNCOUPLED;
- and E_FBS < E_SHUFFLED.

Interpretation:
the source-to-target relation is operational in measured data and the native FBS framework explains it. This is successful P0-Q qualification, **not SI added value**.

### NATIVE_MODEL_NOT_QUALIFIED_FOR_THIS_IMPLEMENTATION

Assign if:
- correct LM-FBS is finite but fails to beat E_UNCOUPLED or E_SHUFFLED on the frozen primary metric.

Interpretation:
do not rescue by changing bands, interface DoFs, regularization, or channels after target scoring. Investigate as a failure/outlier/root-cause branch.

### INVALID_TEST

Assign for:
- hash mismatch;
- irreconcilable frequency/dimension mismatch;
- metadata/interface mapping not executable as frozen;
- nonfinite native output caused by implementation/data incompatibility before a valid comparison exists.

### INDETERMINATE

Assign only if a valid score exists but numerical conditioning makes the ordering unreliable under machine/numerical uncertainty; the reason must be explicit.

## Stability Architecture interpretation ceiling

Even under NATIVE_FRAMEWORK_EQUIVALENT:

- measured A/B FRFs remain native source representations;
- measured AB remains an independent system-level target;
- the result does not automatically rename AB as Chi_arc;
- scalar chi remains not admitted;
- no empirical inheritance mechanism is established;
- no added-value claim beyond FBS is allowed.

The SI-relevant qualification is only that a source/correspondence/transform/independent-target workflow can be instantiated on real measured component/assembly data without circularity.

## No-retuning rule

After measured AB scoring begins, do not change:
- interface DoF count;
- VPT metadata;
- correspondence;
- channel set;
- frequency band;
- primary metric;
- wrong-map permutation;
- baseline;
- pseudo-inverse route;
- outcome rule.

Any scientifically motivated alternative becomes a new post-result P0-Q protocol and does not replace this result.

## Expected outputs

- source hash verification;
- realized environment;
- source and transformed array shapes;
- primary/secondary scores;
- interface conditioning diagnostics;
- frozen disposition;
- no raw FRF payloads committed or redistributed.
