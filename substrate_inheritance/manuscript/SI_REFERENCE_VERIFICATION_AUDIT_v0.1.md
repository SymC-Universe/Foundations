# SI working-manuscript reference verification audit v0.1

**Date:** 14 September 2026  
**Applies to:** `SI_MANUSCRIPT_WORKING.md` and current literature-collision records  
**Status:** bibliographic/provenance audit, not a systematic-review completeness claim

## Purpose

Verify that the current working references resolve to the stated papers and that the cited source class supports the narrow role assigned to it. This audit checks bibliographic identity and obvious claim/source mismatches. It does not certify that the current reference set is exhaustive enough for a final novelty claim.

## Verification levels

- `PUBLISHER_VERIFIED`: title/authors/venue/year/article metadata checked against publisher or primary journal record.
- `INSTITUTIONAL/CROSSREF_VERIFIED`: identity checked against a university/institutional repository or metadata source tied to DOI/Crossref.
- `SECONDARY_BIBLIOGRAPHIC_VERIFIED`: identity checked against a bibliographic database; primary publisher record should still be checked at manuscript freeze.

## Current references

| Reference | Identity verified | Current manuscript role | Audit disposition |
| --- | --- | --- | --- |
| Allemang, R. J. & Brown, D. L. “A Correlation Coefficient for Modal Vector Analysis,” Proc. 1st IMAC, 110-116 (1982) | `SECONDARY_BIBLIOGRAPHIC_VERIFIED` via CiNii and later journal reference lists | origin/established use of modal-vector correlation / MAC lineage | keep; verify conference-proceedings formatting at final style pass |
| Kim, T. S. & Kim, Y. Y. “MAC-based mode-tracking in structural topology optimization,” *Computers & Structures* 74, 375-383 (2000), DOI `10.1016/S0045-7949(99)00056-5` | `PUBLISHER_VERIFIED` | established MAC-based mode tracking | keep |
| Lu, J., Tang, J., Apley, D. W., Zhan, Z. & Chen, W. “A mode tracking method in modal metamodeling for structures with clustered eigenvalues,” *CMAME* 369, 113174 (2020), DOI `10.1016/j.cma.2020.113174` | `PUBLISHER_VERIFIED` | clustered-eigenvalue carrier tracking | keep |
| Greś, S., Döhler, M. & Mevel, L. “Uncertainty quantification of the Modal Assurance Criterion in operational modal analysis,” *MSSP* 152, 107457 (2021), DOI `10.1016/j.ymssp.2020.107457` | `PUBLISHER_VERIFIED` | uncertainty-aware modal correspondence | keep |
| Guyan, R. J. “Reduction of stiffness and mass matrices,” *AIAA Journal* 3, 380 (1965), DOI `10.2514/3.2874` | `SECONDARY/DOI_VERIFIED`; DOI/title/pages consistent | established static condensation | keep; publisher formatting should be rechecked at final reference export |
| Craig, R. R. & Bampton, M. C. C. “Coupling of substructures for dynamic analyses,” *AIAA Journal* 6, 1313-1319 (1968), DOI `10.2514/3.4741` | `SECONDARY/DOI_VERIFIED`; DOI/title/pages consistent | established CMS/substructure coupling | keep |
| Moore, B. C. “Principal component analysis in linear systems: controllability, observability, and model reduction,” *IEEE TAC* 26, 17-32 (1981), DOI `10.1109/TAC.1981.1102568` | `INSTITUTIONAL/CROSSREF_VERIFIED` | established controllability/observability model reduction | keep |
| de Klerk, D., Rixen, D. J. & Voormeeren, S. N. “General framework for dynamic substructuring: history, review and classification of techniques,” *AIAA Journal* 46, 1169-1181 (2008), DOI `10.2514/1.33274` | `INSTITUTIONAL/DOI_VERIFIED` via TUM/TU Delft records | dynamic-substructuring framework/review | keep |
| Hinke, L., Dohnal, F., Mace, B. R., Waters, T. P. & Ferguson, N. S. “Component mode synthesis as a framework for uncertainty analysis,” *JSV* 324, 161-178 (2009), DOI `10.1016/j.jsv.2009.01.056` | `PUBLISHER_VERIFIED` plus Southampton institutional record | component-to-system uncertainty in CMS | keep; manuscript initials should use `N. S. Ferguson` rather than shortened `N. Ferguson` if journal style retains initials |
| Chatterjee, T., Adhikari, S. & Friswell, M. I. “Uncertainty propagation in dynamic sub-structuring by model reduction integrated domain decomposition,” *CMAME* 366, 113060 (2020), DOI `10.1016/j.cma.2020.113060` | `PUBLISHER_VERIFIED` | uncertainty propagation in dynamic substructuring | keep |
| El Kadmiri Pedraza, S., Monner, H. P. & Algermissen, S. “A framework for simulation-based transfer path analysis using dynamic substructuring and component mode synthesis,” *Computers & Structures* 321, 108097 (2026), DOI `10.1016/j.compstruc.2026.108097` | `PUBLISHER_VERIFIED`, open publisher record and DLR copy | multilevel TPA / hierarchical vibration-path comparator | keep |
| Bondsman, B. & Peplow, A. “Response-dependent component mode-synthesis with interface reduction,” *Applied Mathematical Modelling* 158, 116924 (2026), DOI `10.1016/j.apm.2026.116924` | `PUBLISHER_VERIFIED` | modern response-dependent CMS comparator | keep; publisher lists October 2026 issue publication, so final citation should use publisher's then-current publication metadata at freeze |
| López Sancho, M. P., López Sancho, J. M. & Rubio, J. “Highly convergent schemes for the calculation of bulk and surface Green functions,” *Journal of Physics F: Metal Physics* 15, 851-858 (1985), DOI `10.1088/0305-4608/15/4/009` | `CROSSREF/BIBLIOGRAPHIC_VERIFIED` | established iterative surface/bulk Green-function method | keep; normalize diacritics and exact author metadata from final publisher export |
| Inglesfield, J. E. & Benesh, G. A. “Surface electronic structure: Embedded self-consistent calculations,” *Physical Review B* 37, 6682 (1988), DOI `10.1103/PhysRevB.37.6682` | `PUBLISHER_VERIFIED` | surface embedding onto semi-infinite substrate | keep |
| Inglesfield, J. E. “Embedding at surfaces,” *Computer Physics Communications* 137, 89-107 (2001), DOI `10.1016/S0010-4655(01)00173-4` | `PUBLISHER_VERIFIED` | embedding-method review/application | keep |
| Kern, K., Zeppenfeld, P., David, R. & Comsa, G. “Adsorbate-substrate vibrational coupling in physisorbed Kr films on Pt(111),” *Physical Review B* 35, 886(R) (1987), DOI `10.1103/PhysRevB.35.886` | `PUBLISHER_VERIFIED` | direct physical adsorbate-substrate hybridization / linewidth-broadening prior art | keep |
| Hirschmugl, C. J. & Williams, G. P. “Chemical shifts and coupling interactions for the bonding vibrational modes for CO/Cu(111) and (100) surfaces,” *Physical Review B* 52, 14177 (1995), DOI `10.1103/PhysRevB.52.14177` | `PUBLISHER_VERIFIED` | isotopic control separating coupling from chemical/frequency shifts | keep |
| Liu, K. & Gao, S. “Adsorbate vibration and resonance lifetime broadening of a cobalt adatom on a Cu(111) surface,” *Physical Review B* 74, 195433 (2006), DOI `10.1103/PhysRevB.74.195433` | `PUBLISHER/INSTITUTIONAL_VERIFIED` | substrate-coupled adsorbate vibration and resonance lifetime | keep |
| Herrmann, C. & Reiher, M. “Direct targeting of adsorbate vibrations with mode-tracking,” *Surface Science* 600, 1891-1900 (2006), DOI `10.1016/j.susc.2006.01.054` | `DOI/BIBLIOGRAPHIC_VERIFIED` | adsorbate-specific mode tracking prior art | keep; strong direct comparator for future surface route |
| Fritsch, J., Arnold, M. & Schröder, U. “Ab initio calculation of the phonon dispersion of antimony-covered (110) surfaces of III-V compounds,” *Physical Review B* 61, 16682 (2000), DOI `10.1103/PhysRevB.61.16682` | `PUBLISHER_VERIFIED` | clean/pristine-related, overlayer, and interface mode comparison | keep |

