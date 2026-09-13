# SI FM2 Embedding-Depth Function/Limit Map Summary v0.1

**Date:** 2026-09-13  
**Plan:** `SI_FM2_EMBEDDING_DEPTH_PLAN_v0.1.json`  
**Execution freeze:** `SI_FM2_EXECUTION_FREEZE_v0.1.json`  
**Program map:** `SI_FUNCTION_LIMIT_MAP_PLAN_v0.1.json`  
**Epistemic status:** P0-D descriptive/structural synthetic Function/Limit mapping only  
**Physical inheritance claim:** false  
**Physical inheritance length claim:** false

## Purpose

FM2 asks how much of a declared synthetic nearest-neighbor parent substrate must be retained before the child embedding response reproduces the analytic semi-infinite response for a declared **numerical task tolerance**.

It does not ask for, estimate, or calibrate a physical inheritance length.

## Frozen construction

- uniform nearest-neighbor substrate chain;
- onsite stiffness: `4.0`;
- child coupling: `0.6`;
- retained depths: `1, 2, 4, 8, 16, 32, 64, 128` degrees of freedom;
- substrate hopping: `0.35, 0.65, 0.95, 1.25`;
- probe real frequencies: `0.2, 0.7, 1.2, 1.6`;
- imaginary resolvent regularizers: `0.05, 0.15, 0.3`;
- 48 hopping/probe cases;
- 384 depth records.

The imaginary probe component is a resolvent regularizer only. It is not mechanical damping or `gamma`.

Before opening the FM2 result, the numerical verification rule was frozen at absolute direct-matrix versus recursive surface-Green-function agreement `<= 1e-9`.

The effective-depth rule was also frozen before output:

> For a declared numerical tolerance, the effective depth is the shallowest listed depth for which that depth **and every deeper listed depth** remain within tolerance.

A single early threshold crossing therefore cannot masquerade as convergence if a deeper finite chain moves away again.

## Validation provenance

Dedicated workflow:

- GitHub Actions run: `34756837555`;
- execution head: `8b54b251efcb736cdd55080ad921bcedf13569e5`;
- dedicated FM2 tests: `5 passed`;
- workflow conclusion: `success`.

Artifact:

- name: `substrate-inheritance-fm2-embedding-depth-v01`;
- artifact ID: `10317721694`;
- artifact SHA-256: `b897ddf7a70c21949bf93b689a59c20d62c2474c7d73bb6cc09cb7fb43a60d65`.

Generated result SHA-256:

`4415074b6ce0007bfcb07daa96e2e94daa10c04618fe683e2fdc72123ea58847`.

## Numerical verification

Direct finite-matrix and recursive finite-chain surface Green functions agreed with maximum absolute residual:

`5.551115123125783e-16`,

well inside the frozen `1e-9` software/mathematical verification tolerance.

Status:

`FINITE_METHODS_AGREE_WITHIN_FROZEN_TOLERANCE`.

The maximum finite dynamic-matrix 2-norm condition number across the map was approximately `37.3268`. No conditioning-based case deletion or physical cutoff was applied.

## Effective retained depth is task- and regime-dependent

All 48 frozen hopping/probe cases reached every predeclared numerical task tolerance within the listed depth grid, but the required depth varied substantially.

| relative embedding-error task | cases reached | minimum depth | median depth | maximum depth |
|---:|---:|---:|---:|---:|
| `0.1` | 48/48 | 1 | 1 | 32 |
| `0.01` | 48/48 | 1 | 2 | 64 |
| `0.001` | 48/48 | 2 | 4 | 64 |
| `0.0001` | 48/48 | 2 | 4 | 64 |

Thus there is no single numerical embedding depth even inside this one simple synthetic family. The required retained parent extent depends on both the declared accuracy task and the native hopping/probe regime.

## Function and Limit landscape

Across the full 384 depth records:

- maximum relative error to the semi-infinite embedding: approximately `1.97937`;
- minimum relative error: `0.0` at numerical precision;
- two of the 48 hopping/probe cases showed at least one non-monotonic finite-depth error step;
- non-monotonic case fraction: approximately `0.04167`.

The non-monotonic cases validate the reason for the frozen sustained-convergence rule. A first threshold crossing is not necessarily a reliable depth reduction.

### Function Map

The Function Map is the full finite-depth trajectory of the embedded child self-energy toward its semi-infinite reference across the ordinary hopping/probe grid.

### Limit Map

The Limit Map is the region in which shallow reductions have substantial error, convergence is slow or non-monotonic, or a stricter declared numerical task requires much greater retained depth.

No physical cutoff is inferred from these numerical task tolerances.

## What FM2 establishes at P0-D

For this declared synthetic chain family:

1. Parent-depth reduction is a task-dependent approximation problem, not an intrinsic universal depth number.
2. Stronger/more difficult regimes can require substantially deeper retained parent structure for the same requested embedding accuracy.
3. A sustained-depth criterion is safer than declaring convergence at the first favorable finite-depth crossing.
4. Direct and recursive finite-chain implementations agree at numerical precision under the frozen verification rule.
5. The analytic semi-infinite reference makes the reduction error directly measurable rather than self-referential.

## What FM2 does not establish

FM2 does not establish:

- a physical inheritance length;
- a Cu, Ru, Na, CO, H, or other material-specific substrate depth;
- an irreversible bath;
- a damping coefficient;
- a chi coordinate;
- a physical inheritance threshold;
- or a real-system inheritance result.

Finite-bath recurrence is explicitly `NOT_EVALUATED_FREQUENCY_DOMAIN_MAP` here and remains a separate time-domain question.

## Next step

The frozen `SI_FUNCTION_LIMIT_MAP_PLAN_v0.1.json` now leaves one planned P0-D map:

`FM5_RECOVERY_RESILIENCE_LANDSCAPE`.

FM5 will distinguish asymptotic return from finite-time transient amplification and ask how perturbation recovery changes across coupling/organization regimes without defining a universal resilience score.
