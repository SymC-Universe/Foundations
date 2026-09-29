# F-16 GVT SpecialOdd Cross-Excitation-Family Replication Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** stability_inheritance/F16_GVT_SPECIALODD_REPLICATION_PROTOCOL_v0.1.md
**Initial scoring workflow:** 36513450698
**Exact reproducibility rerun:** 36513670338
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**Disposition:** SPECIALODD_AMPLITUDE_SPECIFIC_REPLICATES
**Architecture evidence role:** ARCHITECTURE_SUPPORTING_NATIVE_REPLICATION
**Novelty role:** NATIVE_MODEL_COMPATIBLE_NO_SI_NOVELTY_CLAIM
**P1 eligibility:** NO

## Storage and source identity

Official 4TU archive SHA-256:
2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa

The SpecialOdd layout was qualified without signal scoring:

- each main level file contains 9 estimation realizations;
- each Validation file contains 1 held-out realization;
- each realization contains 49,152 samples = 3 x 16,384;
- period 1 is excluded;
- periods 2 and 3 are steady-state scoring periods.

Primary band:
6.5-8.2 Hz.

Primary estimation-defined support:
69 bins.

Secondary 1-15 Hz support:
574 bins.

## Primary held-out results

| Level | Force RMS N | Amplitude-specific error | Pooled error | Other-amplitude errors | Winner |
|---|---:|---:|---:|---|---|
| 1 | 12.2 | 0.8543157 | 0.9561853 | 0.9215247, 0.9617152 | SPECIFIC |
| 2 | 49.0 | 0.7737025 | 0.8366089 | 0.8153299, 0.8513355 | SPECIFIC |
| 3 | 97.1 | 0.9230795 | 0.9248640 | 1.0064004, 0.9626316 | SPECIFIC |

The amplitude-specific representation has the lowest frozen primary error at all three held-out amplitudes.

Frozen disposition:

**SPECIALODD_AMPLITUDE_SPECIFIC_REPLICATES**

The 97.1 N margin over the pooled representation is small:
0.9230795 versus 0.9248640.

Therefore the categorical 3/3 replication should not be read as three equally strong effects.

## Per-output primary results

At 12.2 N, amplitude-specific error was lower than pooled error for all three outputs:

- excitation: 0.89898 vs 0.96591
- wing: 0.83594 vs 0.95016
- payload: 0.85108 vs 0.95790

At 49.0 N:

- excitation: 0.74659 vs 0.81882
- wing: 0.77607 vs 0.83607
- payload: 0.77872 vs 0.84214

At 97.1 N:

- excitation: 0.91992 vs 0.92143
- wing: 0.92562 vs 0.92762
- payload: 0.92120 vs 0.92283

The global primary ordering is therefore not produced by one selected output.

## Secondary full-band behavior

Over 1-15 Hz, amplitude-specific representations also had lower error than pooled representations at all three amplitudes, although the high-amplitude difference was again very small:

- 12.2 N: 0.95368 vs 0.99191
- 49.0 N: 0.91499 vs 0.94408
- 97.1 N: 0.96214 vs 0.96218

## Interface-relative diagnostic

The prospectively declared interface-relative proxy was:

H_payload - H_wing.

Held-out errors:

| Level | Specific proxy error | Pooled proxy error | Better |
|---|---:|---:|---|
| 12.2 N | 1.01883 | 1.00216 | Pooled |
| 49.0 N | 1.03271 | 0.99583 | Pooled |
| 97.1 N | 0.94856 | 0.95542 | Specific |

This proxy therefore **does not replicate the global amplitude-specific ordering uniformly**.

That failure is retained as a Limit Map result. The simple difference between payload-side and wing-side acceleration FRFs is not a sufficient stand-alone carrier/architecture diagnostic for this declared task.

## Representation separation

Primary-band distances among amplitude-specific estimation representations were substantial:

- low to mid: 0.70836
- low to high: 0.86105
- mid to high: 0.48113

These distances are descriptive and are not physical thresholds.

## Interpretation

The SpecialOdd family provides an independent excitation design and independent held-out realization structure. Its result supports the FullMSine architectural finding at the level of the full three-output response representation: excitation-regime-specific organization generalizes better within each amplitude than a single pooled representation or a representation learned at another amplitude.

The correct evidence role is:

**ARCHITECTURE_SUPPORTING_NATIVE_REPLICATION**

This strengthens the case that realized response organization is regime-dependent in a measured high-order structure whose native benchmark science already identifies nonlinear clearance/friction behavior at an embedded payload interface.

However, the failure of the simple interface-relative proxy to reproduce the same ordering shows that the architectural relation cannot be reduced to that one difference coordinate.

## Function Map additions

- EXCITATION_REGIME_SPECIFIC_RESPONSE_REPLICATES_ACROSS_EXCITATION_DESIGN
- AMPLITUDE_SPECIFIC_MULTI_OUTPUT_ORGANIZATION_TRANSPORTS_TO_HELDOUT_REALIZATION
- ARCHITECTURE_SUPPORTING_NATIVE_REPLICATION

## Limit Map additions

- SIMPLE_INTERFACE_DIFFERENCE_PROXY_NOT_UNIFORMLY_DISCRIMINATING
- HIGH_AMPLITUDE_SPECIFIC_VS_POOLED_MARGIN_SMALL
- CATEGORICAL_REPLICATION_DOES_NOT_IMPLY_UNIFORM_EFFECT_SIZE

## Claim ceiling

No physical chi is admitted.

Native FRFs are not automatically renamed capital Chi.

Chi_arc is not uniquely established solely by this benchmark.

No new F-16 nonlinear mechanism is claimed.

No P1 inheritance claim is promoted.

The result contributes to the integrated Stability Architecture case as native measured evidence.
