# D01C Literature Position and Novelty Firewall

**Status:** PRE-RESULT CONTEXT / NOT EVIDENCE FOR SYMC

D01C deliberately targets an established failure mode of eigenvalue-only stability descriptions.

The following facts are treated as prior art:

1. Stable non-normal linear systems can show substantial finite-time amplification even when every eigenvalue is asymptotically stable.
2. Eigenvalue non-orthogonality, state-transition singular values, pseudospectra, and resolvent norms are standard tools for diagnosing that behavior.
3. The resolvent provides a standard input-output/robustness view of non-normal dynamics.
4. Approaching a defective limit can make eigenvector-based descriptions poorly conditioned even before exact coalescence.

Primary context:

- Trefethen LN, Trefethen AE, Reddy SC, Driscoll TA. *Hydrodynamic Stability Without Eigenvalues*. Science 261 (1993) 578-584. DOI: 10.1126/science.261.5121.578.
- Trefethen LN. *Pseudospectra of Linear Operators*. SIAM Review 39 (1997) 383-406. DOI: 10.1137/S0036144595295284.
- Schmid PJ. *Nonmodal Stability Theory*. Annual Review of Fluid Mechanics 39 (2007) 129-162. DOI: 10.1146/annurev.fluid.38.050304.092139.
- Jovanovic MR. *From Bypass Transition to Flow Control and Data-Driven Turbulence Modeling: An Input-Output Viewpoint*. Annual Review of Fluid Mechanics 53 (2021) 311-345. DOI: 10.1146/annurev-fluid-010719-060244.

## Novelty firewall

D01C may not claim as new:

- transient growth from non-normality;
- pseudospectral sensitivity;
- resolvent amplification;
- the role of eigenvector non-orthogonality;
- numerical abscissa as an initial-growth diagnostic;
- the insufficiency of eigenvalues alone for general finite-time behavior.

The SymC-specific question is instead whether the joint local/spectral and broader-architecture framing yields a reproducible inheritance/refusal interpretation that adds something beyond the strongest standard native toolkit.

If it does not, the correct result is:

`STANDARD_NONMODAL_TOOLKIT_SUFFICIENT`

That outcome narrows the SymC contribution without invalidating the D01A/D01B mathematical findings.
