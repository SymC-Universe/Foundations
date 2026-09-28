# Stability Inheritance Computational Stress Atlas v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Status:** P0-Q FUNCTION/LIMIT STRESS MAPPING ONLY  
**Script SHA256:** 8e0076695703e3ee147e169dc8a74db92bd288d52ad75b0b9f8c93adbe0eb45c  
**Result JSON SHA256:** 44dc253d37eb9fc11668e994ad7c891f8f1a1a0b83aee6c3c73779a9264a6ac9

## Purpose

Test whether the deterministic qualification cases survive parameter variation without retuning their scientific interpretation.

## Results

### ST-001 - same-spectrum rotated-basis family

57 combinations of modal rotation and child coupling were evaluated while preserving identical parent scalar spectra.

- response ratio > 1.05 in 85.96% of cases;
- response ratio > 1.20 in 75.44%;
- median response ratio = 1.7192;
- maximum = 4.8625.

Near-null cases are retained. They show that different modal geometry need not create a large effect for every interface/coupling choice.

### ST-002 - non-proportional damping family

33 positive-damping cases were swept.

- correlation between modal damping off-diagonal fraction and independent-mode reconstruction error = 0.99884;
- reconstruction-error median = 0.07312;
- maximum = 0.14878.

No universal off-diagonal fraction is promoted as a scalar-refusal threshold.

### ST-003 - non-normal transient family

61 systems retained eigenvalues {-1,-2} while non-normal coupling varied.

- transient gain > 1 in 86.89%;
- gain > 2 in 73.77%;
- maximum gain = 7.5042.

This is a Limit Map demonstration that stable spectral location alone does not determine transient response.

### ST-004 - hidden-state memory under observation noise

36 cases varied damping, frequency, and observation noise.

- AR(2) history closure better than AR(1) in 66.67% overall;
- noiseless: 9/9 AR(2) better;
- noise 1e-4: 8/9 better;
- noise 1e-3: 5/9 better;
- noise 1e-2: 2/9 better.

This failure structure is preserved rather than averaged away.

### ST-005 - Duffing regime map

36 nonlinearity/amplitude combinations were mapped.

- 55.56% remained within 5% of the low-amplitude dominant frequency;
- 44.44% shifted by more than 20%;
- maximum relative shift = 2.5.

This maps a representation validity boundary, not a universal transition.

### ST-006 - direct-reference predictor corruption

33 predictor-corruption levels were compared against an unchanged direct assembly reference.

- correlation between absolute predictor corruption and prediction error = 0.98749;
- zero corruption error = 0;
- maximum relative RMS error = 0.5110.

The target remains independent of predictor quality.

## Interpretation

The stress atlas strengthens the Function Map and Limit Map simultaneously. It does not support a monotonic story that richer representations always win. In particular, the memory family contains a real operational failure branch under noise and the rotated-basis family contains legitimate near-null effects.

No stress result is a physical acceptance threshold or empirical SI confirmation.
