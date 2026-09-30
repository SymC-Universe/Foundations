from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
CHAIN_DIR = ROOT / ".external" / "dr1_fullshape" / "baseline" / "official_chain"
OUT_JSON = ROOT / "results" / "dmde_dr1_baseline_audit.json"
OUT_MD = ROOT / "results" / "DMDE_DR1_BASELINE_AUDIT_2026-09-29.md"
CHAIN_FILES = [CHAIN_DIR / f"chain.{i}.txt" for i in range(1, 5)]
FIELDS = ["weight", "minuslogpost", "H0", "ombh2", "omch2",
          "omegam", "omegal", "sigma8", "chi2"]

def header_and_indices(path):
    with path.open("r", encoding="utf-8") as fh:
        header = fh.readline().lstrip("#").split()
    missing = [x for x in FIELDS if x not in header]
    if missing:
        raise RuntimeError(f"{path.name}: missing columns {missing}")
    return header, [header.index(x) for x in FIELDS]

def weighted_quantile(x, w, q):
    order = np.argsort(x)
    xs, ws = x[order], w[order]
    cdf = np.cumsum(ws) - 0.5 * ws
    cdf = cdf / np.sum(ws)
    return np.interp(q, cdf, xs)
def summary(x, w):
    mean = float(np.average(x, weights=w))
    var = float(np.average((x - mean) ** 2, weights=w))
    q16, q50, q84 = weighted_quantile(x, w, [0.16, 0.50, 0.84])
    return {"mean": mean, "sd": var ** 0.5, "q16": float(q16),
            "median": float(q50), "q84": float(q84)}

arrays = []
chain_rows = []
for path in CHAIN_FILES:
    header, idx = header_and_indices(path)
    arr = np.loadtxt(path, comments="#", usecols=idx)
    arrays.append(arr)
    chain_rows.append({"file": path.name, "rows": int(arr.shape[0]),
                       "sum_weight": float(np.sum(arr[:, 0]))})

data = np.vstack(arrays)
cols = {name: data[:, i] for i, name in enumerate(FIELDS)}
w = cols["weight"]
h = cols["H0"] / 100.0
omega_b = cols["ombh2"] / h**2
omega_c = cols["omch2"] / h**2
omega_nu = cols["omegam"] - omega_b - omega_c
omega_nonbaryonic = cols["omegam"] - omega_b
s8 = cols["sigma8"] * np.sqrt(cols["omegam"] / 0.3)
q0 = 0.5 * cols["omegam"] - cols["omegal"]
z_de_eq = (cols["omegal"] / cols["omegam"]) ** (1.0 / 3.0) - 1.0
z_acc = (2.0 * cols["omegal"] / cols["omegam"]) ** (1.0 / 3.0) - 1.0
derived = {
    "Omega_b": omega_b,
    "Omega_cdm": omega_c,
    "Omega_nu_inferred": omega_nu,
    "Omega_nonbaryonic_matter": omega_nonbaryonic,
    "dark_matter_fraction_of_matter": omega_nonbaryonic / cols["omegam"],
    "S8_standard": s8,
    "q0_flat_LCDM": q0,
    "z_matter_DE_equality": z_de_eq,
    "z_acceleration_transition": z_acc,
    "rho_DE_over_rho_m_today": cols["omegal"] / cols["omegam"],
}
raw_keep = ["omegam", "omegal", "sigma8", "H0", "ombh2", "omch2"]
summaries = {k: summary(cols[k], w) for k in raw_keep}
summaries.update({k: summary(v, w) for k, v in derived.items()})

core_names = ["omegam", "sigma8", "H0", "S8_standard"]
core = np.column_stack([cols["omegam"], cols["sigma8"], cols["H0"], s8])
mean = np.average(core, axis=0, weights=w)
centered = core - mean
cov = (centered * w[:, None]).T @ centered / np.sum(w)
sd = np.sqrt(np.diag(cov))
corr = cov / np.outer(sd, sd)

chain_consistency = {}
for j, name in enumerate(["omegam", "sigma8", "H0"]):
    pooled_sd = summaries[name]["sd"]
    means = [float(np.average(a[:, FIELDS.index(name)], weights=a[:, 0]))
             for a in arrays]
    chain_consistency[name] = {
        "chain_means": means,
        "range_in_pooled_sd": float((max(means) - min(means)) / pooled_sd)
    }
best_i = int(np.argmin(cols["minuslogpost"]))
best = {k: float(cols[k][best_i]) for k in raw_keep + ["minuslogpost", "chi2"]}
result = {
    "status": "baseline_dark_sector_reference_only",
    "source": "DESI DR1 full-shape+BAO official posterior chains",
    "chain_files": chain_rows,
    "total_rows": int(data.shape[0]),
    "total_weight": float(np.sum(w)),
    "summaries": summaries,
    "core_correlation_order": core_names,
    "core_correlation_matrix": corr.tolist(),
    "chain_consistency": chain_consistency,
    "best_sample": best,
    "interpretation_guardrail": (
        "Derived quantities are native flat-LCDM re-expressions of the released "
        "posterior and do not constitute evidence for interacting DM, dynamical DE, "
        "modified gravity, or any cross-project stability construct."
    ),
}
OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")

def pm(s):
    return f"{s['median']:.6g} [{s['q16']:.6g}, {s['q84']:.6g}]"

lines = [
    "# DESI DR1 DM/DE Baseline Posterior Audit",
    "",
    "Status: qualified flat-LambdaCDM dark-sector reference posterior.",
    "",
    "## Key posterior summaries",
    "",
    f"- Omega_m = {pm(summaries['omegam'])}",
    f"- Omega_Lambda = {pm(summaries['omegal'])}",
    f"- sigma8 = {pm(summaries['sigma8'])}",
    f"- H0 = {pm(summaries['H0'])} km/s/Mpc",
    f"- S8 = {pm(summaries['S8_standard'])}",
    f"- Omega_cdm = {pm(summaries['Omega_cdm'])}",
    f"- Omega_nu (inferred residual) = {pm(summaries['Omega_nu_inferred'])}",
    f"- non-baryonic matter fraction of matter = {pm(summaries['dark_matter_fraction_of_matter'])}",
    f"- rho_DE/rho_m today = {pm(summaries['rho_DE_over_rho_m_today'])}",
    f"- z(rho_m=rho_DE) = {pm(summaries['z_matter_DE_equality'])}",
    f"- z(q=0) = {pm(summaries['z_acceleration_transition'])}",
    "",
    "## Guardrail",
    "",
    result["interpretation_guardrail"],
]
OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))