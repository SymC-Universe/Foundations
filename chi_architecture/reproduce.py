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
D01C_FREEZE = ROOT / "D01C_PREEXECUTION_FREEZE_v0.1.json"

sys.path.insert(0, str(SRC))

from domain_map_nonnormal import load_freeze, run_d01c  # noqa: E402
from d02a_physical import fetch_locked_source, load_json as load_d02a_json, run_d02a  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_pytest(test_path: str) -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC)
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", test_path],
        check=True,
        cwd=ROOT.parent,
        env=env,
    )


def d01c_result_card(result: dict) -> str:
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
        lines.extend([
            f"### {s['family_id']} | eigenvalues {s['eigenvalues']}",
            "",
            f"- spectral abscissa: {s['spectral_abscissa']:.6g}",
            f"- normal max operator state gain: {s['normal_max_operator_state_gain']:.9g}",
            f"- smallest-angle max operator state gain: {s['smallest_theta_max_operator_state_gain']:.9g}",
            f"- gain ratio: {s['state_gain_ratio_smallest_theta_to_normal']:.9g}",
            f"- minimum scanned stability radius: {s['minimum_scanned_stability_radius']:.9g}",
            f"- first frozen angle with positive numerical abscissa: {s['first_theta_with_positive_numerical_abscissa']}",
            "",
        ])
    lines.extend([
        "## Scope",
        "",
        "This is P0 within-domain synthetic/mathematical evidence. It is not physical confirmation and does not establish a new nonmodal stability law.",
        "",
    ])
    return "\n".join(lines)


def reproduce_d01c(skip_tests: bool = False) -> dict:
    if not skip_tests:
        run_pytest("chi_architecture/tests/test_domain_map_nonnormal.py")

    freeze = load_freeze(D01C_FREEZE)
    result = run_d01c(freeze)

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D01C_NONNORMAL_DOMAIN_MAP_v0.1.json"
    summary = RESULTS / "D01C_SUMMARY_v0.1.json"
    card = RESULTS / "D01C_RESULT_CARD_v0.1.md"
    environment = RESULTS / "D01C_ENVIRONMENT_v0.1.txt"
    manifest = RESULTS / "D01C_REPRO_MANIFEST_v0.1.json"

    write_json(full, result)
    write_json(summary, {
        "schema": result["schema"],
        "status": result["status"],
        "case_count": result["case_count"],
        "max_spectral_residual": result["max_spectral_residual"],
        "eigenvalue_only_sufficiency_status": result["eigenvalue_only_sufficiency_status"],
        "family_summaries": result["family_summaries"],
        "native_toolkit_position": result["native_toolkit_position"],
    })
    card.write_text(d01c_result_card(result), encoding="utf-8")
    environment.write_text(
        "\n".join([
            f"python={platform.python_version()}",
            f"implementation={platform.python_implementation()}",
            f"platform={platform.platform()}",
            f"numpy={np.__version__}",
            f"scipy={scipy.__version__}",
        ]) + "\n",
        encoding="utf-8",
    )

    tracked = [
        D01C_FREEZE,
        ROOT / "src" / "domain_map_nonnormal.py",
        ROOT / "tests" / "test_domain_map_nonnormal.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(manifest, {
        "schema": "d01c-repro-manifest-v0.1",
        "entrypoint": "python chi_architecture/reproduce.py d01c",
        "files": {str(p.relative_to(ROOT.parent)): sha256(p) for p in tracked},
    })
    return result


def d02a_result_card(result: dict) -> str:
    lines = [
        "# D02A CsPbBr3 Physical Calibration Result Card",
        "",
        f"**Status:** {result['status']}",
        f"**Evidence class:** {result['evidence_class']}",
        f"**Lowercase chi:** {result['lowercase_chi']['status']}",
        f"**DHO license:** {result['dho_license']['status']}",
        f"**Linewidth rows:** {len(result['linewidth_records'])}",
        "",
        "## Carrier maps",
        "",
    ]
    for item in result["carrier_maps"]:
        s = item["summary"]
        lines.append(
            f"- {item['temperature_K']:.0f} K {item['phase']}: "
            f"{s['row_count']} source rows, {s['unique_q_count']} unique q values"
        )
    lines.extend([
        "",
        "## Scope",
        "",
        "P0-D physical calibration only. No untouched confirmation. "
        "No chi_DHO is computed because the locked source tables do not tabulate same-condition omega0.",
        "",
    ])
    return "\n".join(lines)


