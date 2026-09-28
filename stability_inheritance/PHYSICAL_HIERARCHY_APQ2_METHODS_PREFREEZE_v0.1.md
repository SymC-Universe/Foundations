# Physical Hierarchy APQ-2 Methods Pre-Freeze Note v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Branch:** stability-inheritance  
**Status:** METHODS EVIDENCE / PLAN INPUT / NOT FROZEN  
**Ceiling:** P0-Q known-truth physical qualification only  
**Target exposure:** No decisive Q1/Q2 assembled outcome may be opened from this note.

## Purpose

This note converts the remaining apparatus-level APQ concerns A4, A5, B2, B4, and B5 into operational pre-freeze requirements using experimental structural-dynamics literature. It does not close any APQ objection. Closure still requires apparatus-specific pilot evidence and a second APQ adjudication.

The note preserves the active project notation:

- lowercase chi = licensed scalar coordinate;
- capital Chi = base modal/vector representation;
- Chi_arc = architecture-level/conglomerate representation reconstructed through Stability Arc machinery where scientifically licensed.

## Evidence basis

1. Scheel, Gibanica, and Nord (2019), *State-Space Dynamic Substructuring with the Transmission Simulator Method*, Experimental Techniques. https://doi.org/10.1007/s40799-019-00317-z  
   Relevance: experimental state-space identification can violate passivity and Newton consistency; reciprocity, passivity, full-rank interface mappings, and directly measured assembly validation matter.

2. Contartese, Nijman, and Desmet (2022), *A procedure to restore measurement induced violations of reciprocity and passivity for FRF-based substructuring*, Mechanical Systems and Signal Processing 167, 108556. https://doi.org/10.1016/j.ymssp.2021.108556  
   Relevance: small measurement-induced reciprocity/passivity violations can substantially alter assembled predictions; physical-consistency conditioning must be explicit rather than silently absorbed.

3. Brake, Schwingshackl, and Reuss (2019), *Observations of variability and repeatability in jointed structures*, Mechanical Systems and Signal Processing 129, 282-307. https://doi.org/10.1016/j.ymssp.2019.04.020  
   Relevance: jointed structures can have substantial variability and repeatability limitations; interface settling, geometry, and experimental setup can dominate the effect being studied.

4. Wall, Allen, and Kuether (2022), *Observations of modal coupling due to bolted joints in an experimental benchmark structure*, Mechanical Systems and Signal Processing 162, 107968. https://doi.org/10.1016/j.ymssp.2021.107968  
   Relevance: bolted interfaces can introduce amplitude-dependent frequency/damping and nonlinear modal coupling; this is a confound for a nominally linear known-truth substructuring benchmark.

5. Ng et al. (2023), *Uncertainty laws of experimental modal analysis with known broadband input*, Mechanical Systems and Signal Processing 204, 110624. https://doi.org/10.1016/j.ymssp.2023.110624  
   Relevance: modal-frequency, damping, and mode-shape uncertainty depend on signal-to-noise ratio, measured DOFs, excitation placement, and data duration; no universal coherence/sample-rate threshold substitutes for a measurement-specific uncertainty budget.

6. Brincker and Lopez-Aenlle (2015), *Mode shape sensitivity of two closely spaced eigenvalues*, Journal of Sound and Vibration 334, 377-387. https://doi.org/10.1016/j.jsv.2014.08.015  
   Relevance: close/repeated modes make individual eigenvectors unstable while the spanned subspace remains the meaningful object.

7. Ocepek et al. (2024), *On the experimental coupling with continuous interfaces using frequency based substructuring*, Mechanical Systems and Signal Processing 217, 111517. https://doi.org/10.1016/j.ymssp.2024.111517  
   Relevance: interface descriptions can become redundant/ill-conditioned and experimental errors can be amplified; interface reduction and conditioning are part of the native comparator problem.

8. Wagner et al. (2026), *Enhancing hybrid dynamic substructuring: A comprehensive review of numerical and experimental techniques*, Mechanical Systems and Signal Processing 253, 114308. https://doi.org/10.1016/j.ymssp.2026.114308  
   Relevance: current review confirms interface modeling, mode selection, assembly choice, and model-reduction design as central determinants of hybrid substructuring quality.

