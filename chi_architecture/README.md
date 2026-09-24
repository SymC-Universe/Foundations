# Chi Architecture Investigation

**Status:** P0-D / P0-Q DOMAIN-FIRST ARCHITECTURE MAPPING  
**Branch:** `chi-architecture-p0`  
**Authority:** SymC General Operations Manual v0.8.6  
**Claim ceiling:** exploratory and qualification evidence only  
**Confirmatory MFR-14:** not yet activated  
**Predictive tool status:** not a tool; no validated cross-domain Atlas; no prospective cross-domain confirmation

## Governance baseline

The active program authority is **SymC General Operations Manual v0.8.6 (23 September 2026)**.

The frozen scientific contracts remain historically bound to the GOM version under which they were preregistered unless a documented prospective amendment changed them before decisive evidence. Current communication, reproducibility-guide presentation, project control, and subsequent experiment governance follow v0.8.6.

## Current scientific question

Can materially different domains each generate a scientifically useful stability-coordinate map from their own native scalar content, modal/vector carriers, coupling/system organization, feedback/relationships, uncertainty, and other structure that earns admission, and do those independently derived domain maps later admit meaningful cross-domain alignment?

The program does **not** assume that every domain has the same formula, dimensionality, components, or scalar chi.

The current ordering is:

`native domain science -> Function Map + Limit Map -> candidate Chi_d coordinate map -> within-domain qualification -> frozen domain map -> cross-domain Stability Architecture Atlas`

The inverse dependency is forbidden:

`desired Atlas pattern -> tune Chi_d -> rediscover desired Atlas pattern`

See `DOMAIN_FIRST_CHI_COORDINATE_PROGRAM_v0.1.md`.

## Scope discipline

Universality is **not** a research target or promotion criterion.

The architecture is being investigated because it may be unusually broad across otherwise different systems and regimes. Its scope must be earned one regime, mechanism, and untouched test at a time. A result that works in several domains remains a bounded cross-regime result unless additional evidence extends that boundary.

`BROAD != UNIVERSAL`

A scientifically valuable outcome may therefore be any of the following:

- broad cross-regime architecture;
- domain-family architecture;
- regime-specific architecture;
- partial transportability of selected components;
- multidimensional rather than scalar coordinate structure;
- no admissible chi coordinate in a particular domain;
- or failure of the proposed architecture outside a narrow class.

None is treated as a continuity failure.

## Historical interpretation of the scalar-first investigation

The program should not be read as having started from the belief that a scalar chi was the fundamental object.

The earlier conceptual premise was that systems are shaped not only by their isolated properties but by pressure, influence, coupling, and feedback from other systems or components, and that a coupled/grouped system can contain scientifically important behavior not recoverable from isolated components alone.

The damped oscillator supplied an early mathematically tractable realization in which competing tendencies admit the scalar coordinate

`chi = gamma / (2 omega_0)`.

That success motivated an extended **scalar-first investigation** because the scalar was measurable, compact, and analytically useful. It did not establish that the scalar was ontologically primary.

The historical progression is recorded as:

`systems/feedback/coupling premise -> tractable scalar probe -> scalar-first testing -> evidence that scalar alone is insufficient -> modal/carrier and conglomerate/system structure -> domain-first architecture/coordinate reconstruction`

Documentary provenance for the earliest pre-mathematical formulation should be added separately if the original paper or dated record is recovered. Such provenance would establish hypothesis history, not empirical correctness.

## Working Chi object

For a domain `d`, the working hypothesis is that native measurable architecture `A_d` may generate a coordinate object

`Chi_d : A_d -> Z_d`.

`Z_d` is the smallest scientifically adequate coordinate space supported by that domain. It is not required to be one-dimensional.

Possible outcomes include scalar, vector, subspace/projector, graph/network, operator/manifold, hybrid discrete-continuous, or refused coordinate structures.

A lowercase scalar `chi_d` is admitted only if one-dimensional compression earns its existence from the native mathematics and preserves the information needed for the declared scientific task.

