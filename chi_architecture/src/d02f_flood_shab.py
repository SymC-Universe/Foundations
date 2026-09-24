from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import requests
from scipy.stats import spearmanr


ZENODO_BASE = "https://zenodo.org/records/20443860/files/"
SOURCES = {
    "main": (
        "CableStayedBridge_SHM_features_2026-03-27_2026-04-10.csv",
        "34ff627723494abe2b224db433d6fa76",
    ),
    "dictionary": (
        "CableStayedBridge_SHM_features_data_dictionary.csv",
        "6d63c4c91e1e50d3b8b8dc0be8f6b762",
    ),
    "mapping": (
        "CableStayedBridge_sensor_channel_mapping.csv",
        "647eca1601a2b9f3549281c5a67cd50d",
    ),
    "readme": (
        "README_CableStayedBridge_SHM_event_dataset.txt",
        "620482add51c782e849a8641ed1fb4c6",
    ),
}
HEADERS = {
    "User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"
}
WATER_EDGES = (3.4025, 3.535, 4.7275)
PRIMARY_MODE = 1
SECONDARY_MODES = (2, 3)
K_MATCH = 30
MAX_MATCH_DISTANCE = 3.0
MIN_BIN_VALID = 10
BOOTSTRAP_N = 10_000
SEED_BASE = 20260924


