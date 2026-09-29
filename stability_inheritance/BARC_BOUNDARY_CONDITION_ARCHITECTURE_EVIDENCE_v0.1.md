# BARC Boundary-Condition Architecture Evidence v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**System:** Box Assembly with Removable Component (BARC)
**Evidence class:** PUBLISHED NATIVE EXPERIMENTAL / PRIOR-ART ARCHITECTURE EVIDENCE
**Architecture evidence role:** ARCHITECTURE_SUPPORTING_NATIVE_BOUNDARY_CONDITION
**Raw-data reanalysis:** NOT REQUIRED FOR THIS EVIDENCE CLASS
**Empirical Stability Inheritance claim:** NONE

## Purpose

Record what the published BARC program establishes as a native structural-dynamics piece of the Stability Architecture without claiming ownership of the mechanism and without conflating literature evidence with a new raw-data analysis.

BARC was created specifically to investigate how boundary conditions and fixture dynamics alter the response of a removable component when it is moved between its next-level assembly and laboratory test configurations.

## Source-derived evidence

### 1. The component's realized dynamics depend on its embedding boundary condition

The Dynamic Substructuring Focus Group's BARC page states that the challenge was developed to design a component test setup that reproduces exposure experienced in the full assembly.

Source:
- Dynamic Substructuring Focus Group, BARC public data index, https://wiki.sem.org/wiki/BARC

Rohe et al. compared the same Removable Component in three configurations:
- a truth configuration attached to the next-level Box assembly;
- a traditional rigid plate fixture;
- flexible fixtures designed to better represent the compliance of the component's assembly.

Their declared comparison target was the component response in the truth assembly.

Source:
- D. P. Rohe et al., "Comparison of Multi-Axis Testing of the BARC Structure with Varying Boundary Conditions," DOI 10.1007/978-3-030-12676-6_17.

### 2. Boundary-condition changes alter modal representation

Manring, Mann, and Schultze explicitly compare BARC modal properties between free-free and fixed-base/shaker-table configurations, including mode shapes, damping, natural frequencies, and reciprocity, to characterize impedance mismatch between configurations.

Source:
- L. H. Manring, B. P. Mann, J. F. Schultze, "Modal Analysis of the Box Assembly with Removable Component in Two Configurations," DOI 10.1007/978-3-030-47709-7_25.

This establishes that the component/assembly modal description is configuration-dependent rather than an immutable property that can be moved between embeddings without qualification.

### 3. Assembly and test realization are variable even within the same nominal BARC design

Rohe et al.'s testing summary reports inter-test/article variability in modal parameters and investigates nonlinearities across multiple BARC structures and participating laboratories.

Source:
- D. P. Rohe et al., "Testing Summary for the Box Assembly with Removable Component Structure," DOI 10.1007/978-3-030-12676-6_16.

The relevant architecture point is not that variability is undesirable. It is that assembly procedure, fixture realization, joint state, and test boundary are part of the realized dynamic object.

### 4. Attachment geometry and contact interface materially condition response

A later numerical/experimental BARC study varied the distance between bolted fixture connections and examined interface/contact effects. The study reports strong influence of contact interference and recommends the widest tested connection geometry for reducing nonlinearities and improving data quality.

Source:
- "Effects of test fixture connections and interference of the BARC structure on its dynamical responses," International Journal of Mechanical Sciences 221 (2022) 107186, DOI 10.1016/j.ijmecsci.2022.107186.

This further narrows the native relation from generic "environment matters" to concrete interface and constraint geometry.

### 5. Fixture design can be treated as architecture reconstruction rather than nuisance suppression

More recent BARC fixture-optimization work defines success by reproducing the component response in its operational/target system and compares rigid, N+1, and optimized fixtures. The stated objective is to match the target system response across the component, with stress-field comparisons used as an additional test.

Source:
- "Optimization of an Impedance-Matched Test Fixture with the Modal Projection Error," Experimental Techniques, DOI 10.1007/s40799-025-00794-5.

