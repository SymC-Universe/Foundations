# c3 boundary-displacement D3 high-precision remediation v0.2

**Status:** FROZEN BEFORE EXECUTION
**Scope:** NUMERICAL_ORACLE_REMEDIATION_ONLY

## Preserved predecessor failure

`c3_displacement_v01` run `33264098911` remains permanently `DISPLACEMENT_MAP_FAILURE` because frozen gate D3 failed at 16 root-adjacent probes. D0, D1, D2, D4, and D5 passed. No v0.1 threshold, probe, fixture, root, or result may be changed.

Failure report:
`stability_arc/measurement_conditioned/c3_displacement_v01/FAILURE_SIGNAL_REPORT_v0.1.md`

The post-failure investigation found that all 16 D3 failures occurred at the frozen two-sided probes approximately `1e-7` relative distance from a `c3=0` root. All 16 retained the same c3 sign and the same joint interval label between the exact quadratic and binary64 determinant reconstruction.

This is a numerical-remediation audit. It does not change the scientific boundary representation.

## Frozen scientific/numerical inputs retained from v0.1

Retain exactly:

- physical and record c3 coefficient formulas from the closed c3 derivation;
- NumPy `default_rng(seed=2026082908)`;
- exactly 256 fresh base tuples generated exactly as v0.1;
- fixed `logspace(-3,3,96)` frequency probes;
- two-sided root probes at relative offset `1e-7` around every finite nonnegative root;
- coefficient-degeneracy tolerance `1e-12`;
- boundary sign tolerance `1e-10`;
- determinant comparison tolerance `2e-10`;
- endpoint equality tolerance `2e-10`.

No tolerance is relaxed.

## High-precision oracle

Use `mpmath==1.3.0` with decimal precision `mp.dps=80`.

For every v0.1 non-boundary fresh probe:

1. convert the frozen binary64-generated base parameters and probe frequency to high-precision numbers using their round-trip decimal representations;
2. independently reconstruct the physical and record 2x2 active matrices `A` and shared multiplicative-noise matrix `B`;
3. independently construct the 3x3 symmetric second-moment generator by applying
   `A P + P A^T + B P B^T`
   to the three symmetric basis matrices;
4. calculate `c3_det_hp=-det(G)` using high-precision arithmetic;
5. independently evaluate the already-frozen c3 quadratic in high precision;
6. compare them using the unchanged relative-or-absolute `2e-10` gate;
7. compare their signs using the same registered boundary convention.

The exact quadratic is not inserted into the matrix or determinant construction.

## Binary64 failure fingerprint

In parallel, reproduce the original v0.1 binary64 determinant diagnostic using NumPy 2.1.3. Record:

- count of determinant-comparison failures under `2e-10`;
- maximum binary64 comparison error;
- count of sign disagreements.

The expected historical fingerprint is 16 comparison failures and 0 sign disagreements. This fingerprint is diagnostic lineage, not the v0.2 pass criterion. A mismatch must be reported but does not permit altering the high-precision gate.

## Frozen gates

- **P0 lineage:** required v0.1 failure report and closed c3 derivation result exist and source identities are captured before execution.
- **P1 panel identity:** regenerate exactly 256 base tuples from seed `2026082908`, with the same fixed and root-adjacent probe construction as v0.1.
- **P2 high-precision determinant equality:** every non-boundary physical and record high-precision determinant agrees with the independently evaluated exact quadratic to relative-or-absolute error `<=2e-10`.
- **P3 high-precision sign preservation:** zero physical or record sign disagreements between high-precision determinant and exact quadratic at every non-boundary probe.
- **P4 v0.1 failure localization:** every binary64 comparison failure must occur at a registered root-adjacent probe, and binary64 sign disagreement count must remain zero. This does not require the exact historical count of 16 to PASS, but the observed count is preserved.
- **P5 precision separation:** high-precision maximum comparison error must be strictly smaller than binary64 maximum comparison error whenever binary64 produces at least one comparison failure.

Overall status is `PASS_D3_HIGH_PRECISION_REMEDIATION` only if P0-P5 pass.

Any high-precision disagreement is `HIGH_PRECISION_D3_FAILURE` and must be preserved. It may not be repaired by relaxing tolerances.

## Composite interpretation

A v0.2 PASS does not erase v0.1 FAIL. It establishes that the v0.1 D3 failure was attributable to its binary64 determinant oracle at deliberately near-singular probes, while the underlying independently reconstructed determinant identity survives the original frozen gate in high precision.

The c3 displacement representation may be treated as numerically closed only by citing both:

1. v0.1 structural gates D0/D1/D2/D4/D5 PASS plus permanent D3 FAIL, and
2. v0.2 independent high-precision D3 remediation PASS.

No stochastic scalar, localization/collapse claim, or universal c3 dominance is licensed.
