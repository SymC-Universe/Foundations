import crypto from "node:crypto";

export const maxDuration = 300;

const ROOT = "https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/cobaya";
const DATASET = "desi-bao-all";
const MODELS = new Set(["base", "base_w", "base_w_wa"]);
const ZMAX = 5;
const GRID_N = 257;

function finite(x) {
  return Number.isFinite(x);
}

function deFactor(a, w0, wa) {
  return Math.pow(a, -3 * (1 + w0 + wa)) * Math.exp(-3 * wa * (1 - a));
}

function omegaM(z, om0, w0, wa) {
  const a = 1 / (1 + z);
  const matter = om0 * Math.pow(a, -3);
  const de = (1 - om0) * deFactor(a, w0, wa);
  const den = matter + de;
  if (!(den > 0) || !finite(den)) return NaN;
  return matter / den;
}

function chiDelta(z, om0, w0, wa) {
  const om = omegaM(z, om0, w0, wa);
  if (!(om > 0) || !finite(om)) return NaN;
  return Math.sqrt(2 / (3 * om));
}

function qOfZ(z, om0, w0, wa) {
  const a = 1 / (1 + z);
  const om = omegaM(z, om0, w0, wa);
  if (!finite(om)) return NaN;
  const ode = 1 - om;
  const w = w0 + wa * (1 - a);
  return 0.5 * (om + ode * (1 + 3 * w));
}

function bisect(fn, lo, hi, flo, fhi) {
  let a = lo, b = hi, fa = flo, fb = fhi;
  for (let i = 0; i < 70; i++) {
    const m = 0.5 * (a + b);
    const fm = fn(m);
    if (!finite(fm)) return NaN;
    if (Math.abs(fm) < 1e-12 || Math.abs(b - a) < 1e-10) return m;
    if (fa === 0) return a;
    if (fb === 0) return b;
    if (fa * fm <= 0) {
      b = m; fb = fm;
    } else {
      a = m; fa = fm;
    }
  }
  return 0.5 * (a + b);
}

function roots(fn) {
  const out = [];
  let z0 = 0;
  let f0 = fn(z0);
  for (let i = 1; i < GRID_N; i++) {
    const z1 = ZMAX * i / (GRID_N - 1);
    const f1 = fn(z1);
    if (finite(f0) && finite(f1)) {
      if (Math.abs(f0) < 1e-12) out.push(z0);
      if (f0 * f1 < 0) {
        const r = bisect(fn, z0, z1, f0, f1);
        if (finite(r)) out.push(r);
      }
    }
    z0 = z1;
    f0 = f1;
  }
  if (finite(f0) && Math.abs(f0) < 1e-12) out.push(ZMAX);
  out.sort((a,b) => a-b);
  const merged = [];
  for (const r of out) {
    if (!merged.length || Math.abs(r - merged[merged.length - 1]) > 1e-6) merged.push(r);
  }
  return merged;
}

function weightedQuantile(values, weights, probs=[0.16,0.5,0.84]) {
  const pairs = [];
  for (let i=0; i<values.length; i++) {
    const x = values[i], w = weights[i];
    if (finite(x) && finite(w) && w >= 0) pairs.push([x,w]);
  }
  if (!pairs.length) return probs.map(() => null);
  pairs.sort((a,b) => a[0]-b[0]);
  let total = 0;
  for (const p of pairs) total += p[1];
  if (!(total > 0)) return probs.map(() => null);
  const out = [];
  for (const prob of probs) {
    const target = prob * total;
    let c = 0;
    let value = pairs[pairs.length-1][0];
    for (const [x,w] of pairs) {
      c += w;
      if (c >= target) { value = x; break; }
    }
    out.push(value);
  }
  return out;
}

function findCol(header, aliases) {
  const lower = new Map(header.map((x,i)=>[x.toLowerCase(), i]));
  for (const a of aliases) {
    const k = a.toLowerCase();
    if (lower.has(k)) return lower.get(k);
  }
  return -1;
}

function parseHeader(lines) {
  for (const line of lines) {
    if (line.startsWith("#")) {
      const h = line.slice(1).trim().split(/\s+/);
      if (h.length > 2 && h.some(x => x.toLowerCase() === "weight")) return h;
    }
  }
  throw new Error("Cobaya header not found");
}

async function fetchChain(model, n) {
  const url = `${ROOT}/${model}/${DATASET}/chain.${n}.txt`;
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`DESI fetch failed ${r.status}: ${url}`);
  const buf = Buffer.from(await r.arrayBuffer());
  return {
    url,
    bytes: buf.length,
    sha256: crypto.createHash("sha256").update(buf).digest("hex"),
    text: buf.toString("utf8")
  };
}

