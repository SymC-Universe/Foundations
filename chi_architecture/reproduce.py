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
from d02a_physical import fetch_locked_source, load_json as load_d02a_json  # noqa: E402
from d02a_physical_v02 import run_d02a_v02  # noqa: E402
from d02b_four_bolt import run_d02b  # noqa: E402
from d02c_wind_blade import run_d02c  # noqa: E402
from d02d_lumo import run_d02d  # noqa: E402
from d02e_jacket import run_d02e  # noqa: E402


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


def d02a_result_card_v02(result: dict) -> str:
    lines = [
        "# D02A CsPbBr3 Physical Calibration Result Card v0.2",
        "",
        f"**Status:** {result['status']}",
        f"**Evidence class:** {result['evidence_class']}",
        f"**Lowercase chi:** {result['lowercase_chi']['status']}",
        f"**DHO license:** {result['dho_license']['status']}",
        f"**Linewidth rows retained:** {len(result['linewidth_records'])}",
        "",
        "## Corrected M-R carrier matrices",
        "",
    ]
    for item in result["carrier_maps"]:
        identifiable = sum(
            1 for row in item["q_metrics"] if row["status"] == "IDENTIFIABLE"
        )
        lines.append(
            f"- {item['temperature_K']:.0f} K {item['phase']}: "
            f"{len(item['energy_axis_meV'])} x {len(item['q_axis_rlu'])} raw matrix; "
            f"{identifiable}/{len(item['q_metrics'])} q profiles identifiable"
        )

    lines.extend(["", "## Pairwise normalized-shape diagnostics", ""])
    for metric in result["pairwise_carrier_shape_metrics"]:
        lines.append(
            f"- {metric['left_temperature_K']:.0f}->{metric['right_temperature_K']:.0f} K: "
            f"centroid RMS difference={metric['centroid_rms_difference_meV']}, "
            f"width RMS difference={metric['width_rms_difference_meV']}, "
            f"centroid Pearson r={metric['centroid_pearson_r']}"
        )

    lines.extend([
        "",
        "## Scope",
        "",
        "P0-D post-result parser development only. v0.1 remains preserved as a partial failure. "
        "Absolute intensity is not compared across instruments and no chi_DHO is computed.",
        "",
    ])
    return "\n".join(lines)


def reproduce_d02a(skip_tests: bool = False) -> dict:
    if not skip_tests:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "chi_architecture/tests/test_d02a_physical.py",
                "chi_architecture/tests/test_d02a_physical_v02.py",
            ],
            check=True,
            cwd=ROOT.parent,
            env=env,
        )

    d02 = ROOT / "d02_cspbbr3"
    freeze_path = d02 / "D02A_PREEXECUTION_FREEZE_v0.1.json"
    lock_path = d02 / "D02A_SOURCE_SCHEMA_LOCK_v0.1.json"
    parser_v01_path = d02 / "D02A_PARSER_CONTRACT_v0.1.json"
    contract_v01_path = d02 / "D02A_EXECUTION_CONTRACT_v0.1.json"
    parser_v02_path = d02 / "D02A_V0.2_CARRIER_PARSER_CONTRACT.json"

    freeze = load_d02a_json(freeze_path)
    lock = load_d02a_json(lock_path)
    contract_v01 = load_d02a_json(contract_v01_path)
    parser_v02 = load_d02a_json(parser_v02_path)

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

    result = run_d02a_v02(
        freeze,
        lock,
        contract_v01,
        parser_v02,
        cache / "FIG3.xlsx",
        cache / "FIG4.xlsx",
        source_records,
    )

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D02A_CSPBBR3_PHYSICAL_RESULT_v0.2.json"
    summary = RESULTS / "D02A_CSPBBR3_SUMMARY_v0.2.json"
    card = RESULTS / "D02A_RESULT_CARD_v0.2.md"
    environment = RESULTS / "D02A_ENVIRONMENT_v0.2.txt"
    manifest = RESULTS / "D02A_REPRO_MANIFEST_v0.2.json"

    write_json(full, result)
    write_json(summary, {
        "schema": result["schema"],
        "status": result["status"],
        "evidence_class": result["evidence_class"],
        "parent_v0_1_status": result["parent_v0_1_status"],
        "lowercase_chi": result["lowercase_chi"],
        "dho_license": result["dho_license"],
        "phase_linewidth_summary": result["phase_linewidth_summary"],
        "pairwise_carrier_shape_metrics": result["pairwise_carrier_shape_metrics"],
        "carrier_q_metrics": [
            {
                "temperature_K": item["temperature_K"],
                "phase": item["phase"],
                "q_metrics": item["q_metrics"],
            }
            for item in result["carrier_maps"]
        ],
    })
    card.write_text(d02a_result_card_v02(result), encoding="utf-8")
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
        parser_v01_path,
        contract_v01_path,
        parser_v02_path,
        ROOT / "src" / "d02a_physical.py",
        ROOT / "src" / "d02a_physical_v02.py",
        ROOT / "tests" / "test_d02a_physical.py",
        ROOT / "tests" / "test_d02a_physical_v02.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(manifest, {
        "schema": "d02a-repro-manifest-v0.2",
        "entrypoint": "python chi_architecture/reproduce.py d02a",
        "files": {
            str(p.relative_to(ROOT.parent)): sha256(p)
            for p in tracked
        },
        "source_files": {
            record["id"]: {
                "sha256": record["sha256"],
                "size_bytes": record["size_bytes"],
            }
            for record in source_records
        },
    })
    return result



