#!/usr/bin/env python3
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
OUT = RESULTS / "dephasing_d_availability_v01.json"
SELECTION = RESULTS / "stageA_dephasing_d_selection.json"
SELECTION_SHA = RESULTS / "stageA_dephasing_d_selection.sha256"

SEED = 2026082921
N_PER_SHELL = 5_000_000
CHUNK = 100_000
MAX_FREEZE = 64
MIN_READY = 16
MAP_TOL = 1e-8
SHELLS = [("S3", 0.90, 0.98), ("S4", 0.98, 0.9999)]


def exact_c3(p, d, h, w, q, u, v, record=False):
    if not record:
        F = (
            -d*d*p + 4*d*d*q*u*u + d*h*h + 4*d*h*q*u*v - d*p*p
            + 9*d*p*q*u*u - 20*d*q*q*u**4 - 4*d*q*u*v*w - d*w*w
            + h*h*p - 5*h*h*q*u*u + h*h*q*v*v + 2*h*p*q*u*v
            - 12*h*q*q*u**3*v - 2*h*q*v*v*w + p*p*q*u*u
            - 8*p*q*q*u**4 - 2*p*q*u*v*w - p*w*w + 16*q**3*u**6
            + 12*q*q*u**3*v*w + 5*q*u*u*w*w + q*v*v*w*w
        )
    else:
        F = (
            -d*d*p + 6*d*d*q*u*u - 2*d*d*q + d*h*h + 6*d*h*q*u*v
            - d*p*p + 13*d*p*q*u*u - 4*d*p*q - 42*d*q*q*u**4
            + 26*d*q*q*u*u - 4*d*q*q - 6*d*q*u*v*w - d*w*w
            + h*h*p - 7*h*h*q*u*u + h*h*q*v*v + 2*h*h*q
            + 4*h*p*q*u*v - 30*h*q*q*u**3*v + 8*h*q*q*u*v
            - 2*h*q*v*v*w + p*p*q*u*u - 12*p*q*q*u**4
            + 4*p*q*q*u*u - 4*p*q*u*v*w - p*w*w + 36*q**3*u**6
            - 24*q**3*u**4 + 4*q**3*u*u + 30*q*q*u**3*v*w
            - 8*q*q*u*v*w + 7*q*u*u*w*w + q*v*v*w*w - 2*q*w*w
        )
    return -4.0 * F


def arr_hash_update(hsh, key, arr):
    hsh.update(key.encode("ascii") + b"\0")
    hsh.update(np.asarray(arr, dtype="<f8").tobytes(order="C"))


def make_row(shell, global_index, i, gamma, gamma_phi, kappa, eta, omega, theta,
             radius, x, y, z, q, u, v, delta, R, c1p, c3p, c3r):
    return {
        "id": f"DPA{global_index:08d}",
        "global_index": int(global_index),
        "shell": shell,
        "gamma": float(gamma[i]),
        "gamma_phi": float(gamma_phi[i]),
        "kappa": float(kappa[i]),
        "eta": float(eta[i]),
        "omega": float(omega[i]),
        "theta": float(theta[i]),
        "r": float(radius[i]),
        "x": float(x[i]),
        "y": float(y[i]),
        "z": float(z[i]),
        "q": float(q[i]),
        "u": float(u[i]),
        "v": float(v[i]),
        "delta_norm": float(abs(delta[i]) / R[i]),
        "c1_phys_norm": float(c1p[i] / R[i]),
        "c3_phys_norm": float(c3p[i] / R[i]**3),
        "c3_record_norm": float(c3r[i] / R[i]**3),
    }


