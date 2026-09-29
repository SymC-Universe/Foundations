# BRB Long-Term History Architecture Candidate v0.1

**Date:** 2026-09-29
**Governance:** SymC GOM v1.0
**Status:** EXPLORATORY PLAN CANDIDATE / NOT FROZEN
**Evidence exposure:** published campaign design and published wear results only; no long-term raw response values inspected
**Evidence role if later tested:** architecture qualification, not wear-mechanism novelty

## Why this is a distinct question

The published long-term BRB study already establishes that wear accumulates at the joint interface and that dynamic properties evolve. Repeating "wear changes dynamics" would therefore add little.

The unresolved architecture question is whether later response can be decomposed into information associated with:

1. contemporaneous operating/excitation level;
2. accumulated loading/wear history;
3. assembly epoch / reassembly state.

The official campaign contains five random-FRF and step-sine checkpoints suitable in principle:

- initial / FirstRound Before: 0 h accumulated monotone loading;
- FirstRound After: 4 h;
- SecondRound After: 8 h;
- ThirdRound Before: after disassembly, scan, cleaning, and reassembly, still approximately 8 h accumulated prior loading;
- ThirdRound After: after a further 4 h, approximately 12 h accumulated loading.

The comparison between SecondRound After and ThirdRound Before is especially valuable because accumulated loading history is approximately held while the assembly is broken and re-established.

## Candidate architecture question

At matched contemporaneous excitation, can later measured response be explained by current operating level alone, or is additional information about accumulated loading history and reassembly epoch required?

This is not a claim that "memory exists." Native wear science already establishes physical history dependence.

The prospective value would be in qualification:

- CURRENT_STATE_SUFFICIENT;
- HISTORY_ADDS_FOR_TASK;
- REASSEMBLY_STATE_ADDS_FOR_TASK;
- HISTORY_PRESENT_BUT_RESPONSE_RELATION_NOT_IDENTIFIABLE;
- MIXED_HISTORY_ARCHITECTURE.

## Candidate representation

Use native empirical response objects first, preferably random-FRF transfer estimates from measured excitation force to all qualified acceleration channels.

Do not force chi, Chi, or Chi_arc before native response qualification.

Potential project-layer interpretation after native analysis:

- chi: may later be admitted only if a specific modal damping coordinate is independently licensed;
- Chi: may be admitted if a repeatable modal/subspace object is identified;
- Chi_arc: may be considered only if a separate architecture-level reconstruction is supported;
- history H: candidate explanatory coordinate is the experimentally declared loading/assembly state, not an invented latent variable.

## Candidate nested comparison

After metadata/layout qualification, a frozen test could compare:

M0: response predicted from contemporaneous excitation level only.

M1: M0 plus accumulated monotone-loading duration/state using the pre-reassembly sequence 0 h, 4 h, 8 h.

Reassembly diagnostic: compare the observed ThirdRound-Before response with the M1 expectation at approximately 8 h. This estimates whether breaking/reforming the assembly creates a response offset not explained by accumulated history alone.

M2: M1 plus the prospectively defined reassembly offset/state.

Held-out target: ThirdRound-After at approximately 12 h, provided the metadata support a clean matched-excitation target and the model can be frozen before numeric response values are opened.

This structure is only a candidate. Exact excitation levels, channels, frequency support, estimator, train/test partition, and metrics must be frozen after metadata-only intake and before signal scoring.

## Bias controls

Do not:

- choose a frequency band from observed differences;
- choose excitation levels based on which show the largest wear effect;
- collapse reassembly and wear into one history variable after seeing results;
- infer a physical memory mechanism beyond native wear/interface science;
- promote the published 2025 result into a new SI claim.

Use every excitation level common to the required state blocks, or define a metadata-only selection rule before scoring.

## Relation to current architecture evidence

Short BRB ringdown:
- modal skeleton persists while fine Chi geometry reorganizes with amplitude;
- local chi tracks but is redundant with amplitude for modal prediction.

Long-term BRB candidate:
- asks whether the physical carrier/interface evolves enough that the mapping from current operating condition to later response itself changes across hours and reassembly.

Together these time scales can test whether "state" must include both fast operating regime and slow carrier history in this domain.

## Stop / refusal conditions

Do not proceed to raw scoring if:

- canonical OSF identity remains ambiguous;
- the five state blocks cannot be identified from metadata alone;
- matched contemporaneous excitation conditions do not exist across the needed states;
- raw data access would require downloading the entire approximately 10 GB project when a provenance-clean bounded subset cannot be defined;
- the proposed held-out target has already been numerically inspected before protocol freeze.

