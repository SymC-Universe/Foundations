# Planar measurement dark-boundary v0.1 result

Status: `PASS_PLANAR_MEASUREMENT_DARK_BOUNDARY`

Canonical run: `33267394149`
Execution commit: `420cb2e14da60e9da07fd094a48016318a526eac`
Artifact: `9719055036`
Artifact ZIP SHA-256: `482f1a48bcc622be3413e1487a68f90b549763ed763105b8e429cbe28d0ad918`

All P0-P7 gates passed.

For the planar measurement axis

`n(theta)=(sin(theta),0,cos(theta))`

with `X_theta=n(theta).sigma/2`, the independently derived physical tangent has an exact y-dark direction. The physical x-z observability determinant reduces to

`Delta_obs = omega-(gamma/2)*sin(theta)*cos(theta)`

or equivalently

`Delta_obs = omega-(gamma/4)*sin(2*theta)`.

The measurement-backaction strength `kappa` cancels from this rank boundary.

When `Delta_obs != 0`, the maximal dark space is exactly one-dimensional, `D=span(e_y)`, and the full same-noise/same-record stochastic tangent dynamics descend to a two-dimensional quotient. The stochastic tangent obeys

`B e_y = -sqrt(2*eta*kappa)*(n dot r)*e_y`,

and the same-record rank-one correction annihilates `e_y`.

Fresh audit: 256/256 generic planar-axis fixtures passed, with zero near-boundary fixtures and zero structural failures. Maximum dark/intertwining residuals were below `6e-16`; maximum second-moment intertwining residual was `1.3322676295501878e-15`.

At the two preregistered positive-frequency exact boundaries, observability rank dropped to 1, dark dimension increased to 2, and both controls returned exactly `REFUSE_QUOTIENT_DIMENSION`.

The generic out-of-plane `(1,1,1)/sqrt(3)` control had observability rank 3, dark dimension 0, and returned `REFUSE_NO_1D_DARK_FACTOR`.

Licensed conclusion: this x-z measurement-plane family has an exact analytic boundary separating the admitted 2D stochastic quotient from a larger-dark-space refusal surface. No c1/c3 angle-independence, stochastic scalar, localization, collapse, or measurement-quality claim is licensed by this structural result.
