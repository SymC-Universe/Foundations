# Silverbox External Benchmark Data Intake v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Use class:** P0-Q EXTERNAL MEASURED BENCHMARK ONLY
**P1 eligibility:** NO
**Status:** INTAKE_PASS_WITH_LIMITS

## Dataset identity

Dataset: Silverbox nonlinear system-identification benchmark.

Native description: measured electronic implementation of a Duffing-like oscillator / second-order linear dynamic block with cubic static nonlinearity in feedback.

Canonical citation:
T. Wigren and J. Schoukens, "Three free data sets for development and benchmarking in nonlinear system identification," 2013 European Control Conference (ECC), pp. 2933-2938.

Official/current loader source:
https://github.com/MaartenSchoukens/nonlinear_benchmarks/blob/master/nonlinear_benchmarks/benchmarks.py

Official archive URL embedded in the loader:
https://drive.google.com/file/d/17iS-6oBUUgrmiAcrZoG9S5sOaljZnDSy/view

Public mirror used for connector-accessible bytes:
https://github.com/matheuswhite/narmax/blob/master/res/SilverboxFiles/SNLS80mV.csv

Mirror Git blob SHA:
e2da84aacb3ec60959274bbe1fd8e47be66ff0b2

Mirror file size:
2,649,634 bytes

Independent public audit record reports the raw SNLS80mV.csv SHA-256 as:
ae62d5a91230c10f76e6dd02c8a4fac3c9d4d8a95fbf50e87cb0c4885003e0f1

Audit source:
https://github.com/Zhengze-lab/sparse-adaptive-closures/blob/dc4dbee17aca0ba0db7de9389f5416c81643691e/results/silverbox_data_audit/raw_files.csv

Columns:
- V1: input
- V2: measured output

Sampling frequency:
610.35 Hz

## Official split inherited prospectively

The official nonlinear_benchmarks loader defines:

- arrow test: samples [100, 40575)
- arrow no-extrapolation test: first 32000 samples of the arrow segment, equivalent to [100, 32100)
- multisine block: [40650, 127400)
- multisine train/validation block: first 75% of multisine = [40650, 105712)
- multisine reserved test block: [105712, 127400)
- test state-initialization window: 50 samples

These indices are frozen for this P0-Q benchmark.

## Exposure statement

Before this intake/protocol freeze, the repository blob was fetched once only to verify connector access and its first approximately 100 characters were inspected. No test segment was parsed, fitted, summarized, or scored. Because Silverbox is a public historical benchmark and is classified P0-Q external/seen data regardless, it is not eligible for untouched P1 evidence.

## Rights/provenance state

The benchmark is publicly distributed for development and benchmarking and is explicitly cited by the official loader. This record does not assert a broader redistribution license beyond the public benchmark use. Raw bytes will not be committed into the SymC repository unless a clear redistribution license is established.

## Limitations

- Public historical benchmark: cannot support a novel untouched-evidence claim.
- Electronic Duffing analog: relevant to nonlinear representation qualification, not a literal mechanical inheritance system.
- Input/output measurements alone do not independently identify a physical damping parameter or license a universal physical chi.
- The strongest published Silverbox system-identification methods are more sophisticated than the deliberately small comparator stack used in this P0-Q representation test; therefore no state-of-the-art superiority claim is permitted.
