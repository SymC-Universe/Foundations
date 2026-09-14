# Substrate Inheritance Targeted Literature Collision v0.1

Date: 2026-09-12
Status: P0-D/P0-Q literature collision after independent experimental ideation
Pre-search record: `SI_EXPERIMENTAL_OPPORTUNITY_v0.1.md`
General Protocol: v0.7.4 Section 50.2

## Sequence integrity

The independent experimental game plans E1-E5 were committed before the targeted searches summarized here. This file therefore records the literature collision rather than retroactively generating the experiments from papers that were already known.

This search is a targeted first collision, not an exhaustive systematic review. `NO_CLOSE_PRECEDENT_FOUND` below means only that this search did not locate a close precedent. It is not proof of novelty.

## Search question 1: has adsorbate/substrate vibrational coupling and hybridization already been demonstrated?

### Result: ALREADY_ANSWERED at the generic-phenomenon level

Prior work clearly establishes that adsorbate and substrate vibrational structures can couple and hybridize.

1. K. Kern, P. Zeppenfeld, R. David, and G. Comsa, "Adsorbate-substrate vibrational coupling in physisorbed Kr films on Pt(111)," *Physical Review B* 35, 886(R) (1987), DOI `10.1103/PhysRevB.35.886`.
   - Inelastic He scattering measured surface-phonon dispersion for 1, 2, 3, and 25 monolayer Kr films on Pt(111).
   - The authors report hybridization between localized adlayer modes and the substrate Rayleigh wave in the intersection region and linewidth broadening where adlayer modes overlap substrate bulk bands.
   - SI consequence: "coupling/hybridization exists" is established physics, not an SI novelty target.

2. K. Liu and S. Gao, "Adsorbate vibration and resonance lifetime broadening of a cobalt adatom on a Cu(111) surface," *Physical Review B* 74, 195433 (2006), DOI `10.1103/PhysRevB.74.195433`.
   - The calculation resolves phonon dispersions, local vibrational densities, polarization distributions, and adsorbate coverage.
   - The frustrated translation and vertical adsorbate vibrations are reported as strongly coupled to substrate atomic vibrations.
   - SI consequence: local vibrational density and polarization/participation are established ways to inspect adsorbate-substrate vibrational mixing.

Disposition for E1 at this level: `DO_NOT_BUILD_ALREADY_ANSWERED` for the question "does adsorbate-substrate vibrational hybridization occur?"

## Search question 2: have experiments separated coupling effects from simple frequency/chemical shifts?

### Result: ALREADY_ANSWERED / METHOD_AVAILABLE

C. J. Hirschmugl and G. P. Williams, "Chemical shifts and coupling interactions for the bonding vibrational modes for CO/Cu(111) and (100) surfaces," *Physical Review B* 52, 14177 (1995), DOI `10.1103/PhysRevB.52.14177`.

- Low-frequency infrared reflection absorption spectra were measured for isotopic mixtures of CO and 13C18O on Cu(100) and Cu(111).
- The isotope data were used to distinguish chemical shifts from coupling effects for the C-metal and hindered-rotation modes.
- The paper assigns a dominant dipole-dipole coupling mechanism for perpendicular modes and reports different behavior for parallel modes on Cu(111).

Related earlier work on isotopic adsorbate mixtures also treats collective vibrational coupling, including CO/Cu(100) and CO/Pt surfaces.

SI consequence:
- isotopic substitution is an established experimental control for separating frequency shifts and collective coupling effects;
- simple frequency movement is insufficient evidence for carrier-resolved inheritance;
- E1 should inherit isotopic controls where feasible rather than claim them as new.

Disposition: `ADOPT_EXISTING_METHOD`.

## Search question 3: has a controlled substrate perturbation been used to measure adsorbate dynamical response?

### Result: PARTIALLY_ANSWERED / METHOD_AVAILABLE

J. P. Culver and collaborators, "Vibrational response of surface adsorbates to femtosecond substrate heating," *Chemical Physics Letters* 214, 431-437 (1993), DOI `10.1016/0009-2614(93)85661-7`.

- CO/Cu(111) adsorbate vibrations were monitored after an impulsive femtosecond excitation of the underlying metal substrate.
- The work measured adsorbate vibrational response and inferred coupling to substrate electron and phonon reservoirs.

A later CO/Cu(111) study, "Temperature-dependent coupling of low frequency adsorbate vibrations to metal substrate electrons," *Chemical Physics* 205, 159-166 (1996), DOI `10.1016/0301-0104(95)00376-2`, used time-resolved IR after substrate excitation to extract temperature-dependent energy-transfer coupling for the frustrated-translation mode.

SI consequence:
- intervention-like substrate-to-adsorbate dynamical response is established experimentally;
- E1/E5 must not claim novelty merely for perturbing a substrate and observing an adsorbate response;
- the residual SI question is whether a **parent architecture characterized before the coupled target is opened** predicts which carrier/subspace structure survives or transforms, and whether that prediction beats frequency-only/generic controls.

Disposition: `MODIFY_TO_TEST_RESIDUAL_QUESTION`.

