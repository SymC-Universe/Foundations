# Stability Inheritance Randomized Computational Qualification Protocol v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Branch:** stability-inheritance  
**Status:** P0-Q COMPUTATIONAL QUALIFICATION PROTOCOL - FROZEN BEFORE RANDOMIZED RUN  
**Scientific ceiling:** method/representation qualification only; no empirical Stability Inheritance claim  
**Physical target exposure:** none

## Purpose

Stress-test the current chi / Chi / Chi_arc representation and refusal logic across randomized known-truth systems without changing the claim ceiling. This protocol is frozen before the randomized ensemble is generated.

The ensemble tests framework behavior, not nature. A passing result means only that the representation/refusal workflow behaves coherently on the predeclared synthetic families.

## Seed and reproducibility

- master seed: 2026092802
- all ensemble generators deterministic from the master seed
- script and complete result tables must be committed
- no failed draw may be silently dropped except for a predeclared mathematical invalidity such as a non-positive-definite matrix; invalid draws must be counted

## RQ-1 Same-spectrum / different modal geometry

Generate 500 two-mode parent pairs with identical positive eigenvalues and proportional damping scalars but randomized orthogonal modal rotations. Couple an identical child at a fixed physical coordinate.

Record:
- exact scalar-spectrum difference, which should remain numerical zero;
- change in assembled response under the fixed coupling;
- modal-basis participation difference.

Expected outcome:
- scalar spectrum remains invariant by construction;
- assembled response differences vary from negligible to large depending on rotation/coupling geometry;
- no minimum effect is required for a pass.

Qualification criterion:
The ensemble must demonstrate both near-null and non-null response differences while preserving scalar-spectrum identity. If all responses are identical despite modal rotation, the implementation is suspect. If scalar spectra change, the generator is invalid.

## RQ-2 Non-proportional damping / scalar-mode reconstruction

Generate 500 stable two- or three-DOF second-order systems with positive-definite M and K and positive-definite damping C. Vary the degree to which C is non-diagonal in the undamped modal basis.

Compare exact state-space response with the response reconstructed after discarding off-diagonal modal damping.

Record:
- off-diagonal modal damping fraction;
- relative response reconstruction error;
- invalid/non-positive-definite draws.

Expected outcome:
Reconstruction error should generally increase with off-diagonal damping content, but no universal monotonic law or refusal threshold is assumed.

Qualification criterion:
Positive association between off-diagonal damping content and reconstruction error across the ensemble, with valid low-error and high-error examples retained.

## RQ-3 Fixed spectrum / non-normal transient geometry

Generate 500 stable first-order matrices with the same frozen eigenvalues {-1,-2} and randomized non-normal coupling strength/direction.

Record:
- eigenvalues;
- eigenvector conditioning;
- maximum transient gain over the frozen time window.

Expected outcome:
Eigenvalues remain unchanged while transient gain varies materially with non-normal geometry.

Qualification criterion:
The ensemble contains both no-amplification/low-amplification cases and substantial transient-amplification cases at the same spectrum.

This is a spectral-summary insufficiency test. Second-order chi is NOT licensed for these first-order systems.

## RQ-4 Hidden-state memory identifiability under observation noise

Generate 300 damped-oscillator cases spanning damping, frequency, initial condition, and observation-noise levels. Observe displacement only.

Compare:
- memoryless AR(1);
- AR(2) history closure fitted by ordinary least squares.

Use a chronological train/test split fixed in the script.

Record:
- test SNR;
- AR(1) and AR(2) test RMSE;
- which model performs better.

Expected outcome:
AR(2) should dominate in high-SNR cases because the displacement-only projection is non-Markovian; at low SNR, predictor noise may erase or reverse the practical advantage.

Qualification criterion:
Both regimes must be visible. A result claiming universal AR(2) superiority is a failure of this protocol's expected Limit Map.

Follow-up classification:
When memory exists mathematically but cannot be estimated reliably from noisy observed lags, classify HISTORY_PRESENT_BUT_NOT_OPERATIONALLY_IDENTIFIABLE for the tested estimator/measurement regime, not NO_MEMORY.

## RQ-5 Direct Chi_arc reference independence

Generate 300 known-truth assemblies. Hold each direct assembly reference fixed while perturbing only the parent/coupling predictor used to reconstruct it.

Record:
- predictor perturbation magnitude;
- prediction error against the unchanged direct reference.

Expected outcome:
Zero predictor corruption yields numerical-zero error; increasing corruption generally increases prediction error.

Qualification criterion:
Strong positive association between predictor corruption magnitude and comparison error, while the direct reference remains unchanged.

## Outcome discipline

Valid outcomes include:
- METHOD_SCOPE_TEST_PASSED;
- METHOD_SCOPE_TEST_FAILED;
- INDETERMINATE;
- INVALID_TEST.

Framework-specific diagnostic labels may be recorded only within the case scope:
- SCALAR_INFORMATION_LOSS;
- MODAL_NONIDENTIFIABLE_SUBSPACE_STABLE;
- HISTORY_PRESENT_BUT_NOT_OPERATIONALLY_IDENTIFIABLE;
- NATIVE_FRAMEWORK_EQUIVALENT;
- FRAMEWORK_NO_ADDED_VALUE;
- FRAMEWORK_NOT_OPERATIONAL.

No result from this ensemble:
- freezes a physical threshold;
- licenses a P1 claim;
- counts as empirical SI confirmation;
- converts known native theory into SI novelty.

## Stop conditions

Stop and audit before interpretation if:
- any generator violates its mathematical construction;
- invalid draws are silently excluded;
- results require retuning the frozen task/metric;
- one family fails and the failure cannot be reproduced from the stored seed.

