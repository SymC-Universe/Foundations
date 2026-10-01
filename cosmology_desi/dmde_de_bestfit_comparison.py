from pathlib import Path
import hashlib
import json
import math
from urllib.request import Request, urlopen
import numpy as np
from scipy.stats import chi2 as chi2dist, norm

ROOT = Path(__file__).resolve().parent
EXT = ROOT / ".external" / "dr1_fullshape"
MANIFEST = EXT / "dr1_v1.0.sha256sum"
OUT = ROOT / "results" / "dmde_de_bestfit_comparison.json"
REPORT = ROOT / "results" / "DMDE_DE_BESTFIT_COMPARISON_2026-09-29.md"
BASE_URL = "https://data.desi.lbl.gov/public/dr1/vac/dr1/full-shape-cosmo-params/v1.0"

DATASETS = {
    "Pantheon+": "pantheonplus",
    "Union3": "union3",
    "DESY5": "desy5sn",
}
TAIL = (
    "_planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_"
    "planck2018-highl-plik-TTTEEE_planck-act-dr6-lensing"
)

def dataset_dir(sn):
    return f"desi-reptvelocileptors-fs-bao-all_{sn}{TAIL}"

def manifest_map():
    out = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        out[rel] = digest
    return out
def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def download_verified(rel, expected_sha, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    req = Request(f"{BASE_URL}/{rel}", headers={"User-Agent": "SymC-DMDE/1.0"})
    with urlopen(req, timeout=60) as r, target.open("wb") as f:
        f.write(r.read())
    got = sha256(target)
    if got != expected_sha:
        raise RuntimeError(f"hash mismatch {rel}: {got} != {expected_sha}")
    return {"relative_path": rel, "sha256": got, "bytes": target.stat().st_size}

def parse_bestfit(path):
    with path.open("r", encoding="utf-8") as f:
        header = f.readline().lstrip("#").split()
        vals = f.readline().split()
    if len(header) != len(vals):
        raise RuntimeError(f"header/value mismatch: {path}")
    d = {k: float(v) for k, v in zip(header, vals)}
    keep = {
        k: d[k] for k in (
            "minuslogpost", "H0", "omegam", "sigma8", "chi2",
            "chi2__CMB", "chi2__SN"
        ) if k in d
    }
    for key in ("w", "wa"):
        if key in d:
            keep[key] = d[key]
    fs_cols = [k for k in d if "fs_bao_likelihoods.desi_fs_bao_all" in k]
    if fs_cols:
        keep["chi2__DESI_FS_BAO"] = d[fs_cols[0]]
    return keep
manifest = manifest_map()
result = {
    "status": "matched_released_iminuit_minimum_comparison",
    "comparison": "flat_LambdaCDM_vs_flat_CPL_w0waCDM",
    "extra_parameters": 2,
    "members": {},
    "guardrails": [
        "Each comparison uses the same DESI FS+BAO+CMB+SN dataset combination.",
        "Delta chi-square uses released iminuit posterior-maximization products, not minima sampled from MCMC chains.",
        "The Wilks diagnostic is asymptotic and descriptive; DESI's published inference remains the authoritative significance statement.",
    ],
}

for label, sn in DATASETS.items():
    rows = {}
    receipts = {}
    for model in ("base", "base_w_wa"):
        rel = f"iminuit/{model}/{dataset_dir(sn)}/bestfit.minimum.txt"
        if rel not in manifest:
            raise RuntimeError(f"manifest path missing: {rel}")
        target = EXT / "de_bestfits" / label.replace("+", "plus") / model / "bestfit.minimum.txt"
        receipts[model] = download_verified(rel, manifest[rel], target)
        rows[model] = parse_bestfit(target)

    delta = rows["base_w_wa"]["chi2"] - rows["base"]["chi2"]
    improvement = -delta
    p_wilks = float(chi2dist.sf(improvement, 2)) if improvement >= 0 else 1.0
    sigma_two_sided = float(norm.isf(p_wilks / 2.0)) if p_wilks > 0 else math.inf
    result["members"][label] = {
        "receipts": receipts,
        "LambdaCDM": rows["base"],
        "w0waCDM": rows["base_w_wa"],
        "delta_chi2_w0wa_minus_LambdaCDM": float(delta),
        "chi2_improvement": float(improvement),
        "asymptotic_Wilks_2dof": {
            "p_value": p_wilks,
            "two_sided_normal_equivalent_sigma": sigma_two_sided,
        },
        "component_delta_chi2": {
            k: float(rows["base_w_wa"][k] - rows["base"][k])
            for k in ("chi2__DESI_FS_BAO", "chi2__CMB", "chi2__SN")
            if k in rows["base"] and k in rows["base_w_wa"]
        }
    }

OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
lines = [
    "# DESI DR1 Matched Dark-Energy Best-Fit Comparison", "",
    "Released iminuit minima; flat LambdaCDM versus flat CPL w0waCDM using identical data in each pair.", ""
]
for label, m in result["members"].items():
    w = m["w0waCDM"]
    lines += [
        f"## {label}", "",
        f"- Delta chi2 (w0wa - LambdaCDM) = {m['delta_chi2_w0wa_minus_LambdaCDM']:.4f}",
        f"- chi2 improvement = {m['chi2_improvement']:.4f} for 2 additional parameters",
        f"- w0 best fit = {w.get('w', float('nan')):.5f}",
        f"- wa best fit = {w.get('wa', float('nan')):.5f}",
        f"- asymptotic 2-dof Wilks p = {m['asymptotic_Wilks_2dof']['p_value']:.6g}",
        f"- two-sided normal-equivalent diagnostic = {m['asymptotic_Wilks_2dof']['two_sided_normal_equivalent_sigma']:.3f} sigma",
        f"- component delta chi2 = {m['component_delta_chi2']}", "",
    ]
lines += ["## Guardrails", ""] + [f"- {x}" for x in result["guardrails"]]
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))