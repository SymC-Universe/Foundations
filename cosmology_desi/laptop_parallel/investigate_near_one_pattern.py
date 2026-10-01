"""Investigate whether d_response ~= 1.01448 and rank1 residual ~= 0.7188%
carry independent or unusual structure.

Reads only canonical completed result JSONs. Writes only to:
    cosmology_desi/laptop_parallel_results/

Tests:
1. exact algebraic dependence between d_eff and rank-1 residual fraction;
2. amplitude-preserving geometry;
3. direction-only row-normalized geometry;
4. leave-one-observable-out sensitivity;
5. relative-amplitude scaling sensitivity;
6. fixed-norm random-direction null in 4D.

No Stability Architecture claim is promoted by this script.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = ROOT / "laptop_parallel_results"
OUT.mkdir(parents=True, exist_ok=True)

PARAMS = ["omegam", "sigma8", "H0", "S8_standard"]
RNG_SEED = 260930
N_NULL = 500_000


def load_json(name):
    with (RESULTS / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def geom(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    R = np.vstack([a, b])
    s = np.linalg.svd(R, compute_uv=False)
    e = s * s
    frac2 = float(e[1] / e.sum())
    deff = float((e.sum() ** 2) / np.square(e).sum())
    cos = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    cos = max(-1.0, min(1.0, cos))
    angle = float(np.degrees(np.arccos(cos)))
    ratio = float(np.linalg.norm(a) / np.linalg.norm(b))
    return {
        "deff": deff,
        "rank1_residual_fraction": frac2,
        "cosine": cos,
        "angle_deg": angle,
        "norm_ratio": ratio,
        "s1": float(s[0]),
        "s2": float(s[1]),
    }


mgj = load_json("dmde_dr1_mg_comparison.json")
nuj = load_json("dmde_neutrino_adversary_analysis.json")

mg = np.array(
    [mgj["descriptive_shifts"][p]["difference_in_baseline_sd"] for p in PARAMS],
    float,
)
nu = np.array(
    [nuj["cmb_fixed_vs_free_mnu"]["shifts"][p]["difference_in_fixed_sd"] for p in PARAMS],
    float,
)

obs = geom(mg, nu)
identity_deff = 1.0 / (
    (1.0 - obs["rank1_residual_fraction"]) ** 2
    + obs["rank1_residual_fraction"] ** 2
)
identity_error = abs(identity_deff - obs["deff"])

mg_u = mg / np.linalg.norm(mg)
nu_u = nu / np.linalg.norm(nu)
direction_only = geom(mg_u, nu_u)

# Leave-one-observable-out sensitivity.
loo = []
for i, name in enumerate(PARAMS):
    keep = np.arange(len(PARAMS)) != i
    g = geom(mg[keep], nu[keep])
    g["removed"] = name
    loo.append(g)

with (OUT / "near_one_pattern_leave_one_out.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    fields = [
        "removed", "deff", "rank1_residual_fraction", "cosine",
        "angle_deg", "norm_ratio", "s1", "s2"
    ]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(loo)

# Relative-amplitude sensitivity: scale MG while leaving neutrino row fixed.
scales = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
scale_rows = []
for scale in scales:
    g = geom(mg * scale, nu)
    g["mg_scale"] = scale
    scale_rows.append(g)

with (OUT / "near_one_pattern_scale_sensitivity.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    fields = [
        "mg_scale", "deff", "rank1_residual_fraction", "cosine",
        "angle_deg", "norm_ratio", "s1", "s2"
    ]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(scale_rows)

# Fixed observed norms, random independent orientations in 4D.
rng = np.random.default_rng(RNG_SEED)
x = rng.normal(size=(N_NULL, 4))
y = rng.normal(size=(N_NULL, 4))
x /= np.linalg.norm(x, axis=1)[:, None]
y /= np.linalg.norm(y, axis=1)[:, None]
c = np.sum(x * y, axis=1)

a = float(np.linalg.norm(mg))
b = float(np.linalg.norm(nu))
tr = a * a + b * b
disc = np.sqrt((a*a - b*b)**2 + 4.0*a*a*b*b*c*c)
lam2 = (tr - disc) / 2.0
null_resid = lam2 / tr

p_resid_le = float(np.mean(null_resid <= obs["rank1_residual_fraction"]))
p_resid_ge = float(np.mean(null_resid >= obs["rank1_residual_fraction"]))
p_abs_cos_ge = float(np.mean(np.abs(c) >= abs(obs["cosine"])))
q = np.quantile(null_resid, [0.025, 0.05, 0.5, 0.95, 0.975])

with (OUT / "near_one_pattern_null_summary.csv").open(
    "w", newline="", encoding="utf-8"
) as f:
    w = csv.writer(f)
    w.writerow(["metric", "value"])
    w.writerow(["n_null", N_NULL])
    w.writerow(["rng_seed", RNG_SEED])
    w.writerow(["observed_deff", obs["deff"]])
    w.writerow(["observed_rank1_residual_fraction", obs["rank1_residual_fraction"]])
    w.writerow(["observed_rank1_residual_percent", 100*obs["rank1_residual_fraction"]])
    w.writerow(["identity_deff_from_residual", identity_deff])
    w.writerow(["identity_absolute_error", identity_error])
    w.writerow(["direction_only_deff", direction_only["deff"]])
    w.writerow(["direction_only_rank1_residual_fraction", direction_only["rank1_residual_fraction"]])
    w.writerow(["direction_only_rank1_residual_percent", 100*direction_only["rank1_residual_fraction"]])
    w.writerow(["fixed_norm_null_p_residual_le_observed", p_resid_le])
    w.writerow(["fixed_norm_null_p_residual_ge_observed", p_resid_ge])
    w.writerow(["fixed_norm_null_p_abs_cos_ge_observed", p_abs_cos_ge])
    w.writerow(["null_residual_q025", q[0]])
    w.writerow(["null_residual_q05", q[1]])
    w.writerow(["null_residual_q50", q[2]])
    w.writerow(["null_residual_q95", q[3]])
    w.writerow(["null_residual_q975", q[4]])

report = f"""# Near-One / 0.7188% Pattern Investigation

