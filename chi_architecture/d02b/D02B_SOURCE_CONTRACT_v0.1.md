# D02B Selected Physical System and Source Contract v0.1

**Date:** 2026-09-22  
**Status:** SELECTED_AND_FROZEN_BEFORE_MACHINE_READABLE_OUTCOME_EXTRACTION  
**Authority:** SymC GOM v0.8.3  
**Parent selection freeze:** D02B_CANDIDATE_SELECTION_FREEZE_v0.1.md

## Selected system

Zhang et al., "Coherent energy transfer in coupled nonlinear microelectromechanical resonators," Nature Communications 16, 3864 (2025).

Article DOI: 10.1038/s41467-025-59292-2

Source-data DOI: 10.6084/m9.figshare.28714484

Code archive DOI: 10.5281/zenodo.15162385

## Why this system won the frozen ranking

The selection is based on source completeness rather than result direction.

1. Machine-readable source data are publicly deposited.
2. Natural-frequency/eigenfrequency and Q/damping quantities are directly reported.
3. Structural asymmetry is independently controlled by a tuning voltage applied to Resonator 2.
4. Carrier/mode organization is independently defined by the two-resonator mechanical model and measured mode localization / amplitude structure.
5. Time-resolved ring-down, frequency tracking, phase difference, and energy-transfer observables are recorded.
6. A native coupled Duffing/resonator model is available as a strong comparator.
7. Public simulation code is archived.

The runner-up was de Jong et al., "Beating Ringdowns of Near-Degenerate Mechanical Resonances" (Physical Review Applied, 2022), which has excellent direct frequency/damping values and fully public data/scripts but a weaker independently controlled change in coupling/organization for the present question.

## Known-context contamination note

During source-eligibility verification, the article abstract/main text and PDF necessarily exposed qualitative statements that transient beating, energy transfer, localization, and nonlinear modulation occur.

Therefore D02B is not pristine untouched P1 confirmation.

The machine-readable extraction, scalar construction, comparison metrics, and decision rules below are frozen before inspecting the source-data workbook numerically. D02B remains P0-Q / physical qualification evidence unless a future untouched system pays the promotion debt.

## Licensed lowercase chi construction

The linear native equations use a damping coefficient omega0/Q in front of x_dot.

For the passive second-order local oscillator,

chi_local = (omega0/Q) / (2 omega0) = 1/(2Q).

Where the paper reports the amplitude-decay rate gamma0 in Hz through

x(t) = X exp(-2 pi gamma0 t)

and

Q = omega0/(4 pi gamma0),

the equivalent licensed scalar is

chi_local = gamma0 / f0 = 1/(2Q).

No alternate scaling may be introduced after outcome inspection.

The scalar is admitted only for linear/small-amplitude conditions where the paper's Q/damping convention is licensed. Nonlinear apparent damping is not silently substituted into the same scalar.

## Frozen primary question

When the local linear damping coordinate is fixed or nearly fixed, does independently controlled structural asymmetry reorganize carrier localization and the realized ring-down energy-transfer response?

## Frozen source fields

The extraction may use only directly supplied article/source-data quantities corresponding to:

- tuning voltage or the paper's native asymmetry variable;
- directly measured/tracked resonance or eigenfrequency;
- Q, gamma0, or directly equivalent damping quantity under a stated convention;
- mode amplitudes / amplitude ratios;
- time-resolved ring-down amplitude;
- tracked ring-down frequency;
- phase difference;
- source-data energy or power-flow quantities where directly supplied;
- native coupling rate / frequency split and native model parameters supplied by the authors.

Derived quantities may be computed only from these fields with equations declared in this contract or the native paper.

## Frozen primary outputs

1. **Scalar map**
   - chi_local under each condition where direct frequency+damping admission is possible;
   - uncertainty propagated from supplied frequency/damping uncertainty where available;
   - refusal for conditions lacking licensed same-condition inputs.

2. **Carrier/organization map**
   - native amplitude ratio / localization descriptor as a function of the controlled tuning/asymmetry condition;
   - mode identity retained according to the paper's native branch definitions.

3. **Independent response map**
   - ring-down energy-transfer metric using a source-native quantity.
   - Preferred hierarchy, chosen before workbook inspection:
     a. directly supplied transfer-rate or transferred-energy quantity;
     b. directly supplied first-transfer / beating timescale;
     c. directly supplied transient amplitude-ratio trajectory.
   - The first available quantity in this hierarchy becomes the primary response; lower entries become secondary checks.

4. **Native comparator**
   - the paper's coupled resonator / Duffing model and standard modal/localization interpretation.

## Frozen comparisons

A. **Scalar-only adequacy**
Does chi_local alone distinguish controlled conditions that have materially different independent ring-down responses?

B. **Carrier added information**
Does the native carrier/localization variable distinguish response changes that chi_local does not?

C. **Native-toolkit sufficiency**
Does the established coupled-resonator model explain the same response without an additional SymC-specific variable?

D. **Inheritance classification**
Classify the local-to-embedded relation as one or more of:
- PRESERVED
- TRANSFORMED
- REORGANIZED
- LOCAL_SCALAR_VALID_BUT_EMBEDDED_INSUFFICIENT
- NO_ADMISSIBLE_SCALAR_CHI
- NON_IDENTIFIABLE
- NO_RELATION_DETECTED
- CONTRADICTS_INHERITANCE_HYPOTHESIS

NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE is reported separately as the added-value verdict and may coexist with a descriptive inheritance classification.

## Failure conditions

D02B counts against the working inheritance interpretation if any of the following occurs:

- the controlled organization change does not produce a reproducible change in the independently defined response beyond uncertainty;
- apparent carrier-response association vanishes under the native model or uncertainty treatment;
- the local scalar alone is sufficient for the declared response and richer organization adds no information;
- carrier identity cannot be defined without post-hoc relabeling;
- the source data do not support same-condition scalar admission;
- extraction requires reverse fitting to the desired conclusion.

## Anti-circularity

- No chi=1 target.
- No Atlas target.
- No outcome-fitted weights.
- No post-result switching of primary response hierarchy.
- No nonlinear damping quantity may be relabeled as linear chi without a new contract.
- Native-model success is not SymC added-value evidence.
- Qualitative outcome statements already seen during eligibility screening are recorded as known context and cannot count as prospective discovery.

## Reproduction target

Reviewer entrypoint:

python chi_architecture/reproduce.py d02b

The source workbook should be downloaded automatically from its stable publisher/source-data location or DOI-derived metadata when possible. Reviewers must not manually assemble figure files.
