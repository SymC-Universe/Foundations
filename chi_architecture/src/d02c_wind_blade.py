from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
import zipfile
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import requests
from scipy import signal


ZENODO_BASE = "https://zenodo.org/records/18427836/files/"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}
FS = 250.0
NPERSEG = 8192
NOVERLAP = 4096
EXPECTED_MAIN_SAMPLES = 150000

ASSETS = {
    "climate_main": ("ClimateChamber_20221115.csv", "7afea2377fb14ca576516c39201a6aac"),
    "modal_x": ("MO04_mpe_X_20221115.csv", "0a08eb30f4361d3ebfd1a6ecfb4ff332"),
    "modal_z": ("MO04_mpe_Z_20221115.csv", "3e1ceb71d0fae2901c9256eb472d021a"),
    "raw_baseline": ("MO04_acceleration_20221115_000000.zip", "dc1bd7d724264e1a37ffdc58865f6304"),
    "raw_intervention": ("MO04_acceleration_20221115_130000.zip", "50e32f0e7e711b89128a895d5c0c9481"),
    "climate_dry": ("ClimateChamber_20220927.csv", "aa3dccbefeb1644e5c8cbc030801b146"),
    "raw_dry": ("MO04_acceleration_20220927.zip", "83d9f4030346d6a3538627320a03437e"),
}

RAW_COLUMNS = {
    "X": (1, 4, 7),
    "Z": (3, 6, 9),
}


class D02CRefusal(RuntimeError):
    pass


