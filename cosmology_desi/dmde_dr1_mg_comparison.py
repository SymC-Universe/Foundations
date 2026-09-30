from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
BASE = ROOT / ".external" / "dr1_fullshape" / "baseline" / "official_chain"
MG = ROOT / ".external" / "dr1_fullshape" / "modified_gravity" / "official_chain"
OUT = ROOT / "results" / "dmde_dr1_mg_comparison.json"
REPORT = ROOT / "results" / "DMDE_DR1_MG_COMPARISON_2026-09-29.md"

def load_set(folder, fields):
    files = [folder / f"chain.{i}.txt" for i in range(1, 5)]
    arrays = []
    for path in files:
        if not path.exists():
            raise RuntimeError(f"missing {path}")
        with path.open("r", encoding="utf-8") as fh:
            header = fh.readline().lstrip("#").split()
        idx = [header.index(x) for x in fields]
        arrays.append(np.loadtxt(path, comments="#", usecols=idx))
    data = np.vstack(arrays)
    return {name: data[:, i] for i, name in enumerate(fields)}

def wq(x, w, qs):
    order = np.argsort(x)
    xs, ws = x[order], w[order]
    cdf = (np.cumsum(ws) - 0.5 * ws) / np.sum(ws)
    return np.interp(qs, cdf, xs)
def summary(x, w):
    mean = float(np.average(x, weights=w))
    sd = float(np.sqrt(np.average((x - mean) ** 2, weights=w)))
    q16, q50, q84 = wq(x, w, [0.16, 0.50, 0.84])
    return {"mean": mean, "sd": sd, "q16": float(q16),
            "median": float(q50), "q84": float(q84)}

base_fields = ["weight", "minuslogpost", "logA", "H0", "ombh2", "omch2",
               "omegam", "omegal", "sigma8", "chi2"]
mg_fields = ["weight", "minuslogpost", "logA", "H0", "ombh2", "omch2",
             "mu0", "Sigma0", "omegam", "omegal", "sigma8", "chi2"]
b = load_set(BASE, base_fields)
m = load_set(MG, mg_fields)
bw, mw = b["weight"], m["weight"]

b_s8 = b["sigma8"] * np.sqrt(b["omegam"] / 0.3)
m_s8 = m["sigma8"] * np.sqrt(m["omegam"] / 0.3)
b_q0 = 0.5 * b["omegam"] - b["omegal"]
m_q0 = 0.5 * m["omegam"] - m["omegal"]
b_zacc = (2 * b["omegal"] / b["omegam"]) ** (1 / 3) - 1
m_zacc = (2 * m["omegal"] / m["omegam"]) ** (1 / 3) - 1

base_vals = {"omegam": b["omegam"], "sigma8": b["sigma8"], "H0": b["H0"],
             "logA": b["logA"], "S8_standard": b_s8,
             "q0": b_q0, "z_acc": b_zacc}
mg_vals = {"omegam": m["omegam"], "sigma8": m["sigma8"], "H0": m["H0"],
           "logA": m["logA"], "S8_standard": m_s8,
           "q0": m_q0, "z_acc": m_zacc}
base_sum = {k: summary(v, bw) for k, v in base_vals.items()}
mg_sum = {k: summary(v, mw) for k, v in mg_vals.items()}
mg_sum["mu0"] = summary(m["mu0"], mw)
mg_sum["Sigma0"] = summary(m["Sigma0"], mw)
mg_sum["mu_today"] = summary(1.0 + m["mu0"], mw)

shifts = {}
for name in base_vals:
    db = mg_sum[name]["median"] - base_sum[name]["median"]
    shifts[name] = {
        "median_difference": float(db),
        "difference_in_baseline_sd": float(db / base_sum[name]["sd"]),
        "sd_ratio_mg_to_baseline": float(mg_sum[name]["sd"] / base_sum[name]["sd"]),
    }

corr_names = ["mu0", "Sigma0", "sigma8", "omegam", "H0", "logA", "S8_standard"]
corr_data = np.column_stack([
    m["mu0"], m["Sigma0"], m["sigma8"], m["omegam"], m["H0"], m["logA"], m_s8
])
means = np.average(corr_data, axis=0, weights=mw)
centered = corr_data - means
cov = (centered * mw[:, None]).T @ centered / np.sum(mw)
sd = np.sqrt(np.diag(cov))
corr = cov / np.outer(sd, sd)
mu_corr = {name: float(corr[0, i]) for i, name in enumerate(corr_names)}

sign_balance = {
    "P_mu0_gt_0": float(np.sum(mw[m["mu0"] > 0]) / np.sum(mw)),
    "P_mu0_lt_0": float(np.sum(mw[m["mu0"] < 0]) / np.sum(mw)),
}
result = {
    "status": "DESI_DR1_modified_gravity_adversary",
    "GR_reference": {"mu0": 0.0, "Sigma0": 0.0},
    "baseline": base_sum,
    "modified_gravity": mg_sum,
    "descriptive_shifts": shifts,
    "mu0_correlations": mu_corr,
    "mu0_sign_balance": sign_balance,
    "sampled_minimum_chi2": {
        "baseline": float(np.min(b["chi2"])),
        "modified_gravity": float(np.min(m["chi2"])),
        "delta_mg_minus_baseline": float(np.min(m["chi2"]) - np.min(b["chi2"])),
        "warning": "Chain-sampled minima are descriptive and are not a calibrated model-selection statistic."
    },
    "Sigma0_guardrail": (
        "DESI FS+BAO alone does not directly constrain Sigma0; its marginal shape is "
        "strongly affected by the hard prior mu0 < 2*Sigma0 + 1. Do not interpret "
        "the one-sided Sigma0 interval as a detection."
    ),
}
OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")

def interval(s):
    return f"{s['median']:.5g} [{s['q16']:.5g}, {s['q84']:.5g}]"

lines = [
    "# DESI DR1 DM/DE Modified-Gravity Adversary",
    "",
    "Flat LambdaCDM background retained; mu0 and Sigma0 are added perturbation-sector parameters.",
    "",
    f"- mu0 = {interval(mg_sum['mu0'])}; GR reference = 0",
    f"- mu(a=1) = {interval(mg_sum['mu_today'])}; GR reference = 1",
    f"- Sigma0 = {interval(mg_sum['Sigma0'])}; DESI-only direct constraint not admitted",
    f"- Omega_m baseline -> MG: {interval(base_sum['omegam'])} -> {interval(mg_sum['omegam'])}",
    f"- sigma8 baseline -> MG: {interval(base_sum['sigma8'])} -> {interval(mg_sum['sigma8'])}",
    f"- S8 baseline -> MG: {interval(base_sum['S8_standard'])} -> {interval(mg_sum['S8_standard'])}",
    f"- H0 baseline -> MG: {interval(base_sum['H0'])} -> {interval(mg_sum['H0'])}",
    "",
    "## Interpretation guardrail",
    "",
    result["Sigma0_guardrail"],
    "",
    "All parameter-shift measures are descriptive because the posteriors are nested and use the same DESI data.",
]
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))