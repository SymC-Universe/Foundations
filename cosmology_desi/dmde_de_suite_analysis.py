from pathlib import Path
import json
import numpy as np
from scipy.stats import chi2 as chi2dist

ROOT = Path(__file__).resolve().parent
BASE = ROOT / ".external" / "dr1_fullshape"
OUT = ROOT / "results" / "dmde_de_suite_analysis.json"
REPORT = ROOT / "results" / "DMDE_DE_SUITE_ANALYSIS_2026-09-29.md"

SUITES = {
    "Pantheon+": BASE / "de_pantheonplus" / "official_chain",
    "Union3": BASE / "de_union3" / "official_chain",
    "DESY5": BASE / "de_desy5" / "official_chain",
}
FIELDS = ["weight", "minuslogpost", "w", "wa", "H0",
          "omegam", "omegal", "sigma8", "chi2"]

def weighted_quantile(x, w, qs):
    order = np.argsort(x)
    xs, ws = x[order], w[order]
    cdf = (np.cumsum(ws) - 0.5 * ws) / np.sum(ws)
    return np.interp(qs, cdf, xs)

def summary(x, wt):
    mean = float(np.average(x, weights=wt))
    sd = float(np.sqrt(np.average((x - mean) ** 2, weights=wt)))
    q16, q50, q84 = weighted_quantile(x, wt, [0.16, 0.50, 0.84])
    return {"mean": mean, "sd": sd, "q16": float(q16),
            "median": float(q50), "q84": float(q84)}
def load_chain_set(folder):
    parts = []
    rows = []
    for i in range(1, 5):
        path = folder / f"chain.{i}.txt"
        if not path.exists():
            raise RuntimeError(f"missing {path}")
        with path.open("r", encoding="utf-8") as fh:
            header = fh.readline().lstrip("#").split()
        idx = [header.index(x) for x in FIELDS]
        arr = np.loadtxt(path, comments="#", usecols=idx)
        parts.append(arr)
        rows.append(int(arr.shape[0]))
    data = np.vstack(parts)
    return {name: data[:, i] for i, name in enumerate(FIELDS)}, rows

def rho_de_ratio(z, w0, wa):
    a = 1.0 / (1.0 + z)
    return a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))

def w_of_z(z, w0, wa):
    return w0 + wa * z / (1.0 + z)

def crossing_z(w0, wa):
    out = np.full_like(w0, np.nan, dtype=float)
    good_wa = np.abs(wa) > 1e-12
    x = np.full_like(w0, np.nan, dtype=float)
    x[good_wa] = (-1.0 - w0[good_wa]) / wa[good_wa]
    good = good_wa & (x > 0.0) & (x < 1.0)
    out[good] = x[good] / (1.0 - x[good])
    return out
results = {}
for label, folder in SUITES.items():
    d, rows = load_chain_set(folder)
    wt, w0, wa = d["weight"], d["w"], d["wa"]
    s8 = d["sigma8"] * np.sqrt(d["omegam"] / 0.3)
    q0 = 0.5 * d["omegam"] + 0.5 * (1.0 + 3.0 * w0) * d["omegal"]

    vals = {
        "w0": w0, "wa": wa, "w0_plus_wa": w0 + wa,
        "omegam": d["omegam"], "sigma8": d["sigma8"],
        "H0": d["H0"], "S8_standard": s8, "q0": q0,
    }
    for z in (0.5, 1.0, 2.0):
        vals[f"w_z{z:g}"] = w_of_z(z, w0, wa)
        vals[f"rhoDE_ratio_z{z:g}"] = rho_de_ratio(z, w0, wa)

    sums = {k: summary(v, wt) for k, v in vals.items()}
    pair = np.column_stack([w0, wa])
    mean = np.average(pair, axis=0, weights=wt)
    cen = pair - mean
    cov = (cen * wt[:, None]).T @ cen / np.sum(wt)
    delta = np.array([-1.0, 0.0]) - mean
    d2 = float(delta @ np.linalg.inv(cov) @ delta)

    cross = crossing_z(w0, wa)
    mask = np.isfinite(cross)
    cross_weight = float(np.sum(wt[mask]) / np.sum(wt))
    cross_summary = summary(cross[mask], wt[mask]) if np.any(mask) else None
    results[label] = {
        "rows_per_chain": rows,
        "summaries": sums,
        "posterior_sign_mass": {
            "P_w0_gt_minus1": float(np.sum(wt[w0 > -1]) / np.sum(wt)),
            "P_wa_lt_0": float(np.sum(wt[wa < 0]) / np.sum(wt)),
            "P_joint_w0_gt_minus1_and_wa_lt_0":
                float(np.sum(wt[(w0 > -1) & (wa < 0)]) / np.sum(wt)),
        },
        "phantom_divide_crossing": {
            "posterior_weight_with_positive_finite_crossing": cross_weight,
            "z_cross_summary_conditional": cross_summary,
        },
        "lcdm_joint_gaussian_diagnostic": {
            "mahalanobis_d2": d2,
            "chi2_2dof_survival": float(chi2dist.sf(d2, 2)),
            "warning": (
                "Covariance-ellipse diagnostic only; not an exact posterior "
                "significance or model-selection statistic."
            ),
        },
        "sampled_minimum_chi2": float(np.min(d["chi2"])),
    }

