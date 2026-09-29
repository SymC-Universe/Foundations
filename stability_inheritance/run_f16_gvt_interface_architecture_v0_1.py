#!/usr/bin/env python3
import hashlib, json, math, urllib.request, zipfile, tempfile, shutil
from pathlib import Path
import numpy as np
from scipy.io import loadmat

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
OUT=Path("stability_inheritance/results/f16_gvt_interface_architecture")
OUT.mkdir(parents=True,exist_ok=True)
INTAKE=Path("stability_inheritance/results/f16_gvt_intake/manifest.json")
if not INTAKE.exists():
    raise RuntimeError("F16 intake manifest missing")
manifest=json.loads(INTAKE.read_text())
if manifest.get("disposition")!="INTAKE_PASS":
    raise RuntimeError(f"F16 intake not passed: {manifest.get('disposition')}")
expected_sha=manifest.get("sha256")

LEVEL_FORCE={1:12.4,2:24.6,3:36.8,4:61.4,5:73.6,6:85.7,7:97.8}
EST=[1,3,5,7]
TEST=[2,4,6]
N=8192
P=9
FS=400.0

def normerr(pred,ref):
    den=np.sum(np.abs(ref)**2)
    if not np.isfinite(den) or den<=np.finfo(float).tiny:
        return math.nan
    return float(np.sqrt(np.sum(np.abs(pred-ref)**2)/den))

