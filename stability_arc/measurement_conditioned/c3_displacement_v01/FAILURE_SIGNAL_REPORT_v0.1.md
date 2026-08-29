# c3 boundary-displacement map v0.1 failure-signal report

**Status:** PERMANENT `DISPLACEMENT_MAP_FAILURE`
**Canonical run:** `33264098911`
**Execution commit:** `8ca5bbf7cc1cf12907bec6bc25ee7ee84ced1c28`
**Classification:** NUMERICAL / NEAR-BOUNDARY DETERMINANT CONDITIONING

## Preserved evidence

- artifact ID: `9718105705`
- artifact ZIP SHA-256: `b7545d48f9b17fb5220ae2197d161b70cbc9b79e1fd0966777d69714e11846f5`
- preregistration SHA-256: `f8243c7266267c0f4ee0c7c59f2f3d450c356434409775157ff861763c3f5411`
- code SHA-256: `9831ecc5afe00cd904893aa6c741087bd5edb18ee3a91a2a52bf66493479925d`
- workflow SHA-256: `fdce61c4a63c984e7d56fdfa51e8d8ea0821109d66434b62e07633c8d2160c7b`

## Frozen gate outcome

- D0 coefficient lineage: PASS
- D1 synthetic interval-engine controls: PASS
- D2 fresh sign-partition controls: PASS, 256 fresh base tuples, 0 partition disagreements
- D3 independent determinant reconstruction: **FAIL**, 16 determinant-comparison failures, maximum relative-or-absolute error `3.973577272775586e-09` against the frozen `2e-10` gate
- D4 channel-swap covariance: PASS, 0 failures
- D5 set reconstruction: PASS, 0 coverage failures

The overall v0.1 result therefore remains `DISPLACEMENT_MAP_FAILURE`. It is not converted to PASS by later analysis.

## Failure investigation

The preserved artifact was reconstructed after the run without changing the frozen v0.1 code or thresholds.

All 16 D3 failures occur on only 7 of the 256 fresh base tuples: `BD070`, `BD079`, `BD185`, `BD193`, `BD217`, `BD254`, and `BD255`.

Every failed D3 probe was one of the preregistered two-sided probes placed approximately `1e-7` relative distance from a nonnegative `c3=0` root. No ordinary log-spaced probe produced a D3 failure.

Critically:

- sign mismatch count among the 16 D3 failures: **0**;
- joint interval-label mismatch count among the 16: **0**;
- D2 global partition disagreements: **0**;
- D4 channel-swap failures: **0**;
- D5 coverage failures: **0**.

Representative root-adjacent cases include:

- `BD193`, `w=224.57109432002673`: physical exact-quadratic `c3=-0.137734511...`, direct binary64 determinant `c3=-0.137734515...`, same NEG sign, comparison error `3.973577272775586e-09`;
- `BD255`, `w=76.38771217839523`: physical exact-quadratic `c3=+0.496082629...`, direct binary64 determinant `c3=+0.496082630...`, same POS sign, comparison error `1.32364613714131e-09`;
- `BD185`, immediately on both sides of record root `w=7.459001185337016`, gave comparison errors about `3.8e-10` while preserving the expected POS/NEG side change.

The failure pattern is consistent with cancellation sensitivity in binary64 evaluation of `-det(G)` when `det(G)` is deliberately driven near zero by root-adjacent probing. This diagnosis is supported by the exact symbolic identity `c3=-det(G)` already closed in the independent c3 derivation phase, but it is **not allowed to overwrite D3 FAIL**.

## What the failure reveals

v0.1 successfully audited the topology/sign partition of the proposed set-valued displacement representation, but its chosen binary64 determinant oracle was not numerically robust enough to satisfy its own strict `2e-10` equality gate arbitrarily close to the derived boundary.

Thus the failure constrains the reproducibility method: a boundary audit that deliberately probes extremely close to `c3=0` needs an independently constructed high-precision determinant oracle or another numerically stable exact reconstruction. Merely loosening the tolerance would be outcome-driven and is prohibited.

## Justified next action

Preserve v0.1 unchanged and create v0.2 as a numerical-remediation audit only.

v0.2 must:

1. retain the same coefficient formulas, seed `2026082908`, 256 base tuples, fixed log probes, root-adjacent offsets, and `2e-10` comparison gate;
2. independently construct the same 2x2 active matrices and 3x3 symmetric second-moment generator;
3. evaluate the determinant with high-precision arithmetic rather than binary64 `numpy.linalg.det`;
4. verify all non-boundary probes against the exact quadratic under the unchanged gate;
5. retain binary64 results only as a diagnostic of the preserved v0.1 failure, not as the v0.2 scientific oracle;
6. fail if any sign/partition inconsistency remains in high precision.

A v0.2 PASS would classify v0.1 as a numerical-oracle failure and license the displacement representation only through the new high-precision audit. It would not erase the permanent v0.1 failure record.