keys = ["w0", "wa", "omegam", "sigma8", "H0", "S8_standard", "q0"]
cross_sample = {}
for key in keys:
    med = {name: results[name]["summaries"][key]["median"] for name in SUITES}
    sd = {name: results[name]["summaries"][key]["sd"] for name in SUITES}
    cross_sample[key] = {
        "medians": med,
        "max_minus_min_median": float(max(med.values()) - min(med.values())),
        "max_pairwise_shift_over_quadrature_sd": float(max(
            abs(med[a] - med[b]) / np.sqrt(sd[a] ** 2 + sd[b] ** 2)
            for i, a in enumerate(SUITES) for b in list(SUITES)[i + 1:]
        )),
    }
result = {
    "status": "physical_dark_energy_three_SN_sensitivity_suite",
    "model": "flat_CPL_w0waCDM",
    "members": results,
    "cross_sample": cross_sample,
    "shared_direction_check": {
        "all_median_w0_gt_minus1": all(
            results[x]["summaries"]["w0"]["median"] > -1 for x in SUITES
        ),
        "all_median_wa_lt_0": all(
            results[x]["summaries"]["wa"]["median"] < 0 for x in SUITES
        ),
    },
    "guardrails": [
        "No supernova sample is primary and no sample is selected by outcome.",
        "CPL-derived w(z), rho_DE(z), q0 and crossing quantities inherit the assumed w0-wa functional form.",
        "Posterior sign masses are descriptive Bayesian chain summaries, not frequentist p-values.",
        "Exact model comparison requires matched LambdaCDM and w0wa best-fit likelihoods."
    ],
}
OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

def iv(s):
    return f"{s['median']:.5g} [{s['q16']:.5g}, {s['q84']:.5g}]"

lines = ["# DESI DR1 Physical Dark-Energy Sensitivity Suite", ""]
for name in SUITES:
    s = results[name]["summaries"]
    p = results[name]["posterior_sign_mass"]
    lines += [
        f"## {name}", "",
        f"- w0 = {iv(s['w0'])}",
        f"- wa = {iv(s['wa'])}",
        f"- Omega_m = {iv(s['omegam'])}",
        f"- H0 = {iv(s['H0'])} km/s/Mpc",
        f"- S8 = {iv(s['S8_standard'])}",
        f"- P(w0 > -1) = {p['P_w0_gt_minus1']:.4f}",
        f"- P(wa < 0) = {p['P_wa_lt_0']:.4f}",
        "",
    ]
lines += [
    "## Cross-sample check", "",
    f"- All three median w0 values exceed -1: {result['shared_direction_check']['all_median_w0_gt_minus1']}",
    f"- All three median wa values are below 0: {result['shared_direction_check']['all_median_wa_lt_0']}",
    f"- Maximum pairwise normalized median shift in w0: {cross_sample['w0']['max_pairwise_shift_over_quadrature_sd']:.3f}",
    f"- Maximum pairwise normalized median shift in wa: {cross_sample['wa']['max_pairwise_shift_over_quadrature_sd']:.3f}",
    "",
    "## Guardrails", "",
]
lines += [f"- {x}" for x in result["guardrails"]]
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))