def repdist(a,b):
    den=np.sum(np.abs(b)**2)
    if den<=np.finfo(float).tiny:
        return math.nan
    return float(np.sqrt(np.sum(np.abs(a-b)**2)/den))

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    zpath=td/"F16GVT_Files.zip"
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, zpath.open("wb") as f:
        while True:
            chunk=resp.read(1024*1024)
            if not chunk: break
            f.write(chunk)
    b=zpath.read_bytes()
    if len(b)!=EXPECTED_SIZE:
        raise RuntimeError(f"source size changed {len(b)} != {EXPECTED_SIZE}")
    sha=hashlib.sha256(b).hexdigest()
    if expected_sha and sha!=expected_sha:
        raise RuntimeError(f"source hash changed {sha} != intake {expected_sha}")
    with zipfile.ZipFile(zpath,"r") as z:
        z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"
    files=list(root.rglob("*.mat"))
    level_files={}
    for p in files:
        name=p.name.replace(" ","").lower()
        if "fullmsine" not in name or "specialodd" in name:
            continue
        for lev in range(1,8):
            if f"level{lev}" in name or f"level0{lev}" in name:
                level_files.setdefault(lev,[]).append(p)
    missing=[lev for lev in range(1,8) if lev not in level_files]
    if missing:
        raise RuntimeError(f"missing FullMSine levels {missing}")
    ambiguous={k:[str(x) for x in v] for k,v in level_files.items() if len(v)!=1}
    if ambiguous:
        raise RuntimeError(f"ambiguous FullMSine files {ambiguous}")

    freq=np.fft.rfftfreq(N,d=1/FS)
    H={}
    input_energy={}
    file_names={}
    for lev in range(1,8):
        p=level_files[lev][0]; file_names[str(lev)]=p.name
        d=loadmat(p)
        if "Force" not in d or "Acceleration" not in d or "Fs" not in d:
            raise RuntimeError(f"missing required arrays in {p.name}")
        force=np.asarray(d["Force"]).squeeze()
        acc=np.asarray(d["Acceleration"])
        fs=float(np.asarray(d["Fs"]).squeeze())
        if abs(fs-FS)>1e-9:
            raise RuntimeError(f"sampling rate {fs} in {p.name}")
        if force.size != P*N:
            raise RuntimeError(f"force length {force.size} != {P*N} in {p.name}")
        if acc.ndim!=2:
            raise RuntimeError(f"acceleration ndim {acc.ndim} in {p.name}")
        if acc.shape[0]==3 and acc.shape[1]==P*N:
            y=acc
        elif acc.shape[1]==3 and acc.shape[0]==P*N:
            y=acc.T
        else:
            raise RuntimeError(f"acceleration shape {acc.shape} in {p.name}")
        u=force.reshape(P,N)[1:,:]
        yy=y.reshape(3,P,N)[:,1:,:]
        U=np.fft.rfft(u,axis=1)
        Y=np.fft.rfft(yy,axis=2)
        den=np.sum(np.abs(U)**2,axis=0)
        num=np.sum(Y*np.conj(U)[None,:,:],axis=1)
        h=num/np.maximum(den[None,:],np.finfo(float).tiny)
        if not np.isfinite(h).all():
            raise RuntimeError(f"nonfinite FRF level {lev}")
        H[lev]=h.T
        input_energy[lev]=den

    pooled=np.sum(np.stack([input_energy[x] for x in EST]),axis=0)
    def support(lo,hi):
        band=(freq>=lo)&(freq<=hi)&(freq>0)
        if not np.any(band): return band
        mx=float(np.max(pooled[band]))
        return band & (pooled > 1e-12*mx)

    sup_primary=support(6.5,8.2)
    sup_full=support(2.0,15.0)
    if int(sup_primary.sum())<3:
        raise RuntimeError(f"insufficient primary support bins {int(sup_primary.sum())}")

    def interp(testlev):
        if testlev==2: a,b=1,3
        elif testlev==4: a,b=3,5
        elif testlev==6: a,b=5,7
        else: raise ValueError(testlev)
        w=(LEVEL_FORCE[testlev]-LEVEL_FORCE[a])/(LEVEL_FORCE[b]-LEVEL_FORCE[a])
        return (1-w)*H[a] + w*H[b]

    scores={}
    ratios=[]
    for t in TEST:
        pred=interp(t)
        inv=H[1]
        ref=H[t]
        eI=normerr(inv[sup_primary],ref[sup_primary])
        eA=normerr(pred[sup_primary],ref[sup_primary])
        eIf=normerr(inv[sup_full],ref[sup_full])
        eAf=normerr(pred[sup_full],ref[sup_full])
        outI=[]; outA=[]
        for j in range(3):
            outI.append(normerr(inv[sup_primary,j],ref[sup_primary,j]))
            outA.append(normerr(pred[sup_primary,j],ref[sup_primary,j]))
        ratio=eA/eI if np.isfinite(eA) and np.isfinite(eI) and eI>0 else math.nan
        ratios.append(ratio)
        scores[str(t)]={
          "force_rms_N":LEVEL_FORCE[t],
          "E_invariant_primary":eI,
          "E_amplitude_primary":eA,
          "ratio_amplitude_over_invariant":ratio,
          "E_invariant_full":eIf,
          "E_amplitude_full":eAf,
          "per_output_invariant_primary":outI,
          "per_output_amplitude_primary":outA
        }

    rel={}
    peak={}
    distance={}
    for lev in range(1,8):
        hrel=H[lev][:,2]-H[lev][:,1]
        rel[str(lev)]=repdist(hrel[sup_primary],(H[1][:,2]-H[1][:,1])[sup_primary])
        idx=np.where(sup_primary)[0]
        peak_i=idx[int(np.argmax(np.abs(hrel[idx])))]
        peak[str(lev)]=float(freq[peak_i])
        distance[str(lev)]={
          "excitation_output":repdist(H[lev][sup_primary,0],H[1][sup_primary,0]),
          "wing_output":repdist(H[lev][sup_primary,1],H[1][sup_primary,1]),
          "payload_output":repdist(H[lev][sup_primary,2],H[1][sup_primary,2])
        }

    finite=all(np.isfinite(r) for r in ratios)
    if not finite:
        disposition="INDETERMINATE"
    else:
        wins=sum(r<1 for r in ratios)
        if wins==3: disposition="AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT"
        elif wins==0: disposition="LOW_AMPLITUDE_REPRESENTATION_NOT_OUTPERFORMED"
        else: disposition="MIXED_AMPLITUDE_ARCHITECTURE"

    out={
      "status":"PUBLIC_EXTERNAL_P0Q",
      "protocol":"F16_GVT_INTERFACE_ARCHITECTURE_PROTOCOL_v0.1",
      "source_sha256":sha,
      "source_size_bytes":len(b),
      "files":file_names,
      "sampling_hz":FS,
      "periods_total":P,
      "periods_scored":"2-9",
      "primary_band_hz":[6.5,8.2],
      "primary_support_bins":int(sup_primary.sum()),
      "full_support_bins":int(sup_full.sum()),
      "scores":scores,
      "interface_relative_distance_from_level1":rel,
      "interface_relative_peak_hz":peak,
      "output_distance_from_level1":distance,
      "disposition":disposition,
      "architecture_evidence_role":"ARCHITECTURE_SUPPORTING_NATIVE" if disposition=="AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT" else "LIMIT_OR_MIXED_NATIVE_EVIDENCE",
      "novelty_role":"NATIVE_MODEL_COMPATIBLE_NO_SI_NOVELTY_CLAIM",
      "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED_NATIVE_FRF_USED","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"}
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
