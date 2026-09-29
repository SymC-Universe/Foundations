# Stability Inheritance P0-N/A0 Later-Literature Addendum - Transferable Joint Interface

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Parent closure:** stability_inheritance/P0N_A0_CLOSURE_v1.0.md
**Rule:** later-literature collision remains active after P0-N closure
**Status:** CLAIM-CEILING NARROWING / NO REOPENING OF CLOSED EVIDENCE

## New collision

Vrtac et al. (2025), DOI 10.1016/j.ymssp.2025.112487, demonstrate native FBS isolation of riveted-joint impedance and explicitly state that the joint to be identified need not originate from the same surrounding assembly as the reference joints, subject to local material/geometry similarity.

Associated public datasets 10.17632/sgmxhdc599.1 and 10.17632/dy66vm8t95.1 contain two assembly configurations, ARB and A'RB', and measured joint-related responses across known rivet-squeezing forces.

## Consequence for residual novelty

The existing P0-N classification remains:

- NEW_INTEGRATION primary;
- NEW_DISCRIMINATING_TEST secondary;
- NEW_BOUNDARY_TEST secondary.

But the residual is narrowed further.

The following are now explicitly prior art / not novel:

- generic isolation of an interface dynamic model from an assembly;
- generic transfer of an isolated interface/joint representation across a different assembly;
- generic claim that a local carrier can retain comparable dynamic identity after host change;
- FBS joint-impedance transfer as an SI-specific mechanism.

The residual program question is therefore not "can a carrier property transfer across hosts?"

It is:

> Across admitted native representations, when is a stability-relevant source/interface relation preserved, transformed, reorganized, rendered nonidentifiable, or invalid under embedding, host change, operating regime, and history, and does the integrated qualification architecture add a scientific decision beyond the strongest native framework?

## Impact on current measured program

The riveted-joint result is positive architecture evidence and negative novelty evidence simultaneously.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_TRANSFERABLE_INTERFACE_OBJECT.

Novelty role:
NATIVE_PRIOR_ART / GENERIC_CROSS_HOST_TRANSFER_CLAIM_REFUSED.

No existing measured result is reclassified upward or downward. No P1 object exists to alter.

## Next implication

Future computational/empirical tests should prioritize transfer failures, conditional equivalence boundaries, cross-representation relations, and architecture-level decisions rather than demonstrations that a native joint/interface model is transferable under conditions already established in FBS literature.
