# Chi Architecture Reproducibility Guide

**Governance:** SymC General Operations Manual v0.8.6  
**Reproducibility status:** R1 and R2 are demonstrated for the listed executable experiments through frozen GitHub Actions reference runs. R3 evidence reconstruction is experiment-specific and is identified in the corresponding source contract/readout.

This guide is reviewer-first. The supported interface is the production entry point:

`python chi_architecture/reproduce.py <experiment>`

The numbered verification sections below are canonical under GOM v0.8.6. Detailed provenance notes follow them.

## V1. D01C fixed-spectrum non-normal map

**[CLAIM]** In the frozen D01C constructions, identical asymptotically stable eigenvalues do not determine finite-time amplification or perturbation robustness; the standard nonmodal toolkit is sufficient to describe the effect.

**Inputs:** branch `chi-architecture-p0`; `D01C_PREEXECUTION_FREEZE_v0.1.json`; DOI-independent synthetic construction encoded in production code.

**Command:**

```bash
python chi_architecture/reproduce.py d01c
```

**Expected output:** exit status 0; `D01C_NONNORMAL_DOMAIN_MAP_v0.1.json`; 26 cases; maximum spectral residual below `1e-10`; status `REFUTED_WITHIN_FROZEN_CONSTRUCTION` for eigenvalue-only sufficiency.

Reference run: `35809467796`.

## V2. D02A CsPbBr3 physical calibration

**[CLAIM]** The frozen CsPbBr3 source data support carrier-resolved reorganization and damping transformation while lowercase chi is refused where same-condition natural frequency is not independently licensed.

**Inputs:** source identities and hashes frozen in the D02A source contract and execution archive.

**Command:**

```bash
python chi_architecture/reproduce.py d02a
```

**Expected output:** exit status 0; `D02A_CSPBBR3_PHYSICAL_RESULT_v0.2.json`; parser/source guards pass; lowercase-chi refusal is preserved; no master scalar is emitted.

Reference run: `35816379440`.

## V3. D02B four-bolt physical perturbation map

**[CLAIM]** In the frozen four-bolt plate experiment, moderate interface perturbation can reorganize the full-field response while local modal chi remains similar at frozen resolution, whereas stronger perturbation transforms or defeats the frozen scalar representation.

**Inputs:** Zenodo DOI `10.5281/zenodo.20038951`; exact source hashes and mapping in `d02b/`; 51-point matched spatial support.

**Command:**

```bash
python chi_architecture/reproduce.py d02b
```

**Expected output:** exit status 0; seven retained families; 18 torque states; 126 scalar attempts; 28 primary comparisons; frozen result files and manifest emitted. The archived interpretation records 16/28 10-to-5 Nm comparisons with similar chi plus embedded reorganization, and 11/11 comparable 10-to-0 Nm pairs with transformed chi.

Reference run: `35823640290`.

## V4. D02C prospective wind-blade test

**[CLAIM]** The first prospectively frozen external test of CA-D007 returns a null in both selected directions under the frozen thermal and completeness controls.

**Inputs:** Zenodo DOI `10.5281/zenodo.18427836`; source hashes in `d02c/D02C_WIND_BLADE_CONTRACT_v0.1.md`; exact mapping and onset-completeness rules in `d02c/`.

**Command:**

```bash
python chi_architecture/reproduce.py d02c
```

**Expected output:** exit status 0; `D02C_WIND_BLADE_RESULT_v0.1.json`; X ordering `NEITHER_CHANGES`; Z ordering `NEITHER_CHANGES`; `ca_d007_domain_specific_support=false`.

Reference run: `35866859136`.

## V5. D02C prospective null record

**[CLAIM]** D02C is a prospectively frozen external test that returns `NEITHER_CHANGES` in both selected directions under the frozen thermal and completeness firewalls, so CA-D007 is not supported by D02C.

**Inputs:** Zenodo DOI `10.5281/zenodo.18427836`; D02C source contract, exact mapping, onset-completeness rule, and archived execution record.

**Command:**

```bash
python chi_architecture/reproduce.py d02c
```

**Expected output:** exit status 0; X ordering `NEITHER_CHANGES`; Z ordering `NEITHER_CHANGES`; `ca_d007_domain_specific_support=false`; full result SHA-256 `9b1f52945acc5cc43ec8590e9950effba65ef37c8e89523f20354b17fd079ab9`.

