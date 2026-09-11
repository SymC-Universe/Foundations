from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from domain_map_linear import run_d01a  # noqa: E402


PLAN = ROOT / "D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json"
OUT = ROOT / "results" / "D01A_SDOF_DOMAIN_MAP_v0.1.json"


def main() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    result = run_d01a(plan)

    records = result["records"]
    collapse = result["scale_collapse"]

    def finite_records(ic_index: int, key: str):
        return [r for r in records if r["initial_condition_index"] == ic_index and r[key] is not None]

    summaries = []
    for ic_index in range(len(result["normalized_initial_conditions"])):
        recs = [r for r in records if r["initial_condition_index"] == ic_index]
        settling = finite_records(ic_index, "settling_tau_2pct")
        abs_integral = finite_records(ic_index, "integral_abs_x_dtau")
        energy_integral = finite_records(ic_index, "integral_energy_dtau")
        slow = finite_records(ic_index, "slowest_dimensionless_decay_rate")
        summaries.append(
            {
                "initial_condition_index": ic_index,
                "minimum_settling_tau_2pct": min(
                    ({"chi": r["chi"], "value": r["settling_tau_2pct"]} for r in settling),
                    key=lambda z: z["value"],
                    default=None,
                ),
                "minimum_integral_abs_x_dtau": min(
                    ({"chi": r["chi"], "value": r["integral_abs_x_dtau"]} for r in abs_integral),
                    key=lambda z: z["value"],
                ),
                "minimum_integral_energy_dtau": min(
                    ({"chi": r["chi"], "value": r["integral_energy_dtau"]} for r in energy_integral),
                    key=lambda z: z["value"],
                ),
                "maximum_slowest_dimensionless_decay_rate": max(
                    ({"chi": r["chi"], "value": r["slowest_dimensionless_decay_rate"]} for r in slow),
                    key=lambda z: z["value"],
                ),
                "first_nonoscillatory_grid_point": next(
                    (
                        {"chi": r["chi"], "regime": r["regime"]}
                        for r in recs
                        if r["zero_crossing_count"] == 0
                    ),
                    None,
                ),
            }
        )

    result["descriptive_landmarks"] = summaries
    result["maximum_scale_collapse_error"] = {
        "x": max(r["max_abs_normalized_x_difference_across_omega0"] for r in collapse),
        "u": max(r["max_abs_normalized_u_difference_across_omega0"] for r in collapse),
    }
    result["interpretation_ceiling"] = (
        "Within-domain exact-anchor response mapping only. Descriptive landmarks are generated "
        "from metrics frozen in D01_LINEAR_DYNAMICS_DOMAIN_MAP_PLAN_v0.1.json and are not cross-domain evidence."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUT)
    print(json.dumps({
        "maximum_scale_collapse_error": result["maximum_scale_collapse_error"],
        "descriptive_landmarks": result["descriptive_landmarks"],
    }, indent=2))


if __name__ == "__main__":
    main()
