from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from substrate_inheritance.depth_validation import (
    finite_chain_dynamic_matrix,
    finite_surface_green,
    recursive_surface_green,
    semi_infinite_surface_green,
)


PLAN_PATH = Path("substrate_inheritance/SI_FM2_EMBEDDING_DEPTH_PLAN_v0.1.json")
FREEZE_PATH = Path("substrate_inheritance/SI_FM2_EXECUTION_FREEZE_v0.1.json")
RESULT_PATH = Path("substrate_inheritance/results/fm2_embedding_depth_landscape.json")


def _effective_depth(records: list[dict[str, Any]], tolerance: float) -> dict[str, Any]:
    errors = [float(row["relative_error_to_semi_infinite"]) for row in records]
    depths = [int(row["retained_depth_dof"]) for row in records]
    for index, depth in enumerate(depths):
        if all(error <= tolerance for error in errors[index:]):
            return {
                "status": "REACHED_WITHIN_GRID",
                "retained_depth_dof": depth,
                "tolerance": tolerance,
                "maximum_error_at_or_beyond_effective_depth": float(max(errors[index:])),
            }
    return {
        "status": "NOT_REACHED_WITHIN_GRID",
        "retained_depth_dof": None,
        "tolerance": tolerance,
        "minimum_error_in_grid": float(min(errors)),
    }