Reference run: `35866859136`.

## V6. D02D LUMO prospective ordering test

**[CLAIM]** The second prospectively frozen CA-D007 test is indeterminate because the frozen environmental/operational matching floor prevents a complete healthy -> 010 -> 111 onset ordering at all three damage locations.

**Inputs:** LUMO DOI `10.25835/0027803`; six source resources and SHA-256 hashes in `D02D_REPRO_MANIFEST_v0.1.json`; frozen MFR-14 and final preexecution analysis freeze in `chi_architecture/d02d/`.

**Command:**

```bash
python chi_architecture/reproduce.py d02d
```

**Expected output:** exit status 0; `D02D_LUMO_PROSPECTIVE_RESULT_v0.1.json`; DAM3, DAM4, and DAM6 each `ORDERING_NON_IDENTIFIABLE`; program outcome `INDETERMINATE`; native-toolkit verdict `NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE`; full result SHA-256 `f372bb0e7e1069fe731e49b8831c3d39559eea5c61679df42e6a428e4f92c111`.

Reference run: `35904120749`.

## V7. Master smoke test

**[CLAIM]** The production entry points for the mature D01C and D02A-D02D experiments execute through the documented interface and reproduce their frozen status outputs.

**Inputs:** branch `chi-architecture-p0`; Python 3.12 environment; pinned dependencies from `chi_architecture/requirements-p0.txt`; network access to the DOI-locked physical source archives.

**Command:**

```bash
set -e
python chi_architecture/reproduce.py d01c
python chi_architecture/reproduce.py d02a
python chi_architecture/reproduce.py d02b
python chi_architecture/reproduce.py d02c
python chi_architecture/reproduce.py d02d
printf 'SYMC_CHI_ARCHITECTURE_SMOKE_TEST=PASS\n'
```

**Expected output:** every command exits 0 and the final line is exactly:

`SYMC_CHI_ARCHITECTURE_SMOKE_TEST=PASS`

This smoke test demonstrates executable package continuity. It does not convert physical qualification, a prospective null, or an indeterminate prospective test into independent replication.

## Detailed provenance and experiment notes

## D01C: minimum reproduction path

Requirements:

- Git
- Python 3.12
- a standard shell / terminal

Run:

```bash
git clone https://github.com/SymC-Universe/Foundations.git
cd Foundations
git checkout chi-architecture-p0
python -m pip install -r chi_architecture/requirements-p0.txt
python chi_architecture/reproduce.py d01c
```

The final command does the scientific work. It:

1. validates the frozen D01C contract;
2. runs the D01C regression/scientific-guard tests;
3. executes every frozen D01C case;
4. writes the full machine-readable result;
5. writes a compact summary;
6. writes a human-readable result card;
7. records the realized Python/NumPy/SciPy environment;
8. hashes the complete reproduction surface into one manifest.

## Outputs

All local outputs land under `chi_architecture/results/`:

- `D01C_NONNORMAL_DOMAIN_MAP_v0.1.json` — full result;
- `D01C_SUMMARY_v0.1.json` — compact result;
- `D01C_RESULT_CARD_v0.1.md` — human-readable result;
- `D01C_ENVIRONMENT_v0.1.txt` — realized runtime;
- `D01C_REPRO_MANIFEST_v0.1.json` — SHA-256 manifest.

A reviewer normally needs only the result card plus the manifest after running the single command.

## GitHub-only reproduction

The repository also contains `.github/workflows/chi-architecture-d01c.yml`.

Running that workflow executes the same single entrypoint and uploads **one artifact bundle** named:

`chi-architecture-d01c-v01`

The bundle contains the five outputs above. There is no multi-artifact scavenger hunt.

## Scientific provenance

The pre-result scientific surface is frozen in:

`chi_architecture/D01C_PREEXECUTION_FREEZE_v0.1.json`

The active resume state is always:

`chi_architecture/CURRENT_CHECKPOINT.md`

The literature/novelty firewall is:

`chi_architecture/D01C_LITERATURE_POSITION.md`

## Reproduction standard

The archival claim is reproduced only when:

- tests pass;
- all frozen cases are present;
- the spectral-residual guard passes;
- the run emits no master chi;
- the manifest hashes the exact local files used and produced.

