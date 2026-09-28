# Physical Hierarchy Parent-Only Pilot Protocol v0.1

**Date:** 2026-09-28  
**Governance:** SymC GOM v1.0  
**Branch:** stability-inheritance  
**Status:** P0-Q METHOD / APPARATUS QUALIFICATION - NOT FROZEN FOR Q1/Q2  
**Scientific ceiling:** known-truth physical qualification only  
**Child coupling:** PROHIBITED in this pilot  
**Decisive Q1/Q2 target exposure:** PROHIBITED

## Purpose

This protocol is the first hands-on physical step after the APQ-2 methods preflight and A5/B5 known-truth method qualification. Its only jobs are to determine whether the proposed parent apparatus can be built reproducibly, whether the measurement chain can support the required native modal/FRF analysis, and what parent-only uncertainty is available for later pre-target equivalence margins.

It does **not** test Stability Inheritance. It does **not** test interface A versus B. It does **not** authorize a child/receiver. It does **not** set a P1 claim.

## Bias and evidence firewall

All data produced under this protocol are P0-Q apparatus/method-qualification data.

Allowed uses:
- determine whether the parent apparatus is mechanically operable;
- estimate unchanged-condition measurement and reassembly variability;
- identify sensor/DAQ defects;
- test reciprocity/passivity/model-consistency code paths;
- test whether individual modes or only modal subspaces are identifiable;
- derive candidate margins for a later APQ freeze.

Prohibited uses:
- compare Q1 interface A versus B assembled outcomes;
- tune a child coupling location to maximize a desired result;
- select an endpoint because it looks favorable;
- claim carrier-resolved inheritance;
- treat parent-only pilot data as untouched P1 evidence.

Any observation that suggests a new scientific endpoint, threshold, comparator, or mechanism enters the Hands-On ledger as exploratory input and carries the appropriate APQ/promotion-debt treatment before scientific use.

## Phase 0 - Hardware identity and safety record

Before excitation, assign an identity to every mechanically relevant object.

Record:
- parent frame/baseplate identity and dimensions;
- station positions and coordinate convention;
- rotor/inertia identity, dimensions, and measured mass;
- shaft identity, diameter, material if known, and unsupported span;
- bearing identity/type and mounting method;
- spring identity, attachment radii/lever arms, free length, and geometry;
- fastener identities and any controlled preload/torque method;
- sensor and excitation hardware identity;
- acquisition device identity;
- software/script version;
- photographs or sketches sufficient to reconstruct geometry.

### Shaft rule

Threaded rod is **not automatically admitted as the torsional shaft**. Before use in the dynamic parent, inspect straightness/runout, bearing fit, thread-contact friction, and visible eccentricity. If it cannot rotate smoothly and repeatably without thread/bearing interference, classify it as frame/preload hardware and use smooth shafting for the dynamic axis.

This is an apparatus-quality decision, not a scientific failure.

## Phase 1 - Single-station buildability

Build one rotor/bearing station on the intended base.

Without connecting the parent coupling spring or second station:
1. check free rotation by hand through the intended motion range;
2. record visible/feelable backlash, binding, stick-slip, bearing play, and axial migration;
3. apply repeated small releases or impulses at several amplitudes;
4. record free-decay time histories if instrumentation is available;
5. repeat after loosening/remounting the bearing station.

### Disposition

- **STATION_BUILDABLE** if the station behaves reproducibly enough to justify a two-station parent pilot.
- **STATION_REDESIGN_REQUIRED** if binding, runout, backlash, or mounting variability dominates the response.
- Do not repair a poor station by adding damping or filtering that hides the mechanical defect.

## Phase 2 - Two-station isolated parent

Assemble parent stations P1 and P2 only. No child and no Q1 interface cartridge.

Use the parent coupling spring and intended base structure. Install inertial/geometry placeholders at any future interface ports if their presence will be part of the eventual parent definition. The parent state used later must be the same adapter state characterized here.

