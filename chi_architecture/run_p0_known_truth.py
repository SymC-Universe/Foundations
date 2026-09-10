from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from p0_known_truth import run_f0_f8  # noqa: E402


def main() -> None:
    results = run_f0_f8()
    record = {
        "schema": "chi-architecture-p0-known-truth-results-v0.1",
        "status": "P0_EXPLORATORY_SYNTHETIC_ONLY",
        "scope": "known_truth_method_stress_not_empirical_confirmation",
        "mfr14_activated": False,
        "program_portfolio_adds_credit": False,
        "real_system_evidence": False,
        "results": results,
    }
    out_dir = ROOT / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "P0_KNOWN_TRUTH_RESULTS_v0.1.json"
    out_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out_path)
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