def reproduce_d02a(skip_tests: bool = False) -> dict:
    if not skip_tests:
        run_pytest("chi_architecture/tests/test_d02a_physical.py")

    d02 = ROOT / "d02_cspbbr3"
    freeze_path = d02 / "D02A_PREEXECUTION_FREEZE_v0.1.json"
    lock_path = d02 / "D02A_SOURCE_SCHEMA_LOCK_v0.1.json"
    parser_path = d02 / "D02A_PARSER_CONTRACT_v0.1.json"
    contract_path = d02 / "D02A_EXECUTION_CONTRACT_v0.1.json"

    freeze = load_d02a_json(freeze_path)
    lock = load_d02a_json(lock_path)
    contract = load_d02a_json(contract_path)

    cache = ROOT / "cache" / "d02a"
    cache.mkdir(parents=True, exist_ok=True)

    sources = {x["id"]: x for x in freeze["source"]["publisher_source_data"]}
    source_records = []
    for source_id in ("FIG3", "FIG4"):
        source_records.append(
            fetch_locked_source(
                sources[source_id],
                lock["sources"][source_id]["sha256"],
                cache / f"{source_id}.xlsx",
            )
        )

    result = run_d02a(
        freeze,
        contract,
        cache / "FIG3.xlsx",
        cache / "FIG4.xlsx",
        source_records,
    )

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D02A_CSPBBR3_PHYSICAL_RESULT_v0.1.json"
    summary = RESULTS / "D02A_CSPBBR3_SUMMARY_v0.1.json"
    card = RESULTS / "D02A_RESULT_CARD_v0.1.md"
    environment = RESULTS / "D02A_ENVIRONMENT_v0.1.txt"
    manifest = RESULTS / "D02A_REPRO_MANIFEST_v0.1.json"

    write_json(full, result)
    write_json(summary, {
        "schema": result["schema"],
        "status": result["status"],
        "evidence_class": result["evidence_class"],
        "lowercase_chi": result["lowercase_chi"],
        "dho_license": result["dho_license"],
        "phase_linewidth_summary": result["phase_linewidth_summary"],
        "carrier_summaries": [
            {
                "temperature_K": x["temperature_K"],
                "phase": x["phase"],
                "role": x["role"],
                "summary": x["summary"],
            }
            for x in result["carrier_maps"]
        ],
    })
    card.write_text(d02a_result_card(result), encoding="utf-8")
    environment.write_text(
        "\n".join([
            f"python={platform.python_version()}",
            f"implementation={platform.python_implementation()}",
            f"platform={platform.platform()}",
            f"numpy={np.__version__}",
            f"scipy={scipy.__version__}",
        ]) + "\n",
        encoding="utf-8",
    )

    tracked = [
        freeze_path,
        lock_path,
        parser_path,
        contract_path,
        ROOT / "src" / "d02a_physical.py",
        ROOT / "tests" / "test_d02a_physical.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(manifest, {
        "schema": "d02a-repro-manifest-v0.1",
        "entrypoint": "python chi_architecture/reproduce.py d02a",
        "files": {str(p.relative_to(ROOT.parent)): sha256(p) for p in tracked},
        "source_files": {
            record["id"]: {
                "sha256": record["sha256"],
                "size_bytes": record["size_bytes"],
            }
            for record in source_records
        },
    })
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Single-entry reproducibility interface for Chi Architecture experiments."
    )
    parser.add_argument("experiment", choices=["d01c", "d02a"])
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
    else:
        result = reproduce_d02a(skip_tests=args.skip_tests)
        print(json.dumps({
            "status": result["status"],
            "evidence_class": result["evidence_class"],
            "lowercase_chi": result["lowercase_chi"]["status"],
            "dho_license": result["dho_license"]["status"],
            "result_card": "chi_architecture/results/D02A_RESULT_CARD_v0.1.md",
            "manifest": "chi_architecture/results/D02A_REPRO_MANIFEST_v0.1.json",
        }, indent=2))


if __name__ == "__main__":
    main()
