# SI Continuity Failure — DESI v0.1d result-serialization literal

**Date:** 2026-10-01  
**Governance:** SymC GOM v1.0 + mandatory Continuity Hardening Addendum  
**Classification:** CONTINUITY_FAILURE / IMPLEMENTATION_SERIALIZATION  
**Scientific authority change:** NONE

## Failure

The convergence-qualified DESI cross-block v0.1d run executed the heavy scientific computation for approximately 3064 s and then terminated while constructing the final Python result dictionary.

Exception:

    NameError: name 'null' is not defined

The invalid token occurred in metadata field:

    "penalty": null

This was introduced when JSON-style metadata was inserted into Python source. Python requires None.

## Scientific impact

The error occurred after the fold computations, at final result construction. Because the process terminated before the output JSON was written, no convergence-qualified machine-readable result was persisted.

Therefore:
- no scientific disposition from v0.1d is admitted;
- no metric is reconstructed from memory or guessed;
- no thresholds or frozen decision rules change;
- the prior provisional v0.1c result remains preserved but numerically unqualified.

## Mechanical repair

Create v0.1e from the exact v0.1d implementation with only:
- "penalty": null -> "penalty": None;
- protocol label noting the mechanical serialization repair.

No source, row, feature, residualization, interaction, control, split, solver, tolerance, weighting, decision rule, or interpretation changes are authorized.

Repair commit:
0ffc14222153c78650413c913faeb7645544dc18

## Recovery

1. Download the commit-pinned v0.1e implementation to Popstop.
2. Syntax-compile before execution.
3. Execute against the same eight SHA-256 verified DESI chains.
4. Apply the pre-frozen convergence-validity audit unchanged.
5. If all required fits converge, persist result and proceed to the already-frozen three-result adjudication.
6. If any required fit reaches the 2000-iteration ceiling, stop at MECHANICAL_NUMERICAL_CONVERGENCE_BLOCK.