def _sha(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_asset(role: str, cache_dir: Path) -> dict[str, Any]:
    if role not in ASSETS:
        raise D02CRefusal(f"unknown source role {role}")
    name, expected_md5 = ASSETS[role]
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / name
    if not path.exists() or _sha(path, "md5") != expected_md5:
        url = ZENODO_BASE + name + "?download=1"
        with requests.get(url, headers=HEADERS, stream=True, timeout=900) as r:
            r.raise_for_status()
            with path.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                    if chunk:
                        f.write(chunk)
    actual = _sha(path, "md5")
    if actual != expected_md5:
        raise D02CRefusal(f"MD5 mismatch for {name}: {actual}")
    return {
        "role": role,
        "filename": name,
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "md5": actual,
        "sha256": _sha(path, "sha256"),
        "url": ZENODO_BASE + name + "?download=1",
    }


def parse_dt(value: str) -> datetime:
    s = str(value).strip()
    if not s:
        raise ValueError("empty timestamp")
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _float(value: Any) -> float:
    return float(str(value).strip())


def load_modal_rows(path: Path) -> list[dict[str, Any]]:
    out = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            try:
                ts = parse_dt(row["timestamp"])
                freq = _float(row["mean_frequency"])
                std_f = _float(row["std_frequency"])
                damping = _float(row["mean_damping"])
                std_d = _float(row["std_damping"])
                size = int(float(row["size"]))
            except Exception:
                continue
            out.append({
                "timestamp": ts,
                "frequency": freq,
                "std_frequency": std_f,
                "damping_pct": damping,
                "std_damping_pct": std_d,
                "size": size,
                "algorithm": str(row.get("algorithm", "")).strip().lower(),
            })
    return out


def frequency_row_admissible(row: dict[str, Any]) -> bool:
    return (
        row.get("algorithm") == "lscf"
        and row.get("size", 0) >= 3
        and math.isfinite(row.get("frequency", math.nan))
        and row["frequency"] > 0
    )


def scalar_from_row(row: dict[str, Any] | None) -> dict[str, Any]:
    if row is None or not frequency_row_admissible(row):
        return {"status": "NON_IDENTIFIABLE"}
    d = float(row["damping_pct"])
    sd = float(row["std_damping_pct"])
    n = int(row["size"])
    if not (math.isfinite(d) and math.isfinite(sd) and d > 0 and sd >= 0 and n >= 3):
        return {"status": "NON_IDENTIFIABLE"}
    chi = d / 100.0
    if not (0.0 < chi < 1.0):
        return {"status": "NO_ADMISSIBLE_SCALAR_CHI"}
    se = (sd / math.sqrt(n)) / 100.0
    return {
        "status": "ADMITTED",
        "chi": chi,
        "se_chi": se,
        "lower95": chi - 1.96 * se,
        "upper95": chi + 1.96 * se,
        "frequency_hz": float(row["frequency"]),
        "std_frequency_hz": float(row["std_frequency"]),
        "cluster_size": n,
        "source_damping_percent": d,
        "source_std_damping_percent": sd,
        "timestamp": row["timestamp"].isoformat(),
    }


def group_by_timestamp(rows: list[dict[str, Any]]) -> dict[datetime, list[dict[str, Any]]]:
    groups: dict[datetime, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if frequency_row_admissible(row):
            groups[row["timestamp"]].append(row)
    for ts in groups:
        groups[ts].sort(key=lambda r: r["frequency"])
    return dict(sorted(groups.items()))


def nearest_timestamp_rows(
    groups: dict[datetime, list[dict[str, Any]]],
    target: datetime,
    tolerance_seconds: float = 300.0,
) -> tuple[datetime | None, list[dict[str, Any]]]:
    if not groups:
        return None, []
    candidates = sorted(
        groups,
        key=lambda ts: (abs((ts - target).total_seconds()), ts),
    )
    best = candidates[0]
    if abs((best - target).total_seconds()) > tolerance_seconds:
        return None, []
    return best, groups[best]


def build_baseline_track(
    rows: list[dict[str, Any]],
    targets: list[datetime],
) -> dict[str, Any]:
    groups = group_by_timestamp(rows)
    per_target = [nearest_timestamp_rows(groups, t) for t in targets]
    first_rows = per_target[0][1]
    if not first_rows:
        raise D02CRefusal("no modal rows at first baseline target")

    tracks = []
    for row in first_rows:
        tracks.append({"rows": [row], "presence": 1, "last": row["frequency"]})

    for _, current_rows in per_target[1:]:
        # Preserve one slot per target in all tracks.
        for tr in tracks:
            tr["rows"].append(None)
        pairs = []
        for ti, tr in enumerate(tracks):
            last = float(tr["last"])
            for ri, row in enumerate(current_rows):
                rel = abs(float(row["frequency"]) - last) / last
                if rel <= 0.10:
                    pairs.append((rel, ti, ri))
        pairs.sort()
        used_t = set()
        used_r = set()
        for rel, ti, ri in pairs:
            if ti in used_t or ri in used_r:
                continue
            row = current_rows[ri]
            tracks[ti]["rows"][-1] = row
            tracks[ti]["last"] = row["frequency"]
            tracks[ti]["presence"] += 1
            used_t.add(ti)
            used_r.add(ri)

    eligible = []
    for tr in tracks:
        if tr["presence"] >= 10:
            freqs = [r["frequency"] for r in tr["rows"] if r is not None]
            tr["median_frequency"] = float(np.median(freqs))
            eligible.append(tr)
    if not eligible:
        raise D02CRefusal("no baseline modal track meets 10/12 presence floor")
    selected = min(eligible, key=lambda tr: tr["median_frequency"])
    return {
        "rows": selected["rows"],
        "presence": selected["presence"],
        "median_frequency": selected["median_frequency"],
    }


def sequential_track(
    rows: list[dict[str, Any]],
    targets: list[datetime],
    initial_frequency: float,
    tolerance_seconds: float = 300.0,
) -> list[dict[str, Any] | None]:
    groups = group_by_timestamp(rows)
    prev = float(initial_frequency)
    out = []
    for target in targets:
        _, candidates = nearest_timestamp_rows(groups, target, tolerance_seconds)
        if not candidates:
            out.append(None)
            continue
        ordered = sorted(candidates, key=lambda r: abs(r["frequency"] - prev))
        row = ordered[0]
        if abs(row["frequency"] - prev) / prev > 0.10:
            out.append(None)
            continue
        out.append(row)
        prev = float(row["frequency"])
    return out


def prespray_track(
    rows: list[dict[str, Any]],
    start: datetime,
    end: datetime,
    initial_frequency: float,
) -> list[dict[str, Any]]:
    groups = group_by_timestamp(rows)
    times = [ts for ts in groups if start <= ts <= end]
    prev = float(initial_frequency)
    out = []
    for ts in times:
        candidates = groups[ts]
        row = min(candidates, key=lambda r: abs(r["frequency"] - prev))
        if abs(row["frequency"] - prev) / prev > 0.10:
            continue
        out.append(row)
        prev = float(row["frequency"])
    return out


def scalar_control_envelope(
    baseline_rows: list[dict[str, Any] | None],
    prespray_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    baseline = [scalar_from_row(r) for r in baseline_rows]
    baseline_valid = [x for x in baseline if x["status"] == "ADMITTED"]
    control = [scalar_from_row(r) for r in prespray_rows]
    control_valid = [x for x in control if x["status"] == "ADMITTED"]
    if len(baseline_valid) < 10 or len(control_valid) < 20:
        return {
            "status": "CONTROL_INADEQUATE",
            "baseline_valid_count": len(baseline_valid),
            "prespray_valid_count": len(control_valid),
        }
    return {
        "status": "ADEQUATE",
        "baseline_valid_count": len(baseline_valid),
        "prespray_valid_count": len(control_valid),
        "lower": min(x["lower95"] for x in control_valid),
        "upper": max(x["upper95"] for x in control_valid),
        "baseline_center": float(np.median([x["chi"] for x in baseline_valid])),
    }


def scalar_change_status(scalar: dict[str, Any], envelope: dict[str, Any]) -> str:
    if envelope.get("status") != "ADEQUATE":
        return "NON_IDENTIFIABLE"
    if scalar.get("status") != "ADMITTED":
        return "NON_IDENTIFIABLE"
    if scalar["upper95"] < envelope["lower"] or scalar["lower95"] > envelope["upper"]:
        return "TRANSFORMED"
    return "UNCHANGED"


def read_main_raw_member(zf: zipfile.ZipFile, member: str) -> dict[str, np.ndarray]:
    raw = zf.read(member)
    arr = np.loadtxt(
        io.BytesIO(raw),
        delimiter=",",
        skiprows=1,
        usecols=(1, 3, 4, 6, 7, 9),
        dtype=float,
    )
    if arr.ndim != 2 or arr.shape[1] != 6:
        raise D02CRefusal(f"unexpected raw shape in {member}: {arr.shape}")
    n = arr.shape[0]
    if n < 0.95 * EXPECTED_MAIN_SAMPLES or n > 1.05 * EXPECTED_MAIN_SAMPLES:
        raise D02CRefusal(f"RAW_WINDOW_LENGTH_INVALID {member}: {n}")
    if not np.all(np.isfinite(arr)):
        raise D02CRefusal(f"nonfinite acceleration in {member}")
    return {
        "X": arr[:, [0, 2, 4]],
        "Z": arr[:, [1, 3, 5]],
    }


def _csd_vector(data: np.ndarray, target_frequency: float, nperseg: int = NPERSEG) -> np.ndarray:
    if data.ndim != 2 or data.shape[1] != 3:
        raise D02CRefusal("organization data must be Nx3")
    nps = min(int(nperseg), data.shape[0])
    if nps < 1024:
        raise D02CRefusal("insufficient samples for CSD")
    nov = min(NOVERLAP, nps // 2)
    matrix = None
    freqs = None
    for i in range(3):
        for k in range(i, 3):
            f, p = signal.csd(
                data[:, i],
                data[:, k],
                fs=FS,
                window="hann",
                nperseg=nps,
                noverlap=nov,
                detrend="constant",
                scaling="density",
                return_onesided=True,
            )
            if freqs is None:
                freqs = f
                idx = int(np.argmin(np.abs(freqs - target_frequency)))
                matrix = np.zeros((3, 3), dtype=complex)
            value = p[idx]
            matrix[i, k] = value
            matrix[k, i] = np.conjugate(value)
    matrix = 0.5 * (matrix + matrix.conj().T)
    vals, vecs = np.linalg.eigh(matrix)
    vec = vecs[:, int(np.argmax(vals))]
    norm = np.linalg.norm(vec)
    if not np.isfinite(norm) or norm <= 0:
        raise D02CRefusal("invalid CSD eigenvector")
    return vec / norm


def mac_dissimilarity(a: np.ndarray, b: np.ndarray) -> float:
    aa = np.vdot(a, a).real
    bb = np.vdot(b, b).real
    if aa <= 0 or bb <= 0:
        return math.nan
    mac = abs(np.vdot(a, b)) ** 2 / (aa * bb)
    mac = min(1.0, max(0.0, float(np.real(mac))))
    return 1.0 - mac


def reference_vector(vectors: list[np.ndarray]) -> np.ndarray:
    if len(vectors) < 2:
        raise D02CRefusal("insufficient vectors for reference")
    p = np.zeros((3, 3), dtype=complex)
    for v in vectors:
        p += np.outer(v, np.conjugate(v))
    p /= len(vectors)
    vals, vecs = np.linalg.eigh(0.5 * (p + p.conj().T))
    v = vecs[:, int(np.argmax(vals))]
    return v / np.linalg.norm(v)


def block_vectors(data: np.ndarray, target_frequency: float) -> list[np.ndarray]:
    block = int(50 * FS)
    vectors = []
    for i in range(12):
        start = i * block
        stop = start + block
        if stop > len(data):
            continue
        chunk = data[start:stop]
        try:
            vectors.append(_csd_vector(chunk, target_frequency))
        except D02CRefusal:
            continue
    return vectors


def full_and_block_vectors(data: np.ndarray, target_frequency: float) -> tuple[np.ndarray, list[np.ndarray]]:
    full = _csd_vector(data, target_frequency)
    blocks = block_vectors(data, target_frequency)
    return full, blocks


def parse_member_start(member: str) -> datetime:
    m = re.search(r"(\d{8})_(\d{6})\.csv$", member)
    if not m:
        raise D02CRefusal(f"cannot parse raw member timestamp {member}")
    dt = datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")
    return dt.replace(tzinfo=timezone.utc)


def main_raw_members(path: Path) -> list[tuple[datetime, str]]:
    with zipfile.ZipFile(path) as zf:
        items = [(parse_member_start(n), n) for n in zf.namelist() if n.lower().endswith(".csv")]
    return sorted(items)


def spatial_psd(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    psds = []
    f_ref = None
    for i in range(3):
        f, p = signal.welch(
            data[:, i],
            fs=FS,
            window="hann",
            nperseg=NPERSEG,
            noverlap=NOVERLAP,
            detrend="constant",
            scaling="density",
        )
        f_ref = f
        psds.append(p)
    return f_ref, np.mean(np.vstack(psds), axis=0)


def select_dry_peak(window1: np.ndarray, window2: np.ndarray) -> float | None:
    f1, p1 = spatial_psd(window1)
    f2, p2 = spatial_psd(window2)
    mask1 = (f1 >= 0.5) & (f1 <= 4.0)
    mask2 = (f2 >= 0.5) & (f2 <= 4.0)
    med1 = float(np.median(p1[mask1]))
    med2 = float(np.median(p2[mask2]))
    peaks1, _ = signal.find_peaks(p1[mask1], height=5.0 * med1)
    peaks2, _ = signal.find_peaks(p2[mask2], height=5.0 * med2)
    freqs1 = f1[mask1][peaks1]
    freqs2 = f2[mask2][peaks2]
    pairs = []
    for a in freqs1:
        for b in freqs2:
            if abs(a - b) <= 0.1:
                pairs.append((0.5 * (a + b), abs(a - b)))
    if not pairs:
        return None
    pairs.sort(key=lambda x: (x[0], x[1]))
    return float(pairs[0][0])


def read_dry_raw(path: Path) -> dict[str, np.ndarray]:
    with zipfile.ZipFile(path) as zf:
        members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if len(members) != 1:
            raise D02CRefusal("dry-run archive must contain one CSV")
        raw = zf.read(members[0])
    arr = np.loadtxt(
        io.BytesIO(raw),
        delimiter=",",
        skiprows=1,
        usecols=(1, 3, 4, 6, 7, 9),
        dtype=float,
    )
    if arr.ndim != 2 or arr.shape[1] != 6 or not np.all(np.isfinite(arr)):
        raise D02CRefusal("invalid dry-run raw matrix")
    needed = 12 * EXPECTED_MAIN_SAMPLES
    if arr.shape[0] < needed:
        raise D02CRefusal(f"dry-run shorter than 120 minutes: {arr.shape[0]}")
    arr = arr[:needed]
    return {
        "X": arr[:, [0, 2, 4]],
        "Z": arr[:, [1, 3, 5]],
    }


def dry_organization_threshold(data: np.ndarray) -> dict[str, Any]:
    windows = [
        data[i * EXPECTED_MAIN_SAMPLES:(i + 1) * EXPECTED_MAIN_SAMPLES]
        for i in range(12)
    ]
    target = select_dry_peak(windows[0], windows[1])
    if target is None:
        return {"status": "NON_IDENTIFIABLE"}
    first_vectors = [_csd_vector(windows[i], target) for i in (0, 1)]
    ref = reference_vector(first_vectors)
    all_blocks = []
    for w in windows:
        all_blocks.extend(block_vectors(w, target))
    if len(all_blocks) < 100:
        return {
            "status": "CONTROL_INADEQUATE",
            "target_frequency_hz": target,
            "valid_block_count": len(all_blocks),
        }
    d = [mac_dissimilarity(ref, v) for v in all_blocks]
    return {
        "status": "ADEQUATE",
        "target_frequency_hz": target,
        "valid_block_count": len(d),
        "threshold": float(np.max(d)),
        "median": float(np.median(d)),
        "q95": float(np.quantile(d, 0.95)),
    }


def parse_climate_main(path: Path) -> list[dict[str, Any]]:
    out = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            dt = None
            for key in ("t_a", "t"):
                try:
                    dt = parse_dt(row.get(key, ""))
                    break
                except Exception:
                    pass
            if dt is None:
                continue
            vals = []
            for key in ("T_left_fan", "T_right_fan"):
                try:
                    v = float(row[key])
                    if math.isfinite(v):
                        vals.append(v)
                except Exception:
                    pass
            if vals:
                out.append({"timestamp": dt, "temperature_C": float(np.mean(vals))})
    return out


def climate_window_summary(rows: list[dict[str, Any]], start: datetime) -> dict[str, Any]:
    stop = start + timedelta(minutes=10)
    vals = [r["temperature_C"] for r in rows if start <= r["timestamp"] < stop]
    if not vals:
        return {"status": "MISSING"}
    return {
        "status": "AVAILABLE",
        "median_C": float(np.median(vals)),
        "min_C": float(np.min(vals)),
        "max_C": float(np.max(vals)),
        "n": len(vals),
    }


def stage_label(start: datetime) -> str:
    hm = start.strftime("%H:%M")
    if hm == "11:20":
        return "SPRAY_ONSET_STRADDLING"
    if datetime(2022, 11, 15, 11, 30, tzinfo=timezone.utc) <= start <= datetime(2022, 11, 15, 12, 10, tzinfo=timezone.utc):
        return "SPRAY_INITIAL"
    if datetime(2022, 11, 15, 12, 20, tzinfo=timezone.utc) <= start <= datetime(2022, 11, 15, 12, 40, tzinfo=timezone.utc):
        return "SPRAY_ACCELERATED"
    if datetime(2022, 11, 15, 12, 50, tzinfo=timezone.utc) <= start <= datetime(2022, 11, 15, 13, 10, tzinfo=timezone.utc):
        return "POST_SPRAY_PRE_HEATING"
    return "UNCLASSIFIED"


def onset_index(statuses: list[str], changed: str) -> dict[str, Any]:
    for i, status in enumerate(statuses):
        if status == changed:
            if all(s == "UNCHANGED" for s in statuses[:i]):
                return {"status": "IDENTIFIABLE_CHANGE", "index": i}
            return {"status": "ORDERING_NON_IDENTIFIABLE", "index": None}
        if status == "NON_IDENTIFIABLE":
            return {"status": "ORDERING_NON_IDENTIFIABLE", "index": None}
    if all(s == "UNCHANGED" for s in statuses):
        return {"status": "IDENTIFIABLE_NO_CHANGE", "index": None}
    return {"status": "ORDERING_NON_IDENTIFIABLE", "index": None}


def classify_order(
    scalar_statuses: list[str],
    org_statuses: list[str],
    org_midnight_statuses: list[str],
) -> dict[str, Any]:
    scalar = onset_index(scalar_statuses, "TRANSFORMED")
    org = onset_index(org_statuses, "CHANGED")
    org_mid = onset_index(org_midnight_statuses, "CHANGED")

    # If dry-run thermal threshold removes/delays an otherwise favorable organization-first onset.
    if org_mid["status"] == "IDENTIFIABLE_CHANGE":
        p = org_mid["index"]
        scalar_i = scalar["index"] if scalar["status"] == "IDENTIFIABLE_CHANGE" else None
        prelim_favorable = scalar_i is None or p < scalar_i
        effective_i = org["index"] if org["status"] == "IDENTIFIABLE_CHANGE" else None
        if prelim_favorable and (effective_i is None or effective_i > p):
            return {
                "outcome": "NATIVE_MEASUREMENT_SENSITIVITY_PRECLUDES_ORDERING",
                "scalar_onset_index": scalar_i,
                "organization_onset_index": effective_i,
                "organization_midnight_only_onset_index": p,
            }

    if scalar["status"] == "ORDERING_NON_IDENTIFIABLE" or org["status"] == "ORDERING_NON_IDENTIFIABLE":
        return {
            "outcome": "ORDERING_NON_IDENTIFIABLE",
            "scalar_onset_index": scalar.get("index"),
            "organization_onset_index": org.get("index"),
        }

    s_change = scalar["status"] == "IDENTIFIABLE_CHANGE"
    o_change = org["status"] == "IDENTIFIABLE_CHANGE"
    si = scalar["index"]
    oi = org["index"]

    if s_change and o_change:
        if oi < si:
            outcome = "ORGANIZATION_PRECEDES_SCALAR"
        elif si < oi:
            outcome = "SCALAR_PRECEDES_ORGANIZATION"
        else:
            outcome = "SIMULTANEOUS_WITHIN_FROZEN_RESOLUTION"
    elif o_change and not s_change:
        outcome = "ORGANIZATION_CHANGES_SCALAR_DOES_NOT"
    elif s_change and not o_change:
        outcome = "SCALAR_CHANGES_ORGANIZATION_DOES_NOT"
    else:
        outcome = "NEITHER_CHANGES"

    return {
        "outcome": outcome,
        "scalar_onset_index": si,
        "organization_onset_index": oi,
    }


def run_d02c(cache_dir: Path) -> dict[str, Any]:
    sources = {role: fetch_asset(role, cache_dir) for role in ASSETS}

    rows = {
        "X": load_modal_rows(Path(sources["modal_x"]["path"])),
        "Z": load_modal_rows(Path(sources["modal_z"]["path"])),
    }

    baseline_starts = [
        datetime(2022, 11, 15, 0, 0, tzinfo=timezone.utc) + timedelta(minutes=10 * i)
        for i in range(12)
    ]
    baseline_midpoints = [x + timedelta(minutes=5) for x in baseline_starts]
    intervention_starts = [
        datetime(2022, 11, 15, 11, 20, tzinfo=timezone.utc) + timedelta(minutes=10 * i)
        for i in range(12)
    ]
    intervention_midpoints = [x + timedelta(minutes=5) for x in intervention_starts]

    selected_tracks = {}
    intervention_tracks = {}
    scalar_envelopes = {}
    for direction in ("X", "Z"):
        track = build_baseline_track(rows[direction], baseline_midpoints)
        selected_tracks[direction] = track
        prespray = prespray_track(
            rows[direction],
            datetime(2022, 11, 15, 0, 0, tzinfo=timezone.utc),
            datetime(2022, 11, 15, 11, 20, tzinfo=timezone.utc),
            track["median_frequency"],
        )
        scalar_envelopes[direction] = scalar_control_envelope(track["rows"], prespray)
        initial = prespray[-1]["frequency"] if prespray else track["median_frequency"]
        intervention_tracks[direction] = sequential_track(
            rows[direction],
            intervention_midpoints,
            initial,
        )

    # Raw file maps.
    baseline_members = main_raw_members(Path(sources["raw_baseline"]["path"]))
    intervention_members = main_raw_members(Path(sources["raw_intervention"]["path"]))
    if [x[0] for x in baseline_members] != baseline_starts:
        raise D02CRefusal("baseline raw timestamps do not match frozen list")
    if [x[0] for x in intervention_members] != intervention_starts:
        raise D02CRefusal("intervention raw timestamps do not match frozen list")

    baseline_full_vectors = {"X": [], "Z": []}
    baseline_block_vectors = {"X": [], "Z": []}

    with zipfile.ZipFile(sources["raw_baseline"]["path"]) as zf:
        for i, (start, member) in enumerate(baseline_members):
            matrix = read_main_raw_member(zf, member)
            for direction in ("X", "Z"):
                row = selected_tracks[direction]["rows"][i]
                if row is None:
                    baseline_full_vectors[direction].append(None)
                    continue
                full, blocks = full_and_block_vectors(matrix[direction], row["frequency"])
                baseline_full_vectors[direction].append(full)
                baseline_block_vectors[direction].extend(blocks)

    refs = {}
    midnight_thresholds = {}
    for direction in ("X", "Z"):
        fulls = [v for v in baseline_full_vectors[direction] if v is not None]
        if len(fulls) < 10 or len(baseline_block_vectors[direction]) < 100:
            raise D02CRefusal(f"organization baseline inadequate for {direction}")
        ref = reference_vector(fulls)
        refs[direction] = ref
        d = [mac_dissimilarity(ref, v) for v in baseline_block_vectors[direction]]
        midnight_thresholds[direction] = {
            "valid_full_window_count": len(fulls),
            "valid_block_count": len(d),
            "threshold": float(np.max(d)),
            "median": float(np.median(d)),
            "q95": float(np.quantile(d, 0.95)),
        }

    dry_data = read_dry_raw(Path(sources["raw_dry"]["path"]))
    dry_thresholds = {
        direction: dry_organization_threshold(dry_data[direction])
        for direction in ("X", "Z")
    }

    effective_thresholds = {}
    for direction in ("X", "Z"):
        dry = dry_thresholds[direction]
        if dry.get("status") != "ADEQUATE":
            effective_thresholds[direction] = {
                "status": "DRY_CONTROL_INADEQUATE",
                "threshold": None,
            }
        else:
            effective_thresholds[direction] = {
                "status": "ADEQUATE",
                "threshold": max(
                    midnight_thresholds[direction]["threshold"],
                    dry["threshold"],
                ),
                "midnight_threshold": midnight_thresholds[direction]["threshold"],
                "dry_threshold": dry["threshold"],
            }

    climate = parse_climate_main(Path(sources["climate_main"]["path"]))

    trajectories = {"X": [], "Z": []}
    with zipfile.ZipFile(sources["raw_intervention"]["path"]) as zf:
        for i, (start, member) in enumerate(intervention_members):
            matrix = read_main_raw_member(zf, member)
            for direction in ("X", "Z"):
                row = intervention_tracks[direction][i]
                scalar = scalar_from_row(row)
                scalar_status = scalar_change_status(scalar, scalar_envelopes[direction])

                if row is None:
                    org_record = {
                        "status": "NON_IDENTIFIABLE",
                        "block_count": 0,
                    }
                    midnight_only_status = "NON_IDENTIFIABLE"
                else:
                    try:
                        full, blocks = full_and_block_vectors(matrix[direction], row["frequency"])
                        d = [mac_dissimilarity(refs[direction], v) for v in blocks]
                        if len(d) < 10:
                            org_record = {
                                "status": "NON_IDENTIFIABLE",
                                "block_count": len(d),
                            }
                            midnight_only_status = "NON_IDENTIFIABLE"
                        else:
                            q025 = float(np.quantile(d, 0.025))
                            full_d = mac_dissimilarity(refs[direction], full)
                            eff = effective_thresholds[direction]
                            if eff["status"] != "ADEQUATE":
                                org_status = "NON_IDENTIFIABLE"
                            else:
                                org_status = "CHANGED" if q025 > eff["threshold"] else "UNCHANGED"
                            midnight_only_status = (
                                "CHANGED"
                                if q025 > midnight_thresholds[direction]["threshold"]
                                else "UNCHANGED"
                            )
                            org_record = {
                                "status": org_status,
                                "block_count": len(d),
                                "full_window_dissimilarity": float(full_d),
                                "block_q025": q025,
                                "block_median": float(np.median(d)),
                                "block_q975": float(np.quantile(d, 0.975)),
                                "effective_threshold": eff.get("threshold"),
                            }
                    except D02CRefusal:
                        org_record = {
                            "status": "NON_IDENTIFIABLE",
                            "block_count": 0,
                        }
                        midnight_only_status = "NON_IDENTIFIABLE"

                trajectories[direction].append({
                    "index": i,
                    "window_start": start.isoformat(),
                    "window_midpoint": intervention_midpoints[i].isoformat(),
                    "stage": stage_label(start),
                    "temperature": climate_window_summary(climate, start),
                    "matched_frequency_hz": None if row is None else float(row["frequency"]),
                    "scalar": scalar,
                    "scalar_change_status": scalar_status,
                    "organization": org_record,
                    "organization_midnight_only_status": midnight_only_status,
                })

    orderings = {}
    for direction in ("X", "Z"):
        scalar_statuses = [r["scalar_change_status"] for r in trajectories[direction]]
        org_statuses = [r["organization"]["status"] for r in trajectories[direction]]
        org_mid = [r["organization_midnight_only_status"] for r in trajectories[direction]]
        ordering = classify_order(scalar_statuses, org_statuses, org_mid)
        for key in ("scalar_onset_index", "organization_onset_index", "organization_midnight_only_onset_index"):
            if key in ordering and ordering[key] is not None:
                ordering[key.replace("_index", "_window_start")] = trajectories[direction][ordering[key]]["window_start"]
        orderings[direction] = ordering

    favorable = {"ORGANIZATION_PRECEDES_SCALAR", "ORGANIZATION_CHANGES_SCALAR_DOES_NOT"}
    opposite = "SCALAR_PRECEDES_ORGANIZATION"
    support = (
        any(orderings[d]["outcome"] in favorable for d in ("X", "Z"))
        and not any(orderings[d]["outcome"] == opposite for d in ("X", "Z"))
    )

    return {
        "schema": "d02c-wind-blade-prospective-result-v0.1",
        "status": "D02C_PROSPECTIVE_EXECUTED",
        "evidence_class": "PROSPECTIVE_EXTERNAL_PHYSICAL_DOMAIN_SPECIFIC",
        "source_record": "10.5281/zenodo.18427836",
        "source_files": {
            role: {
                k: rec[k]
                for k in ("filename", "size_bytes", "md5", "sha256", "url")
            }
            for role, rec in sources.items()
        },
        "selected_modes": {
            d: {
                "baseline_presence": selected_tracks[d]["presence"],
                "baseline_median_frequency_hz": selected_tracks[d]["median_frequency"],
            }
            for d in ("X", "Z")
        },
        "scalar_control_envelopes": scalar_envelopes,
        "organization_midnight_thresholds": midnight_thresholds,
        "organization_dry_thresholds": dry_thresholds,
        "organization_effective_thresholds": effective_thresholds,
        "trajectories": trajectories,
        "orderings": orderings,
        "ca_d007_domain_specific_support": bool(support),
        "native_toolkit_verdict_preinterpretation": "NOT_ASSIGNED_BY_RUNNER",
        "scope": (
            "Prospectively frozen external physical D02C test of CA-D007. "
            "No universal ordering or new native dynamics are implied."
        ),
    }
