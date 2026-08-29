# Secular-continuation / mode-correspondence audit v0.1

**Status:** FROZEN BEFORE EXECUTION

## Purpose

The closed information-rank bridge establishes, under the registered local continuous-measurement convention,

`A_rec = A_phys + U V^T`

with `rank(U V^T) <= m` for `m` scalar record channels, and away from physical poles the comparative characteristic relation is governed by

`det(I_m - V^T (zI-A_phys)^(-1) U)`.

This audit asks a narrower outcome-free question: can the low-rank bridge support a reproducible correspondence between physical and inference spectral **clusters** along the fixed interpolation

`A(t) = A_phys + t U V^T`, `t in [0,1]`,

without forcing one-to-one eigenvector labels through degeneracies, defective points, conjugate-pair collisions, or ambiguous assignments?

No localization outcome, historical E16-E27 score, GFSA external-candidate response, or chi-based target may be read or used by this audit.

## Frozen scientific representation

The continuation parameter is a bookkeeping coordinate for the already-closed conditioning update. It is not asserted to be physical time or measurement strength.

Use the fixed grid

`t_j = j/16`, `j=0,...,16`.

At each grid point construct `A(t_j)` directly from the frozen `A_phys,U,V`.

The licensed correspondence object, if this audit passes, is

`S = (A_phys, U, V, {A(t_j)}, cluster_paths, refusal_record, secular_root_record)`.

The full physical and record-conditioned generators remain full matrices. No scalar chi or scalarized generator is licensed.

## Fresh quantum controls

Use three fresh parameter/base-state fixtures not used in the conditional tangent, joint-channel v0.1/v0.2, moment-lift v0.1, or information-rank v0.1 audits:

1. `eta=0.66, gamma=0.22, kappa=0.14, omega=1.02, base=(0.18,-0.12,0.22)`
2. `eta=0.79, gamma=0.34, kappa=0.18, omega=1.27, base=(-0.27,0.08,0.16)`
3. `eta=0.57, gamma=0.28, kappa=0.12, omega=0.81, base=(0.11,0.29,-0.18)`

Use the already-closed conventions:

- `x=sigma_z/2`;
- `H=omega sigma_y/2`;
- amplitude-damping collapse amplitude `sqrt(gamma)`;
- unconditional measurement term `2 kappa D[x]`;
- `A_phys` from direct Liouvillian action;
- `u=-4 eta kappa h`, with `h` the Bloch coordinates of `H_x(rho)`;
- `v` the Bloch measurement functional for `delta mu=Tr(x delta rho)`;
- `U=u`, `V=v` for the one-record fixtures.

These are representation controls only, not localization tests.

## Frozen numerical admissibility and refusal rules

For any real `n x n` matrix `A`, define

`scale(A)=max(1, ||A||_2)`.

At each continuation point compute the complex eigenvalues and right-eigenvector matrix `X`.

A point is refused as `REFUSE_DEGENERATE_OR_COLLISION` if

`min_{i != j} |lambda_i-lambda_j| / scale(A) <= 1e-7`.

A point is refused as `REFUSE_NEAR_DEFECTIVE` if

`cond_2(X) >= 1e8`.

For a real matrix, an eigenvalue is treated as real if

`|Im(lambda)| <= 1e-10 scale(A)`.

Non-real eigenvalues must form conjugate pairs with residual

`|lambda_j-conj(lambda_i)| <= 1e-9 scale(A)`;

otherwise return `REFUSE_CONJUGACY_INCONSISTENT`.

Cluster each admissible spectrum into real singletons and complex-conjugate pairs. A complex pair is a single 2D invariant-subspace object and may not be split into two independently labeled modes.

For an admissible eigendecomposition `A=X Lambda X^-1`, define the spectral projector for a singleton as `P_i = x_i y_i^T`, where `y_i^T` is the matching row of `X^-1`; for a conjugate pair use the sum of the two projectors. Projector idempotency, mutual decomposition, and `sum P = I` are numerical controls, not mode-selection metrics.

## Frozen adjacent-step correspondence rule

Between adjacent admissible continuation points:

1. the multiset of cluster dimensions must be unchanged; otherwise return `REFUSE_BRANCH_TOPOLOGY_CHANGE`;
2. only clusters of equal dimension may be matched;
3. represent a real singleton by its real eigenvalue and a conjugate pair by `alpha+i|beta|`, where the pair is `alpha +/- i beta`;
4. define the normalized spectral cost between two eligible clusters as `|z_a-z_b| / max(1,scale(A_a),scale(A_b))`;
5. enumerate all dimension-compatible assignments and choose the unique minimum-total-cost assignment;
6. if the second-best total cost differs from the best by `<=1e-6`, return `REFUSE_AMBIGUOUS_ASSIGNMENT`.

No localization metric, overlap weighting, hand label, preferred branch, damping ratio, or chi value enters the matching cost.

The correspondence may therefore return a branch path or a refusal. Refusal is a valid result.

## Frozen secular-root rule

For each positive continuation point `t_j>0` and each eigenvalue `z` of `A(t_j)`, evaluate the physical resolvent only if

`sigma_min(zI-A_phys) / scale(A_phys) > 1e-8`.

Otherwise record `REFUSE_NEAR_PHYSICAL_POLE` for that root.

For admissible roots verify

