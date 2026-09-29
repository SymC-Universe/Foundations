# External Measured Benchmark Synthesis v0.7

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Status:** P0-Q CROSS-BENCHMARK SYNTHESIS / NOT A CONFIRMATORY CLAIM  
**Benchmarks:** Silverbox, Fine Steering Mirror, Wiener-Hammerstein 2009, F-16 GVT, pyFBS measured lab testbench, BARC published experimental program, Brake-Reuss Beam  
**Empirical Stability Inheritance claim:** NONE

## Purpose

Compare the current public measured-data qualification results without treating native nonlinear modeling, operating-regime dependence, or better predictive fit as Stability Inheritance.

The synthesis asks only:

1. what representation failures recur across measured systems;
2. whether scalar, modal/state, and architecture-level labels are actually licensed;
3. what the strongest native explanation already provides;
4. which unresolved SI question remains after the native explanation is admitted.

## Benchmark matrix

| Benchmark | Native system issue | Frozen/available comparison | Measured result | chi status | Chi status | Chi_arc status | Native explanation | SI consequence |
|---|---|---|---|---|---|---|---|---|
| Silverbox | Duffing-like cubic feedback | linear ARX-2 vs cubic NARX-2 on reserved measured segments | nonlinear model lower one-step and free-run error on both reserved segments | physical chi REFUSED; model-local chi candidate diagnostic only | linear state representation locally useful but task-limited | no independent Chi_arc inheritance object constructed | native nonlinear oscillator/system-identification structure | representation adequacy differs from local fit; no inheritance claim |
| Fine Steering Mirror | piezo hysteresis / operating-amplitude dependence | published amplitude-specific linear BLAs, pooled linear BLA, shared nonlinear NL-LFR | shared nonlinear NL-LFR beats every linear baseline at 100/200/300 mV; pooled vs amplitude-specific linear ordering is mixed | chi NOT ADMITTED | linear state representation regime/task dependent | no independent Chi_arc inheritance object constructed | native nonlinear hysteretic model transports across amplitudes | representation class can matter more than local specialization; no inheritance claim |
| Wiener-Hammerstein 2009 | static nonlinearity between LTI blocks | frozen linear ARX-8 vs polynomial NARX-8 on official held-out test | nonlinear M2 improves one-step RMSE ~17.6% and free-run RMSE ~45.0% without divergence | chi NOT ADMITTED | linear autoregressive representation highly accurate locally but less adequate recursively | no independent Chi_arc inheritance object constructed | native Wiener-Hammerstein/nonlinear system-identification structure | local accuracy does not imply recursive architectural adequacy; no inheritance claim |
| F-16 GVT | clearance/friction nonlinearity at payload mounting interface | frozen Level-1 invariant FRF vs force-amplitude-conditioned interpolation on reserved FullMSine levels 2/4/6 in 6.5-8.2 Hz torsional band | amplitude-conditioned representation lower error on all three reserved levels; error ratios 0.533, 0.117, 0.0335 | chi NOT ADMITTED | native multi-output FRF organization is amplitude-conditioned | no unique Chi_arc object claimed, but system-level organization is directly supported | native nonlinear structural/interface dynamics | embedded interface regime conditions realized system response; architecture-supporting native evidence |
| pyFBS lab testbench | measured component/assembly substructuring | B-derived current SVT + LM-FBS decoupling of AB-B against independently measured A | E_DEC 1.203 vs E_BASE 1.253; 4.01% global improvement; DEC better at 80.25% of positive-frequency bins | chi NOT ADMITTED | native component/assembly FRF and reduced-coordinate structure | no unique Chi_arc object; explicit hierarchical transformation is operational | native SVT / LM-FBS dynamic substructuring | direct architecture-supporting native hierarchical-transformation evidence; novelty remains native-equivalent |
| BARC published experimental program | same removable component under different next-level/test boundary conditions | next-level Box truth configuration vs rigid/flexible fixtures; free-free vs fixed-base; attachment-geometry studies | published studies show boundary/fixture realization changes modal and dynamic response and motivates impedance-matched fixtures | chi NOT ADMITTED | modal/FRF response is configuration dependent | no unique Chi_arc coordinate; boundary architecture is experimentally consequential | native structural dynamics / fixture impedance / joint-contact mechanics | architecture-supporting native boundary-condition evidence; raw public test-data route currently partial |
| Brake-Reuss Beam | bolted-joint nonlinear ringdown with full-field DIC | pre-frozen HIGH/LOW amplitude spatial-basis qualification with split-half repeatability | rank-1 energy >0.99994; HIGH/LOW principal angle 0.944 deg; own-amplitude basis gives ~2.7x lower held-out projection residual than opposite-amplitude basis | chi NOT ADMITTED in this test | Chi ADMITTED as repeatable native 1D modal subspace; fine geometry amplitude-conditioned | Chi_arc NOT IDENTIFIED | native jointed-structure amplitude-dependent modal geometry | first clean measured project-Chi admission; stable modal skeleton plus reproducible fine reorganization |

