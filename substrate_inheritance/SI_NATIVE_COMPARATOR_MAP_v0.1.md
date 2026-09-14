# Substrate Inheritance native comparator map v0.1

**Date:** 14 September 2026  
**Status:** P0-D/P0-Q comparator preparation, not a P1 comparator freeze  
**Sources:** literature-collision v0.1-v0.2, attribution ledger v0.3

## Purpose

A future SI claim must be compared with the strongest fair native method for the **same frozen scientific task**. This map prevents a later analysis from choosing an easy but scientifically irrelevant comparator after seeing the result.

No comparator in this file is frozen for P1. The exact task must be frozen first.

## Comparator decision map

| Scientific task | Native baseline/comparator family | What it already does well | What an SI-specific claim would have to add | Current status |
| --- | --- | --- | --- | --- |
| Track one mode across parameter/system change | MAC/CMAC, domain-native mode tracking | vector similarity and mode identity tracking | prospective parent-to-child prediction with intervention/specificity or another task-specific added value | candidate only |
| Track carriers in crowded/near-degenerate spectra | clustered-eigenvalue/subspace mode tracking; uncertainty-aware modal correlation | avoids unstable one-to-one matching, quantifies correspondence uncertainty | inheritance-specific predictive relation, not just tracking | candidate only |
| Target surface adsorbate vibrational modes | adsorbate-specific mode tracking; full vibrational analysis | targeted adsorbate mode extraction | independent parent/substrate carrier prediction and specificity | candidate only |
| Compare clean and adsorbate-covered surface phonons | EELS/He-scattering/native phonon and first-principles surface analyses | directly resolves changed/overlayer/interface modes | prospective prediction before covered-system reveal plus intervention/specificity | candidate only |
| Assemble/reduce coupled components | Craig-Bampton/CMS/dynamic substructuring | efficient component reduction and assembly | declared inheritance-information preservation beyond ordinary response adequacy | candidate only |
| Exact partitioned linear elimination | Schur complement/dynamic stiffness | exact response equivalence for declared partitioned linear quantities | nothing if SI merely asks exact elimination; SI must ask a different scientific question | established known truth |
| Propagate component uncertainty to system response | CMS uncertainty frameworks; stochastic dynamic substructuring | component-level uncertainty through coupled system | uncertainty used to gate prospectively claimed parent-child inheritance | candidate only |
| Preserve a task-specific response under reduction | balanced/input-output model reduction; response-dependent CMS | optimizes/preserves response-relevant information | inheritance-specific carrier/source relation that adds predictive information | candidate only |
| Trace source-to-receiver contributions through hierarchy | Transfer Path Analysis, FBS, DS/CMS multilevel TPA | source/path contribution and hierarchical transmission | frozen parent carrier prediction + specificity + closure of inherited relation | candidate only |
| Semi-infinite surface/substrate embedding | surface Green functions and embedding potentials | exact/efficient open substrate response | SI cannot claim embedding novelty; must use embedding as native machinery | established known truth |
| Demonstrate adsorbate-substrate hybridization | surface vibrational spectroscopy and first-principles vibrational analysis | shows mixing/hybridization/coupling | SI must go beyond generic influence | already answered |
| Separate coupling effects from simple shifts | isotopic substitution/dilution and native spectroscopy | distinguishes coupling from chemical/frequency shifts | use as inherited control in SI physical test | already answered |
| Demonstrate substrate perturbation affects adsorbate | pump-probe / substrate-heating response experiments | establishes parent-to-child dynamical influence | prospective carrier transformation and specificity | already answered at influence level |
| Multi-parent interaction decomposition | inclusion-exclusion/Möbius and related factorial intervention designs | main and interaction decomposition | physical subset design with common response and prospective SI semantics | candidate application only |

## Comparator selection rule for future P1

1. Freeze the exact scientific task and claim.
2. Search for the strongest method that answers **that task**, not a neighboring one.
3. Freeze implementation/version/settings for both SI and comparator before decisive target reveal.
4. Use identical target evidence and uncertainty treatment where scientifically possible.
5. Define `ADDS`, `TIES`, `WORSE`, `INCOMPARABLE`, and `NO_NATIVE_COMPARATOR` decision logic before the result.
6. If the native method already answers the task, do not redefine the task after seeing a tie.
7. If no method answers the same task after a good-faith search, record `NO_NATIVE_COMPARATOR` and the nearest methods considered. That status does not itself establish superiority.

## Current likely comparator combinations by SI physical route

### Future surface-vibrational parent/child test

Minimum serious native comparison set is likely to include:

- full native vibrational/phonon analysis;
- adsorbate-specific mode tracking;
- frequency-only matching as a deliberately simpler baseline;
- subspace-aware mode tracking when crowding requires it;
- uncertainty-aware modal correspondence;
- isotope/coverage/native physical controls where available.

SI would have to show value in the **prospective parent-to-child evidence sequence**, not merely produce similar mode assignments.

### Future hierarchical closure physical test

Minimum serious comparison set is likely to include:

- full unreduced system/reference;
- exact Schur/dynamic condensation where mathematically available;
- CMS/dynamic substructuring;
- task-appropriate response-dependent or input-output reduction;
- multilevel Transfer Path Analysis if the task concerns hierarchical propagation.

SI would have to show that a declared inherited relation remains scientifically informative after grouping/re-embedding, not merely that a reduced model reproduces response.

## Current `NO_NATIVE_COMPARATOR` status

No current P1 task is frozen, so `NO_NATIVE_COMPARATOR` cannot yet be legitimately assigned. The literature presently suggests strong neighboring comparators for most anticipated SI tasks.

`P1_COMPARATOR_FREEZE = NOT_APPLICABLE_YET`

`NO_NATIVE_COMPARATOR = NOT_EVALUATED_FOR_A_FROZEN_P1_TASK`

`CURRENT_USE = COMPARATOR_PREPARATION_ONLY`.