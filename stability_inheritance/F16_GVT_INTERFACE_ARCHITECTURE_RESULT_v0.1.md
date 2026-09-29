# F-16 GVT Interface-to-System Architecture P0-Q Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Protocol:** stability_inheritance/F16_GVT_INTERFACE_ARCHITECTURE_PROTOCOL_v0.1.md
**Workflow run:** 36512731466
**Evidence class:** PUBLIC EXTERNAL MEASURED / P0-Q
**Disposition:** AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT
**Architecture evidence role:** ARCHITECTURE_SUPPORTING_NATIVE
**Novelty role:** NATIVE_MODEL_COMPATIBLE_NO_SI_NOVELTY_CLAIM
**P1 eligibility:** NO

## Source identity

Official 4TU runtime source:
https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f

Archive:
- expected bytes: 148,455,295
- observed bytes: 148,455,295
- SHA-256: 2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa
- ZIP integrity: PASS
- archive members: 51
- BenchmarkData members: 41
- Validation-labeled members: 18
- SpecialOddMSine members: 6

Raw archive and signal values were not redistributed.

## Frozen FullMSine scoring

Files:
- Level 1: F16Data_FullMSine_Level1.mat
- Level 2 held-out: F16Data_FullMSine_Level2_Validation.mat
- Level 3: F16Data_FullMSine_Level3.mat
- Level 4 held-out: F16Data_FullMSine_Level4_Validation.mat
- Level 5: F16Data_FullMSine_Level5.mat
- Level 6 held-out: F16Data_FullMSine_Level6_Validation.mat
- Level 7: F16Data_FullMSine_Level7.mat

Sampling: 400 Hz.
Periods per level: 9.
Period 1 discarded as frozen.
Primary band: 6.5-8.2 Hz.
Primary excited support: 34 Fourier bins.
Full 2-15 Hz support: 267 bins.

The frozen amplitude-conditioned representation used only bracketing estimation levels 1/3, 3/5, and 5/7 to predict reserved levels 2, 4, and 6, respectively.

## Primary held-out results

| Held-out level | Force RMS N | Fixed Level-1 error | Amplitude-conditioned error | Ratio conditioned/fixed | Error reduction |
|---|---:|---:|---:|---:|---:|
| 2 | 24.6 | 0.5793214 | 0.3086432 | 0.5327668 | 46.72% |
| 4 | 61.4 | 1.5634159 | 0.1824404 | 0.1166935 | 88.33% |
| 6 | 85.7 | 1.8315811 | 0.0612828 | 0.0334590 | 96.65% |

All three predeclared held-out levels satisfy R_t < 1.

The frozen primary disposition is therefore:

**AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT**

The same ordering also held over the full 2-15 Hz secondary band.

## Output-specific primary-band results

At every reserved level, amplitude conditioning improved the excitation-point, wing-side, and payload-side outputs separately.

Level 2:
- excitation point: 0.54556 -> 0.28997
- wing side: 0.58354 -> 0.31122
- payload side: 0.58441 -> 0.31118

Level 4:
- excitation point: 1.30750 -> 0.15314
- wing side: 1.59702 -> 0.18543
- payload side: 1.61689 -> 0.18955

Level 6:
- excitation point: 1.47689 -> 0.04922
- wing side: 1.87230 -> 0.06291
- payload side: 1.92138 -> 0.06405

The effect is therefore not confined to one chosen output.

## Interface-relative architecture diagnostics

The frozen interface-relative proxy was H_payload - H_wing.

Distance from the Level-1 reference in the primary torsional band:

| Level | Relative-response distance from Level 1 |
|---|---:|
| 1 | 0.0000 |
| 2 | 0.5520 |
| 3 | 0.8878 |
| 4 | 1.1911 |
| 5 | 1.2718 |
| 6 | 1.3141 |
| 7 | 1.3953 |

The largest interface-relative response in the frozen 6.5-8.2 Hz band shifted from:
- 7.3242 Hz at Level 1
to:
- 7.2266 Hz by Levels 4-7.

This peak-shift diagnostic was secondary and did not determine the primary disposition.

## Interpretation

The result provides measured evidence that one fixed low-amplitude response representation is not adequate across the declared excitation regimes, whereas an amplitude-conditioned representation estimated without the reserved levels transports substantially better to every held-out level.

This is directly relevant to the Stability Architecture reconstruction because the benchmark's native scientific context locates important clearance/friction nonlinearities at the payload mounting interface, while the measured response changes appear across excitation-point, wing-side, and payload-side outputs.

The correct evidence classification is:

**ARCHITECTURE_SUPPORTING_NATIVE**

The result supports the architectural proposition that realized system response can depend systematically on an embedded interface regime and that representation adequacy changes with that regime.

It does not show that Stability Inheritance invented or uniquely explains this behavior. The native F-16 benchmark already anticipates excitation-dependent stiffness/damping and nonlinear interface effects.

## What this result does not establish

- no physical scalar chi is admitted;
- native FRFs are not automatically renamed capital Chi;
- Chi_arc is not automatically identified solely from this test;
- no carrier-resolved inheritance claim is made;
- no universal amplitude law is claimed;
- no universal monotonicity is claimed from the secondary distance trend;
- no novelty is claimed for clearance/friction nonlinearities or amplitude-dependent structural dynamics.

## Function / Limit consequence

Function:
- AMPLITUDE_CONDITIONED_SYSTEM_RESPONSE_TRANSPORTS
- LOCAL_INTERFACE_REGIME_ASSOCIATED_WITH_GLOBAL_RESPONSE_ORGANIZATION
- ARCHITECTURE_SUPPORTING_NATIVE

Limit:
- FIXED_LOW_AMPLITUDE_REPRESENTATION_INSUFFICIENT_ACROSS_DECLARED_REGIME
- LOCAL_LINEAR_VALIDITY_DOES_NOT_IMPLY_CROSS_REGIME_ADEQUACY

## Next preplanned check

Run the already frozen F16_GVT_SPECIALODD_LAYOUT_PREFLIGHT_v0.1.md without signal scoring. If the published 10-realization x 3-period layout is qualified, construct a separate cross-excitation replication protocol before inspecting its signal outcomes.
