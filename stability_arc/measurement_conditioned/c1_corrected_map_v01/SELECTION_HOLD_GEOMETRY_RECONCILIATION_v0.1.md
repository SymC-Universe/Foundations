# H7 selection-hold geometry reconciliation v0.1

Classification: `MODEL-DOMAIN / SAMPLING-GEOMETRY SIGNAL`

This note is an audit consistency check, not new prospective evidence.

## Why H7 returned zero corrected destabilizing candidates

H7 sampled Bloch radius only from `r in [0.05,0.98]`.

A previously preserved H4 crossing, `XC002679`, has

- `gamma=1`;
- `kappa=7.13390807096159`;
- `omega=5.531011477185077`;
- `eta=0.1436084182509635`;
- `x=0.16060572259621236`;
- `z=-0.9850913026355294`.

Using the already-closed exact formulas, this historical case has audit-only values approximately

- Bloch radius `sqrt(x^2+z^2) = 0.9980977270`;
- `c1_phys/R = 0.8157818501`;
- normalized `c3_phys = +0.0033015784`;
- normalized `c3_record = -0.0152232288`.

It therefore lies strongly inside the H7 algebraic `I_destab + positive c1_phys` condition, but it lies outside H7's registered radial sampling support because `0.9980977270 > 0.98`.

The H7 empty selection is therefore not inconsistent with H4/H5. It identifies a domain boundary between the broad truncated radial frame and the near-pure-state target geometry.

## What is and is not learned

Learned: repeating the same H7 generator with more draws is not the justified next step. The missing corrected-destabilizing class lies outside, or is at least strongly suppressed inside, the registered `r<0.98` state domain.

Not learned: no theorem of impossibility is licensed for `r<0.98`, and no universal claim is licensed that near-pure states are required. Both require fresh tests.

## Next justified phase

Use a new seed and a preregistered radial-shell by orientation-sign design that explicitly includes shells on both sides of the old `r=0.98` truncation. Stage A may use only the exact c1 and c3 coordinates, freeze eligible selections before full mean-square reveal, and then test where genuine physical STABLE -> record UNSTABLE crossings are admissible.
