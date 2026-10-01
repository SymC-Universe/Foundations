# QFT Generator / Retarded-Pole Clean-Room Result v0.1

**Date:** 2026-10-01  
**Task:** `QFT_GENERATOR_POLE_CLEANROOM_V01`  
**Workflow run:** 36864049059  
**Frozen source commit:** `d2c0037a5b2f40f0c15869d33f68315fcda725da`  
**Result SHA-256:** `8e374cdcb4cd6bd6c285dc623ed5c254ba78782fec6ab0628650245c347ba1c3`  
**Artifact digest:** `sha256:e041448853e9d6564be7fca3c95013ec9417f38b20f20063577fc7eed64b1bc5`  
**Status:** COMPLETE / QUALIFIED REDUCED-GENERATOR CORE

For the source-locked local Markovian equation

[
ddot q+gammadot q+omega^2q=0,
]

the clean-room first-order generator at (omega=1), (gamma=2) is

[
A=egin{pmatrix}0&1\\-1&-2end{pmatrix}.
]

At the analytic boundary (chi=gamma/(2|omega|)=1):

- generator eigenvalue (-1) has algebraic multiplicity 2;
- geometric multiplicity is 1;
- therefore the reduced first-order generator is defective;
- retarded poles coincide at (Omega=-i);
- pole separation is numerically 0;
- discriminant (gamma^2-4omega^2) is 0.

**Disposition:** the local Markovian reduced-generator / retarded-pole EP core is independently reproduced.

**Ceiling:** this does not independently derive the microscopic self-energy, validate the manuscript's covariance phrasing, establish universal (chi=1) optimality, or establish cross-domain inheritance. Those remain separate source-audit questions.