## Additional v0.2-collision source not yet required in the manuscript working list

**Lehwald, S., Rocca, M., Ibach, H. & Rahman, T. S., “Surface phonon dispersion of ordered overlayers,” *Journal of Electron Spectroscopy and Related Phenomena* 38, 29-44 (1986), DOI `10.1016/0368-2048(86)85070-8`.**

Identity and scope are publisher-verified. The paper compares clean and adsorbate-covered Ni(100) surface phonons/resonances by high-resolution EELS. It is useful support for the prior-art ceiling on descriptive clean-versus-covered phonon comparison. Add to the manuscript only if that specific sentence needs another physical example; do not add citations merely to inflate the bibliography.

## Corrections / normalization items

1. Use `N. S. Ferguson` in the Hinke et al. reference if full initials are retained.
2. Normalize `López Sancho` spelling/diacritics consistently across manuscript and bibliography manager.
3. At manuscript freeze, re-export AIAA/IEEE/Elsevier/APS citations from primary records into one target-journal style rather than hand-normalizing punctuation.
4. Re-check the Bondsman & Peplow publication metadata at freeze because the publisher currently assigns it to the October 2026 volume issue while the article record is already available.
5. The Allemang & Brown conference citation has no DOI in the current working record; keep the proceedings identity/pages and do not invent one.

## Claim-support audit

The references currently support the narrow roles assigned to them:

- modal correspondence/tracking and uncertainty are established;
- dynamic substructuring, CMS, response reduction, and uncertainty propagation are established;
- multilevel Transfer Path Analysis is established;
- surface Green-function embedding is established;
- adsorbate/substrate vibrational hybridization and resonance broadening are established;
- isotope-based separation of coupling effects is established;
- adsorbate-specific mode tracking is established;
- clean/pristine-related versus covered-surface phonon comparison is established.

None of these references is evidence that SI's **full prospective inheritance sequence** has been physically demonstrated. Conversely, SI may not claim novelty for the native methods or phenomena those papers already establish.

## Remaining reference work before manuscript freeze

- perform claim-specific nearest-prior-art searches for any sentence that will carry novelty weight;
- re-open every reference actually used in final prose and verify the exact claim against the source, not only the bibliographic identity;
- remove references not materially used;
- export the final bibliography in target-journal style;
- archive the final reference/DOI verification ledger with the manuscript freeze.

## Current disposition

`WORKING_REFERENCE_IDENTITIES = VERIFIED_WITH_NOTED_NORMALIZATION_ITEMS`

`CURRENT_BIBLIOGRAPHY = SUFFICIENT_FOR_WORKING_DRAFT_NOT_FINAL_NOVELTY_CERTIFICATION`

`FULL_SEQUENCE_PRIOR_ART_EXHAUSTIVENESS = NOT_ESTABLISHED`

`PUBLICATION_LEVEL_NOVELTY = NOT_CERTIFIED`.