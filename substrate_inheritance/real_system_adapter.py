from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


SCHEMA = "substrate-inheritance-real-system-input-v0.2"
CORRESPONDENCE_PROTOCOL = "substrate_inheritance/CORRESPONDENCE_PROTOCOL_v0.2.json"
ALLOWED_ROLES = {"development_only", "prospective_validation", "contrast_limit"}
ALLOWED_OBJECT_KINDS = {"mass_weightable_hessian", "harmonic_force_constant_matrix"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class IngestionRefusal(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True)
class MechanicalObject:
    object_id: str
    coordinate_ids: tuple[str, ...]
    masses: np.ndarray
    stiffness: np.ndarray
    matrix_units: str
    mass_units: str
    symmetry_absolute_tolerance: float
    source_artifact_sha256: str


def _require(mapping: dict[str, Any], field: str, where: str) -> Any:
    if field not in mapping:
        raise IngestionRefusal("MISSING_FIELD", f"{where}.{field} is required")
    return mapping[field]


def _validate_sha256(value: Any, where: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise IngestionRefusal("INVALID_SHA256", f"{where} must be a 64-character hexadecimal SHA-256")
    return value.lower()


def _finite_float(value: Any, where: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise IngestionRefusal("INVALID_NUMBER", f"{where} must be numeric") from exc
    if not math.isfinite(out):
        raise IngestionRefusal("NONFINITE_NUMBER", f"{where} must be finite")
    return out


def _validate_mechanical_object(raw: Any, where: str) -> MechanicalObject:
    if not isinstance(raw, dict):
        raise IngestionRefusal("INVALID_OBJECT", f"{where} must be an object")

    object_id = _require(raw, "object_id", where)
    object_kind = _require(raw, "object_kind", where)
    coordinate_ids_raw = _require(raw, "coordinate_ids", where)
    masses_raw = _require(raw, "masses", where)
    stiffness_raw = _require(raw, "stiffness_matrix", where)
    matrix_units = _require(raw, "matrix_units", where)
    mass_units = _require(raw, "mass_units", where)
    tolerance = _finite_float(_require(raw, "symmetry_absolute_tolerance", where), f"{where}.symmetry_absolute_tolerance")
    source_hash = _validate_sha256(_require(raw, "source_artifact_sha256", where), f"{where}.source_artifact_sha256")

    if not isinstance(object_id, str) or not object_id.strip():
        raise IngestionRefusal("INVALID_OBJECT_ID", f"{where}.object_id must be a nonempty string")
    if object_kind not in ALLOWED_OBJECT_KINDS:
        raise IngestionRefusal("UNSUPPORTED_OBJECT_KIND", f"{where}.object_kind={object_kind!r} is not supported")
    if tolerance < 0.0:
        raise IngestionRefusal("INVALID_TOLERANCE", f"{where}.symmetry_absolute_tolerance must be nonnegative")
    if not isinstance(matrix_units, str) or not matrix_units.strip():
        raise IngestionRefusal("INVALID_UNITS", f"{where}.matrix_units must be a nonempty string")
    if not isinstance(mass_units, str) or not mass_units.strip():
        raise IngestionRefusal("INVALID_UNITS", f"{where}.mass_units must be a nonempty string")
    if not isinstance(coordinate_ids_raw, list) or not coordinate_ids_raw:
        raise IngestionRefusal("INVALID_COORDINATES", f"{where}.coordinate_ids must be a nonempty list")
    if any(not isinstance(item, str) or not item.strip() for item in coordinate_ids_raw):
        raise IngestionRefusal("INVALID_COORDINATES", f"{where}.coordinate_ids must contain nonempty strings")
    if len(set(coordinate_ids_raw)) != len(coordinate_ids_raw):
        raise IngestionRefusal("DUPLICATE_COORDINATES", f"{where}.coordinate_ids contains duplicates")

    n = len(coordinate_ids_raw)
    try:
        masses = np.asarray(masses_raw, dtype=float)
        stiffness = np.asarray(stiffness_raw, dtype=float)
    except (TypeError, ValueError) as exc:
        raise IngestionRefusal("INVALID_MATRIX_DATA", f"{where} masses/matrix must be numeric") from exc

    if masses.shape != (n,):
        raise IngestionRefusal("DIMENSION_MISMATCH", f"{where}.masses must have length {n}")
    if stiffness.shape != (n, n):
        raise IngestionRefusal("DIMENSION_MISMATCH", f"{where}.stiffness_matrix must have shape ({n}, {n})")
    if not np.all(np.isfinite(masses)) or not np.all(np.isfinite(stiffness)):
        raise IngestionRefusal("NONFINITE_DATA", f"{where} masses/matrix contains nonfinite values")
    if np.any(masses <= 0.0):
        raise IngestionRefusal("NONPOSITIVE_MASS", f"{where}.masses must all be positive")

    asymmetry = float(np.max(np.abs(stiffness - stiffness.T)))
    if asymmetry > tolerance:
        raise IngestionRefusal(
            "ASYMMETRIC_MATRIX",
            f"{where}.stiffness_matrix asymmetry {asymmetry:.6g} exceeds declared tolerance {tolerance:.6g}",
        )

    # Symmetrization is a numerical cleanup only after the declared tolerance passes.
    stiffness = 0.5 * (stiffness + stiffness.T)

    return MechanicalObject(
        object_id=object_id,
        coordinate_ids=tuple(coordinate_ids_raw),
        masses=masses,
        stiffness=stiffness,
        matrix_units=matrix_units,
        mass_units=mass_units,
        symmetry_absolute_tolerance=tolerance,
        source_artifact_sha256=source_hash,
    )


def _validate_mapping(raw: Any, parent: MechanicalObject, child: MechanicalObject) -> list[tuple[int, int, str, str]]:
    if not isinstance(raw, list):
        raise IngestionRefusal("INVALID_MAPPING", "shared_coordinate_map must be a list")
    if len(raw) != len(parent.coordinate_ids):
        raise IngestionRefusal(
            "INCOMPLETE_PARENT_MAPPING",
            "shared_coordinate_map must contain exactly one entry for every parent coordinate",
        )

    parent_index = {name: i for i, name in enumerate(parent.coordinate_ids)}
    child_index = {name: i for i, name in enumerate(child.coordinate_ids)}
    seen_parent: set[str] = set()
    seen_child: set[str] = set()
    resolved: list[tuple[int, int, str, str]] = []

    for idx, item in enumerate(raw):
        if not isinstance(item, dict):
            raise IngestionRefusal("INVALID_MAPPING", f"shared_coordinate_map[{idx}] must be an object")
        p = _require(item, "parent_coordinate_id", f"shared_coordinate_map[{idx}]")
        c = _require(item, "child_coordinate_id", f"shared_coordinate_map[{idx}]")
        if p not in parent_index:
            raise IngestionRefusal("UNKNOWN_PARENT_COORDINATE", f"mapping references unknown parent coordinate {p!r}")
        if c not in child_index:
            raise IngestionRefusal("UNKNOWN_CHILD_COORDINATE", f"mapping references unknown child coordinate {c!r}")
        if p in seen_parent:
            raise IngestionRefusal("DUPLICATE_PARENT_MAPPING", f"parent coordinate {p!r} is mapped more than once")
        if c in seen_child:
            raise IngestionRefusal("DUPLICATE_CHILD_MAPPING", f"child coordinate {c!r} is mapped more than once")
        seen_parent.add(p)
        seen_child.add(c)
        resolved.append((parent_index[p], child_index[c], p, c))

    if seen_parent != set(parent.coordinate_ids):
        raise IngestionRefusal("INCOMPLETE_PARENT_MAPPING", "not every parent coordinate is mapped exactly once")
    return resolved


def validate_real_system_record(record: Any) -> tuple[MechanicalObject, MechanicalObject, list[tuple[int, int, str, str]]]:
    if not isinstance(record, dict):
        raise IngestionRefusal("INVALID_RECORD", "input must be a JSON object")
    if _require(record, "schema", "record") != SCHEMA:
        raise IngestionRefusal("SCHEMA_MISMATCH", f"record.schema must equal {SCHEMA!r}")
    system_id = _require(record, "system_id", "record")
    role = _require(record, "system_role", "record")
    channel = _require(record, "channel", "record")
    protocol = _require(record, "correspondence_protocol", "record")
    provenance = _require(record, "provenance", "record")

    if not isinstance(system_id, str) or not system_id.strip():
        raise IngestionRefusal("INVALID_SYSTEM_ID", "record.system_id must be a nonempty string")
    if role not in ALLOWED_ROLES:
        raise IngestionRefusal("INVALID_SYSTEM_ROLE", f"unsupported system_role {role!r}")
    if channel != "mechanical_harmonic":
        raise IngestionRefusal("UNSUPPORTED_CHANNEL", "v0.2 adapter accepts only mechanical_harmonic records")
    if protocol != CORRESPONDENCE_PROTOCOL:
        raise IngestionRefusal("PROTOCOL_MISMATCH", f"correspondence_protocol must equal {CORRESPONDENCE_PROTOCOL!r}")
    if not isinstance(provenance, dict):
        raise IngestionRefusal("INVALID_PROVENANCE", "record.provenance must be an object")

    for field in ("source_repository", "source_ref", "source_commit"):
        value = _require(provenance, field, "record.provenance")
        if not isinstance(value, str) or not value.strip():
            raise IngestionRefusal("INVALID_PROVENANCE", f"record.provenance.{field} must be a nonempty string")

    frozen = _require(provenance, "mapping_frozen_before_target_carrier_inspection", "record.provenance")
    kinetics = _require(provenance, "target_kinetics_used_to_choose_mapping", "record.provenance")
    chi_used = _require(provenance, "chi_used_to_choose_mapping", "record.provenance")
    if frozen is not True:
        raise IngestionRefusal("MAPPING_NOT_PROSPECTIVE", "mapping must be frozen before target carrier inspection")
    if kinetics is not False:
        raise IngestionRefusal("TARGET_LEAKAGE", "target kinetics may not be used to choose the mapping")
    if chi_used is not False:
        raise IngestionRefusal("TARGET_LEAKAGE", "chi may not be used to choose the mapping")

    parent = _validate_mechanical_object(_require(record, "parent", "record"), "record.parent")
    child = _validate_mechanical_object(_require(record, "child", "record"), "record.child")

    if parent.matrix_units != child.matrix_units:
        raise IngestionRefusal("MATRIX_UNIT_MISMATCH", "parent and child matrix_units differ; convert upstream")
    if parent.mass_units != child.mass_units:
        raise IngestionRefusal("MASS_UNIT_MISMATCH", "parent and child mass_units differ; convert upstream")

    resolved_mapping = _validate_mapping(_require(record, "shared_coordinate_map", "record"), parent, child)
    return parent, child, resolved_mapping


def _mass_weighted_modes(obj: MechanicalObject) -> tuple[np.ndarray, np.ndarray]:
    inv_sqrt_m = 1.0 / np.sqrt(obj.masses)
    dynamical = inv_sqrt_m[:, None] * obj.stiffness * inv_sqrt_m[None, :]
    values, vectors = np.linalg.eigh(dynamical)
    return values, vectors


def analyze_real_system_record(record: dict[str, Any]) -> dict[str, Any]:
    parent, child, mapping = validate_real_system_record(record)
    parent_values, parent_modes = _mass_weighted_modes(parent)
    child_values, child_modes = _mass_weighted_modes(child)

    parent_order = [p_idx for p_idx, _, _, _ in sorted(mapping, key=lambda row: row[0])]
    child_order = [c_idx for _, c_idx, _, _ in sorted(mapping, key=lambda row: row[0])]
    if parent_order != list(range(len(parent.coordinate_ids))):
        raise IngestionRefusal("INTERNAL_MAPPING_ERROR", "parent mapping could not be placed in coordinate order")

    projected = child_modes[np.asarray(child_order), :]
    participation = np.sum(np.abs(projected) ** 2, axis=0)

    norms = np.linalg.norm(projected, axis=0)
    normalized_projected = np.zeros_like(projected)
    nonzero = norms > 0.0
    normalized_projected[:, nonzero] = projected[:, nonzero] / norms[nonzero]
    overlap = np.abs(parent_modes.T.conj() @ normalized_projected) ** 2
    overlap[:, ~nonzero] = 0.0

    return {
        "schema": "substrate-inheritance-real-system-analysis-v0.1",
        "system_id": record["system_id"],
        "system_role": record["system_role"],
        "channel": "mechanical_harmonic",
        "software_admissibility_status": "PASS_INPUT_CONTRACT",
        "correspondence_protocol": CORRESPONDENCE_PROTOCOL,
        "parent_object_id": parent.object_id,
        "child_object_id": child.object_id,
        "parent_source_artifact_sha256": parent.source_artifact_sha256,
        "child_source_artifact_sha256": child.source_artifact_sha256,
        "parent_mass_weighted_eigenvalues": parent_values.tolist(),
        "child_mass_weighted_eigenvalues": child_values.tolist(),
        "parent_to_child_projected_modal_overlap_matrix": overlap.tolist(),
        "child_substrate_participation_weights": participation.tolist(),
        "shared_coordinate_mapping_record": [
            {"parent_coordinate_id": p_name, "child_coordinate_id": c_name}
            for _, _, p_name, c_name in sorted(mapping, key=lambda row: row[0])
        ],
        "physical_inheritance_threshold_applied": False,
        "inheritance_promotion_label_assigned": False,
        "chi_computed": False,
        "damping_computed": False,
        "interpretation": (
            "Carrier-resolved preprocessing only. The overlap matrix describes direction correspondence after projecting child mass-weighted modes onto the prospectively mapped parent coordinates. "
            "Participation weights report how much of each normalized full child mode lies on those shared substrate coordinates. Neither quantity alone assigns physical inheritance."
        ),
    }


def canonical_record_sha256(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def analyze_file(input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    source = Path(input_path)
    record = json.loads(source.read_text(encoding="utf-8"))
    result = analyze_real_system_record(record)
    result["input_record_canonical_sha256"] = canonical_record_sha256(record)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result