The `--skip-tests` option exists only for development debugging and does not qualify an archival reproduction.


## Archived reference execution

The first frozen D01C archival reproduction is permanently indexed in:

`chi_architecture/results/D01C_ARCHIVAL_RECORD_v0.1.json`

Reference execution:

- execution commit: `9818612abae93e460af7ab45281fd9a5e4ae68e7`
- GitHub Actions run: `35809467796`
- artifact: `chi-architecture-d01c-v01`
- artifact ID: `10728829675`
- artifact digest: `sha256:7178cd28a579b17d35da57e37ebfccb4a540ac6f0f23a688233d9f2c665c305e`
- full result SHA-256: `ab24c3dcb9490d1b07c9043b922e326f149cf71fd3522c67e2b54c1d53206d38`

The compact result card and summary are stored in the repository. The full result is regenerated by the one-command entrypoint, so long-term reproduction does not depend on the temporary GitHub Actions artifact remaining available.


## D02A: physical CsPbBr3 calibration

The supported reviewer command is:

```bash
python chi_architecture/reproduce.py d02a
```

That single entrypoint:

1. runs the preserved v0.1 source/parser guards and the corrected v0.2 matrix-parser tests;
2. downloads the two exact publisher source workbooks;
3. verifies the frozen SHA-256 hashes;
4. reconstructs the valid six-row M-point linewidth table;
5. reconstructs the three frozen M-R S(Q,E) matrices;
6. applies the frozen per-q normalized shape comparison;
7. preserves lowercase-chi refusal;
8. writes the full v0.2 result, compact summary, result card, environment record, and manifest.

The current D02A outputs are:

- `D02A_CSPBBR3_PHYSICAL_RESULT_v0.2.json`
- `D02A_CSPBBR3_SUMMARY_v0.2.json`
- `D02A_RESULT_CARD_v0.2.md`
- `D02A_ENVIRONMENT_v0.2.txt`
- `D02A_REPRO_MANIFEST_v0.2.json`

The original v0.1 parser failure is intentionally preserved in:

`d02_cspbbr3/D02A_V0.1_POSTEXECUTION_INTEGRITY_AUDIT.md`

The corrected scientific readout is:

`d02_cspbbr3/D02A_PHYSICAL_CALIBRATION_READOUT_v0.2.md`

The reference v0.2 execution is indexed in:

`results/D02A_EXECUTION_ARCHIVE_v0.2.json`

Reference workflow:

- run: `35816379440`
- artifact: `chi-architecture-d02a-physical-v02`
- artifact ID: `10731212172`
- artifact digest: `sha256:049c4648f71b13e30a5470ebfeaf06cea3a482f642826aec06e92efb461528a9`
- full result SHA-256: `234315fb8e181c1538844efa6a94776e8dcdfaf9e67fda85006982584e511f2e`
- manifest SHA-256: `c3ac58b6b9779412dc8541644a6cb26cb5976b2093f2f97b3b976b9277821442`

D02A does not require manual spreadsheet editing or manual figure digitization.


## D02B: four-bolt physical inheritance test

Reviewer-facing reproduction remains one scientific command:

```bash
git clone https://github.com/SymC-Universe/Foundations.git
cd Foundations
git checkout chi-architecture-p0
python -m pip install -r chi_architecture/requirements-p0.txt
python chi_architecture/reproduce.py d02b
```

The D02B wrapper automatically downloads the public Zenodo support bundles and 635 MB raw archive, verifies the published checksums, uses the exact 51-point intersection across all 18 torque states, reconstructs the seven source-retained resonance families, applies the frozen half-power admission/refusal rules, and emits one compact result bundle.

Reviewers do not select or unpack the 1,838 raw response files manually.

The frozen scientific contract is in `chi_architecture/d02b/`. The raw source is DOI `10.5281/zenodo.20038951`.


## D02B archived reference execution

The first successful frozen D02B physical reproduction is indexed by:

`chi_architecture/results/D02B_ARCHIVAL_RECORD_v0.1.json`

Reference execution:

