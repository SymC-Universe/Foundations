# Validation Environment

This file records the reference environment used to harden the substrate-inheritance computational validation workflow. It is an implementation and reproducibility record, not a scientific result.

## Reference successful environment

The successful GitHub Actions runs used:

- runner operating system: Ubuntu 24.04;
- Python: CPython 3.12.14;
- NumPy: 2.5.2;
- pytest: 9.1.1;
- iniconfig: 2.3.0;
- packaging: 26.3;
- pluggy: 1.6.0;
- Pygments: 2.21.0.

The dependency set is pinned in `requirements-validation.txt`.

## GitHub Actions provenance

The validation workflow pins action implementations by commit SHA rather than relying only on mutable major-version tags:

- `actions/checkout`: `11d5960a326750d5838078e36cf38b85af677262`;
- `actions/setup-python`: `a26af69be951a213d495a4c3e4e4022e16d87065`;
- `actions/upload-artifact`: `ea165f8d65b6e75b540449e92b4886f43607fa02`.

The workflow also writes the realized runtime package environment into the uploaded validation artifact so a future reviewer can compare the executed environment with the pinned declaration.

## Change rule

Dependency, Python, runner, or action-version changes are allowed when needed, but they are treated as reproducibility changes. They should:

1. be made explicitly;
2. run the full validation suite;
3. preserve the evidence guards;
4. record any numerical differences;
5. avoid changing scientific thresholds or labels merely to recover a passing build.

If a dependency change materially changes a numerical result, the affected evidence should be reviewed before the new environment becomes authoritative.