## Cross-benchmark Function Map

### Function F-EM1 - Local reduced representations can remain useful

The nonlinear representation benchmarks and F-16 permit useful reduced or local representations in at least some operating or prediction tasks, while pyFBS adds an explicit measured component-to-assembly transformation lane.

This supports:

**LOCAL_REPRESENTATION_USEFUL**

It does not imply:
- scalar sufficiency;
- global validity;
- inheritance;
- a unique Stability Architecture coordinate.

### Function F-EM2 - Richer native representation can transport better across the declared task

Silverbox:
- cubic nonlinear terms improve both local and recursive measured prediction.

FSM:
- one shared nonlinear representation outperforms multiple locally specialized linear models across all measured amplitudes.

WH2009:
- polynomial nonlinear autoregression improves both held-out one-step and long recursive simulation.

F-16 GVT:
- a force-amplitude-conditioned complex FRF representation built only from designated estimation levels improves held-out prediction at every reserved excitation level in the published wing-torsion band;
- the interface-adjacent relative-response proxy changes strongly across excitation level, while the effect is also visible at the excitation-point output.

This supports the general qualification statement:

> representation class must be matched to the system/task/regime rather than inferred from local fit quality alone.

This statement is native-model compatible and is not SI novelty.

## Cross-benchmark Limit Map

### Limit L-EM1 - Good one-step/local fit does not license recursive/global adequacy

The clearest measured example is WH2009:
- M1 one-step NRMSE ~0.00364;
- M1 free-run NRMSE ~0.1812.

A locally accurate linear model can therefore be operationally inadequate for the recursive task.

Silverbox shows the same direction with a smaller but material gap between linear and nonlinear free-run performance.

### Limit L-EM2 - Operating-condition specialization is not the same as architectural adequacy

FSM rejects a simplistic rule that each amplitude requires its own local linear model.

A pooled linear model can outperform an amplitude-specific linear model at 200 mV, while a shared nonlinear model outperforms all of them.

Therefore:
- operating regime matters;
- representation class matters;
- local specialization alone is not the architecture.

### Limit L-EM3 - Richer predictive model is not automatically Chi_arc

None of the four measured benchmark results independently constructs an architecture-level/conglomerate object that is separate from the predictor being scored.

Therefore the following inference is refused:

[
\text{better nonlinear model} \Rightarrow \Chi_{\mathrm{arc}}
]

A Chi_arc claim still requires an independently motivated/reconstructed system-level object under the project definition.

### Limit L-EM4 - Scalar chi is not supported program-wide by these benchmarks

- Silverbox permits only a model-local damping-ratio-like candidate from a fitted linear pole pair.
- FSM does not admit chi from the available published baseline evidence.
- WH2009 does not admit physical chi from the input/output record.

Thus the external measured benchmark set currently strengthens the case for **conditional scalar admission**, not a universal scalar axis.

## What the three benchmarks do NOT test

None of these three measured lanes establishes:

- lower-level source characterization followed by higher-level target reconstruction;
- carrier-specific inheritance;
- source-to-descendant preservation;
- causal cross-level transfer beyond native system identification;
- an independently measured Chi_arc object receiving inherited structure;
- a universal chi-to-Chi-to-Chi_arc ladder.

Therefore they qualify representation/refusal logic, not Stability Inheritance itself.

## Residual SI question after measured-data qualification

After admitting the native nonlinear explanations, the remaining discriminating question is narrower:

> When source and target representations are independently defined across an actual embedding, coupling, or lineage transition, does lower-level stability-relevant structure add a nonredundant, carrier-specific constraint on the target architecture beyond the strongest native target model?

That question remains untested by Silverbox, FSM, WH2009, and F-16 GVT.

## Current measured-data disposition

- REPRESENTATION_QUALIFICATION_TRANSPORT: SUPPORTED across four measured benchmark lanes.
- ARCHITECTURE_SUPPORTING_NATIVE: SUPPORTED directly in F-16 GVT for an embedded interface-regime/system-response relation.
- CONDITIONAL_SCALAR_ADMISSION: SUPPORTED as a governance/qualification rule.
- RICHER_MODEL_EQUALS_CHI_ARC: REFUSED.
- NONLINEAR_MODEL_SUCCESS_EQUALS_INHERITANCE: REFUSED.
- EMPIRICAL_STABILITY_INHERITANCE: NOT TESTED.
- NATIVE_MODEL_FIRST: REINFORCED.

## Next computational implication