### Coordinate convention

Freeze a simple physical coordinate system before modal analysis:
- theta_1: P1 angular displacement/velocity coordinate;
- theta_2: P2 angular displacement/velocity coordinate;
- positive direction defined physically on the apparatus;
- input locations and sensor signs recorded.

## Phase 3 - Measurement-chain qualification

The preferred measurement object for passivity testing is mechanical mobility when feasible:

Y_ij(j omega) = v_i(j omega) / F_j(j omega).

If the apparatus instead measures displacement or acceleration, preserve the native measurement and document the conversion used for any mobility/passivity check. Do not impose a mobility phase rule directly on receptance or accelerance.

Before modal fitting, record:
- sampling rate;
- record duration;
- anti-alias/filter settings;
- trigger/timing route;
- sensor ranges;
- excitation range;
- number of averages/repeats;
- clipping/saturation status;
- signal-to-noise/coherence diagnostics where available.

Run at multiple excitation amplitudes to detect obvious amplitude dependence, friction, joint chatter, or saturation.

No universal coherence, sample-rate, or phase-error threshold is frozen here. The purpose is to characterize the measurement path and its uncertainty.

## Phase 4 - Same-configuration repeatability block

With the two-station parent left mechanically unchanged, acquire a repeat block sufficient to estimate short-term measurement variability.

**Initial collection target:** 10 repeated excitations/releases under the same configuration. This is a pilot sampling target, not a scientific acceptance threshold and not a stopping rule for later decisive work.

For each repeat, preserve raw data and extract where licensed:
- modal frequency estimates;
- damping estimates with method and uncertainty;
- mode shape / response-vector estimates;
- FRF or transfer-function estimates;
- reciprocity residuals where matched transfer pairs exist;
- mobility dissipative/Hermitian metrics where the measurement form licenses them;
- model rank/conditioning diagnostics.

## Phase 5 - Reassembly repeatability block

Disassemble only the mechanical elements that will later be routinely disturbed by the interface protocol, then restore the identical parent configuration.

**Initial collection target:** at least 5 independent reassembly cycles, with at least 2 response acquisitions per restored configuration.

The number is a pilot information target, not a final equivalence criterion. If variability estimates are visibly unstable across cycles, expand the pilot before deriving margins.

Record for every cycle:
- what was removed/reinstalled;
- fastener/preload procedure;
- bearing/shaft seating notes;
- adapter state;
- anomalies;
- raw data identities.

The goal is to separate measurement repeatability from reassembly/boundary-condition repeatability.

## Phase 6 - Parent-only native-physics checks

### 6.1 Reciprocity

Where the apparatus and coordinates license reciprocity, compare matched transfer pairs using the unchanged-condition repeatability distribution as context.

A fixed 1 dB or fixed phase threshold is not assumed.

### 6.2 Passivity / dissipation

For mobility, examine the drive-point real part and, for multiport data where supported, the eigenvalues of the Hermitian/dissipative part.

A slightly negative estimate is not automatically a physical passivity failure. Compare the magnitude and frequency structure against the parent-only measurement uncertainty and model-identification uncertainty.

### 6.3 Identified-model consistency

If a modal/state-space model is fit, record separately:
- raw-data physical-consistency verdict;
- unconditioned identified-model verdict;
- any conditioned-model verdict.

Check stability, reciprocity where applicable, nonnegative dissipation/passivity where applicable, second-order/Newton consistency, rank/conditioning, and sensitivity to model order.

If raw data are credible but the fitted model is not, classify MODEL_PATH_NOT_QUALIFIED rather than FRAMEWORK_NOT_OPERATIONAL.

## Phase 7 - Mode identity / subspace qualification

