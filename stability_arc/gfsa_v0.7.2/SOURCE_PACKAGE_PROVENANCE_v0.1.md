# GFSA v0.7.2 source-package provenance capsule v0.1

Status: VERIFIED LOCAL CLEAN-EXTRACT CHECKPOINT
Date: 2026-08-29
Branch: `agent/stability-arc-gfsa-v072`

This record preserves the identity and mechanical reproduction status of the supplied Generator-First Stability Architecture v0.7.2 archive. It does not add or modify any scientific criterion.

## Archive identity

- Supplied archive: `Generator_First_Stability_Architecture_v0.7.2(1).zip`
- SHA-256: `d4d78900a619a2579a7056ea7529116cde00dd4e937ff4c4790dad7e90816812`
- Clean-extracted file count: `1213`

## Key frozen-file hashes

- `PREREGISTRATION_EQUIVALENCE_BRIDGE_v0.7.2.md`: `014e4f507b79d71ed21f5531a524bfd2113b58d97134de553bfb18db79fd50aa`
- `INTERFACE_LICENSE_v0.7.2.md`: `8425c12764f2069068c5e3d7c607e0c66b14977f28b0b6eac98d446b867bd53f`
- `INTERFACE_BRIDGE_REPORT_v0.7.2.md`: `a7f1531ce88f32188b2112438faf5b8e18ad8f2816d8bd09a5b3b937fb16af76`
- `REPRODUCIBILITY_GUIDE_v0.7.2.md`: `676445e726986f14595d485a92a2fb91949f5a0af465e32e41170cdab45c624b`
- `code/validate_package_v072.py`: `348d68c8abf70736d40402cb7fd0ca414ccec6dd20c432ba6092b05f81cbbf4d`
- `code/score_equiv_v072.py`: `545c67d729104466d26739da79bd4eedc9a606b36c4d501cb56e59a06f283b65`
- `observer/sk_equivalence_observer_v072.py`: `097bdfa68bc624cf3bf2e46e5ecc9efc31106671f8c5a000d4ab8d4e26afca1a`
- `MANIFEST_SHA256.txt`: `132d16fd828c8752df6be4490da3b8a7c83abedfa2f31bb06a0742f3330b20be`

## Clean-extract validation

Executed from a fresh extraction of the supplied archive:

`python code/validate_package_v072.py`

Observed terminal state:

- `PACKAGE VALIDATION: PASS`
- `C18 PASS_CALIBRATION_VALIDITY`
- `OBS18 PASS`
- `OBS19 PASS`
- `external_interface LICENSED_FOR_EXTERNAL_NUMERICAL_ADMISSION`
- `observable_ep_firewall PASS`

## Independent frozen-result rescoring

The two documented rescore commands in `REPRODUCIBILITY_GUIDE_v0.7.2.md` were executed without parameter changes.

- OBS18 regenerated result SHA-256: `49207d7ec04e83bea4a0302397859644d696d1fb140b4c65afde98e6a2188e82`
- Stored OBS18 result SHA-256: `49207d7ec04e83bea4a0302397859644d696d1fb140b4c65afde98e6a2188e82`
- OBS18 byte comparison: MATCH

- OBS19 regenerated result SHA-256: `eb2e13c5bc17fd53d9fa02c375f0abf495afeed79b0f8b212814cd2f9bf4d952`
- Stored OBS19 result SHA-256: `eb2e13c5bc17fd53d9fa02c375f0abf495afeed79b0f8b212814cd2f9bf4d952`
- OBS19 byte comparison: MATCH

## Scope firewall

This checkpoint verifies faithful preservation and rescoring of the v0.7.2 synthetic calibration/validation/holdout release. It does **not** license inspection of external candidate response values by itself.

The exact frozen v0.7 external-candidate admission contract remains a separate required input. Until that contract is recovered and hashed, the active anti-circularity control requires `PROVENANCE_HOLD` for external numerical scoring.
