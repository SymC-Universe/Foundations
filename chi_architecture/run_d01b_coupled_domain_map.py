from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from domain_map_linear import run_d01b  # noqa: E402


PLAN = ROOT / "D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json"
FREEZE = ROOT / "D01B_EXECUTION_FREEZE_v0.1.json"
OUT = ROOT / "results" / "D01B_COUPLED_2DOF_DOMAIN_MAP_v0.1.json"


def _case_key(record: dict) -> dict:
    return record["parameters"]


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    execution = json.loads(FREEZE.read_text(encoding="utf-8"))
    result = run_d01b(plan, execution)
    records = result["records"]

    exact_scalarized = [
        r for r in records
        if r["exact_real_modal_scalarization"]["status"] == "EXACT_REAL_MODAL_SCALARIZATION_ADMISSIBLE"
    ]
    all_responses = [
        (r, response)
        for r in records
        for response in r["responses"]
    ]
    finite_settling = [
        (r, response)
        for r, response in all_responses
        if response["settling_time_2pct"] is not None
    ]
    unsettled = [
        (r, response)
        for r, response in all_responses
        if response["settling_time_2pct"] is None
    ]

    max_spectral = max(records, key=lambda r: r["spectral_displacement_from_uncoupled_rms"])
    max_receiver = max(all_responses, key=lambda z: z[1]["receiving_component_peak_energy_fraction"])
    max_balance = max(all_responses, key=lambda z: z[1]["maximum_energy_balance_residual_fraction"])
    min_sep = min(records, key=lambda r: r["minimum_normalized_eigenvalue_separation"])

    summary = {
        "parameter_case_count": len(records),
        "response_count": len(all_responses),
        "asymptotically_stable_case_count": sum(1 for r in records if r["asymptotic_stability"]),
        "exact_real_modal_scalarization_case_count": len(exact_scalarized),
        "no_exact_real_modal_scalarization_case_count": len(records) - len(exact_scalarized),
        "not_settled_within_fixed_window_response_count": len(unsettled),
        "maximum_spectral_displacement_from_uncoupled": {
            "value": max_spectral["spectral_displacement_from_uncoupled_rms"],
            "parameters": _case_key(max_spectral),
        },
        "largest_receiving_component_peak_energy_fraction": {
            "value": max_receiver[1]["receiving_component_peak_energy_fraction"],
            "time": max_receiver[1]["receiving_component_peak_time"],
            "perturbation": max_receiver[1]["meaning"],
            "parameters": _case_key(max_receiver[0]),
        },
        "smallest_normalized_eigenvalue_separation": {
            "value": min_sep["minimum_normalized_eigenvalue_separation"],
            "parameters": _case_key(min_sep),
        },
        "maximum_energy_balance_residual_fraction": {
            "value": max_balance[1]["maximum_energy_balance_residual_fraction"],
            "perturbation": max_balance[1]["meaning"],
            "parameters": _case_key(max_balance[0]),
        },
        "minimum_settling_time_2pct": None,
        "maximum_finite_settling_time_2pct": None,
    }

    if finite_settling:
        fastest = min(finite_settling, key=lambda z: z[1]["settling_time_2pct"])
        slowest = max(finite_settling, key=lambda z: z[1]["settling_time_2pct"])
        summary["minimum_settling_time_2pct"] = {
            "value": fastest[1]["settling_time_2pct"],
            "perturbation": fastest[1]["meaning"],
            "parameters": _case_key(fastest[0]),
        }
        summary["maximum_finite_settling_time_2pct"] = {
            "value": slowest[1]["settling_time_2pct"],
            "perturbation": slowest[1]["meaning"],
            "parameters": _case_key(slowest[0]),
        }

    result["descriptive_summary"] = summary
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUT)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
