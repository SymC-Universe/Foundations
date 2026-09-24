# D02C Candidate Selection Record v0.2

**Date:** 2026-09-23  
**Status:** SELECTED_BEFORE_DECISIVE_NUMERIC_OUTCOME_INSPECTION  
**Authority:** SymC GOM v0.8.3  
**Parent:** D02C_CANDIDATE_SELECTION_FREEZE_v0.1.md

## Search audit

The dedicated external deep search failed before returning a ranked result. Candidate selection therefore proceeded under the already-frozen ranking using public-source and repository-schema verification.

No failed search result was substituted or inferred.

## Candidates screened under the frozen rules

### Hyun et al. 2026 YIG/CoFeB magnonic crystal

Strengths:
- graded field/geometry;
- independent hybridization/carrier structure;
- open Zenodo archive;
- strong native micromagnetic/spin-wave comparator.

Failure:
- no sufficiently direct same-condition damping/Q/linewidth coordinate was verified from the archived experimental data without inventing a new scalar route.

Disposition:
INELIGIBLE_D02C_AXIS_2.

### SSDV piezoelectric structural-control dataset

Strengths:
- dense phase-shift and voltage perturbation grid;
- raw experimental FRFs;
- open Zenodo archive and Matlab analysis scripts.

Failure:
- no independently measured organization/carrier observable distinct from resonance frequency/amplitude was verified.

Disposition:
INELIGIBLE_D02C_AXIS_3.

### Quartz optomechanical strong-coupling dataset

Strengths:
- independent detuning and pump-power control;
- linewidth and normal-mode splitting;
- direct Figshare API access with 47 machine-readable files;
- strong coupled-mode comparator.

Limitation:
- in the native linearized coupled-mode model, branch linewidth and hybrid-mode participation are structurally coupled through the same eigenproblem. This makes an apparent ordering especially vulnerable to unequal fit sensitivity or native algebraic dependence.

Additional provenance:
- a method-schema probe exposed the published pump-power/coupling-rate series before D02C selection. Pump power is therefore not pristine for a prospective ordering test.

Disposition:
ELIGIBLE_BUT_NOT_SELECTED / LOWER_INDEPENDENCE_RANK.

### Progressive-crack cantilever-beam paper

Strengths:
- 54 progressive crack configurations;
- reported natural frequencies, damping ratios, and mode shapes.

Failure:
- Zenodo record contains only the PDF, not the machine-readable 54-configuration measurement data.

Disposition:
INELIGIBLE_D02C_AXIS_7.

### Full-scale wind-turbine blade climate-chamber icing experiment

Dataset DOI:
10.5281/zenodo.18427836

Methods/publication DOI:
10.1088/1742-6596/2647/19/192008

Verified source structure:
- 12 baseline raw ten-minute acceleration windows from 00:00 through 01:50 UTC;
- 12 intervention raw ten-minute windows from 11:20 through 13:10 UTC;
- intervention schedule independently published:
  - spray start 11:23 UTC;
  - accelerated spray 12:13 UTC;
  - spray end 12:49 UTC;
- full-day X and Z automated-OMA tables with:
  - mean_frequency;
  - std_frequency;
  - mean_damping;
  - std_damping;
  - cluster size;
  - algorithm;
  - timestamp;
- chamber-temperature time series;
- independent earlier dry-run climate/acceleration record;
- three spatial accelerometers at distinct blade positions.

This supports:
- direct local/modal scalar from source OMA damping ratio;
- independent spatial organization from three-sensor cross-spectral mode vectors;
- separate scalar and organization uncertainty routes;
- a time-ordered physical intervention;
- native OMA / environmental-operational-variability comparator;
- direct Zenodo automation.

## Selection

D02C selects the full-scale wind-turbine blade climate-chamber experiment.

Selection is based on completeness and independence of observables, not on the direction of the decisive damping/organization response.

## Known-context firewall

Before selection, public methods text exposed:
- the event schedule;
- baseline mode-frequency examples;
- that natural frequency is temperature-sensitive in the experiment;
- the general published premise that icing can shift blade frequencies.

D02C therefore does not use natural-frequency onset as the decisive local scalar outcome.

The decisive local scalar is modal damping ratio, and the decisive organization observable is the independently reconstructed spatial modal vector/MAC. Their intervention-time ordering has not been inspected before this selection record.

The temperature dependence of frequency is treated as native context/confounding information, not D02C evidence.
