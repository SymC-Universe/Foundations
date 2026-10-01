"""Laptop-safe adversarial geometry analysis.

Reads only canonical completed result JSONs. Writes only to:
    cosmology_desi/laptop_parallel_results/

Purpose:
- compare standardized response vectors from completed adversaries;
- test whether a single scalar response amplitude preserves adversary identity;
- provide a pre-F3 geometry diagnostic without defining or promoting capital Chi.

Outputs:
- adversarial_geometry_vectors.csv
- adversarial_geometry_summary.csv
- LAPTOP_ADVERSARIAL_GEOMETRY_REPORT.md
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = ROOT / "laptop_parallel_results"
OUT.mkdir(parents=True, exist_ok=True)

PARAMS = ["omegam", "sigma8", "H0", "S8_standard"]


def load_json(name):
    with (RESULTS / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def unit(v):
    n = float(np.linalg.norm(v))
    if n == 0:
        return v.copy()
    return v / n


mg = load_json("dmde_dr1_mg_comparison.json")
nu = load_json("dmde_neutrino_adversary_analysis.json")

mg_vec = np.array(
    [mg["descriptive_shifts"][p]["difference_in_baseline_sd"] for p in PARAMS],
    dtype=float,
)
nu_vec = np.array(
    [nu["cmb_fixed_vs_free_mnu"]["shifts"][p]["difference_in_fixed_sd"] for p in PARAMS],
    dtype=float,
)

vectors = {
    "modified_gravity": mg_vec,
    "free_neutrino_mass": nu_vec,
}

with (OUT / "adversarial_geometry_vectors.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    w = csv.writer(f)
    w.writerow(["adversary", *PARAMS, "l2_norm"])
    for name, vec in vectors.items():
        w.writerow([name, *[f"{x:.12g}" for x in vec], f"{np.linalg.norm(vec):.12g}"])

u_mg = unit(mg_vec)
u_nu = unit(nu_vec)
cosine = float(np.dot(u_mg, u_nu))
cosine = max(-1.0, min(1.0, cosine))
angle_deg = float(np.degrees(np.arccos(cosine)))

# Two-row response matrix: adversaries x observables.
R = np.vstack([mg_vec, nu_vec])
singular_values = np.linalg.svd(R, compute_uv=False)
sv2 = singular_values ** 2
response_deff = float((sv2.sum() ** 2) / np.square(sv2).sum())

# Best rank-1 reconstruction and residual fraction.
u, s, vt = np.linalg.svd(R, full_matrices=False)
rank1 = s[0] * np.outer(u[:, 0], vt[0, :])
residual = R - rank1
fro2 = float(np.sum(R ** 2))
resid2 = float(np.sum(residual ** 2))
rank1_residual_fraction = resid2 / fro2 if fro2 else float("nan")

with (OUT / "adversarial_geometry_summary.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    w = csv.writer(f)
    w.writerow(["metric", "value"])
    w.writerow(["cosine_similarity_mg_vs_mnu", f"{cosine:.12g}"])
    w.writerow(["angle_degrees_mg_vs_mnu", f"{angle_deg:.12g}"])
    w.writerow(["response_effective_dimension", f"{response_deff:.12g}"])
    w.writerow(["rank1_residual_fraction", f"{rank1_residual_fraction:.12g}"])
    for i, val in enumerate(singular_values, start=1):
        w.writerow([f"singular_value_{i}", f"{val:.12g}"])

report = f"""# Laptop Adversarial Geometry Report

Scope: canonical completed-result analysis only. No active-run files were touched.

## Standardized response vectors

Observable order:
{", ".join(PARAMS)}

Modified-gravity response:
{mg_vec.tolist()}

Free-neutrino-mass response:
{nu_vec.tolist()}

## Geometry

Cosine similarity:

{cosine:.6f}

Angle between response directions:

{angle_deg:.6f} degrees

Effective dimensionality of the two-adversary response matrix:

{response_deff:.6f}

Fraction of total squared response not captured by the best rank-1 approximation:

{rank1_residual_fraction:.6f}

## Interpretation rule

This is a representation diagnostic, not evidence for Stability Architecture.

If the two completed adversaries are nearly collinear and the rank-1 residual is tiny,
a single response amplitude may preserve most of their currently sampled structure.

If they are materially non-collinear and rank-1 loss is non-trivial, the direction
of the multivariate response contains information that a scalar amplitude discards.
That would motivate, but not yet qualify, a vector/modal representation for adversarial
response.

No capital-Chi construction is promoted by this run.
"""

with (OUT / "LAPTOP_ADVERSARIAL_GEOMETRY_REPORT.md").open(
    "w", encoding="utf-8"
) as f:
    f.write(report)

print("Laptop adversarial geometry analysis complete.")
print(f"Output folder: {OUT}")
print(f"MG-vs-neutrino cosine similarity = {cosine:.6f}")
print(f"MG-vs-neutrino angle = {angle_deg:.6f} degrees")
print(f"Response effective dimension = {response_deff:.6f}")
print(f"Best rank-1 residual fraction = {rank1_residual_fraction:.6f}")