## Search question 4: are modal/correspondence tracking and uncertainty established methods?

### Result: ALREADY_ANSWERED / STRONG NATIVE METHOD FAMILY

1. R. J. Allemang and D. L. Brown, "A Correlation Coefficient for Modal Vector Analysis," Proceedings of the 1st International Modal Analysis Conference, pp. 110-116 (1982).
   - Introduced the Modal Assurance Criterion (MAC) family used to compare mode-shape vectors.

2. T. S. Kim and Y. Y. Kim, "Mac-based mode-tracking in structural topology optimization," *Computers & Structures* 74, 375-383 (2000), DOI `10.1016/S0045-7949(99)00056-5`.
   - Uses MAC explicitly for tracking modes as structures change.

3. J. Lu, J. Tang, D. W. Apley, Z. Zhan, and W. Chen, "A mode tracking method in modal metamodeling for structures with clustered eigenvalues," *Computer Methods in Applied Mechanics and Engineering* 369, 113174 (2020), DOI `10.1016/j.cma.2020.113174`.
   - Treats clustered eigenvalues, crossing/veering, and transformation within the clustered subspace rather than relying only on individual eigenvectors.

4. S. Greś, M. Döhler, and L. Mevel, "Uncertainty quantification of the Modal Assurance Criterion in operational modal analysis," *Mechanical Systems and Signal Processing* 152, 107457 (2021), DOI `10.1016/j.ymssp.2020.107457`.
   - Develops uncertainty bounds for MAC estimates obtained from measured modal data.

SI consequence:
- vector overlap, MAC-like correspondence, clustered-subspace handling, and uncertainty-aware mode comparison are not by themselves novel;
- SI should compare against these native methods rather than presenting modal overlap as an SI invention;
- any added value must come from the specific prospective parent-to-child evidence architecture, coupling/intervention/specificity closure, hierarchical use, or measurable tool value.

Disposition: `ADOPT_EXISTING_METHOD` and `STANDARD_TOOLKIT_CANDIDATE` for future frozen comparisons.

## Search question 5: is subsystem reduction/re-embedding an established field?

### Result: ALREADY_ANSWERED at the general method level

Several mature method families directly overlap the mathematical core of SI hierarchical closure.

1. R. J. Guyan, "Reduction of stiffness and mass matrices," *AIAA Journal* 3, 380 (1965), DOI `10.2514/3.2874`.
   - Classic structural reduction/static condensation.

2. R. R. Craig and M. C. C. Bampton, "Coupling of substructures for dynamic analyses," *AIAA Journal* 6, 1313-1319 (1968), DOI `10.2514/3.4741`.
   - Component Mode Synthesis (CMS) couples reduced substructures for dynamic analysis.

3. D. de Klerk, D. J. Rixen, and S. N. Voormeeren, "General Framework for Dynamic Substructuring: History, Review and Classification of Techniques," *AIAA Journal* 46, 1169-1181 (2008), DOI `10.2514/1.33274`.
   - Reviews dynamic substructuring as a mature field for assembling and reducing coupled components.

4. B. C. Moore, "Principal component analysis in linear systems: Controllability, observability, and model reduction," *IEEE Transactions on Automatic Control* 26, 17-32 (1981), DOI `10.1109/TAC.1981.1102568`.
   - Establishes balanced-system ideas linking controllability/observability to model reduction and input-output relevance.

5. The Mori-Zwanzig formalism provides a mathematically consistent projection framework in which unresolved dynamics appear as memory terms. A representative modern treatment is P. Stinis and collaborators' memory-estimation literature, including *Proceedings of the Royal Society A* work on a priori memory estimation in reduced-order models (2017).
   - SI consequence: when reduced variables retain memory of eliminated substrate degrees of freedom, adding a local Markovian coefficient without qualification is not justified.

SI consequence:
- reduction, grouping, substructuring, and preserving system response are established scientific fields;
- FM4 cannot claim novelty for asking whether a reduced subsystem preserves higher-level dynamics;
- the nearest native comparison for linear mechanical FM4 is dynamic substructuring/CMS plus exact frequency-domain Schur condensation, with balanced/model-reduction concepts relevant when the task is input-output preservation.

Disposition: `ADOPT_EXISTING_METHOD` and `STANDARD_TOOLKIT_CANDIDATE`.

## Search question 6: are semi-infinite surface embedding and surface Green functions established?

### Result: ALREADY_ANSWERED / STRONG NATIVE METHOD FAMILY

1. M. P. Lopez Sancho, J. M. Lopez Sancho, and J. Rubio, "Highly convergent schemes for the calculation of bulk and surface Green functions," *Journal of Physics F: Metal Physics* 15, 851-858 (1985), DOI `10.1088/0305-4608/15/4/009`.
   - Iterative principal-layer method for bulk and surface Green functions of semi-infinite solids.

2. J. E. Inglesfield and G. A. Benesh, "Surface electronic structure: Embedded self-consistent calculations," *Physical Review B* 37, 6682 (1988), DOI `10.1103/PhysRevB.37.6682`.
   - Embeds a surface region onto a semi-infinite substrate using a substrate-Green-function-derived embedding potential.

