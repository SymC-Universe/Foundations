from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import requests
from scipy.signal import find_peaks, get_window


SERVER = "https://dataverse.csuc.cat"
PID = "doi:10.34810/data1011"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}
FS = 1600.0
NPERSEG = 8192
NOVERLAP = 4096
TARGET_HZ = 8.7890625
WINDOW_LOW_HZ = 0.95 * TARGET_HZ
WINDOW_HIGH_HZ = 1.05 * TARGET_HZ
STATE_ORDER = ("9Nm", "6Nm", "NoBolt")
LOCATION_ORDER = ("level_1", "level_2", "level_3", "level_4")
BOOTSTRAP_SEED = 20260923
BOOTSTRAP_N = 10000


class D02ERefusal(RuntimeError):
    pass


def api_json(url: str, **params) -> dict:
    r = requests.get(url, params=params, headers=HEADERS, timeout=180)
    r.raise_for_status()
    x = r.json()
    if x.get("status") != "OK":
        raise D02ERefusal("Dataverse API did not return OK")
    return x


def dataset_files() -> list[dict]:
    x = api_json(f"{SERVER}/api/datasets/:persistentId/", persistentId=PID)
    return x["data"]["latestVersion"]["files"]


def original_csv_files(files: list[dict], directory: str) -> list[dict]:
    rows = []
    for item in files:
        if item.get("directoryLabel", "") != directory:
            continue
        df = item["dataFile"]
        label = item["label"]
        if label.endswith(".csv") and df.get("contentType") == "text/csv":
            rows.append({
                "id": int(df["id"]),
                "filename": label,
                "md5": df.get("md5"),
                "size": int(df.get("filesize", 0)),
                "directory": directory,
            })
    rows.sort(key=lambda x: int(x["filename"].split("_")[1].split(".")[0]))
    return rows


def fetch_bytes(file_id: int) -> bytes:
    r = requests.get(f"{SERVER}/api/access/datafile/{file_id}", headers=HEADERS, timeout=300)
    r.raise_for_status()
    return r.content


def parse_response_csv(raw: bytes) -> tuple[list[str], np.ndarray]:
    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))
    rows = iter(reader)
    try:
        header = next(rows)
    except StopIteration as exc:
        raise D02ERefusal("empty CSV") from exc
    width = len(header)
    clean = []
    for row in rows:
        if not row or all(not str(x).strip() for x in row):
            continue
        if len(row) != width:
            continue
        try:
            clean.append([float(x) for x in row])
        except ValueError:
            continue
    if not clean:
        raise D02ERefusal("no complete numeric rows matching CSV header width")
    data = np.asarray(clean, dtype=float)
    if data.ndim != 2 or data.shape[1] != width:
        raise D02ERefusal("unexpected parsed CSV dimensionality")
    keep = []
    names = []
    for i, name in enumerate(header):
        low = name.strip().lower()
        if low in {"", "time", "timestamp", "t", "index", "sample", "unnamed: 0"}:
            continue
        keep.append(i)
        names.append(name)
    x = data[:, keep]
    if x.shape[1] != 24:
        raise D02ERefusal(f"expected 24 response channels, got {x.shape[1]}")
    if not np.all(np.isfinite(x)):
        raise D02ERefusal("nonfinite response value")
    return names, x


