from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "D02F_FLOOD_SHAB_COMPLETENESS_PROBE_v0.1.json"
BASE = "https://zenodo.org/records/20443860/files/"
FILES = {
    "main": ("CableStayedBridge_SHM_features_2026-03-27_2026-04-10.csv", "34ff627723494abe2b224db433d6fa76"),
    "dictionary": ("CableStayedBridge_SHM_features_data_dictionary.csv", "6d63c4c91e1e50d3b8b8dc0be8f6b762"),
    "mapping": ("CableStayedBridge_sensor_channel_mapping.csv", "647eca1601a2b9f3549281c5a67cd50d"),
    "readme": ("README_CableStayedBridge_SHM_event_dataset.txt", "620482add51c782e849a8641ed1fb4c6"),
}
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(name: str, expected_md5: str) -> bytes:
    r = requests.get(BASE + name + "?download=1", headers=HEADERS, timeout=180)
    r.raise_for_status()
    data = r.content
    actual = md5(data)
    if actual != expected_md5:
        raise RuntimeError(f"MD5 mismatch for {name}: {actual}")
    return data


def to_float(x: str):
    x = (x or "").strip()
    if not x or x.lower() in {"nan", "na", "none"}:
        return None
    try:
        y = float(x)
    except ValueError:
        return None
    return y if math.isfinite(y) else None


def percentile(values, q):
    vals = sorted(values)
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0]
    pos = (len(vals) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return vals[lo]
    frac = pos - lo
    return vals[lo] * (1 - frac) + vals[hi] * frac


def mode_groups(headers):
    groups = defaultdict(set)
    # Accept source naming such as freq_mode_01_Hz, damping_mode_01,
    # modal_complexity_factor_mode_01, and phi_mode_01_*.
    pattern = re.compile(r"(?:^|_)mode_?(\\d{1,2})(?:_|$)", re.I)
    for h in headers:
        low = h.lower()
        if not any(k in low for k in ("freq", "damp", "mcf", "complexity", "phi_", "shape", "real", "imag")):
            continue
        m = pattern.search(h)
        if m:
            key = f"mode_{int(m.group(1)):02d}"
            groups[key].add(h)
    return {k: sorted(v) for k, v in sorted(groups.items())}


def classify_columns(headers):
    return {
        "timestamp_candidates": [h for h in headers if any(k in h.lower() for k in ("time", "date"))],
        "water_candidates": [h for h in headers if "water" in h.lower() or "gauge" in h.lower() or "hydro" in h.lower()],
        "damping_columns": [h for h in headers if "damp" in h.lower()],
        "frequency_columns": [h for h in headers if "freq" in h.lower()],
        "mcf_columns": [h for h in headers if "mcf" in h.lower() or "complexity" in h.lower()],
        "mode_shape_columns": [h for h in headers if any(k in h.lower() for k in ("mode_shape", "shape_real", "shape_imag", "real", "imag")) and "mode" in h.lower()],
    }


def main():
    fetched = {}
    for role,(name,checksum) in FILES.items():
        data = fetch(name, checksum)
        fetched[role] = {
            "filename": name,
            "md5": checksum,
            "sha256": sha256(data),
            "bytes": data,
        }

    text = fetched["main"]["bytes"].decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    headers = reader.fieldnames or []
    rows = list(reader)
    classes = classify_columns(headers)

    if not classes["water_candidates"]:
        raise RuntimeError("No water/gauge/hydrometric candidate column found")
    water_col = classes["water_candidates"][0]

    water_values = []
    for r in rows:
        v = to_float(r.get(water_col, ""))
        if v is not None:
            water_values.append(v)

    if len(water_values) < 30:
        raise RuntimeError("Too few non-missing water-level observations for D02F candidate probe")

    q25 = percentile(water_values, 0.25)
    q50 = percentile(water_values, 0.50)
    q75 = percentile(water_values, 0.75)
    wmin = min(water_values)
    wmax = max(water_values)

    # Control-only quartile bins. These are a completeness probe, not the final D02F intervention freeze.
    def water_bin(v):
        if v is None:
            return None
        if v <= q25:
            return "Q1_LOW"
        if v <= q50:
            return "Q2"
        if v <= q75:
            return "Q3"
        return "Q4_HIGH"

    groups = mode_groups(headers)

    per_bin_rows = defaultdict(int)
    per_bin_complete = defaultdict(lambda: defaultdict(int))
    per_bin_scalar = defaultdict(lambda: defaultdict(int))
    per_bin_org = defaultdict(lambda: defaultdict(int))

    # Infer mode-level fields only from names. No scientific values are emitted.
    for r in rows:
        w = to_float(r.get(water_col, ""))
        b = water_bin(w)
        if b is None:
            continue
        per_bin_rows[b] += 1
        for mode, cols in groups.items():
            damping = [c for c in cols if "damp" in c.lower()]
            freq = [c for c in cols if "freq" in c.lower()]
            org = [c for c in cols if any(k in c.lower() for k in ("mcf", "real", "imag", "shape"))]
            scalar_ok = bool(damping and freq) and all(to_float(r.get(c, "")) is not None for c in damping + freq)
            org_ok = bool(org) and all(to_float(r.get(c, "")) is not None for c in org)
            if scalar_ok:
                per_bin_scalar[b][mode] += 1
            if org_ok:
                per_bin_org[b][mode] += 1
            if scalar_ok and org_ok:
                per_bin_complete[b][mode] += 1

    result = {
        "schema": "d02f-flood-shab-completeness-probe-v0.1",
        "status": "METADATA_AND_MISSINGNESS_ONLY_NO_DAMPING_OR_MODE_SHAPE_VALUES_EMITTED",
        "source_doi": "10.5281/zenodo.20443860",
        "sources": {
            role: {k:v for k,v in meta.items() if k != "bytes"}
            for role,meta in fetched.items()
        },
        "row_count": len(rows),
        "headers": headers,
        "column_classes": classes,
        "inferred_mode_groups": groups,
        "water_control": {
            "column": water_col,
            "nonmissing_count": len(water_values),
            "missing_count": len(rows)-len(water_values),
            "min": wmin,
            "q25": q25,
            "median": q50,
            "q75": q75,
            "max": wmax,
            "probe_bins": ["Q1_LOW","Q2","Q3","Q4_HIGH"],
        },
        "probe_completeness": {
            b: {
                "row_count": per_bin_rows[b],
                "scalar_nonmissing_by_mode": dict(per_bin_scalar[b]),
                "organization_nonmissing_by_mode": dict(per_bin_org[b]),
                "joint_nonmissing_by_mode": dict(per_bin_complete[b]),
            }
            for b in ("Q1_LOW","Q2","Q3","Q4_HIGH")
        },
        "guard": (
            "This probe uses only source structure, control-variable values, and missingness. "
            "It does not emit damping, frequency, MCF, or mode-shape values and does not inspect relative onset."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "row_count": result["row_count"],
        "water_nonmissing": result["water_control"]["nonmissing_count"],
        "mode_group_count": len(groups),
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
