# F-16 GVT Stability Architecture Synthesis v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Status:** INTEGRATIVE ARCHITECTURE SYNTHESIS / NOT A CLAIM PROMOTION
**Domain:** measured nonlinear structural dynamics
**Native benchmark:** F-16 ground-vibration test with clearance/friction nonlinearities at payload mounting interface

## Purpose

Conglomerate the F-16 measured results as pieces of Stability Architecture while preserving their different evidence classes, failures, and native explanation.

This synthesis does not ask whether Stability Inheritance invented the F-16 physics. It asks what the established/native and newly qualified measurements jointly say about how local interface regime, excitation design, and realized multi-location response fit together.

## Evidence lanes

### FullMSine: prospective P0-Q architecture qualification

Evidence class:
PUBLIC EXTERNAL MEASURED / P0-Q / frozen before reserved scoring.

Primary result:
an amplitude-conditioned three-output FRF representation built from Levels 1/3/5/7 outperformed a fixed Level-1 representation at reserved Levels 2/4/6 in the frozen 6.5-8.2 Hz wing-torsion band.

Conditioned/fixed error ratios:
- 24.6 N: 0.53277
- 61.4 N: 0.11669
- 85.7 N: 0.03346

The ordering also held separately at excitation, wing-side, and payload-side outputs.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE.

### SpecialOdd multisine: prospective P0-Q replication

Evidence class:
PUBLIC EXTERNAL MEASURED / P0-Q / independent excitation design with held-out Validation realization.

At 12.2, 49.0, and 97.1 N, the amplitude-specific three-output representation had lower held-out error than the pooled and cross-amplitude representations.

Specific vs pooled:
- 12.2 N: 0.85432 vs 0.95619
- 49.0 N: 0.77370 vs 0.83661
- 97.1 N: 0.92308 vs 0.92486

The high-amplitude margin is small and must remain so in interpretation.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_REPLICATION.

Important failure:
the simple interface-relative proxy H_payload - H_wing did not reproduce the full-response ordering uniformly at low and mid amplitude.

### FullMSine -> SpecialOdd direct transport: P0-D mixed result

Evidence class:
POST-RESULT EXPLORATORY / promotion debt because SpecialOdd target scoring completed before protocol commitment.

At 49.0 N, FullMSine amplitude conditioning modestly improved prediction of SpecialOdd response:
- ratio 0.9544.

At 97.1 N, amplitude conditioning was worse than the fixed low-amplitude reference:
- ratio 1.0434.

Disposition:
CROSS_EXCITATION_MIXED.

This is a central Limit Map result. Scalar excitation amplitude does not define one universal response-architecture mapping across excitation designs.

### Sine sweep: method failure plus P0-D recovery

The prospective v0.1 sine-sweep analysis failed its frozen raw Hilbert-phase input-coordinate gate before producing a response score.

An input-only diagnostic then showed that the experimental chirp itself was recoverable:
- quadratic-phase coordinate qualified all seven levels;
- zero-crossing coordinate independently agreed;
- the raw samplewise Hilbert derivative was the operational failure.

The redesigned v0.2 response analysis is therefore P0-D/post-result.

Its conditioned/fixed ratios were:
- 19.2 N: 0.50706
- 57.6 N: 0.12224
- 86.0 N: 0.03214.

The interface-relative proxy favored conditioning at all three levels in this family.

Evidence role:
ARCHITECTURE_SUPPORTING_NATIVE_EXPLORATORY with promotion debt.

## What the F-16 evidence says together

### 1. One fixed low-amplitude representation is not globally adequate

The strongest clean evidence is the prospective FullMSine result and the independent SpecialOdd replication. The response representation changes materially with operating/excitation regime.

This supports a Stability Architecture principle of **conditional representation adequacy** rather than a universal fixed response object.

### 2. The organization is not reducible to scalar excitation amplitude

Within each excitation family, amplitude/regime conditioning is informative.

Across FullMSine and SpecialOdd, the same amplitude-conditioned map does not transport uniformly.

Therefore the architecture must contain at least one additional conditioning dimension beyond force RMS amplitude. Candidates already licensed by native science include excitation spectral design, steady-state/history construction, nonlinear detection-line structure, and the way interface nonlinearities are sampled.

No single additional variable is promoted from the current data.

### 3. Local interface physics contributes to system-wide organization without defining it alone

