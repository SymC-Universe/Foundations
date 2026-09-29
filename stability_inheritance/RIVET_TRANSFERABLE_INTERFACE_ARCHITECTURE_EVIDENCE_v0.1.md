# Transferable Riveted-Joint Architecture Evidence and Prior-Art Collision v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Evidence class:** PUBLISHED NATIVE EXPERIMENTAL / LATER-LITERATURE A0 COLLISION
**Primary source:** T. Vrtac, M. Kodric, M. Pogacar, G. Cepon, "Dynamic substructuring-based identification of the rivet-squeezing force," Mechanical Systems and Signal Processing 229 (2025) 112487.
**DOI:** 10.1016/j.ymssp.2025.112487
**Supporting public datasets:** 10.17632/sgmxhdc599.1 and 10.17632/dy66vm8t95.1
**Architecture evidence role:** ARCHITECTURE_SUPPORTING_NATIVE_TRANSFERABLE_INTERFACE_OBJECT
**Novelty role:** PRIOR_ART_COLLISION_FOR_GENERIC_CROSS_HOST_INTERFACE_TRANSFER
**Empirical Stability Inheritance claim:** NONE

## Source-derived evidence

The published approach uses Frequency-Based Substructuring to decouple the dynamic impedance of a riveted joint from the surrounding structural assembly.

A reference library of isolated joint impedances is associated with known rivet-squeezing forces. For a structure of interest, the joint impedance is independently decoupled from its current assembly and compared with the reference library.

The paper explicitly states that the joint of interest does not need to originate from the same assembly as the reference-dataset joints. Transfer is conditioned on sufficient similarity in material and geometry near the joint.

The paper demonstrates classification of rivet-squeezing force on validation samples and describes the calibrated joint dynamic model as transferable.

The later public datasets make the cross-assembly structure explicit:
- assemblies ARB and A'RB' are distinct configurations;
- the same riveted-joint property, squeezing force, is represented across both configurations;
- the larger dataset includes 120 ARB samples and 23 A'RB' samples over squeezing forces approximately 4.94-8.62 kN;
- the datasets are organized so that FBS can isolate joint dynamic models from each assembly.

## Stability Architecture interpretation

This is strong native evidence that a declared interface object can sometimes be separated from its host and retain useful identity across a changed assembly.

An evidence-compatible relation is:

host A + joint J + host B
-> native decoupling
-> J_hat

and

different host A' + joint J' + host B'
-> native decoupling
-> J'_hat,

where J_hat and J'_hat can be compared in a host-reduced representation when local joint material/geometry assumptions are sufficiently compatible.

The correct architecture evidence role is:

**ARCHITECTURE_SUPPORTING_NATIVE_TRANSFERABLE_INTERFACE_OBJECT**

This is a more specific constituent than generic "environment matters" because native engineering deliberately constructs a representation intended to remove surrounding-host influence.

## Prior-art collision

This source removes a broad possible SI novelty claim:

> "A stability-relevant carrier/interface representation can be isolated from one host and compared or transferred across another host."

That concept is already demonstrated natively for riveted-joint dynamic impedances.

Therefore the following novelty claims are refused:

- generic cross-host transferability of an isolated interface model;
- generic statement that carrier properties can survive a change in surrounding assembly;
- generic use of FBS-decoupled joint impedance as an SI invention;
- generic claim that interface identity can be separated from host dynamics.

Any residual SI contribution must be narrower, for example:

- a qualification architecture deciding when such transfer is scientifically admissible;
- explicit relation among scalar, modal/vector, architecture-level, and history representations;
- cross-domain Function/Limit mapping of preservation, transformation, reorganization, and refusal;
- prospective tests where native transfer conditions themselves break or require additional architecture;
- evidence that a declared relation adds a nonredundant scientific decision beyond the strongest native framework.

## Boundary conditions on the native transfer

The native paper does not claim unconstrained universality.

Transfer is limited by similarity of material and geometry near the joint. Later joint-identification literature also emphasizes residual dynamics, interface correspondence, conditioning, and experimental errors as constraints.

Therefore the architecture evidence is conditional:

**TRANSFERABLE_INTERFACE_OBJECT_WHEN_NATIVE_LOCAL_EQUIVALENCE_CONDITIONS_HOLD**

not:

**INTERFACE_OBJECT_IS_HOST_INDEPENDENT_UNIVERSALLY**.

## Relation to current SI measured evidence

F-16:
- interface regime conditions system response.

pyFBS:
- component/assembly relation is operational through native hierarchical transformation, but conditioning limits recovery.

BARC:
- embedding boundary changes realized component dynamics.

BRB:
- modal skeleton persists with fine amplitude-conditioned geometry;
- local chi tracks but is redundant with amplitude for modal prediction;
- interface wear stores history over longer time scales.

Riveted-joint transfer:
- an interface object can be deliberately isolated and transferred across host configurations under native equivalence constraints.

Together these pieces suggest that "inheritance" cannot simply mean persistence of a component or interface property under embedding. Native structural dynamics already contains examples of such persistence and transfer.

The research target therefore remains the broader qualification architecture: which object persists, under what equivalence class, which representation is needed, what changes under embedding/history, and when transfer must be refused.

## Project notation

chi:
- not inferred from this paper by default.

Chi:
- native joint impedance is a multivariate dynamic object and may contribute to a modal/vector representation, but is not automatically renamed project Chi.

Chi_arc:
- not uniquely identified.

Transfer relation:
- directly supported as a native host-reduced interface relation.

## Function Map additions

- NATIVE_INTERFACE_OBJECT_CAN_BE_HOST_REDUCED
- JOINT_DYNAMIC_PROPERTIES_CAN_TRANSFER_ACROSS_DISTINCT_ASSEMBLIES_UNDER_LOCAL_EQUIVALENCE
- HOST_INFLUENCE_CAN_BE PARTIALLY_REMOVED_BY_NATIVE_DECOUPLING
- LOCAL_MATERIAL_GEOMETRY DEFINES_TRANSFER_EQUIVALENCE_CLASS

## Limit Map additions

- CROSS_HOST_TRANSFER_IS_NOT_SI_NOVELTY_BY_ITSELF
- TRANSFERABILITY_IS_CONDITIONAL_NOT_UNIVERSAL
- INTERFACE_REPRESENTATION_DEPENDS_ON_NATIVE_DECOUPLING_VALIDITY
- LOCAL_GEOMETRY_MATERIAL_MISMATCH CAN_BREAK_TRANSFER
