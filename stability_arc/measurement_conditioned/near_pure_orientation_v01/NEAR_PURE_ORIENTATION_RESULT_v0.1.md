# Near-pure orientation admissibility test v0.1 result

Status: `PASS_H9N / PASS_H9P / PASS_H9F`

Canonical run: `33267026845`
Execution commit: `a58dd2374cddf98552d2f51aa169ecaad8bd325a`
Artifact: `9718950210`
Artifact ZIP SHA-256: `320cb803afe7768eccde1613ba4a26f3dfad9902219413b4c24067f40d607a21`

## Frozen fresh design

Seed `2026082914` generated exactly 1,000,000 fresh near-pure states in the unchanged H8 highest radial shell `0.995 <= r < 0.9999`:

- 500000 with `x*z<0` (NEG);
- 500000 with `x*z>0` (POS).

Stage A used only the already-derived exact physical c1 and separate physical/record c3 formulas. It froze eligible cases and their digest before constructing any A, B, G, c2, final Hurwitz margin, eigenvalue, or full class.

Unchanged thresholds: `C1_TOL=1e-8`, `MAP_TOL=1e-8`, `RH_TOL=1e-9`, reconstruction tolerance `2e-10`.

## Result

All N0-N5 audit/reconstruction gates passed. Maximum c1/c3 reconstruction error was `1.080649077427649e-13`.

Stage-A eligible counts:

- NEG: `33`;
- POS: `0`.

Registered outcomes:

- **H9N negative-orientation existence: PASS.** 33 >= the frozen 20-case minimum.
- **H9P positive-orientation absence: PASS.** 0 eligible cases in 500000 matched POS draws.
- **H9F c1+c3 full-class sufficiency: PASS.** All `33/33` frozen eligible cases were complete physical STABLE -> same-record UNSTABLE crossings.

There were:

- 0 H9F counterexamples;
- 0 physical m2 blockers;
- 0 physical final-Hurwitz blockers;
- 0 boundary cases.

## Licensed bounded conclusion

Within the registered near-pure state shell and broad rate/frequency distributions, the c1+c3 admissible destabilizing class was prospectively observed only for `x*z<0`, and every frozen admissible case was a complete mean-square STABLE -> UNSTABLE crossing.

This is bounded evidence, not a theorem that `x*z<0` is universally necessary, not a radius-only law, and not a stochastic scalar reduction.

The next justified step is outcome-free algebra: derive the exact dependence of physical and record c3 on the orientation product `u=x*z`, identify the corresponding channel-specific sign thresholds/half-lines at fixed magnitudes, and test that decomposition on fresh controls before transfer to another measurement/dissipation geometry.