The highest-value nonphysical next tests are those that add at least one of the missing SI gates rather than another generic nonlinear-vs-linear benchmark:

1. independent source and target representations;
2. explicit correspondence/carrier map;
3. frozen source-to-target transformation;
4. target prediction on measured data;
5. intervention or matched-condition specificity;
6. strongest native target comparator.

Public structural substructuring data such as F-16 GVT remains preferred if provenance-clean raw access becomes available.


## F-16-specific architectural contribution

F-16 differs from the other external measured lanes because the benchmark supplies both a native localized mechanism context and spatially separated responses on opposite sides of the interface plus the excitation location. The frozen FullMSine test therefore bears on the organization of response across an embedded interface rather than only on generic nonlinear model class.

The result does not prove a new causal mechanism. The benchmark authors already identify clearance and friction at the payload interface as the expected dominant nonlinearity. Its contribution to the Stability Architecture case is integrative: a local interface regime is measurably associated with broad changes in the realized response representation, and an amplitude-conditioned map learned from designated estimation levels transports to independent reserved levels.

The next useful question is whether this relation survives an independent excitation family without redesigning the analysis around the FullMSine outcome.


## pyFBS-specific contribution

The pyFBS measured lab testbench contributes something structurally different from the nonlinear model-comparison benchmarks.

Using the current official SVT metadata, the B-derived transform was qualified without downloading the A target. After the scoring protocol was frozen, LM-FBS decoupling of measured assembly AB and measured component B was compared with independently measured component A.

The native decoupling reduced the global normalized complex error from 1.25333 for the no-decoupling assembly-side baseline to 1.20313, a 4.01% improvement, and had lower per-frequency error at 80.25% of positive-frequency bins.

This is classified simultaneously as:

- **ARCHITECTURE_SUPPORTING_NATIVE_HIERARCHICAL_TRANSFORMATION** for evidence role;
- **NATIVE_FRAMEWORK_EQUIVALENT** for novelty / added-value role.

The result is not strong evidence of carrier specificity. Interface matrices are often ill-conditioned, absolute recovery error remains large, and the deterministic reduced-coordinate shuffle was only slightly worse globally and not consistently worse by frequency.

## Revised measured-data picture

Across the current measured lanes, the Stability Architecture evidence is no longer only "richer models can fit nonlinear systems better." It now includes at least three distinct empirical pieces:

1. **representation/regime adequacy:** Silverbox, FSM, and WH2009;
2. **embedded-interface regime conditioning of system response:** F-16;
3. **explicit measured component/assembly hierarchical transformation:** pyFBS.

These pieces are compatible but not interchangeable. Their common architectural content is relational: realized stability-relevant behavior depends on which representation is admitted, how components/interfaces are coupled, which operating context is active, and whether the declared transformation remains identifiable and well-conditioned.

The novelty firewall remains separate. Native theories are sufficient explanations for each measured lane individually.


## BARC-specific contribution

BARC contributes the clearest current native evidence that the embedding boundary itself is a constituent of realized dynamics.

The challenge explicitly holds the removable component conceptually fixed while changing what it is attached to. Published comparisons use the next-level Box assembly as a truth/operational configuration and compare traditional rigid and more compliant fixtures. Other BARC studies compare free-free and fixed-base modal organization and vary bolted attachment geometry/contact realization.

This is classified as:

- **ARCHITECTURE_SUPPORTING_NATIVE_BOUNDARY_CONDITION** for evidence role;
- **NATIVE_PRIOR_ART** for mechanism/novelty role.

The architectural contribution is not merely that "environment matters." It is that a component representation does not uniquely specify its embedded response unless the boundary/interface realization is also declared. Native engineering can improve target-response reproduction by designing the laboratory boundary to reproduce relevant next-level impedance rather than by suppressing all fixture dynamics.

BARC therefore complements the measured lanes already present:

1. nonlinear/regime representation adequacy: Silverbox, FSM, WH2009;
2. localized interface regime conditioning of system response: F-16;
3. explicit measured hierarchical transformation: pyFBS;
4. boundary/embedding realization of component behavior: BARC.

The raw BARC Test Data share is currently unavailable from the runner, so this entry remains published-experimental evidence rather than a new raw-data reanalysis.


## Brake-Reuss Beam contribution

The Brake-Reuss Beam contributes a different architectural piece from the existing measured lanes because it directly resolves a spatial modal/vector object using full-field DIC during a single resonance decay.

The result is neither complete modal invariance nor wholesale modal reorganization. The measured slow-mode response remains more than 99.994% rank 1 in both high- and low-amplitude strata, but the fitted high- and low-amplitude vectors differ by 0.944 degrees, a change far larger than the split-half within-stratum variation. Each amplitude-specific basis also represents its own held-out peaks substantially better than the opposite-amplitude basis.

