from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import zipfile

import numpy as np
import requests


ZENODO_BASE = "https://zenodo.org/records/20038951/files/"
ASSETS = {
    "documentation": ("01_documentation.zip", "3eb96c388b4811380ab86af9bb4be1ad"),
    "processed": ("02_processed_tables.zip", "a8261869e61e2c41b799360f344b4394"),
    "raw": ("00_raw_exports.zip", "68450ff0f1c25492ee243b8adba29991"),
}
HEADERS = {
    "User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"
}


class D02BRefusal(RuntimeError):
    pass


def file_hash(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_asset(role: str, cache_dir: Path) -> dict:
    if role not in ASSETS:
        raise D02BRefusal(f"unknown source role: {role}")
    name, expected_md5 = ASSETS[role]
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / name

    valid = path.exists() and file_hash(path, "md5") == expected_md5
    if not valid:
        url = ZENODO_BASE + name + "?download=1"
        with requests.get(url, headers=HEADERS, stream=True, timeout=900) as r:
            r.raise_for_status()
            with path.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                    if chunk:
                        f.write(chunk)

    actual_md5 = file_hash(path, "md5")
    if actual_md5 != expected_md5:
        raise D02BRefusal(f"MD5 mismatch for {name}: {actual_md5}")

    return {
        "role": role,
        "filename": name,
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "md5": actual_md5,
        "sha256": file_hash(path, "sha256"),
        "url": ZENODO_BASE + name + "?download=1",
    }


def _read_csv_from_zip(zf: zipfile.ZipFile, member: str) -> list[dict[str, str]]:
    text = zf.read(member).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def load_support_tables(documentation_zip: Path, processed_zip: Path) -> dict:
    with zipfile.ZipFile(documentation_zip) as doc, zipfile.ZipFile(processed_zip) as proc:
        torque = _read_csv_from_zip(doc, "01_documentation/torque_states.csv")
        audit = _read_csv_from_zip(proc, "02_processed_tables/resonance_group_selection_audit.csv")
        windows = _read_csv_from_zip(proc, "02_processed_tables/adaptive_tracking_windows.csv")
        tracked = _read_csv_from_zip(proc, "02_processed_tables/tracked_frequencies.csv")
        per_case = _read_csv_from_zip(proc, "02_processed_tables/per_case_metrics.csv")
        dose = _read_csv_from_zip(proc, "02_processed_tables/dose_response.csv")

    retained = [
        row for row in audit
        if str(row["retained"]).strip().lower() in {"true", "1", "yes"}
    ]
    if len(retained) != 7 or len(windows) != 7:
        raise D02BRefusal("source retained-family count is not seven")
    if len(torque) != 18:
        raise D02BRefusal("source torque-state count is not eighteen")

    return {
        "torque_states": torque,
        "retained": retained,
        "windows": windows,
        "tracked": tracked,
        "per_case": per_case,
        "dose": dose,
    }


def parse_response_member(path: str) -> tuple[str, str, int] | None:
    normalized = path.replace("\\", "/")
    if "/Amplitude/" in normalized:
        kind = "Amplitude"
    elif "/Phase/" in normalized:
        kind = "Phase"
    else:
        return None

    stem = normalized.rsplit("/", 1)[-1]
    if not stem.endswith(".txt") or "_6mmSchraub" not in stem:
        raise D02BRefusal(f"unexpected raw response member: {path}")
    stem = stem[:-4]
    case_name, suffix = stem.split("_6mmSchraub", 1)
    point_token = suffix.lstrip("_")
    if not point_token.isdigit():
        raise D02BRefusal(f"cannot parse point from {path}")
    return kind, case_name, int(point_token)


def build_raw_index(zf: zipfile.ZipFile, cases: list[str]) -> tuple[dict, list[int], dict]:
    index: dict[tuple[str, str, int], str] = {}
    point_sets: dict[tuple[str, str], set[int]] = defaultdict(set)
    non_response = []

    for name in zf.namelist():
        if name.endswith("/"):
            continue
        parsed = parse_response_member(name)
        if parsed is None:
            non_response.append(name)
            continue
        kind, case, point = parsed
        key = (kind, case, point)
        if key in index:
            raise D02BRefusal(f"duplicate raw member for {key}")
        index[key] = name
        point_sets[(kind, case)].add(point)

    expected_cases = set(cases)
    found_amp = {case for kind, case in point_sets if kind == "Amplitude"}
    found_phase = {case for kind, case in point_sets if kind == "Phase"}
    if found_amp != expected_cases or found_phase != expected_cases:
        raise D02BRefusal("raw archive case set does not match torque-state codebook")

    sets = []
    for case in cases:
        sets.append(point_sets[("Amplitude", case)])
        sets.append(point_sets[("Phase", case)])
    common = sorted(set.intersection(*sets))
    if len(common) != 51:
        raise D02BRefusal(f"expected 51 common points, got {len(common)}")

    counts = {
        "amplitude_members": sum(1 for k in index if k[0] == "Amplitude"),
        "phase_members": sum(1 for k in index if k[0] == "Phase"),
        "non_response_members": len(non_response),
        "common_point_count": len(common),
        "used_amplitude_members": len(cases) * len(common),
        "used_phase_members": len(cases) * len(common),
    }
    return index, common, counts


def parse_amplitude_member(raw: bytes) -> np.ndarray:
    text = raw.decode("cp1252", errors="replace")
    marker = text.find("[ Hz ]")
    if marker < 0:
        raise D02BRefusal("Polytec unit row not found")
    start = text.find("\n", marker)
    if start < 0:
        raise D02BRefusal("Polytec data block not found")
    body = text[start + 1:].replace("\t", " ")
    arr = np.fromstring(body, dtype=float, sep=" ")
    if arr.size != 102400:
        raise D02BRefusal(f"expected 102400 numeric fields, got {arr.size}")
    freq = arr[0::2]
    values = arr[1::2]
    if freq.size != 51200 or values.size != 51200:
        raise D02BRefusal("unexpected Polytec data length")
    if freq[0] != 1.0 or freq[-1] != 51200.0:
        raise D02BRefusal("unexpected frequency axis endpoints")
    if not np.all(np.diff(freq) == 1.0):
        raise D02BRefusal("frequency axis is not exact 1 Hz spacing")
    if not np.all(np.isfinite(values)):
        raise D02BRefusal("non-finite amplitude value")
    return values


def spatial_rms_for_case(
    zf: zipfile.ZipFile,
    index: dict,
    case: str,
    common_points: list[int],
) -> np.ndarray:
    sumsq = np.zeros(51200, dtype=float)
    for point in common_points:
        member = index[("Amplitude", case, point)]
        values = parse_amplitude_member(zf.read(member))
        sumsq += values * values
    return np.sqrt(sumsq / float(len(common_points)))


def _interp_crossing(f0: float, y0: float, f1: float, y1: float, target: float) -> float:
    if y1 == y0:
        return 0.5 * (f0 + f1)
    frac = (target - y0) / (y1 - y0)
    return float(f0 + frac * (f1 - f0))


def analyze_half_power(spectrum: np.ndarray, family_hz: int, half_width_hz: int) -> dict:
    if spectrum.shape != (51200,):
        raise D02BRefusal("spectrum must have 51200 bins")

    lo_hz = max(1, int(family_hz - half_width_hz))
    hi_hz = min(51200, int(family_hz + half_width_hz))
    seg = spectrum[lo_hz - 1:hi_hz]
    rel_peak = int(np.argmax(seg))
    peak_hz = float(lo_hz + rel_peak)
    peak_value = float(seg[rel_peak])

    base = {
        "family_hz": int(family_hz),
        "window_low_hz": lo_hz,
        "window_high_hz": hi_hz,
        "peak_hz": peak_hz,
        "peak_amplitude_m_per_N": peak_value,
    }

    if rel_peak == 0 or rel_peak == len(seg) - 1:
        return {**base, "status": "WINDOW_TRUNCATED"}

    maxima = np.where((seg[1:-1] > seg[:-2]) & (seg[1:-1] > seg[2:]))[0] + 1
    competitors = [
        int(i) for i in maxima
        if int(i) != rel_peak
        and abs(int(i) - rel_peak) >= 2
        and float(seg[int(i)]) >= 0.90 * peak_value
    ]
    if competitors:
        return {
            **base,
            "status": "NON_IDENTIFIABLE_MODAL_OVERLAP",
            "competitor_peak_hz": [float(lo_hz + i) for i in competitors],
            "competitor_ratio": [float(seg[i] / peak_value) for i in competitors],
        }

    target = peak_value / math.sqrt(2.0)
    left = rel_peak
    while left > 0 and seg[left] >= target:
        left -= 1
    if left == 0 and seg[left] >= target:
        return {**base, "status": "HALF_POWER_CROSSING_NOT_OBSERVED"}

    right = rel_peak
    while right < len(seg) - 1 and seg[right] >= target:
        right += 1
    if right == len(seg) - 1 and seg[right] >= target:
        return {**base, "status": "HALF_POWER_CROSSING_NOT_OBSERVED"}

    f_left = _interp_crossing(
        float(lo_hz + left), float(seg[left]),
        float(lo_hz + left + 1), float(seg[left + 1]),
        target,
    )
    f_right = _interp_crossing(
        float(lo_hz + right - 1), float(seg[right - 1]),
        float(lo_hz + right), float(seg[right]),
        target,
    )
    bandwidth = float(f_right - f_left)
    if not math.isfinite(bandwidth) or bandwidth <= 0.0:
        return {**base, "status": "NO_ADMISSIBLE_SCALAR_CHI"}

    chi = bandwidth / (2.0 * peak_hz)
    resolution = 1.0 / (2.0 * peak_hz)
    return {
        **base,
        "status": "ADMITTED",
        "half_power_left_hz": f_left,
        "half_power_right_hz": f_right,
        "half_power_bandwidth_hz": bandwidth,
        "chi": float(chi),
        "chi_resolution_1Hz": float(resolution),
    }


def similar_chi(a: dict, b: dict) -> tuple[bool, float, float] | None:
    if a.get("status") != "ADMITTED" or b.get("status") != "ADMITTED":
        return None
    diff = abs(float(a["chi"]) - float(b["chi"]))
    threshold = max(float(a["chi_resolution_1Hz"]), float(b["chi_resolution_1Hz"]))
    return bool(diff <= threshold), float(diff), float(threshold)


def _float_row(row: dict, keys: list[str]) -> dict:
    out = dict(row)
    for k in keys:
        out[k] = float(out[k])
    return out


def classify_family(
    family: int,
    scalar_by_case: dict[str, dict],
    primary_cases: dict[int, str],
    per_case_map: dict[tuple[int, int], dict],
    tight_case: str,
) -> dict:
    tight = scalar_by_case[tight_case]
    pairs = []
    transformed = False
    reorganized = False
    similar_reorganized = False
    admitted_pair_count = 0
    all_four_admitted_similar = tight.get("status") == "ADMITTED"

    for bolt in (1, 2, 3, 4):
        case = primary_cases[bolt]
        loose = scalar_by_case[case]
        relation = similar_chi(tight, loose)
        native = per_case_map[(family, bolt)]
        response_reorganized = (
            abs(float(native["f_case"]) - float(native["f_base"])) >= 1.0
            or float(native["one_minus_MACa"]) > 1e-12
            or float(native["one_minus_CMAC"]) > 1e-12
            or float(native["one_minus_CMAC_phaseonly"]) > 1e-12
        )
        reorganized = reorganized or response_reorganized

        pair = {
            "bolt": bolt,
            "case_name": case,
            "tight_scalar_status": tight.get("status"),
            "case_scalar_status": loose.get("status"),
            "response_reorganized": bool(response_reorganized),
            "native_response": {
                "f_base_hz": float(native["f_base"]),
                "f_case_hz": float(native["f_case"]),
                "frequency_shift_hz": float(native["f_case"]) - float(native["f_base"]),
                "one_minus_MACa": float(native["one_minus_MACa"]),
                "one_minus_CMAC": float(native["one_minus_CMAC"]),
                "one_minus_CMAC_phaseonly": float(native["one_minus_CMAC_phaseonly"]),
            },
        }

        if relation is None:
            all_four_admitted_similar = False
            pair["chi_relation"] = "NOT_COMPARABLE"
        else:
            admitted_pair_count += 1
            is_similar, diff, threshold = relation
            pair["chi_difference"] = diff
            pair["chi_similarity_threshold"] = threshold
            pair["chi_relation"] = (
                "SIMILAR_AT_FROZEN_RESOLUTION"
                if is_similar
                else "CHI_TRANSFORMED_AT_FROZEN_RESOLUTION"
            )
            if not is_similar:
                transformed = True
                all_four_admitted_similar = False
            if is_similar and response_reorganized:
                similar_reorganized = True

        pairs.append(pair)

    labels = []
    if tight.get("status") != "ADMITTED" or admitted_pair_count == 0:
        labels.append("NO_ADMISSIBLE_SCALAR_CHI")
    if transformed:
        labels.append("TRANSFORMED")
    if reorganized:
        labels.append("REORGANIZED")
    if similar_reorganized:
        labels.append("LOCAL_SCALAR_VALID_BUT_EMBEDDED_INSUFFICIENT")
    if all_four_admitted_similar and not reorganized:
        labels.extend(["PRESERVED", "NO_RELATION_DETECTED"])

    return {
        "family_hz": family,
        "labels": labels,
        "tight_scalar": tight,
        "primary_pairs": pairs,
        "admitted_primary_pair_count": admitted_pair_count,
    }


def run_d02b(cache_dir: Path) -> dict:
    documentation = fetch_asset("documentation", cache_dir)
    processed = fetch_asset("processed", cache_dir)
    raw = fetch_asset("raw", cache_dir)

    tables = load_support_tables(Path(documentation["path"]), Path(processed["path"]))
    torque = tables["torque_states"]
    cases = [row["case_name"] for row in torque]

    all_tight = [
        row for row in torque
        if all(float(row[f"bolt{i}_Nm"]) == 10.0 for i in range(1, 5))
    ]
    if len(all_tight) != 1:
        raise D02BRefusal("could not uniquely identify all-tight case")
    tight_case = all_tight[0]["case_name"]

    primary_cases = {}
    dose_cases = {}
    for row in torque:
        vals = [float(row[f"bolt{i}_Nm"]) for i in range(1, 5)]
        zeros = [i + 1 for i, x in enumerate(vals) if x == 0.0]
        fives = [i + 1 for i, x in enumerate(vals) if x == 5.0]
        tens = sum(x == 10.0 for x in vals)
        if len(zeros) == 1 and tens == 3:
            primary_cases[zeros[0]] = row["case_name"]
        if len(fives) == 1 and tens == 3:
            dose_cases[fives[0]] = row["case_name"]
    if set(primary_cases) != {1, 2, 3, 4} or set(dose_cases) != {1, 2, 3, 4}:
        raise D02BRefusal("could not identify all four single-bolt 0/5 Nm cases")

    family_windows = {
        int(float(row["retained_resonance_group_hz"])): int(float(row["rounded_window_half_width_hz"]))
        for row in tables["windows"]
    }
    families = sorted(family_windows)
    if families != [3325, 4703, 7034, 7861, 8163, 8428, 8695]:
        raise D02BRefusal(f"unexpected retained families: {families}")

    per_case_map = {
        (int(float(row["family"])), int(row["bolt"])): row
        for row in tables["per_case"]
    }

    tracked_map = {int(float(row["family_hz"])): row for row in tables["tracked"]}

    spectra = {}
    with zipfile.ZipFile(raw["path"]) as zf:
        index, common_points, raw_counts = build_raw_index(zf, cases)
        if raw_counts["amplitude_members"] != 919 or raw_counts["phase_members"] != 919:
            raise D02BRefusal("unexpected raw response-member counts")
        if raw_counts["used_amplitude_members"] != 918:
            raise D02BRefusal("unexpected matched amplitude member count")

        for case in cases:
            spectra[case] = spatial_rms_for_case(zf, index, case, common_points)

    scalar_records = []
    scalar_map: dict[int, dict[str, dict]] = {}
    status_counts = Counter()
    for family in families:
        scalar_map[family] = {}
        for case in cases:
            record = analyze_half_power(spectra[case], family, family_windows[family])
            record["case_name"] = case
            scalar_map[family][case] = record
            scalar_records.append(record)
            status_counts[record["status"]] += 1

    crosschecks = []
    for family in families:
        row = tracked_map[family]
        checks = [(tight_case, float(row["tight_hz"]), "tight")]
        for bolt in (1, 2, 3, 4):
            checks.append((primary_cases[bolt], float(row[f"bolt{bolt}_hz"]), f"bolt{bolt}"))
        for case, expected, label in checks:
            observed = float(scalar_map[family][case]["peak_hz"])
            diff = observed - expected
            crosschecks.append({
                "family_hz": family,
                "condition": label,
                "case_name": case,
                "source_tracked_hz": expected,
                "raw_reconstructed_peak_hz": observed,
                "difference_hz": diff,
                "within_frozen_tolerance": bool(abs(diff) <= 1.0),
            })
    if not all(x["within_frozen_tolerance"] for x in crosschecks):
        raise D02BRefusal("raw peak reconstruction failed source tracked-frequency cross-check")

    family_results = [
        classify_family(
            family,
            scalar_map[family],
            primary_cases,
            per_case_map,
            tight_case,
        )
        for family in families
    ]

    primary_pairs = [
        pair
        for fam in family_results
        for pair in fam["primary_pairs"]
    ]
    comparable = [p for p in primary_pairs if p["chi_relation"] != "NOT_COMPARABLE"]
    similar = [p for p in comparable if p["chi_relation"] == "SIMILAR_AT_FROZEN_RESOLUTION"]
    transformed_pairs = [
        p for p in comparable if p["chi_relation"] == "CHI_TRANSFORMED_AT_FROZEN_RESOLUTION"
    ]
    similar_reorganized = [p for p in similar if p["response_reorganized"]]

    dose_rows = []
    dose_native = {
        (int(float(row["group"])), int(row["bolt"]), int(float(row["torque_Nm"]))): row
        for row in tables["dose"]
    }
    for family in families:
        for bolt in (1, 2, 3, 4):
            cases_by_torque = {
                10: tight_case,
                5: dose_cases[bolt],
                0: primary_cases[bolt],
            }
            for torque_nm in (10, 5, 0):
                native = dose_native[(family, bolt, torque_nm)]
                scalar = scalar_map[family][cases_by_torque[torque_nm]]
                dose_rows.append({
                    "family_hz": family,
                    "bolt": bolt,
                    "torque_Nm": torque_nm,
                    "case_name": cases_by_torque[torque_nm],
                    "scalar_status": scalar["status"],
                    "chi": scalar.get("chi"),
                    "chi_resolution_1Hz": scalar.get("chi_resolution_1Hz"),
                    "raw_peak_hz": scalar["peak_hz"],
                    "native_f_tracked_hz": float(native["f_tracked"]),
                    "one_minus_MACa": float(native["one_minus_MACa"]),
                    "one_minus_CMAC": float(native["one_minus_CMAC"]),
                    "one_minus_CMAC_phaseonly": float(native["one_minus_CMAC_phaseonly"]),
                })

    family_label_counts = Counter(
        label for fam in family_results for label in fam["labels"]
    )

    return {
        "schema": "d02b-four-bolt-physical-result-v0.1",
        "status": "P0_Q_PHYSICAL_D02B_EXECUTED",
        "evidence_class": "PHYSICAL_REPEATED_CONDITION_P0_Q",
        "source_record": "10.5281/zenodo.20038951",
        "source_files": {
            "documentation": {k: documentation[k] for k in ("filename","size_bytes","md5","sha256","url")},
            "processed": {k: processed[k] for k in ("filename","size_bytes","md5","sha256","url")},
            "raw": {k: raw[k] for k in ("filename","size_bytes","md5","sha256","url")},
        },
        "retained_families_hz": families,
        "torque_state_count": len(cases),
        "common_point_ids": common_points,
        "raw_member_counts": raw_counts,
        "scalar_status_counts": dict(status_counts),
        "scalar_records": scalar_records,
        "tracked_frequency_crosschecks": crosschecks,
        "family_results": family_results,
        "dose_response": dose_rows,
        "primary_summary": {
            "primary_pair_count": len(primary_pairs),
            "comparable_chi_pair_count": len(comparable),
            "similar_chi_pair_count": len(similar),
            "transformed_chi_pair_count": len(transformed_pairs),
            "response_reorganized_pair_count": sum(p["response_reorganized"] for p in primary_pairs),
            "similar_chi_and_reorganized_pair_count": len(similar_reorganized),
            "family_label_counts": dict(family_label_counts),
        },
        "added_value_verdict_preinterpretation": "NOT_ASSIGNED_BY_RUNNER",
        "scope": (
            "Physical P0-Q qualification. The runner reports frozen native/scalar mappings only; "
            "scientific added-value interpretation is archived downstream."
        ),
    }
