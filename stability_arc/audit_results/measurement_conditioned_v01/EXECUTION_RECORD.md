# Conditional tangent derivation audit v0.1 execution record

## Frozen source

- preregistration: `stability_arc/measurement_conditioned/PREREGISTRATION_CONDITIONAL_TANGENT_DERIVATION_AUDIT_v0.1.md`
- preregistration SHA-256: `0dc7cf7f1538a5e591e1df48f80de3bb370796aabfbac01728e584577b514938`
- implementation: `stability_arc/measurement_conditioned/code/conditional_tangent_audit_v01.py`
- implementation SHA-256: `c8e95b5e865fd467f4c7aca8783b0346f8d1ab283db1e23265922193590281ac`

## Attempt 1: mechanical failure preserved

GitHub Actions run `33231598000` stopped before scientific execution. Checkout and frozen-source identity capture passed. `actions/setup-python@v5` then failed because workflow-level `cache: pip` requires a `requirements.txt` or `pyproject.toml`, neither of which exists in this repository.

Classification: **MECHANICAL / CI CONFIGURATION**.

Scientific consequence: **NONE**. The scientific audit step was skipped, no T0-T4 criterion was evaluated, and no scientific outcome existed to condition a repair on.

Repair: remove only the pip-cache option. No preregistered equation, fixture, parameter, tolerance, decision rule, code under scientific audit, or interpretation was changed.

## Attempt 2: frozen audit executed

GitHub Actions run `33231627696`, head commit `3cc3c498f62a2f6a03b9b0fe8d7fb3ea1225cdd2`.

Environment:
- Python `3.12.14`
- NumPy `2.1.3`
- Linux Azure hosted runner

Artifact:
- name: `stability-arc-conditional-tangent-audit-v01`
- artifact ID: `9708659316`
- artifact ZIP digest: `sha256:7b650e93e518a468da674a4422828988ef0ae4ede97ab54023d21e41f4abf962`
- result JSON SHA-256: `0a29b702cd17b929fa075e0bda3664a1263692a7e29969a06b31a4a758904ba6`
- environment lock SHA-256: `922bda33668b532b1f38c3212a5f3cf7f0618296eaa35ef1388793e0c3cd5845`
- source identity SHA-256: `357c98cad20480dbf6aaa2e5d32a7f1627a0e9106ae2c63d15fd70c4e9e9f281`

## Frozen decisions

- **T0 PASS**: trace/tangent validity. Maximum registered trace residual was `6.938893903907228e-18`, below `5e-12`.
- **T1 PASS**: same-noise tangent finite-difference agreement. Maximum fine-epsilon Frobenius error was `1.7007870458309456e-09`, below `1e-7`, with the required error decrease for every fixture.
- **T2 PASS**: same-record tangent finite-difference agreement. Maximum fine-epsilon Frobenius error was `1.7064751790239328e-09`, below `1e-7`, with the required error decrease for every fixture.
- **T3 PASS**: exact second-order reduction. All three registered oscillator cases gave zero reported floating-point difference between `-tr(A)/(2 sqrt(det(A)))` and `Gamma/(2 Omega)`.
- **T4 PASS**: both registered nonpositive-determinant controls returned `REFUSE`.

Overall: **PASS / DERIVATION_AUDIT_ONLY**.

## Interpretation firewall

This closes only the registered mathematical/implementation consistency checks for the same-noise and same-record first variations and the exact second-order block reduction. It does not show that a tangent spectrum predicts localization, does not define a unique scalar for a general stochastic conditional generator, and does not turn any prior localization result into confirmation.

The next step must remain pre-outcome: derive/audit the measurement-dressed spectral baseline and the rule for when a response-relevant second-order mode pair is licensed or refused before any new prospective localization target is generated.