- execution commit: `cd4127b963cf2057841dff320c547ec7f3fad73d`
- GitHub Actions run: `35823640290`
- artifact: `chi-architecture-d02b-four-bolt-v01`
- artifact ID: `10734281523`
- artifact digest: `sha256:3730a4a6db3803501fe35c74f740836cdf86a3d21d95f2de2707748fa1b0af1f`
- full result SHA-256: `d7e0001413ef438aea2d8ea8757f7b4eeb8d6dab5ecfdf62be02b9f2575d4f10`
- reproduction manifest SHA-256: `beb792895ba4d98afd29848623422dd86be574727144877a291087fc809b465f`

The artifact is convenient but not required for long-term reproduction. The one-command entrypoint regenerates the full result from the DOI-locked Zenodo sources.


## D02C: prospective wind-blade ordering test

D02C is reproduced through the same one-command interface:

```bash
git clone https://github.com/SymC-Universe/Foundations.git
cd Foundations
git checkout chi-architecture-p0
python -m pip install -r chi_architecture/requirements-p0.txt
python chi_architecture/reproduce.py d02c
```

The wrapper automatically downloads and checksum-verifies the locked Zenodo OMA, climate, baseline-acceleration, intervention-acceleration, and dry-run control assets for DOI `10.5281/zenodo.18427836`.

The prospectively frozen D02C test compares:
- local/modal chi from source LSCF damping ratio;
- independent three-sensor cross-spectral modal-vector organization;
- the published climate-chamber icing intervention on a common 10-minute grid;
- conservative pre-spray and dry-run thermal sensitivity controls.

Reviewers do not manually select windows, modes, or sensor files.


## D02C archived prospective execution

Reviewer command:

```bash
python chi_architecture/reproduce.py d02c
```

Reference execution:

- execution commit: `0401811345c037bfee77d8471cbc295acbb12dd8`
- GitHub Actions run: `35866859136`
- artifact: `chi-architecture-d02c-wind-blade-v01`
- artifact ID: `10752811690`
- artifact digest: `sha256:071dae782bafc8b0174eafb3d3832e94d88b76a3fa647cb0ccf5b56aeb9b4211`
- full result SHA-256: `9b1f52945acc5cc43ec8590e9950effba65ef37c8e89523f20354b17fd079ab9`
- reproduction manifest SHA-256: `9c5483a003aa1f3a4dbcc1691e6936cd1fbbbf0b79486b4ef9e70fd47ba9f48f`

Outcome:

- X: `NEITHER_CHANGES`
- Z: `NEITHER_CHANGES`
- CA-D007 support: false

The archived artifact is convenient but unnecessary for long-term reproduction because the one-command entrypoint reacquires the DOI-locked Zenodo sources and regenerates the complete result.


## D02D opening note

D02D is the second prospective CA-D007 experiment. It is not yet an executable verification section because the target system and complete MFR-14 have not been frozen.

Candidate selection is restricted to systems with at least three graded perturbation levels, a directly licensed local scalar, an independent organization observable, automated public-data access, and prior native evidence that the intervention range measurably changes at least one frozen observable while leaving the relative onset ordering uninspected.

Once D02D is frozen and executed, it will receive the next canonical verification number rather than being inserted retroactively into V1-V5.


## D02D pending canonical verification

D02D has now reached the final preexecution stage. Once the first frozen execution is archived, it will receive canonical verification section V6.

Planned production command:

```bash
python chi_architecture/reproduce.py d02d
```

The command automatically acquires the six DOI-locked LUMO exemplar resources, applies the frozen campaign-paired environmental controls, reconstructs the X/Y FDD mode families, estimates modal chi through frozen half-power bandwidth, computes complex-MAC organization, and emits one compact artifact bundle.

No reviewer will manually choose damage locations, severity files, modes, channels, or thresholds.


## D02D archived prospective execution

Reference execution:

- execution commit: `856ed0ae63df13b557fba8a4cfd44aa8c720c32e`
- GitHub Actions run: `35904120749`
- artifact: `chi-architecture-d02d-lumo-v01`
- artifact ID: `10770159354`
- artifact digest: `sha256:bf84f37f6250b6cd2b96a8006cb39ef32c4eecef1cc82049f3b1a10c13412832`
- full result SHA-256: `f372bb0e7e1069fe731e49b8831c3d39559eea5c61679df42e6a428e4f92c111`
- reproduction manifest SHA-256: `9af1dfbdf6f9d5dac7a0a61d46029a3390ab9cf0431876bface750f4695dfe37`

Outcome:

