# DESI Cross-Block Relational v0.1e Convergence Audit Result v0.1

**Date:** 2026-10-01  
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum  
**Parent protocol:** `stability_inheritance/DESI_CROSS_BLOCK_CONVERGENCE_VALIDITY_AUDIT_v0.1.md`  
**Frozen scientific design:** unchanged from DESI cross-block v0.1c  
**Execution host:** Popstop  
**Status:** COMPLETE / MECHANICAL_NUMERICAL_CONVERGENCE_BLOCK / NO SCIENTIFIC PROMOTION

## Receiving-side continuity finding

The DM/DE-to-SI transfer worksheet recorded that transfer-time inspection did not find a checked v0.1e result in the Stability Inheritance tree and therefore treated the prior Popstop PID as stale pending verification.

Receiving-side review located the completed machine-readable result at:

`cosmology_desi/results/desi_cross_block_relational_v0_1e.json`

Local result SHA-256:

`67fac38688da46e1f41a27fc8abc1c82d910a61951eb554419374ef59472fe68`

The prior launcher/session identity is no longer live. The computation is complete; this file is the durable result source discovered after transfer.

## Frozen numerical configuration

- objective: unpenalized logistic regression;
- solver: `lbfgs`;
- tolerance: (10^{-8});
- maximum iterations: 2000;
- rows: 2,064,946;
- interaction features: 49;
- pairing-destroyed control: within-model/source-chain circular shift (max(1,n/3));
- source pair, folds, weighting, residualization, features, interactions, and controls: unchanged;
- equivalence guard: 1024 rows, exact allclose = true, maximum absolute difference = 0.0.

## Observed metrics

Additive representation (A):

- mean log loss = 0.6629694083;
- mean AUC = 0.6478719357;
- fold iterations = 226, 263, 192, 180;
- convergence warnings = none.

Interaction representation (X):

- mean log loss = 0.6558912729;
- mean AUC = 0.6615900211;
- (X) beat (A) in all four folds;
- every fold reached 2000 iterations;
- every fold emitted a convergence warning.

Pairing-destroyed interaction control (X_{\rm shift}):

- mean log loss = 0.6631892258;
- mean AUC = 0.6472462638;
- (X) beat (X_{\rm shift}) in all four folds;
- every fold reached 2000 iterations;
- every fold emitted a convergence warning.

The raw decision logic therefore still labels the metric pattern `CROSS_BLOCK_RELATIONSHIP_ADDS`, but the required numerical validity condition was not met.

## Protocol adjudication

Rule 6 of the frozen convergence audit requires every recovery fit to terminate without `ConvergenceWarning` before the 2000-iteration ceiling.

Rule 7 states that if any required fit reaches the ceiling, execution must stop as:

`MECHANICAL_NUMERICAL_CONVERGENCE_BLOCK`

That rule applies here.

### Final disposition

**MECHANICAL_NUMERICAL_CONVERGENCE_BLOCK**

The raw relationship-adds pattern is retained as **provisional numerical evidence only**. It is not a convergence-qualified DESI Result 3 and it may not enter the frozen three-result SI adjudication as a promoted result.

This is an implementation/numerical-validity block, not a scientific falsification of the cross-block hypothesis and not evidence for a physical (Chi), (Chi_{\rm arc}), DM/DE mechanism, or cosmological Stability Inheritance carrier.

## Next gate

No solver, regularization, tolerance, feature, scaling, source, split, or scientific-design change is authorized by this result.

Any further DESI Result 3 rescue requires a new explicit prospective numerical-method gate. Until such a gate is frozen, the correct state is **NEED_MORE_INFO / SCIENTIFIC_GATE** and the three-result adjudication remains unexecuted.

Broader Stability Inheritance U0/U1/U2 work may continue outside this blocked DESI numerical sublane.
