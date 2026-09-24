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
from scipy.stats import spearmanr


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
    pattern = re.compile(r"(?:^|_)mode_?(\d{1,2})(?:_|$)", re.I)
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
    if "mode_01" not in groups:
        raise RuntimeError("mode grouping failed: mode_01 absent")
    required_probe = {"freq_mode_01_Hz", "damping_mode_01", "phi_mode_01_AM1Z_real"}
    if not required_probe.issubset(set(groups["mode_01"])):
        raise RuntimeError("mode_01 grouping failed source-header regression guard")

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

    def truthy(v):
        return str(v or "").strip().lower() in {"1","true","yes","y"}

    event_rows = [r for r in rows if truthy(r.get("april_2026_hydrometric_event_window"))]
    pre_rows = [r for r in rows if truthy(r.get("pre_event_window"))]

    event_water = [to_float(r.get(water_col, "")) for r in event_rows]
    event_water = [v for v in event_water if v is not None]
    event_q = {
        "q25": percentile(event_water, 0.25),
        "median": percentile(event_water, 0.50),
        "q75": percentile(event_water, 0.75),
        "min": min(event_water) if event_water else None,
        "max": max(event_water) if event_water else None,
    }

    def event_bin(v):
        if v is None or event_q["q25"] is None:
            return None
        if v <= event_q["q25"]:
            return "E1_LOW"
        if v <= event_q["median"]:
            return "E2"
        if v <= event_q["q75"]:
            return "E3"
        return "E4_HIGH"

    event_counts = defaultdict(int)
    event_joint = defaultdict(lambda: defaultdict(int))
    covariates = ["temp_air_C", "wind_speed_kmh", "rms_AM1Z_microg", "rms_AM2Z_microg"]
    event_cov_nonmissing = defaultdict(int)
    pre_cov_nonmissing = defaultdict(int)

    for r in event_rows:
        b = event_bin(to_float(r.get(water_col, "")))
        if b is None:
            continue
        event_counts[b] += 1
        for cov in covariates:
            if to_float(r.get(cov, "")) is not None:
                event_cov_nonmissing[cov] += 1
        for mode, cols in groups.items():
            damping = [x for x in cols if "damp" in x.lower()]
            freq = [x for x in cols if "freq" in x.lower()]
            org = [x for x in cols if any(k in x.lower() for k in ("mcf", "real", "imag", "shape"))]
            scalar_ok = bool(damping and freq) and all(to_float(r.get(x, "")) is not None for x in damping + freq)
            org_ok = bool(org) and all(to_float(r.get(x, "")) is not None for x in org)
            if scalar_ok and org_ok:
                event_joint[b][mode] += 1

    for r in pre_rows:
        for cov in covariates:
            if to_float(r.get(cov, "")) is not None:
                pre_cov_nonmissing[cov] += 1

    native_response_cols = [
        h for h in headers
        if h.startswith("rms_")
        or h.startswith("loadcell_")
        or "displacement" in h.lower()
        or h.lower().startswith("disp_")
    ]
    native_power = []
    for col in native_response_cols:
        xs, ys = [], []
        for r in event_rows:
            x = to_float(r.get(water_col, ""))
            y = to_float(r.get(col, ""))
            if x is not None and y is not None:
                xs.append(x)
                ys.append(y)
        if len(xs) >= 20 and len(set(xs)) >= 3:
            rho, p = spearmanr(xs, ys)
            if math.isfinite(float(rho)) and math.isfinite(float(p)):
                native_power.append({
                    "field": col,
                    "n": len(xs),
                    "abs_spearman_rho": abs(float(rho)),
                    "p_value": float(p),
                })
    native_power.sort(key=lambda x: (-x["abs_spearman_rho"], x["p_value"], x["field"]))
    strongest_native_power = native_power[0] if native_power else None
    native_power_pass = bool(
        strongest_native_power
        and strongest_native_power["abs_spearman_rho"] >= 0.20
        and strongest_native_power["p_value"] < 0.01
    )

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
        "native_intervention_power_gate": {
            "allowed_response_fields": native_response_cols,
            "criterion": "at least one non-modal native response has abs Spearman rho >=0.20 with p<0.01 versus event water level",
            "pass": native_power_pass,
            "strongest_response": strongest_native_power,
            "all_tested_summaries": native_power,
            "guard": "No modal frequency, damping, MCF, or mode-shape values are used in this power gate.",
        },
        "event_only_completeness": {
            "event_row_count": len(event_rows),
            "event_water_nonmissing_count": len(event_water),
            "event_water_summary": event_q,
            "event_bins": {
                b: {
                    "row_count": event_counts[b],
                    "joint_nonmissing_by_mode": dict(event_joint[b]),
                }
                for b in ("E1_LOW","E2","E3","E4_HIGH")
            },
            "event_covariate_nonmissing": dict(event_cov_nonmissing),
            "pre_event_row_count": len(pre_rows),
            "pre_event_covariate_nonmissing": dict(pre_cov_nonmissing),
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