- DAM3: `ORDERING_NON_IDENTIFIABLE`;
- DAM4: `ORDERING_NON_IDENTIFIABLE`;
- DAM6: `ORDERING_NON_IDENTIFIABLE`;
- program outcome: `INDETERMINATE`.

The archive record also preserves the post-hash/pre-archive-commit result-card exposure as an integrity-sequencing deviation. No scientific or computational content changed after that exposure.


## D02E prospective opening note

D02E is not yet an executable verification section. Under GOM v0.8.6, it will receive the next V-number only after the source contract, MFR-14 record, production entry point, expected output, and first archived execution exist.

The candidate-selection gate is itself fixed by the prospective failures already observed.

**[CLAIM]** The D02E selection process must improve power against the two prior prospective failure modes without selecting on the desired scalar-versus-organization ordering.

**Inputs:** D02C prospective null record, D02D prospective indeterminate record, CA-D007 ledger entry, and the active GOM v0.8.6.

**Verification before candidate promotion:**

```text
REQUIRE >=3 graded perturbation levels
REQUIRE licensed local scalar
REQUIRE independent organization observable
REQUIRE automated public source access
REQUIRE native evidence that >=1 frozen observable changes over the intervention range
REQUIRE pre-verifiable environmental/operational overlap sufficient for every graded level
REQUIRE relative scalar-versus-organization onset remains uninspected
REQUIRE native comparator
```

**Expected output:** either a frozen D02E candidate/source contract satisfying every requirement above, or the explicit status `NO_ELIGIBLE_D02E_SYSTEM`. No criterion is relaxed because a candidate appears scientifically attractive.

This opening note is selection provenance, not a substitute for the eventual executable D02E V-section.


## D02E prospective offshore-jacket reproduction

D02E is the third prospective CA-D007 test and directly incorporates the power/identifiability lessons from D02C and D02D.

The healthy-only baseline selection is archived before any damaged A_1 response file is used:

- workflow run: `35944132810`
- artifact: `d02e-healthy-baseline-selection-v01`
- artifact ID: `10786042762`
- artifact digest: `sha256:ed50d5fd65b032721c5f20be928514bbba859bdf13b9c07007a8d92305038d5c`
- result SHA-256: `8f4f554439bc520940f24b2b70f704c9a48e7c78c4c9828643631f442058f3bc`
- selected primary family: `8.7890625 Hz`
- admitted healthy chi replicates: `17/20`

Reviewer command:

```bash
git clone https://github.com/SymC-Universe/Foundations.git
cd Foundations
git checkout chi-architecture-p0
python -m pip install -r chi_architecture/requirements-p0.txt
python chi_architecture/reproduce.py d02e
```

The one command automatically retrieves the frozen A_1 original CSV slice from DOI `10.34810/data1011` and analyzes:

- Healthy 12 Nm, 20 replicates;
- 9 Nm, four locations x 20 replicates;
- 6 Nm, four locations x 20 replicates;
- NoBolt, four locations x 20 replicates.

Dataverse-generated `.tab` derivatives are excluded.

The implementation reproduces the healthy 8.7890625 Hz family, applies the fixed +/-5% tracking window, half-power modal chi, complex FDD mode-shape dissimilarity, 10,000-resample bootstrap scalar intervals, healthy leave-one-out organization threshold, >=16/20 completeness floors, onset blocking after an earlier non-identifiable state, and the frozen symmetric 3-of-4 domain adjudication.

Reviewers do not choose damage locations, mode families, excitation levels, thresholds, channel subsets, or replacement estimators.



## D02E archived prospective execution

Reference execution:

- execution commit: `4711271eb0bee1b22760fa6885c56c11e139abc7`;
- GitHub Actions run: `36019987959`;
- artifact: `chi-architecture-d02e-jacket-v01`;
- artifact ID: `10816468481`;
- artifact digest: `sha256:952b78b21005bc67eb9af5e98f5f5e0994593f2add5109d25ce8b644b3e282f3`;
- full result SHA-256: `81dd533d98c31137eb65db4a6a572bce844e0be8094d724cb686207f234497b0`;
- reproduction manifest SHA-256: `9abf3f526c6b8553e0505261e623230ac885d29cb7dd1e27c20b6ffdfd0a2ae6`.

Outcome:

