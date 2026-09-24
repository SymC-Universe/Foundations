# D02E Candidate Selection Record v0.1

**Date:** 2026-09-23  
**Status:** SELECTED_BEFORE_DECISIVE_VIBRATION_OUTCOME_INSPECTION  
**Authority:** SymC GOM v0.8.6  
**Parent freeze:** D02E_CANDIDATE_SELECTION_FREEZE_v0.1.md

## Search result

The completeness-ranked external search identified the offshore jacket bolt-loosening corpus as the strongest provisional candidate.

Independent metadata/API verification then established:

- dataset DOI: 10.34810/data1011;
- article DOI: 10.1016/j.dib.2024.110222;
- Dataverse version: 3.0;
- 780 original CSV vibration experiments;
- three fixed white-noise excitation amplitudes: A_05, A_1, A_2;
- four bolt states: Healthy = 12 Nm, 9 Nm, 6 Nm, NoBolt;
- four physical damage locations for non-healthy states;
- 20 original CSV replicates per condition;
- eight triaxial accelerometers, 24 response channels;
- public nonrestricted individual Dataverse file IDs;
- successful metadata-only GitHub Actions API access.

No vibration-response CSV values were opened during candidate selection.

## Selected confirmatory slice

Primary D02E uses fixed excitation amplitude:

A_1

and all four physical bolt locations.

For each location, the graded sequence is:

12 Nm healthy -> 9 Nm -> 6 Nm -> NoBolt.

All 20 original CSV replicates are retained at every state.

The healthy A_1 reference is shared across the four location strata because the source contains one intact structure rather than a location-specific healthy structure.

Total original CSV files in the frozen primary source slice:

- healthy: 20;
- 9 Nm: 4 locations x 20 = 80;
- 6 Nm: 4 x 20 = 80;
- NoBolt: 4 x 20 = 80;
- total = 260 original CSV files.

Dataverse-generated .tab derivatives are not used.

## Why A_1 is frozen

A_1 is the middle of the three source-defined shaker amplitudes.

It is selected before response inspection as a fixed operational condition that avoids choosing either the lowest excitation, where signal-to-noise may be weakest, or the highest excitation, where amplitude-dependent nonlinearities may be strongest.

A_05 and A_2 remain untouched sensitivity strata and are not used to rescue the primary result.

## Why the candidate fixes prior prospective failures

D02C power issue:
the source documentation establishes that graded bolt loosening changes the structure's vibration behavior over the tested range, without supplying the D02E scalar-versus-organization onset ordering.

D02D completeness issue:
each required A_1 graded state has 20 same-protocol laboratory replicates. No temperature/log-RMS overlap filter is needed before the primary ordering test.

## Candidate alternatives

The search also surfaced a flexible-wing benchmark, Orion joint data, TRC/CEA jointed structures, and other SHM datasets.

They ranked below the selected system because the jacket corpus has the strongest verified combination of:

- complete graded states;
- fixed matched operation;
- high replicate count;
- spatial sensing;
- direct public individual-file automation;
- native modal-analysis comparator.

## Evidence ceiling

D02E is a prospective domain-specific test of CA-D007.

Candidate selection was based on methods, metadata, file counts, repository access, and the existence of measurable intervention effects. Relative damping-versus-mode-shape onset was not inspected.
