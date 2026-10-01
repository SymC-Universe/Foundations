"""Laptop-safe transition-topology redundancy audit.

Question:
Does q=0 root count carry information beyond the present acceleration sign,
or is the apparent ~0.97-bit topology entropy already encoded by q0?

Reads the same released DR2 BAO likelihood implementation already validated
in desi_bao_profile_gate.py. Writes only to laptop_parallel_results.

This test may DEMOTE topology if it is redundant. It cannot promote new physics.
"""

from __future__ import annotations

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
SEED = 260950


def entropy_binary(x):
    vals, counts = np.unique(x, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def conditional_entropy(x, y):
    # H(X|Y)
    out = 0.0
    for yy in np.unique(y):
        m = y == yy
        out += float(m.mean()) * entropy_binary(x[m])
    return out


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


om, w0, wa = posterior()
zq, zchi, zq2, nq, nchi, q0_numeric, chi0 = gate.root_topology(
    om, w0, wa, zpoints=1001, batch=3000
)

# Analytic present-day q0 for flat matter + CPL DE. wa drops out at a=1.
q0_analytic = 0.5 * (
    om + (1.0 - om) * (1.0 + 3.0 * w0)
)
analytic_error = np.max(np.abs(q0_numeric - q0_analytic))

root_two = nq == 2
present_decelerating = q0_numeric > 0
present_accelerating = q0_numeric < 0

tp = int(np.sum(root_two & present_decelerating))
tn = int(np.sum((~root_two) & present_accelerating))
fp = int(np.sum(root_two & present_accelerating))
fn = int(np.sum((~root_two) & present_decelerating))
other = int(np.sum(~np.isin(nq, [1, 2])))

agreement = float(np.mean(root_two == present_decelerating))
h_root = entropy_binary(root_two)
h_root_given_sign = conditional_entropy(root_two, present_decelerating)
mi = h_root - h_root_given_sign

# Is wa doing anything beyond the current q0 sign for root count?
# Within each q0-sign class, summarize wa and count any topology exceptions.
wa_two = wa[root_two]
wa_one = wa[~root_two]

def qstats(x):
    return [float(v) for v in np.quantile(x, [0.16, 0.5, 0.84])]

# Historical branch information in the two-root class.
m = root_two & np.isfinite(zq) & np.isfinite(zq2) & np.isfinite(zchi)
branch_sep = zq2[m] - zq[m]
recent_offset = zq[m] - zchi[m]
earlier_offset = zq2[m] - zchi[m]

# Test whether the branch offsets are reducible to q0 alone via simple linear
# least-squares on a held-out split. This is diagnostic, not a final model.
rng = np.random.default_rng(260951)
idx = np.flatnonzero(m)
rng.shuffle(idx)
cut = len(idx) // 2
tr, te = idx[:cut], idx[cut:]

def heldout_r2(y):
    Xtr = np.column_stack([np.ones(len(tr)), q0_numeric[tr]])
    beta, *_ = np.linalg.lstsq(Xtr, y[tr], rcond=None)
    Xte = np.column_stack([np.ones(len(te)), q0_numeric[te]])
    pred = Xte @ beta
    yt = y[te]
    sse = float(np.sum((yt - pred) ** 2))
    sst = float(np.sum((yt - np.mean(yt)) ** 2))
    return 1.0 - sse / sst if sst > 0 else float("nan")

# arrays defined on full sample for easy indexing
sep_full = np.full(N, np.nan)
recent_full = np.full(N, np.nan)
earlier_full = np.full(N, np.nan)
sep_full[m] = branch_sep
recent_full[m] = recent_offset
earlier_full[m] = earlier_offset

r2_sep_q0 = heldout_r2(sep_full)
r2_recent_q0 = heldout_r2(recent_full)
r2_earlier_q0 = heldout_r2(earlier_full)

result = {
    "n": N,
    "seed": SEED,
    "analytic_q0_max_abs_error": float(analytic_error),
    "root_two_fraction": float(root_two.mean()),
    "present_decelerating_fraction": float(present_decelerating.mean()),
    "root_two_equals_present_decelerating_agreement": agreement,
    "contingency": {
        "two_root_and_decelerating": tp,
        "one_root_and_accelerating": tn,
        "two_root_but_accelerating": fp,
        "one_root_but_decelerating": fn,
        "other_root_counts": other,
    },
    "root_count_entropy_bits": h_root,
    "root_count_conditional_entropy_given_q0_sign_bits": h_root_given_sign,
    "mutual_information_rootcount_q0sign_bits": mi,
    "wa_q16_q50_q84_one_root": qstats(wa_one),
    "wa_q16_q50_q84_two_root": qstats(wa_two),
    "two_root_branch_separation_q16_q50_q84": qstats(branch_sep),
    "two_root_recent_minus_chi_q16_q50_q84": qstats(recent_offset),
    "two_root_earlier_minus_chi_q16_q50_q84": qstats(earlier_offset),
    "heldout_linear_r2_branch_separation_from_q0_only": float(r2_sep_q0),
    "heldout_linear_r2_recent_offset_from_q0_only": float(r2_recent_q0),
    "heldout_linear_r2_earlier_offset_from_q0_only": float(r2_earlier_q0),
}

(OUT / "transition_topology_redundancy.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8"
)

report = f"""# Transition-Topology Redundancy Audit

The q-root-count entropy is {h_root:.8f} bits.

Conditioning only on the sign of present-day q0 leaves

H(root count | sign(q0)) = {h_root_given_sign:.12f} bits.

Thus

I(root count ; sign(q0)) = {mi:.8f} bits.

Agreement between "two q=0 roots" and "presently decelerating":

{100*agreement:.8f}%

Contingency:
- two roots + decelerating: {tp}
- one root + accelerating: {tn}
- two roots + accelerating: {fp}
- one root + decelerating: {fn}
- other root counts: {other}

The analytic CPL present-day q0 expression matches the numerical q0 to a
maximum absolute error of {analytic_error:.3e}. Since wa drops out at a=1,
the current acceleration sign is determined by Omega_m and w0.

This means root-count entropy should not be counted as independent information
if the agreement is effectively exact. The root count is then a historical
/topological rendering of a present-state split already visible in q0 sign.

However, two-root branch locations may still contain history that q0 alone
does not preserve. Held-out linear q0-only R2 values are:

- branch separation: {r2_sep_q0:.8f}
- recent-branch offset from chi_delta=1: {r2_recent_q0:.8f}
- earlier-branch offset from chi_delta=1: {r2_earlier_q0:.8f}

These are diagnostics only. Poor q0-only prediction would justify a later
multivariable/history sufficiency test; strong prediction would further
demote topology as redundant.
"""

(OUT / "TRANSITION_TOPOLOGY_REDUNDANCY_REPORT.md").write_text(
    report, encoding="utf-8"
)

print("Transition-topology redundancy audit complete.")
print(f"root-count entropy = {h_root:.6f} bits")
print(f"H(root count | q0 sign) = {h_root_given_sign:.12f} bits")
print(f"root-count/q0-sign agreement = {100*agreement:.6f}%")
print(f"held-out R2 branch separation from q0 only = {r2_sep_q0:.6f}")
print(f"held-out R2 recent offset from q0 only = {r2_recent_q0:.6f}")
print(f"held-out R2 earlier offset from q0 only = {r2_earlier_q0:.6f}")
