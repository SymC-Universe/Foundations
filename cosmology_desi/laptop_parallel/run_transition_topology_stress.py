"""Laptop-safe DR2 transition-topology stress test.

This script reuses the already-validated DESI DR2 BAO likelihood implementation
from cosmology_desi/desi_bao_profile_gate.py, but writes ONLY to
cosmology_desi/laptop_parallel_results/.

Purpose:
- quantify when an unlabeled scalar transition is ambiguous;
- characterize one-root versus two-root topology;
- measure branch separation and which q=0 branch is nearest chi_delta=1;
- verify that root-count conclusions are stable to posterior resampling and
  reasonable redshift-grid refinement.

This is a representation audit, not evidence for new cosmological dynamics.
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

RESAMPLES = 80000
POSTERIOR_SEED = 260930
SENSITIVITY_N = 20000
REPLICATE_N = 20000
REPLICATE_SEEDS = [260931, 260932, 260933, 260934, 260935]


def entropy_bits(counts: np.ndarray) -> float:
    vals, n = np.unique(counts, return_counts=True)
    p = n / n.sum()
    return float(-(p * np.log2(p)).sum())


def qstats(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return [float("nan")] * 3
    return [float(v) for v in np.quantile(x, [0.16, 0.5, 0.84])]


def build_weighted_w0wa_posterior():
    rows, cov = gate.load_data(DATA)
    like = gate.BAOLikelihood(rows, cov)

    dim = 3
    u = qmc.Sobol(
        dim,
        scramble=True,
        seed=gate.SEEDS["w0wa"],
    ).random_base2(gate.SOBOL_POWERS["w0wa"])

    om = 0.05 + 0.55 * u[:, 0]
    w0 = -3.0 + 4.0 * u[:, 1]
    wa = -3.0 + 5.0 * u[:, 2]
    valid = w0 + wa < 0.0

    logw = np.full(len(u), -np.inf)
    idx = np.flatnonzero(valid)
    l, _, _ = like.profile_marginal(om[idx], w0[idx], wa[idx])
    logw[idx] = l

    return om, w0, wa, logw


def posterior_draw(om, w0, wa, logw, n, seed):
    lw = logw - np.nanmax(logw)
    wt = np.exp(lw)
    wt[~np.isfinite(wt)] = 0.0
    wt /= wt.sum()
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(wt), size=n, replace=True, p=wt)
    return om[idx], w0[idx], wa[idx]


om, w0, wa, logw = build_weighted_w0wa_posterior()
rom, rw0, rwa = posterior_draw(
    om, w0, wa, logw, RESAMPLES, POSTERIOR_SEED
)

zq, zchi, zq2, nq, nchi, q0, chi0 = gate.root_topology(
    rom, rw0, rwa, zpoints=1001, batch=3000
)

one = nq == 1
two = nq == 2
valid_chi = np.isfinite(zchi)
two_valid = two & np.isfinite(zq) & np.isfinite(zq2) & valid_chi

recent_dist = np.abs(zq[two_valid] - zchi[two_valid])
earlier_dist = np.abs(zq2[two_valid] - zchi[two_valid])
nearest_dist = np.minimum(recent_dist, earlier_dist)
recent_nearest = recent_dist < earlier_dist
earlier_nearest = earlier_dist < recent_dist
ties = ~(recent_nearest | earlier_nearest)

branch_sep = zq2[two_valid] - zq[two_valid]
primary_abs = np.abs(zq[two_valid] - zchi[two_valid])

root_values, root_counts = np.unique(nq, return_counts=True)
root_fraction = {
    str(int(k)): float(v / len(nq))
    for k, v in zip(root_values, root_counts)
}
chi_values, chi_counts = np.unique(nchi, return_counts=True)
chi_fraction = {
    str(int(k)): float(v / len(nchi))
    for k, v in zip(chi_values, chi_counts)
}

summary = {
    "scope": "DESI_DR2_BAO_w0wa_transition_topology_representation_audit",
    "resamples": RESAMPLES,
    "posterior_seed": POSTERIOR_SEED,
    "q_root_fractions": root_fraction,
    "chi_root_fractions": chi_fraction,
    "q_root_count_entropy_bits": entropy_bits(nq),
    "scalar_unlabeled_ambiguity_fraction": float(np.mean(nq != 1)),
    "one_q_root_fraction": float(one.mean()),
    "two_q_root_fraction": float(two.mean()),
    "present_accelerating_fraction": float(np.mean(q0 < 0)),
    "present_decelerating_fraction": float(np.mean(q0 > 0)),
    "two_root_branch_separation_q16_q50_q84": qstats(branch_sep),
    "two_root_recent_to_chi_abs_q16_q50_q84": qstats(recent_dist),
    "two_root_earlier_to_chi_abs_q16_q50_q84": qstats(earlier_dist),
    "two_root_nearest_to_chi_abs_q16_q50_q84": qstats(nearest_dist),
    "two_root_recent_branch_nearest_fraction": float(recent_nearest.mean()),
    "two_root_earlier_branch_nearest_fraction": float(earlier_nearest.mean()),
    "two_root_nearest_tie_fraction": float(ties.mean()),
    "two_root_primary_abs_q16_q50_q84": qstats(primary_abs),
    "two_root_median_primary_minus_nearest_abs": float(
        np.median(primary_abs) - np.median(nearest_dist)
    ),
}

# Grid sensitivity on a fixed posterior subset.
rng = np.random.default_rng(260940)
sub_idx = rng.choice(RESAMPLES, size=SENSITIVITY_N, replace=False)
grid_rows = []
grid_results = {}
for zpoints, batch in [(501, 2500), (1001, 2000), (2001, 1000)]:
    _, _, _, gnq, gnchi, _, _ = gate.root_topology(
        rom[sub_idx],
        rw0[sub_idx],
        rwa[sub_idx],
        zpoints=zpoints,
        batch=batch,
    )
    row = {
        "zpoints": zpoints,
        "q_one_fraction": float(np.mean(gnq == 1)),
        "q_two_fraction": float(np.mean(gnq == 2)),
        "q_entropy_bits": entropy_bits(gnq),
        "chi_one_fraction": float(np.mean(gnchi == 1)),
    }
    grid_rows.append(row)
    grid_results[zpoints] = gnq

# Exact root-count agreement across grid resolutions on the same subset.
summary["grid_sensitivity"] = {
    "n": SENSITIVITY_N,
    "rows": grid_rows,
    "q_count_agreement_501_vs_1001": float(
        np.mean(grid_results[501] == grid_results[1001])
    ),
    "q_count_agreement_1001_vs_2001": float(
        np.mean(grid_results[1001] == grid_results[2001])
    ),
    "q_count_agreement_501_vs_2001": float(
        np.mean(grid_results[501] == grid_results[2001])
    ),
}

# Posterior-resampling stability using the same weighted likelihood cloud.
rep_rows = []
for seed in REPLICATE_SEEDS:
    a, b, c = posterior_draw(om, w0, wa, logw, REPLICATE_N, seed)
    _, _, _, rnq, rnchi, rq0, _ = gate.root_topology(
        a, b, c, zpoints=1001, batch=2500
    )
    rep_rows.append({
        "seed": seed,
        "n": REPLICATE_N,
        "q_one_fraction": float(np.mean(rnq == 1)),
        "q_two_fraction": float(np.mean(rnq == 2)),
        "q_entropy_bits": entropy_bits(rnq),
        "chi_one_fraction": float(np.mean(rnchi == 1)),
        "present_accelerating_fraction": float(np.mean(rq0 < 0)),
    })

summary["posterior_resample_stability"] = rep_rows

(OUT / "transition_topology_stress.json").write_text(
    json.dumps(summary, indent=2) + "\n",
    encoding="utf-8",
)

with (OUT / "transition_topology_grid_sensitivity.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    fields = list(grid_rows[0].keys())
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(grid_rows)

with (OUT / "transition_topology_resample_stability.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    fields = list(rep_rows[0].keys())
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rep_rows)

report = f"""# DR2 BAO Transition-Topology Stress Test

