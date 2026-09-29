# Brake-Reuss Beam Scalar-Modal Relation P0-D Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** stability_inheritance/BRB_SCALAR_MODAL_RELATION_PROTOCOL_v0.1.md
**Workflow run:** 36523393398
**Evidence class:** PUBLIC EXTERNAL MEASURED / POST-RESULT P0-D
**Promotion debt:** YES
**Disposition:** CHI_TRACKS_BUT_IS_REDUNDANT_WITH_AMPLITUDE
**Empirical Stability Inheritance claim:** NONE

## Purpose

Test whether a locally licensed scalar damping coordinate chi tracks or adds nonredundant information about the already-measured amplitude-conditioned modal/vector geometry Chi during the Brake-Reuss Beam slow-mode ringdown.

This analysis was frozen after the positive BRB modal-geometry result was known. It is therefore P0-D and cannot be promoted as prospective confirmation.

## Frozen windowing and scalar admission

The 3.18 s DIC ringdown was divided into:
- 0.25 s windows;
- 0.125 s step;
- 24 complete windows.

All 24 windows satisfied the frozen local scalar-admission rules.

Per window:
- 40 or 41 absolute response peaks were available;
- local exponential envelope fits were strongly linear;
- median envelope R2 = 0.999267;
- minimum envelope R2 = 0.993419;
- the damped angular frequency estimate was effectively constant at 506.7085 rad/s in the recorded windows;
- local chi_ring was defined as sigma / sqrt(sigma^2 + omega_d^2).

Observed chi range:
- minimum = 0.00146876
- maximum = 0.00405466

This is a **LOCAL_EFFECTIVE_CONDITIONAL chi**, not a universal scalar coordinate for the entire beam.

## Modal/vector window qualification

Every window remained strongly rank 1:

- median rank-1 energy fraction = 0.99999356
- minimum rank-1 energy fraction = 0.99994863

The final chronological valid window was frozen as the low-amplitude modal reference.

Principal angle to that final basis ranged from:
- 0.000 degrees
to:
- 1.29180 degrees.

Thus the windowed result reproduces the parent modal finding continuously through the decay: the modal skeleton is preserved while its fine geometry evolves with response level.

## Scalar-modal association

Across all 24 valid windows:

- Spearman rho(chi, modal angle) = 0.98696
  - p = 6.03e-19
- Spearman rho(log amplitude, modal angle) = 0.99826
  - p = 1.50e-28
- Spearman rho(chi, log amplitude) = 0.98609
  - p = 1.22e-18

Therefore local chi strongly tracks the same evolving ringdown regime that carries the modal deformation.

However, chi is also strongly tied to response amplitude, so correlation alone does not establish a nonredundant scalar-modal relation.

## Frozen chronological prediction comparison

Valid windows:
- TRAIN = first 16
- TEST = final 8

Test RMSE for modal angle in degrees:

| Model | Predictor | Test RMSE |
|---|---|---:|
| M0 | constant only | 0.53483 |
| M_amp | log response amplitude | 0.10191 |
| M_chi | local chi | 0.33458 |
| M_both | log amplitude + chi | 0.10377 |

The frozen outcome rule therefore yields:

**CHI_TRACKS_BUT_IS_REDUNDANT_WITH_AMPLITUDE**

because:
- M_chi improves over the constant baseline;
- M_both does not improve over M_amp.

The slight M_both degradation relative to M_amp is descriptive only. No independent equivalence margin exists.

## Stability Architecture interpretation

This result gives a useful relation among three objects:

1. response amplitude describes the operating state of the ringdown;
2. local chi tracks the amplitude-dependent dissipation regime;
3. Chi geometry also changes with that regime.

The scalar and modal layers therefore co-vary strongly, but the scalar does not provide additional held-out information about modal geometry once response amplitude is already known.

The correct interpretation is not that chi is useless. It is that:

**SCALAR_TRACKING_IS_NOT_SCALAR_SUFFICIENCY**

For this declared task, local chi is a compact coordinate of the evolving dissipative regime, while Chi retains the spatial organization itself.

This is consistent with the program-wide rule that scalar and modal representations can be complementary rather than nested replacements.

## Project notation

### chi

**LOCAL_EFFECTIVE_CHI_ADMITTED_CONDITIONALLY**

The short-window second-order decay approximation is exceptionally good by the recorded envelope-fit diagnostics, so the scalar is licensed locally for this task.

The scalar is not promoted into:
- a universal BRB coordinate;
- a universal joint-state coordinate;
- Chi;
- Chi_arc.

### Chi

**ADMITTED_NATIVE_MODAL_SUBSPACE_FOR_DECLARED_TASK**

The already-qualified one-dimensional DIC spatial subspace remains the modal/vector object.

### Chi_arc

**NOT IDENTIFIED**

Neither strong chi-Chi correlation nor their common amplitude dependence constructs a unique architecture-level object.

## Function / Limit map

Function:
- LOCAL_CHI_TRACKS_MODAL_GEOMETRY_DURING_RINGDOWN
- SCALAR_AND_MODAL_LAYERS_COVARY_WITH_OPERATING_STATE
- LOCAL_SECOND_ORDER_SCALAR_IS_OPERATIONALLY_ADMISSIBLE_IN_SHORT_WINDOWS

Limit:
- CHI_ADDS_NO_HELD_OUT_MODAL_INFORMATION_BEYOND_AMPLITUDE_IN_DECLARED_TASK
- SCALAR_TRACKING_DOES_NOT_IMPLY_SCALAR_SUFFICIENCY
- CHI_TO_CHI_MAPPING_IS_NOT_UNIVERSALIZED_FROM_ONE_RINGDOWN

## Scientific ceiling

This is post-result evidence with promotion debt.

It does not establish:
- a universal chi-to-Chi map;
- scalar causation of modal geometry;
- Stability Inheritance novelty;
- a new damping mechanism;
- Chi_arc.

A fresh independent jointed-system test would be required to promote the scalar-modal relation beyond exploratory architecture mapping.
