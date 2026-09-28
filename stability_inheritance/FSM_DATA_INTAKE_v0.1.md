# Fine Steering Mirror External Benchmark Data Intake v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Use class:** P0-Q EXTERNAL MEASURED BENCHMARK ONLY
**P1 eligibility:** NO
**Status:** INTAKE_PASS

## Dataset identity

Dataset: CubeSpec Fine Steering Mirror benchmark.

Official repository:
https://github.com/merijnfloren/fsm-benchmark-data

Official benchmark loader:
https://github.com/MaartenSchoukens/nonlinear_benchmarks/blob/master/nonlinear_benchmarks/benchmarks.py

Native description:
- three voltage inputs applied to piezo actuators;
- three non-collocated displacement outputs;
- orthogonal random-phase multisine excitation;
- 100 mV, 200 mV, and 300 mV amplitude levels;
- mostly linear platform with hysteretic piezo nonlinearities;
- sampling frequency 6400 Hz;
- train and test realizations separated by the official dataset.

Citation:
M. Floren, L. Peri, J. De Maeyer, W. De Munter, D. Vandepitte, and J.-P. Noël, "Data-driven state-space identification and nonlinearity assessment of the CubeSpec Fine Steering Mirror," ISMA-USD 2024, pp. 2042-2052.

License:
Creative Commons Attribution 4.0 International (CC BY 4.0), as stated in the official repository LICENSE.

Raw benchmark object:
https://github.com/merijnfloren/fsm-benchmark-data/raw/refs/heads/main/data/combined_data.npz

Expected arrays from the official loader:
- u_100mV_train, y_100mV_train
- u_200mV_train, y_200mV_train
- u_300mV_train, y_300mV_train
- corresponding *_test arrays

Expected train structure:
N=8192 samples, 3 inputs/outputs, R=6 realizations, P=2 steady-state periods.

Expected test structure:
N=8192 samples, 3 inputs/outputs, R_test=3 realizations, P=2 periods.

## Evidence class and exposure

This is a public historical benchmark and is P0-Q external measured evidence only. It is never untouched P1 evidence.

Before the protocol freeze, only repository documentation, loader semantics, and license were inspected. Raw combined_data.npz and official test values were not opened or summarized.

## Scientific role

Use the benchmark to test:
- whether one linear frequency-response representation transports across excitation amplitudes;
- whether amplitude-conditioned response architecture is measurably different;
- whether a pooled linear representation is sufficient for the declared frequency-domain task.

Do not use it to claim a new hysteresis mechanism or Stability Inheritance novelty.

## chi admission

No scalar chi is admitted from this dataset by default. The benchmark supplies input/output measurements, not an independently licensed damping scalar. Any later scalar diagnostic must enter separately and cannot be treated as physical chi without native identification.
