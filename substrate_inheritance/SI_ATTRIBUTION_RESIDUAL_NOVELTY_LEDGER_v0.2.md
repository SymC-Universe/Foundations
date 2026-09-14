# Substrate Inheritance Attribution and Residual Novelty Ledger v0.2

Date: 2026-09-12
Status: P0-D/P0-Q attribution ledger after initial targeted literature collision
Supersedes status conclusions in: `SI_ATTRIBUTION_RESIDUAL_NOVELTY_LEDGER_v0.1.md`
Source collision: `SI_LITERATURE_COLLISION_v0.1.md`
General Protocol: v0.7.4 Section 50.3

## Attribution rule

Credit follows the work. The literature collision removed several broad candidate novelty statements from consideration. The current residual question is narrower and remains provisional until a deeper nearest-prior-art review is complete.

## Adjudicated established or strongly precedent-covered components

### Modal vector correlation and tracking

Status: `ESTABLISHED_NATIVE_METHOD`.

Closest sources identified in the first collision include:
- Allemang and Brown (1982), MAC;
- Kim and Kim (2000), MAC-based mode tracking;
- Lu et al. (2020), clustered-eigenvalue/subspace mode tracking;
- Greś et al. (2021), uncertainty quantification for MAC.

SI may use or compare against these methods. It may not claim novelty for vector overlap, MAC-like correspondence, mode tracking, subspace tracking, or attaching uncertainty to a modal-correlation statistic by themselves.

### Structural condensation, dynamic substructuring, and component mode synthesis

Status: `ESTABLISHED_NATIVE_METHOD`.

Closest sources identified include:
- Guyan (1965), stiffness/mass reduction;
- Craig and Bampton (1968), coupling of substructures/component-mode synthesis;
- de Klerk, Rixen, and Voormeeren (2008), general dynamic-substructuring framework.

SI may not claim novelty for dividing a dynamical system into substructures, reducing components, reassembling them, or testing a reduced component against the full system in general.

### Input-output-oriented model reduction

Status: `ESTABLISHED_NATIVE_METHOD`.

Moore (1981) provides a major precedent linking controllability/observability and model reduction. Future FM4 comparisons must be explicit about whether the declared higher-level task is modal/spectral preservation or input-output response preservation, because different native comparators are strongest for different tasks.

### Green-function embedding and semi-infinite substrate reduction

Status: `ESTABLISHED_NATIVE_METHOD`.

Closest sources identified include:
- Lopez Sancho, Lopez Sancho, and Rubio (1985), iterative surface/bulk Green functions;
- Inglesfield and Benesh (1988), embedded surface calculation using substrate Green functions;
- Inglesfield (2001), surface embedding review/applications.

SI's embedding/self-energy calculations are inherited native mathematics. The program may test how these objects support a prospectively defined inheritance question, but may not claim the embedding principle itself as new.

### Adsorbate-substrate vibrational coupling/hybridization

Status: `ESTABLISHED_PHYSICAL_PHENOMENON`.

Closest sources identified include:
- Kern et al. (1987), experimentally observed adlayer/substrate phonon hybridization and linewidth broadening;
- Liu and Gao (2006), adsorbate-induced vibration, substrate mixing, local vibrational density and polarization analysis.

SI may not claim novelty for the observation that adsorbate and substrate vibrations hybridize or that substrate motion contributes to adsorbate modes.

### Isotope controls for vibrational coupling

Status: `ESTABLISHED_EXPERIMENTAL_METHOD`.

Hirschmugl and Williams (1995) used mixed isotopes on CO/Cu(111) and Cu(100) to distinguish chemical shifts from coupling effects. Isotopic dilution/substitution is therefore an inherited experimental control where scientifically appropriate.

### Substrate perturbation followed by adsorbate vibrational response

Status: `ESTABLISHED_EXPERIMENTAL_PHENOMENON/METHOD`.

Femtosecond substrate-heating work on CO/Cu(111) measured adsorbate vibrational response and coupling to substrate reservoirs. SI may not claim novelty merely for perturbing the substrate and observing an adsorbate response.

