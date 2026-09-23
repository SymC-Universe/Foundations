# D02B Orion Beam Source Contract v0.2

**Date:** 2026-09-22  
**Status:** SELECTED_AND_FROZEN_BEFORE_D02B_NUMERIC_EXTRACTION  
**Authority:** SymC GOM v0.8.3  
**Selection correction:** D02B_CANDIDATE_SELECTION_CORRECTION_v0.2.md

## Selected physical system

Orion beam: two duraluminum beams assembled by a three-bolt lap joint with localized contact patches.

Dataset DOI: 10.17632/p4fg6snh3r.1

Data article DOI: 10.1016/j.dib.2021.107627

Native-method article DOI: 10.1016/j.ymssp.2021.108172

## Frozen physical interpretation target

The bolted lap joint is the D02B stability-inheritance substrate candidate.

The lower-level beam dynamics are embedded into a joined structure whose interface condition is deliberately changed by bolt tightening torque and whose response is probed at multiple excitation amplitudes.

D02B asks whether local/modal damping-frequency coordinates remain sufficient after the interface state changes, or whether interface-mediated organization is required to explain the realized response.

## Frozen scalar construction

For any resonance that is adequately represented by a passive second-order local/modal factor,

chi = gamma/(2 omega_n) = zeta

where zeta is the conventional modal damping ratio.

If the data are represented by resonance frequency f_n and quality factor Q,

chi = 1/(2Q).

If a lightly damped half-power bandwidth Delta_f is licensed by the native FRF conditions,

Q = f_n/Delta_f
and
chi = Delta_f/(2 f_n).

No alternate scalar normalization may be introduced after outcome inspection.

## Scalar admission requirements

A scalar chi may be emitted for a torque/excitation/mode condition only when:

1. a distinct resonance can be identified under the native data;
2. the same-condition bandwidth/decay estimate is identifiable;
3. the half-power or fitted second-order interpretation is adequate for that condition;
4. no unresolved modal overlap or severe nonlinearity invalidates the local scalar approximation.

Otherwise return NO_ADMISSIBLE_SCALAR_CHI or NON_IDENTIFIABLE.

## Controlled variables

Primary controlled organization variable:

- bolt tightening torque.

Secondary stress-test variable:

- excitation amplitude / RMS force or base acceleration.

The torque contrast is primary because it changes the joint/interface state independently of the response metric.

## Frozen mode targets

Use the modes explicitly emphasized by the dataset/data article:

- 3rd bending mode in Dataset #1 where available;
- 6th bending mode in Dataset #1 and/or Dataset #2.

If both support complete same-condition frequency+damping extraction, both must be retained.

No mode may be dropped because its result is inconvenient.

## Frozen response hierarchy

Primary response:

1. same-condition modal damping ratio / linewidth and resonance-frequency shift across torque at a fixed low excitation level sufficient to approximate the linear/native modal regime.

Independent embedded-response stress test:

2. FRF/transmissibility response change across torque at higher excitation levels, quantified using predeclared native observables:
   - resonance-frequency shift;
   - peak response magnitude;
   - linewidth/damping where identifiable;
   - response-shape distortion or refusal when one-mode scalar fitting becomes inadequate.

Because damping is part of chi, D02B must not use the same damping estimate as both predictor and independent outcome in the same test.

Therefore the central inheritance comparison is:

- local/modal chi at the low-excitation reference condition;
- interface state / torque;
- higher-excitation FRF realization as the independent consequence.

## Carrier / substrate descriptor

Primary substrate descriptor:

- bolt tightening torque with the known lap-joint/contact-patch architecture.

Secondary native organization descriptors may include:

- specimen identity;
- bolt role/location if explicitly encoded;
- excitation channel;
- mode identity.

No post-hoc learned latent variable is allowed in v0.2.

## Native comparator

The strongest native comparator is standard jointed-structure vibration analysis using FRFs/transmissibility, modal frequency/damping, torque dependence, excitation-amplitude dependence, and the companion paper's Duffing-Van der Pol / nonlinear joint interpretation where applicable.

If this native toolkit fully explains the result, report:

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE

even if the descriptive inheritance classification remains meaningful.

## Frozen primary tests

### T1: scalar preservation under interface change
At the lowest common excitation level, estimate admissible chi for each selected mode across torque.

Classify whether chi is preserved, transformed, non-identifiable, or refused.

### T2: fixed/local scalar versus embedded response
Within matched mode/specimen conditions, test whether similar low-excitation chi values can accompany materially different higher-excitation FRF responses when torque differs.

### T3: substrate information
Test whether torque/interface state distinguishes higher-excitation response variation not captured by low-excitation chi alone.

### T4: native-toolkit comparison
Compare any inheritance framing against the standard FRF/modal/nonlinear interpretation.

No new SymC-specific variable is admitted unless a later separately frozen experiment establishes incremental value.

## Predeclared outcome states

- PRESERVED
- TRANSFORMED
- REORGANIZED
- LOCAL_SCALAR_VALID_BUT_EMBEDDED_INSUFFICIENT
- NO_ADMISSIBLE_SCALAR_CHI
- NON_IDENTIFIABLE
- NO_RELATION_DETECTED
- CONTRADICTS_INHERITANCE_HYPOTHESIS

Added-value verdict:

- NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE
- or INCREMENTAL_VALUE_UNRESOLVED

D02B v0.2 does not pre-authorize a positive incremental-value claim.

## Failure conditions

The working inheritance interpretation is weakened if:

- torque does not reproducibly alter the relevant response beyond measurement variability;
- low-excitation chi alone predicts the higher-excitation response as well as interface-aware models;
- the apparent relation is explained entirely by a shared-input algebraic construction;
- mode matching is unstable or requires post-hoc relabeling;
- damping extraction is not valid under the selected conditions;
- conclusions depend on selectively excluding torque, amplitude, specimen, or mode conditions.

## Reproducibility rule

The eventual supported reviewer command remains:

python chi_architecture/reproduce.py d02b

The command must download or access the public Mendeley dataset automatically, validate source hashes/metadata, execute the frozen extraction, and generate one compact result bundle.

Reviewers must not manually pick MAT/ASCII files or run the supplied Matlab scripts themselves.