The cross-domain Atlas is downstream of these independently derived coordinates. The Atlas records placements; it does not create them.

## Current starting basis

Where native science supports them, inspect:

- **scalar:** compressed stability coordinates, invariants, rates, ratios, spectra, or other defensibly derived scalar summaries;
- **vector/modal:** resolved carrier structure such as eigenvectors, invariant subspaces, projectors, participation structure, latent modes, or other domain-native multidimensional objects;
- **conglomerate/system:** organization created by coupling, feedback, networks, subsystem interaction, memory, environmental structure, cross-layer mappings, or collective behavior;
- **relationships/open channels:** feedback paths, coupling direction, disagreement, inheritance, uncertainty/nonidentifiability, adequacy, and other domain-native structure not reducible to the first three views.

These are starting representations, not a mandated complete decomposition.

## Chi naming and admission rule

An object is not called chi merely because it is a useful stability quantity.

- `chi = gamma / (2 omega_0)` remains a licensed scalar construction only for a justified passive second-order factor with the required conventions and boundary structure.
- A different regime may generate a different candidate scalar chi only through its own native model, derivation, validity conditions, uncertainty treatment, nulls, and admission rules.
- A scalar chi is not required for an architecture to be scientifically meaningful.
- Any proposed scalar compression must earn its existence by preserving or adding scientifically useful information beyond the richer native representation.
- A domain may legitimately return `NO_ADMISSIBLE_SCALAR_CHI` or `NO_ADMISSIBLE_CHI_COORDINATE`.
- A visually attractive cross-domain alignment cannot be used to retrofit a domain coordinate.

## Joint lowercase chi / broader Chi target

Where a domain admits a local/modal lowercase `chi` and also supports a broader domain/system `Chi` architecture, their relationship is itself a research target rather than an after-the-fact comparison.

Each applicable domain map should ask:
- what information the local/modal coordinate contributes to the broader organization;
- how coupling, hierarchy, environment, or system organization changes the realized meaning of the local/modal coordinate;
- whether perturbation exposes that relationship more clearly than static placement;
- whether response/recovery behavior is stable, reorganized, or non-identifiable.

No domain is required to produce a scalar. `NOT_APPLICABLE`, `NO_ADMISSIBLE_SCALAR_CHI`, `NO_ADMISSIBLE_CHI_COORDINATE`, and `NON_IDENTIFIABLE` remain valid outcomes.

When a claim involves recovery/resilience, report resistance, finite-time response, first reclaim, sustained recovery, reorganization, basin robustness, and repeated-perturbation behavior separately where measurable. Do not equate stability with recovery by definition.

Current migration record: `GOM_V0.8.3_MIGRATION_20260921.md`.

## Function Map and Limit Map

Under SymC GOM v0.8.3, every mature domain investigation should characterize both:

1. **Function Map:** ordinary supported operation, variation, perturbation response, compensation/redistribution where present, alternate stable organizations, and trajectories through the functioning regime;
2. **Limit Map:** transitions, saturation, model breakdown, loss of identifiability, refusal, instability, and qualified rare natural limit states.

The objective is to map the phenomenon, not only to attack it.

Qualified rare natural occurrences are high-information limit testbeds. They must be selected using domain-native rarity/extremeness rather than favorable chi placement. Already-viewed rare events are P0-D/P0-Q evidence; P1 use requires independent prospective selection/freeze.

## D01 linear-dynamics map

`D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json` is the first domain-map plan.

### D01A exact SDOF anchor: complete

The frozen D01A plan scanned `chi=0...4` in increments of `0.05`, four values of `omega0`, and two normalized initial conditions.

GitHub Actions run `34615114508` completed successfully. Artifact `chi-architecture-d01a-domain-map-v01`, ID `10269408539`, digest `sha256:fcaefcb95485a390b79530a890fad3dff5f4419fc3d31749c9240eeec8a7012c`.

Observed within-domain results:

- normalized trajectories at fixed chi collapse across `omega0=0.5,1,2,5` to machine precision;
- maximum normalized displacement collapse error = `0.0`;
- maximum normalized velocity collapse error = `1.1102230246251565e-16`;
- `chi=1` is the exact first nonoscillatory grid point and maximizes the slowest dimensionless decay rate;
- for initial displacement `(x0,u0)=(1,0)`, the frozen grid gives minimum 2% state-settling time at `chi=0.80`, minimum integrated absolute displacement at `chi=0.65`, and minimum integrated energy at `chi=0.70`;
- for initial normalized velocity `(x0,u0)=(0,1)`, minimum 2% state-settling time occurs at `chi=0.75`, while two integrated metrics continue improving through the upper scanned boundary and therefore do not license an interior optimum claim.

Interpretation: within the exact oscillator, chi earns its existence as a dimensionless response-placement coordinate, while different function metrics and perturbations value different locations on that coordinate. `chi=1` is structurally special but is not a task-independent optimum.

See `D01A_SDOF_DOMAIN_MAP_READOUT_v0.1.md`.

### D01B coupled 2DOF extension: complete

The frozen 1,152-case / 2,304-response D01B map completed successfully. All cases remained asymptotically stable, but only 227/1,152 admitted exact real modal scalarization. Fixed isolated-component chi values could accompany large coupling-driven changes in settling and redistribution behavior.

The exact equal-component subfamily also exposed an invariant symmetric branch that preserves its local chi while the antisymmetric branch is transformed by coupling. This is retained as an exact model-level inheritance mechanism with post-result promotion debt, not physical confirmation.

See `D01B_COUPLED_2DOF_DOMAIN_MAP_READOUT_v0.1.md`.

### D01C non-normal extension: complete

D01C was frozen before output at commit `b8bf36c2776e2d788cdbf7a5f33e4254d1cb5f9b` and executed through the single-entry reproduction interface at commit `9818612abae93e460af7ab45281fd9a5e4ae68e7`.

GitHub Actions run `35809467796` completed successfully with one reviewer artifact, `chi-architecture-d01c-v01` (artifact ID `10728829675`).

Across two fixed-spectrum non-normal families, eigenvalues were preserved to maximum residual `2.22e-16` while worst-case state gain changed from 1.0 to 28.65x in N1 and from 1.0 to 74.50x in N2 as carrier non-orthogonality increased.

The correct novelty verdict is deliberately narrow:

`STANDARD_NONMODAL_TOOLKIT_SUFFICIENT_FOR_D01C`

Established state-transition, numerical-abscissa, conditioning, and resolvent analysis explain the synthetic result. D01C therefore does not create a new SymC non-normal stability quantity. It strengthens the representation rule that scalar/spectral coordinates may remain valid for asymptotic placement while being insufficient for finite-time response and robustness questions.

See `D01C_NONNORMAL_DOMAIN_MAP_READOUT_v0.1.md` and `REPRODUCIBILITY_GUIDE.md`.

## D02 physical calibration

### D02A CsPbBr3 phonon carrier test: complete

D02A moved the architecture program from constructed linear systems to publisher-supplied physical source data.

The first prospective parser failed scientifically and remains preserved as:

`PARTIAL_VALID_LINEWIDTH__CARRIER_PARSER_INADEQUATE__CHI_REFUSED`.

A separate post-result v0.2 parser repair reconstructed the Figure 3 source matrices correctly:

- 300 K orthorhombic M-R: 46 x 21;
- 385 K tetragonal M-R: 38 x 21;
- 419 K cubic M-R: 21 x 21.

All three retained the same 21 source-defined M-R q positions.

The source M-point linewidth changes from 0.77 +/- 0.07 meV at 300 K to 9.11 +/- 0.49 meV at 385 K, while the normalized carrier maps retain a zero-energy maximum across all frozen q positions. The distributed carrier shape partly persists and partly reorganizes across phase.

Lowercase chi is **refused**, not estimated, because the locked source table does not provide same-condition natural frequency `omega0`.

The native-comparator verdict is:

