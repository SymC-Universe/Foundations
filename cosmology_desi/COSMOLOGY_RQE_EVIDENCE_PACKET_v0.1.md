# Cosmology Representation Qualification Evidence Packet v0.1

**Status:** TEMPLATE — thresholds must be frozen before evaluation  
**Purpose:** Define the exact evidence required by the Representation Qualification Engine.

## Identity

- preregistration ID:
- scientific target (Y):
- native model:
- dataset lineage:
- holdout identity:
- nuisance treatment:
- covariance identity:
- frozen code commit:
- frozen source set:

## F1 — local (chi)

**Question:** Does the (chi)-level coordinate contain independent information for (Y), or is it only a useful re-expression of native model variables?

Required:
- exact (chi) definition;
- native-variable comparator;
- algebraic dependence audit;
- uncertainty propagation;
- preregistered sufficiency metric.

Sources/comparators: [Chr26].

Allowed statuses: pass / fail / indeterminate.

## F2 — modal necessity

**Question:** Does resolved modal/scale/redshift structure add information beyond the scalar representation?

Required:
- modal operator/matrix definition;
- eigenvalue/eigenvector or basis definition;
- scale/redshift domain;
- (d_{m eff}) or equivalent information-dimensionality measure;
- summary-sufficiency/complementarity measure;
- lower-order predictive comparison.

Sources/comparators: [Nad16, Lee26b, Sui25, Hea20, Bas19].

## F3 — aggregate (Chi)

**Question:** Does the relation among qualified local/modal components add information beyond their marginals?

Required:
- explicit (Chi) construction;
- proof it is not a hidden average/relabeling;
- conditional incremental-information test;
- matched-complexity null;
- relation-randomization or equivalent null where possible.

Sources/comparators: [Sui25, Nad16].

## F4 — Stability Arc

**Question:** Does the trajectory through qualified state space add information beyond static states?

Required:
- arc/state-space definition;
- endpoint-only comparator;
- static-state comparator;
- trajectory metric;
- held-out temporal/redshift test.

Sources/comparators: [Chr26, Roy11, Wie10].

## F5 — Stability Inheritance

**Question:** Does earlier qualified architecture improve prediction of later qualified state after standard cosmological history variables are conditioned out?

Required:
- explicit inheritance map;
- standard transfer/history comparator;
- lag/epoch definition;
- conditional predictive test;
- failure under shuffled/history-destroyed null.

Sources/comparators: [Vru21, Wie10].

## F6 — joint DM/DE function

**Question:** Does the integrated representation jointly organize DM-side and DE-side observables beyond ordinary expansion-growth analysis?

DM-side minimum candidates:
- (fsigma_8(z));
- (P(k,z)) or full-shape equivalent;
- lensing / potential information where available.

DE-side minimum candidates:
- (H(z));
- distance/BAO;
- (q(z)) or equivalent acceleration coordinate.

Required comparator:
- ordinary expansion-growth reconstruction.

Sources/comparators: [Roy11, Sha21, Bas19, Per22, You26, Kun07b, Mar19].

## F7 — matched adversarial transport

Required when data are available:
- (Lambda)CDM/GR;
- dynamical DE;
- free (sum m_
u);
- modified gravity;
- interacting dark sector;
- SN/sample/systematic variant.

Required rejection / misspecification comparator:
- posterior predictive / relative-entropy consistency;
- compression-loss or field-vs-summary diagnostic.

Sources/comparators: [Nic18, Hea20, Kun07b, Mar19, You26].

## Decision packet

For each gate record:
- status;
- metric;
- observed value;
- frozen threshold;
- uncertainty;
- reason;
- source keys;
- data/checkpoint identity.

No gate may be re-thresholded after the held-out result is inspected.