## A4 - Interface repeatability and parent-boundary confounding

### Operational requirement

The baseline parent is defined in the exact adapter state used during Q1. Unused ports carry the same inertial adapter/blank state prospectively specified for all parent characterizations.

For Q1, use the **same active child-coupling cartridge** at interface A and interface B wherever mechanically feasible. The unused parent port carries an independently characterized equal-purpose inertial blank. This is preferred to using two nominally matched active cartridges because cartridge-to-cartridge variation would become an avoidable carrier confound.

Before target exposure, characterize:

- isolated-parent modal frequencies and damping where licensed;
- modal/subspace geometry at the measurement coordinates;
- interface-adapter mass and geometry;
- active cartridge stiffness/geometry/preload descriptor;
- unchanged-condition repeatability across assembly/disassembly cycles;
- evidence for settling or wear.

A conditioning/settling phase may be defined from pilot evidence, but it is excluded permanently from decisive evidence. The final conditioning schedule must be fixed before Q1/Q2 targets.

### Drift rule

Do not freeze an arbitrary percent-drift threshold.

For each tracked quantity q, estimate the unchanged-condition repeatability distribution and instrument contribution before target exposure. The later A/B contrast is invalid if parent change across the A/B sequence exceeds the frozen repeatability/equivalence region.

Outcome on failure: **INVALID_TEST**, not inheritance support or falsification.

## A5 - Measurement and model physical consistency

### Separate three objects

1. **Raw measured dynamics**: direct time histories / FRFs.
2. **Identified model**: modal or state-space representation fit to those measurements.
3. **Conditioned model**, if used: a prospectively specified reciprocity/passivity/physical-consistency repair.

These three may not be silently collapsed.

### Reciprocity

Where the mechanical configuration and coordinates license Maxwell-Betti reciprocity, evaluate reciprocal transfer pairs against the distribution of reciprocal mismatch observed in unchanged-condition repeats. A universal 1 dB / fixed-phase cutoff is not frozen.

### Passivity

The passivity test must name the FRF representation.

For mobility
[
Y(j\omega)=v(j\omega)/F(j\omega),
]
a passive linear reciprocal drive point has nonnegative real part within measurement uncertainty. For a multiport mobility matrix, use the Hermitian/dissipative part as the natural matrix-level object where supported.

Do **not** apply a generic phase bound directly to receptance or accelerance without the appropriate transformation. If receptance or accelerance is measured, convert or apply a representation-specific consistency test before passivity adjudication.

### State-space physical consistency

Identified models must be checked for:

- stability;
- reciprocity where licensed;
- passivity/nonnegative dissipation;
- Newton/second-order consistency appropriate to the chosen input/output form;
- interface input/output rank and conditioning;
- model-order sensitivity;
- residual/high-frequency treatment.

If the raw measurement object is physically consistent but the identified model is not, classify this first as **MODEL_PATH_NOT_QUALIFIED**, not FRAMEWORK_NOT_OPERATIONAL.

If a prospective conditioning step is used, preserve both unconditioned and conditioned results. If conditioning changes the scientific outcome class or the SI/native comparator ordering materially, the affected result is **INDETERMINATE** until the model path is independently qualified.

### Coherence and sampling

Coherence is a diagnostic, not a universal fixed pass threshold. Sampling rate, record length, excitation placement, and averaging must be justified by the target bandwidth and by the measured uncertainty of modal quantities. Frequency resolution follows record duration and must be small enough that discretization is not the dominant contributor to the pre-target uncertainty budget.

No physical pass/fail number is inherited from the digital twin.

## B5 - Close modes and modal nonidentifiability

### One-to-one mode labels are conditional

Individual mode matching is admitted only when the pairing is stable across unchanged-condition repeats and the identification uncertainty supports a unique correspondence.

When close modes rotate/mix under perturbations or repeated fits, treat the **subspace** as the primary object.

### Subspace comparison

If a physically justified mass metric M is available over matched coordinates, construct M-orthonormal subspace bases Q1 and Q2 and obtain principal angles from the singular values of

