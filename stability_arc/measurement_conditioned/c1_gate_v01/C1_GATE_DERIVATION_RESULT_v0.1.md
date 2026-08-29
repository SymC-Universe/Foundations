# Exact c1 first-Hurwitz-gate derivation v0.1 result

Status: `PASS_C1_GATE_DERIVATION`

Canonical run: `33266715420`
Execution commit: `87503d9b9deb107f04779979b941d861f6d0984d`
Artifact: `9718862521`
Artifact ZIP SHA-256: `b6484ea6fb9a6ff367e8b383bb09443776d01474c0c7d0ce2958b4a2e10fe1ba`

All C0-C5 gates passed.

The independently constructed symmetric second-moment generators give

`c1_phys = 9*gamma/2 + 3*kappa - 14*q*z^2`

and

`c1_record = 9*gamma/2 + 3*kappa + 6*q - 20*q*z^2`,

where `q=eta*kappa`.

Therefore

`Delta_c1 = c1_record-c1_phys = 6*q*(1-z^2)`.

For physical Bloch states with `x^2+z^2<1`, `Delta_c1>0` whenever `q>0`, and equals zero at `q=0`.

Fresh clean-room checks: 128/128 passed; maximum formula error `4.376740930020571e-15`; direction failures `0`; fixed q=0 equality passed; maximum non-orthogonal active-coordinate transform error `3.2909465637156463e-15`.

This licenses c1 as a separate exact mean-square coordinate and licenses the nonnegative conditioning displacement of c1 in this model. It does not establish that c1 plus the c3 map is sufficient for full mean-square class displacement.
