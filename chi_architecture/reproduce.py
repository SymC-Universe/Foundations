from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
import scipy


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
RESULTS = ROOT / "results"
FREEZE = ROOT / "D01C_PREEXECUTION_FREEZE_v0.1.json"

sys.path.insert(0, str(SRC))

from domain_map_nonnormal import load_freeze, run_d01c  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_tests() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "chi_architecture/tests/test_domain_map_nonnormal.py"],
        check=True,
        cwd=ROOT.parent,
        env=env,
    )


def result_card(result: dict) -> str:
    lines = [
        "# D01C Reproduction Result Card",
        "",
        f"**Status:** {result['status']}",
        f"**Cases:** {result['case_count']}",
        f"**Maximum spectral residual:** {result['max_spectral_residual']:.3e}",
        f"**Eigenvalue-only sufficiency:** {result['eigenvalue_only_sufficiency_status']}",
        "",
        "## Frozen-family summaries",
        "",
    ]
    for s in result["family_summaries"]:
        lines.extend(
            [
                f"### {s['family_id']} | eigenvalues {s['eigenvalues']}",
                "",
                f"- spectral abscissa: {s['spectral_abscissa']:.6g}",
                f"- normal max operator state gain: {s['normal_max_operator_state_gain']:.9g}",
                f"- smallest-angle max operator state gain: {s['smallest_theta_max_operator_state_gain']:.9g}",
                f"- gain ratio: {s['state_gain_ratio_smallest_theta_to_normal']:.9g}",
                f"- minimum scanned stability radius: {s['minimum_scanned_stability_radius']:.9g}",
                f"- first frozen angle with positive numerical abscissa: {s['first_theta_with_positive_numerical_abscissa']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Scope",
            "",
            "This is P0 within-domain synthetic/mathematical evidence. It is not physical confirmation and does not establish a new nonmodal stability law.",
            "",
        ]
    )
    return "\n".join(lines)


def reproduce_d01c(skip_tests: bool = False) -> dict:
    if not skip_tests:
        run_tests()

    freeze = load_freeze(FREEZE)
    result = run_d01c(freeze)

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D01C_NONNORMAL_DOMAIN_MAP_v0.1.json"
    summary = RESULTS / "D01C_SUMMARY_v0.1.json"
    card = RESULTS / "D01C_RESULT_CARD_v0.1.md"
    environment = RESULTS / "D01C_ENVIRONMENT_v0.1.txt"
    manifest = RESULTS / "D01C_REPRO_MANIFEST_v0.1.json"

    write_json(full, result)
    write_json(
        summary,
        {
            "schema": result["schema"],
            "status": result["status"],
            "case_count": result["case_count"],
            "max_spectral_residual": result["max_spectral_residual"],
            "eigenvalue_only_sufficiency_status": result["eigenvalue_only_sufficiency_status"],
            "family_summaries": result["family_summaries"],
            "native_toolkit_position": result["native_toolkit_position"],
        },
    )
    card.write_text(result_card(result), encoding="utf-8")
    environment.write_text(
        "\n".join(
            [
                f"python={platform.python_version()}",
                f"implementation={platform.python_implementation()}",
                f"platform={platform.platform()}",
                f"numpy={np.__version__}",
                f"scipy={scipy.__version__}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    tracked = [
        FREEZE,
        ROOT / "src" / "domain_map_nonnormal.py",
        ROOT / "tests" / "test_domain_map_nonnormal.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(
        manifest,
        {
            "schema": "d01c-repro-manifest-v0.1",
            "entrypoint": "python chi_architecture/reproduce.py d01c",
            "files": {
                str(p.relative_to(ROOT.parent)): sha256(p)
                for p in tracked
            },
        },
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Single-entry reproducibility interface for Chi Architecture experiments."
    )
    parser.add_argument("experiment", choices=["d01c"])
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip pytest only for local debugging. Do not use for archival reproduction.",
    )
    args = parser.parse_args()

    if args.experiment == "d01c":
        result = reproduce_d01c(skip_tests=args.skip_tests)
        print(json.dumps({
            "status": result["status"],
            "case_count": result["case_count"],
            "eigenvalue_only_sufficiency_status": result["eigenvalue_only_sufficiency_status"],
            "result_card": "chi_architecture/results/D01C_RESULT_CARD_v0.1.md",
            "manifest": "chi_architecture/results/D01C_REPRO_MANIFEST_v0.1.json",
        }, indent=2))


if __name__ == "__main__":
    main()
