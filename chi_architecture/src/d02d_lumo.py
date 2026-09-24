from __future__ import annotations

import hashlib
import io
import json
import math
from pathlib import Path
from typing import Any
import zipfile

import numpy as np
import requests
from scipy.io import loadmat
from scipy.signal import find_peaks, get_window


FS_EXPECTED = 1651.6129032258063
SAMPLE_COUNT_EXPECTED = 990600
BLOCK_LEN = 328671
NPERSEG = 32768
NOVERLAP = 16384
FMIN = 0.3
FMAX = 10.0
TRACK_HALF_WIDTH = 0.15
PEAK_MIN_SEP_HZ = 0.20
MODE_PROMINENCE = 5.0
BOOTSTRAP_N = 5000

HEADERS = {
    "User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"
}

RESOURCES = {
    ("DAM3", "010"): {
        "url": "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/37be937f-8e16-414e-9fd4-92d59196417c/download/exemplary_datasets_dam3_010.zip",
        "expected_size": 559776282,
    },
    ("DAM3", "111"): {
        "url": "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/78da8221-a6bb-4ad9-9f53-e3d9164b3c52/download/exemplary_datasets_dam3_111.zip",
        "expected_size": 638712761,
    },
    ("DAM4", "010"): {
        "url": "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/1f56230e-3f8e-4347-90a1-08bdb3cd4872/download/exemplary_datasets_dam4_010.zip",
        "expected_size": 629562821,
    },
    ("DAM4", "111"): {
        "url": "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/83ee4ee4-d86b-49ce-92dd-743bd779d845/download/exemplary_datasets_dam4_111.zip",
        "expected_size": 665801542,
    },
    ("DAM6", "010"): {
        "url": "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/6b497c7b-48c3-4c5d-9d08-c3f37ff92122/download/exemplary_datasets_dam6_010.zip",
        "expected_size": 643610180,
    },
    ("DAM6", "111"): {
        "url": "https://data.uni-hannover.de/dataset/93b52576-6a5a-4ce9-8c27-a0372590f7b0/resource/d9661b47-1f25-4194-99e8-6805fcd5810e/download/exemplary_datasets_dam6_111.zip",
        "expected_size": 680154659,
    },
}

DIRECTION_CHANNELS = {
    "X": [f"accel{i:02d}x" for i in range(1, 10)],
    "Y": [f"accel{i:02d}y" for i in range(1, 10)],
}


