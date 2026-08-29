# QuTiP runtime admission v0.1 result

**Status:** RUNTIME_ADMITTED
**Scope:** RUNTIME_ADMISSION_ONLY
**Historical notebook cross-check:** STILL PENDING
**Branch:** `agent/stability-arc-gfsa-v072`

## Frozen source identities

Workflow run: `33231741394`
Head commit: `aeb141066fa9e21ad58b341da8c02ab01644ae3a`

- preregistration SHA-256: `0b5a9d09dce1fd1555deeed3f2b85ae8d764b7a14235c39a66d3a2a7051a5412`
- runtime code SHA-256: `74e17512b324e2ad07262f632c61ce59edf28deb2390cbe217381d8c99edfb3a`
- workflow SHA-256: `ff220dd5c99c84ae9557b9f4b8ad082215ce08c9e3148c92e67b29e91820d2b4`

## Environment

- Ubuntu 24.04 hosted runner
- Python 3.12.14
- QuTiP 5.3.1
- NumPy 2.5.2
- SciPy 1.18.1
- packaging 26.3

## Frozen admission gates

- **Q0 runtime version:** PASS. Observed QuTiP version exactly `5.3.1`.
- **Q1 analytic dephasing smoke test:** PASS. `gamma=0.37`, 101 time points on `[0,5]`, maximum absolute error `1.5216428117525993e-10`, below the frozen `1e-7` gate.
- **Q2 state-validity checks:** PASS. Maximum trace error `0.0`, maximum Hermiticity Frobenius error `0.0`, minimum density eigenvalue `0.0`, satisfying the frozen trace, Hermiticity, and positivity gates.
- **Q3 provenance/manifest capture:** PASS. Source identity, environment, import check, result JSON, stdout, and manifest were present and independently hash-verified.

Final workflow status:

`RUNTIME_ADMITTED`

`HISTORICAL_NOTEBOOK_CROSSCHECK_STILL_PENDING`

## Preserved artifact

Artifact ID: `9708692674`
Artifact name: `stability-arc-qutip-runtime-admission-v01`
Artifact ZIP SHA-256: `ccea56a1929ca10832e56c34e31cb4bbe27f2b1d95e64a942f85e3d884446dd1`
Artifact size: 7226 bytes
Artifact retention expiry: 2026-11-27

## Interpretation firewall

This result establishes only that a pinned QuTiP 5.3.1 environment is available and passes the frozen analytic/runtime integrity gates. It does **not** reproduce or reconstruct the historical notebook `history/v0.6_source/notebooks/Stability_Measurement_v0.6_QuTiP_Crosscheck.ipynb`, whose expected historical SHA-256 remains `be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`.

It therefore does not yet establish agreement between an independent QuTiP implementation and the historical Stability Arc measurement results.

## Next safe use

The admitted runtime may now be used for independently preregistered QuTiP work whose scientific inputs are frozen before execution. Historical-notebook equivalence remains a separate provenance problem. Measurement-conditioned same-noise and same-record channels must remain separately auditable while also permitting a preregistered joint/comparative analysis that preserves both identities and does not collapse them into a scalar unless independently justified.
