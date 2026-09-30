from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parent
EXT = ROOT / ".external" / "dr1_fullshape"
OUT = ROOT / "results" / "dmde_neutrino_adversary_analysis.json"
REPORT = ROOT / "results" / "DMDE_NEUTRINO_ADVERSARY_2026-09-29.md"

def wq(x, wt, qs):
    order = np.argsort(x)
    xs, ws = x[order], wt[order]
    cdf = (np.cumsum(ws) - 0.5 * ws) / np.sum(ws)
    return np.interp(qs, cdf, xs)

def summary(x, wt):
    mean = float(np.average(x, weights=wt))
    sd = float(np.sqrt(np.average((x - mean) ** 2, weights=wt)))
    q16, q50, q84, q95 = wq(x, wt, [0.16, 0.50, 0.84, 0.95])
    return {"mean": mean, "sd": sd, "q16": float(q16), "median": float(q50),
            "q84": float(q84), "q95": float(q95)}

def load(folder, fields):
    parts = []
    rows = []
    for i in range(1, 5):
        path = folder / "official_chain" / f"chain.{i}.txt"
        with path.open("r", encoding="utf-8") as fh:
            header = fh.readline().lstrip("#").split()
        idx = [header.index(x) for x in fields]
        arr = np.loadtxt(path, comments="#", usecols=idx)
        parts.append(arr)
        rows.append(int(arr.shape[0]))
    data = np.vstack(parts)
    return {name: data[:, j] for j, name in enumerate(fields)}, rows
def corr(x, y, wt):
    mx = np.average(x, weights=wt)
    my = np.average(y, weights=wt)
    dx, dy = x - mx, y - my
    cov = np.average(dx * dy, weights=wt)
    sx = np.sqrt(np.average(dx * dx, weights=wt))
    sy = np.sqrt(np.average(dy * dy, weights=wt))
    return float(cov / (sx * sy))

def standard_s8(d):
    return d["sigma8"] * np.sqrt(d["omegam"] / 0.3)

base_fields = ["weight", "H0", "omegam", "sigma8", "logA", "chi2"]
free_fields = ["weight", "mnu", "H0", "omegam", "sigma8", "logA", "chi2"]

fixed, fixed_rows = load(EXT / "cmb_fixed_mnu", base_fields)
free, free_rows = load(EXT / "cmb_free_mnu", free_fields)
fw, nw = fixed["weight"], free["weight"]
fixed_vals = {k: fixed[k] for k in ("H0", "omegam", "sigma8", "logA")}
free_vals = {k: free[k] for k in ("H0", "omegam", "sigma8", "logA")}
fixed_vals["S8_standard"] = standard_s8(fixed)
free_vals["S8_standard"] = standard_s8(free)
fixed_sum = {k: summary(v, fw) for k, v in fixed_vals.items()}
free_sum = {k: summary(v, nw) for k, v in free_vals.items()}
mnu_sum = summary(free["mnu"], nw)

cmb_shifts = {}
for k in fixed_vals:
    delta = free_sum[k]["median"] - fixed_sum[k]["median"]
    cmb_shifts[k] = {
        "median_difference": float(delta),
        "difference_in_fixed_sd": float(delta / fixed_sum[k]["sd"]),
        "sd_ratio_free_to_fixed": float(free_sum[k]["sd"] / fixed_sum[k]["sd"]),
    }
cmb = {
    "fixed_mnu_eV": 0.06,
    "fixed_rows": fixed_rows,
    "free_rows": free_rows,
    "mnu_free_posterior": mnu_sum,
    "P_mnu_gt_0p06": float(np.sum(nw[free["mnu"] > 0.06]) / np.sum(nw)),
    "fixed_summary": fixed_sum,
    "free_summary": free_sum,
    "shifts": cmb_shifts,
    "mnu_correlations": {
        k: corr(free["mnu"], free_vals[k], nw) for k in free_vals
    },
}
del fixed, free, fixed_vals, free_vals

