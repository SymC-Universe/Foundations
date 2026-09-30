# ERIES EuroProteas Cross-Substrate Source Qualification v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** FROZEN BEFORE NUMERIC RESPONSE ACCESS
**Lifecycle stage:** P0-N / P0-Q source and hierarchy qualification
**Evidence role if qualified:** development / architecture qualification only
**P1 eligibility:** NO at this stage

## Why this lane follows BRB

The completed BRB lane is information-rich in modal persistence/reorganization, scalar redundancy, physical interface history, and partial reset. The next benchmark should therefore add a nonredundant relation rather than continue same-source mining.

The ERIES EuroProteas program is selected for source qualification because the same full-scale prototype structure is represented under materially different lower-level foundation/isolation realizations in public or formally registered datasets.

The scientific target is not the generic claim that foundations or soil-structure interaction matter. That is established native prior art. The useful Stability Architecture question is whether a common qualification framework can separate what is preserved in the upper structure from what is reorganized by the lower-level foundation/substrate realization, while retaining the strongest native soil-structure-interaction description as the comparator.

## Frozen source identities to audit

1. **ERIES-RESPOND**, canonical Zenodo record 15518567.
   - pile-group foundation tests;
   - EuroProteas mounted on the pile-group foundation;
   - nominal dynamic range described as 1-10 Hz and 0.1-20 kN.
2. **ERIES-RESPOND pointer / repository alias**, Zenodo record 21354286.
   - metadata/pointer identity only; never substitute pointer content for the canonical numeric archive without provenance resolution.
3. **ERIES-POLIS**, Zenodo record 15575887.
   - EuroProteas on expanded-polystyrene isolation;
   - forced- and free-vibration families.
4. **ERIES-GISIS**, Zenodo record 17721150.
   - EuroProteas on micropiles with encased rubber isolators;
   - identity is useful even if numeric files are not currently public.

## This task is metadata-only

The v0.1 intake may query only public repository metadata and file descriptors:
- title;
- DOI / record identity;
- publication and access state;
- file names;
- declared file sizes;
- checksums;
- repository download/metadata links;
- descriptions and related identifiers.

It may not download or parse any experimental response file, archive member body, acceleration time series, displacement series, force series, FRF, spectrum, fitted parameter, or outcome value.

## Qualification criteria

Return **ERIES_EUROPROTEAS_SOURCE_MATRIX_QUALIFIED** if:
- RESPOND canonical identity is resolved and exposes a public numeric archive descriptor;
- POLIS identity is resolved and exposes a public numeric archive descriptor;
- GISIS identity is resolved, with its current public/embargo access state recorded rather than bypassed;
- the RESPOND pointer/alias is distinguishable from the canonical numeric archive;
- all retrieved titles are consistent with their frozen source roles.

Return **ERIES_EUROPROTEAS_SOURCE_MATRIX_PARTIAL** if RESPOND and POLIS are resolved but one auxiliary identity/access-state check is unavailable.

Return **ERIES_EUROPROTEAS_SOURCE_IDENTITY_AMBIGUOUS** if canonical/alias identity cannot be distinguished without opening numeric content.

Return **ERIES_EUROPROTEAS_SOURCE_BLOCKED** if the official metadata sources cannot be reached.

## Next gate if qualified

Do not score responses immediately. Construct an outcome-blind archive-layout/channel/matched-test preflight to determine whether a legitimate matched hierarchy can be frozen without inspecting response values.

A later scoring protocol, if licensed, must include:
- explicit lower-level foundation/substrate representation;
- explicit upper-level foundation/roof or system target;
- matched excitation/frequency rules defined without outcomes;
- strongest native SSI/system-identification comparator;
- preserved Function and Limit cases;
- explicit REFUSED / INVALID_TEST / NEED_MORE_INFO routes;
- no automatic identification of lowercase chi, capital Chi, or Chi_arc from generic channels.

Cross-substrate comparison is allowed only after source/layout qualification demonstrates a defensible correspondence. No generic "substrate matters" claim is eligible for novelty.