This is classified as:

- **ARCHITECTURE_SUPPORTING_NATIVE_MODAL_REORGANIZATION** for evidence role;
- **KNOWN_NATIVE_AMPLITUDE_DEPENDENT_MODE_SHAPE** for novelty role.

For the declared ringdown task, the native one-dimensional modal subspace is sufficiently well qualified to instantiate capital Chi. This is the strongest current measured admission of the project modal/vector layer.

The architectural lesson is resolution dependent. A modal structure can be strongly preserved while still deforming reproducibly with operating state. Therefore preservation and transformation should not be treated as mutually exclusive binary categories without specifying representation resolution.

The next relation test is scalar-modal rather than another modal confirmation: determine whether a separately licensed local damping scalar chi co-varies with, predicts, or fails to capture the measured Chi deformation along the same decay. Because that question was formulated after observing the positive modal result, any such analysis is P0-D with explicit promotion debt.


## BRB scalar-modal and history extension

The BRB lane now supplies both a directly measured Chi object and an explicit post-result chi-to-Chi relation test.

The local scalar is scientifically admissible in short fixed windows because the native ringdown is extremely well approximated by an exponentially decaying single slow mode in those windows. The scalar strongly covaries with the modal deformation, but chronological held-out scoring shows that response amplitude explains the modal geometry substantially better and that adding chi to amplitude does not improve prediction.

Thus the current measured relation is:

[
	ext{operating amplitude/state}
longrightarrow
{chi_{mathrm{local}},,Chi_{mathrm{modal}}}
]

with strong covariance between the two representations, rather than evidence for a universal deterministic map

[
chi ightarrow Chi.
]

This directly supports the program rule that scalar and modal layers may be complementary views of the same evolving regime without one being a complete compression of the other.

The published 2025 BRB wear campaign adds a slower history dimension. Repeated excitation changes the physical joint interface and later dynamic behavior, establishing a native route by which past loading can be embodied in the carrier itself. That evidence is distinct from projection-memory or autoregressive closure.

Taken together, BRB now contributes:

- measured modal/vector admission;
- persistent modal skeleton plus fine state-conditioned deformation;
- local scalar-modal covariance with scalar redundancy relative to amplitude;
- published physical history storage through evolving interface wear.

All four remain native-compatible evidence and do not promote an SI-specific mechanism.


## BRB scalar-modal relation and slow-history extension

The Brake-Reuss Beam now contributes more than the original modal-geometry qualification. In the same ringdown, a locally licensed effective damping scalar chi tracks the evolving modal deformation strongly, but chronological held-out prediction shows that response amplitude explains the modal angle substantially better and that adding chi to amplitude does not improve the declared task.

This supports:

**SCALAR_TRACKING_IS_NOT_SCALAR_SUFFICIENCY**

and provides direct measured evidence that the scalar and modal layers can be complementary coordinates of an operating regime without one being a complete compression of the other.

Published long-term BRB wear experiments add a slower physical-history layer. Repeated loading changes the interface itself and changes later resonance, damping, and nonlinear response. The relevant evidence role is:

**ARCHITECTURE_SUPPORTING_NATIVE_HISTORY_INTERFACE_STATE**

This is distinct from formal projection memory because the carrier/interface is physically modified.

## Transferable riveted-joint prior-art addition

Published riveted-joint FBS work demonstrates that a host-reduced interface impedance can be compared or transferred across distinct surrounding assemblies when local material/geometry conditions are compatible.

Evidence role:

**ARCHITECTURE_SUPPORTING_NATIVE_TRANSFERABLE_INTERFACE_OBJECT**

Novelty consequence:

**GENERIC_CROSS_HOST_TRANSFER_IS_NOT_A_STABILITY_INHERITANCE_NOVELTY**

This sharpens the cross-benchmark synthesis. Native evidence now contains both sides of the architecture problem:

- embedding and boundary conditions can materially reorganize realized response;
- some local/interface representations can nevertheless be isolated and transported across hosts under qualified conditions;
- operating regime and history can alter either the realized response or the carrier state itself;
- scalar, modal, and system-level descriptions need not carry the same information.

The remaining contribution cannot be simply "parts affect wholes" or "properties can transfer." It must concern the conditions, representation choices, boundaries, and scientific decisions that determine when preservation, transformation, reorganization, or refusal is the correct interpretation.

## Current source-access boundary

The raw riveted-joint datasets are publicly described and licensed CC BY 4.0, but the current runtime did not recover a provenance-clean file-specific Mendeley download route. The raw lane is therefore SOURCE_ACCESS_HOLD. Published experimental evidence is retained without pretending a raw reanalysis occurred.

A separate long-term BRB OSF identity/layout intake is underway. Its raw response values remain uninspected.