class D02FRefusal(RuntimeError):
    pass


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def _float(value: Any) -> float | None:
    s = str(value or "").strip()
    if not s or s.lower() in {"nan", "na", "none"}:
        return None
    try:
        x = float(s)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def _hash_bytes(data: bytes, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def fetch_sources(cache_dir: Path) -> dict[str, dict[str, Any]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = {}
    for role, (name, expected_md5) in SOURCES.items():
        path = cache_dir / name
        if not path.exists() or _hash_bytes(path.read_bytes(), "md5") != expected_md5:
            r = requests.get(ZENODO_BASE + name + "?download=1", headers=HEADERS, timeout=180)
            r.raise_for_status()
            path.write_bytes(r.content)
        data = path.read_bytes()
        actual = _hash_bytes(data, "md5")
        if actual != expected_md5:
            raise D02FRefusal(f"MD5 mismatch for {name}: {actual}")
        out[role] = {
            "filename": name,
            "path": str(path),
            "md5": actual,
            "sha256": _hash_bytes(data, "sha256"),
            "size_bytes": len(data),
            "url": ZENODO_BASE + name + "?download=1",
        }
    return out


def load_rows(main_path: Path) -> list[dict[str, str]]:
    text = main_path.read_text(encoding="utf-8-sig", errors="replace")
    return list(csv.DictReader(io.StringIO(text)))


def mode_shape_fields(headers: list[str], mode: int) -> list[tuple[str, str]]:
    tag = f"phi_mode_{mode:02d}_"
    reals = sorted(h for h in headers if h.startswith(tag) and h.endswith("_real"))
    pairs = []
    for real in reals:
        imag = real[:-5] + "_imag"
        if imag not in headers:
            raise D02FRefusal(f"missing imaginary pair for {real}")
        pairs.append((real, imag))
    if not pairs:
        raise D02FRefusal(f"no complex mode-shape fields for mode {mode}")
    return pairs


def mode_vector(row: dict[str, str], pairs: list[tuple[str, str]]) -> np.ndarray | None:
    vals = []
    for real_col, imag_col in pairs:
        re = _float(row.get(real_col))
        im = _float(row.get(imag_col))
        if re is None or im is None:
            return None
        vals.append(complex(re, im))
    v = np.asarray(vals, dtype=complex)
    norm = float(np.linalg.norm(v))
    if not math.isfinite(norm) or norm <= 0.0:
        return None
    return v / norm


def mode_scalar(row: dict[str, str], mode: int) -> float | None:
    freq = _float(row.get(f"freq_mode_{mode:02d}_Hz"))
    chi = _float(row.get(f"damping_mode_{mode:02d}"))
    if freq is None or chi is None or freq <= 0.0 or not (0.0 < chi < 1.0):
        return None
    return chi


def eov_vector(row: dict[str, str]) -> np.ndarray | None:
    temp = _float(row.get("temp_air_C"))
    wind = _float(row.get("wind_speed_kmh"))
    r1 = _float(row.get("rms_AM1Z_microg"))
    r2 = _float(row.get("rms_AM2Z_microg"))
    if None in (temp, wind, r1, r2):
        return None
    if r1 < 0.0 or r2 < 0.0:
        return None
    op = math.log1p((r1 + r2) / 2.0)
    return np.asarray([temp, wind, op], dtype=float)


def robust_center_scale(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    center = np.median(x, axis=0)
    mad = np.median(np.abs(x - center), axis=0)
    scale = 1.4826 * mad
    for j in range(x.shape[1]):
        if not math.isfinite(float(scale[j])) or scale[j] <= 0.0:
            q25, q75 = np.percentile(x[:, j], [25.0, 75.0])
            scale[j] = (q75 - q25) / 1.349
        if not math.isfinite(float(scale[j])) or scale[j] <= 0.0:
            scale[j] = np.std(x[:, j], ddof=1)
        if not math.isfinite(float(scale[j])) or scale[j] <= 0.0:
            raise D02FRefusal(f"EOV covariate {j} has zero robust scale")
    return center, scale


def principal_reference(vectors: list[np.ndarray]) -> np.ndarray:
    if not vectors:
        raise D02FRefusal("empty mode-vector reference set")
    p = np.zeros((vectors[0].size, vectors[0].size), dtype=complex)
    for v in vectors:
        p += np.outer(v, v.conj())
    p /= float(len(vectors))
    vals, vecs = np.linalg.eigh(p)
    v = vecs[:, int(np.argmax(vals))]
    return v / np.linalg.norm(v)


def dissimilarity(ref: np.ndarray, vec: np.ndarray) -> float:
    x = 1.0 - abs(np.vdot(ref, vec)) ** 2
    return float(min(1.0, max(0.0, np.real_if_close(x).item())))


def scalar_margin(event_chi: float, controls: np.ndarray) -> float:
    q025, q975 = np.percentile(controls, [2.5, 97.5])
    if event_chi > q975:
        return float(event_chi - q975)
    if event_chi < q025:
        return float(q025 - event_chi)
    return float(-min(event_chi - q025, q975 - event_chi))


def organization_margin(event_vec: np.ndarray, control_vecs: list[np.ndarray]) -> tuple[float, float, float]:
    if len(control_vecs) != K_MATCH:
        raise D02FRefusal("organization matching must contain exactly 30 controls")
    ref = principal_reference(control_vecs)
    d_event = dissimilarity(ref, event_vec)
    loo = []
    for j, vec in enumerate(control_vecs):
        subset = control_vecs[:j] + control_vecs[j + 1:]
        ref_j = principal_reference(subset)
        loo.append(dissimilarity(ref_j, vec))
    threshold = float(np.percentile(np.asarray(loo), 97.5))
    return float(d_event - threshold), d_event, threshold


def water_bin(water: float) -> str:
    q25, q50, q75 = WATER_EDGES
    if water <= q25:
        return "E1_LOW"
    if water <= q50:
        return "E2"
    if water <= q75:
        return "E3"
    return "E4_HIGH"


def bootstrap_median_ci(values: list[float], seed: int) -> dict[str, float]:
    a = np.asarray(values, dtype=float)
    if a.size == 0:
        raise D02FRefusal("cannot bootstrap empty values")
    rng = np.random.default_rng(seed)
    samples = rng.choice(a, size=(BOOTSTRAP_N, a.size), replace=True)
    meds = np.median(samples, axis=1)
    low, high = np.percentile(meds, [2.5, 97.5])
    return {
        "n": int(a.size),
        "median": float(np.median(a)),
        "lower95": float(low),
        "upper95": float(high),
    }


def onset(statuses: dict[str, str], changed_token: str) -> tuple[str | None, bool]:
    ordered = ("E1_LOW", "E2", "E3", "E4_HIGH")
    for i, level in enumerate(ordered):
        status = statuses[level]
        if status == "NON_IDENTIFIABLE":
            # Any missing earlier or current state blocks later onset.
            return None, False
        if status == changed_token:
            return level, True
    return None, True


def ordering(scalar_status: dict[str, str], org_status: dict[str, str]) -> dict[str, Any]:
    levels = ("E1_LOW", "E2", "E3", "E4_HIGH")
    t_chi, chi_ident = onset(scalar_status, "TRANSFORMED")
    t_org, org_ident = onset(org_status, "CHANGED")
    if not chi_ident or not org_ident:
        return {"outcome": "ORDERING_NON_IDENTIFIABLE", "t_chi": t_chi, "t_org": t_org}
    if t_chi is None and t_org is None:
        out = "NEITHER_CHANGES"
    elif t_chi is None:
        out = "ORGANIZATION_CHANGES_SCALAR_DOES_NOT"
    elif t_org is None:
        out = "SCALAR_CHANGES_ORGANIZATION_DOES_NOT"
    else:
        i_chi = levels.index(t_chi)
        i_org = levels.index(t_org)
        if i_org < i_chi:
            out = "ORGANIZATION_PRECEDES_SCALAR"
        elif i_chi < i_org:
            out = "SCALAR_PRECEDES_ORGANIZATION"
        else:
            out = "SIMULTANEOUS_WITHIN_FROZEN_LEVELS"
    return {"outcome": out, "t_chi": t_chi, "t_org": t_org}


def analyze_mode(rows: list[dict[str, str]], mode: int) -> dict[str, Any]:
    headers = list(rows[0].keys())
    pairs = mode_shape_fields(headers, mode)

    controls = []
    for idx, row in enumerate(rows):
        if not _truthy(row.get("pre_event_window")):
            continue
        chi = mode_scalar(row, mode)
        vec = mode_vector(row, pairs)
        eov = eov_vector(row)
        if chi is None or vec is None or eov is None:
            continue
        controls.append({"row_index": idx, "chi": chi, "vec": vec, "eov": eov})
    if len(controls) < 100:
        raise D02FRefusal(f"mode {mode}: pre-event control pool below 100 ({len(controls)})")

    x_control = np.vstack([c["eov"] for c in controls])
    center, scale = robust_center_scale(x_control)
    z_control = (x_control - center) / scale

    event_items = []
    for idx, row in enumerate(rows):
        if not _truthy(row.get("april_2026_hydrometric_event_window")):
            continue
        water = _float(row.get("water_level_proxy_m"))
        if water is None:
            continue
        chi = mode_scalar(row, mode)
        vec = mode_vector(row, pairs)
        eov = eov_vector(row)
        if chi is None or vec is None or eov is None:
            event_items.append({
                "row_index": idx,
                "water_level_proxy_m": water,
                "bin": water_bin(water),
                "status": "NON_IDENTIFIABLE",
            })
            continue
        z = (eov - center) / scale
        dist = np.linalg.norm(z_control - z, axis=1)
        order_idx = np.argsort(dist)
        chosen = order_idx[:K_MATCH]
        d30 = float(dist[chosen[-1]])
        if d30 > MAX_MATCH_DISTANCE:
            event_items.append({
                "row_index": idx,
                "water_level_proxy_m": water,
                "bin": water_bin(water),
                "status": "EOV_NON_IDENTIFIABLE",
                "distance_30th": d30,
            })
            continue
        matched = [controls[int(k)] for k in chosen]
        s_margin = scalar_margin(chi, np.asarray([m["chi"] for m in matched], dtype=float))
        o_margin, d_event, t_org = organization_margin(vec, [m["vec"] for m in matched])
        event_items.append({
            "row_index": idx,
            "water_level_proxy_m": water,
            "bin": water_bin(water),
            "status": "VALID",
            "distance_30th": d30,
            "chi": chi,
            "scalar_margin": s_margin,
            "organization_dissimilarity": d_event,
            "organization_threshold": t_org,
            "organization_margin": o_margin,
        })

    bin_results = {}
    scalar_status = {}
    org_status = {}
    for i, level in enumerate(("E1_LOW", "E2", "E3", "E4_HIGH")):
        subset = [x for x in event_items if x["bin"] == level]
        valid = [x for x in subset if x["status"] == "VALID"]
        s_vals = [x["scalar_margin"] for x in valid]
        o_vals = [x["organization_margin"] for x in valid]
        if len(s_vals) < MIN_BIN_VALID:
            s_summary = None
            s_status = "NON_IDENTIFIABLE"
        else:
            s_summary = bootstrap_median_ci(s_vals, SEED_BASE + i)
            s_status = "TRANSFORMED" if s_summary["lower95"] > 0.0 else "UNCHANGED"
        if len(o_vals) < MIN_BIN_VALID:
            o_summary = None
            o_status = "NON_IDENTIFIABLE"
        else:
            o_summary = bootstrap_median_ci(o_vals, SEED_BASE + 100 + i)
            o_status = "CHANGED" if o_summary["lower95"] > 0.0 else "UNCHANGED"
        scalar_status[level] = s_status
        org_status[level] = o_status
        bin_results[level] = {
            "source_rows": len(subset),
            "valid_rows": len(valid),
            "scalar_status": s_status,
            "scalar_margin_bootstrap": s_summary,
            "organization_status": o_status,
            "organization_margin_bootstrap": o_summary,
        }

    result_ordering = ordering(scalar_status, org_status)
    return {
        "mode": f"mode_{mode:02d}",
        "control_pool_n": len(controls),
        "eov_center": center.tolist(),
        "eov_scale": scale.tolist(),
        "shape_component_count": len(pairs),
        "event_rows": event_items,
        "bins": bin_results,
        "ordering": result_ordering,
    }


def native_power_gate(rows: list[dict[str, str]]) -> dict[str, Any]:
    candidates = [
        h for h in rows[0]
        if h.startswith("rms_")
        or h.startswith("loadcell_")
        or "displacement" in h.lower()
        or h.lower().startswith("disp_")
    ]
    summaries = []
    for col in candidates:
        xs, ys = [], []
        for row in rows:
            if not _truthy(row.get("april_2026_hydrometric_event_window")):
                continue
            x = _float(row.get("water_level_proxy_m"))
            y = _float(row.get(col))
            if x is not None and y is not None:
                xs.append(x)
                ys.append(y)
        if len(xs) >= 20 and len(set(xs)) >= 3:
            rho, p = spearmanr(xs, ys)
            if math.isfinite(float(rho)) and math.isfinite(float(p)):
                summaries.append({
                    "field": col,
                    "n": len(xs),
                    "abs_spearman_rho": abs(float(rho)),
                    "p_value": float(p),
                })
    summaries.sort(key=lambda x: (-x["abs_spearman_rho"], x["p_value"], x["field"]))
    strongest = summaries[0] if summaries else None
    passed = bool(
        strongest
        and strongest["abs_spearman_rho"] >= 0.20
        and strongest["p_value"] < 0.01
    )
    return {"pass": passed, "strongest": strongest}


def run_d02f(cache_dir: Path) -> dict[str, Any]:
    sources = fetch_sources(cache_dir)
    rows = load_rows(Path(sources["main"]["path"]))
    if len(rows) != 718:
        raise D02FRefusal(f"unexpected source row count: {len(rows)}")

    power = native_power_gate(rows)
    if not power["pass"]:
        raise D02FRefusal("predeclared native intervention power gate failed")

    primary = analyze_mode(rows, PRIMARY_MODE)
    secondary = {f"mode_{m:02d}": analyze_mode(rows, m) for m in SECONDARY_MODES}

    outcome = primary["ordering"]["outcome"]
    support = outcome in {
        "ORGANIZATION_PRECEDES_SCALAR",
        "ORGANIZATION_CHANGES_SCALAR_DOES_NOT",
    }
    adverse = outcome in {
        "SCALAR_PRECEDES_ORGANIZATION",
        "SCALAR_CHANGES_ORGANIZATION_DOES_NOT",
    }

    return {
        "schema": "d02f-flood-shab-prospective-result-v0.1",
        "status": "P1_PROSPECTIVE_EXTERNAL_D02F_EXECUTED",
        "claim_id": "CA-D007-D02F-v0.1",
        "source_doi": "10.5281/zenodo.20443860",
        "source_files": {
            role: {k:v for k,v in meta.items() if k != "path"}
            for role,meta in sources.items()
        },
        "water_bin_edges_m": {
            "q25": WATER_EDGES[0],
            "median": WATER_EDGES[1],
            "q75": WATER_EDGES[2],
        },
        "native_intervention_power_gate": power,
        "primary": primary,
        "secondary_robustness": secondary,
        "outcome": outcome,
        "ca_d007_support": support,
        "ca_d007_adverse_ordering": adverse,
        "native_toolkit_verdict": "NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE",
        "scope": (
            "Prospectively frozen external physical test of CA-D007. "
            "Secondary modes cannot change the primary mode-01 verdict."
        ),
    }
