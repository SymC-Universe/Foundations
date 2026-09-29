# F-16 GVT External Benchmark Data Intake v0.1

**Date:** 2026-09-28
**Governance:** SymC GOM v1.0
**Use class:** P0-Q EXTERNAL MEASURED BENCHMARK
**P1 eligibility:** NO
**Status:** ACQUISITION / IDENTITY PREFLIGHT - RAW VALUES NOT SCORED

## Dataset identity

Dataset: F-16 Aircraft Benchmark Based on Ground Vibration Test Data.

Creators:
- Jean-Philippe Noel
- Maarten Schoukens

Publisher:
- 4TU.Centre for Research Data

DOI:
- 10.4121/12954911

Official dataset description states that the benchmark is a full-scale F-16 ground-vibration experiment with clearance/friction nonlinearities concentrated at payload mounting interfaces. The public package contains system description material plus estimation and validation/test data in CSV and MAT formats.

## Official programmatic source

The maintained MaartenSchoukens/nonlinear_benchmarks loader for F16() downloads the package from:

https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f

The loader declares an expected download size of 148,455,295 bytes and extracts F16GVT_Files/BenchmarkData.

The loader assigns files containing Validation to the test collection and other nonspecial multisine files to the training collection. This intake records that loader semantics but does not open or score signal values.

## Rights / redistribution boundary

The dataset is publicly accessible through 4TU for research use, but recent published work using the dataset reports a license that does not permit redistribution by downstream authors. Therefore:

- raw F-16 payload files will not be committed to this repository;
- raw files will not be uploaded as GitHub Actions artifacts;
- only hashes, archive/file metadata, source pointers, and derived results allowed by the governing license may be retained;
- any later analysis must reacquire the source from the official 4TU endpoint at runtime.

This is a conservative compliance posture. It does not assert broader redistribution rights.

## Intake preflight

The first execution is acquisition/identity only.

Allowed:
- download the official archive;
- record HTTP/final source identity;
- compute archive SHA-256;
- verify total byte size;
- list archive member names, sizes, CRC values, and extensions;
- identify the BenchmarkData file inventory;
- classify filenames as estimation/training, Validation/test, SpecialOddMSine, or other based on names only.

Prohibited:
- parse MAT/CSV numeric signal values;
- inspect outputs to choose channels or frequency bands;
- fit any model;
- score any train/test outcome.

## Intake dispositions

- INTAKE_PASS if the official archive downloads, its byte size matches the maintained loader declaration, the ZIP is structurally valid, and a nonempty BenchmarkData inventory is present.
- INTAKE_IDENTITY_CHANGED if the official source downloads but byte size or expected layout differs from the maintained loader declaration. Preserve the new hash/layout and require adjudication before scoring.
- INTAKE_BLOCKED_SOURCE if the official source cannot be downloaded.
- INVALID_ARCHIVE if the download is not a valid archive.

An INTAKE_PASS permits construction of a separately frozen F-16 P0-Q protocol. It does not authorize scoring by itself.
