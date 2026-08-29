# Conditional measurement-tangent derivation audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

This is a derivation/implementation audit for the next Stability Arc quantum-position frontier. It is not a localization holdout and does not score any prior Phase 4 localization outcome. It tests whether the proposed linearized dynamics of a normalized continuously measured state are internally correct and reduce to the established second-order damping coordinate in the exact two-dimensional limit.

No E16-E27 position errors, external-candidate responses, or GFSA v0.7 external-candidate numerical values may be read by this audit.

## Frozen conditional equation convention

Use

`d rho = L(rho) dt + sqrt(2 eta kappa) H_x(rho) dW`

with

`H_x(rho) = x rho + rho x - 2 Tr(x rho) rho`.

`L` is linear and may contain Hamiltonian evolution, ordinary Lindblad dissipation, and unconditional measurement backaction.

For a traceless perturbation `delta rho`, define `delta mu = Tr(x delta rho)`.

### T1: same-noise physical tangent

The registered tangent is

`d(delta rho) = L(delta rho) dt + sqrt(2 eta kappa) deltaH_x dW`,

where

`deltaH_x = x delta rho + delta rho x - 2 mu delta rho - 2 delta mu rho`.

### T2: same-record inference tangent

For a fixed detector increment

`dY = sqrt(8 eta kappa) mu dt + dW`,

candidate filters use their own innovation `dY - sqrt(8 eta kappa) mu_candidate dt`.

The registered first variation is

`d(delta rho) = L(delta rho) dt + sqrt(2 eta kappa) deltaH_x dW - 4 eta kappa delta mu H_x(rho) dt`.

The same-noise and same-record tangents are distinct objects and may not be conflated.

## Fixed numerical fixture

Two-level Hilbert space with Pauli operators.

- `eta = 0.73`
- `kappa = 0.41`
- `omega = 1.17`
- `gamma = 0.23`
- measured operator `x = sigma_z / 2`
- Hamiltonian `H = omega sigma_y / 2`
- amplitude-damping collapse amplitude `sqrt(gamma)`
- unconditional measurement term `2 kappa D[x]`
- base Bloch vector `(0.20, -0.25, 0.30)`
- tangent Bloch vector `(-0.13, 0.21, 0.17)`
- `dt in {1e-4, 3e-5, 1e-5}`
- normalized innovation coefficients `dW/sqrt(dt) in {0.37, -0.61}`
- finite-difference perturbations `epsilon in {1e-4, 1e-5}`

No parameter is selected from an observed audit result.

## Frozen gates

### T0 trace/tangent validity

PASS requires:
- `Tr(delta rho)=0` initially to absolute tolerance `1e-14`;
- `Tr(L(delta rho))`, `Tr(deltaH_x)`, and `Tr(H_x(rho))` each have absolute magnitude `<=5e-12` for every registered fixture.

### T1 same-noise finite-difference gate

For every registered `dt` and innovation coefficient, compare the analytic first-variation one-step Euler-Maruyama map with a centered-by-base forward finite difference of the nonlinear same-noise map.

PASS requires Frobenius error `<=1e-7` at `epsilon=1e-5`, and the `epsilon=1e-5` error must be smaller than the corresponding `epsilon=1e-4` error.

### T2 same-record finite-difference gate

Repeat T1 while holding `dY` fixed and allowing each perturbed candidate state to construct its own innovation.

PASS uses the same `1e-7` error and monotonic finite-difference criteria.

### T3 exact second-order reduction

For real oscillator blocks

`A = [[0,1/m],[-m Omega^2,-Gamma]]`,

define

`chi_block = -tr(A)/(2 sqrt(det(A)))`.

Fixed checks are `(m,Omega,Gamma) = (1,1,0.6), (2.3,0.7,1.4), (0.4,2.1,5.0)`.

PASS requires `|chi_block - Gamma/(2 Omega)| <= 1e-14` for every case.

### T4 refusal controls

The scalar block coordinate is REFUSED if the supplied real 2x2 block is not asymptotically stable (`tr >= 0`) or has `det <= 0`. PASS requires refusal on both registered negative controls:

- `diag(1,-2)`;
- `[[0,1],[1,-1]]`.

This refusal does not claim that no higher-dimensional stability representation exists.

## Decision rule

Overall PASS requires `T0 & T1 & T2 & T3 & T4`.

Any failed gate remains failed and is investigated as a signal. No tolerance, fixture, equation, or distinction between same-noise and same-record tangents may be changed inside v0.1 after execution. A scientifically motivated replacement requires a new version and preserved v0.1 result.

## Interpretation firewall

A PASS validates only the stated differential identities and exact second-order reduction. It does **not** establish that a particular tangent spectrum predicts localization, that a scalar chi exists for a general conditional generator, or that chi=1 is an optimum under measurement. Those require a separately preregistered prospective phase on untouched systems.
