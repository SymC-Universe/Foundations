# D02E Final Preexecution Implementation Freeze v0.1

**Date:** 2026-09-24  
**Status:** FROZEN_BEFORE_DAMAGED_A_1_VIBRATION_VALUES  
**Authority:** SymC GOM v0.8.6  
**Parent:** D02E_JACKET_MFR14_v0.1.md  
**Healthy selection archive:** results/D02E_HEALTHY_SELECTION_ARCHIVE_v0.1.json

## Frozen primary mode

Healthy-only selection fixed the primary family at:

8.7890625 Hz

with:
- 20/20 identifiable healthy replicates;
- 17/20 admitted healthy half-power chi estimates;
- healthy median chi = 0.028856666306254334.

No damaged vibration record contributed to this selection.

## Source slice

Use original text/csv files only.

Healthy:
DATA/A_1/Healthy

Damage states, all four locations:
DATA/A_1/9Nm/level_1 ... level_4
DATA/A_1/6Nm/level_1 ... level_4
DATA/A_1/NoBolt/level_1 ... level_4

Use all 20 original CSV replicates in every directory.

Dataverse-generated tabular derivatives are excluded.

## Fixed modal tracking window

The primary family tracking window is fixed to +/-5% of the healthy-selected median frequency:

lower = 0.95 * 8.7890625 Hz
upper = 1.05 * 8.7890625 Hz.

No damaged state may shift or widen this window.

Within each replicate:

1. compute the first FDD singular-value spectrum over the 24 frozen response channels;
2. find local peaks inside the fixed window;
3. if no peak exists, status = NON_IDENTIFIABLE;
4. choose the peak nearest 8.7890625 Hz;
5. if another local peak inside the window has amplitude >=90% of the chosen peak, status = NON_IDENTIFIABLE_MODAL_OVERLAP;
6. otherwise retain that peak as the tracked family for both scalar and organization calculations.

No sequential damaged-state retargeting is allowed.

## Scalar extraction

At the selected FDD peak:

- half-power threshold = one-half of first-singular-value power;
- interpolate the left and right threshold crossings linearly in frequency;
- chi = bandwidth / (2 f_peak).

ADMITTED only when:
- both crossings occur inside the fixed tracking window;
- bandwidth is finite and positive;
- the selected peak is not at the window boundary;
- the modal-overlap guard above passes.

Otherwise scalar is refused.

State-level scalar adjudication requires >=16/20 ADMITTED replicates.

For each adjudicable state:
- median chi over admitted replicates;
- 10,000 bootstrap resamples of replicate median;
- seed = 20260923;
- 95% percentile interval.

Healthy reference is recomputed from the same 20 DOI-locked healthy files and must reproduce:
- primary frequency = 8.7890625 Hz;
- >=16 admitted scalar replicates.

SCALAR_TRANSFORMED iff the damaged-state 95% bootstrap interval lies fully outside the healthy 95% bootstrap interval.

Otherwise SCALAR_UNCHANGED.

## Organization extraction

For every replicate with an identifiable tracked family, use the unit-norm complex first FDD left singular vector at that replicate's tracked peak.

Healthy reference:
- retain every healthy replicate with an identifiable primary-family vector;
- require >=16/20;
- form P_i = v_i v_i^H;
- v_ref is the principal eigenvector of mean(P_i).

Healthy leave-one-out threshold:
- for each valid healthy replicate i, build v_ref,-i from the other valid healthy vectors;
- D_i = 1 - |v_ref,-i^H v_i|^2;
- T_org = 97.5th percentile of valid healthy D_i values.

For a damaged replicate:

D_org = 1 - |v_ref^H v_damage|^2.

State-level organization adjudication requires >=16/20 identifiable organization vectors.

ORGANIZATION_CHANGED iff the 2.5th percentile of the damaged state's replicate D_org values is strictly greater than T_org.

Otherwise ORGANIZATION_UNCHANGED.

No alternate channel subset or shape metric may replace complex FDD-vector dissimilarity.

## Onset completeness

For each physical bolt location separately, inspect states in severity order:

9 Nm -> 6 Nm -> NoBolt.

An onset for an observable is identifiable only if:
- that state is adjudicable; and
- every earlier damaged state is adjudicable and explicitly UNCHANGED for that observable.

If an earlier state is non-identifiable, a later changed state cannot rescue the onset.

A DOES_NOT_CHANGE conclusion requires all three damaged states to be adjudicable and unchanged.

If these requirements fail, the location ordering is ORDERING_NON_IDENTIFIABLE.

## Frozen location ordering

Use the MFR-14 categories exactly:

- ORGANIZATION_PRECEDES_SCALAR
- SCALAR_PRECEDES_ORGANIZATION
- SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION
- ORGANIZATION_CHANGES_SCALAR_DOES_NOT
- SCALAR_CHANGES_ORGANIZATION_DOES_NOT
- NEITHER_CHANGES
- ORDERING_NON_IDENTIFIABLE

## Frozen domain adjudication

SUPPORT only if:
- >=3/4 locations are ORGANIZATION_PRECEDES_SCALAR or ORGANIZATION_CHANGES_SCALAR_DOES_NOT; and
- zero locations are SCALAR_PRECEDES_ORGANIZATION.

ADVERSE only if:
- >=3/4 locations are SCALAR_PRECEDES_ORGANIZATION or SCALAR_CHANGES_ORGANIZATION_DOES_NOT; and
- zero locations are ORGANIZATION_PRECEDES_SCALAR.

All other complete mixtures are NO_SUPPORT_OR_INDETERMINATE.

Any completeness failure is retained and may make the domain result INDETERMINATE.

## Computational implementation

For efficiency only, FDD may be computed with a vectorized Welch/CSD implementation rather than repeated pairwise scipy.signal.csd calls provided regression tests demonstrate numerical agreement on the selected window to floating-point tolerance.

This is a mechanical optimization. It does not alter:
- Hann window;
- sampling frequency 1600 Hz;
- nperseg 8192;
- 50% overlap;
- constant detrend;
- density scaling;
- frequency grid;
- singular-value definition;
- frozen tracking/admission rules.

## Native-toolkit verdict ceiling

D02E may report standard FDD/OMA ordering only.

No new SymC scalar or carrier metric is authorized.

If the frozen native toolkit expresses the result completely, verdict:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE.
