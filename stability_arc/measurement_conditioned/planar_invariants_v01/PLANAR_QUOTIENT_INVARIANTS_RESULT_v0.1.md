# Planar quotient invariants v0.1 result

Status: `PASS_PLANAR_QUOTIENT_INVARIANTS`

Canonical run: `33267544870`
Execution commit: `2b543ee666ad82db57b7f49dd56b33d8da2ece80`
Artifact: `9719098959`
Artifact ZIP SHA-256: `fb03af1fc0b1321309f9e6a53cc9cafa44583609c0187bdd4244da5907489ec7`

All Q0-Q7 gates passed.

For every admitted planar measurement axis away from the exact observability boundary, define measured-axis coordinate `u`, in-plane perpendicular coordinate `v`, `q=eta*kappa`,

`p=gamma*(1+cos(theta)^2)/2`,

`d=kappa+gamma*(1+sin(theta)^2)/2`,

`h=gamma*sin(2*theta)/4`.

The exact canonical quotient is

`A_phys=[[-p,h-omega],[h+omega,-d]]`,

`B=-sqrt(2q)*[[2u,0],[v,u]]`,

`A_record=A_phys+[[-2q(1-u^2),0],[2quv,0]]`.

The complete physical and same-record second-moment characteristic triples `(c1,c2,c3)` were derived exactly from these matrices and preserved in the run artifact.

The first coefficients simplify to

`c1_phys=3*(p+d)-14*q*u^2`,

`c1_record=3*(p+d)+6*q-20*q*u^2`,

so

`c1_record-c1_phys=6*q*(1-u^2)`.

At `theta=0`, the exact symbolic c1/c3 expressions reduce to the previously closed sigma_z formulas. Fresh clean-room checks used 64 X45 fixtures and 128 additional random planar-axis fixtures with zero failures and zero near-boundary exclusions. Maximum quotient-matrix error was `8.881784197001252e-16`; maximum invariant-coefficient error was `5.690418132570708e-15`; maximum non-orthogonal coordinate polynomial error was `7.389644451905042e-13`.

Both exact observability-boundary controls retained dark dimension 2 and returned `REFUSE_QUOTIENT_DIMENSION`.

Licensed conclusion: the entire mean-square invariant triple extends exactly across the admitted x-z planar measurement family in the canonical quotient coordinates. This does not establish angle-independent crossing behavior, a stochastic scalar, localization, collapse, or measurement quality.
