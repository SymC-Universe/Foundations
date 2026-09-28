# Physical Hierarchy A5/B5 Known-Truth Method Qualification v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Status:** P0-Q KNOWN-TRUTH METHOD QUALIFICATION ONLY  
**Script:** stability_inheritance/physical_hierarchy_methods_known_truth_v0_1.py  
**Seed:** 20260928  
**Physical evidence:** none  
**Q1/Q2 target exposure:** none

## Purpose

Qualify two method paths before hardware execution:

- A5: representation-specific reciprocity/passivity detection;
- B5: refusal of unstable one-to-one mode labels with subspace fallback for near-degenerate modes.

This is code/method qualification only. It does not support an empirical Stability Inheritance claim.

## A5 known-truth controls

A two-DOF passive parent with symmetric positive damping was evaluated over 1500 frequency points from 0.05 to 2.0 Hz using receptance H=x/F and mobility Y=v/F=i*omega*H.

### Exact passive control

- maximum relative reciprocity residual: 1.9206824514056212e-16
- minimum eigenvalue of the mobility dissipative/Hermitian part: 0.0011284218904200915
- frequencies with negative dissipative eigenvalue under the synthetic numerical tolerance: 0 / 1500

**Disposition:** PASS. The detector accepts the known passive reciprocal model.

### Known-bad negative-damping control

One damping entry was forced negative.

- maximum relative reciprocity residual: 1.409577372445296e-16
- minimum mobility dissipative eigenvalue: -62.980665636013214
- frequencies with negative dissipative eigenvalue: 1500 / 1500

**Disposition:** PASS AS NEGATIVE CONTROL. The detector rejects the deliberately non-passive model while reciprocity remains intact, demonstrating that reciprocity and passivity are distinct gates.

### Passive model plus asymmetric measurement-like FRF noise

Noise levels are synthetic method probes, not physical thresholds.

| Relative noise level | Max reciprocity residual | Min dissipative eigenvalue | Negative-frequency count |
|---:|---:|---:|---:|
| 1e-4 | 0.0003800187 | 0.0010996919 | 0 |
| 1e-3 | 0.0044254107 | 0.0006325025 | 0 |
| 1e-2 | 0.0420653501 | -0.0105353308 | 41 |
| 5e-2 | 0.1964672426 | -2.5096194533 | 479 |

**Interpretation:** an actually passive system can appear to violate passivity after sufficiently large measurement-like corruption. Therefore the physical A5 gate may not use a zero-tolerance sign test. It must be evaluated against the pre-target measurement/identification uncertainty budget. This also supports preserving raw measured FRFs, identified models, and any conditioned models as separate objects.

No synthetic noise level is promoted into a physical acceptance threshold.

## B5 known-truth controls

A three-DOF system was used with two closely spaced low modes separated from a third mode. Small symmetric stiffness perturbations were applied for 400 deterministic draws.

### Near-degenerate case

Base frequencies:

- 0.1591549431 Hz
- 0.1591708578 Hz
- 0.3183098862 Hz

Results across 400 perturbations:

- individual identity swap fraction: 0.34
- median diagonal individual-mode MAC: 0.7570944750
- 5th percentile diagonal MAC: 0.0286215769
- median off-diagonal MAC: 0.2429055250
- median maximum two-mode subspace angle: 0.0002411422 degrees
- 95th percentile maximum subspace angle: 0.0005066209 degrees

The individual eigenvectors can rotate/swap severely while the two-dimensional subspace remains essentially unchanged.

### Well-separated control

Base low modes are approximately 0.15915 and 0.19492 Hz.

Across 400 perturbations:

- individual identity swap fraction: 0.0
- median diagonal individual-mode MAC: 0.9999999062
- 5th percentile diagonal MAC: 0.9999992417
- median off-diagonal MAC: 9.38e-8
- median maximum subspace angle: 0.0002733003 degrees
- 95th percentile maximum subspace angle: 0.0005594407 degrees

**Interpretation:** the code path distinguishes the intended regimes. Near-degenerate individual-mode identity becomes unstable without implying loss of the containing subspace, whereas the well-separated control preserves one-to-one identity.

## Method consequences

1. **B5 synthetic method logic passes.** MODAL_NONIDENTIFIABLE for unstable labels with stable subspace is operationally testable.
2. No fixed delta_crowd frequency threshold is justified by this result. The physical trigger must come from repeatability/uncertainty and pairing stability.
3. **A5 synthetic detection logic passes** for exact passive and known-bad non-passive controls.
4. Synthetic noisy controls show that a physical passivity decision requires uncertainty, not an exact sign test.
5. These results qualify code paths only. A4/A5/B2/B4/B5 remain open for apparatus-specific physical evidence and second APQ adjudication.

## Next exact action

Proceed to parent-only physical qualification:

- single-station shaft/bearing buildability;
- repeated isolated-parent modal identification;
- sensor/DAQ timing, noise, linearity, record-duration and anti-alias qualification;
- raw mobility/FRF reciprocity and uncertainty-aware passivity evaluation;
- pairing stability and same-condition subspace-angle distribution;
- repeatability-derived candidate equivalence regions.

Do not couple the child or inspect decisive Q1/Q2 assembly outcomes before these steps and the second APQ freeze gate.
