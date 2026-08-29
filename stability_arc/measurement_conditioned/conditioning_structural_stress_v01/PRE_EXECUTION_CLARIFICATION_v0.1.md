# Pre-execution clarification for conditioning structural stress v0.1

**Timing:** before audit implementation and before any stress fixture outcome was generated or inspected.

The first frozen prose version of `PREREGISTRATION_CONDITIONING_STRUCTURAL_STRESS_v0.1.md` stated that the explicit corner panel contained **16** cases and said to use all combinations of two `eta` values and four `(gamma,kappa,omega)` tuples, but its final bullet said the two state signs were to be "alternating by combination index." Read literally, alternation would produce only 8 cases, conflicting with the explicit count of 16 and the phrase "all combinations."

This is a preregistration-text ambiguity, not a scientific outcome.

The controlling interpretation is fixed **before execution** as the complete Cartesian product:

`2 eta values x 4 dynamical tuples x 2 state signs = 16 corner cases`.

Both states

- `(x,y,z)=(0.04,0,0.998)`
- `(x,y,z)=(0.04,0,-0.998)`

are therefore tested for every `(eta, gamma, kappa, omega)` combination.

No parameter value, threshold, hypothesis, directional gate, or decision rule is changed. This note exists so the ambiguity is not silently resolved inside code after execution.

Original preregistration blob SHA before this clarification: `5a1d0967b7d2ea2d9102e6e749c7427da4e4730d`.