def execute():
    rng = np.random.default_rng(SEED)
    selected = []
    shell_counts = {}
    shell_hashes = {}
    total_generated = 0

    for shell_index, (shell, lo, hi) in enumerate(SHELLS):
        count = 0
        sh = hashlib.sha256()
        sh.update(f"seed={SEED};shell={shell};n={N_PER_SHELL};chunk={CHUNK};schema=dephasing-d-availability-v0.1\n".encode("ascii"))
        shell_offset = shell_index * N_PER_SHELL

        for start in range(0, N_PER_SHELL, CHUNK):
            n = min(CHUNK, N_PER_SHELL - start)
            gamma = 10.0 ** rng.uniform(math.log10(0.1), math.log10(2.0), n)
            gamma_phi = 10.0 ** rng.uniform(math.log10(0.001), math.log10(2.0), n)
            kappa = 10.0 ** rng.uniform(math.log10(0.05), math.log10(5.0), n)
            eta = rng.uniform(0.01, 0.95, n)
            omega = 10.0 ** rng.uniform(math.log10(0.02), math.log10(10.0), n)
            theta = rng.uniform(-math.pi, math.pi, n)
            radius = rng.uniform(lo, hi, n)
            dirs = rng.normal(size=(n, 3))
            dirs /= np.linalg.norm(dirs, axis=1)[:, None]
            xyz = radius[:, None] * dirs
            x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
            q = eta * kappa

            for key, arr in [
                ("gamma", gamma), ("gamma_phi", gamma_phi), ("kappa", kappa),
                ("eta", eta), ("omega", omega), ("theta", theta), ("r", radius),
                ("x", x), ("y", y), ("z", z), ("q", q),
            ]:
                arr_hash_update(sh, key, arr)

            sn, cs = np.sin(theta), np.cos(theta)
            a = 0.5 * gamma + gamma_phi
            b = gamma
            u = sn*x + cs*z
            v = cs*x - sn*z
            p = a*sn*sn + b*cs*cs
            d = kappa + a*cs*cs + b*sn*sn
            h = (b-a)*sn*cs
            delta = omega - h
            R = a + b + kappa + omega + q
            c1p = 3.0*(p+d) - 14.0*q*u*u
            c3p = exact_c3(p, d, h, omega, q, u, v, False)
            c3r = exact_c3(p, d, h, omega, q, u, v, True)

            mask = (
                (np.abs(delta)/R > MAP_TOL)
                & (c1p/R > MAP_TOL)
                & (c3p/R**3 > MAP_TOL)
                & (c3r/R**3 < -MAP_TOL)
            )
            idx = np.flatnonzero(mask)
            count += int(idx.size)

            if len(selected) < MAX_FREEZE and idx.size:
                for ii in idx:
                    if len(selected) >= MAX_FREEZE:
                        break
                    global_index = shell_offset + start + int(ii) + 1
                    selected.append(make_row(
                        shell, global_index, int(ii), gamma, gamma_phi, kappa, eta,
                        omega, theta, radius, x, y, z, q, u, v, delta, R, c1p, c3p, c3r
                    ))
            total_generated += n

        shell_counts[shell] = count
        shell_hashes[shell] = sh.hexdigest()

    payload = {
        "schema": "stability-arc-dephasing-d-availability-stageA-v0.1",
        "seed": SEED,
        "n_per_shell": N_PER_SHELL,
        "n_total": total_generated,
        "chunk_size": CHUNK,
        "map_tolerance": MAP_TOL,
        "shells": [{"name": s, "lo": lo, "hi": hi} for s, lo, hi in SHELLS],
        "shell_hashes": shell_hashes,
        "available_counts": shell_counts,
        "available_total": int(sum(shell_counts.values())),
        "selected": selected,
    }
    selection_bytes = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    SELECTION.write_bytes(selection_bytes)
    selection_sha = hashlib.sha256(selection_bytes).hexdigest()
    SELECTION_SHA.write_text(selection_sha + "  stageA_dephasing_d_selection.json\n", encoding="utf-8")

    replay_sha = hashlib.sha256(SELECTION.read_bytes()).hexdigest()
    deterministic_hash_ok = replay_sha == selection_sha
    ready = deterministic_hash_ok and payload["available_total"] >= MIN_READY
    status = "READY_FOR_BLIND_REVEAL_H11" if ready else (
        "SELECTION_HOLD_H11" if deterministic_hash_ok else "MECHANICAL_OR_PROVENANCE_HOLD"
    )

    result = {
        "schema": "stability-arc-dephasing-d-availability-v0.1",
        "environment": {"python": platform.python_version(), "numpy": np.__version__},
        "status": status,
        "minimum_ready": MIN_READY,
        "maximum_frozen": MAX_FREEZE,
        "generated_total": total_generated,
        "available_counts": shell_counts,
        "available_total": payload["available_total"],
        "frozen_count": len(selected),
        "selection_sha256": selection_sha,
        "shell_hashes": shell_hashes,
        "deterministic_hash_ok": deterministic_hash_ok,
        "hidden_full_stability_computed": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    execute()
