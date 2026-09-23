# D02D Candidate Selection Record v0.1

**Date:** 2026-09-23  
**Status:** SELECTED_BEFORE_DECISIVE_DAMAGE-STATE TRAJECTORY INSPECTION  
**Authority:** SymC General Operations Manual v0.8.4  
**Target:** second prospective test of CA-D007

## Selected system

LUMO, Leibniz University Test Structure for Monitoring.

Dataset DOI: 10.25835/0027803  
Methods paper DOI: 10.1002/stc.3077

The system is an outdoor lattice tower with reversible damage mechanisms at multiple heights and continuous multichannel vibration measurements.

## Why LUMO is selected

The selection is based on the frozen D02D ranking, not on the relative onset outcome.

1. The public benchmark contains healthy and reversible damaged states.
2. Three retained damage locations have two physical damage extents in addition to healthy reference:
   - 010: one damage mechanism removed;
   - 111: all damage mechanisms removed.
3. The source literature establishes modal identification of natural frequency, damping ratio, and mode shapes using operational modal analysis.
4. The decisive organization observable can be reconstructed independently from multichannel cross-spectral spatial geometry rather than defined as an algebraic transform of damping.
5. The source literature documents that structural/environmental changes measurably alter modal properties, satisfying the D02D activity requirement without requiring inspection of scalar-versus-organization onset ordering.
6. The dataset is public through a CKAN repository with stable resource identifiers and direct downloadable ZIP resources.
7. Three damage locations, DAM3, DAM4, and DAM6, are available at both 010 and 111 extents, enabling replication strata without selecting a favorable location after execution.

## Candidate audit

### LUMO lattice tower
Disposition: SELECTED.

Strengths:
- physically reversible structural damage;
- three ordered levels per retained location: healthy, 010, 111;
- multichannel vibration field;
- established OMA damping and mode-shape science;
- public DOI and CKAN API;
- three location strata.

Primary limitation:
- outdoor environmental and operational variability.

Disposition:
handled prospectively as a competing explanation and matching/control requirement.

### Offshore jacket bolt-loosening dataset
Disposition: ELIGIBLE_BUT_NOT_SELECTED.

Strengths:
- healthy, 9 Nm, 6 Nm, bolt-absent levels;
- 20 repeated measurements per structural state;
- 24 vibration channels;
- controlled laboratory setting.

Reason not selected:
the substrate and perturbation family are too close to D02B's bolted-interface experiment to provide the strongest independence test available.

### Composite-plate added-mass dataset
Disposition: NOT_SELECTED.

Strengths:
- public FRFs;
- seven sensors;
- repeated impact measurements;
- several damage-identification scenarios.

Limitation:
the six scenarios are not verified as one simple ordered three-level intervention ladder suitable for a prospectively frozen onset ordering without additional post-selection choices.

### Mass-reinforced beam dataset
Disposition: INELIGIBLE_AXIS_3.

Strengths:
- healthy plus three ordered mass-loss levels;
- 70 repeated measurements per condition;
- public raw FRFs.

Failure:
the primary measured response is a single driven-point FRF. No sufficiently independent spatial/carrier organization observable was verified for the D02D claim.

## Independence note

The dedicated literature deep search remained in progress when this selection was frozen. Selection therefore rests on the explicit frozen criteria plus independently verified public methods/repository evidence. If the later search reveals that LUMO fails a frozen eligibility axis, the test must be invalidated before decisive execution rather than silently switching outcomes.

No LUMO damage-state damping-versus-organization onset ordering was inspected before this record.