def _nonmonotonic_steps(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for left, right in zip(records[:-1], records[1:]):
        a = float(left["relative_error_to_semi_infinite"])
        b = float(right["relative_error_to_semi_infinite"])
        if b > a + 1e-15:
            out.append(
                {
                    "from_depth": int(left["retained_depth_dof"]),
                    "to_depth": int(right["retained_depth_dof"]),
                    "from_error": a,
                    "to_error": b,
                }
            )
    return out


def evaluate_case(
    *,
    depths: list[int],
    hopping: float,
    real_frequency: float,
    imaginary_regularizer: float,
    onsite_stiffness: float,
    child_coupling: float,
    tolerances: list[float],
) -> dict[str, Any]:
    z = complex(real_frequency, imaginary_regularizer)
    onsite = complex(onsite_stiffness) - z**2
    g_inf = semi_infinite_surface_green(onsite, hopping)
    sigma_inf = (child_coupling**2) * g_inf

    records: list[dict[str, Any]] = []
    for depth in depths:
        matrix = finite_chain_dynamic_matrix(depth, onsite, hopping)
        g_matrix = finite_surface_green(depth, onsite, hopping)
        g_recursive = recursive_surface_green(depth, onsite, hopping)
        sigma = (child_coupling**2) * g_matrix
        error = abs(sigma - sigma_inf) / max(abs(sigma_inf), 1e-15)
        records.append(
            {
                "retained_depth_dof": int(depth),
                "finite_self_energy_real": float(np.real(sigma)),
                "finite_self_energy_imag": float(np.imag(sigma)),
                "relative_error_to_semi_infinite": float(error),
                "matrix_vs_recursive_surface_green_absolute_residual": float(abs(g_matrix - g_recursive)),
                "finite_dynamic_matrix_condition_number_2norm": float(np.linalg.cond(matrix)),
            }
        )

    effective = {str(tol): _effective_depth(records, tol) for tol in tolerances}
    nonmonotonic = _nonmonotonic_steps(records)

    return {
        "substrate_hopping": float(hopping),
        "probe_frequency": {
            "real": float(real_frequency),
            "imaginary_regularizer": float(imaginary_regularizer),
        },
        "semi_infinite_self_energy": {
            "real": float(np.real(sigma_inf)),
            "imag": float(np.imag(sigma_inf)),
        },
        "depth_records": records,
        "effective_depth_by_declared_numerical_tolerance": effective,
        "nonmonotonic_error_step_count": len(nonmonotonic),
        "nonmonotonic_error_steps": nonmonotonic,
        "finite_bath_recurrence_status": "NOT_EVALUATED_FREQUENCY_DOMAIN_MAP",
    }


def run_fm2(plan: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    if plan.get("schema") != "substrate-inheritance-fm2-embedding-depth-plan-v0.1":
        raise ValueError("FM2 requires frozen plan v0.1")
    if execution.get("schema") != "substrate-inheritance-fm2-execution-freeze-v0.1":
        raise ValueError("FM2 requires execution freeze v0.1")
    if execution.get("parameter_overrides") is not False:
        raise ValueError("FM2 execution may not override parent scientific parameters")
    if plan.get("physical_inheritance_claim") is not False:
        raise ValueError("FM2 cannot carry physical inheritance claim")

    grid = plan["parameter_grid"]
    depths = [int(x) for x in grid["retained_depth_dof"]]
    hoppings = [float(x) for x in grid["substrate_hopping"]]
    real_frequencies = [float(x) for x in grid["probe_real_frequency"]]
    imaginary_regularizers = [float(x) for x in grid["probe_imaginary_regularizer"]]
    tolerances = [float(x) for x in plan["declared_numerical_task_tolerances"]]
    construction = plan["native_synthetic_construction"]

    case_count = len(hoppings) * len(real_frequencies) * len(imaginary_regularizers)
    if case_count != int(grid["parameter_case_count_excluding_depth"]):
        raise ValueError("FM2 case count does not match frozen plan")
    if case_count * len(depths) != int(grid["total_depth_records"]):
        raise ValueError("FM2 depth-record count does not match frozen plan")

    cases = []
    for hopping in hoppings:
        for real_frequency in real_frequencies:
            for imaginary_regularizer in imaginary_regularizers:
                cases.append(
                    evaluate_case(
                        depths=depths,
                        hopping=hopping,
                        real_frequency=real_frequency,
                        imaginary_regularizer=imaginary_regularizer,
                        onsite_stiffness=float(construction["substrate_onsite_stiffness"]),
                        child_coupling=float(construction["child_coupling"]),
                        tolerances=tolerances,
                    )
                )

    all_depth_records = [row for case in cases for row in case["depth_records"]]
    max_method_residual = max(
        float(row["matrix_vs_recursive_surface_green_absolute_residual"])
        for row in all_depth_records
    )
    max_condition = max(float(row["finite_dynamic_matrix_condition_number_2norm"]) for row in all_depth_records)
    max_error = max(float(row["relative_error_to_semi_infinite"]) for row in all_depth_records)
    min_error = min(float(row["relative_error_to_semi_infinite"]) for row in all_depth_records)
    nonmonotonic_cases = sum(1 for case in cases if case["nonmonotonic_error_step_count"] > 0)

    tolerance_summary: dict[str, Any] = {}
    for tolerance in tolerances:
        key = str(tolerance)
        reached = [
            case["effective_depth_by_declared_numerical_tolerance"][key]
            for case in cases
            if case["effective_depth_by_declared_numerical_tolerance"][key]["status"] == "REACHED_WITHIN_GRID"
        ]
        not_reached = case_count - len(reached)
        depths_reached = [int(item["retained_depth_dof"]) for item in reached]
        tolerance_summary[key] = {
            "reached_case_count": len(reached),
            "not_reached_case_count": not_reached,
            "reached_fraction": float(len(reached) / case_count),
            "minimum_effective_depth_dof": min(depths_reached) if depths_reached else None,
            "median_effective_depth_dof": float(np.median(depths_reached)) if depths_reached else None,
            "maximum_effective_depth_dof": max(depths_reached) if depths_reached else None,
        }

    method_tol = float(execution["finite_method_agreement"]["absolute_tolerance"])
    numerical_status = (
        "FINITE_METHODS_AGREE_WITHIN_FROZEN_TOLERANCE"
        if max_method_residual <= method_tol
        else "NUMERICAL_VERIFICATION_FAILURE"
    )

    return {
        "scope": "synthetic_fm2_embedding_depth_function_limit_map_only",
        "status": "P0_D_DESCRIPTIVE_STRUCTURAL",
        "physical_inheritance_claim": False,
        "physical_thresholds_frozen": False,
        "atlas_target_used": False,
        "chi_used": False,
        "numerical_effective_depth_is_physical_inheritance_length": False,
        "imaginary_probe_is_damping": False,
        "plan": str(PLAN_PATH),
        "execution_freeze": str(FREEZE_PATH),
        "case_count": case_count,
        "depth_record_count": len(all_depth_records),
        "numerical_verification": {
            "status": numerical_status,
            "frozen_absolute_tolerance": method_tol,
            "maximum_matrix_vs_recursive_surface_green_residual": max_method_residual,
        },
        "summary": {
            "maximum_relative_error_to_semi_infinite": max_error,
            "minimum_relative_error_to_semi_infinite": min_error,
            "maximum_finite_dynamic_matrix_condition_number_2norm": max_condition,
            "nonmonotonic_convergence_case_count": nonmonotonic_cases,
            "nonmonotonic_convergence_case_fraction": float(nonmonotonic_cases / case_count),
            "effective_depth_by_declared_numerical_tolerance": tolerance_summary,
            "finite_bath_recurrence_status": "NOT_EVALUATED_FREQUENCY_DOMAIN_MAP",
        },
        "cases": cases,
    }


def write_fm2(plan_path: Path = PLAN_PATH, freeze_path: Path = FREEZE_PATH, result_path: Path = RESULT_PATH) -> dict[str, Any]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    result = run_fm2(plan, freeze)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_fm2()
    print(json.dumps({"numerical_verification": result["numerical_verification"], "summary": result["summary"]}, indent=2, sort_keys=True))
