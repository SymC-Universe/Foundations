# Chemistry Handoff Rules v1.0

**Purpose:** apply the closed Stability Arc architecture to ChemSA and related chemistry work without importing unsupported universal claims.

## 1. What chemistry inherits

Chemistry inherits a **coupled scalar-modal analysis protocol**.

It does not inherit a requirement that every reaction, barrier, vibrational mode, friction model, surface coordinate, or rate process collapse to one scalar.

It also does not inherit a rule that scalar coordinates are dispensable.

The chemistry analysis must preserve both the scalar stability information and the physical mode/direction to which that information belongs.

## 2. Required chemistry workflow

### A. Define the physical object first

Identify the actual object being analyzed:

- normal mode;
- reaction coordinate;
- local Hessian block;
- dynamical matrix;
- response matrix;
- generalized Langevin or friction kernel;
- barrier mode;
- surface phonon/adsorbate mode;
- conformational mode;
- fitted generator.

Do not select a Stability Arc coordinate before the physical carrier is defined.

### B. Preserve modal geometry

Record, where available:

- eigenvector or mode direction;
- mode identity and symmetry;
- participation weights;
- coupling to neighboring modes;
- degeneracy or near-degeneracy;
- basis/coordinate convention;
- whether the mode is localized, delocalized, reactive, bath-like, or mixed.

### C. Compute scalar coordinates attached to that mode

Potential quantities include:

- mode damping rate;
- oscillation frequency;
- \(\chi=\Gamma/(2\Omega)\) when the mode genuinely supports that reduction;
- repeated-root discriminant or equivalent boundary distance;
- eigenvalue real and imaginary parts;
- Routh-Hurwitz margins for higher-order reduced dynamics;
- barrier height, rate, friction coordinate, or other domain-specific scalar when physically justified.

### D. Keep the assignment

A scalar must remain attached to its mode or subspace.

If a calculation changes basis or tracks modes across parameter values, preserve the mode correspondence rule.

Avoid comparing "the nearest scalar value" when the associated modes are physically different.

## 3. When \(\chi\) is appropriate

Use \(\chi\) confidently when the identified chemistry mode is genuinely represented by an underdamped/critically damped/overdamped second-order structure with physically meaningful \(\Gamma\) and \(\Omega\).

In that case, \(\chi\) is a high-value scalar coordinate.

Still report the mode identity and vector/subspace information that tells us what \(\chi\) describes.

## 4. When \(\chi\) is insufficient

Do not treat a single \(\chi\) as the complete chemistry stability descriptor when:

- several coupled modes compete;
- the mode is strongly non-normal;
- memory/friction is frequency-dependent;
- the effective generator is higher than second order;
- stochastic multiplicative structure materially affects stability;
- mode identity changes across the scan;
- the response is nonidentifiable;
- multiple scalar margins are independently required.

In these cases, carry a scalar vector plus modal geometry.

## 5. No scalar-only optimization

Do not optimize chemistry parameters merely to make a scalar approach 1.

A result near \(\chi=1\) is meaningful only if:

1. the associated mode is physically and numerically identified;
2. the repeated-root/damping interpretation is the registered question;
3. the coordinate was not selected after outcome inspection;
4. competing stability coordinates do not invalidate the interpretation.

## 6. Distinguish chemical questions

Do not collapse:

- barrier height;
- reaction rate;
- damping morphology;
- rate turnover;
- dynamic stability;
- mode localization;
- exceptional-point proximity;
- observability;
- friction regime.

A relationship among them is evidence only after a registered comparison.

## 7. Minimum chemistry stability record

Every promoted chemistry coordinate should include:

1. system, phase, temperature, medium, and geometry;
2. source model or computational method;
3. exact mode/reaction-coordinate definition;
4. modal/vector representation;
5. scalar coordinate set;
6. scalar-to-mode assignment;
7. uncertainty and numerical-quality record;
8. stability/reduction/refusal status;
9. source/data/code provenance;
10. statement of what the coordinate is and is not claimed to predict.

## 8. Cross-source and cross-system use

For literature atlases, maintain the existing pairing discipline.

Do not pair scalar quantities from different physical definitions merely because they share a symbol.

If rate, barrier, frequency, or friction data are paired across sources, require the same system, phase, temperature, medium, and coordinate definition to the extent specified by the relevant atlas contract.

Do not pool across generator or boundary classes without a frozen pooling rule.

## 9. Refusal is a valid chemistry result

Examples:

- mode correspondence not identifiable;
- damping estimate not separable from inhomogeneous broadening;
- no stable 2D reduction;
- higher-order dynamics required;
- insufficient uncertainty information;
- inconsistent source definitions;
- response window inadequate.

Return a refusal or nonidentifiable state rather than manufacture a scalar.

## 10. What chemistry may cite internally from this handoff

It may rely on the following architecture statements:

- scalar and modal information are complementary;
- a legitimate 2D quotient can carry a basis-invariant \(\chi\)-type coordinate;
- stochastic or higher-order stability may require multiple invariant margins;
- one scalar gate can be insufficient for full stability;
- distinct stability metrics can order the same dynamics differently;
- preservation of mode identity and scalar-to-mode assignment is mandatory for interpretation.

It may not inherit the bounded quantum crossing statistics as evidence for a chemical mechanism.

## 11. Escalation rule

If chemistry exposes a system that does not fit the current contract, do not alter the contract retroactively to fit it.

Record the mismatch as a model-boundary or identifiability signal. If important, open a new Stability Arc derivation phase with a fresh preregistration.
