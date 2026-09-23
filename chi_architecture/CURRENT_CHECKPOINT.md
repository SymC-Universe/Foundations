# Chi Architecture Active Checkpoint

**Checkpoint ID:** D02A-CP3-V0.2-EXECUTED  
**Date:** 2026-09-22  
**Branch:** `chi-architecture-p0`  
**Execution commit:** `2eb3f529eb215cb21e03394e35dfb45f6f078781`  
**Workflow run:** `35816379440`  
**Protocol:** SymC GOM v0.8.3

## Corrected physical execution

D02A v0.2 executed successfully under the frozen corrected-matrix contract.

- artifact: `chi-architecture-d02a-physical-v02`
- artifact ID: `10731212172`
- artifact digest: `sha256:049c4648f71b13e30a5470ebfeaf06cea3a482f642826aec06e92efb461528a9`
- full result SHA-256: `234315fb8e181c1538844efa6a94776e8dcdfaf9e67fda85006982584e511f2e`
- summary SHA-256: `4912e2fa20f05d14751567469696cfc7d0f0805ec2ba07d290572a0b1dc03fcb`
- result card SHA-256: `9895adb148000768e2dbaea317572fb78c176d48a5d914212c55a0978571061c`
- manifest SHA-256: `c3ac58b6b9779412dc8541644a6cb26cb5976b2093f2f97b3b976b9277821442`

Permanent compact archival metadata:

`chi_architecture/results/D02A_EXECUTION_ARCHIVE_v0.2.json`

## Archived facts before interpretation

- v0.1 partial failure remains preserved.
- all three corrected M-R matrices reconstructed with 21/21 identifiable q profiles.
- 300 K matrix: 46 x 21.
- 385 K matrix: 38 x 21.
- 419 K matrix: 21 x 21.
- six-row M-point linewidth table unchanged.
- lowercase chi remains refused.
- no cross-instrument absolute intensity comparison.
- no categorical carrier-similarity threshold.
- no DHO refit.

Pairwise normalized-shape diagnostics are archived in the execution record and must not be altered.

## Resume rule

1. Read the v0.1 integrity audit, v0.2 parser contract, and this archive.
2. Do not change any extraction or comparison rule in response to the archived numbers.
3. Interpret the linewidth transformation and carrier-shape evolution against standard q-resolved phonon analysis.
4. Decide whether the inheritance/transformation language adds anything beyond native phonon analysis.
5. If native methods already state the full result, record `NATIVE_PHONON_TOOLKIT_SUFFICIENT`.
6. Preserve P0-D / post-result provenance; D02A cannot pay untouched confirmation debt.
7. Keep lowercase chi refused unless a separate future omega0-identification protocol is frozen before fitting.
