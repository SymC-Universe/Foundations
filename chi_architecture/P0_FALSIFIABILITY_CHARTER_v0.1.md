# P0 Falsifiability Charter v0.1

**Workstream:** Chi Architecture Investigation  
**Status:** P0 EXPLORATORY / NOT CONFIRMATORY  
**Purpose tag:** HYPOTHESIS_GENERATION + FEASIBILITY  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1  
**MFR-14 status:** NOT ACTIVATED  

## 1. Purpose

Build and try to break a candidate cross-regime stability-architecture representation before any generalized chi claim is frozen for confirmation.

The current starting representations are scalar, vector/modal, and conglomerate/system. They are not assumed exhaustive, ontologically independent, or universally present.

## 2. Native object first

Every synthetic or real example begins with a named governing object or accepted statistical structure `G`.

Allowed sequence:

`G -> native observables -> S/M/C where applicable -> cross-component relationships -> outcome/failure analysis`

Forbidden sequence:

`desired chi pattern -> choose G/normalization/mode/coupling to recover it`

## 3. Representation definitions

### 3.1 Scalar representation S

A named compressed quantity derived from the native model or data representation.

Examples may include eigenvalues, spectral gaps, decay rates, stability margins, concentration measures, or a licensed scalar chi.

A scalar is not called chi unless the active domain-specific admission rule licenses that name.

### 3.2 Vector/modal representation M

A named resolved carrier representation derived from the native model.

Examples may include right/left modes, invariant subspaces, projectors, participation structure, singular vectors, latent directions, or other native multidimensional carriers.

If individual modes are non-identifiable because of degeneracy, crowding, or conditioning, the representation must move to an appropriate subspace/projector description or refuse.

### 3.3 Conglomerate/system representation C

A named native object describing organization created by interaction, coupling, feedback, network structure, memory, environment, cross-layer mapping, or collective behavior.

`C` is **not** defined as arbitrary concatenation of S and M and is not "whatever combination predicts best."

An algebraic reconstruction such as `A = V Lambda V^-1` demonstrates mathematical completeness of a representation but does not by itself establish independent scientific added value for C.

### 3.4 Additional relationship structure R

Cross-component relationships may be measured explicitly when justified. Examples include coupling strength, alignment, transfer, disagreement, synergy, feedback response, or inheritance mappings.

R is not automatically a fourth chi component. It is initially a relationship object whose status must be earned.

### 3.5 Uncertainty/open channel U

Each analysis preserves uncertainty, residuals, conditioning, refusal, and non-identifiability. Precision in one representation cannot repair uncertainty in another.

## 4. Disagreement vocabulary

The following terms are intentionally separated.

### 4.1 Neutral discordance

`DISCORDANCE` means only that two prospectively defined representation-level responses are incompatible under the declared comparison rule.

It has no favorable or unfavorable interpretation by itself.

### 4.2 Compensatory discordance

A discordance may be described as `COMPENSATORY_DISCORDANCE_CANDIDATE` only when all of the following are observed in a known-truth or prospectively specified test:

1. an identified perturbation changes one declared representation;
2. another declared representation responds in a prospectively defined opposing or mitigating direction;
3. an independently defined native system property is preserved or recovers relative to an appropriate control;
4. the responsible coupling/feedback path is independently identifiable in the model;
5. ablation, sign reversal, or rewiring of that path weakens, removes, or reverses the preservation/recovery effect as expected.

At P0 this label remains methodological and exploratory.

### 4.3 Destabilizing discordance

`DESTABILIZING_DISCORDANCE` is used when the same predeclared discordance accompanies worsening of the independent native stability outcome.

### 4.4 Nonfunctional discordance

`NONFUNCTIONAL_DISCORDANCE` is used when discordance has no reproducible relation to the independent outcome under the tested design.

### 4.5 Epistemic discordance

`EPISTEMIC_DISCORDANCE` is used when disagreement is reproducibly induced by observer-only measurement/estimation noise without a corresponding change in the known physical state.

## 5. Noise-entry controls

Known-truth tests should separately inject comparable perturbations at different locations:

- `PROCESS_NOISE`: enters the governing state dynamics;
- `FEEDBACK_OR_SENSOR_NOISE`: enters a measurement that the modeled controller/response actually uses;
- `OBSERVER_ONLY_NOISE`: added after the physical trajectory is generated and therefore cannot alter the physical system.

No noise source is called biologically or physically compensatory merely because the final measured series is noisy.

## 6. Conglomerate added-value test

A conglomerate/system representation is scientifically nontrivial only if, on an independently defined task, it contributes something not obtained from the appropriate lower-level representations or native baseline alone.

Candidate value axes include:

- future-state prediction;
- perturbation recovery;
- transient-amplification prediction;
- stability-boundary localization;
- uncertainty calibration;
- transfer/generalization;
- correct refusal;
- interpretable compression with bounded information loss.

At P0, these are exploratory diagnostics. A later `ADDS` claim requires the full General Protocol confirmatory path.

## 7. Mandatory known-truth families

The first computational battery will include, at minimum:

### F0. Normal decoupled baseline

A system where scalar eigenvalue stability is sufficient and no conglomerate advantage should be manufactured.

