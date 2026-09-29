#!/usr/bin/env python3
"""Independent DESI DR2 BAO Stability-Architecture gate.

This lane uses the released 13-point DESI DR2 Gaussian BAO likelihood pinned in
cosmology_desi/data/.  It is independent of, and does not replace, replaying
DESI's released Cobaya posterior chains.

The sampled cosmological scale parameter is analytically marginalized through
h r_d.  Stability quantities depend only on the late-time background shape.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq, differential_evolution
from scipy.stats import qmc

C_OVER_100 = 2997.92458
ZMAX = 5.0
UPSTREAM_COMMIT = "bb0c1c9009dc76d1391300e169e8df38fd1096db"
MODEL_PRIORS = {
    "base": {"Omega_m": (0.05, 0.60)},
    "w": {"Omega_m": (0.05, 0.60), "w": (-3.0, 1.0)},
    "w0wa": {"Omega_m": (0.05, 0.60), "w0": (-3.0, 1.0), "wa": (-3.0, 2.0)},
}
SOBOL_POWERS = {"base": 17, "w": 19, "w0wa": 20}
SEEDS = {"base": 101, "w": 202, "w0wa": 303}


def load_data(root: Path):
    mean = root / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
    covf = root / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
    rows = []
    for line in mean.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        z, value, quantity = line.split()
        rows.append((float(z), float(value), quantity))
    cov = np.loadtxt(covf)
    if cov.shape != (13, 13) or len(rows) != 13:
        raise RuntimeError("DESI DR2 BAO likelihood shape mismatch")
    return rows, cov


class BAOLikelihood:
    def __init__(self, rows, cov):
        self.z = np.array([r[0] for r in rows])
        self.data = np.array([r[1] for r in rows])
        self.qty = np.array([r[2] for r in rows])
        self.icov = np.linalg.inv(cov)
        self.icov_data = self.icov @ self.data
        self.data_icov_data = float(self.data @ self.icov_data)
        self.xg, self.wg = leggauss(48)
        self.unique_z = np.unique(self.z)

    @staticmethod
    def e2(z, om, w0, wa):
        a = 1.0 / (1.0 + z)
        de = a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
        return om * a ** -3 + (1.0 - om) * de

    def shape(self, om, w0, wa):
        """Return dimensionless BAO vector g with model=(c/100/hrd)*g."""
        om = np.asarray(om)
        w0 = np.asarray(w0)
        wa = np.asarray(wa)
        n = len(om)
        out = np.empty((n, len(self.z)))
        cache = {}
        for zz in self.unique_z:
            ez = np.sqrt(self.e2(zz, om, w0, wa))
            dh = 1.0 / ez
            zn = 0.5 * zz * (self.xg + 1.0)
            an = 1.0 / (1.0 + zn[None, :])
            de = an ** (-3.0 * (1.0 + w0[:, None] + wa[:, None]))
            de *= np.exp(-3.0 * wa[:, None] * (1.0 - an))
            en = np.sqrt(om[:, None] * an ** -3 + (1.0 - om[:, None]) * de)
            dm = 0.5 * zz * np.sum(self.wg[None, :] / en, axis=1)
            cache[zz] = (dh, dm)
        for j, (zz, quantity) in enumerate(zip(self.z, self.qty)):
            dh, dm = cache[zz]
            if quantity == "DH_over_rs":
                out[:, j] = dh
            elif quantity == "DM_over_rs":
                out[:, j] = dm
            elif quantity == "DV_over_rs":
                out[:, j] = (zz * dm * dm * dh) ** (1.0 / 3.0)
            else:
                raise RuntimeError(f"Unknown BAO quantity: {quantity}")
        return out

    def profile_marginal(self, om, w0, wa, batch=12000):
        """Laplace-marginalize a broad flat prior in h r_d.

        Conditional on background shape the BAO vector is linear in
        s=(c/100)/(h r_d), so chi^2 is exactly quadratic in s.  The returned
        volume factor is the local transformation for a flat h r_d prior.
        """
        n = len(om)
        logp = np.full(n, -np.inf)
        hrd = np.full(n, np.nan)
        chi2min = np.full(n, np.nan)
        for start in range(0, n, batch):
            stop = min(n, start + batch)
            g = self.shape(om[start:stop], w0[start:stop], wa[start:stop])
            aa = np.einsum("ni,ij,nj->n", g, self.icov, g)
            bb = g @ self.icov_data
            scale = bb / aa
            h = C_OVER_100 / scale
            chi = self.data_icov_data - bb * bb / aa
            sigma_h = C_OVER_100 / (np.sqrt(aa) * scale * scale)
            ok = (h > 20.0) & (h < 200.0) & np.isfinite(chi) & (sigma_h > 0)
            logp[start:stop] = np.where(ok, -0.5 * chi + np.log(sigma_h), -np.inf)
            hrd[start:stop] = h
            chi2min[start:stop] = chi
        return logp, hrd, chi2min


def background(z, om, w0, wa):
    a = 1.0 / (1.0 + z)
    de = a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
    e2 = om * a ** -3 + (1.0 - om) * de
    oma = om * a ** -3 / e2
    wz = w0 + wa * (1.0 - a)
    q = 0.5 * (oma + (1.0 - oma) * (1.0 + 3.0 * wz))
    chi = np.sqrt(2.0 / (3.0 * oma))
    return q, chi


def weighted_quantile(x, logw, probs=(0.16, 0.5, 0.84)):
    mask = np.isfinite(x) & np.isfinite(logw)
    x = x[mask]
    lw = logw[mask]
    lw -= np.max(lw)
    w = np.exp(lw)
    order = np.argsort(x)
    x, w = x[order], w[order]
    cdf = np.cumsum(w)
    cdf /= cdf[-1]
    return [float(np.interp(p, cdf, x)) for p in probs]


def weighted_mean_hpd(x, logw, mass=0.68):
    """DESI-style posterior mean plus shortest 68% credible interval."""
    mask = np.isfinite(x) & np.isfinite(logw)
    x = x[mask]
    lw = logw[mask]
    lw -= np.max(lw)
    w = np.exp(lw)
    w /= w.sum()
    mean = float(np.sum(w * x))
    order = np.argsort(x)
    xs, ws = x[order], w[order]
    cdf = np.cumsum(ws)
    starts = np.concatenate(([0.0], cdf[:-1]))
    valid = starts + mass <= 1.0
    ii = np.flatnonzero(valid)
    jj = np.searchsorted(cdf, starts[valid] + mass, side="left")
    widths = xs[jj] - xs[ii]
    k = int(np.argmin(widths))
    lo, hi = float(xs[ii[k]]), float(xs[jj[k]])
    return {
        "mean": mean,
        "hpd68": [lo, hi],
        "minus": mean - lo,
        "plus": hi - mean,
    }


def importance_ess(logw):
    lw = logw[np.isfinite(logw)]
    lw -= np.max(lw)
    w = np.exp(lw)
    return float(w.sum() ** 2 / np.dot(w, w))


def posterior_resample(parameters, logw, n=80000, seed=991):
    lw = logw - np.nanmax(logw)
    w = np.exp(lw)
    w[~np.isfinite(w)] = 0.0
    w /= w.sum()
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(w), n, replace=True, p=w)
    return [x[idx] for x in parameters]


def root_topology(om, w0, wa, zpoints=1001, batch=4000):
    n = len(om)
    zg = np.linspace(0.0, ZMAX, zpoints)
    zq = np.full(n, np.nan)
    zchi = np.full(n, np.nan)
    zq_second = np.full(n, np.nan)
    nq = np.zeros(n, dtype=int)
    nchi = np.zeros(n, dtype=int)
    q0 = np.empty(n)
    chi0 = np.empty(n)

    for start in range(0, n, batch):
        stop = min(n, start + batch)
        a = 1.0 / (1.0 + zg[None, :])
        omi = om[start:stop, None]
        w0i = w0[start:stop, None]
        wai = wa[start:stop, None]
        de = a ** (-3.0 * (1.0 + w0i + wai)) * np.exp(-3.0 * wai * (1.0 - a))
        e2 = omi * a ** -3 + (1.0 - omi) * de
        oma = omi * a ** -3 / e2
        wz = w0i + wai * (1.0 - a)
        qv = 0.5 * (oma + (1.0 - oma) * (1.0 + 3.0 * wz))
        cv = np.sqrt(2.0 / (3.0 * oma)) - 1.0
        q0[start:stop] = qv[:, 0]
        chi0[start:stop] = cv[:, 0] + 1.0

        for values, primary, counts in ((qv, zq, nq), (cv, zchi, nchi)):
            cross = (values[:, :-1] * values[:, 1:] < 0) | (np.abs(values[:, :-1]) < 1e-12)
            counts[start:stop] = cross.sum(axis=1)
            for j in range(stop - start):
                loc = np.flatnonzero(cross[j])
                if len(loc):
                    k = loc[0]
                    f0, f1 = values[j, k], values[j, k + 1]
                    primary[start + j] = zg[k] - f0 * (zg[k + 1] - zg[k]) / (f1 - f0)
                if values is qv and len(loc) >= 2:
                    k = loc[1]
                    f0, f1 = values[j, k], values[j, k + 1]
                    zq_second[start + j] = zg[k] - f0 * (zg[k + 1] - zg[k]) / (f1 - f0)
    return zq, zchi, zq_second, nq, nchi, q0, chi0


def q16_50_84(x):
    x = np.asarray(x)
    x = x[np.isfinite(x)]
    return [float(v) for v in np.quantile(x, (0.16, 0.5, 0.84))]


def fractions(x):
    values, counts = np.unique(x, return_counts=True)
    return {str(int(v)): float(c / len(x)) for v, c in zip(values, counts)}


def lcdm_identity_gate():
    oms = np.linspace(0.12, 0.55, 257)
    diffs = []
    for om in oms:
        fq = lambda z: background(z, om, -1.0, 0.0)[0]
        fc = lambda z: background(z, om, -1.0, 0.0)[1] - 1.0
        rq = brentq(fq, 0.0, 5.0, xtol=1e-13, rtol=1e-13)
        rc = brentq(fc, 0.0, 5.0, xtol=1e-13, rtol=1e-13)
        diffs.append(abs(rq - rc))
    maximum = float(max(diffs))
    return {"max_abs_delta_z": maximum, "pass": maximum < 1e-10}


def run(model, like, resamples=80000):
    dim = {"base": 1, "w": 2, "w0wa": 3}[model]
    u = qmc.Sobol(dim, scramble=True, seed=SEEDS[model]).random_base2(SOBOL_POWERS[model])
    om = 0.05 + 0.55 * u[:, 0]

    if model == "base":
        w0 = np.full(len(u), -1.0)
        wa = np.zeros(len(u))
        valid = np.ones(len(u), dtype=bool)
    elif model == "w":
        w0 = -3.0 + 4.0 * u[:, 1]
        wa = np.zeros(len(u))
        valid = np.ones(len(u), dtype=bool)
    else:
        w0 = -3.0 + 4.0 * u[:, 1]
        wa = -3.0 + 5.0 * u[:, 2]
        valid = w0 + wa < 0.0

    logw = np.full(len(u), -np.inf)
    hrd = np.full(len(u), np.nan)
    chi2min = np.full(len(u), np.nan)
    idx = np.flatnonzero(valid)
    l, h, c = like.profile_marginal(om[idx], w0[idx], wa[idx])
    logw[idx], hrd[idx], chi2min[idx] = l, h, c

    rom, rw0, rwa = posterior_resample([om, w0, wa], logw, n=resamples, seed=991 + dim)
    zq, zc, zq2, nq, nc, q0, chi0 = root_topology(rom, rw0, rwa)
    dz = zq - zc

    params = {
        "Omega_m": weighted_quantile(om, logw),
        "hrd_profile_Mpc": weighted_quantile(hrd, logw),
    }
    if model == "w":
        params["w"] = weighted_quantile(w0, logw)
    if model == "w0wa":
        params["w0"] = weighted_quantile(w0, logw)
        params["wa"] = weighted_quantile(wa, logw)

    desi_style = {
        "Omega_m": weighted_mean_hpd(om, logw),
        "hrd_profile_Mpc": weighted_mean_hpd(hrd, logw),
    }
    if model == "w":
        desi_style["w"] = weighted_mean_hpd(w0, logw)
    if model == "w0wa":
        desi_style["w0"] = weighted_mean_hpd(w0, logw)
        desi_style["wa_upper_68"] = weighted_quantile(wa, logw, (0.68,))[0]

    result = {
        "model": model,
        "scope": "independent_released_DR2_BAO_likelihood_reconstruction",
        "sobol_points": int(len(u)),
        "valid_prior_points": int(valid.sum()),
        "importance_ess": importance_ess(logw),
        "chi2_min_sampled": float(np.nanmin(chi2min)),
        "parameters_q16_q50_q84": params,
        "parameters_DESI_style_mean_HPD68": desi_style,
        "derived_q16_q50_q84": {
            "z_q0_primary": q16_50_84(zq),
            "z_chi_delta_eq_1": q16_50_84(zc),
            "delta_z_primary": q16_50_84(dz),
            "q0": q16_50_84(q0),
            "chi_delta_0": q16_50_84(chi0),
        },
        "q_root_fractions": fractions(nq),
        "chi_root_fractions": fractions(nc),
        "valid_delta_fraction": float(np.isfinite(dz).mean()),
    }

    if model == "base":
        ztr = (2.0 * (1.0 - rom) / rom) ** (1.0 / 3.0) - 1.0
        result["derived_q16_q50_q84"]["z_q0_exact_LCDM"] = q16_50_84(ztr)
        result["derived_q16_q50_q84"]["z_chi_delta_eq_1_exact_LCDM"] = q16_50_84(ztr)
        result["derived_q16_q50_q84"]["delta_z_exact_LCDM"] = [0.0, 0.0, 0.0]

    if model == "w0wa":
        one = nq == 1
        two = nq == 2

        def group(mask):
            return {
                "fraction": float(mask.mean()),
                "Omega_m": q16_50_84(rom[mask]),
                "w0": q16_50_84(rw0[mask]),
                "wa": q16_50_84(rwa[mask]),
                "q0": q16_50_84(q0[mask]),
                "chi_delta_0": q16_50_84(chi0[mask]),
                "z_q0_primary": q16_50_84(zq[mask]),
                "z_chi_delta_eq_1": q16_50_84(zc[mask]),
                "delta_z_primary": q16_50_84(dz[mask]),
            }

        result["topology"] = {
            "one_q_root": group(one),
            "two_q_roots": group(two),
            "two_q_roots_second_q_crossing": q16_50_84(zq2[two]),
            "present_decelerating_fraction": float((q0 > 0).mean()),
            "present_accelerating_fraction": float((q0 < 0).mean()),
            "delta_z_negative_fraction": float((dz[np.isfinite(dz)] < 0).mean()),
            "delta_z_positive_fraction": float((dz[np.isfinite(dz)] > 0).mean()),
        }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="cosmology_desi/data")
    ap.add_argument("--out", default="cosmology_desi/results/desi_bao_profile_gate.json")
    ap.add_argument("--resamples", type=int, default=80000)
    args = ap.parse_args()

    rows, cov = load_data(Path(args.data))
    like = BAOLikelihood(rows, cov)
    result = {
        "upstream": {
            "repository": "CobayaSampler/bao_data",
            "commit": UPSTREAM_COMMIT,
            "mean_blob_sha": "8aff444fdb42c0946342aa0011ab287eda097c4c",
            "covariance_blob_sha": "fd8e5697ab61379b07b52efb781ea6713417a4d9",
        },
        "interpretation_firewall": (
            "Derived transition structure is not evidence for SI, DM-DE interaction, "
            "modified gravity, or dynamical dark energy by itself."
        ),
        "lcdm_identity_gate": lcdm_identity_gate(),
        "models": {},
    }
    if not result["lcdm_identity_gate"]["pass"]:
        raise SystemExit("FAIL: LambdaCDM q=0 <-> chi_delta=1 identity gate")

    for model in ("base", "w", "w0wa"):
        print(f"RUN {model}", flush=True)
        result["models"][model] = run(model, like, args.resamples)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
