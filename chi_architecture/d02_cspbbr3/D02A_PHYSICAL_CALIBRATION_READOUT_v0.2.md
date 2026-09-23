# D02A CsPbBr3 Physical Calibration Readout v0.2

**Date:** 2026-09-22  
**Status:** P0-D PHYSICAL CALIBRATION / POST-RESULT PARSER DEVELOPMENT  
**Scientific freeze:** `27164b36a0c3ecd1931cfe8cdf840f6fc7b9fbb6`  
**v0.1 partial archive:** `d5af53320608be627b8edfcc3dfc2eb778986310`  
**v0.2 execution archive:** `c83f2136e7b633f6a4172b79941c136dbccad3de`  
**Claim ceiling:** no untouched confirmation, no recovery claim, no new phonon law, no licensed lowercase chi

## 1. Why this experiment matters

D02A was the first post-D01 test on real material source data rather than a constructed linear family.

The target was deliberately joint:

1. a local native damping observable;
2. a carrier-resolved reciprocal-space organization;
3. thermal embedding across structural phases;
4. the question of whether local scalar information can be preserved, transformed, reorganized, or refused without discarding the carrier structure.

The 2021 CsPbBr3 result was qualitatively known before the D02A freeze, so this experiment is physical calibration only.

## 2. Source integrity

The publisher source workbooks were fetched directly and SHA-256 locked.

- Figure 3 source SHA-256: `6db8784c4e8e95c560ccce0bebe70b86dfc7613cccfe62853dc7eec7a25a1a0a`
- Figure 4 source SHA-256: `938d401c4b6ce766244d2c1dba9edd5d0804067ec8d21b5d43379241bab78bf5`

The reviewer-facing reproduction command is:

`python chi_architecture/reproduce.py d02a`

The command downloads the exact publisher files, verifies the locked hashes, runs both v0.1 and v0.2 parser tests, reconstructs the valid source quantities, and writes the result/summary/card/manifest bundle.

## 3. v0.1 failure is retained

The first prospective FIG3 parser treated columns A:C as row-wise q/E/intensity tuples.

That interpretation was wrong. The workbook stores Figure 3 as 2D matrices.

The official v0.1 status remains:

`PARTIAL_VALID_LINEWIDTH__CARRIER_PARSER_INADEQUATE__CHI_REFUSED`

The failure was not rewritten after the fact.

Valid v0.1 content:

- exact source-file hashes;
- the six-row Figure 4b M-point linewidth table;
- source linewidth uncertainties;
- lowercase-chi refusal.

Invalid v0.1 content:

- the original A:C carrier-map extraction;
- a direct goodness-of-fit interpretation from vertically offset plotting curves.

## 4. Corrected v0.2 carrier geometry

After a full workbook-layout diagnostic, v0.2 was separately frozen before corrected carrier extraction.

### 300 K, orthorhombic

- q axis: 21 values, 0.5 to 1.0 rlu;
- energy axis: 46 values, -0.5 to 3.0 meV;
- source S(Q,E) matrix: 46 x 21.

### 385 K, tetragonal

- q axis: 21 values, 0.5 to 1.0 rlu;
- energy axis: 38 values, -0.5 to 2.2 meV;
- source S(Q,E) matrix: 38 x 21.

### 419 K, cubic

- q axis: 21 values, 0.5 to 1.0 rlu;
- energy axis: 21 values, 0.0 to 4.0 meV;
- source S(Q,E) matrix: 21 x 21.

All three maps therefore retain the same source-defined M-R q grid.

Because SPINS and CNCS intensities are not assumed to share an absolute calibration, v0.2 does not compare raw intensity amplitudes across instruments.

## 5. Frozen normalized carrier-shape comparison

The comparison uses only the common nonnegative energy support:

`0.0 to 2.2 meV`

on a fixed 0.2 meV grid.

For each q column:

1. source intensity is linearly interpolated onto the common energy grid;
2. negative interpolated values are clipped to zero;
3. the q-column is normalized by its positive common-window sum;
4. the normalized energy centroid, RMS width, and grid peak are recorded.

No categorical similarity threshold was introduced.

All 21 q profiles were identifiable in every phase.

## 6. Local linewidth transformation

The source M-point linewidth table is:

| Temperature (K) | Phase bin | Linewidth (meV) | Source error (meV) |
|---:|---|---:|---:|
| 50 | orthorhombic | 0.200 | 0.030 |
| 100 | orthorhombic | 0.320 | 0.050 |
| 200 | orthorhombic | 0.493 | 0.037 |
| 300 | orthorhombic | 0.770 | 0.070 |
| 385 | tetragonal | 9.110 | 0.490 |
| 500 | cubic | 9.490 | 0.230 |