def d02b_result_card(result: dict) -> str:
    s = result["primary_summary"]
    lines = [
        "# D02B Four-Bolt Physical Result Card v0.1",
        "",
        f"**Status:** {result['status']}",
        f"**Evidence class:** {result['evidence_class']}",
        f"**Retained families:** {len(result['retained_families_hz'])}",
        f"**Torque states:** {result['torque_state_count']}",
        f"**Admitted scalar records:** {result['scalar_status_counts'].get('ADMITTED', 0)} / {len(result['scalar_records'])}",
        "",
        "## Frozen primary map",
        "",
        f"- primary comparisons: {s['primary_pair_count']}",
        f"- comparable chi pairs: {s['comparable_chi_pair_count']}",
        f"- similar-chi pairs: {s['similar_chi_pair_count']}",
        f"- transformed-chi pairs: {s['transformed_chi_pair_count']}",
        f"- response-reorganized pairs: {s['response_reorganized_pair_count']}",
        f"- similar-chi + reorganized pairs: {s['similar_chi_and_reorganized_pair_count']}",
        "",
        "## Family labels",
        "",
    ]
    for fam in result["family_results"]:
        lines.append(
            f"- {fam['family_hz']} Hz: "
            + (", ".join(fam["labels"]) if fam["labels"] else "NO_FAMILY_LABEL_TRIGGERED")
        )
    lines.extend([
        "",
        "## Interpretation ceiling",
        "",
        "Physical P0-Q qualification only. Added-value interpretation is deliberately not assigned by the runner.",
        "",
    ])
    return "\n".join(lines)


def reproduce_d02b(skip_tests: bool = False) -> dict:
    if not skip_tests:
        run_pytest("chi_architecture/tests/test_d02b_four_bolt.py")

    cache = ROOT / "cache" / "d02b"
    result = run_d02b(cache)

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D02B_FOUR_BOLT_PHYSICAL_RESULT_v0.1.json"
    summary = RESULTS / "D02B_SUMMARY_v0.1.json"
    card = RESULTS / "D02B_RESULT_CARD_v0.1.md"
    environment = RESULTS / "D02B_ENVIRONMENT_v0.1.txt"
    manifest = RESULTS / "D02B_REPRO_MANIFEST_v0.1.json"

    write_json(full, result)
    write_json(summary, {
        "schema": result["schema"],
        "status": result["status"],
        "evidence_class": result["evidence_class"],
        "retained_families_hz": result["retained_families_hz"],
        "scalar_status_counts": result["scalar_status_counts"],
        "primary_summary": result["primary_summary"],
        "family_results": result["family_results"],
        "tracked_frequency_crosschecks": result["tracked_frequency_crosschecks"],
        "source_files": result["source_files"],
        "scope": result["scope"],
    })
    card.write_text(d02b_result_card(result), encoding="utf-8")
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
        ROOT / "d02b" / "D02B_CANDIDATE_SELECTION_FREEZE_v0.1.md",
        ROOT / "d02b" / "D02B_CANDIDATE_SELECTION_CORRECTION_v0.3.md",
        ROOT / "d02b" / "D02B_FOUR_BOLT_SOURCE_CONTRACT_v0.3.md",
        ROOT / "d02b" / "D02B_EXACT_SOURCE_MAPPING_v0.1.md",
        ROOT / "d02b" / "D02B_RAW_PARSER_AND_CLASSIFICATION_FREEZE_v0.1.md",
        ROOT / "src" / "d02b_four_bolt.py",
        ROOT / "tests" / "test_d02b_four_bolt.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(manifest, {
        "schema": "d02b-repro-manifest-v0.1",
        "entrypoint": "python chi_architecture/reproduce.py d02b",
        "files": {
            str(p.relative_to(ROOT.parent)): sha256(p)
            for p in tracked
        },
        "source_files": result["source_files"],
    })
    return result


