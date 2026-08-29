# QuTiP 5.3.1 runtime admission v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

This phase tests only whether the current GitHub Actions environment can install and execute the independently maintained QuTiP solver stack required by the historical Stability Arc independent-engine cross-check.

It does **not** reproduce the historical notebook and does **not** close the historical QuTiP scientific-validation gap. The original notebook remains a separately tracked provenance target:

- historical path: `history/v0.6_source/notebooks/Stability_Measurement_v0.6_QuTiP_Crosscheck.ipynb`
- expected historical SHA-256: `be5b0eb655dc7ab2212a5176123804f798992dbe3e4e5a8bda56537d65bc9d82`
- target historical QuTiP release: `5.3.1`

No historical notebook result, localization outcome, GFSA external-candidate response, or prior scientific score is used to choose this runtime test.

## Fixed environment target

- GitHub-hosted Ubuntu runner
- CPython `3.12`
- QuTiP exactly `5.3.1`
- dependency versions are resolved by pip and recorded with `pip freeze`; they are not tuned after outcome inspection

## Fixed analytic smoke model

Use a two-level system with

- Hamiltonian `H=0`;
- initial state `|+><+|`, where `|+>` is the +1 eigenstate of `sigma_x`;
- one dephasing collapse operator `c=sqrt(gamma) sigma_z`;
- `gamma=0.37`;
- `t=linspace(0,5,101)`.

For this Lindblad convention,

`<sigma_x>(t) = exp(-2 gamma t)`

exactly.

Run QuTiP `mesolve` with fixed numerical options `atol=1e-12`, `rtol=1e-10`, and stored states.

## Frozen gates

### Q0 package identity

PASS requires imported `qutip.__version__ == "5.3.1"`.

### Q1 analytic solver accuracy

PASS requires the maximum absolute error between QuTiP `<sigma_x>(t)` and `exp(-2 gamma t)` over all 101 times to be `<=1e-7`.

### Q2 density-matrix validity

Across all stored states:

- maximum absolute trace error `|Tr(rho)-1| <=1e-10`;
- maximum Frobenius Hermiticity residual `||rho-rho^dagger||_F <=1e-10`;
- minimum density-matrix eigenvalue `>=-1e-9`.

### Q3 provenance capture

PASS requires preservation of:

- workflow commit SHA and ref;
- preregistration SHA-256;
- runtime-test source SHA-256;
- Python version;
- QuTiP version;
- `pip freeze` environment lock;
- raw result JSON and stdout;
- SHA-256 manifest of emitted evidence.

## Decision

`RUNTIME_ADMITTED` requires `Q0 & Q1 & Q2 & Q3`.

Any failure remains part of the record. A package-install or runner failure is mechanical/runtime evidence, not a scientific failure. A numerical disagreement after QuTiP successfully executes is investigated before any tolerance or fixture is changed. No gate, model parameter, analytic target, or tolerance may be changed inside v0.1 after execution.

## Interpretation firewall

A PASS establishes only that the current GitHub environment can run QuTiP 5.3.1 correctly on this independent analytic control. It does not establish agreement with the historical Stability Arc SciPy calculations, does not reconstruct the missing notebook, and does not promote any new physical claim.