3. J. E. Inglesfield, "Embedding at surfaces," *Computer Physics Communications* 137, 89-107 (2001), DOI `10.1016/S0010-4655(01)00173-4`.
   - Reviews embedding methods and surface/adsorbate applications.

SI consequence:
- Green-function embedding, surface self-energy, and semi-infinite reduction are established methods and must be cited as such;
- SI's finite-depth/semi-infinite validation is method qualification, not a new embedding principle.

Disposition: `ADOPT_EXISTING_METHOD`.

## Search question 7: did the targeted collision locate the exact SI residual experiment?

### Result: RESIDUAL_QUESTION_IDENTIFIED, NOT A NOVELTY PROOF

This targeted pass located strong precedents for:

- adsorbate-substrate vibrational hybridization;
- isotope-based separation of coupling and chemical/frequency shifts;
- substrate perturbation followed by adsorbate vibrational response;
- modal vector comparison and mode tracking;
- clustered-subspace handling;
- uncertainty-aware modal comparison;
- dynamic substructuring/component-mode synthesis;
- input-output-oriented model reduction;
- semi-infinite Green-function embedding.

It did **not** locate, in this first targeted search, a study matching the full proposed SI evidentiary sequence:

1. independently characterize a parent/substrate carrier architecture;
2. freeze physical coordinate and carrier/subspace mapping before target inspection;
3. prospectively predict the carrier-resolved child/coupled-system transformation;
4. test that prediction on an independently generated child object;
5. intervene on the parent and test the predicted child change;
6. defeat frequency-only, same-spectrum, generic-parent, or coupling-rewire controls;
7. preserve uncertainty and nonidentifiability rather than force a match;
8. optionally test whether the resulting effective subsystem remains adequate after re-embedding at a higher level.

This sequence is therefore a **residual research question**, not an established novelty claim.

Classification: `RESIDUAL_QUESTION_IDENTIFIED`.

## Experimental dispositions after collision

### E1 adsorbate-on-substrate vibrational inheritance

Disposition: `MODIFY_TO_TEST_RESIDUAL_QUESTION`.

Do not test whether coupling/hybridization exists. Test the stricter prospective carrier-prediction and specificity question. Inherit mixed-isotope controls, native modal tracking/subspace methods, and uncertainty methods where experimentally appropriate.

### E2 thickness/depth inheritance and hierarchical closure

Disposition: `USE_AS_KNOWN_TRUTH_QUALIFICATION` first, then `MODIFY_TO_TEST_RESIDUAL_QUESTION` if physical data become available.

Dynamic substructuring, CMS, exact frequency-domain condensation, Green-function embedding, and semi-infinite surface methods already provide strong native comparators. FM4 should be constructed as a comparison against those methods, not as a replacement for them.

### E3 tabletop coupled-oscillator analogue

Disposition: `USE_AS_KNOWN_TRUTH_QUALIFICATION`.

Its value is controlled hardware semantics and method failure detection. It cannot establish domain-native surface/material inheritance by analogy.

### E4 multi-parent source attribution

Disposition: `METHOD_AVAILABLE / RESIDUAL_APPLICATION_QUESTION`.

Interaction decomposition is established mathematics. The residual question is whether prospectively defined physical source interventions make this decomposition informative for SI without violating common-response and subset-completeness requirements.

### E5 rare/extreme limit probe

Disposition: `DEFER_UNTIL_ORDINARY_FUNCTION_MAP_EXISTS`.

The Function Map should not be displaced by an extreme system. A rare case is useful only after the ordinary supported region and the exact limit question are clear.

## Immediate consequence for SI investigation

The literature collision **narrows** the program rather than weakening it.

The current SI research target is no longer allowed to be phrased as any of the following:

- substrates influence adsorbates;
- adsorbate and substrate modes hybridize;
- mode shapes can be tracked;
- substructures can be reduced and coupled;
- Green functions can embed a semi-infinite substrate;
- isotope substitution can reveal vibrational coupling;
- substrate excitation can change adsorbate vibrational response.

All of those have substantial prior art.

The surviving question is narrower:

> Does an independently characterized parent/substrate architecture provide prospectively useful, uncertainty-aware, carrier-resolved information about a child/coupled system that cannot be reduced to ordinary frequency matching or generic coupling influence, and if an effective inherited subsystem is formed, what higher-level quantities does it preserve after grouping or re-embedding?

That question is suitable for continued P0-D/P0-Q work. It is not yet a P1 claim.

## Next computational action

Proceed with `FM4_HIERARCHICAL_CLOSURE_LANDSCAPE` using native comparators explicitly:

- unreduced full block system as the reference;
- exact Schur/dynamic-stiffness condensation as a known-truth reference where mathematically exact;
- reduced/static condensation or truncated modal/CMS-like approximations as deliberately lossy comparators;
- task-specific preservation metrics for transfer response, poles/subspaces where licensed, perturbation propagation, and transient/recovery behavior where licensed.

The scientific question is not "can we reduce a system?" It is "which declared SI-relevant quantities survive which reduction over which regime, and where does closure fail?"