`NATIVE_PHONON_TOOLKIT_SUFFICIENT`

The physical pattern is therefore retained as:

`CARRIER_CORRESPONDENCE_PERSISTS / LOCAL_DAMPING_TRANSFORMS / DISTRIBUTED_SHAPE_REORGANIZES / SCALAR_CHI_REFUSED`.

This is a useful physical calibration of the representation rules, not a new phonon law or untouched confirmation.

See:

- `d02_cspbbr3/D02A_PHYSICAL_CALIBRATION_READOUT_v0.2.md`
- `d02_cspbbr3/D02A_V0.1_POSTEXECUTION_INTEGRITY_AUDIT.md`
- `results/D02A_EXECUTION_ARCHIVE_v0.2.json`
- `REPRODUCIBILITY_GUIDE.md`

## D02B four-bolt physical perturbation: complete

D02B is the first physical map in this workstream with a directly licensed same-condition modal chi and an independently controlled physical interface state.

The selected Zenodo four-bolt LDV dataset provides 18 bolt-torque configurations, seven source-retained resonance families, 51 matched scan points, raw FRFs, and native MAC/CMAC response metrics.

The one-command run completed successfully:

`python chi_architecture/reproduce.py d02b`

Primary 10->0 Nm result:

- 28/28 comparisons reorganize in native full-field response;
- 11/28 admit chi in both states;
- 11/11 comparable pairs transform beyond the frozen one-bin chi resolution;
- 17/28 primary comparisons are refused/non-identifiable under the frozen half-power/window rules;
- zero primary pairs preserve similar chi.

Secondary 10->5->0 Nm result:

- all 28/28 5 Nm scalar estimates are admitted;
- 16/28 remain similar to the 10 Nm chi while embedded response has already reorganized;
- those cases span 6/7 mode families;
- with further loosening, amplitude MAC and complex CMAC dissimilarity increase in 28/28 sequences, phase-only dissimilarity in 24/28, and absolute frequency shift in 28/28.

The resulting bounded interpretation is a graded hierarchy:

`moderate substrate change -> embedded reorganization can precede scalar transformation`

followed, under stronger perturbation, by

`stronger substrate change -> local chi transforms or is refused/non-identifiable + embedded response further reorganizes`.

The native-toolkit verdict is:

`NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE`.

See:

- `d02b/D02B_FOUR_BOLT_SOURCE_CONTRACT_v0.3.md`
- `d02b/D02B_EXACT_SOURCE_MAPPING_v0.1.md`
- `d02b/D02B_RAW_PARSER_AND_CLASSIFICATION_FREEZE_v0.1.md`
- `D02B_FOUR_BOLT_PHYSICAL_READOUT_v0.1.md`
- `results/D02B_ARCHIVAL_RECORD_v0.1.json`
- `results/D02B_INTERPRETED_SUMMARY_v0.1.json`
- `REPRODUCIBILITY_GUIDE.md`

## Anti-circularity position

The workstream must not follow these invalid chains:

`inspect favorable architecture -> choose a scalar that matches it -> call that scalar chi -> use the match as evidence for chi architecture`

or

`inspect desired cross-domain Atlas alignment -> alter domain coordinate -> claim the altered coordinate independently aligns across domains`.

Instead:

`native model -> native observables -> Function/Limit Map -> candidate domain coordinate -> within-domain qualification -> freeze -> cross-domain comparison`.

The conglomerate cannot mean "whatever combination performs best." It must be a named native mathematical or physical relationship whose construction is fixed independently of the outcome being used to test it.

### Designed fixtures are not evidence for the hypothesis they encode

F0-F8 are **known-truth designed fixtures**. Their parameters were chosen to exercise specific mathematical and software behaviors. Correct recovery qualifies implementation behavior only.

Therefore:

- F4's analytically selected feedback cases verify the Hurwitz coupling criterion; they do not establish compensatory discordance.
- F1/F6 verify established fixed-spectrum non-normal behavior; they do not establish added architecture value beyond standard non-normal analysis.
- F8 verifies admission/refusal behavior for a licensed second-order scalar; it does not establish cross-regime chi.
- no F0-F8 success counts as empirical confirmation, P1 evidence, or program-level `ADDS`.

`P0_EXPERIMENT_PLAN_v0.2.json` remains the immutable current fixture source. It is not silently rewritten around the new domain-first program.

## Current developmental domain sequence

1. second-order damped dynamics, exact scalar anchor;
2. coupled/non-normal linear dynamics;
3. NSD synthetic known-truth dynamics and observable-rank/refusal architecture;
4. GRI static multi-omic architecture with biological chi withheld;
5. substrate-inheritance coupled dynamics;
6. Chemistry single-barrier versus network-resolved systems;
7. additional mature domains such as power-grid, seismological, quantum/open-system, and cosmological systems after native-domain audit.

Already-viewed GRI, Barrier Atlas, and NSD evidence remains calibration/provenance evidence for rules learned from it, not pristine confirmation.

## Current status against the General Protocol

See:

- `DOMAIN_FIRST_CHI_COORDINATE_PROGRAM_v0.1.md`
- `DOMAIN_CHI_MAP_SCHEMA_v0.1.json`
- `D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json`
- `D01A_SDOF_DOMAIN_MAP_READOUT_v0.1.md`
- `GENERAL_PROTOCOL_AUDIT_20260910.md`
- `CIRCULARITY_AUDIT_20260910.md`
- `CROSS_PROJECT_UPDATE_AUDIT_20260910.md`
- `POST_RESULT_DISCOVERY_LEDGER.md`
- `P0_FALSIFIABILITY_CHARTER_v0.1.md`
- `P0_EXPERIMENT_PLAN_v0.1.json` for preserved historical v0.1 provenance
- `P0_EXPERIMENT_PLAN_v0.2.json` for current P0 fixture execution

## D02C prospective wind-blade test: complete

D02C is the first prospectively frozen external physical test of CA-D007.

System:
- full-scale wind-turbine blade climate-chamber icing experiment;
- dataset DOI `10.5281/zenodo.18427836`;
- local scalar: LSCF modal damping ratio;
- independent organization observable: three-sensor complex CSD principal-vector dissimilarity;
- thermal/no-icing dry-run firewall;
- twelve baseline and twelve intervention windows.

Frozen outcome:

- X direction: `NEITHER_CHANGES`;
- Z direction: `NEITHER_CHANGES`;
- CA-D007 domain-specific support: `false`.

No intervention scalar confidence interval left the pre-spray control envelope.

No intervention organization window exceeded the effective midnight/dry-run threshold.

Therefore D02C is a prospective null:

`NO_SUPPORT / NO_CLEAN_REVERSAL`.

CA-D007 is not prospectively replicated and its promotion debt remains unpaid.

Native-toolkit verdict:

`NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE`.

See:
- `D02C_WIND_BLADE_PROSPECTIVE_READOUT_v0.1.md`
- `d02c/D02C_WIND_BLADE_CONTRACT_v0.1.md`
- `d02c/D02C_ONSET_COMPLETENESS_RULE_v0.1.md`
- `results/D02C_ARCHIVAL_RECORD_v0.1.json`
- `REPRODUCIBILITY_GUIDE.md`

## D02D prospective LUMO test: complete

D02D is the second prospectively frozen external physical test of CA-D007.

The three location-level orderings are all `ORDERING_NON_IDENTIFIABLE`, producing the frozen program result `INDETERMINATE`.

The primary source of indeterminacy is environmental/operational completeness rather than modal-track failure. The strict paired healthy temperature/log-RMS rectangle left fewer than the required 10 matched damaged blocks in enough 010/111 campaigns to prevent a complete onset ordering.

A DAM6 111 response is identifiable, but the preceding 010 level is not, so the frozen rules prevent using the later response to rescue the hypothesis.

CA-D007 now has zero prospective supporting tests, one prospective null (D02C), and one prospective indeterminate test (D02D).

