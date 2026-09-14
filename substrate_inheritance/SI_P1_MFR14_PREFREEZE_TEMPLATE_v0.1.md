# SI future P1 / MFR-14 prefreeze template v0.1

**Date:** 14 September 2026  
**Status:** `TEMPLATE_ONLY_NOT_FROZEN`  
**Program authority:** SymC General Operations Manual v0.8.0  
**Purpose:** prepare the SI-specific information that a future physical confirmatory record will need without prematurely choosing a claim, threshold, comparator, target, or decisive evidence.

> This template does **not** replace or reinterpret the authoritative MFR-14 specification in the GOM. At any actual P1 freeze, the completed record must be reconciled line-by-line with the then-current authoritative GOM before decisive evidence is opened.

## A. Claim identity

- Claim ID: `TBD`
- Exact one-sentence claim: `TBD`
- Claim maturity before freeze: `P0-D / P0-Q / other`
- Why the claim is worth a confirmatory test: `TBD`
- Explicit nonclaims: `TBD`

## B. Native scientific task

- Domain/system: `TBD`
- Native governing object(s): `TBD`
- Parent object: `TBD`
- Child/coupled object: `TBD`
- Physical carrier/subspace: `TBD`
- Local versus embedded distinction: `TBD`
- Required scalar view, if any: `TBD / NOT_APPLICABLE`
- Required modal/subspace view: `TBD / NOT_APPLICABLE`
- Required conglomeration/system view: `TBD / NOT_APPLICABLE`
- Additional/open-channel object: `TBD / NONE`

## C. Prospective SI correspondence

- Parent characterization source/provenance: `TBD`
- Parent characterization date/hash: `TBD`
- Child target still unopened at freeze: `YES REQUIRED`
- Shared coordinate/degree-of-freedom map: `TBD`
- Carrier/subspace correspondence rule: `TBD`
- Transformation/prediction rule: `TBD`
- Degeneracy/crowding handling: `TBD`
- Non-normal handling if relevant: `TBD / NOT_APPLICABLE`
- Representation-invariance requirement: `TBD`

## D. Evidence class and epistemic states

For each required object record separately:

- existence/admission;
- participation;
- observability;
- identifiability;
- estimate;
- regime/branch placement;
- uncertainty/tolerance;
- final admission/refusal.

Any state not scientifically applicable should be marked `NOT_APPLICABLE`, not filled by analogy.

## E. Prospective prediction

- Exact predicted target quantity: `TBD`
- Prediction unit/representation: `TBD`
- Directional/quantitative expectation: `TBD`
- Uncertainty envelope: `TBD`
- Decision statistic: `TBD`
- Predeclared success/failure/refusal logic: `TBD`
- Missing-data rule: `TBD`
- Nonidentifiability rule: `TBD`

## F. Intervention / counterfactual

- Parent intervention: `TBD`
- Why intervention is physically separable from target fitting: `TBD`
- Predicted child change: `TBD`
- Counterfactual/null expectation: `TBD`
- Failure condition: `TBD`

If the exact claim does not require intervention, justify that explicitly rather than silently omitting the gate.

## G. Specificity and negative controls

Potential controls, frozen only when scientifically appropriate:

- frequency-only matching;
- same-spectrum carrier scramble;
- generic-parent control;
- coupling rewire;
- coordinate permutation / representation control;
- unrelated parent control;
- native-domain null;
- exact tie/nonidentifiability known-bad case.

For each selected control:

- implementation: `TBD`
- expected behavior: `TBD`
- decision rule: `TBD`

## H. Native comparator

- Frozen scientific task: `TBD`
- Strongest fair native comparator: `TBD`
- Comparator version/settings: `TBD`
- Why it answers the same task: `TBD`
- Same evidence/uncertainty inputs: `TBD`
- SI added-value decision categories: `ADDS / TIES / WORSE / INCOMPARABLE / NO_NATIVE_COMPARATOR`
- Good-faith nearest-method search record: `TBD`

`NO_NATIVE_COMPARATOR` may be used only after the search is complete for the frozen task. It does not itself establish `ADDS`.

## I. Function/Limit placement

- Expected ordinary functioning regime: `TBD`
- Declared limit regime/question: `TBD`
- Why the target was selected independently of the desired result: `TBD`
- Rare/extreme-system proportionality control: `TBD / NOT_APPLICABLE`

## J. Hierarchical closure, if activated

- Reduced subsystem: `TBD`
- Higher-level question: `TBD`
- Quantities that must be preserved: `TBD`
- Full/unreduced reference: `TBD`
- Reduction/native comparator: `TBD`
- Closure uncertainty: `TBD`
- Supported/partial/failed/unresolved rule: `TBD`

No single generic “closure score” is required.

## K. Recovery/resilience, if activated

- Perturbation: `TBD`
- state metric: `TBD`
- finite-time amplification metric: `TBD`
- asymptotic return metric: `TBD`
- reorganization criterion: `TBD`
- resilience interpretation ceiling: `TBD`

Asymptotic stability does not imply finite-time resilience.

## L. Decisive evidence independence

- Decisive dataset/system: `TBD`
- Evidence not used for architecture/threshold tuning: `YES REQUIRED`
- Blind/temporal freeze mechanism: `TBD`
- Access/opening event: `TBD`
- Audit trail: `TBD`

## M. Multiplicity and stopping

- Number of primary confirmatory tests: `TBD`
- Secondary/exploratory tests: `TBD`
- Multiplicity treatment: `TBD`
- Sequential stopping rule: `TBD`
- Mechanical retry rule: `TBD`
- Scientific HOLD rule: `TBD`

## N. Falsification

The record must specify what result would:

- support only substrate influence;
- support conditional inheritance but not full inheritance;
- support the full frozen inheritance claim;
- make the claim nonidentifiable;
- falsify the proposed parent-to-child relation;
- show SI adds no value over the native comparator;
- trigger a science-changing redesign rather than a retry.

## O. Provenance and reproducibility

- code commit: `TBD`
- environment lock: `TBD`
- source hashes: `TBD`
- mapping/contract hashes: `TBD`
- known-truth tests: `TBD`
- negative/mutation tests: `TBD`
- regeneration instructions: `TBD`
- artifact destination: `TBD`

## P. Freeze signatures/status

- Scientific record complete: `NO`
- GOM/MFR-14 line-by-line audit complete: `NO`
- User-approved P1 freeze: `NO`
- Decisive evidence opened: `NO`

**Current disposition:** `PREFREEZE_TEMPLATE_ONLY; NO_P1_CLAIM_CREATED`.