def vectorized_fdd_window(
    x: np.ndarray,
    fs: float = FS,
    nperseg: int = NPERSEG,
    noverlap: int = NOVERLAP,
    low_hz: float = WINDOW_LOW_HZ,
    high_hz: float = WINDOW_HIGH_HZ,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if x.ndim != 2 or x.shape[1] < 2:
        raise D02ERefusal("response matrix must be samples x channels")
    if x.shape[0] < nperseg:
        raise D02ERefusal("response record shorter than nperseg")
    step = nperseg - noverlap
    starts = np.arange(0, x.shape[0] - nperseg + 1, step, dtype=int)
    if starts.size < 1:
        raise D02ERefusal("no Welch segments")

    freq = np.fft.rfftfreq(nperseg, d=1.0 / fs)
    sel = np.where((freq >= low_hz) & (freq <= high_hz))[0]
    if sel.size < 3:
        raise D02ERefusal("tracking window has too few spectral bins")

    win = get_window("hann", nperseg, fftbins=True).astype(float)
    scale = 1.0 / (fs * float(np.sum(win * win)))
    accum = np.zeros((sel.size, x.shape[1], x.shape[1]), dtype=complex)

    for start in starts:
        seg = np.asarray(x[start:start + nperseg], dtype=float)
        seg = seg - np.mean(seg, axis=0, keepdims=True)
        fft = np.fft.rfft(seg * win[:, None], axis=0)[sel]
        accum += np.einsum("fc,fd->fcd", np.conjugate(fft), fft, optimize=True)

    accum *= scale / float(starts.size)
    # selected frequencies are interior one-sided bins, so scipy CSD doubles power.
    accum *= 2.0

    s1 = np.empty(sel.size, dtype=float)
    vecs = np.empty((sel.size, x.shape[1]), dtype=complex)
    for i, mat in enumerate(accum):
        vals, vec = np.linalg.eigh(mat)
        idx = int(np.argmax(np.real(vals)))
        s1[i] = float(np.real(vals[idx]))
        v = vec[:, idx]
        vecs[i] = v / np.linalg.norm(v)
    return freq[sel], s1, vecs


def _interp_crossing(x0: float, y0: float, x1: float, y1: float, target: float) -> float:
    if y1 == y0:
        return 0.5 * (x0 + x1)
    return float(x0 + (target - y0) * (x1 - x0) / (y1 - y0))


def analyze_primary_family(freq: np.ndarray, s1: np.ndarray, vecs: np.ndarray) -> dict:
    peaks, _ = find_peaks(s1)
    if len(peaks) == 0:
        return {"status": "NON_IDENTIFIABLE"}
    q = int(min(peaks, key=lambda z: abs(float(freq[z]) - TARGET_HZ)))
    competitors = [
        int(z) for z in peaks
        if int(z) != q and float(s1[int(z)]) >= 0.90 * float(s1[q])
    ]
    if competitors:
        return {
            "status": "NON_IDENTIFIABLE_MODAL_OVERLAP",
            "f_peak_hz": float(freq[q]),
            "competitor_hz": [float(freq[z]) for z in competitors],
        }
    if q == 0 or q == len(s1) - 1:
        return {"status": "NON_IDENTIFIABLE", "f_peak_hz": float(freq[q])}

    peak = float(s1[q])
    target = peak / 2.0

    left = q
    while left > 0 and s1[left] >= target:
        left -= 1
    right = q
    while right < len(s1) - 1 and s1[right] >= target:
        right += 1

    base = {
        "status": "IDENTIFIABLE",
        "f_peak_hz": float(freq[q]),
        "mode_vector_real": [float(v) for v in np.real(vecs[q])],
        "mode_vector_imag": [float(v) for v in np.imag(vecs[q])],
    }

    if (left == 0 and s1[left] >= target) or (right == len(s1) - 1 and s1[right] >= target):
        return {**base, "scalar_status": "NO_ADMISSIBLE_SCALAR_CHI"}

    fl = _interp_crossing(
        float(freq[left]), float(s1[left]),
        float(freq[left + 1]), float(s1[left + 1]),
        target,
    )
    fr = _interp_crossing(
        float(freq[right - 1]), float(s1[right - 1]),
        float(freq[right]), float(s1[right]),
        target,
    )
    bw = float(fr - fl)
    if not math.isfinite(bw) or bw <= 0:
        return {**base, "scalar_status": "NO_ADMISSIBLE_SCALAR_CHI"}

    chi = bw / (2.0 * float(freq[q]))
    return {
        **base,
        "scalar_status": "ADMITTED",
        "bandwidth_hz": bw,
        "chi": float(chi),
    }


def analyze_raw(raw: bytes) -> dict:
    names, x = parse_response_csv(raw)
    freq, s1, vecs = vectorized_fdd_window(x)
    result = analyze_primary_family(freq, s1, vecs)
    result["channel_names"] = names
    result["sample_count"] = int(x.shape[0])
    return result


def download_and_analyze(meta: dict) -> dict:
    raw = fetch_bytes(meta["id"])
    actual = hashlib.md5(raw).hexdigest()
    if meta["md5"] and actual != meta["md5"]:
        raise D02ERefusal(f"MD5 mismatch: {meta['directory']}/{meta['filename']}")
    out = analyze_raw(raw)
    out["file"] = {
        "id": meta["id"],
        "filename": meta["filename"],
        "directory": meta["directory"],
        "md5": actual,
        "size": len(raw),
    }
    return out


def bootstrap_median_ci(values: list[float]) -> dict:
    arr = np.asarray(values, dtype=float)
    if arr.size < 1:
        raise D02ERefusal("cannot bootstrap empty values")
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    idx = rng.integers(0, arr.size, size=(BOOTSTRAP_N, arr.size))
    meds = np.median(arr[idx], axis=1)
    lo, hi = np.percentile(meds, [2.5, 97.5])
    return {
        "n": int(arr.size),
        "median": float(np.median(arr)),
        "lower95": float(lo),
        "upper95": float(hi),
    }


def complex_vector(record: dict) -> np.ndarray | None:
    if record.get("status") != "IDENTIFIABLE":
        return None
    re = np.asarray(record["mode_vector_real"], dtype=float)
    im = np.asarray(record["mode_vector_imag"], dtype=float)
    v = re + 1j * im
    norm = float(np.linalg.norm(v))
    if not math.isfinite(norm) or norm <= 0:
        return None
    return v / norm


def principal_reference(vectors: list[np.ndarray]) -> np.ndarray:
    if len(vectors) < 1:
        raise D02ERefusal("no vectors for reference")
    p = np.mean([np.outer(v, np.conjugate(v)) for v in vectors], axis=0)
    vals, vecs = np.linalg.eigh(p)
    v = vecs[:, int(np.argmax(np.real(vals)))]
    return v / np.linalg.norm(v)


def dissimilarity(vref: np.ndarray, v: np.ndarray) -> float:
    value = 1.0 - abs(np.vdot(vref, v)) ** 2
    return float(max(0.0, min(1.0, np.real(value))))


def healthy_references(records: list[dict]) -> dict:
    admitted_chi = [float(r["chi"]) for r in records if r.get("scalar_status") == "ADMITTED"]
    if len(admitted_chi) < 16:
        raise D02ERefusal(f"healthy admitted chi below frozen floor: {len(admitted_chi)}")
    scalar = bootstrap_median_ci(admitted_chi)

    vectors = [complex_vector(r) for r in records]
    vectors = [v for v in vectors if v is not None]
    if len(vectors) < 16:
        raise D02ERefusal(f"healthy organization vectors below frozen floor: {len(vectors)}")
    vref = principal_reference(vectors)

    loo = []
    for i, v in enumerate(vectors):
        others = vectors[:i] + vectors[i + 1:]
        ref_i = principal_reference(others)
        loo.append(dissimilarity(ref_i, v))
    threshold = float(np.percentile(np.asarray(loo), 97.5))

    return {
        "scalar": scalar,
        "organization_threshold": threshold,
        "organization_valid_n": len(vectors),
        "organization_leave_one_out": [float(x) for x in loo],
        "reference_vector_real": [float(x) for x in np.real(vref)],
        "reference_vector_imag": [float(x) for x in np.imag(vref)],
    }


def state_summary(records: list[dict], healthy: dict) -> dict:
    chis = [float(r["chi"]) for r in records if r.get("scalar_status") == "ADMITTED"]
    if len(chis) >= 16:
        scalar_ci = bootstrap_median_ci(chis)
        h = healthy["scalar"]
        transformed = (
            scalar_ci["upper95"] < h["lower95"]
            or scalar_ci["lower95"] > h["upper95"]
        )
        scalar_status = "TRANSFORMED" if transformed else "UNCHANGED"
    else:
        scalar_ci = None
        scalar_status = "NON_IDENTIFIABLE"

    vref = np.asarray(healthy["reference_vector_real"], dtype=float) + 1j * np.asarray(
        healthy["reference_vector_imag"], dtype=float
    )
    dvals = []
    for r in records:
        v = complex_vector(r)
        if v is not None:
            dvals.append(dissimilarity(vref, v))

    if len(dvals) >= 16:
        lower = float(np.percentile(np.asarray(dvals), 2.5))
        changed = lower > float(healthy["organization_threshold"])
        org_status = "CHANGED" if changed else "UNCHANGED"
        org_summary = {
            "valid_n": len(dvals),
            "median": float(np.median(dvals)),
            "lower2_5": lower,
            "upper97_5": float(np.percentile(np.asarray(dvals), 97.5)),
        }
    else:
        org_status = "NON_IDENTIFIABLE"
        org_summary = {"valid_n": len(dvals)}

    return {
        "scalar_status": scalar_status,
        "scalar_admitted_n": len(chis),
        "scalar_ci": scalar_ci,
        "organization_status": org_status,
        "organization": org_summary,
        "record_status_counts": {
            key: sum(1 for r in records if r.get("scalar_status") == key or r.get("status") == key)
            for key in (
                "ADMITTED",
                "NO_ADMISSIBLE_SCALAR_CHI",
                "IDENTIFIABLE",
                "NON_IDENTIFIABLE",
                "NON_IDENTIFIABLE_MODAL_OVERLAP",
            )
        },
    }


def observable_onset(states: dict[str, dict], field: str, changed_label: str) -> dict:
    prior_valid = True
    for idx, state in enumerate(STATE_ORDER):
        status = states[state][field]
        if status == "NON_IDENTIFIABLE":
            return {"kind": "NON_IDENTIFIABLE", "onset_index": None, "onset_state": None}
        if status == changed_label:
            if not prior_valid:
                return {"kind": "NON_IDENTIFIABLE", "onset_index": None, "onset_state": None}
            return {"kind": "CHANGED", "onset_index": idx, "onset_state": state}
        prior_valid = prior_valid and status == "UNCHANGED"
    return {"kind": "DOES_NOT_CHANGE", "onset_index": None, "onset_state": None}


def classify_location(states: dict[str, dict]) -> dict:
    scalar = observable_onset(states, "scalar_status", "TRANSFORMED")
    org = observable_onset(states, "organization_status", "CHANGED")

    if scalar["kind"] == "NON_IDENTIFIABLE" or org["kind"] == "NON_IDENTIFIABLE":
        outcome = "ORDERING_NON_IDENTIFIABLE"
    elif scalar["kind"] == "DOES_NOT_CHANGE" and org["kind"] == "DOES_NOT_CHANGE":
        outcome = "NEITHER_CHANGES"
    elif scalar["kind"] == "DOES_NOT_CHANGE" and org["kind"] == "CHANGED":
        outcome = "ORGANIZATION_CHANGES_SCALAR_DOES_NOT"
    elif scalar["kind"] == "CHANGED" and org["kind"] == "DOES_NOT_CHANGE":
        outcome = "SCALAR_CHANGES_ORGANIZATION_DOES_NOT"
    elif scalar["kind"] == "CHANGED" and org["kind"] == "CHANGED":
        if org["onset_index"] < scalar["onset_index"]:
            outcome = "ORGANIZATION_PRECEDES_SCALAR"
        elif scalar["onset_index"] < org["onset_index"]:
            outcome = "SCALAR_PRECEDES_ORGANIZATION"
        else:
            outcome = "SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION"
    else:
        outcome = "ORDERING_NON_IDENTIFIABLE"

    return {"outcome": outcome, "scalar_onset": scalar, "organization_onset": org}


def domain_outcome(location_outcomes: dict[str, str]) -> str:
    values = list(location_outcomes.values())
    if any(v == "ORDERING_NON_IDENTIFIABLE" for v in values):
        return "INDETERMINATE"
    org_first = sum(v in {"ORGANIZATION_PRECEDES_SCALAR", "ORGANIZATION_CHANGES_SCALAR_DOES_NOT"} for v in values)
    scalar_first = sum(v in {"SCALAR_PRECEDES_ORGANIZATION", "SCALAR_CHANGES_ORGANIZATION_DOES_NOT"} for v in values)
    if org_first >= 3 and scalar_first == 0:
        return "SUPPORT"
    if scalar_first >= 3 and org_first == 0:
        return "ADVERSE"
    return "NO_SUPPORT"


def _analyze_group(metas: list[dict], max_workers: int = 6) -> list[dict]:
    results = [None] * len(metas)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {
            pool.submit(download_and_analyze, meta): i
            for i, meta in enumerate(metas)
        }
        for future in as_completed(future_map):
            i = future_map[future]
            results[i] = future.result()
    return results


def run_d02e() -> dict:
    files = dataset_files()

    healthy_meta = original_csv_files(files, "DATA/A_1/Healthy")
    if len(healthy_meta) != 20:
        raise D02ERefusal(f"expected 20 healthy original CSVs, got {len(healthy_meta)}")

    groups = {"Healthy": healthy_meta}
    for state in STATE_ORDER:
        for location in LOCATION_ORDER:
            directory = f"DATA/A_1/{state}/{location}"
            metas = original_csv_files(files, directory)
            if len(metas) != 20:
                raise D02ERefusal(f"expected 20 original CSVs in {directory}, got {len(metas)}")
            groups[f"{state}/{location}"] = metas

    healthy_records = _analyze_group(healthy_meta)
    hfreq = [
        float(r["f_peak_hz"])
        for r in healthy_records
        if r.get("status") == "IDENTIFIABLE"
    ]
    if len(hfreq) < 16:
        raise D02ERefusal("healthy primary family lost identifiability")
    if abs(float(np.median(hfreq)) - TARGET_HZ) > (FS / NPERSEG):
        raise D02ERefusal("healthy production run does not reproduce frozen primary family")

    healthy = healthy_references(healthy_records)

    locations = {}
    for location in LOCATION_ORDER:
        states = {}
        for state in STATE_ORDER:
            records = _analyze_group(groups[f"{state}/{location}"])
            states[state] = state_summary(records, healthy)
            states[state]["records"] = records
        ordering = classify_location(states)
        locations[location] = {"states": states, "ordering": ordering}

    location_outcomes = {
        location: locations[location]["ordering"]["outcome"]
        for location in LOCATION_ORDER
    }
    outcome = domain_outcome(location_outcomes)

    source_files = {}
    for metas in groups.values():
        for meta in metas:
            key = f"{meta['directory']}/{meta['filename']}"
            source_files[key] = {
                "id": meta["id"],
                "md5": meta["md5"],
                "size": meta["size"],
            }

    return {
        "schema": "d02e-jacket-prospective-result-v0.1",
        "status": "P1_PROSPECTIVE_D02E_EXECUTED",
        "claim_id": "CA-D007-D02E-v0.1",
        "source_pid": PID,
        "primary_family_hz": TARGET_HZ,
        "tracking_window_hz": [WINDOW_LOW_HZ, WINDOW_HIGH_HZ],
        "healthy": healthy,
        "healthy_records": healthy_records,
        "locations": locations,
        "location_orderings": location_outcomes,
        "outcome": outcome,
        "native_toolkit_verdict": "NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE",
        "source_counts": {
            "healthy": 20,
            "damaged": 240,
            "total": 260,
        },
        "source_files": source_files,
        "scope": (
            "Prospectively frozen domain-specific D02E test of CA-D007. "
            "No secondary mode, excitation amplitude, or alternate threshold may alter the primary verdict."
        ),
    }