Native-toolkit verdict:

`NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE`.

See:
- `D02D_LUMO_PROSPECTIVE_READOUT_v0.1.md`
- `d02d/D02D_LUMO_MFR14_v0.1.md`
- `d02d/D02D_LUMO_FINAL_PREEXECUTION_FREEZE_v0.1.md`
- `results/D02D_ARCHIVAL_RECORD_v0.1.json`
- `REPRODUCIBILITY_GUIDE.md`

## D02E opening requirement

D02E is the next prospective CA-D007 experiment.

The selection problem has changed after two prospective outcomes:

- D02C returned `NEITHER_CHANGES` in both directions, so the next system should have independent native evidence that the planned intervention range measurably moves at least one frozen observable.
- D02D returned `INDETERMINATE` because the frozen environmental/operational matching floor left insufficient graded damaged blocks, so D02E must demonstrate control/intervention overlap adequacy before the candidate is selected.

The D02E candidate screen therefore requires, before decisive ordering inspection:

1. at least three ordered perturbation levels;
2. a directly licensed local scalar;
3. an independent organization/carrier observable;
4. automated public-data access;
5. native evidence that the intervention range is strong enough to move at least one of the two observables, without revealing their relative onset;
6. pre-verifiable control/intervention environmental and operational overlap sufficient to meet the frozen completeness floor at every required perturbation level;
7. a strong native comparator;
8. explicit permission for scalar-first, organization-first, simultaneous, single-observable, neither, and non-identifiable outcomes.

This is a power and identifiability correction. It is not a favorable-outcome filter.

## D02E prospective offshore-jacket test: active

D02E is the next prospective CA-D007 test after the D02C null and D02D indeterminate result.

Selected system:
- scaled offshore-jacket bolt-loosening benchmark;
- dataset DOI `10.34810/data1011`, Dataverse version 3.0;
- fixed operational slice: A_1 white-noise excitation;
- graded states: Healthy 12 Nm -> 9 Nm -> 6 Nm -> NoBolt;
- four physical bolt locations;
- 20 original CSV replicates per state;
- 24 acceleration-response channels.

The healthy-only baseline gate is complete and archived before damaged values were opened.

Frozen primary family:
- 8.7890625 Hz;
- 17/20 healthy half-power chi estimates admitted;
- median healthy chi = 0.028856666306254334.

The final damaged-state implementation rules are frozen in `d02e/D02E_FINAL_PREEXECUTION_FREEZE_v0.1.md`.

Reviewer command:

`python chi_architecture/reproduce.py d02e`

The command downloads only the DOI-locked original CSV files required by the frozen A_1 slice, verifies source MD5 values, applies the fixed FDD tracking window, half-power chi, complex mode-shape organization metric, bootstrap/leave-one-out thresholds, completeness logic, and 3-of-4 adjudication.

D02E is specifically designed to correct both prior prospective failure modes without selecting on the desired ordering:
- D02C lacked detectable movement in either frozen observable;
- D02D lacked enough matched graded data to identify the ordering.

D02E therefore requires both measurable native intervention power and complete matched operation before execution, while leaving relative scalar-versus-organization onset unseen.

## Project control

**STATUS:** D01A-D01C and D02A-D02D are complete. D02C is a prospective null and D02D is prospectively indeterminate. CA-D007 remains unconfirmed with unpaid promotion debt.  
**CURRENT GATE:** execute the already-selected and frozen D02E offshore-jacket A_1 analysis without altering the 8.7890625 Hz primary family or MFR-14 decision rules.  
**NEXT ACTION:** run the dedicated D02E archival workflow, archive the result before interpretation, then apply the frozen 3-of-4 support/adverse rule.  
**WHY:** D02E now has a healthy-only selected primary family, 20 matched replicates at every graded state/location, fixed excitation, and automated public access, directly addressing the D02C power and D02D completeness failures without inspecting the desired ordering.  
**USER ACTION:** none. Public-source candidate search and preregistration can proceed autonomously.
