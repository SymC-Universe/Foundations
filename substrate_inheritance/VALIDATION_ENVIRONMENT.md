# Validation Environment

This file records the validation environment used by the substrate-inheritance computational workflow. It is an implementation and reproducibility record, not a scientific result.

## Reference successful environment

The hardened reference validation used:

- runner operating system: Ubuntu 24.04;
- Python: CPython 3.12.14;
- NumPy: 2.5.2;
- pytest: 9.1.1;
- iniconfig: 2.3.0;
- packaging: 26.3;
- pluggy: 1.6.0;
- Pygments: 2.21.0.

The dependency set is pinned in `requirements-validation.txt`.

## Reference action revisions

Reference run `33292821080` used the following reviewed action commits:

- `actions/checkout`: `11d5960a326750d5838078e36cf38b85af677262`;
- `actions/setup-python`: `a26af69be951a213d495a4c3e4e4022e16d87065`;
- `actions/upload-artifact`: `ea165f8d65b6e75b540449e92b4886f43607fa02`.

These values describe the fixed reference milestone and are retained for reproduction even after later CI infrastructure upgrades.

## Current workflow action revisions

The current workflow pins the newer Node 24 action lines by exact commit SHA:

- `actions/checkout` v7.0.1: `3d3c42e5aac5ba805825da76410c181273ba90b1`;
- `actions/setup-python` v7.0.0: `5fda3b95a4ea91299a34e894583c3862153e4b97`;
- `actions/upload-artifact` v7.0.1: `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`.

The workflow writes the realized runtime package environment into every uploaded validation artifact so a future reviewer can compare an executed run with the declared package pins.

## Change rule

Dependency, Python, runner, or action-version changes are allowed when needed, but they are treated as reproducibility changes. They should:

1. be made explicitly;
2. run the full validation suite;
3. preserve the evidence guards;
4. record any numerical differences;
5. avoid changing scientific thresholds or labels merely to recover a passing build.

A newer action or dependency version is not adopted solely because it is newer. It must survive the unchanged validation route. If an infrastructure change materially changes a numerical result, the affected evidence should be reviewed before the new environment becomes authoritative.
