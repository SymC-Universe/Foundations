#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_SELECTION_SHA = "364ba6a18b5ea8b8cad7a164028013bf605db5a44f847bcc9e1d13dfacb46de5"
EXPECTED_H10_CODE_SHA256 = "1ab51476fef7e6bf37da92a889054f8a688fbaf03aa2c5a2ae708a4c97bac350"
EXPECTED_COUNT = 64

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "dephasing_d_replication_blind_reveal_v01.json"
H10_SOURCE = ROOT.parent / "dephasing_crossing_v01" / "dephasing_crossing_transfer_v01.py"
PREFIX_MARKER = "# X0: deterministic generator and Stage A exact c1/c3-only screening."


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_closed_h10_definitions():
    src_bytes = H10_SOURCE.read_bytes()
    src_sha = sha256_bytes(src_bytes)
    if src_sha != EXPECTED_H10_CODE_SHA256:
        raise RuntimeError(f"H10 source SHA mismatch: {src_sha}")
    text = src_bytes.decode("utf-8")
    if PREFIX_MARKER not in text:
        raise RuntimeError("H10 prefix marker missing")
    prefix = text.split(PREFIX_MARKER, 1)[0]
    ns = {"__file__": str(H10_SOURCE), "__name__": "h10_closed_definitions"}
    exec(compile(prefix, str(H10_SOURCE), "exec"), ns, ns)
    return ns, src_sha


