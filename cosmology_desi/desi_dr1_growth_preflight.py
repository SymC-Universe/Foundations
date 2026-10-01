#!/usr/bin/env python3
"""Exploratory DESI DR1 ShapeFit+BAO growth preflight.

This script is deliberately not a confirmatory cosmology analysis. The compressed
ShapeFit blocks were inspected during gate design and are used only to engineer
covariance handling and candidate growth-trajectory diagnostics.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2


def weighted_linear_fit(z, y, sigma):
    X = np.column_stack([np.ones_like(z), z])
    W = np.diag(1.0 / sigma**2)
    cov = np.linalg.inv(X.T @ W @ X)
    beta = cov @ X.T @ W @ y
    return beta, cov


def background_lcdm(z, omega_m0):
    z = np.asarray(z, dtype=float)
    e2 = omega_m0 * (1.0 + z)**3 + (1.0 - omega_m0)
    omega_m = omega_m0 * (1.0 + z)**3 / e2
    chi_delta = np.sqrt(2.0 / (3.0 * omega_m))
    q = 0.5 * omega_m - (1.0 - omega_m)
    return q, chi_delta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="cosmology_desi/data/desi_dr1_shapefit_bao_appendixA.json")
    ap.add_argument("--out", default="cosmology_desi/results/desi_dr1_growth_preflight.json")
    ap.add_argument("--omega-m0", type=float, default=0.2962,
                    help="Published DESI DR1 FS+BAO central Omega_m used only for background overlay.")
    args = ap.parse_args()

    payload = json.loads(Path(args.data).read_text())
    bins = payload["bins"]
    z = np.array([b["z"] for b in bins], dtype=float)
    fs8 = np.array([b["vector"][2] for b in bins], dtype=float)
    fid = np.array([b["f_sigma_s8_fid"] for b in bins], dtype=float)
    var = np.array([b["covariance_unscaled"][2][2] for b in bins], dtype=float) * float(payload["covariance_scale"])

    g = fs8 / fid
    sigma_g = np.sqrt(var) / fid
    residual = g - 1.0
    chi2_growth = float(np.sum((residual / sigma_g)**2))
    dof = len(g)
    p = float(chi2.sf(chi2_growth, dof))

    weights = 1.0 / sigma_g**2
    const = float(np.sum(weights * g) / np.sum(weights))
    const_sigma = float(np.sqrt(1.0 / np.sum(weights)))

    beta, beta_cov = weighted_linear_fit(z, g, sigma_g)
    q, chi_delta = background_lcdm(z, args.omega_m0)
    z_transition = float((2.0 * (1.0 - args.omega_m0) / args.omega_m0)**(1.0 / 3.0) - 1.0)

    out = {
        "status": "exploratory_engineering_only",
        "not_confirmatory_reason": payload["holdout_status"],
        "coordinate": "g_SF(z_i)=f_sigma_s8(z_i)/f_sigma_s8_fid(z_i)",
        "bins": [
            {
                "name": b["name"],
                "z": float(zz),
                "f_sigma_s8": float(f),
                "f_sigma_s8_fid": float(ff),
                "g_SF": float(gg),
                "sigma_g_SF": float(ss),
                "q_LCDM_overlay": float(qq),
                "chi_delta_LCDM_overlay": float(cc),
            }
            for b, zz, f, ff, gg, ss, qq, cc in zip(bins, z, fs8, fid, g, sigma_g, q, chi_delta)
        ],
        "growth_only_fiducial_test": {
            "chi2": chi2_growth,
            "dof": dof,
            "p_value": p,
        },
        "weighted_constant_g_SF": {
            "estimate": const,
            "sigma": const_sigma,
        },
        "weighted_linear_g_SF_vs_z": {
            "intercept": float(beta[0]),
            "intercept_sigma": float(np.sqrt(beta_cov[0, 0])),
            "slope_per_redshift": float(beta[1]),
            "slope_sigma": float(np.sqrt(beta_cov[1, 1])),
            "covariance": beta_cov.tolist(),
        },
        "background_overlay": {
            "model": "flat_LCDM",
            "omega_m0": args.omega_m0,
            "z_q0_equals_z_chi_delta_1": z_transition,
            "interpretation": "coordinate overlay only; no transition/break claim was preregistered for six sparse points",
        },
    }

    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
