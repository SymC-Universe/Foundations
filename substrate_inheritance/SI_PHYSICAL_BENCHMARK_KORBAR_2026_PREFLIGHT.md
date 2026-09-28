# SI Physical Benchmark Preflight: Korbar A–J–B Dynamic Substructuring Dataset

**Date:** 2026-09-27  
**Status:** P0-D / P0-Q candidate physical route, NOT FROZEN FOR P1  
**Active GOM:** v0.8.8  
**Dataset:** Jure Korbar (2026), *Dynamic joint identification of a resilient insert: substructure frequency response functions*, Mendeley Data v1, DOI 10.17632/2wdk4m5n97.1, CC BY 4.0.

## Why this route is being considered

The first Chemistry routes were re-audited before reuse.

- H/Ru(0001): clean Ru parent is qualified, but the shared-H reference ended in a scientific HOLD and adsorption never became an admitted child system.
- CO/Cu(111): clean-surface depth convergence remains unresolved in the audited branch, so a fully admitted parent/adsorbate child pair is not presently available.

Neither route will be bent around SI.

The Korbar dataset provides an independent physical benchmark in which:
- substructure A is measured separately;
- substructure B is measured separately;
- the assembled system AJB is measured separately;
- component and assembly frequency-response functions are supplied;
- interface DOF locations and orientations are supplied;
- virtual-point interface metadata are supplied;
- a numerical companion contains five joint stiffness variants.

This is unusually well matched to a prospective parent/component → assembled-system test.

## Existing SI contract boundary

Frozen `REAL_SYSTEM_INPUT_SCHEMA_v0.2.json` currently supports a mechanical-harmonic stiffness/Hessian channel. The Korbar dataset is an FRF/admittance dataset.

Therefore:

- v0.2 is **not changed**;
- this route begins as a separate P0-Q **response-channel candidate**;
- it cannot inherit v0.2 promotion authority by analogy;
- any future physical claim requires its own frozen response-channel contract and MFR-14 record.

## Development / decisive-evidence split

### Development source

`numerical.h5` contains:
- component FRFs `Y_A`, `Y_B`;
- five assembly FRF families `Y_AJB_i` for joint Young's moduli 0.2, 0.4, 0.6, 0.8, and 1.0 GPa;
- response/excitation geometry;
- virtual-point metadata.

Candidate use:
- map Function/Limit behavior as coupling/joint stiffness changes;
- develop carrier/subspace lineage handling;
- expose splitting, merging, weak participation, and nonidentifiability;
- establish strongest native dynamic-substructuring comparator implementation;
- freeze no physical threshold from the later experimental target.

### Candidate physical decisive source

`experimental.h5` contains:
- experimental component FRFs `Y_A`, `Y_B`;
- experimental assembly FRF `Y_AJB`;
- response/excitation DOF geometry;
- virtual-point metadata.

Prospective opening sequence if this route is promoted:

1. hash and register the entire file without inspecting datasets numerically;
2. open only frequency, component A/B, channel/impact geometry, and virtual-point metadata;
3. independently characterize parent/component carriers and uncertainty;
4. freeze interface correspondence and assembly prediction/lineage rules;
5. freeze native comparator implementation and refusal logic;
6. only then open `Y_AJB`;
7. adjudicate the frozen physical test once.

The existence and names of HDF5 groups are public metadata and are not treated as target outcomes.

## Candidate residual scientific question

Not:

> Can dynamic substructuring predict an assembly response?

That is established prior art.

Instead:

> Given independently measured component dynamics and a prospectively fixed interface correspondence, can SI identify which component carrier/subspace structures survive, transform, split, merge, or become nonidentifiable in the assembled physical system, and does that carrier-lineage information add measurable value beyond standard dynamic substructuring / VPT / mode-tracking outputs for the same task?

## Native comparator burden

At minimum:
- direct experimental dynamic substructuring;
- Virtual Point Transformation where appropriate;
- standard modal/subspace tracking;
- frequency-only matching as a deliberately weak comparator;
- full component and assembly FRF error;
- uncertainty on extracted modes/carriers.

A response match alone is not SI added value.

## Candidate Function / Limit questions

Using only the numerical five-joint landscape:

1. Which parent/component poles and subspaces remain identifiable as joint stiffness changes?
2. Where do individual-mode correspondences fail while subspace correspondence survives?
3. Where do two parent carriers merge into an assembly carrier?
4. Where does an assembly carrier become emergent rather than traceable to one parent?
5. Does interface participation predict lineage confidence?
6. Does a response-accurate native assembly model imply carrier-lineage identifiability, or can the two disagree?
7. What refusal states are needed for weakly participating or non-identifiable carriers?

## Candidate refusal states

P0-Q only, not frozen:
- `RESPONSE_CHANNEL_NOT_ADMITTED`
- `PARENT_CARRIER_NONIDENTIFIABLE`
- `INTERFACE_MAP_INCOMPLETE`
- `SUBSPACE_ONLY`
- `SPLIT`
- `MERGED`
- `EMERGENT_ASSEMBLY_CARRIER`
- `WEAK_PARTICIPATION`
- `NATIVE_COMPARATOR_EQUIVALENT`
- `INSUFFICIENT_UNCERTAINTY_RESOLUTION`

## Independence / leakage controls

- Do not inspect physical `Y_AJB` values before a P1 freeze if this route is selected.
- Public descriptions of dataset organization may be used.
- Numerical `Y_AJB_i` variants are development evidence and permanently excluded from later physical independence claims.
- Literature describing standard dynamic-substructuring performance is prior art, not target evidence.
- If a publication explicitly reports the exact experimental carrier-lineage result we would test, source-independence must be downgraded and the route may become development-only.

## Current disposition

`PHYSICAL_ROUTE_CANDIDATE = STRONG`

`P1_FREEZE = NOT_CREATED`

`EXPERIMENTAL_ASSEMBLY_OUTCOME_OPENED_BY_SI = NO`

`NEXT = VERIFY_MACHINE_ACCESS_AND_FILE_HASHES_WITHOUT_OPENING_ASSEMBLY_VALUES`