Expected lesson: the architecture should be allowed to collapse to a simpler adequate description.

### F1. Same scalar spectrum, different modal geometry

Construct systems with matched eigenvalues and deliberately different eigenvector/subspace geometry.

Question: which native behaviors change despite scalar equivalence?

### F2. Same modal geometry, different scalar spectrum

Hold the modal basis fixed while changing the scalar spectrum.

Question: which native behaviors change despite modal equivalence?

### F3. Same local subsystems, different coupling

Hold local subsystem operators fixed while varying coupling sign, magnitude, topology, or directionality.

Question: does whole-system behavior change specifically with the conglomerate interaction?

### F4. Feedback compensation versus destabilization

Create known feedback systems in which coupling is deliberately stabilizing, neutral, or destabilizing.

Question: can the declared discordance vocabulary correctly distinguish the three without post-hoc relabeling?

### F5. Process noise versus observer-only noise

Use matched noise scales with different entry points.

Question: can the analysis distinguish physical response from measurement disagreement?

### F6. Non-normal transient growth

Use stable eigenvalues with variable non-normality and known transient amplification.

Question: does the modal/conglomerate analysis add the expected information beyond eigenvalue stability, and does it agree with native non-normal diagnostics?

### F7. Degenerate/crowded subspace case

Create exact or practical degeneracy so individual-vector identity is unstable.

Question: does the method move to subspace/projector language or refuse rather than invent stable mode identities?

### F8. Null / non-applicable architecture

Include systems in which a proposed scalar chi is not licensed, one starting representation is not meaningful, or coupling is absent.

Question: can the framework return `NOT_APPLICABLE`, `NO_ADMISSIBLE_CHI`, or `NO_ADDED_ARCHITECTURE_VALUE` without manufacturing completeness?

## 8. Native comparator rule during P0

Each family must be evaluated against the strongest obvious native diagnostic for the exact known-truth task.

Candidate families include, as appropriate:

- eigenvalue stability;
- Lyapunov analysis;
- transient norm / singular-value analysis;
- pseudospectral or resolvent diagnostics;
- standard state-space/control metrics;
- standard covariance/latent-factor methods.

These are candidate comparator families only. The final comparator for any P1 claim must be selected and frozen under MFR-05 before decisive evidence is opened.

## 9. Explicit outcomes that count against the architecture

The following are legitimate negative outcomes and may not be reinterpreted as hidden success:

- `NO_ADDED_ARCHITECTURE_VALUE`: S/M/C terminology adds no measurable value beyond the native standard analysis on the frozen task;
- `DOMAIN_LIMITED`: the construction works only in the formulation domain or requires incompatible remapping elsewhere;
- `NO_STABLE_CROSS_REGIME_MAPPING`: proposed correspondences fail under untouched generators or coordinate-consistent transformations;
- `CONGLOMERATE_REDUNDANT`: C supplies no independent task-relevant information beyond an appropriate lower-level/native representation;
- `DISCORDANCE_NONFUNCTIONAL`: disagreement does not predict preservation, recovery, or another predeclared outcome;
- `DISCORDANCE_DESTABILIZING`: disagreement tracks deterioration rather than compensation;
- `NO_COUPLING_SPECIFICITY`: apparent compensation persists when the proposed feedback/coupling path is ablated or rewired;
- `EPISTEMIC_NOISE_EXPLAINS_RESULT`: observer-only noise reproduces the apparent architecture effect;
- `NO_ADMISSIBLE_CHI`: no defensible chi coordinate arises in the regime;
- `NOT_APPLICABLE`: a proposed starting representation is not meaningful for the native model;
- `NONIDENTIFIABLE`: data/model conditioning cannot support the requested representation;
- `STANDARD_TOOLKIT_EQUIVALENT`: the construction reproduces native results in different notation without additional scientific content;
- `STANDARD_TOOLKIT_SUBTRACTS`: the construction performs worse or misleads relative to the native method.

## 10. Prohibited rescue moves

After an outcome is viewed, the same exploratory result may not be upgraded by:

- redefining S, M, C, R, or the stability outcome to make the result favorable;
- choosing a different scalar because it aligns better with C;
- selecting a mode because it lies near a preferred scalar boundary;
- redefining disagreement as compensation after seeing recovery;
- removing a failed synthetic family from the reported battery;
- converting method refusal into a scientific prediction unless refusal was independently specified prospectively;
- adding a new component and claiming it retroactively explains the failure that motivated it;
- treating an algebraic identity as empirical added value.

A changed definition starts a new exploratory version and preserves the original result.

## 11. Transition to P1

P1 begins only after P0 identifies a narrow claim worth testing and the complete MFR-14 is committed before untouched decisive evidence is opened.

No P0 success counts toward the cross-domain program portfolio `ADDS` threshold.

## 12. Immediate implementation order

1. implement F0-F3 exact linear generators;
2. implement F4-F5 feedback/noise-entry experiments;
3. implement F6 non-normal controls against native diagnostics;
4. implement F7-F8 refusal/nonidentifiability cases;
5. preserve all outcomes in a machine-readable record;
6. only then decide whether a P1 claim is scientifically mature enough to freeze.