### Higher-order subset/Mobius source decomposition

Status: `ESTABLISHED_MATHEMATICS; SI APPLICATION STATUS UNRESOLVED`.

The exact subset decomposition used in SI-next is not treated as a mathematical invention. The residual question is whether a frozen physical intervention design makes such decomposition useful for SI without normalization or completeness artifacts.

## Candidate residual contributions still open

The following remain **candidate residual contributions**, not novelty conclusions:

1. **Prospective carrier-resolved inheritance evidence architecture**
   - independently characterize parent architecture;
   - freeze parent-child physical mapping before target inspection;
   - predict child carrier/subspace transformation prospectively;
   - test against an independently generated child object;
   - intervene on the parent;
   - defeat frequency-only, same-spectrum, generic-parent, and coupling-specificity controls;
   - preserve nonidentifiability and uncertainty rather than force a match.

2. **Fail-closed integration of influence, carrier correspondence, coupling specificity, uncertainty, refusal, and promotion semantics**
   - candidate contribution may be the evidentiary integration rather than any mathematical primitive.

3. **SI-specific hierarchical closure question**
   - not whether substructuring/model reduction exists;
   - instead whether an effective subsystem carrying a prospectively specified parent-child relationship preserves declared SI-relevant higher-level quantities after grouping/re-embedding, and where that preservation fails.

4. **Function/Limit map of inheritance-like correspondence**
   - map the ordinary supported interior and the loss/nonidentifiability boundaries under independently defined controls.

5. **A domain tool that adds measurable value over the strongest native method on a frozen task**
   - requires later standard-toolkit comparison and untouched decisive evidence.

6. **A new empirical prediction from SI that survives untouched prospective testing**
   - no such physical prediction has yet been confirmed.

## Current closest standard-toolkit candidates by task

These are comparator candidates, not yet a frozen MFR-05 selection.

| Frozen future task type | Current strongest candidate family |
| --- | --- |
| mode/carrier correspondence across parameter/system change | MAC/CMAC plus clustered-subspace mode tracking and uncertainty |
| structural subsystem reduction/reassembly | dynamic substructuring / Component Mode Synthesis |
| static structural condensation | Guyan/static condensation |
| exact frequency-domain elimination for a partitioned linear system | Schur complement / dynamic stiffness condensation |
| stable input-output model reduction | balanced/model-reduction methods based on controllability and observability |
| semi-infinite surface embedding | surface Green-function / embedding methods |
| adsorbate-substrate vibrational mixing | native phonon/VDOS/polarization and surface-vibration analysis |

A P1 claim will need one frozen scientific task and the strongest fair comparator for that task. SI is not permitted to combine weak competitors from different tasks into a straw baseline.

## Current contribution-language ceiling

Allowed:
- "we investigate";
- "we formalize a prospective evidence architecture";
- "we test whether";
- "the current engine integrates";
- "the current targeted search did not locate a study matching the full sequence";
- "candidate residual contribution".

Not allowed yet:
- "first";
- "novel universal inheritance law";
- "new Green-function method";
- "new mode-tracking method";
- "new component-mode synthesis";
- "first demonstration that substrate modes influence adsorbate modes";
- "unique framework" without an exhaustive legitimate prior-art basis.

## Current status

TARGETED_PRIMARY_LITERATURE_COLLISION = INITIAL_PASS_COMPLETE
NEAREST_LEGITIMATE_PRIOR_ART = IDENTIFIED_FOR_MAJOR_METHOD_PRIMITIVES
RESIDUAL_NOVELTY = NARROWED_BUT_NOT_CONFIRMED
STANDARD_TOOLKIT_COMPARATOR = TASK_DEPENDENT_CANDIDATES_IDENTIFIED_NOT_FROZEN
PHYSICAL_ADDED_VALUE = NOT_TESTED

The next deeper literature work should focus specifically on whether any prior study already implements the **full prospective parent-characterization -> frozen carrier mapping -> child prediction -> intervention -> specificity-control** sequence, and whether model-reduction literature already contains an equivalent hierarchical-closure criterion tied to parent-child carrier inheritance rather than generic response preservation.
