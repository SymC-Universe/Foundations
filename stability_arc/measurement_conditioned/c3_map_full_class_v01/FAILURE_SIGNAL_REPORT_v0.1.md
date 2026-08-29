# H6 failure-signal report v0.1

Classification: `SCIENTIFIC / MODEL-BOUNDARY / SUFFICIENCY_FAIL`

The run itself was mechanically and numerically healthy. V0-V4 and V6 passed. H6 failed only because V5 found 512 robust full-class counterexamples.

## Last valid checkpoint

The exact separate c3 surfaces, displacement sign sets, Stage-A freeze, and direct c3 reconstruction remain valid. The failure begins only at the attempted promotion from a c3 sign-displacement label to complete four-gate mean-square class displacement.

## Preserved signal

All 512 failed predictions came from `I_destab`. Every one had physical `m1 <= RH_TOL`; 506 also had physical `m2 <= RH_TOL`, and 6 had physical `mh <= RH_TOL`. None failed physical `m3`, because `I_destab` requires physical c3 positive by construction.

The opposite map class, `I_stab`, produced 512/512 correct full-class crossings in this frozen panel. That asymmetry is preserved as a bounded observation and is not generalized.

## What the failure excludes

This run excludes the claim that c3 sign displacement alone is a sufficient full mean-square class coordinate across the registered broad measured-qubit sampling frame.

It does not invalidate the c3 boundary geometry itself.

## Smallest justified next question

Derive the exact channel-specific first Hurwitz coefficient c1 directly from the active stochastic quotient, independently verify `c1=-tr(G)`, and then freeze a new fresh test of the smallest post-H6 correction:

`I_destab` plus robust physical `c1>0`.

Do not add c2 or the final Hurwitz determinant margin unless the fresh c1-corrected test demonstrates they are still required. This preserves the failure as information rather than making the predictor tautological.
