# c3 displacement-map full-class validation v0.1 result

Status: `FAIL_C3_MAP_FULL_CLASS_H6`

Canonical run: `33266630910`
Execution commit: `569cbc22e68c1c40a662f1ec6f44997d6de2e1ad`
Artifact: `9718837319`
Artifact ZIP SHA-256: `8d91e981377264dc51d0dd517e09e48d0741903325e1fcd8f8b56016fd250d7e`

## Prospective design

A fresh seed `2026082909` generated exactly 250000 broad measured-qubit candidates. Stage A used only the frozen exact c3 quadratics. It selected and hashed the first 512 robust `I_destab` and first 512 robust `I_stab` cases before any 2x2 drift/noise matrix, 3x3 second-moment generator, eigenvalue, or non-c3 Routh-Hurwitz margin was constructed.

Available Stage-A counts were:

- `I_destab`: 4402;
- `I_stab`: 45092.

Direct-generator c3 reconstruction remained clean, with maximum relative-or-absolute error `6.618944047620114e-13`, below the frozen `2e-10` gate. No selected case was boundary-classed.

## H6 result

The strong registered sufficiency claim failed.

- `I_destab` full-class precision: `0/512 = 0.0`;
- `I_stab` full-class precision: `512/512 = 1.0`;
- total robust counterexamples: `512`;
- boundary cases: `0`.

Every `I_destab` counterexample was already physically non-stable through the physical `m1` margin. Failure decomposition across the 512 cases:

- physical `m1` blocker: 512;
- physical `m2` blocker: 506;
- physical `m3` blocker: 0, as required by `I_destab`;
- physical `mh` blocker: 6.

The `I_stab` side had no recorded blocker in the 512-case frozen panel.

## Scientific interpretation

The exact c3 displacement map remains valid as a channel-specific boundary coordinate, but **c3 sign displacement alone is not sufficient for full mean-square class displacement** across the broad fresh sampling frame.

The failure is strongly structured rather than random: every false `I_destab` prediction violated the physical first Hurwitz margin before same-record conditioning was evaluated. This identifies the physical `c1` gate as the smallest common missing admissibility coordinate in the failed panel.

The 512/512 `I_stab` result is a bounded prospective sub-result from this panel only. It is not promoted to a theorem or universal one-sided rule.

No threshold is changed and no counterexample is removed.