The 300 K to 385 K change is:

`0.77 -> 9.11 meV`

or a factor of:

`11.8312x`.

The difference is 8.34 meV. Dividing by the quadrature-combined source uncertainties gives a descriptive standardized difference of approximately:

`16.85`.

The 385 K to 500 K change is only:

`9.11 -> 9.49 meV`

with a descriptive standardized difference of approximately:

`0.70`.

This is a strong phase-associated transformation of the local damping observable, followed by persistence of the large-linewidth regime.

## 7. Carrier-shape result

Every q profile in the frozen common window has its maximum at 0 meV in all three phase maps.

Thus the source-defined M-R sector retains a strong quasielastic maximum throughout the orthorhombic, tetragonal, and cubic maps under this normalized representation.

The distributed shape, however, does not remain identical.

### 300 K -> 385 K

- centroid RMS difference: `0.09924 meV`
- width RMS difference: `0.14747 meV`
- centroid Pearson r: `0.8511`
- width Pearson r: `0.7730`

### 385 K -> 419 K

- centroid RMS difference: `0.24327 meV`
- width RMS difference: `0.13918 meV`
- centroid Pearson r: `0.3033`
- width Pearson r: `0.4080`

### 300 K -> 419 K

- centroid RMS difference: `0.27299 meV`
- width RMS difference: `0.21395 meV`
- centroid Pearson r: `0.4905`
- width Pearson r: `0.7239`

The 300-to-385 K normalized centroid/width organization is substantially more correlated than the 385-to-419 K organization, while the zero-energy maximum remains present across the whole M-R q grid.

No threshold converts these descriptive numbers into a binary inheritance claim.

## 8. Lowercase chi remains refused

The Figure 4 source table reports a DHO-derived linewidth `Gamma_LW`, but it does not tabulate the same-condition natural frequency `omega0` required by the frozen candidate construction

`chi_DHO = Gamma/(2 omega0)`.

The plotting curves are not reverse-fit for `omega0`.

Therefore:

`LOWERCASE_CHI = REFUSED`

with status:

`OMEGA0_NOT_IDENTIFIABLE_FROM_LOCKED_SOURCE_TABLES`.

This is a scientific result, not a missing-data nuisance to be patched away.

## 9. Joint chi / Chi interpretation

D02A supports a bounded architecture statement:

- a local damping observable can transform sharply;
- the same reciprocal-space carrier sector remains traceable;
- the normalized distributed spectral organization can partly persist and partly reorganize across phase;
- a scalar chi need not be available for the carrier-resolved architecture to remain scientifically meaningful.

For this physical system the most faithful state is therefore not a new scalar. It is the native joint object:

`temperature/phase + M-R carrier sector + q-resolved spectral shape + M-point linewidth`.

That is a broader architecture in the descriptive sense, not evidence for a new physical field or master Chi coordinate.

## 10. Native-comparator verdict

The original phonon work already reports:

- extreme damping on warming from the orthorhombic to tetragonal phase;
- overdamping throughout the M-R region in the cubic phase;
- extended overdamped modes over Brillouin-zone edges;
- corresponding two-dimensional sheets of correlated octahedral rotations.

The D02A reproduction numerically restates and decomposes those facts, but it does not outperform the native q-resolved neutron/X-ray plus anharmonic-phonon analysis.

Official comparator verdict:

`NATIVE_PHONON_TOOLKIT_SUFFICIENT`

This is not a failure of the architecture investigation. It establishes a boundary:

`SYMC_REPRESENTATION_USEFUL != NEW_NATIVE_PHYSICS`.

## 11. Stability-inheritance consequence

D02A does not justify the claim that a scalar stability value is inherited.

It supports a weaker, more defensible physical pattern:

`CARRIER_CORRESPONDENCE_PERSISTS / LOCAL_DAMPING_TRANSFORMS / DISTRIBUTED_SHAPE_REORGANIZES / SCALAR_CHI_REFUSED`.

That pattern is a useful candidate template for future untouched tests, but D02A cannot confirm it prospectively because the paper's broad result and the v0.2 parser repair were already known before the relevant interpretations were frozen.

## 12. What the next physical test must improve

The next test should be untouched at the decisive-outcome level and should ideally contain:

1. a directly tabulated local natural frequency and damping/linewidth under the same condition, so scalar admission can be tested rather than assumed;
2. an independently defined carrier or invariant subspace;
3. a controlled coupling, substrate, temperature, pressure, or environmental change;
4. a future/held-out outcome or perturbation response;
5. the strongest domain-native comparator;
6. a failure outcome frozen before inspection.

D02A closes the first real-data loop and tells us exactly what the next physical experiment must contain.