def d02c_result_card(result: dict) -> str:
    lines = [
        "# D02C Wind-Blade Prospective Result Card v0.1",
        "",
        f"**Status:** {result['status']}",
        f"**Evidence class:** {result['evidence_class']}",
        f"**CA-D007 domain-specific support flag:** {result['ca_d007_domain_specific_support']}",
        "",
        "## Selected modes",
        "",
    ]
    for direction in ("X", "Z"):
        mode = result["selected_modes"][direction]
        ordering = result["orderings"][direction]
        lines.extend([
            f"### {direction}",
            "",
            f"- baseline presence: {mode['baseline_presence']}/12",
            f"- baseline median frequency: {mode['baseline_median_frequency_hz']:.9g} Hz",
            f"- prospective ordering: {ordering['outcome']}",
            f"- scalar onset: {ordering.get('scalar_onset_window_start')}",
            f"- organization onset: {ordering.get('organization_onset_window_start')}",
            "",
        ])
    lines.extend([
        "## Interpretation ceiling",
        "",
        "This card reports the prospectively frozen result only. The native-toolkit added-value verdict is intentionally assigned after archival checkpointing.",
        "",
    ])
    return "\n".join(lines)


def reproduce_d02c(skip_tests: bool = False) -> dict:
    if not skip_tests:
        run_pytest("chi_architecture/tests/test_d02c_wind_blade.py")

    cache = ROOT / "cache" / "d02c"
    result = run_d02c(cache)

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D02C_WIND_BLADE_RESULT_v0.1.json"
    summary = RESULTS / "D02C_SUMMARY_v0.1.json"
    card = RESULTS / "D02C_RESULT_CARD_v0.1.md"
    environment = RESULTS / "D02C_ENVIRONMENT_v0.1.txt"
    manifest = RESULTS / "D02C_REPRO_MANIFEST_v0.1.json"

    write_json(full, result)
    write_json(summary, {
        "schema": result["schema"],
        "status": result["status"],
        "evidence_class": result["evidence_class"],
        "selected_modes": result["selected_modes"],
        "scalar_control_envelopes": result["scalar_control_envelopes"],
        "organization_midnight_thresholds": result["organization_midnight_thresholds"],
        "organization_dry_thresholds": result["organization_dry_thresholds"],
        "organization_effective_thresholds": result["organization_effective_thresholds"],
        "orderings": result["orderings"],
        "ca_d007_domain_specific_support": result["ca_d007_domain_specific_support"],
        "source_files": result["source_files"],
        "scope": result["scope"],
    })
    card.write_text(d02c_result_card(result), encoding="utf-8")
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
        ROOT / "d02c" / "D02C_CANDIDATE_SELECTION_FREEZE_v0.1.md",
        ROOT / "d02c" / "D02C_CANDIDATE_SELECTION_RECORD_v0.2.md",
        ROOT / "d02c" / "D02C_WIND_BLADE_CONTRACT_v0.1.md",
        ROOT / "d02c" / "D02C_WIND_EXACT_MAPPING_v0.1.md",
        ROOT / "d02c" / "D02C_DRY_PEAK_ADEQUACY_ADDENDUM_v0.1.md",
        ROOT / "d02c" / "D02C_ONSET_COMPLETENESS_RULE_v0.1.md",
        ROOT / "src" / "d02c_wind_blade.py",
        ROOT / "tests" / "test_d02c_wind_blade.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(manifest, {
        "schema": "d02c-repro-manifest-v0.1",
        "entrypoint": "python chi_architecture/reproduce.py d02c",
        "files": {
            str(p.relative_to(ROOT.parent)): sha256(p)
            for p in tracked
        },
        "source_files": result["source_files"],
    })
    return result


