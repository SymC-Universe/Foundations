#!/usr/bin/env python3
"""DESI DR2 scalar Stability Architecture gate.

Downloads official DESI DR2 Cobaya posterior chains, preserves provenance,
and derives q(z), chi_delta(z), transition roots, and Delta z.

No capital-Chi or SI inference is performed here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import numpy as np
import pandas as pd
import requests
from scipy.optimize import brentq

ROOT = "https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/cobaya/"
MODELS = {
    "base": {"w0": -1.0, "wa": 0.0},
    "base_w": {"wa": 0.0},
    "base_w_wa": {},
}
DATASET = "desi-bao-all"
ZMIN, ZMAX = 0.0, 5.0
GRID_N = 2001

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        for k, v in attrs:
            if k.lower() == "href" and v:
                self.hrefs.append(v)

@dataclass
class Roots:
    all_roots: list[float]
    primary: float | None

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def discover_files(url: str) -> list[str]:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    p = LinkParser()
    p.feed(r.text)
    out = []
    for href in p.hrefs:
        name = href.split("?")[0].rstrip("/").split("/")[-1]
        if not name or href.startswith("?") or href.startswith("/"):
            continue
        if name.endswith((".txt", ".yaml", ".yml", ".paramnames", ".properties.ini")):
            out.append(urljoin(url, href))
    return sorted(set(out))

def download_model(model: str, outdir: Path) -> tuple[list[Path], list[dict]]:
    url = f"{ROOT}{model}/{DATASET}/"
    files = discover_files(url)
    chain_urls = [u for u in files if re.search(r"(?:^|[._])\d+\.txt$", u.split("/")[-1]) or u.endswith(".txt")]
    if not chain_urls:
        raise RuntimeError(f"No .txt chain files discovered at {url}")
    model_dir = outdir / model
    model_dir.mkdir(parents=True, exist_ok=True)
    local, provenance = [], []
    for u in files:
        name = u.split("/")[-1]
        p = model_dir / name
        r = requests.get(u, timeout=120)
        r.raise_for_status()
        p.write_bytes(r.content)
        provenance.append({
            "model": model,
            "dataset": DATASET,
            "url": u,
            "file": str(p),
            "bytes": p.stat().st_size,
            "sha256": sha256(p),
        })
        if u in chain_urls:
            local.append(p)
    return local, provenance

def read_chain_file(path: Path) -> pd.DataFrame:
    # Cobaya chain text files carry a commented whitespace-delimited header.
    header = None
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("#"):
                candidate = line[1:].strip().split()
                if len(candidate) >= 2:
                    header = candidate
            elif line.strip():
                break
    if not header:
        raise RuntimeError(f"Could not identify Cobaya header in {path}")
    df = pd.read_csv(path, sep=r"\s+", comment="#", names=header, engine="python")
    df["_source_file"] = path.name
    return df

def concat_chains(paths: Iterable[Path]) -> pd.DataFrame:
    frames = [read_chain_file(p) for p in paths]
    if not frames:
        raise RuntimeError("No chain frames parsed")
    return pd.concat(frames, ignore_index=True)

def first_column(df: pd.DataFrame, aliases: list[str]) -> str | None:
    lower = {c.lower(): c for c in df.columns}
    for a in aliases:
        if a.lower() in lower:
            return lower[a.lower()]
    return None

def weights(df: pd.DataFrame) -> np.ndarray:
    c = first_column(df, ["weight", "weights"])
    if c is None:
        return np.ones(len(df), dtype=float)
    w = np.asarray(df[c], dtype=float)
    if np.any(~np.isfinite(w)) or np.any(w < 0) or w.sum() <= 0:
        raise RuntimeError("Invalid posterior weights")
    return w

def weighted_quantile(x: np.ndarray, w: np.ndarray, qs=(0.16, 0.5, 0.84)):
    m = np.isfinite(x) & np.isfinite(w) & (w >= 0)
    x, w = x[m], w[m]
    if x.size == 0 or w.sum() <= 0:
        return [None for _ in qs]
    order = np.argsort(x)
    x, w = x[order], w[order]
    c = np.cumsum(w) - 0.5 * w
    c /= w.sum()
    return [float(np.interp(q, c, x)) for q in qs]

def de_factor(a: np.ndarray | float, w0: float, wa: float):
    a = np.asarray(a, dtype=float)
    return a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))

def w_of_a(a: np.ndarray | float, w0: float, wa: float):
    return w0 + wa * (1.0 - np.asarray(a, dtype=float))

def e2(a, om0: float, w0: float, wa: float):
    ode0 = 1.0 - om0
    return om0 * np.asarray(a) ** -3 + ode0 * de_factor(a, w0, wa)

def omega_m_a(a, om0: float, w0: float, wa: float):
    matter = om0 * np.asarray(a) ** -3
    return matter / e2(a, om0, w0, wa)

def chi_delta_z(z, om0: float, w0: float, wa: float):
    a = 1.0 / (1.0 + np.asarray(z))
    oma = omega_m_a(a, om0, w0, wa)
    return np.sqrt(2.0 / (3.0 * oma))

def q_z(z, om0: float, w0: float, wa: float):
    a = 1.0 / (1.0 + np.asarray(z))
    oma = omega_m_a(a, om0, w0, wa)
    odea = 1.0 - oma
    return 0.5 * (oma + odea * (1.0 + 3.0 * w_of_a(a, w0, wa)))

def roots_on_grid(fn) -> Roots:
    z = np.linspace(ZMIN, ZMAX, GRID_N)
    y = np.asarray(fn(z), dtype=float)
    roots: list[float] = []
    for i in range(len(z) - 1):
        if not np.isfinite(y[i]) or not np.isfinite(y[i + 1]):
            continue
        if y[i] == 0.0:
            roots.append(float(z[i]))
        elif y[i] * y[i + 1] < 0:
            roots.append(float(brentq(fn, float(z[i]), float(z[i + 1]), xtol=1e-12, rtol=1e-12)))
    if np.isfinite(y[-1]) and y[-1] == 0.0:
        roots.append(float(z[-1]))
    # Merge numerical duplicates.
    roots = sorted(roots)
    merged = []
    for r in roots:
        if not merged or abs(r - merged[-1]) > 1e-7:
            merged.append(r)
    return Roots(merged, merged[0] if merged else None)

def extract_params(df: pd.DataFrame, model: str):
    om_col = first_column(df, ["omegam", "omega_m", "Omega_m", "Omega_m0"])
    if om_col is None:
        raise RuntimeError(f"{model}: cannot find Omega_m column; columns={list(df.columns)}")
    om = np.asarray(df[om_col], dtype=float)
    defaults = MODELS[model]
    if "w0" in defaults:
        w0 = np.full(len(df), defaults["w0"])
    else:
        wc = first_column(df, ["w", "w0", "w_0", "w0p", "w0_de"])
        if wc is None:
            raise RuntimeError(f"{model}: cannot find w0/w column")
        w0 = np.asarray(df[wc], dtype=float)
    if "wa" in defaults:
        wa = np.full(len(df), defaults["wa"])
    else:
        wac = first_column(df, ["wa", "w_a", "wa_de"])
        if wac is None:
            raise RuntimeError(f"{model}: cannot find wa column")
        wa = np.asarray(df[wac], dtype=float)
    return om, w0, wa, om_col

def analyse_model(model: str, df: pd.DataFrame, outdir: Path):
    om, w0, wa, om_col = extract_params(df, model)
    wgt = weights(df)
    rows = []
    for i in range(len(df)):
        if not (0.0 < om[i] < 1.0 and np.isfinite(w0[i]) and np.isfinite(wa[i])):
            rows.append((i, math.nan, math.nan, math.nan, -1, -1, math.nan, math.nan))
            continue
        rq = roots_on_grid(lambda z: q_z(z, om[i], w0[i], wa[i]))
        rc = roots_on_grid(lambda z: chi_delta_z(z, om[i], w0[i], wa[i]) - 1.0)
        dz = (rq.primary - rc.primary) if rq.primary is not None and rc.primary is not None else math.nan
        rows.append((i,
                     rq.primary if rq.primary is not None else math.nan,
                     rc.primary if rc.primary is not None else math.nan,
                     dz, len(rq.all_roots), len(rc.all_roots),
                     float(q_z(0.0, om[i], w0[i], wa[i])),
                     float(chi_delta_z(0.0, om[i], w0[i], wa[i]))))
    arr = pd.DataFrame(rows, columns=["row", "z_q0", "z_chi1", "delta_z", "n_q_roots", "n_chi_roots", "q0", "chi_delta0"])
    arr["weight"] = wgt
    arr.to_csv(outdir / f"{model}_derived.csv.gz", index=False, compression="gzip")

    valid = np.isfinite(arr["delta_z"].to_numpy())
    def wf(mask):
        return float(wgt[mask].sum() / wgt.sum())
    summary = {
        "model": model,
        "dataset": DATASET,
        "samples": int(len(df)),
        "omega_m_column": om_col,
        "weight_sum": float(wgt.sum()),
        "valid_delta_z_weight_fraction": wf(valid),
        "q_root_counts_weight_fraction": {str(n): wf(arr["n_q_roots"].to_numpy() == n) for n in sorted(set(arr["n_q_roots"]))},
        "chi_root_counts_weight_fraction": {str(n): wf(arr["n_chi_roots"].to_numpy() == n) for n in sorted(set(arr["n_chi_roots"]))},
    }
    for name in ["z_q0", "z_chi1", "delta_z", "q0", "chi_delta0"]:
        vals = arr[name].to_numpy(float)
        q16, q50, q84 = weighted_quantile(vals, wgt)
        summary[name] = {"q16": q16, "median": q50, "q84": q84}

    if model == "base":
        good = valid
        if good.any():
            max_abs = float(np.nanmax(np.abs(arr.loc[good, "delta_z"])))
            summary["lcdm_identity_max_abs_delta_z"] = max_abs
            summary["lcdm_identity_pass"] = bool(max_abs < 1e-8)
        else:
            summary["lcdm_identity_max_abs_delta_z"] = None
            summary["lcdm_identity_pass"] = False
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="cosmology_desi/results")
    ap.add_argument("--data", default="cosmology_desi/data")
    ap.add_argument("--models", nargs="+", default=list(MODELS))
    args = ap.parse_args()
    out = Path(args.out)
    data = Path(args.data)
    out.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)

    provenance, summaries = [], []
    for model in args.models:
        if model not in MODELS:
            raise SystemExit(f"Unknown model: {model}")
        chains, prov = download_model(model, data)
        provenance.extend(prov)
        df = concat_chains(chains)
        summaries.append(analyse_model(model, df, out))

    (out / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    base = next((x for x in summaries if x["model"] == "base"), None)
    if base and not base.get("lcdm_identity_pass", False):
        print(json.dumps(base, indent=2))
        raise SystemExit("FAIL: LambdaCDM identity gate")
    print(json.dumps(summaries, indent=2))

if __name__ == "__main__":
    main()
