# F-16 GVT Cross-Excitation Exploratory Result v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Corrected protocol status:** POST-RESULT EXPLORATORY / PROMOTION DEBT
**Exposure correction:** commit 7e9b876a34bcc1cc32074c793185a7025882ce86
**Workflow run:** 36513837314
**Evidence class:** P0-D POST-RESULT EXPLORATORY
**Disposition:** CROSS_EXCITATION_MIXED
**Confirmatory consequence:** NONE

## Provenance

The original cross-excitation protocol was committed after the SpecialOdd validation scoring had technically completed. This was corrected before execution. The analysis therefore cannot increase the confirmatory ceiling and is retained only for architecture mapping and future hypothesis construction.

## Exploratory result

The predictor was constructed only from FullMSine estimation levels and evaluated against already-seen SpecialOdd Validation targets on the 34-bin common estimation-supported frequency set in the frozen 6.5-8.2 Hz band.

At 49.0 N:
- amplitude-conditioned FullMSine predictor error = 0.9866468
- fixed FullMSine Level-1 predictor error = 1.0337648
- ratio = 0.954421

Amplitude conditioning improved the cross-family comparison modestly.

At 97.1 N:
- amplitude-conditioned predictor error = 0.9896574
- fixed Level-1 predictor error = 0.9485075
- ratio = 1.043384

Amplitude conditioning was worse than the fixed low-amplitude reference.

The low-amplitude 12.2 N case used the predeclared no-extrapolation Level-1 anchor and therefore has ratio exactly 1 by construction.

Frozen exploratory disposition:

**CROSS_EXCITATION_MIXED**

## Interpretation

The FullMSine amplitude relation does not transport as a single universal map into SpecialOdd response organization.

This narrows the positive within-family results:

- FullMSine: amplitude-conditioned representations strongly improve all three reserved levels.
- SpecialOdd: amplitude-specific representations win at all three held-out realizations.
- Direct FullMSine -> SpecialOdd amplitude transport: mixed.

The architecture therefore appears to be conditioned by more than scalar excitation amplitude alone. Excitation design, spectral support, history/steady-state construction, nonlinear detection-line structure, or other native features can change the realized response representation.

This is exactly the kind of result that argues against collapsing the architecture to one amplitude coordinate.

## Function / Limit consequence

Function:
- OPERATING_REGIME_CONDITIONING_CAN_TRANSPORT_PARTIALLY_ACROSS_EXCITATION_FAMILIES.

Limit:
- AMPLITUDE_ALONE_DOES_NOT_DEFINE_A_UNIVERSAL_CROSS_EXCITATION_MAP.
- WITHIN_FAMILY_REPLICATION_DOES_NOT_GUARANTEE_CROSS_FAMILY_TRANSPORT.

## Claim ceiling

No SI-specific claim is promoted.

No new mechanism is asserted.

The result carries promotion debt because its SpecialOdd targets were already seen before protocol commitment.

Fresh untouched evidence is required for any future cross-excitation confirmation.
