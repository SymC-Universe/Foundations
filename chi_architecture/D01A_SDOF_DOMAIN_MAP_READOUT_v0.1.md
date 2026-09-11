# D01A SDOF Domain Chi Map Readout v0.1

**Date:** 11 September 2026  
**Status:** P0-D/P0-Q within-domain exact-anchor readout  
**Plan:** `D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json`, fixed before this result was opened  
**Artifact:** GitHub Actions run 34615114508, artifact `chi-architecture-d01a-domain-map-v01`, artifact ID 10269408539  
**Artifact digest:** `sha256:fcaefcb95485a390b79530a890fad3dff5f4419fc3d31749c9240eeec8a7012c`

## 1. Scope

This readout maps the exact passive single-degree-of-freedom oscillator

`x_ddot + gamma*x_dot + omega0^2*x = 0`

after the native nondimensionalization

`tau = omega0*t`,

which gives

`d2x/dtau2 + 2*chi*dx/dtau + x = 0`,

with

`chi = gamma/(2*omega0)`.

This is an exact within-domain anchor. It does not establish a cross-domain chi architecture and is not evidence for an Atlas alignment.

## 2. Coordinate-collapse result

The plan scanned:

- `chi = 0.00 ... 4.00` in increments of `0.05`;
- `omega0 = 0.5, 1.0, 2.0, 5.0`;
- normalized initial conditions `(x0,u0)=(1,0)` and `(0,1)`;
- normalized time `tau=0...30`.

For fixed chi and fixed normalized initial condition, changing omega0 produced the same normalized trajectory to machine precision.

Maximum observed cross-omega0 collapse errors:

- normalized displacement: `0.0`;
- normalized velocity: `1.1102230246251565e-16`.

This verifies the exact analytic statement that, after the declared nondimensionalization, the response shape depends on chi rather than omega0 and gamma separately.

Within this declared model, chi therefore earns a real role as a **dimensionless dynamic-similarity coordinate** and response-shape compression.

## 3. Critical point remains structurally special, but not uniquely optimal

For both normalized initial conditions:

- `chi=1.0` is the first nonoscillatory grid point;
- `chi=1.0` maximizes the slowest dimensionless decay rate, with value `1.0`.

Those are native structural properties of the second-order roots.

However, other predeclared function metrics do not all optimize at chi=1.

### Initial displacement `(x0,u0)=(1,0)`

On the frozen grid:

- minimum 2% state-settling time: `chi=0.80`, `tau=4.56`;
- minimum integral absolute displacement: `chi=0.65`, value `1.605706095625046`;
- minimum integrated normalized energy: `chi=0.70`, value `0.7071428571404265`;
- maximum slowest decay rate: `chi=1.00`, value `1.0`.

### Initial normalized velocity `(x0,u0)=(0,1)`

On the frozen grid:

- minimum 2% state-settling time: `chi=0.75`, `tau=4.99`;
- minimum integral absolute displacement occurs at the upper scan boundary `chi=4.00`, value `0.9774978002297837`;
- minimum integrated normalized energy also occurs at the upper scan boundary `chi=4.00`, value `0.0625003298370766`;
- maximum slowest decay rate: `chi=1.00`, value `1.0`.

Because the latter two minima occur at the scan boundary, no interior optimum is claimed for those metrics.

## 4. Scientific interpretation

The first domain map supports a distinction that the boundary-only framing obscures:

`chi=1` is an exact structural transition for the licensed oscillator, but `chi=1` is not a task-independent statement of "best function." Different independently declared response objectives and different initial perturbations select different regions of the same chi coordinate.

Thus, within the exact oscillator itself, chi behaves more naturally as a **placement coordinate over a response landscape** than as a universal optimum.

The response landscape contains at least:

- an undamped/nondecaying endpoint at chi=0;
- an underdamped functioning region in which increasing chi changes decay, oscillation count, settling, integrated displacement, and integrated energy differently;
- the exact root-coalescence / oscillatory-to-nonoscillatory boundary at chi=1;
- an overdamped region in which the slow mode becomes progressively slower as chi increases, even though some perturbation-specific integrated quantities may continue to improve over the scanned range.

No single metric is authorized to redefine chi. The coordinate is derived from the governing equation; the metrics reveal what different locations on that coordinate mean.

## 5. Relevance to the domain-first Atlas program

This is the first clean example of the desired dependency:

`native equations -> independently derived chi coordinate -> Function/Limit Map -> eventual Atlas placement`.

The coordinate was not selected by a desired Atlas pattern.

The next scientific question is harder and more relevant to architectural chi:

**When multiple dynamical components are coupled, can their full functioning and limit behavior still be placed adequately with one scalar coordinate, or must Chi become a multidimensional object containing modal and coupling/system information?**

D01B addresses that question without predeclaring a master scalar.

## 6. Claim ceiling

Allowed:

- exact within-domain dimensionless-response collapse;
- descriptive Function/Limit mapping of the licensed passive SDOF model;
- the statement that different predeclared function metrics select different chi regions within that model;
- use of D01A as a P0 anchor for D01B method development.

Not established:

- a cross-domain chi coordinate;
- a universal optimum;
- a biological, chemical, neural, or other imported chi;
- a validated Stability Architecture Atlas;
- an architectural conglomerate beyond this exact SDOF model.
