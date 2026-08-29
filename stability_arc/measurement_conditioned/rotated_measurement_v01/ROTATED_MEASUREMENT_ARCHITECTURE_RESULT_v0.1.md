# Rotated measurement architecture v0.1 result

Status: `PASS_ROTATED_AXIS_STOCHASTIC_QUOTIENT`

Canonical run: `33267236939`
Execution commit: `db02b49ed7167f61632af4e85b05e78151fcbccb`
Artifact: `9719008823`
Artifact ZIP SHA-256: `5e366dd89671fc2dd03803a182ebad326f1fd472ab888a5197f58c449704007f`

The measured observable was changed from `sigma_z/2` to

`X45=(sigma_x+sigma_z)/(2*sqrt(2))`

while retaining the Hamiltonian `omega*sigma_y/2` and amplitude damping `sqrt(gamma)*sigma_-`.

All R0-R7 gates passed on 128 fresh fixtures. There were zero structural failures.

Maximum residuals:

- rank-one bridge reconstruction: `4.440892098500626e-16`;
- physical dark-factor reconstruction/invariance: `6.953888646053306e-16`;
- stochastic/same-record dark compatibility: `6.71291532748312e-16`;
- quotient intertwining: `6.953888646053304e-16`;
- second-moment intertwining: `7.092835258144695e-16`;
- active-coordinate invariant comparison: `9.094947017729282e-12`, below the frozen `5e-9` gate.

The fixed generic three-dimensional measurement-axis control had observability rank 3 and returned exactly `REFUSE_NO_1D_DARK_FACTOR`.

Licensed conclusion: the exact dark/active stochastic quotient architecture transfers to this fixed 45-degree x-z measurement axis for the registered fresh fixtures, while the framework also correctly refuses a generic axis where the required one-dimensional dark factor is absent. No sigma_z-specific c1/c3 orientation rule, stochastic scalar, localization, collapse, or measurement-quality conclusion is transferred by this result.