function paramsForRow(model, toks, idx) {
  const om0 = Number(toks[idx.om]);
  let w0 = -1, wa = 0;
  if (model === "base_w") w0 = Number(toks[idx.w]);
  if (model === "base_w_wa") {
    w0 = Number(toks[idx.w0]);
    wa = Number(toks[idx.wa]);
  }
  return {om0,w0,wa};
}

function countsFraction(counts, weights) {
  const total = weights.reduce((a,b)=>a+b,0);
  const acc = {};
  for (let i=0;i<counts.length;i++) {
    const k = String(counts[i]);
    acc[k] = (acc[k] || 0) + weights[i];
  }
  for (const k of Object.keys(acc)) acc[k] /= total;
  return acc;
}

export default async function handler(req, res) {
  try {
    const model = String(req.query?.model || "base");
    if (!MODELS.has(model)) {
      return res.status(400).json({error:"model must be base, base_w, or base_w_wa"});
    }

    const weights = [], zq = [], zchi = [], dz = [], q0s = [], chi0s = [];
    const nq = [], nchi = [], provenance = [];
    let header = null, idx = null, samples = 0, rejected = 0;

    for (let n=1;n<=4;n++) {
      const f = await fetchChain(model,n);
      provenance.push({url:f.url,bytes:f.bytes,sha256:f.sha256});
      const lines = f.text.split(/\r?\n/);
      if (!header) {
        header = parseHeader(lines);
        idx = {
          weight: findCol(header,["weight","weights"]),
          om: findCol(header,["omegam","omega_m","Omega_m","Omega_m0"]),
          w: findCol(header,["w","w0","w_0"]),
          w0: findCol(header,["w","w0","w_0"]),
          wa: findCol(header,["wa","w_a"])
        };
        if (idx.weight < 0 || idx.om < 0) throw new Error(`required columns missing: ${header.join(",")}`);
        if (model === "base_w" && idx.w < 0) throw new Error("w column missing");
        if (model === "base_w_wa" && (idx.w0 < 0 || idx.wa < 0)) throw new Error("w0/wa columns missing");
      }
      for (const line of lines) {
        if (!line || line[0] === "#") continue;
        const toks = line.trim().split(/\s+/);
        if (toks.length < header.length) continue;
        const wt = Number(toks[idx.weight]);
        const {om0,w0,wa} = paramsForRow(model,toks,idx);
        if (!(wt >= 0) || !(om0 > 0 && om0 < 1) || !finite(w0) || !finite(wa)) {
          rejected++;
          continue;
        }
        const qr = roots(z => qOfZ(z,om0,w0,wa));
        const cr = roots(z => chiDelta(z,om0,w0,wa)-1);
        const qprimary = qr.length ? qr[0] : NaN;
        const cprimary = cr.length ? cr[0] : NaN;
        weights.push(wt);
        zq.push(qprimary);
        zchi.push(cprimary);
        dz.push(finite(qprimary)&&finite(cprimary) ? qprimary-cprimary : NaN);
        q0s.push(qOfZ(0,om0,w0,wa));
        chi0s.push(chiDelta(0,om0,w0,wa));
        nq.push(qr.length);
        nchi.push(cr.length);
        samples++;
      }
      f.text = null;
    }

    const totalWeight = weights.reduce((a,b)=>a+b,0);
    const validMask = dz.map(finite);
    let validWeight = 0;
    for (let i=0;i<weights.length;i++) if (validMask[i]) validWeight += weights[i];

    function summary(arr) {
      const [q16,median,q84] = weightedQuantile(arr,weights);
      return {q16,median,q84};
    }

    const output = {
      status:"ok",
      model,
      dataset:DATASET,
      samples,
      rejected_rows:rejected,
      columns:{header,indices:idx},
      weight_sum:totalWeight,
      valid_delta_z_weight_fraction:validWeight/totalWeight,
      q_root_counts_weight_fraction:countsFraction(nq,weights),
      chi_root_counts_weight_fraction:countsFraction(nchi,weights),
      z_q0:summary(zq),
      z_chi1:summary(zchi),
      delta_z:summary(dz),
      q0:summary(q0s),
      chi_delta0:summary(chi0s),
      provenance
    };

    if (model === "base") {
      let maxAbs = 0;
      for (const x of dz) if (finite(x)) maxAbs = Math.max(maxAbs,Math.abs(x));
      output.lcdm_identity_max_abs_delta_z = maxAbs;
      output.lcdm_identity_pass = maxAbs < 1e-7;
      if (!output.lcdm_identity_pass) {
        output.status = "fail";
        return res.status(422).json(output);
      }
    }

    return res.status(200).json(output);
  } catch (err) {
    console.error(err);
    return res.status(500).json({status:"error",error:String(err?.stack || err)});
  }
}