def main(selection_path):
    selection_path = Path(selection_path)
    raw = selection_path.read_bytes()
    selection_sha = sha256_bytes(raw)
    if selection_sha != EXPECTED_SELECTION_SHA:
        result = {"status": "PROVENANCE_HOLD", "reason": "SELECTION_SHA_MISMATCH", "observed_sha256": selection_sha}
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    payload = json.loads(raw.decode("utf-8"))
    rows = payload.get("selected", [])
    if len(rows) != EXPECTED_COUNT or payload.get("available_total", 0) < 16:
        result = {"status": "PROVENANCE_HOLD", "reason": "SELECTION_COUNT_OR_READINESS", "selected_count": len(rows), "available_total": payload.get("available_total")}
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    try:
        ns, h10_source_sha = load_closed_h10_definitions()
    except Exception as exc:
        result = {"status": "PROVENANCE_HOLD", "reason": "H10_SOURCE_BINDING", "detail": str(exc)}
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    canonical_scalar = ns["canonical_scalar"]
    full_matrices = ns["full_matrices"]
    dark_space = ns["dark_space"]
    quotient_full = ns["quotient_full"]
    canonical_matrices = ns["canonical_matrices"]
    Gnum = ns["Gnum"]
    rh = ns["rh"]
    Kfull = ns["Kfull"]
    max_abs = ns["max_abs"]
    relabs = ns["relabs"]
    MAP_TOL = ns["MAP_TOL"]
    RH_TOL = ns["RH_TOL"]
    RECON_TOL = ns["RECON_TOL"]
    MATRIX_TOL = ns["MATRIX_TOL"]
    MOMENT_TOL = ns["MOMENT_TOL"]

    replay_failures = []
    for f in rows:
        m = canonical_scalar(f)
        ok = (
            abs(m["delta"])/m["R"] > MAP_TOL
            and m["c1p"]/m["R"] > MAP_TOL
            and m["c3p"]/m["R"]**3 > MAP_TOL
            and m["c3r"]/m["R"]**3 < -MAP_TOL
        )
        if not ok:
            replay_failures.append(f["id"])

    if replay_failures:
        result = {"status": "PROVENANCE_HOLD", "reason": "STAGE_A_REPLAY", "replay_failures": replay_failures}
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"status": result["status"], "reason": result["reason"], "count": len(replay_failures)}, indent=2))
        return

    recon_failures = []
    boundary_rows = []
    counterexamples = []
    correct = 0
    blockers = {"m2": 0, "mh": 0}
    max_matrix_error = 0.0
    max_c13_error = 0.0
    max_moment_error = 0.0

    for f in rows:
        rho, A, Ar, B, Vt, imag = full_matrices(f)
        reasons = []
        rho_min = float(ns["np"].min(ns["np"].linalg.eigvalsh(rho)))
        singular_values, D = dark_space(A, Vt)
        if rho_min <= 0.0:
            reasons.append("NONPOSITIVE_DENSITY")
        if D.shape[1] != 1:
            reasons.append("DARK_DIMENSION")

        Apf, Arf, Bf, L, C = quotient_full(f, A, Ar, B)
        Apc, Arc, Bc, meta = canonical_matrices(f)
        matrix_error = max(max_abs(Apf-Apc), max_abs(Arf-Arc), max_abs(Bf-Bc))
        max_matrix_error = max(max_matrix_error, matrix_error)
        if matrix_error > MATRIX_TOL:
            reasons.append("CANONICAL_MATRIX")

        Gp, Gr = Gnum(Apf, Bf), Gnum(Arf, Bf)
        rp, rr = rh(Gp, meta["R"]), rh(Gr, meta["R"])
        c13_error = max(
            relabs(rp["c1"], meta["c1p"]), relabs(rr["c1"], meta["c1r"]),
            relabs(rp["c3"], meta["c3p"]), relabs(rr["c3"], meta["c3r"]),
        )
        max_c13_error = max(max_c13_error, c13_error)
        if c13_error > RECON_TOL:
            reasons.append("C1_C3_RECONSTRUCTION")

        J = ns["np"].kron(L, L)
        moment_error = max(
            max_abs(J@Kfull(A, B)-Kfull(Apf, Bf)@J),
            max_abs(J@Kfull(Ar, B)-Kfull(Arf, Bf)@J),
        )
        max_moment_error = max(max_moment_error, moment_error)
        if moment_error > MOMENT_TOL:
            reasons.append("MOMENT_INTERTWINING")
        if imag > 1e-11:
            reasons.append("NONREAL")

        if reasons:
            recon_failures.append({
                "id": f["id"], "reasons": reasons, "rho_min": rho_min,
                "singular_values": [float(x) for x in singular_values],
                "matrix_error": matrix_error, "c13_error": c13_error,
                "moment_error": moment_error,
            })
            continue

        record = {"id": f["id"], "shell": f["shell"], "physical": rp, "record": rr}
        if rp["class"] == "BOUNDARY" or rr["class"] == "BOUNDARY":
            boundary_rows.append(record)
            continue

        if rp["class"] == "STABLE" and rr["class"] == "UNSTABLE":
            correct += 1
        else:
            missing = []
            if rp["margins"]["m2"] <= RH_TOL:
                missing.append("m2")
                blockers["m2"] += 1
            if rp["margins"]["mh"] <= RH_TOL:
                missing.append("mh")
                blockers["mh"] += 1
            counterexamples.append({**record, "blocking_margins": missing})

    if recon_failures:
        status = "RECONSTRUCTION_HOLD"
    elif boundary_rows:
        status = "BOUNDARY_HOLD"
    elif counterexamples:
        status = "FAIL_H12D_REPLICATION"
    else:
        status = "PASS_H12D_REPLICATION"

    result = {
        "schema": "stability-arc-dephasing-d-replication-blind-reveal-v0.1",
        "status": status,
        "selection_sha256": selection_sha,
        "h10_source_sha256": h10_source_sha,
        "frozen_count": len(rows),
        "correct_count": correct,
        "counterexample_count": len(counterexamples),
        "blockers": blockers,
        "boundary_count": len(boundary_rows),
        "reconstruction_failure_count": len(recon_failures),
        "max_matrix_error": max_matrix_error,
        "max_c13_error": max_c13_error,
        "max_moment_error": max_moment_error,
        "counterexamples": counterexamples,
        "boundary_rows": boundary_rows,
        "reconstruction_failures": recon_failures,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["status", "frozen_count", "correct_count", "counterexample_count", "blockers", "boundary_count", "reconstruction_failure_count", "max_matrix_error", "max_c13_error", "max_moment_error"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: dephasing_d_replication_blind_reveal_v01.py <stageA_selection.json>")
    main(sys.argv[1])