- level_1: `ORDERING_NON_IDENTIFIABLE`;
- level_2: `ORDERING_NON_IDENTIFIABLE`;
- level_3: `ORDERING_NON_IDENTIFIABLE`;
- level_4: `ORDERING_NON_IDENTIFIABLE`;
- domain result: `INDETERMINATE`.

The first damaged 9 Nm level admitted only 8/20, 3/20, 2/20, and 15/20 half-power chi estimates across the four locations, below the frozen 16/20 scalar floor in every stratum.

This is the measured reason D02E is indeterminate. A later experiment cannot claim to solve D02E merely by adding replicates or loosening thresholds. It must prospectively demonstrate a perturbation-robust scalar measurement route before relative onset is inspected.

Reviewer reproduction:

```bash
python chi_architecture/reproduce.py d02e
```

The command reacquires and MD5-verifies all 260 original A_1 CSV files from DOI `10.34810/data1011`. No manual damage-state, location, mode, or threshold selection is required.



## D02F opening note

D02F exists specifically to resolve the measured D02E scalar-admission failure.

The next candidate must demonstrate, before relative onset inspection:

- at least three graded perturbation levels;
- a source-native local scalar that remains directly measurable across every required level;
- preference for source-reported damping, Q, linewidth, or decay over a fragile half-power-only route;
- an independent organization/carrier observable at every level;
- pre-verifiable completeness;
- native evidence that the intervention range moves at least one relevant observable or response;
- automated public-data access;
- unseen relative scalar-versus-organization onset;
- a strong native comparator.

This is an identifiability correction, not a favorable-outcome filter.

Reviewer-facing target remains:

`python chi_architecture/reproduce.py d02f`


## D02F prospective FLOOD-SHAB reproduction

STATUS

D02F is frozen under `D02F_FLOOD_SHAB_MFR14_v0.1.md` and executes through the common reviewer interface.

CURRENT GATE

First decisive execution must be archived before interpretation.

REPRODUCTION

```bash
git clone https://github.com/SymC-Universe/Foundations.git
cd Foundations
git checkout chi-architecture-p0
python -m pip install -r chi_architecture/requirements-p0.txt
python chi_architecture/reproduce.py d02f
```

WHAT THE COMMAND DOES

The wrapper automatically:
- downloads and MD5-verifies the DOI-locked FLOOD-SHAB CSV, data dictionary, mapping, and README;
- reconstructs the frozen E1-E4 water-level strata;
- uses source-reported modal damping ratio as local chi;
- constructs phase-invariant complex mode-shape organization;
- conditions each event record on 30 matched pre-event controls using the frozen temperature, wind, and operational-intensity covariates;
- executes the 10,000-resample frozen bin-level onset test;
- reports mode 1 as primary and modes 2-3 as secondary robustness only;
- writes one compact result bundle and SHA-256 manifest.

WHY

D02F directly addresses D02E's scalar-admission failure by using a source-reported damping ratio with pre-verified same-record complex mode-shape completeness across every event-water stratum.

USER ACTION

NONE.


## D02F archived prospective execution

STATUS

D02F completed successfully and returned a clean prospective null.

REFERENCE EXECUTION

- execution commit: `558b46a77e0dd2a0709e75b541d20aed231a738e`;
- GitHub Actions run: `36036875749`;
- artifact: `chi-architecture-d02f-flood-shab-v01`;
- artifact ID: `10824482673`;
- artifact digest: `sha256:457977822e445009dda266765c56fc26758f7e6e84e1a28e705038ac52a46118`;
- full result SHA-256: `0cf6d223b4c788f9d9239009029558a46601dbfa30a47a12af8f71a8f9bb6919`;
- reproduction manifest SHA-256: `4bd6270a5e3b927622aa68063bea56782aca22df94cfbd222eeb03d3bc744196`.

OUTCOME

Primary mode 1:
`NEITHER_CHANGES`.

All four bins retained >=10 valid matched-EOV rows, so this is not an identifiability failure.

REPRODUCTION

```bash
python chi_architecture/reproduce.py d02f
```

NEXT EXPERIMENT REQUIREMENT

D02G may proceed only as a target-observable power correction. Before relative onset is inspected, independent native evidence must establish that the intervention range changes the exact licensed scalar or exact organization observable. Generic response power is no longer sufficient.
