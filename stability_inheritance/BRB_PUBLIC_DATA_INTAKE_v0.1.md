# Brake-Reuss Beam Public Data Intake v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Source repository:** mattiacenedese/BRBtesting
**Frozen source commit:** 2d42d3a618206da58642674d3287ae34dfc7d5e5
**Repository license:** GPL-3.0
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**Status:** FROZEN METADATA-ONLY INTAKE
**P1 eligibility:** NO
**Numeric response scoring:** PROHIBITED

## Scientific role

The Brake-Reuss Beam is a bolted lap-joint benchmark with measured hammer-impact, forced-response, and resonance-decay data. The resonance-decay dataset also contains full-field DIC measurements according to the source README and associated Part I measurement paper.

The intended Stability Architecture role is to test whether modal/vector response organization changes with response amplitude in a jointed structure. This targets the modal/vector layer more directly than prior scalar/model-comparison benchmarks.

No such test is authorized by this intake. The intake only establishes file identity and internal data layout.

## Frozen repository files

At source commit 2d42d3a618206da58642674d3287ae34dfc7d5e5:

- ForcedFrequencyResponses.mat
  - Git blob: 466a68a7655f344c753625a1f5a3b02ef365bb40
  - bytes: 12,527
- HammerImpact.mat
  - Git blob: aba81f3d9b2a62a9a43782da51585e0780ad959d
  - bytes: 979,254
- ShakerRingdown.mat
  - Git blob: 739048b2b1c71839f773ff1aecf4880fda5d62ed
  - bytes: 56,919,612
- showData.mlx
  - Git blob: 2cc7f972823328d6ace9b3ec957147a221ae4b09
  - bytes: 1,756,787

## Allowed intake operations

For the three MAT files:

- download from raw.githubusercontent.com pinned to the frozen commit;
- verify byte size and Git blob SHA;
- compute SHA-256;
- read MAT-file header/version;
- list top-level variable/dataset names, shapes, dtypes/classes, and nesting metadata only;
- for MATLAB v7.3/HDF5, list HDF5 group/dataset paths, shapes, and dtypes without reading dataset values.

For showData.mlx:

- verify byte size/Git blob SHA and SHA-256;
- inspect the zipped MATLAB live-script package only for text/code XML sufficient to identify variable names and intended plotting/measurement semantics;
- do not execute the script;
- do not extract numerical result values from embedded outputs.

## Prohibited operations

- no numerical array values;
- no plots or response summaries;
- no peak/mode selection from outcomes;
- no amplitude bins;
- no modal/subspace metrics;
- no DIC spatial scoring;
- no comparison among ringdown levels;
- no threshold or endpoint selection from numeric results.

## Intake dispositions

- BRB_LAYOUT_QUALIFIED if source identities match and enough metadata/code semantics exist to define a prospective ringdown modal/vector test without numeric outcome inspection.
- BRB_LAYOUT_NEEDS_MAPPING if the source is valid but data organization remains ambiguous without a non-value mapping step.
- BRB_SOURCE_IDENTITY_MISMATCH if bytes/blob identities differ.
- BRB_LAYOUT_INVALID if files cannot be parsed at the metadata level.

A qualified layout permits a separately frozen P0-Q analysis protocol before any response-field scoring.
