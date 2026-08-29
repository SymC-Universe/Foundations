# Active-quotient scalar admissibility v0.1 pre-execution amendment a

**Status:** FROZEN BEFORE FIRST EXECUTION

This amendment was added after adversarial review of the frozen v0.1 preregistration but **before any execution of v0.1 code**. No active-quotient audit result had been observed.

The standing scientific control requires explicit refusal when a nontrivial conditioning-dark factor is not identifiable. The base preregistration described dark-factor identifiability as an admissibility requirement but did not include a dedicated refusal fixture for the case `dim(D)=0`. This amendment closes that pre-execution coverage gap without changing any registered quantum fixture, tolerance, scalar formula, positive gate, or interpretation.

## Added refusal control RQ8: no identifiable nontrivial dark factor

Use the real stable 3x3 control

`A=[[-0.45,0.70,0.10],[-0.60,-0.55,0.40],[-0.20,-0.50,-0.75]]`

with one measurement functional

`V=(1,0,0)^T`

and update column

`U=(0.12,-0.08,0.15)^T`.

The observability stack `[V^T; V^T A; V^T A^2]` must have full rank under the already-frozen SVD tolerance, so the maximal conditioning-dark subspace has dimension zero.

Required result:

`REFUSE_NONIDENTIFIABLE_DARK_FACTOR`.

No quotient scalar may be produced.

## Amended A6 refusal gate

A6 now requires **RQ1-RQ8** to return exactly their preregistered refusal labels. No fallback scalar is permitted.

All other v0.1 preregistration text remains unchanged and controlling.