class D02DRefusal(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_resource(location: str, severity: str, cache_dir: Path) -> dict[str, Any]:
    spec = RESOURCES[(location, severity)]
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{location}_{severity}.zip"
    if not path.exists() or path.stat().st_size != int(spec["expected_size"]):
        with requests.get(spec["url"], headers=HEADERS, stream=True, timeout=1200) as r:
            r.raise_for_status()
            with path.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                    if chunk:
                        f.write(chunk)
    if path.stat().st_size != int(spec["expected_size"]):
        raise D02DRefusal(
            f"size mismatch for {location} {severity}: "
            f"{path.stat().st_size} != {spec['expected_size']}"
        )
    return {
        "path": path,
        "url": spec["url"],
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def list_campaign_members(zf: zipfile.ZipFile) -> tuple[list[str], list[str]]:
    mats = [x for x in zf.namelist() if x.lower().endswith(".mat")]
    healthy = sorted(
        x for x in mats
        if any("healthy" in part.lower() for part in x.replace("\\", "/").split("/")[:-1])
    )
    damaged = sorted(x for x in mats if x not in healthy)
    if len(healthy) != 5 or len(damaged) != 5:
        raise D02DRefusal(f"expected 5 healthy + 5 damaged MAT files, got {len(healthy)} + {len(damaged)}")
    return healthy, damaged


def load_record(zf: zipfile.ZipFile, member: str) -> dict[str, Any]:
    raw = zf.read(member)
    mat = loadmat(io.BytesIO(raw), variable_names=["Dat"], squeeze_me=True, struct_as_record=False)
    if "Dat" not in mat:
        raise D02DRefusal(f"Dat missing in {member}")
    dat = mat["Dat"]
    fs = float(dat.Fs)
    data = np.asarray(dat.Data, dtype=np.float64)
    names = [str(x) for x in np.asarray(dat.ChannelNames).reshape(-1).tolist()]
    if abs(fs - FS_EXPECTED) > 1e-9:
        raise D02DRefusal(f"sampling-rate mismatch in {member}: {fs}")
    if not (0.99 * SAMPLE_COUNT_EXPECTED <= data.shape[0] <= 1.01 * SAMPLE_COUNT_EXPECTED):
        raise D02DRefusal(f"sample-count refusal in {member}: {data.shape}")
    if data.shape[1] != len(names):
        raise D02DRefusal(f"channel metadata mismatch in {member}")
    return {
        "member": member,
        "time": str(dat.Time),
        "fs": fs,
        "data": data,
        "channel_names": names,
    }


def channel_indices(names: list[str], direction: str) -> tuple[list[int], int]:
    required = DIRECTION_CHANNELS[direction]
    missing = [x for x in required if x not in names]
    if missing:
        raise D02DRefusal(f"missing {direction} channels: {missing}")
    if "temp01" not in names:
        raise D02DRefusal("temp01 missing")
    return [names.index(x) for x in required], names.index("temp01")


def split_blocks(record: dict[str, Any], direction: str) -> list[dict[str, Any]]:
    data = record["data"]
    idx, temp_idx = channel_indices(record["channel_names"], direction)
    out = []
    for block_id in range(3):
        start = block_id * BLOCK_LEN
        stop = start + BLOCK_LEN
        x = np.asarray(data[start:stop, idx], dtype=np.float64)
        temp = np.asarray(data[start:stop, temp_idx], dtype=np.float64)
        if x.shape != (BLOCK_LEN, 9):
            raise D02DRefusal("unexpected block shape")
        valid = bool(np.isfinite(x).all() and np.isfinite(temp).all())
        if not valid:
            out.append({
                "record": record["member"],
                "block_id": block_id,
                "raw_valid": False,
            })
            continue
        x = x - np.mean(x, axis=0, keepdims=True)
        rms = float(np.sqrt(np.mean(x * x)))
        if not math.isfinite(rms) or rms <= 0.0:
            out.append({
                "record": record["member"],
                "block_id": block_id,
                "raw_valid": False,
            })
            continue
        out.append({
            "record": record["member"],
            "block_id": block_id,
            "raw_valid": True,
            "x": x,
            "temperature_c": float(np.median(temp)),
            "log_rms": float(np.log(rms)),
        })
    return out


def fdd(block: np.ndarray, fs: float) -> dict[str, np.ndarray]:
    n = block.shape[0]
    if n < NPERSEG:
        raise D02DRefusal("block shorter than nperseg")
    step = NPERSEG - NOVERLAP
    starts = range(0, n - NPERSEG + 1, step)
    win = get_window("hann", NPERSEG, fftbins=True).astype(np.float64)
    freqs_all = np.fft.rfftfreq(NPERSEG, d=1.0 / fs)
    mask = (freqs_all >= FMIN) & (freqs_all <= FMAX)
    freqs = freqs_all[mask]
    csd = np.zeros((freqs.size, 9, 9), dtype=np.complex128)
    count = 0
    for start in starts:
        seg = block[start:start + NPERSEG]
        seg = seg - np.mean(seg, axis=0, keepdims=True)
        xf = np.fft.rfft(seg * win[:, None], axis=0)[mask]
        csd += np.einsum("fi,fj->fij", np.conjugate(xf), xf, optimize=True)
        count += 1
    if count < 3:
        raise D02DRefusal("insufficient spectral segments")
    csd /= float(count)
    eigvals = np.linalg.eigvalsh(csd)
    s1 = np.maximum(eigvals[:, -1].real, 0.0)
    return {"freqs": freqs, "s1": s1, "csd": csd}


def preprocess_blocks(blocks: list[dict[str, Any]], fs: float) -> None:
    for block in blocks:
        if not block.get("raw_valid"):
            continue
        out = fdd(block.pop("x"), fs)
        block.update(out)


def local_peaks(freqs: np.ndarray, s1: np.ndarray, center: float, half_width: float) -> np.ndarray:
    mask = (freqs >= center - half_width) & (freqs <= center + half_width)
    inds = np.where(mask)[0]
    if inds.size < 3:
        return np.array([], dtype=int)
    p, _ = find_peaks(s1[inds])
    return inds[p]


def select_family(healthy_blocks: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [b for b in healthy_blocks if b.get("raw_valid") and "s1" in b]
    if len(valid) < 24:
        return {"status": "MODE_FAMILY_NON_IDENTIFIABLE", "reason": "healthy_block_floor"}
    freqs = valid[0]["freqs"]
    norms = []
    for b in valid:
        median = float(np.median(b["s1"]))
        if median <= 0:
            continue
        norms.append(b["s1"] / median)
    if len(norms) < 24:
        return {"status": "MODE_FAMILY_NON_IDENTIFIABLE", "reason": "spectrum_floor"}
    median_spec = np.median(np.vstack(norms), axis=0)
    df = float(np.median(np.diff(freqs)))
    distance = max(1, int(math.ceil(PEAK_MIN_SEP_HZ / df)))
    candidates, props = find_peaks(median_spec, prominence=MODE_PROMINENCE, distance=distance)
    for idx in candidates:
        center = float(freqs[idx])
        presence = 0
        for b in valid:
            peaks = local_peaks(b["freqs"], b["s1"], center, TRACK_HALF_WIDTH)
            if peaks.size:
                presence += 1
        if presence >= 24:
            return {
                "status": "IDENTIFIED",
                "frequency_hz": center,
                "healthy_presence": presence,
                "healthy_block_count": len(valid),
                "median_normalized_peak": float(median_spec[idx]),
            }
    return {
        "status": "MODE_FAMILY_NON_IDENTIFIABLE",
        "reason": "no_candidate_passed",
        "candidate_count": int(len(candidates)),
    }


def interpolate_crossing(f0: float, y0: float, f1: float, y1: float, target: float) -> float:
    if y1 == y0:
        return 0.5 * (f0 + f1)
    return float(f0 + (target - y0) * (f1 - f0) / (y1 - y0))


def track_block(block: dict[str, Any], f_ref: float) -> dict[str, Any]:
    if not block.get("raw_valid") or "s1" not in block:
        return {"status": "RAW_BLOCK_INVALID"}
    freqs = block["freqs"]
    s1 = block["s1"]
    peaks = local_peaks(freqs, s1, f_ref, TRACK_HALF_WIDTH)
    if peaks.size == 0:
        return {"status": "MODE_NON_IDENTIFIABLE"}
    nearest_order = sorted(peaks.tolist(), key=lambda i: abs(float(freqs[i]) - f_ref))
    pick = int(nearest_order[0])
    if len(nearest_order) > 1:
        second = int(nearest_order[1])
        if float(s1[second]) >= 0.90 * float(s1[pick]):
            return {"status": "MODAL_OVERLAP_NON_IDENTIFIABLE"}
    peak_f = float(freqs[pick])
    peak = float(s1[pick])
    vals, vecs = np.linalg.eigh(block["csd"][pick])
    vec = np.asarray(vecs[:, -1], dtype=np.complex128)
    vec /= np.linalg.norm(vec)
    base = {
        "status": "TRACKED",
        "peak_hz": peak_f,
        "peak_psd": peak,
        "mode_vector": vec,
    }

    inds = np.where((freqs >= f_ref - TRACK_HALF_WIDTH) & (freqs <= f_ref + TRACK_HALF_WIDTH))[0]
    if inds.size < 3 or pick == inds[0] or pick == inds[-1]:
        return {**base, "scalar_status": "WINDOW_TRUNCATED"}
    threshold = peak / 2.0
    pos = int(np.where(inds == pick)[0][0])
    left_pos = pos
    while left_pos > 0 and float(s1[inds[left_pos]]) >= threshold:
        left_pos -= 1
    if left_pos == 0 and float(s1[inds[left_pos]]) >= threshold:
        return {**base, "scalar_status": "HALF_POWER_CROSSING_NOT_OBSERVED"}
    right_pos = pos
    while right_pos < len(inds) - 1 and float(s1[inds[right_pos]]) >= threshold:
        right_pos += 1
    if right_pos == len(inds) - 1 and float(s1[inds[right_pos]]) >= threshold:
        return {**base, "scalar_status": "HALF_POWER_CROSSING_NOT_OBSERVED"}

    il0, il1 = inds[left_pos], inds[left_pos + 1]
    ir0, ir1 = inds[right_pos - 1], inds[right_pos]
    fl = interpolate_crossing(float(freqs[il0]), float(s1[il0]), float(freqs[il1]), float(s1[il1]), threshold)
    fr = interpolate_crossing(float(freqs[ir0]), float(s1[ir0]), float(freqs[ir1]), float(s1[ir1]), threshold)
    bw = fr - fl
    if not math.isfinite(bw) or bw <= 0:
        return {**base, "scalar_status": "NO_ADMISSIBLE_SCALAR_CHI"}
    chi = bw / (2.0 * peak_f)
    return {
        **base,
        "scalar_status": "ADMITTED",
        "half_power_left_hz": fl,
        "half_power_right_hz": fr,
        "bandwidth_hz": bw,
        "chi": float(chi),
    }


def projective_reference(vectors: list[np.ndarray]) -> np.ndarray:
    if len(vectors) < 1:
        raise D02DRefusal("no vectors for reference")
    dim = int(np.asarray(vectors[0]).size)
    if dim < 1 or any(int(np.asarray(v).size) != dim for v in vectors):
        raise D02DRefusal("projective reference requires equal nonzero vector dimensions")
    p = np.zeros((dim, dim), dtype=np.complex128)
    for v in vectors:
        v = np.asarray(v, dtype=np.complex128).reshape(-1)
        p += np.outer(v, np.conjugate(v))
    p /= float(len(vectors))
    vals, vecs = np.linalg.eigh(p)
    ref = np.asarray(vecs[:, -1], dtype=np.complex128)
    return ref / np.linalg.norm(ref)


def dorg(ref: np.ndarray, vec: np.ndarray) -> float:
    return float(max(0.0, min(1.0, 1.0 - abs(np.vdot(ref, vec)) ** 2)))


def bootstrap_median_ci(values: list[float], seed: int) -> tuple[float, float, float]:
    x = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, x.size, size=(BOOTSTRAP_N, x.size))
    meds = np.median(x[idx], axis=1)
    return float(np.median(x)), float(np.quantile(meds, 0.025)), float(np.quantile(meds, 0.975))


def evaluate_campaign(
    healthy_blocks: list[dict[str, Any]],
    damaged_blocks: list[dict[str, Any]],
    f_ref: float,
    seed: int,
) -> dict[str, Any]:
    htracks = [track_block(b, f_ref) for b in healthy_blocks]
    dtracks = [track_block(b, f_ref) for b in damaged_blocks]

    raw_h = [b for b in healthy_blocks if b.get("raw_valid")]
    if len(raw_h) < 10:
        return {"status": "NON_IDENTIFIABLE", "reason": "healthy_raw_floor"}

    tmin = min(float(b["temperature_c"]) for b in raw_h)
    tmax = max(float(b["temperature_c"]) for b in raw_h)
    rmin = min(float(b["log_rms"]) for b in raw_h)
    rmax = max(float(b["log_rms"]) for b in raw_h)

    matched = [
        bool(
            b.get("raw_valid")
            and tmin <= float(b["temperature_c"]) <= tmax
            and rmin <= float(b["log_rms"]) <= rmax
        )
        for b in damaged_blocks
    ]

    hchi = [
        float(t["chi"]) for t in htracks
        if t.get("scalar_status") == "ADMITTED"
    ]
    dchi = [
        float(t["chi"]) for t, keep in zip(dtracks, matched)
        if keep and t.get("scalar_status") == "ADMITTED"
    ]

    if len(hchi) >= 10 and len(dchi) >= 10:
        med, lo, hi = bootstrap_median_ci(dchi, seed)
        h_lo, h_hi = min(hchi), max(hchi)
        scalar_status = "TRANSFORMED" if (hi < h_lo or lo > h_hi) else "UNCHANGED"
        scalar = {
            "status": scalar_status,
            "healthy_n": len(hchi),
            "damage_n": len(dchi),
            "healthy_envelope": [h_lo, h_hi],
            "damage_median": med,
            "damage_median_ci95": [lo, hi],
        }
    else:
        scalar = {
            "status": "NON_IDENTIFIABLE",
            "healthy_n": len(hchi),
            "damage_n": len(dchi),
        }

    hvectors = [
        t["mode_vector"] for t in htracks
        if t.get("status") == "TRACKED" and "mode_vector" in t
    ]
    dvectors = [
        t["mode_vector"] for t, keep in zip(dtracks, matched)
        if keep and t.get("status") == "TRACKED" and "mode_vector" in t
    ]
    if len(hvectors) >= 10 and len(dvectors) >= 10:
        ref = projective_reference(hvectors)
        hd = [dorg(ref, v) for v in hvectors]
        dd = [dorg(ref, v) for v in dvectors]
        threshold = max(hd)
        q025 = float(np.quantile(dd, 0.025))
        org_status = "CHANGED" if q025 > threshold else "UNCHANGED"
        organization = {
            "status": org_status,
            "healthy_n": len(hvectors),
            "damage_n": len(dvectors),
            "healthy_threshold": float(threshold),
            "damage_q025": q025,
            "damage_median": float(np.median(dd)),
            "damage_max": float(np.max(dd)),
        }
    else:
        organization = {
            "status": "NON_IDENTIFIABLE",
            "healthy_n": len(hvectors),
            "damage_n": len(dvectors),
        }

    return {
        "status": "EVALUATED",
        "environment": {
            "healthy_temperature_range_c": [tmin, tmax],
            "healthy_log_rms_range": [rmin, rmax],
            "matched_damage_blocks": int(sum(matched)),
            "total_damage_blocks": len(damaged_blocks),
        },
        "scalar": scalar,
        "organization": organization,
        "track_status_counts": {
            "healthy": {
                key: sum(1 for x in htracks if x.get("scalar_status", x.get("status")) == key)
                for key in sorted({x.get("scalar_status", x.get("status")) for x in htracks})
            },
            "damage": {
                key: sum(1 for x in dtracks if x.get("scalar_status", x.get("status")) == key)
                for key in sorted({x.get("scalar_status", x.get("status")) for x in dtracks})
            },
        },
    }


def classify_direction(c010: dict[str, Any], c111: dict[str, Any]) -> str:
    if c010.get("status") != "EVALUATED" or c111.get("status") != "EVALUATED":
        return "ORDERING_NON_IDENTIFIABLE"
    s010 = c010["scalar"]["status"]
    o010 = c010["organization"]["status"]
    s111 = c111["scalar"]["status"]
    o111 = c111["organization"]["status"]
    if "NON_IDENTIFIABLE" in (s010, o010, s111, o111):
        return "ORDERING_NON_IDENTIFIABLE"
    if o010 == "CHANGED" and s010 == "UNCHANGED":
        if s111 == "TRANSFORMED":
            return "ORGANIZATION_PRECEDES_SCALAR"
        if s111 == "UNCHANGED":
            return "ORGANIZATION_ONLY_THROUGH_111"
    if s010 == "TRANSFORMED" and o010 == "UNCHANGED":
        if o111 == "CHANGED":
            return "SCALAR_PRECEDES_ORGANIZATION"
        if o111 == "UNCHANGED":
            return "SCALAR_ONLY_THROUGH_111"
    if o010 == "CHANGED" and s010 == "TRANSFORMED":
        return "SIMULTANEOUS_AT_010"
    if o010 == "UNCHANGED" and s010 == "UNCHANGED":
        if o111 == "CHANGED" and s111 == "TRANSFORMED":
            return "SIMULTANEOUS_AT_111"
        if o111 == "UNCHANGED" and s111 == "UNCHANGED":
            return "NEITHER_CHANGES"
        if o111 == "CHANGED" and s111 == "UNCHANGED":
            return "ORGANIZATION_ONLY_THROUGH_111"
        if o111 == "UNCHANGED" and s111 == "TRANSFORMED":
            return "SCALAR_ONLY_THROUGH_111"
    return "ORDERING_NON_IDENTIFIABLE"


def classify_location(x_class: str, y_class: str) -> str:
    if x_class == "ORDERING_NON_IDENTIFIABLE" or y_class == "ORDERING_NON_IDENTIFIABLE":
        return "ORDERING_NON_IDENTIFIABLE"
    return x_class if x_class == y_class else "ORDERING_NON_IDENTIFIABLE"


def adjudicate(location_classes: dict[str, str]) -> str:
    adequate = [x for x in location_classes.values() if x != "ORDERING_NON_IDENTIFIABLE"]
    supportive = {"ORGANIZATION_PRECEDES_SCALAR", "ORGANIZATION_ONLY_THROUGH_111"}
    n_support = sum(x in supportive for x in adequate)
    n_scalar_first = sum(x == "SCALAR_PRECEDES_ORGANIZATION" for x in adequate)
    if n_support >= 2 and n_scalar_first == 0:
        return "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST"
    if n_scalar_first >= 2:
        return "EMPIRICAL_CLAIM_FALSIFIED"
    if len(adequate) == 3 and n_support == 0 and all(
        x in {"SCALAR_PRECEDES_ORGANIZATION", "SIMULTANEOUS_AT_010", "SIMULTANEOUS_AT_111"}
        for x in adequate
    ):
        return "EMPIRICAL_CLAIM_FALSIFIED"
    return "INDETERMINATE"


def process_archive(path: Path, direction: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    with zipfile.ZipFile(path) as zf:
        healthy_members, damaged_members = list_campaign_members(zf)
        healthy_blocks: list[dict[str, Any]] = []
        damaged_blocks: list[dict[str, Any]] = []
        for member in healthy_members:
            record = load_record(zf, member)
            blocks = split_blocks(record, direction)
            preprocess_blocks(blocks, record["fs"])
            healthy_blocks.extend(blocks)
            del record
        for member in damaged_members:
            record = load_record(zf, member)
            blocks = split_blocks(record, direction)
            preprocess_blocks(blocks, record["fs"])
            damaged_blocks.extend(blocks)
            del record
    return healthy_blocks, damaged_blocks


def run_d02d(cache_dir: Path) -> dict[str, Any]:
    sources: dict[str, Any] = {}
    outputs: dict[str, Any] = {}
    location_classes: dict[str, str] = {}

    for loc_index, location in enumerate(("DAM3", "DAM4", "DAM6"), start=1):
        archives = {}
        for severity in ("010", "111"):
            src = fetch_resource(location, severity, cache_dir)
            sources[f"{location}_{severity}"] = {
                k: (str(v) if isinstance(v, Path) else v)
                for k, v in src.items() if k != "path"
            }
            archives[severity] = src["path"]

        loc_result = {"directions": {}}
        direction_classes = {}
        for dir_index, direction in enumerate(("X", "Y"), start=1):
            healthy010, damage010 = process_archive(archives["010"], direction)
            healthy111, damage111 = process_archive(archives["111"], direction)
            family = select_family(healthy010 + healthy111)
            if family["status"] != "IDENTIFIED":
                direction_class = "ORDERING_NON_IDENTIFIABLE"
                loc_result["directions"][direction] = {
                    "family": family,
                    "ordering": direction_class,
                }
                direction_classes[direction] = direction_class
                continue
            f_ref = float(family["frequency_hz"])
            c010 = evaluate_campaign(
                healthy010,
                damage010,
                f_ref,
                20260923 + 100 * loc_index + 10 * 1 + dir_index,
            )
            c111 = evaluate_campaign(
                healthy111,
                damage111,
                f_ref,
                20260923 + 100 * loc_index + 10 * 2 + dir_index,
            )
            direction_class = classify_direction(c010, c111)
            loc_result["directions"][direction] = {
                "family": family,
                "severity_010": c010,
                "severity_111": c111,
                "ordering": direction_class,
            }
            direction_classes[direction] = direction_class

        loc_class = classify_location(direction_classes["X"], direction_classes["Y"])
        loc_result["ordering"] = loc_class
        outputs[location] = loc_result
        location_classes[location] = loc_class

    outcome = adjudicate(location_classes)
    return {
        "schema": "d02d-lumo-prospective-result-v0.1",
        "status": "D02D_PROSPECTIVE_EXECUTED",
        "claim_id": "CA-D007-D02D-LUMO-v0.1",
        "dataset_doi": "10.25835/0027803",
        "source_files": sources,
        "analysis": {
            "sampling_rate_hz": FS_EXPECTED,
            "block_len": BLOCK_LEN,
            "nperseg": NPERSEG,
            "noverlap": NOVERLAP,
            "frequency_band_hz": [FMIN, FMAX],
            "track_half_width_hz": TRACK_HALF_WIDTH,
            "bootstrap_n": BOOTSTRAP_N,
        },
        "locations": outputs,
        "location_orderings": location_classes,
        "outcome": outcome,
        "native_toolkit_verdict": "NATIVE_TOOLKIT_SUFFICIENT_NO_INCREMENTAL_VALUE",
        "scope": "Prospectively frozen external physical test of CA-D007 under GOM v0.8.4 MFR-14.",
    }
