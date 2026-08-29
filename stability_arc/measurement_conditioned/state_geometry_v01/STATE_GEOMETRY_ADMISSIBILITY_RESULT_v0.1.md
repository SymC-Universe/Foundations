# State-geometry admissibility audit v0.1 result

Canonical run: `33266926497`
Execution commit: `b2a7c5312f32556b5047e5a62a1bfd8300505d82`
Artifact: `9718921406`
Artifact ZIP SHA-256: `1c746df3f8efef56e003879840471be94759caab6a307d7585fedc55d7073bed`

Mechanical gates G0-G5: all PASS. Maximum c1/c3 full-generator reconstruction error: `9.43689570931383e-15`.

## Registered scientific outcomes

- H8E high-radius existence threshold: **FAIL**. Only 2 eligible cases were found across R3+R4, below the preregistered minimum of 20.
- H8L low-radius absence replication: **PASS**. Zero eligible cases occurred across R1+R2 (`0.90 <= r < 0.98`).
- H8F c1+c3 full-class sufficiency: **INSUFFICIENT_H8F**. Only 2 cases were available, below the 20-case scoring minimum. Both 2/2 were complete physical STABLE -> record UNSTABLE crossings with zero m2 or mh blockers, but this is not promoted as confirmation.

## Stratified signal

Eligible counts by frozen stratum:

- R1 NEG/POS: 0 / 0;
- R2 NEG/POS: 0 / 0;
- R3 NEG/POS: 0 / 0;
- R4 NEG/POS: 2 / 0.

Thus both fresh eligible cases occurred only in the highest radial shell `0.995 <= r < 0.9999` and only with `x*z<0`.

The two frozen cases differed substantially in `|z|`, kappa, eta, and omega, so the shared observed coordinates are high radius and negative orientation product rather than one single narrow parameter tuple.

This outcome is retained as a failed existence threshold plus an insufficient sufficiency test. It motivates a new fresh same-shell orientation test; it does not authorize changing the H8 thresholds or counting the 2/2 result as a PASS.