`det(I_m - t_j V^T (zI-A_phys)^(-1) U) = 0`

with absolute residual `<=2e-8`.

At `t=0`, evaluation at the physical eigenvalues must be refused as near-pole rather than regularized or shifted.

The direct characteristic polynomial of `A(t)` remains authoritative at or near physical poles.

## Frozen negative/refusal controls

### N1 initial degeneracy

`A_phys=diag(-1,-1,-2)`, `U=(1,0,0)^T`, `V=(0.1,0,0)^T`.

The audit must return `REFUSE_DEGENERATE_OR_COLLISION` at `t=0`.

### N2 conjugate-pair collision

Use

`A_phys=[[-1,1,0],[-1,-1,0],[0,0,-3]]`,

`U=(0,2,0)^T`, `V=(1,0,0)^T`.

At `t=1/2` the 2x2 conjugate pair coalesces. The audit must refuse the path at that grid point rather than relabel the pair as two real modes.

### N3 physical-pole secular refusal

For every positive quantum fixture, evaluating the secular resolvent exactly at each `A_phys` eigenvalue must return `REFUSE_NEAR_PHYSICAL_POLE`.

## Fixed common-coordinate control

Use the fixed orthogonal rotation

`Q=Rz(0.33) Ry(-0.41) Rx(0.26)`.

Transform

`A_phys' = Q^T A_phys Q`, `U'=Q^T U`, `V'=Q^T V`.

The transformed audit must return the same refusal/admissibility status at every `t_j`, the same cluster-dimension sequence, and branch representatives agreeing to `<=2e-9` after canonical conjugate-pair representation.

For each admissible matched spectral projector verify

`P' = Q^T P Q`

to maximum absolute residual `<=2e-8` after correspondence.

This common orthogonal coordinate change may not be used to choose or repair a branch.

## Frozen gates

### S0 path construction and low-rank identity

For every fresh quantum fixture and every `t_j`, verify

`A(t_j)-A_phys = t_j U V^T`

to maximum absolute residual `<=5e-14`, and verify `rank(UV^T)<=1` with singular-value rank tolerance `1e-12`.

### S1 spectral admissibility and projector algebra

For every continuation point that is not refused by the frozen rules, require:

- conjugacy classification consistency;
- projector idempotency `||P^2-P||_max <=2e-9`;
- decomposition `||sum P-I||_max <=2e-9`.

Fresh quantum fixtures must either produce a fully admissible path or an explicit frozen-rule refusal. No manual rescue is allowed.

### S2 continuation correspondence

For every fresh quantum fixture with a fully admissible path:

- apply the frozen adjacent-step assignment exactly;
- preserve cluster dimension along every matched branch;
- recover the `t=0` physical spectrum and `t=1` record-conditioned spectrum to canonical-representative residual `<=2e-9`.

If a fresh fixture refuses, S2 records the exact refusal and does not substitute a different matching rule.

### S3 secular-root consistency and pole refusal

Every admissible positive-`t` root must satisfy the frozen secular determinant residual `<=2e-8`.

Every N3 exact physical-pole probe must return `REFUSE_NEAR_PHYSICAL_POLE`.

### S4 mandatory negative-control refusal

N1 must refuse at `t=0` as `REFUSE_DEGENERATE_OR_COLLISION`.

N2 must refuse at `t=1/2` as `REFUSE_DEGENERATE_OR_COLLISION` or `REFUSE_NEAR_DEFECTIVE`; it may not continue through the collision under a new label.

### S5 common-coordinate invariance

Require the frozen status/cluster-sequence invariance, branch-representative residual `<=2e-9`, and projector covariance residual `<=2e-8`.

### S6 interpretation firewall

Every output must state:

- `PHYSICAL_GENERATOR=FULL_MATRIX_REQUIRED`;
- `RECORD_GENERATOR=FULL_MATRIX_REQUIRED`;
- `MODE_OBJECT=INVARIANT_CLUSTER_OR_REFUSE`;
- `SECULAR_OBJECT=COMPARATIVE_ONLY`;
- `SCALAR_CHI=NOT_LICENSED`.

The audit may report endpoint branch displacements in real part and oscillation magnitude as descriptive geometry only. No sign pattern or branch is promoted as a localization predictor.

## Decision rule

Overall `PASS` requires S0, S3, S4, S5, and S6 to pass, and S1-S2 to be executed faithfully. A fresh quantum fixture that triggers a preregistered refusal is retained as a scientifically meaningful identifiability/boundary result and does not authorize threshold loosening. The final audit report must distinguish `PASS_WITH_ALL_FRESH_PATHS_ADMISSIBLE` from `PASS_WITH_FRESH_REFUSAL`.

No threshold, path grid, cluster rule, matching cost, ambiguity margin, pole guard, defectivity guard, fixture, coordinate transform, or interpretation may be changed inside v0.1 after first execution. A scientifically motivated correction requires a new version with the v0.1 result preserved.

## Interpretation firewall

A successful audit would establish only that the already-closed low-rank conditioning bridge can support an outcome-free spectral-cluster continuation when the spectrum is numerically identifiable, while explicitly refusing degeneracies, defective neighborhoods, topology changes, ambiguous assignments, and physical-resolvent poles.

It would not establish that any branch controls localization, that one mode is physically privileged, that a scalar chi exists for the conditional generator, or that chi=1 is an optimum under measurement.