The benchmark's native science identifies clearance/friction at the payload mount as a dominant nonlinearity.

FullMSine changes appear at all three outputs, not only at the payload-side sensor.

SpecialOdd shows that a simple payload-minus-wing response coordinate is not a universally adequate carrier proxy.

Sine sweep shows that the same proxy can be informative in another excitation design.

Together this supports:

LOCAL_INTERFACE_REGIME_CONDITIONS_GLOBAL_RESPONSE

while refusing:

SIMPLE_INTERFACE_DIFFERENCE_EQUALS_ARCHITECTURE.

### 4. Architecture is a relation, not merely a richer predictor

The F-16 results are strongest when interpreted as relations among:

- embedded interface regime;
- excitation/operating context;
- multi-location response organization;
- representation validity.

A better response model by itself is not Chi_arc.

The data instead provide native measured pieces from which an architecture-level reconstruction can be constrained.

### 5. Method operability belongs in the Limit Map

The failed sine-sweep raw-phase coordinate is informative.

The physical excitation was present and independently recoverable, but one representation/estimator of the input coordinate was not operational.

Thus representation failure can occur at the measurement/estimation layer without implying absence of the underlying structure.

This parallels the computational history result in which latent history exists but is not always operationally recoverable from noisy observations.

## Current F-16 architecture map

A minimal evidence-compatible schematic is:

embedded payload-interface mechanics
+ excitation design
+ excitation amplitude/regime
+ measurement/representation operator
-> realized multi-location response organization.

This is a working relation map, not a mechanistic equation and not a universal ontology.

The evidence does not justify reducing these terms to one scalar.

## Relation to project notation

### chi

No physical project chi is admitted from the F-16 benchmark by default.

### Chi

The measured multichannel response/modal organization is relevant to the modal/vector layer, but the native FRF objects are not automatically renamed Chi without a project-level admission rule.

### Chi_arc

The F-16 evidence supports the existence of organized system-level response conditioned by embedded interface and excitation regime, but no unique Chi_arc coordinate/object has yet been reconstructed and independently validated.

The correct status is:

ARCHITECTURE_LEVEL_EVIDENCE_PRESENT / CHI_ARC_NOT_YET_UNIQUELY_IDENTIFIED.

## Function Map

Supported:
- AMPLITUDE_CONDITIONED_SYSTEM_RESPONSE_TRANSPORTS_WITHIN_FULLMSINE
- EXCITATION_REGIME_SPECIFIC_RESPONSE_REPLICATES_IN_SPECIALODD
- LOCAL_INTERFACE_REGIME_ASSOCIATED_WITH_GLOBAL_RESPONSE_ORGANIZATION
- CONDITIONAL_REPRESENTATION_ADEQUACY
- INPUT_COORDINATE_STRUCTURE_CAN_BE_RECOVERABLE_WHEN_ONE_ESTIMATOR_FAILS

Exploratory:
- SINESWEEP_AMPLITUDE_CONDITIONED_RESPONSE
- PARTIAL_CROSS_EXCITATION_TRANSPORT

## Limit Map

Supported:
- FIXED_LOW_AMPLITUDE_REPRESENTATION_INSUFFICIENT_ACROSS_DECLARED_REGIME
- AMPLITUDE_ALONE_NOT_A_UNIVERSAL_CROSS_EXCITATION_MAP
- SIMPLE_INTERFACE_DIFFERENCE_PROXY_NOT_UNIFORMLY_DISCRIMINATING
- HIGH_AMPLITUDE_SPECIALODD_SPECIFIC_VS_POOLED_MARGIN_SMALL
- RAW_HILBERT_PHASE_DERIVATIVE_NOT_OPERATIONAL_FOR_SINESWEEP_COORDINATE
- SAME_DATA_REDESIGN_REQUIRES_PROMOTION_DEBT

## Scientific ceiling

The F-16 program materially strengthens the integrated Stability Architecture case.

It does not establish:
- a universal Stability Inheritance law;
- SI-specific added value beyond native structural dynamics;
- a unique Chi_arc object;
- a physical scalar chi;
- a new mechanism of interface nonlinearity;
- a universal amplitude-response law.

The next strongest evidence would come from a different measured hierarchical system with independently characterized source/component and assembly/target objects, rather than additional retuning of F-16.