This is important because native engineering practice itself treats the boundary/interface dynamics as something that must sometimes be reconstructed to recover the target behavior, rather than removed by making a fixture maximally rigid.

## Stability Architecture interpretation

The published BARC evidence supports a relation of the form:

component native structure
+ attachment/interface state
+ next-level boundary impedance
+ excitation/test configuration
-> realized component response and modal organization.

This is an architecture relation, not a new force and not a scalar law.

The same nominal component can exhibit different realized dynamic behavior when the embedding boundary changes. Conversely, a laboratory setup can be designed to better reproduce the target response by reproducing relevant boundary dynamics.

The correct evidence classification is:

**ARCHITECTURE_SUPPORTING_NATIVE_BOUNDARY_CONDITION**

The novelty classification remains native/prior-art. Stability Inheritance does not own the fact that boundary conditions affect dynamics.

## Relation to active project notation

### chi

No project scalar chi is admitted from these publications by default. Individual modal damping quantities may be native scalar descriptors, but no cross-configuration scalar compression is assumed sufficient.

### Chi

Modal/vector structure is directly relevant because BARC publications compare natural frequencies, damping, mode shapes, FRFs, and multi-axis response across configurations. Native modal objects are not automatically renamed project capital Chi without an explicit mapping.

### Chi_arc

The BARC program is strong evidence that system-level realized organization depends on embedding constraints, but no unique project Chi_arc object is reconstructed from the literature evidence alone.

Current status:

**ARCHITECTURE_LEVEL_BOUNDARY_EVIDENCE_PRESENT / CHI_ARC_NOT_UNIQUELY_IDENTIFIED**

## Function Map additions

- EMBEDDING_BOUNDARY_CONDITIONS_REALIZE_DIFFERENT_COMPONENT_DYNAMICS
- BOUNDARY_IMPEDANCE_CAN_BE_ENGINEERED_TO_REPRODUCE_TARGET_RESPONSE
- MODAL_ORGANIZATION_IS_CONFIGURATION_DEPENDENT
- INTERFACE_GEOMETRY_CONDITIONS_REALIZED_RESPONSE
- NATIVE_ENGINEERING_CAN_RECONSTRUCT_TARGET_BOUNDARY_ARCHITECTURE

## Limit Map additions

- RIGID_FIXTURE_IS_NOT_A_UNIVERSAL_NEUTRAL_REFERENCE
- COMPONENT_ONLY_CHARACTERIZATION_DOES_NOT_UNIQUELY_DETERMINE_EMBEDDED_RESPONSE
- NOMINALLY_IDENTICAL_ASSEMBLIES_CAN_SHOW MODAL_VARIABILITY
- BOUNDARY_AND_JOINT_REALIZATION_MUST_BE_DECLARED FOR TRANSPORT
- FIXTURE_SUPPRESSION_OF_DYNAMICS_CAN MISREPRESENT SERVICE_ENVIRONMENT

## Relation to existing measured SI evidence

BARC adds a piece that differs from the current F-16 and pyFBS lanes:

- F-16: local nonlinear interface/operating regime conditions global response organization;
- pyFBS: measured component/assembly objects are related through an explicit native hierarchical transformation;
- BARC: changing the embedding boundary of the same component changes its realized dynamics, and engineering the boundary can recover target-like response.

Together these strengthen a relational architecture in which component properties, interface/coupling, boundary impedance, operating context, and representation jointly determine realized behavior.

## Scientific ceiling

This evidence does not establish:
- a universal inheritance law;
- SI-specific added value;
- a physical scalar chi;
- a unique Chi_arc object;
- that every environment is a substrate;
- that boundary matching alone is sufficient for all stability tasks.

It does establish that boundary/interface architecture is a native, experimentally consequential constituent that the broader Stability Architecture reconstruction must be capable of representing or explicitly refusing.