Scope: representation stress test using the already-validated independent
DESI DR2 BAO w0wa likelihood lane. No active Victus-run file was read or
modified.

The central question is whether the background transition can be represented
by one unlabeled scalar event, or whether branch/topology information is
required.

Main posterior resample: {RESAMPLES}

q=0 root fractions:
{json.dumps(root_fraction, indent=2)}

chi_delta=1 root fractions:
{json.dumps(chi_fraction, indent=2)}

q-root-count entropy:
{summary["q_root_count_entropy_bits"]:.8f} bits

Fraction for which an unlabeled single q=0 transition is structurally
ambiguous:
{100*summary["scalar_unlabeled_ambiguity_fraction"]:.6f}%

Among two-q-root cases, branch separation z_earlier-z_recent
(q16, median, q84):
{summary["two_root_branch_separation_q16_q50_q84"]}

Fraction for which the recent q=0 branch is nearest chi_delta=1:
{100*summary["two_root_recent_branch_nearest_fraction"]:.6f}%

Fraction for which the earlier q=0 branch is nearest chi_delta=1:
{100*summary["two_root_earlier_branch_nearest_fraction"]:.6f}%

Median absolute primary-branch distance minus median nearest-branch distance:
{summary["two_root_median_primary_minus_nearest_abs"]:.8f}

Grid-resolution q-root-count agreement:
501 vs 1001: {summary["grid_sensitivity"]["q_count_agreement_501_vs_1001"]:.8f}
1001 vs 2001: {summary["grid_sensitivity"]["q_count_agreement_1001_vs_2001"]:.8f}
501 vs 2001: {summary["grid_sensitivity"]["q_count_agreement_501_vs_2001"]:.8f}

Interpretation:
- The root-count distribution is treated as topology of the chosen w0wa
  posterior, not as evidence for new physics.
- If the two-root fraction and root counts are stable to grid refinement and
  posterior resampling, the failure of a single unlabeled delta-z is a real
  representation issue rather than a root-finder artifact.
- This test does not establish modal necessity in the perturbation sector.
  It only establishes whether the background transition representation itself
  requires branch/topology labels.
"""

(OUT / "TRANSITION_TOPOLOGY_STRESS_REPORT.md").write_text(
    report,
    encoding="utf-8",
)

print("Transition-topology stress test complete.")
print(f"q-root entropy = {summary['q_root_count_entropy_bits']:.6f} bits")
print(
    "unlabeled scalar ambiguity fraction = "
    f"{100*summary['scalar_unlabeled_ambiguity_fraction']:.4f}%"
)
print(
    "two-root branch separation median = "
    f"{summary['two_root_branch_separation_q16_q50_q84'][1]:.6f}"
)
print(
    "earlier branch nearest chi fraction = "
    f"{100*summary['two_root_earlier_branch_nearest_fraction']:.4f}%"
)
print(
    "grid count agreement 501/1001/2001: "
    f"{summary['grid_sensitivity']['q_count_agreement_501_vs_1001']:.6f}, "
    f"{summary['grid_sensitivity']['q_count_agreement_1001_vs_2001']:.6f}, "
    f"{summary['grid_sensitivity']['q_count_agreement_501_vs_2001']:.6f}"
)
