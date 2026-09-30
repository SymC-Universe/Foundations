# Near-One / 0.7188% Pattern Investigation

Scope: canonical completed MG and free-neutrino adversarial responses only.

## 1. The two reported numbers are algebraically linked

Observed best rank-1 residual fraction:

0.007188352738

or, as a percentage:

0.71883527%

Observed effective dimension:

1.014480039471

For a rank-two spectrum with residual fraction f, the participation-ratio effective dimension is exactly

d_eff = 1 / ((1-f)^2 + f^2).

Substituting the observed residual gives:

1.014480039471

Absolute numerical discrepancy:

2.220e-16

Therefore 1.01448 and 0.7188% are not independent coincidences. They encode the same two-singular-value spectrum.

## 2. Raw amplitude-preserving geometry

MG / neutrino response norm ratio:

0.10481953

Cosine similarity:

-0.57974081

Angle:

125.43231497 degrees

The MG response norm is only about 10.482% of the neutrino response norm. This amplitude imbalance strongly forces the raw two-row matrix toward rank one.

## 3. Direction-only geometry

After normalizing each adversary response vector to unit length:

direction-only d_eff = 1.49689460
direction-only rank-1 residual = 21.01295928%

Thus the near-1 raw d_eff and 0.7188% raw residual are not invariant to removing relative response amplitude. The directional structure is much less one-dimensional.

## 4. Fixed-norm random-direction null

Null: two independent random directions in four dimensions with the observed MG and neutrino norms held fixed.

N = 500000
seed = 260930

P(null residual <= observed) = 0.30628600
P(null residual >= observed) = 0.69371400
P(|null cosine| >= |observed cosine|) = 0.30628600

Null residual quantiles:
2.5% = 0.00156805
5%   = 0.00245159
50%  = 0.00906695
95%  = 0.01085073
97.5%= 0.01086339

The observed residual is therefore not unusual under a null that preserves the strong response-amplitude imbalance.

## 5. Interpretation

The scientifically meaningful feature is not numerical proximity of 1.01448 to 1 or the percentage rendering 0.7188 to an earlier ~0.72 value.

The meaningful current result is a split between:

- amplitude-weighted structure: almost rank one because the neutrino adversary dominates total response magnitude;
- response direction: materially non-collinear, so adversary identity is not represented by amplitude alone.

The percentage form 0.7188% is a presentation choice for the dimensionless fraction 0.007188. Multiplying by 100 cannot create a scale-invariant correspondence to an unrelated ~0.72 stability coordinate.

This result does not refute the broader Stability Architecture program. It specifically refuses promotion of this numerical near-match as evidence. The directional-versus-amplitude separation remains a legitimate object for subsequent representation testing.

## Literature context

The participation-ratio logic is compared against [Lee26b]; representation sufficiency against [Sui25]; and compression sensitivity against [Hea20].

[Lee26b] arXiv:2602.08207
[Sui25] DOI 10.3847/1538-4357/ae3aa4
[Hea20] DOI 10.1093/mnras/staa2589