Scope: canonical completed MG and free-neutrino adversarial responses only.

## 1. The two reported numbers are algebraically linked

Observed best rank-1 residual fraction:

{obs["rank1_residual_fraction"]:.12f}

or, as a percentage:

{100*obs["rank1_residual_fraction"]:.8f}%

Observed effective dimension:

{obs["deff"]:.12f}

For a rank-two spectrum with residual fraction f, the participation-ratio
effective dimension is exactly

d_eff = 1 / ((1-f)^2 + f^2).

Substituting the observed residual gives:

{identity_deff:.12f}

Absolute numerical discrepancy:

{identity_error:.3e}

Therefore 1.01448 and 0.7188% are not independent coincidences. They encode
the same two-singular-value spectrum.

## 2. Raw amplitude-preserving geometry

MG / neutrino response norm ratio:

{obs["norm_ratio"]:.8f}

Cosine similarity:

{obs["cosine"]:.8f}

Angle:

{obs["angle_deg"]:.8f} degrees

The MG response norm is only about {100*obs["norm_ratio"]:.3f}% of the
neutrino response norm. This amplitude imbalance strongly forces the raw
two-row matrix toward rank one.

## 3. Direction-only geometry

After normalizing each adversary response vector to unit length:

direction-only d_eff = {direction_only["deff"]:.8f}
direction-only rank-1 residual = {100*direction_only["rank1_residual_fraction"]:.8f}%

Thus the near-1 raw d_eff and 0.7188% raw residual are not invariant to
removing relative response amplitude. The directional structure is much
less one-dimensional.

## 4. Fixed-norm random-direction null

Null: two independent random directions in four dimensions with the
observed MG and neutrino norms held fixed.

N = {N_NULL}
seed = {RNG_SEED}

P(null residual <= observed) = {p_resid_le:.8f}
P(null residual >= observed) = {p_resid_ge:.8f}
P(|null cosine| >= |observed cosine|) = {p_abs_cos_ge:.8f}

Null residual quantiles:
2.5% = {q[0]:.8f}
5%   = {q[1]:.8f}
50%  = {q[2]:.8f}
95%  = {q[3]:.8f}
97.5%= {q[4]:.8f}

The observed residual is therefore not unusual under a null that preserves
the strong response-amplitude imbalance.

## 5. Interpretation

The scientifically meaningful feature is not numerical proximity of
1.01448 to 1 or the percentage rendering 0.7188 to an earlier ~0.72 value.

The meaningful current result is a split between:

- amplitude-weighted structure: almost rank one because the neutrino
  adversary dominates total response magnitude;
- response direction: materially non-collinear, so adversary identity is
  not represented by amplitude alone.

The percentage form 0.7188% is a presentation choice for the dimensionless
fraction 0.007188. Multiplying by 100 cannot create a scale-invariant
correspondence to an unrelated ~0.72 stability coordinate.

This result does not refute the broader Stability Architecture program.
It specifically refuses promotion of this numerical near-match as evidence.
The directional-versus-amplitude separation remains a legitimate object
for subsequent representation testing.
"""

with (OUT / "NEAR_ONE_PATTERN_INVESTIGATION.md").open(
    "w", encoding="utf-8"
) as f:
    f.write(report)

print("Near-one pattern investigation complete.")
print(f"raw d_eff = {obs['deff']:.9f}")
print(f"raw rank-1 residual = {100*obs['rank1_residual_fraction']:.6f}%")
print(f"d_eff reconstructed exactly from residual = {identity_deff:.9f}")
print(f"direction-only d_eff = {direction_only['deff']:.9f}")
print(f"direction-only residual = {100*direction_only['rank1_residual_fraction']:.6f}%")
print(f"fixed-norm null P(residual <= observed) = {p_resid_le:.6f}")
print(f"fixed-norm null P(|cos| >= observed) = {p_abs_cos_ge:.6f}")
