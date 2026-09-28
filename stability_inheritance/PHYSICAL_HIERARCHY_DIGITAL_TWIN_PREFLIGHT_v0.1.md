# Stability Inheritance Physical Hierarchy Digital-Twin Preflight v0.1

**Status:** PASS FOR APPARATUS-FEASIBILITY / KNOWN-TRUTH ONLY  
**Date:** 2026-09-27  
**Script:** physical_hierarchy_digital_twin_v0_1.py  
**Scientific ceiling:** design feasibility only. No physical or empirical Stability Inheritance evidence.

## Candidate system

A three-degree-of-freedom torsional hierarchy was used as a known-truth digital twin. Coordinates 1 and 2 form the independently characterized two-mode parent. Coordinate 3 is the child/receiver. The same child coupling spring is attached either to parent coordinate 1 (interface A) or parent coordinate 2 (interface B).

Nominal inertias are 0.045, 0.060, and 0.055 kg m^2. Nominal ground torsional stiffnesses are 0.6, 1.5, and 0.9 N m/rad. Parent internal coupling is 0.12 N m/rad and child interface coupling is 0.18 N m/rad. Rayleigh damping is used only for the digital-twin design study.

The isolated parent has modal frequencies 0.627297 and 0.834087 Hz with modal damping ratios chi = 0.046483 and 0.048618. Its first mode is concentrated on parent coordinate 1 while the second is concentrated on coordinate 2. The child isolated frequency is intentionally near the first parent mode for a measurable known-truth coupling contrast.

## Nominal A/B result

The isolated parent is identical in both conditions. Only the coupling map changes.

Assembly A modal frequencies:
- 0.635785 Hz
- 0.760391 Hz
- 0.839942 Hz

Assembly B modal frequencies:
- 0.627743 Hz
- 0.691537 Hz
- 0.888990 Hz

For a 0.1 rad child release with all other coordinates initially at rest, the peak response of parent coordinate 1 is 4.1333 times larger under interface A than interface B. Parent coordinate 2 shows the complementary direction, with interface B producing a 1.6530 times larger peak than interface A.

In the nominal time-domain model the all-coordinate 0.005 rad settling criterion differs by approximately 1.05 s between A and B, while the child's first zero-crossing time is unchanged. Thus the design contains both interface-sensitive and interface-insensitive response features.

## Tolerance sweep

A deterministic 2,000-draw paired sweep applied independent uniform +/-5% perturbations to every inertia and stiffness while comparing A versus B within each same sampled apparatus.

Parent-coordinate-1 peak ratio A/B:
- minimum 3.0266
- 5th percentile 3.5385
- median 4.1539
- 95th percentile 4.8612
- maximum 5.3347

Parent-coordinate-2 peak ratio B/A:
- minimum 1.4245
- 5th percentile 1.5223
- median 1.6775
- 95th percentile 1.8492
- maximum 2.0164

Assembly mode-2 relative shift B versus A:
- 5th percentile -10.765%
- median -9.009%
- 95th percentile -7.535%

Assembly mode-3 relative shift B versus A:
- 5th percentile +5.306%
- median +5.795%
- 95th percentile +6.274%

Mode 1 is not selected as a primary design contrast because its A/B relative shift can change sign within the tolerance sweep.

## Interpretation

The candidate geometry has a robust, easily measurable interface-specific effect without changing the isolated parent. It is therefore suitable for testing whether scalar chi, modal/vector Chi, coupling, and directly measured Chi_arc remain distinguishable in a physical benchmark.

This does **not** establish a novel inheritance effect. The expected A/B difference is standard coupled-mode physics and should be predicted by component-mode/dynamic-substructuring methods. A successful experiment would first qualify the SI representation/refusal workflow against known native physics.

## Pre-freeze consequence

The eventual physical design should target the robust parent-coordinate-1 transfer contrast and mode-2/mode-3 assembly shifts rather than the weak first-mode shift. Actual equivalence/effect thresholds may not inherit these digital-twin values. They must be derived from real apparatus repeatability and measurement uncertainty before any physical qualification run.
