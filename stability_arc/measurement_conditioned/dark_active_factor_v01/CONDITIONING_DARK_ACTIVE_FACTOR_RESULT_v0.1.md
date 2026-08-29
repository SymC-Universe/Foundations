# Conditioning-dark / active-sector factorization audit v0.1 result

**Status:** PASS
**Scope:** COMPARATIVE_DARK_ACTIVE_FACTORIZATION_ONLY
**Canonical workflow run:** `33250353613`
**Execution commit:** `6d8cb0020038e0e0831fe858890c009e48247fd3`

## Frozen source identities

- preregistration SHA-256: `696a34c47201265ff0f36c361c66e5f8550b8251467ceb16c181a7b9852c761b`
- audit code SHA-256: `7a1a73fe8510d6f92f7a544916d6f35e7b3636329022694462862b14586c70c5`
- workflow SHA-256: `e6c8296cae61bf0241ea2b6def7372ed58d6d2e4941dd1070d1471372c12efc3`
- result JSON SHA-256: `59644460988d8775fa2b72e3d51b8eea480d3fa83bfb64bea17339208f125fda`

## Artifact

- artifact ID: `9714162157`
- artifact ZIP SHA-256: `134a131d17ee9e5ca45a0cbbe4830f199a30df256194eb465999b6fb42dd3429`
- artifact retention expiry: 2026-11-27

## Frozen decision

All preregistered gates F0-F7 passed.

- F0 maximal invariant dark-space construction: PASS; maximum residual `2.6423307986078724e-16` versus `1e-10` gate.
- F1 instantaneous-nullspace distinction: PASS; S1 admitted its invariant full kernel, while S2 returned exactly `REFUSE_FULL_KERNEL_FACTOR`.
- F2 global common characteristic factor: PASS; maximum physical polynomial reconstruction residual `1.3322676295501878e-15` and record-conditioned residual `4.440892098500626e-16` versus `2e-9` gate.
- F3 active-quotient bridge identity: PASS; maximum residual `8.326672684688674e-17`.
- F4 moved-spectrum completeness: PASS; all conditioning-induced characteristic-polynomial change was accounted for by the active quotient after extracting only the independently constructed dark factor.
- F5 exact dark-mode preservation: PASS; maximum residual `8.683741725690198e-17`.
- F6 refusal controls: PASS; cross-sector degeneracy returned `REFUSE_DEGENERATE_SECTOR_ATTRIBUTION`, and defective active quotient returned `REFUSE_DEFECTIVE_ACTIVE_SECTOR`.
- F7 coordinate covariance: PASS; maximum reconstructed-projector residual `5.551115123125783e-16` and dark-factor polynomial residual `1.1102230246251565e-16`.

## Quantum-control result

For each of the three fresh registered quantum controls QF1-QF3:

- the instantaneous conditioning-null space `ker(V^T)` had dimension 2;
- that full 2D nullspace was **not** invariant under `A_phys` and therefore correctly returned `REFUSE_FULL_KERNEL_FACTOR`;
- the maximal dynamically invariant dark subspace `D=ker([V^T;V^T A;...])` had dimension 1;
- the one-dimensional dark mode was identifiable and exactly preserved by record conditioning;
- the remaining quotient was two-dimensional;
- the quotient conditioning update retained rank 1.

The full-kernel invariance residuals were `0.88`, `1.19`, and `0.67`, respectively, while the maximal-dark invariance/annihilation residuals were at numerical roundoff.

This establishes an important distinction for the registered local model: **instantaneous measurement invisibility is not sufficient for dynamical conditioning darkness.** A perturbation direction can satisfy `V^T x=0` at one instant yet rotate under `A_phys` into the measurement-visible sector. Only the maximal `A_phys`-invariant subspace inside that nullspace is an exact common physical/inference factor.

## Exact licensed factorization

For the registered controls, with orthogonal coordinates adapted to the maximal dark subspace,

`Q^T A_phys Q = [[A_D, *],[0,A_A]]`

and

`Q^T A_rec Q = [[A_D, *],[0,Arec_A]]`.

Thus

`det(zI-A_phys) = det(zI-A_D) det(zI-A_A)`

and

`det(zI-A_rec) = det(zI-A_D) det(zI-Arec_A)`.

The dark factor is globally common and requires no division by a physical resolvent, so it remains meaningful at physical poles. Every conditioning-induced change in the characteristic polynomial is contained in the active quotient.

The active quotient obeys

`Arec_A - A_A = U_A V_A^T`

and preserves the previously closed information-rank bound.

## Interpretation firewall

This PASS does not establish stochastic immunity of the dark mode. The shared stochastic tangent matrix `B`, and hence the `B tensor B` term in the second-moment generator, remains outside this deterministic conditioning-difference factorization.

It does not establish localization prediction, a universal dark-space dimension, a preferred eigenmode, or a scalar chi for the full generator.

A new scientific question is now licensed without consulting localization outcomes: because the three fresh quantum controls leave an exact **two-dimensional active quotient**, test whether the already-registered real stable 2x2 Stability Arc coordinate is mathematically admissible on that quotient, with explicit refusal whenever quotient dimension, stability, identifiability, or coordinate invariance fails.
