# D02C Prospective Wind-Blade Test of CA-D007 v0.1

**Date:** 2026-09-23  
**Status:** PROSPECTIVE_EXTERNAL_PHYSICAL_NULL  
**Authority:** SymC General Operations Manual v0.8.3  
**Target:** CA-D007, ARCHITECTURE_REORGANIZATION_CAN_PRECEDE_SCALAR_TRANSFORMATION  
**Dataset DOI:** 10.5281/zenodo.18427836  
**Publication DOI:** 10.1088/1742-6596/2647/19/192008  
**Successful workflow:** 35866859136  
**Execution commit:** 0401811345c037bfee77d8471cbc295acbb12dd8  
**Artifact ID:** 10752811690  
**Full result SHA-256:** 9b1f52945acc5cc43ec8590e9950effba65ef37c8e89523f20354b17fd079ab9

## 1. Prospective status

D02C was selected and frozen before the decisive damping/organization trajectories were inspected.

The test prospectively fixed:

- the full-scale climate-chamber icing intervention;
- two baseline-selected low-order modal families, one X and one Z;
- local scalar chi = modal damping ratio zeta;
- independent organization coordinate from three-sensor complex CSD principal vectors;
- pre-spray scalar control envelopes;
- midnight and dry-run organization thresholds;
- completeness rules;
- ordering categories;
- explicit supportive and contrary outcomes.

D02C is therefore the first prospectively frozen external physical test of CA-D007 in this workstream.

## 2. Frozen outcome

Both directions returned the same result:

- X: NEITHER_CHANGES
- Z: NEITHER_CHANGES

No scalar transformation onset was detected.

No organization-change onset was detected.

The runner therefore set:

ca_d007_domain_specific_support = false.

## 3. Local scalar result

### X direction

Selected baseline modal family:
- median frequency = 1.6458337698424748 Hz.

Pre-spray scalar control envelope:
- lower = 0.007099991973988179;
- upper = 0.09953984230859775.

Across the twelve intervention windows:
- admitted chi range = 0.008212434123149393 to 0.030643139697059233;
- minimum intervention lower95 = 0.00793482863917304;
- maximum intervention upper95 = 0.03267692044376181.

Every intervention 95% interval remained inside the frozen pre-spray scalar envelope.

Therefore X scalar status remained UNCHANGED for all twelve intervention windows.

### Z direction

Selected baseline modal family:
- median frequency = 2.0312862854419125 Hz.

Pre-spray scalar control envelope:
- lower = 0.0026511747772442174;
- upper = 0.042032172369455556.

Across the twelve intervention windows:
- admitted chi range = 0.006998699485623103 to 0.012494402348652069;
- minimum intervention lower95 = 0.006570623682231827;
- maximum intervention upper95 = 0.012875738634778753.

Every intervention 95% interval remained inside the frozen pre-spray scalar envelope.

Therefore Z scalar status remained UNCHANGED for all twelve intervention windows.

## 4. Organization result

### X direction

Effective organization threshold:

T_org = 0.11472577814744833.

This threshold is the maximum of:
- midnight baseline threshold = 0.048075560944617624;
- dry-run thermal threshold = 0.11472577814744833.

Largest intervention full-window dissimilarity:

0.017003559353776843,

which is about 14.8% of the effective threshold.

Largest intervention block-level 2.5th percentile:

0.0017267933632615557,

which is about 1.5% of the effective threshold.

No X intervention window satisfied the frozen CHANGED criterion.

### Z direction

Effective organization threshold:

T_org = 0.00872249224709043.

This threshold is the maximum of:
- midnight baseline threshold = 0.0031699325481574503;
- dry-run thermal threshold = 0.00872249224709043.

Largest intervention full-window dissimilarity:

0.0021906392466501945,

about 25.1% of the effective threshold.

Largest intervention block-level 2.5th percentile:

7.885555092995155e-05,

about 0.9% of the effective threshold.

No Z intervention window satisfied the frozen CHANGED criterion.

## 5. CA-D007 decision

The frozen supportive outcomes required at least one direction to show:

- ORGANIZATION_PRECEDES_SCALAR, or
- ORGANIZATION_CHANGES_SCALAR_DOES_NOT,

with the thermal/dry-run firewall intact.

Neither direction did.

The frozen explicit adverse outcome was a clean:

SCALAR_PRECEDES_ORGANIZATION

under comparable data quality.

That also did not occur.

Therefore D02C is classified as:

PROSPECTIVE_NULL / NO_SUPPORT / NO_CLEAN_REVERSAL.

It does not confirm CA-D007.

It does not satisfy the predeclared clean contradiction condition either.

## 6. What the null means

The null is scientifically important because the experiment was designed to prevent a weak organization signal from being promoted merely because the organization metric happened to be more sensitive than the scalar.

The dry-run thermal control materially enlarged the organization threshold, and the full pre-spray history materially enlarged the scalar no-change envelope.

After those controls, neither observable crossed its own prospectively defined detection boundary.

This means D02C supplies no evidence that architecture reorganized before local scalar transformation in this wind-blade icing experiment.

The correct interpretation is not that the blade did nothing physically. Natural-frequency and icing effects belong to the native experiment and prior literature. The D02C question was narrower: whether the selected modal damping ratio and independently reconstructed spatial organization crossed their frozen thresholds in an ordered way.

They did not.

## 7. Native-toolkit verdict

All D02C quantities are standard:

- Operational Modal Analysis / LSCF modal damping;
- modal-frequency tracking;
- cross-spectral density matrices;
- principal spatial spectral vectors;
- complex modal assurance;
- environmental/temperature control.

No additional SymC variable is required.

Verdict:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE.

## 8. Effect on CA-D007

Before D02C:

CA-D007 had one physical post-result generating system, D02B, and unpaid prospective promotion debt.

After D02C:

- the first prospectively frozen external physical test provides no support;
- promotion debt remains unpaid;
- CA-D007 must not be described as prospectively replicated;
- the hypothesis remains open only as a bounded candidate because D02C returned neither a supportive ordering nor the predeclared clean opposite ordering.

The next test, if pursued, should improve power against a null by choosing a system in which the intervention is known independently to produce a measurable change in at least one of the two frozen observables, while still hiding the relative onset ordering before execution.

## 9. Reproducibility

Reviewer command:

python chi_architecture/reproduce.py d02c

The command automatically acquires and verifies the Zenodo sources, reconstructs the two baseline-selected modal tracks, computes the scalar and organization control envelopes, executes the twelve-window prospective intervention map, and emits a single compact result bundle.
