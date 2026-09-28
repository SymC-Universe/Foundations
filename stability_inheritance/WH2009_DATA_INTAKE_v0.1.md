# Wiener-Hammerstein 2009 External Benchmark Data Intake v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Use class:** P0-Q EXTERNAL MEASURED BENCHMARK ONLY
**P1 eligibility:** NO
**Status:** INTAKE_PASS_WITH_LIMITS

## Dataset identity

Dataset: Wiener-Hammerstein benchmark introduced for IFAC SYSID 2009.

Official benchmark page:
https://www.nonlinearbenchmark.org/benchmarks/wiener-hammerstein

Official loader:
https://github.com/MaartenSchoukens/nonlinear_benchmarks/blob/master/nonlinear_benchmarks/benchmarks.py

Native system class:
A static nonlinearity sandwiched between two linear time-invariant blocks.

Canonical citation:
J. Schoukens, J. Suykens, and L. Ljung, "Wiener-Hammerstein Benchmark," 15th IFAC Symposium on System Identification (SYSID 2009), St. Malo, France, 2009.

Public text mirror used for runtime-accessible bytes:
https://github.com/matheuswhite/narmax/blob/master/res/wienerhammer.csv

Mirror Git blob SHA:
865a402fc495291422133f7473867a82a8aee12e

Mirror size:
4,478,837 bytes

The mirror repository identifies this file as the IFAC SYSID 2009 Wiener-Hammerstein benchmark and reports 188,000 samples.

Expected columns:
- uBenchMark
- yBenchMark

Official loader split:
- discard initial samples [0, 5200)
- retained benchmark record [5200, 184000)
- official train [5200, 105200), 100,000 samples
- official test [105200, 184000), 78,800 samples
- test initialization window = 50 samples

## Exposure statement

Before this intake/protocol freeze, only official loader semantics, benchmark description, and public mirror metadata were inspected. Raw CSV values and official test outcomes were not parsed, summarized, fitted, or scored.

This remains a public historical benchmark and therefore P0-Q only even with a pre-scoring protocol freeze.

## Rights/provenance limits

The source is a public system-identification benchmark. This record does not infer redistribution rights for the mirror beyond using the publicly accessible benchmark for analysis. Raw bytes will not be committed into the SymC repository.

## Scientific role

Test whether a simple nonlinear autoregressive representation materially changes held-out one-step/free-run behavior relative to a linear representation with the same lag horizon.

Do not claim Wiener-Hammerstein mechanism discovery, state-of-the-art system identification, or Stability Inheritance novelty.

## chi admission

No physical chi is admitted from the input/output record by default.