[
Q_1^T M Q_2.
]

If only a common sensor-coordinate space is available, orthonormalize each retained basis in that common measurement metric and obtain principal angles from the singular values of

[
Q_1^T Q_2.
]

Do not insert an unmeasured mass matrix only to preserve a preferred formula.

### Crowding/nonidentifiability trigger

Do not freeze an arbitrary relative-frequency crowding threshold.

Declare one-to-one identity **MODAL_NONIDENTIFIABLE** when unchanged-repeat evidence shows unstable mode assignment, overlapping/indistinguishable modal estimates, or repeated basis rotation while the containing subspace remains reproducible. The subspace tolerance is derived from unchanged-condition repeatability before Q1/Q2 target exposure.

If even the subspace is unstable beyond the frozen repeatability region, the sector is not qualified for the intended modal comparison.

## B4 - Physical specificity control

Label scrambling remains code validation only.

The physical Q1 control is:

- same parent;
- same child;
- same active coupling cartridge moved A <-> B;
- same sensor set and excitation family;
- inertially characterized inactive-port blank;
- parent remeasurement before/after each interface condition.

If the parent or interface identity changes beyond the frozen repeatability region, Q1 is **INVALID_TEST**.

A cartridge identity cross-check may be added in the pilot only if a second cartridge exists, but it cannot replace the same-cartridge A/B control.

## B2 - Framework-level failure triggers for this benchmark

The following verdicts are **task/domain scoped**, not program-wide verdicts.

**FRAMEWORK_NOT_OPERATIONAL** for this benchmark if, after valid measurement qualification:

- chi / Chi / Chi_arc assignments are not reproducible under native-equivalent parameterizations;
- the direct Chi_arc target cannot be constructed without parent-predictor or outcome leakage;
- the result class changes materially under arbitrary modal basis rotations inside a natively equivalent subspace;
- a required layer can only be made identifiable through post-result normalization or target-dependent tuning.

**FRAMEWORK_NO_ADDED_VALUE** for this benchmark if, across the predeclared valid cases and failure cases, the SI layer/refusal distinctions produce no nonredundant prediction, boundary, identifiability decision, or scientific refusal beyond the strongest native CMS/substructuring workflow.

**NATIVE_FRAMEWORK_EQUIVALENT** remains a valid successful qualification outcome.

## Apparatus consequence

The three-station torsional hierarchy remains a defensible apparatus candidate because its lumped, low-frequency design can make parent modes, coupling location, and direct assembly response observable. However, the benchmark should minimize friction-joint behavior in the dynamic load path. A spring/pin or similarly repeatable coupling cartridge is preferable to making a bolted friction interface itself the scientific carrier.

Existing bearings, springs, fasteners, and aluminum stock may support the parent-only preflight. Threaded rod should not be presumed adequate as a precision rotating shaft; runout, straightness, bearing fit, and friction must be checked before apparatus identity is frozen. Speaker magnets remain outside the first cycle because damping manipulation is deferred.

## APQ status after this note

- A4: **METHOD SPECIFIED / PHYSICAL PILOT REQUIRED**
- A5: **METHOD SPECIFIED / PHYSICAL PILOT REQUIRED**
- B2: **TRIGGERS SPECIFIED / SECOND APQ REQUIRED**
- B4: **CONTROL SPECIFIED / PHYSICAL PILOT REQUIRED**
- B5: **METRIC LOGIC SPECIFIED / PHYSICAL PILOT REQUIRED**

No objection is closed by this note.

## Next exact action

Complete the **parent-only apparatus qualification packet** without the child coupled:

1. verify shaft/bearing/baseplate buildability and low-friction repeatability;
2. identify at least two parent modes with repeated measurements;
3. quantify unchanged-condition frequency/damping/subspace uncertainty;
4. qualify sensor timing, noise, linearity, clipping, and record duration;
5. implement representation-specific reciprocity/passivity/model-consistency checks on parent-only data;
6. only after those results exist, derive candidate repeatability margins and run the second APQ pass.

Decisive Q1/Q2 assembled outcomes remain unopened.