def d02d_result_card(result: dict) -> str:
    lines = [
        "# D02D LUMO Prospective Result Card v0.1",
        "",
        f"**Status:** {result['status']}",
        f"**Claim ID:** {result['claim_id']}",
        f"**Outcome:** {result['outcome']}",
        f"**Native-toolkit verdict:** {result['native_toolkit_verdict']}",
        "",
        "## Frozen location orderings",
        "",
    ]
    for location in ("DAM3", "DAM4", "DAM6"):
        lines.append(f"- {location}: {result['location_orderings'][location]}")
        for direction in ("X", "Y"):
            d = result["locations"][location]["directions"].get(direction, {})
            lines.append(f"  - {direction}: {d.get('ordering', 'ORDERING_NON_IDENTIFIABLE')}")
    lines.extend([
        "",
        "## Scope",
        "",
        "This is the prospectively frozen D02D external physical test of CA-D007. "
        "The result must be interpreted under the frozen MFR-14 consequence table.",
        "",
    ])
    return "\n".join(lines)


def reproduce_d02d(skip_tests: bool = False) -> dict:
    if not skip_tests:
        run_pytest("chi_architecture/tests/test_d02d_lumo.py")

    cache = ROOT / "cache" / "d02d"
    result = run_d02d(cache)

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D02D_LUMO_PROSPECTIVE_RESULT_v0.1.json"
    summary = RESULTS / "D02D_SUMMARY_v0.1.json"
    card = RESULTS / "D02D_RESULT_CARD_v0.1.md"
    environment = RESULTS / "D02D_ENVIRONMENT_v0.1.txt"
    manifest = RESULTS / "D02D_REPRO_MANIFEST_v0.1.json"

    write_json(full, result)
    write_json(summary, {
        "schema": result["schema"],
        "status": result["status"],
        "claim_id": result["claim_id"],
        "location_orderings": result["location_orderings"],
        "outcome": result["outcome"],
        "native_toolkit_verdict": result["native_toolkit_verdict"],
        "analysis": result["analysis"],
        "source_files": result["source_files"],
        "scope": result["scope"],
    })
    card.write_text(d02d_result_card(result), encoding="utf-8")
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
        ROOT / "d02d" / "D02D_CANDIDATE_SELECTION_FREEZE_v0.1.md",
        ROOT / "d02d" / "D02D_CANDIDATE_SELECTION_RECORD_v0.1.md",
        ROOT / "d02d" / "D02D_LUMO_MFR14_v0.1.md",
        ROOT / "d02d" / "D02D_LUMO_SOURCE_LOCK_v0.1.json",
        ROOT / "d02d" / "D02D_LUMO_FINAL_PREEXECUTION_FREEZE_v0.1.md",
        ROOT / "src" / "d02d_lumo.py",
        ROOT / "tests" / "test_d02d_lumo.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(manifest, {
        "schema": "d02d-repro-manifest-v0.1",
        "entrypoint": "python chi_architecture/reproduce.py d02d",
        "files": {
            str(p.relative_to(ROOT.parent)): sha256(p)
            for p in tracked
        },
        "source_files": result["source_files"],
    })
    return result


def d02e_result_card(result: dict) -> str:
    lines = [
        "# D02E Offshore-Jacket Prospective Result Card v0.1",
        "",
        f"**Status:** {result['status']}",
        f"**Claim ID:** {result['claim_id']}",
        f"**Primary family:** {result['primary_family_hz']:.9g} Hz",
        f"**Outcome:** {result['outcome']}",
        f"**Native-toolkit verdict:** {result['native_toolkit_verdict']}",
        "",
        "## Frozen location orderings",
        "",
    ]
    for location in ("level_1", "level_2", "level_3", "level_4"):
        item = result["locations"][location]
        lines.append(f"- {location}: {item['ordering']['outcome']}")
        for state in ("9Nm", "6Nm", "NoBolt"):
            s = item["states"][state]
            lines.append(
                f"  - {state}: scalar={s['scalar_status']} "
                f"(n={s['scalar_admitted_n']}), organization={s['organization_status']} "
                f"(n={s['organization']['valid_n']})"
            )
    lines.extend([
        "",
        "## Scope",
        "",
        "This is the prospectively frozen D02E primary A_1 test of CA-D007. "
        "Secondary mode and alternate excitation amplitudes cannot alter the primary verdict.",
        "",
    ])
    return "\n".join(lines)


