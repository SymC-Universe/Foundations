# GFSA v0.7.2 execution checkpoint

Date: 2026-08-28
Branch: `agent/stability-arc-gfsa-v072`

## Supplied release

- Archive: `Generator_First_Stability_Architecture_v0.7.2(1).zip`
- SHA-256: `d4d78900a619a2579a7056ea7529116cde00dd4e937ff4c4790dad7e90816812`
- Package contents: 1,213 files

## Independent local verification

The supplied release was unpacked and checked directly from the preserved code and data.

Command:

```text
python code/validate_package_v072.py .
```

Result:

```text
PACKAGE VALIDATION: PASS
C18 PASS_CALIBRATION_VALIDITY
OBS18 PASS
OBS19 PASS
external_interface LICENSED_FOR_EXTERNAL_NUMERICAL_ADMISSION
observable_ep_firewall PASS
```

Frozen OBS18 predictions were rescored from the preserved truth and prediction files:

- status: PASS
- rational emit fraction: 0.9166666666666666
- Spearman: 0.9049047728796058
- median absolute error: 0.019033179062645234
- rational coverage: 0.9854545454545455
- near/far AUC: 0.9897039897039898
- stress emitted coverage: 0.9305555555555556
- stress false-licensed fraction: 0.05
- EP violations: 0

Frozen OBS19 blind-holdout predictions were rescored from the preserved truth and prediction files:

- status: PASS
- rational emit fraction: 0.865
- Spearman: 0.8941167668669715
- median absolute error: 0.0249890643872549
- rational coverage: 0.9884393063583815
- near/far AUC: 0.9895652173913043
- stress emitted coverage: 0.9393939393939394
- stress false-licensed fraction: 0.05
- EP violations: 0

All eight stored gates pass in both OBS18 and OBS19.

## Scientific firewall

This checkpoint does not change the frozen v0.7.2 interpretation. The observable interface licenses only the finite-band visible modal pole-proximity result admitted by the frozen protocol, or `NONIDENTIFIABLE`. It does not license hidden-generator order or rationality, mechanical chi, or an observable-only exceptional-point label.

## Current frontier

The next executable scientific step is external numerical admission under the already-frozen v0.7 external-candidate contract. No external candidate threshold or scoring rule may be reconstructed or retuned after viewing candidate response values.

## Operational state

GitHub organization write access was restored on 2026-08-28. This branch is now the controlled execution lane for the next Stability Arc work.
