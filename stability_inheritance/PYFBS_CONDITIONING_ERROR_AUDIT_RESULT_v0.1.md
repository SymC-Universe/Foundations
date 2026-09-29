# pyFBS Native Hierarchical Conditioning / Error Audit Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** PYFBS_CONDITIONING_ERROR_AUDIT_PROTOCOL_v0.1.md
**Workflow run:** 36516878144
**Evidence class:** P0-D POST-RESULT LIMIT MAP
**Parent disposition:** NATIVE_FRAMEWORK_EQUIVALENT
**Parent disposition changed:** NO
**Disposition:** CONDITIONING_ERROR_MAP_COMPLETE

## Correlation structure

Descriptive Spearman rank correlations on all 800 positive-frequency bins:

- log condition number vs log DEC/BASE error ratio: **0.2655**
- log condition number vs log DEC absolute normalized error: **0.4245**
- log condition number vs log DEC/SHUFFLED ratio: **-0.1575**
- log independent-target norm vs log DEC error: **0.2650**
- log independent-target norm vs log DEC/BASE ratio: **0.3313**

Higher interface condition number is therefore associated with larger native recovery error and, more weakly, with reduced benefit over the no-decoupling baseline. The relation is not strong enough to explain the complete failure structure.

## Conditioning quartiles

| Condition quartile | Median condition | Median DEC error | Median BASE error | Median DEC/BASE | Fraction DEC < BASE |
|---|---:|---:|---:|---:|---:|
| Q1 lowest | 45.60 | 0.5265 | 1.1176 | 0.4095 | 0.900 |
| Q2 | 165.57 | 0.6179 | 1.1959 | 0.4162 | 0.870 |
| Q3 | 781.31 | 0.9597 | 1.1237 | 0.7990 | 0.720 |
| Q4 highest | 2816.74 | 0.9470 | 1.5606 | 0.7331 | 0.720 |

The largest drop in recovery benefit appears between the lower two and upper two condition quartiles, but Q4 is not uniformly worse than Q3. No conditioning threshold is inferred.

## Success versus failure bins

Native decoupling improves over baseline at 642 / 800 bins.

For bins where DEC < BASE:
- median condition = 257.99
- p90 condition = 2899.62
- median DEC error = 0.61965
- median BASE error = 1.33777
- median DEC/BASE = 0.42534
- median target norm = 12.22

For bins where DEC >= BASE:
- median condition = 892.65
- p90 condition = 5386.04
- median DEC error = 1.19115
- median BASE error = 0.98842
- median DEC/BASE = 1.21451
- median target norm = 21.63

The non-improving bins therefore have both higher typical interface condition number and larger typical independent-target response magnitude.

## Mapping-specificity limit

Conditioning does not explain the weak shuffled-map diagnostic in a simple way.

Fraction DEC < SHUFFLED by condition quartile:
- Q1: 0.210
- Q2: 0.590
- Q3: 0.655
- Q4: 0.530

The correlation between condition number and DEC/SHUFFLED ratio is weak and negative (-0.158).

This reinforces the v0.4 conclusion that the deterministic reduced-coordinate shuffle is not a robust carrier-specificity test.

## Interpretation

The native hierarchical transformation is operational, but its recoverability is materially conditioned.

The strongest supported Limit Map statement is:

**INTERFACE_CONDITIONING_CONSTRAINS_NATIVE_HIERARCHICAL_RECOVERY_BUT_DOES_NOT_FULLY_DETERMINE_IT**

A second factor is associated with independent-target response magnitude, and additional frequency-local measurement/interface structure may contribute.

This result does not justify:
- a universal condition-number threshold;
- deleting high-condition frequencies from the parent score;
- rescoring the parent protocol on a selected band;
- carrier-specific inheritance;
- reinterpretation of the parent NATIVE_FRAMEWORK_EQUIVALENT result.

## Architecture consequence

The measured hierarchy now supplies both Function and Limit evidence:

Function:
- explicit component/assembly transformation can move an embedded response toward an independent component target.

Limit:
- the realized recoverability depends materially on transform/interface conditioning and other frequency-local structure.

This is consistent with Stability Architecture being a relation among admitted component structure, coupling/interface geometry, transformation quality, and realized response rather than a property carried intact by one object alone.
