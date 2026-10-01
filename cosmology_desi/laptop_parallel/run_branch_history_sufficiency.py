"""Laptop-safe branch-history sufficiency audit.

Purpose:
After finding q-root count is exactly redundant with sign(q0), test whether
two-root branch geometry contains information not recoverable from present
state alone, and whether that information is absorbed by the native CPL
history parameter wa.

This is a representation sufficiency test. It cannot establish new physics.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from scipy.stats import qmc

import desi_bao_profile_gate as gate

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "laptop_parallel_results"
OUT.mkdir(parents=True, exist_ok=True)

N = 80000
SEED = 260960
SPLIT_SEED = 260961


def posterior():
    rows, cov = gate.load_data(DATA)
    like = gate.BAOLikelihood(rows, cov)
    u = qmc.Sobol(
        3, scramble=True, seed=gate.SEEDS["w0wa"]
    ).random_base2(gate.SOBOL_POWERS["w0wa"])
    om = 0.05 + 0.55 * u[:, 0]
    w0 = -3.0 + 4.0 * u[:, 1]
    wa = -3.0 + 5.0 * u[:, 2]
    valid = w0 + wa < 0.0

    logw = np.full(len(u), -np.inf)
    idx = np.flatnonzero(valid)
    l, _, _ = like.profile_marginal(om[idx], w0[idx], wa[idx])
    logw[idx] = l

    lw = logw - np.nanmax(logw)
    wt = np.exp(lw)
    wt[~np.isfinite(wt)] = 0.0
    wt /= wt.sum()

    rng = np.random.default_rng(SEED)
    draw = rng.choice(len(wt), size=N, replace=True, p=wt)
    return om[draw], w0[draw], wa[draw]


def fit_r2(X, y, train, test):
    Xtr = np.column_stack([np.ones(len(train)), X[train]])
    Xte = np.column_stack([np.ones(len(test)), X[test]])
    beta, *_ = np.linalg.lstsq(Xtr, y[train], rcond=None)
    pred = Xte @ beta
    yt = y[test]
    sse = float(np.sum((yt - pred) ** 2))
    sst = float(np.sum((yt - np.mean(yt)) ** 2))
    return 1.0 - sse / sst if sst > 0 else float("nan")


def poly2(X):
    cols = [X]
    extra = []
    for i in range(X.shape[1]):
        extra.append((X[:, i] ** 2)[:, None])
        for j in range(i + 1, X.shape[1]):
            extra.append((X[:, i] * X[:, j])[:, None])
    return np.column_stack([cols[0], *extra])


om, w0, wa = posterior()
zq, zchi, zq2, nq, nchi, q0, chi0 = gate.root_topology(
    om, w0, wa, zpoints=1001, batch=3000
)

m = (
    (nq == 2)
    & np.isfinite(zq)
    & np.isfinite(zq2)
    & np.isfinite(zchi)
)

idx = np.flatnonzero(m)
rng = np.random.default_rng(SPLIT_SEED)
rng.shuffle(idx)
cut = len(idx) // 2
train, test = idx[:cut], idx[cut:]

targets = {
    "branch_separation": zq2 - zq,
    "recent_minus_chi": zq - zchi,
    "earlier_minus_chi": zq2 - zchi,
}

predictors = {
    "q0_only": q0[:, None],
    "q0_plus_zchi": np.column_stack([q0, zchi]),
    "q0_plus_wa": np.column_stack([q0, wa]),
    "present_native_om_w0": np.column_stack([om, w0]),
    "native_om_w0_wa": np.column_stack([om, w0, wa]),
    "native_om_w0_wa_poly2": poly2(np.column_stack([om, w0, wa])),
}

rows = []
for tname, y in targets.items():
    for pname, X in predictors.items():
        r2 = fit_r2(X, y, train, test)
        rows.append({
            "target": tname,
            "predictor_set": pname,
            "heldout_r2": float(r2),
        })

with (OUT / "branch_history_sufficiency.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    w = csv.DictWriter(
        f, fieldnames=["target", "predictor_set", "heldout_r2"]
    )
    w.writeheader()
    w.writerows(rows)

lookup = {
    (r["target"], r["predictor_set"]): r["heldout_r2"]
    for r in rows
}

summary = {
    "n_total": N,
    "n_two_root": int(len(idx)),
    "train_n": int(len(train)),
    "test_n": int(len(test)),
    "results": rows,
    "incremental_r2_wa_over_q0": {
        t: float(
            lookup[(t, "q0_plus_wa")] - lookup[(t, "q0_only")]
        )
        for t in targets
    },
    "incremental_r2_full_native_over_present_native": {
        t: float(
            lookup[(t, "native_om_w0_wa")]
            - lookup[(t, "present_native_om_w0")]
        )
        for t in targets
    },
}

(OUT / "branch_history_sufficiency.json").write_text(
    json.dumps(summary, indent=2) + "\n", encoding="utf-8"
)

report_lines = [
    "# Branch-History Sufficiency Audit",
    "",
    "The root-count class was already found to be exactly redundant with sign(q0).",
    "This audit asks whether branch locations retain history beyond present state,",
    "and whether that history is absorbed by the native CPL parameter wa.",
    "",
]

for t in targets:
    report_lines += [
        f"## {t}",
        "",
        f"q0 only held-out R2: {lookup[(t, 'q0_only')]:.8f}",
        f"q0 + zchi held-out R2: {lookup[(t, 'q0_plus_zchi')]:.8f}",
        f"q0 + wa held-out R2: {lookup[(t, 'q0_plus_wa')]:.8f}",
        f"Omega_m + w0 held-out R2: {lookup[(t, 'present_native_om_w0')]:.8f}",
        f"Omega_m + w0 + wa held-out R2: {lookup[(t, 'native_om_w0_wa')]:.8f}",
        f"native quadratic held-out R2: {lookup[(t, 'native_om_w0_wa_poly2')]:.8f}",
        "",
        "Increment from adding wa to q0: "
        f"{summary['incremental_r2_wa_over_q0'][t]:.8f}",
        "Increment from adding wa to present native variables: "
        f"{summary['incremental_r2_full_native_over_present_native'][t]:.8f}",
        "",
    ]

report_lines += [
    "## Interpretation",
    "",
    "If wa produces a large held-out gain, the two-root branch geometry is carrying",
    "history that q0 alone discards, but that history remains native CPL information.",
    "In that case branch topology is a potentially useful compression/representation",
    "of model history, not an independent new cosmological degree of freedom.",
    "",
    "If even the full native CPL variables predict branch geometry poorly under simple",
    "held-out models, a more flexible native-model comparator is required before any",
    "claim of irreducible trajectory information is admissible.",
]

(OUT / "BRANCH_HISTORY_SUFFICIENCY_REPORT.md").write_text(
    "\n".join(report_lines) + "\n", encoding="utf-8"
)

print("Branch-history sufficiency audit complete.")
for t in targets:
    print(
        f"{t}: q0={lookup[(t,'q0_only')]:.6f}, "
        f"q0+wa={lookup[(t,'q0_plus_wa')]:.6f}, "
        f"native3={lookup[(t,'native_om_w0_wa')]:.6f}, "
        f"native_poly2={lookup[(t,'native_om_w0_wa_poly2')]:.6f}"
    )