def reproduce_d02e(skip_tests: bool = False) -> dict:
    if not skip_tests:
        run_pytest("chi_architecture/tests/test_d02e_jacket.py")

    result = run_d02e()

    RESULTS.mkdir(parents=True, exist_ok=True)
    full = RESULTS / "D02E_JACKET_PROSPECTIVE_RESULT_v0.1.json"
    summary = RESULTS / "D02E_SUMMARY_v0.1.json"
    card = RESULTS / "D02E_RESULT_CARD_v0.1.md"
    environment = RESULTS / "D02E_ENVIRONMENT_v0.1.txt"
    manifest = RESULTS / "D02E_REPRO_MANIFEST_v0.1.json"

    write_json(full, result)
    write_json(summary, {
        "schema": result["schema"],
        "status": result["status"],
        "claim_id": result["claim_id"],
        "primary_family_hz": result["primary_family_hz"],
        "healthy": result["healthy"],
        "location_orderings": result["location_orderings"],
        "outcome": result["outcome"],
        "native_toolkit_verdict": result["native_toolkit_verdict"],
        "source_counts": result["source_counts"],
        "scope": result["scope"],
    })
    card.write_text(d02e_result_card(result), encoding="utf-8")
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
        ROOT / "d02e" / "D02E_CANDIDATE_SELECTION_FREEZE_v0.1.md",
        ROOT / "d02e" / "D02E_CANDIDATE_SELECTION_RECORD_v0.1.md",
        ROOT / "d02e" / "D02E_JACKET_MFR14_v0.1.md",
        ROOT / "d02e" / "D02E_FINAL_PREEXECUTION_FREEZE_v0.1.md",
        ROOT / "results" / "D02E_HEALTHY_SELECTION_ARCHIVE_v0.1.json",
        ROOT / "src" / "d02e_jacket.py",
        ROOT / "tests" / "test_d02e_jacket.py",
        Path(__file__).resolve(),
        full,
        summary,
        card,
        environment,
    ]
    write_json(manifest, {
        "schema": "d02e-repro-manifest-v0.1",
        "entrypoint": "python chi_architecture/reproduce.py d02e",
        "files": {
            str(p.relative_to(ROOT.parent)): sha256(p)
            for p in tracked
        },
        "source_files": result["source_files"],
    })
    return result

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Single-entry reproducibility interface for Chi Architecture experiments."
    )
    parser.add_argument("experiment", choices=["d01c", "d02a", "d02b", "d02c", "d02d", "d02e"])
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
    elif args.experiment == "d02a":
        result = reproduce_d02a(skip_tests=args.skip_tests)
        print(json.dumps({
            "status": result["status"],
            "evidence_class": result["evidence_class"],
            "lowercase_chi": result["lowercase_chi"]["status"],
            "dho_license": result["dho_license"]["status"],
            "result_card": "chi_architecture/results/D02A_RESULT_CARD_v0.2.md",
            "manifest": "chi_architecture/results/D02A_REPRO_MANIFEST_v0.2.json",
        }, indent=2))
    elif args.experiment == "d02b":
        result = reproduce_d02b(skip_tests=args.skip_tests)
        print(json.dumps({
            "status": result["status"],
            "evidence_class": result["evidence_class"],
            "primary_summary": result["primary_summary"],
            "result_card": "chi_architecture/results/D02B_RESULT_CARD_v0.1.md",
            "manifest": "chi_architecture/results/D02B_REPRO_MANIFEST_v0.1.json",
        }, indent=2))
    elif args.experiment == "d02c":
        result = reproduce_d02c(skip_tests=args.skip_tests)
        print(json.dumps({
            "status": result["status"],
            "evidence_class": result["evidence_class"],
            "orderings": result["orderings"],
            "ca_d007_domain_specific_support": result["ca_d007_domain_specific_support"],
            "result_card": "chi_architecture/results/D02C_RESULT_CARD_v0.1.md",
            "manifest": "chi_architecture/results/D02C_REPRO_MANIFEST_v0.1.json",
        }, indent=2))
    elif args.experiment == "d02d":
        result = reproduce_d02d(skip_tests=args.skip_tests)
        print(json.dumps({
            "status": result["status"],
            "claim_id": result["claim_id"],
            "location_orderings": result["location_orderings"],
            "outcome": result["outcome"],
            "result_card": "chi_architecture/results/D02D_RESULT_CARD_v0.1.md",
            "manifest": "chi_architecture/results/D02D_REPRO_MANIFEST_v0.1.json",
        }, indent=2))
    else:
        result = reproduce_d02e(skip_tests=args.skip_tests)
        print(json.dumps({
            "status": result["status"],
            "claim_id": result["claim_id"],
            "primary_family_hz": result["primary_family_hz"],
            "location_orderings": result["location_orderings"],
            "outcome": result["outcome"],
            "result_card": "chi_architecture/results/D02E_RESULT_CARD_v0.1.md",
            "manifest": "chi_architecture/results/D02E_REPRO_MANIFEST_v0.1.json",
        }, indent=2))


if __name__ == "__main__":
    main()