Across unchanged repeats and reassembly cycles:
1. attempt ordinary one-to-one mode pairing;
2. record pairing stability, MAC/shape similarity, and uncertainty;
3. if labels rotate or swap in a close-mode sector, construct a matched modal subspace;
4. compute principal angles in a physically justified mass metric or, if unavailable, a common sensor-coordinate metric.

Known-truth method qualification already established that unstable individual labels can coexist with a stable subspace. The physical pilot now determines whether that situation occurs in this apparatus.

Possible parent-only dispositions:
- INDIVIDUAL_MODES_IDENTIFIABLE;
- MODAL_NONIDENTIFIABLE_SUBSPACE_STABLE;
- MODAL_SUBSPACE_NOT_QUALIFIED.

No arbitrary frequency-spacing threshold defines these outcomes.

## Phase 8 - Candidate margin construction

Only after Phases 3-7 are complete may candidate pre-target margins be proposed.

Candidate margins must be based on:
- unchanged-condition measurement repeatability;
- reassembly/boundary repeatability;
- sensor/instrument uncertainty where available;
- model-identification uncertainty where applicable.

Keep separate candidate regions for frequency, damping, modal/subspace geometry, FRF/transfer behavior, and any directly measured architecture-level quantity. Do not compress them into one omnibus tolerance unless the native analysis justifies that reduction.

These are **candidate freeze inputs**, not final frozen values. They require the second APQ adjudication before Q1/Q2.

## Required raw-data manifest

Each physical acquisition must have a manifest row with:

| Field | Required content |
|---|---|
| run_id | unique immutable ID |
| date_time | local timestamp with timezone |
| operator | person running acquisition |
| apparatus_version | geometry/hardware revision |
| configuration | SINGLE_STATION / PARENT_FIXED / PARENT_REASSEMBLED |
| reassembly_cycle | cycle number or n/a |
| excitation_id | hammer/release/actuator identity |
| excitation_level | native units or documented ordinal level |
| input_sensor_id | or n/a if no measured input |
| output_sensor_ids | channel mapping |
| sample_rate | Hz |
| record_duration | seconds |
| filter_settings | anti-alias / processing |
| raw_file | immutable raw-data path/name |
| calibration_pointer | calibration record |
| anomaly_note | none or explicit anomaly |
| outcome_exposure | must be NO_Q1_Q2 |
| code_commit | analysis code SHA |

## Parent-only stop conditions

Stop before any child/Q1/Q2 execution if:
- single-station mechanics remain dominated by binding, backlash, or nonrepeatable friction;
- parent modal/FRF estimates are not reproducible enough to support a stable native representation;
- sensor timing/noise/clipping prevents credible FRF/modal estimation;
- raw data or model path fail physical-consistency checks without a prospectively valid remedy;
- reassembly changes parent identity beyond the candidate repeatability region;
- neither individual modes nor stable subspaces can be identified for the planned contrast;
- a material plan change is required.

A stop here is successful qualification information, not a failed inheritance experiment.

## Pilot closeout packet

Before child coupling, produce:
1. PARENT_HARDWARE_IDENTITY.md
2. PARENT_RAW_DATA_MANIFEST.csv
3. PARENT_MEASUREMENT_QUALIFICATION.md
4. PARENT_REPEATABILITY_RESULTS.csv
5. PARENT_MODAL_SUBSPACE_QUALIFICATION.md
6. PARENT_CANDIDATE_MARGIN_PACKET.md
7. updated APQ objection ledger
8. updated WORKING_INVESTIGATION.md

Only after the second APQ adjudication may the plan be frozen for Q1/Q2.

## Hands-On use

The Hands-On workbook sheet is the proper intake lane for physical observations such as:
- "this bearing sticks near one angle";
- "threaded rod visibly wobbles";
- "one spring attachment chatters";
- "P1/P2 modes exchange labels between repeats";
- "the raw FRF is reciprocal but the fitted model is not";
- "the second station changes the first station's baseline more than expected."

These observations remain exploratory until classified and routed through the evidence/APQ structure.
