# Conditional measurement-tangent derivation audit v0.1 result

**Status:** PASS
**Interpretation:** DERIVATION_AUDIT_ONLY
**Branch:** `agent/stability-arc-gfsa-v072`

## Frozen sources

- Preregistration: `stability_arc/measurement_conditioned/PREREGISTRATION_CONDITIONAL_TANGENT_DERIVATION_AUDIT_v0.1.md`
- Audit code: `stability_arc/measurement_conditioned/code/conditional_tangent_audit_v01.py`
- preregistration SHA-256: `0dc7cf7f1538a5e591e1df48f80de3bb370796aabfbac01728e584577b514938`
- audit-code SHA-256: `c8e95b5e865fd467f4c7aca8783b0346f8d1ab283db1e23265922193590281ac`

## Mechanical failure retained as evidence

Initial run `33231598000` at commit `644f1a8b3cd0b756c090190dee293c5111460d52` failed before dependency installation or scientific execution. `actions/setup-python@v5` was configured with pip caching, but the repository contained neither `requirements.txt` nor `pyproject.toml`, so setup-python stopped with:

`No file ... matched to [**/requirements.txt or **/pyproject.toml]`

Classification: **MECHANICAL / CI CONFIGURATION**.

No T0-T4 gate executed in the failed run, so it contains no scientific outcome. The failure artifact was preserved as artifact `9708649933`; its uploaded ZIP digest was `e901f5daccfd797b01967c92fbbf589ec9d1aab7c436ff93ba6852ffdf1d3daf`.

The smallest non-scientific repair removed the inappropriate setup-python cache request. No equation, fixture, tolerance, dependency version, gate, or decision rule changed. Repair commit: `3cc3c498f62a2f6a03b9b0fe8d7fb3ea1225cdd2`.

## Successful frozen rerun

Workflow run: `33231627696`
Head commit: `3cc3c498f62a2f6a03b9b0fe8d7fb3ea1225cdd2`
Runner: Ubuntu 24.04, Python 3.12.14, NumPy 2.1.3

### Gate results

- **T0 trace/tangent validity: PASS.** Largest listed trace residual was `6.938893903907228e-18`; base-state eigenvalues were approximately `0.2806258903151969` and `0.7193741096848031`.
- **T1 same-noise finite-difference gate: PASS.** Maximum fine-epsilon Frobenius error: `1.7007870458309456e-09`, below the frozen `1e-7` gate; every registered row improved when epsilon decreased from `1e-4` to `1e-5`.
- **T2 same-record finite-difference gate: PASS.** Maximum fine-epsilon Frobenius error: `1.7064751790239328e-09`, below the frozen `1e-7` gate; every registered row improved when epsilon decreased.
- **T3 exact second-order reduction: PASS.** Maximum absolute error in `chi_block = Gamma/(2 Omega)` across the three registered blocks: `0.0`.
- **T4 refusal controls: PASS.** Both registered unstable/invalid 2x2 controls returned `REFUSE`.

Overall decision: **PASS** under the preregistered rule `T0 & T1 & T2 & T3 & T4`.

## Preserved evidence

Successful artifact ID: `9708659316`
Artifact ZIP SHA-256: `7b650e93e518a468da674a4422828988ef0ae4ede97ab54023d21e41f4abf962`
Artifact size: 3254 bytes
Artifact retention expiry: 2026-11-27

Internal file SHA-256 values recorded by the workflow:

- `conditional_tangent_audit_v01.json`: `0a29b702cd17b929fa075e0bda3664a1263692a7e29969a06b31a4a758904ba6`
- `stdout.txt`: `0a29b702cd17b929fa075e0bda3664a1263692a7e29969a06b31a4a758904ba6`
- `environment_lock.txt`: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- `source_identity.txt`: `357c98cad20480dbf6aaa2e5d32a7f1627a0e9106ae2c63d15fd70c4e9e9f281`

## Interpretation firewall

This PASS closes only the registered differential-identity and exact two-dimensional reduction audit. It does **not** establish that a conditional tangent spectrum predicts localization, that a unique scalar chi exists for a general conditional generator, or that chi=1 is optimal under measurement.

The next safe work is reproducibility/representation work that does not use prior localization outcomes as fitting targets. Any prospective localization test requires a separate freeze and untouched evidence.
