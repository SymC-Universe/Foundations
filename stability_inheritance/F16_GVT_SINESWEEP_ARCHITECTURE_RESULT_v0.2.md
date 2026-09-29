# F-16 GVT Sine-Sweep Architecture Result v0.2

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** F16_GVT_SINESWEEP_ARCHITECTURE_PROTOCOL_v0.2.md
**Input-coordinate qualification:** F16_GVT_SINESWEEP_INPUT_COORDINATE_RESULT_v0.1.md
**Workflow run:** 36515853668
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-D POST-RESULT
**Promotion debt:** YES
**Disposition:** SINESWEEP_P0D_AMPLITUDE_CONDITIONED_SUPPORT
**Architecture evidence role:** ARCHITECTURE_SUPPORTING_NATIVE_EXPLORATORY
**Confirmatory consequence:** NONE

## Primary result

Using the input-only qualified C2 quadratic-phase chirp coordinate, the amplitude-conditioned response representation outperformed the fixed Level-1 representation at all three held-out sine-sweep levels in the fixed 6.5-8.2 Hz band.

| Held-out level | Force N | Conditioned error | Fixed error | Ratio |
|---|---:|---:|---:|---:|
| 2 | 19.2 | 0.4667478 | 0.9204978 | 0.5070602 |
| 4 | 57.6 | 0.1851541 | 1.5147123 | 0.1222371 |
| 6 | 86.0 | 0.0588262 | 1.8300811 | 0.0321440 |

The same ordering held over the 2.5-14.5 Hz secondary grid.

## Output-specific result

Conditioning improved all three outputs separately at every held-out level. The result is not produced by one selected channel.

The interface-relative proxy H_payload - H_wing also favored the conditioned representation at all three held-out levels:

- Level 2: 0.40959 vs 0.88684
- Level 4: 0.17790 vs 1.06826
- Level 6: 0.07407 vs 1.02341

This differs from the SpecialOdd family, where the same simple interface-relative proxy did not uniformly reproduce the full-response ordering.

## Frequency organization

Primary-band peak frequencies shifted with excitation. For wing-side and payload-side outputs the dominant primary-band location moved from approximately 7.20 Hz at low excitation toward approximately 6.95 Hz at higher levels.

This is descriptive and not a new transition threshold.

## Interpretation

The sine-sweep family is consistent with the broader measured F-16 architecture picture: one fixed low-amplitude response object is a poor representation across excitation regimes, while amplitude-conditioned response organization tracks held-out behavior much more closely.

Because the v0.1 sine-sweep scoring path had already loaded the records before its coordinate gate failed, this v0.2 result cannot be promoted as prospective replication. It remains useful architecture-supporting native evidence with promotion debt.

Together with FullMSine and SpecialOdd, the F-16 evidence now suggests that response organization is conditioned by operating regime, but the mixed FullMSine-to-SpecialOdd transport and the SpecialOdd interface-proxy failure show that scalar excitation amplitude alone does not define a universal architecture map.

## Function / Limit updates

Function:
- AMPLITUDE_CONDITIONED_RESPONSE_REAPPEARS_IN_SINESWEEP_EXPLORATORY
- INTERFACE_RELATIVE_PROXY_INFORMATIVE_IN_THIS_EXCITATION_FAMILY

Limit:
- RAW_HILBERT_PHASE_DERIVATIVE_NOT_OPERATIONAL_FOR_SINESWEEP_COORDINATE
- INPUT_COORDINATE_ESTIMATOR_AFFECTS_ANALYSIS_OPERABILITY
- SAME_SIMPLE_INTERFACE_PROXY_NOT_UNIVERSAL_ACROSS_EXCITATION_FAMILIES
- SINESWEEP_V0_2_CARRIES_PROMOTION_DEBT

## Claim ceiling

No physical chi is admitted.
No native response object is automatically renamed capital Chi.
Chi_arc is not uniquely identified from this analysis.
No new F-16 nonlinear mechanism is claimed.
No empirical Stability Inheritance claim is promoted.
