# Orientation c3 decomposition v0.1

Status: `PASS_ORIENTATION_C3_DECOMPOSITION`
Run: `33267107733`
Commit: `c455754373d3c00746ca236741301822a3940e52`
Artifact: `9718973273`
Artifact SHA-256: `99d7fc09f65df50663d1a75ce9a5883d3a8d647b11ab89055386f0ad754eb40f`

All O0-O5 gates passed.

For `x=s*a`, `z=b`, `s=+/-1`, the exact independently derived form is

`c3_phys(s)=E_phys+s*M_phys`

with

`M_phys=16*a*b*q*omega*(gamma+kappa-3*q*b^2)`,

and

`c3_record(s)=E_record+s*M_record`

with

`M_record=4*a*b*q*omega*(7*gamma+6*kappa+8*q-30*q*b^2)`.

Orientation reversal therefore changes each c3 by exactly `2*M`.

The exact first Hurwitz coefficients are orientation-sign independent. At `q=0`, both c1 and c3 are orientation invariant.

Fresh verification used 512 independent magnitude/rate tuples and both signs. Direct determinant class labels matched the affine formulas with zero mismatches. Maximum c3 error was `7.87148124459236e-14`; maximum active-coordinate invariant error was `1.3864337316759462e-13`.

This licenses an exact orientation-sign decomposition for c3 in this measured-qubit active representation. It does not universalize the bounded H9 negative-orientation result.
