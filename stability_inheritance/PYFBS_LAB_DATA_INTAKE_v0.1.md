# pyFBS Academic Lab Testbench Data Intake v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Investigation:** Stability Inheritance  
**Status:** P0-Q EXTERNAL MEASURED DATA INTAKE / RAW OUTCOMES NOT YET SCORED  
**P1 eligibility:** NO  
**Purpose:** source-to-target / component-to-assembly qualification against native Frequency-Based Substructuring (FBS)

## Dataset identity and provenance

Authoritative software/documentation project:
- pyFBS: https://gitlab.com/pyFBS/pyFBS
- documentation: https://pyfbs.readthedocs.io/
- current stable package pinned for execution if needed: pyFBS 1.0.6

The official pyFBS documentation states that the academic testbench is used to evaluate and compare dynamic-substructuring methodologies and includes:
- component geometry/FEM files;
- positional sensor/impact metadata;
- experimental FRF measurements.

The package downloader points to the official public data repository:
- https://gitlab.com/pyFBS/pyFBS_data

Files admitted for the first intake:
- lab_testbench/Measurements/Y_A.p
- lab_testbench/Measurements/Y_B.p
- lab_testbench/Measurements/Y_AB.p
- lab_testbench/Measurements/coupling_example.xlsx

Expected scientific roles:
- Y_A: independently measured substructure A FRFs;
- Y_B: independently measured substructure B FRFs;
- Y_AB: independently measured assembled-system FRFs;
- coupling_example.xlsx: geometry/channel/interface metadata needed for the native coupling map.

## Rights / redistribution state

The pyFBS software package is MIT-licensed. The example-data repository is publicly downloadable and explicitly used by the official package/documentation, but a separate explicit data-license statement has not yet been located.

Therefore:
- internal P0-Q analysis of the publicly downloadable files is permitted for this working investigation;
- raw data will **not** be vendored, republished, or redistributed in the SymC repository;
- the SymC repository will retain only source URLs, hashes, file sizes, metadata summaries, code, and derived aggregate metrics;
- rights state is **CLEARED_WITH_CONSTRAINTS / NO_RAW_REDISTRIBUTION** until a dataset-specific license is confirmed.

## Outcome exposure state

Before the scoring protocol is frozen:
- raw FRF numerical values may not be inspected, plotted, summarized, or fitted;
- acquisition is limited to downloading the exact files, computing hashes/file sizes, and validating container/file readability without extracting scientific response values;
- metadata sheet names/column structure may be inspected only to define the interface map and channel correspondence, because those are design/provenance objects rather than target outcomes.

## Evidence class

All results from this dataset are:
- PUBLIC_EXTERNAL_P0Q;
- already public and ineligible for future P1 confirmation;
- eligible for measured-data method qualification and native-equivalence/refusal testing only.

## Scientific claim ceiling

This dataset can qualify whether the SI workflow can:
1. keep independently measured component/source representations separate from an independently measured assembly target;
2. freeze an explicit interface/correspondence map before assembly scoring;
3. reproduce a native LM-FBS component-to-assembly transformation;
4. preserve NATIVE_FRAMEWORK_EQUIVALENT / NO_ADDED_INHERITANCE_VALUE as valid outcomes;
5. refuse scalar or architecture labels not natively supported.

It cannot establish a novel inheritance mechanism, because experimental dynamic substructuring already predicts component-to-assembly response.

## Intake gate

The next action is acquisition-only hashing. No FRF values are scored until:
- acquisition manifest is committed;
- source hashes are known;
- interface metadata structure is inspected;
- the exact coupling/scoring protocol and outcome rule are committed prospectively.


## Acquisition-only manifest

Acquisition workflow run: 36499434590  
Outcome exposure: NO FRF numerical values inspected or scored.

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| Y_A.p | 468036 | 3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4 |
| Y_B.p | 5658516 | 2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12 |
| Y_AB.p | 9349524 | 197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7 |
| coupling_example.xlsx | 28885 | 44df97fd4f97e2bcce122afd6578113c23e2820a32f957baaeb5b4c8a4162ad4 |

The raw files were deleted from the runner before artifact upload; only the manifest was retained.

## Metadata-only inspection

Metadata workflow run: 36499498798  
Outcome exposure: NO FRF numerical values inspected.

The coupling workbook contains dedicated A, B, AB, virtual-point channel, and virtual-point reference sheets. The virtual interface contains six generalized response coordinates (three translational and three rotational), matching the documented pyFBS VPT/LM-FBS coupling formulation.

This metadata is sufficient to freeze the interface transformation and scoring design before opening the FRF payloads.