DE = {
    "Pantheon+": ("de_pantheonplus", "de_mnu_pantheonplus"),
    "Union3": ("de_union3", "de_mnu_union3"),
    "DESY5": ("de_desy5", "de_mnu_desy5"),
}
de_fields_fixed = ["weight", "w", "wa", "H0", "omegam", "sigma8"]
de_fields_free = ["weight", "mnu", "w", "wa", "H0", "omegam", "sigma8"]
de_results = {}
for label, (fixed_key, free_key) in DE.items():
    d0, rows0 = load(EXT / fixed_key, de_fields_fixed)
    d1, rows1 = load(EXT / free_key, de_fields_free)
    w0, w1 = d0["weight"], d1["weight"]
    d0["S8_standard"] = standard_s8(d0)
    d1["S8_standard"] = standard_s8(d1)
    keys = ["w", "wa", "H0", "omegam", "sigma8", "S8_standard"]
    s0 = {k: summary(d0[k], w0) for k in keys}
    s1 = {k: summary(d1[k], w1) for k in keys}
    shifts = {}
    for k in keys:
        delta = s1[k]["median"] - s0[k]["median"]
        shifts[k] = {
            "median_difference": float(delta),
            "difference_in_fixed_sd": float(delta / s0[k]["sd"]),
            "sd_ratio_free_to_fixed": float(s1[k]["sd"] / s0[k]["sd"]),
        }
    msum = summary(d1["mnu"], w1)
    de_results[label] = {
        "fixed_rows": rows0,
        "free_rows": rows1,
        "mnu_free_posterior": msum,
        "fixed_summary": s0,
        "free_summary": s1,
        "shifts": shifts,
        "mnu_correlations": {
            k: corr(d1["mnu"], d1[k], w1) for k in keys
        },
        "free_mnu_sign_mass": {
            "P_w0_gt_minus1": float(np.sum(w1[d1["w"] > -1]) / np.sum(w1)),
            "P_wa_lt_0": float(np.sum(w1[d1["wa"] < 0]) / np.sum(w1)),
            "P_joint": float(np.sum(w1[(d1["w"] > -1) & (d1["wa"] < 0)]) / np.sum(w1)),
        },
    }
    del d0, d1

result = {
    "status": "neutrino_mass_adversarial_suite",
    "cmb_fixed_vs_free_mnu": cmb,
    "w0wa_free_mnu_robustness": de_results,
    "guardrails": [
        "The CMB neutrino gate is DESI FS+BAO+CMB, not a DESI-only neutrino constraint.",
        "Free-mnu chains use the DESI release prior mnu > 0 and three degenerate mass eigenstates.",
        "The w0-wa robustness test compares each free-mnu chain only to the same SN sample with fixed mnu.",
        "Posterior mass above thresholds is descriptive and is not a frequentist significance."
    ],
}
OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
def iv(s):
    return f"{s['median']:.5g} [{s['q16']:.5g}, {s['q84']:.5g}]"

lines = [
    "# DESI DR1 Neutrino-Mass Adversarial Suite", "",
    "## DESI FS+BAO+CMB: fixed versus free neutrino mass", "",
    f"- free sum mnu 95% upper = {mnu_sum['q95']:.5g} eV",
    f"- free sum mnu median = {mnu_sum['median']:.5g} eV",
    f"- P(sum mnu > 0.06 eV) = {cmb['P_mnu_gt_0p06']:.5f}",
]
for k in ("omegam", "sigma8", "H0", "S8_standard"):
    lines.append(
        f"- {k}: fixed {iv(fixed_sum[k])} -> free {iv(free_sum[k])}; "
        f"shift {cmb_shifts[k]['difference_in_fixed_sd']:.3f} fixed-sigma"
    )

for label, d in de_results.items():
    lines += ["", f"## {label}: w0wa fixed-mnu versus free-mnu", ""]
    lines += [
        f"- sum mnu 95% upper = {d['mnu_free_posterior']['q95']:.5g} eV",
        f"- w0: {iv(d['fixed_summary']['w'])} -> {iv(d['free_summary']['w'])}; "
        f"shift {d['shifts']['w']['difference_in_fixed_sd']:.3f} fixed-sigma",
        f"- wa: {iv(d['fixed_summary']['wa'])} -> {iv(d['free_summary']['wa'])}; "
        f"shift {d['shifts']['wa']['difference_in_fixed_sd']:.3f} fixed-sigma",
        f"- free-mnu P(w0>-1, wa<0) = {d['free_mnu_sign_mass']['P_joint']:.5f}",
    ]

lines += ["", "## Guardrails", ""] + [f"- {x}" for x in result["guardrails"]]
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))