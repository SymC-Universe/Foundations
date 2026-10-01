"""Laptop-safe RQE baseline analysis.

Reads only already-canonical DESI result/data files and writes only to:
    cosmology_desi/laptop_parallel_results/

This script does NOT read or write active-run checkpoints/results.

Outputs:
- bao_correlation_eigenspectrum.csv
- baseline_core_correlation_eigenspectrum.csv
- adversarial_response_matrix.csv
- LAPTOP_RQE_BASELINE_REPORT.md

Scientific note:
The eigenvalue participation ratios here are diagnostic summaries of
normalized correlation structure. They are NOT substituted for the
Lee-style Fisher information dimension required by RQE F2.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DATA = ROOT / "data"
OUT = ROOT / "laptop_parallel_results"
OUT.mkdir(parents=True, exist_ok=True)


def load_json(name: str):
    with (RESULTS / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def participation_ratio(eigenvalues: np.ndarray) -> float:
    vals = np.asarray(eigenvalues, dtype=float)
    vals = vals[np.isfinite(vals)]
    vals = vals[vals > 0]
    if vals.size == 0:
        return float("nan")
    return float(vals.sum() ** 2 / np.square(vals).sum())


def correlation_from_covariance(cov: np.ndarray) -> np.ndarray:
    sd = np.sqrt(np.diag(cov))
    if np.any(sd <= 0):
        raise ValueError("Covariance has non-positive diagonal entries.")
    corr = cov / np.outer(sd, sd)
    return (corr + corr.T) / 2.0


def write_eigenspectrum(path: Path, eigenvalues: np.ndarray):
    vals = np.sort(np.real(eigenvalues))[::-1]
    total = vals.sum()
    cumulative = 0.0
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "eigenvalue", "fraction", "cumulative_fraction"])
        for i, val in enumerate(vals, start=1):
            frac = float(val / total) if total else float("nan")
            cumulative += frac
            w.writerow([i, f"{val:.12g}", f"{frac:.12g}", f"{cumulative:.12g}"])


baseline = load_json("dmde_dr1_baseline_audit.json")
mg = load_json("dmde_dr1_mg_comparison.json")
nu = load_json("dmde_neutrino_adversary_analysis.json")

core_names = baseline["core_correlation_order"]
core_corr = np.array(baseline["core_correlation_matrix"], dtype=float)
core_eigs = np.linalg.eigvalsh(core_corr)
core_deff = participation_ratio(core_eigs)
write_eigenspectrum(OUT / "baseline_core_correlation_eigenspectrum.csv", core_eigs)

bao_cov = np.loadtxt(DATA / "desi_gaussian_bao_ALL_GCcomb_cov.txt")
bao_corr = correlation_from_covariance(bao_cov)
bao_eigs = np.linalg.eigvalsh(bao_corr)
bao_deff = participation_ratio(bao_eigs)
write_eigenspectrum(OUT / "bao_correlation_eigenspectrum.csv", bao_eigs)

params = ["omegam", "sigma8", "H0", "S8_standard"]
rows = []

for p in params:
    shift = mg["descriptive_shifts"][p]["difference_in_baseline_sd"]
    width = mg["descriptive_shifts"][p]["sd_ratio_mg_to_baseline"]
    rows.append({
        "adversary": "modified_gravity",
        "parameter": p,
        "median_shift_reference_sd": shift,
        "sd_ratio": width,
        "source": "dmde_dr1_mg_comparison.json",
    })

nu_block = nu["cmb_fixed_vs_free_mnu"]
for p in params:
    shift = nu_block["shifts"][p]["difference_in_fixed_sd"]
    width = nu_block["shifts"][p]["sd_ratio_free_to_fixed"]
    rows.append({
        "adversary": "free_neutrino_mass",
        "parameter": p,
        "median_shift_reference_sd": shift,
        "sd_ratio": width,
        "source": "dmde_neutrino_adversary_analysis.json",
    })

with (OUT / "adversarial_response_matrix.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    fields = [
        "adversary",
        "parameter",
        "median_shift_reference_sd",
        "sd_ratio",
        "source",
    ]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

largest_mg = max(
    (r for r in rows if r["adversary"] == "modified_gravity"),
    key=lambda r: abs(r["median_shift_reference_sd"]),
)
largest_nu = max(
    (r for r in rows if r["adversary"] == "free_neutrino_mass"),
    key=lambda r: abs(r["median_shift_reference_sd"]),
)

report = f"""# Laptop RQE Baseline Report

Scope: canonical-results-only parallel analysis. No active-run files were touched.

## Correlation-structure diagnostics

DR1 core posterior variables:
{", ".join(core_names)}

Normalized correlation participation ratio:

d_corr_core = {core_deff:.6f}

DR2 BAO 13-element normalized correlation participation ratio:

d_corr_BAO = {bao_deff:.6f}

These are correlation-structure diagnostics only. They are not the
Lee-style Fisher-information d_eff required to adjudicate RQE F2.
The latter remains pending the qualified resolved/full-shape information
matrix or equivalent held-out representation comparison.

## Adversarial response baseline

Largest standardized modified-gravity shift among
Omega_m, sigma8, H0, S8:

- {largest_mg["parameter"]}: {largest_mg["median_shift_reference_sd"]:.6f} reference SD
- posterior-width ratio: {largest_mg["sd_ratio"]:.6f}

Largest standardized free-neutrino-mass shift among the same variables:

- {largest_nu["parameter"]}: {largest_nu["median_shift_reference_sd"]:.6f} reference SD
- posterior-width ratio: {largest_nu["sd_ratio"]:.6f}

The complete matrix is in adversarial_response_matrix.csv.

## RQE interpretation

This run does not promote F2, F3, F4, F5, F6, or F7.

It establishes a reusable baseline describing:
1. normalized covariance/correlation dimensionality in already-canonical data;
2. the scale and direction of already-completed MG and neutrino adversarial responses;
3. the exact comparator outputs the active resolved/full-shape lane must later beat or explain.

No Stability Architecture claim is inferred from these diagnostics alone.
"""

with (OUT / "LAPTOP_RQE_BASELINE_REPORT.md").open("w", encoding="utf-8") as f:
    f.write(report)

print("Laptop-safe RQE baseline complete.")
print(f"Output folder: {OUT}")
print(f"DR1 core correlation d_corr = {core_deff:.6f}")
print(f"DR2 BAO correlation d_corr = {bao_deff:.6f}")
print(
    "Largest MG standardized shift: "
    f"{largest_mg['parameter']} = {largest_mg['median_shift_reference_sd']:.6f} SD"
)
print(
    "Largest free-mnu standardized shift: "
    f"{largest_nu['parameter']} = {largest_nu['median_shift_reference_sd']:.6f} SD"
)
