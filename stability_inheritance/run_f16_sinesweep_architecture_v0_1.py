#!/usr/bin/env python3
import hashlib, json, math, urllib.request, zipfile, tempfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import hilbert, fftconvolve, windows

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
EXPECTED_SHA256="2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa"
OUT=Path("stability_inheritance/results/f16_gvt_sinesweep_architecture")
OUT.mkdir(parents=True,exist_ok=True)

FS=400.0
LEVEL_FORCE={1:4.8,2:19.2,3:28.8,4:57.6,5:67.0,6:86.0,7:95.6}
EST=[1,3,5,7]
TEST=[2,4,6]
WINDOW_S=4.0
NWIN=int(round(WINDOW_S*FS))
HALF=NWIN//2
MONO_GATE=0.90
GRID_PRIMARY=np.arange(6.5,8.2+1e-12,0.05)
GRID_SECONDARY=np.arange(2.5,14.5+1e-12,0.05)

def smooth_complex(x,w):
    return fftconvolve(x,w,mode="same")

def trajectory(voltage,force,acc):
    voltage=np.asarray(voltage,float).reshape(-1)
    force=np.asarray(force,float).reshape(-1)
    acc=np.asarray(acc,float)
    if acc.ndim!=2:
        raise RuntimeError(f"acc ndim {acc.ndim}")
    if acc.shape[0]!=3 and acc.shape[1]==3:
        acc=acc.T
    if acc.shape[0]!=3 or acc.shape[1]!=voltage.size or force.size!=voltage.size:
        raise RuntimeError(f"shape mismatch v={voltage.shape} f={force.shape} a={acc.shape}")
    v=hilbert(voltage-np.mean(voltage))
    u=hilbert(force-np.mean(force))
    y=np.vstack([hilbert(acc[j]-np.mean(acc[j])) for j in range(3)])
    phase=np.unwrap(np.angle(v))
    finst=np.gradient(phase)*FS/(2*np.pi)
    w=windows.hann(NWIN,sym=True)
    w=w/np.sum(w)
    den=smooth_complex(np.abs(u)**2,w).real
    H=np.empty((voltage.size,3),complex)
    for j in range(3):
        num=smooth_complex(y[j]*np.conj(u),w)
        H[:,j]=num/np.maximum(den,np.finfo(float).tiny)
    valid=np.isfinite(finst)&np.isfinite(den)
    valid[:HALF]=False; valid[-HALF:]=False
    valid &= (finst>=2.0)&(finst<=15.0)
    maxden=float(np.max(den[valid])) if np.any(valid) else 0.0
    valid &= den > 1e-12*maxden
    fv=finst[valid]; Hv=H[valid]
    if fv.size<10:
        raise RuntimeError("insufficient valid chirp samples")
    monotonic_fraction=float(np.mean(np.diff(fv)<0))
    coverage=(float(np.min(fv)),float(np.max(fv)))
    if monotonic_fraction<MONO_GATE:
        raise RuntimeError(f"chirp monotonicity gate failed {monotonic_fraction}")
    order=np.argsort(fv)
    x=fv[order]; Y=Hv[order]
    # collapse exact duplicate x coordinates by retaining the first sorted occurrence
    xu,idx=np.unique(x,return_index=True)
    Yu=Y[idx]
    def interp(grid):
        if grid.min()<xu.min() or grid.max()>xu.max():
            raise RuntimeError(f"frequency coverage {xu.min()}-{xu.max()} does not cover grid {grid.min()}-{grid.max()}")
        out=np.empty((grid.size,3),complex)
        for j in range(3):
            out[:,j]=np.interp(grid,xu,Yu[:,j].real)+1j*np.interp(grid,xu,Yu[:,j].imag)
        return out
    return interp(GRID_PRIMARY),interp(GRID_SECONDARY),{
      "n_samples":int(voltage.size),
      "valid_samples":int(fv.size),
      "monotonic_decreasing_fraction":monotonic_fraction,
      "valid_frequency_min_hz":coverage[0],
      "valid_frequency_max_hz":coverage[1],
      "force_energy_max":maxden
    }

def normerr(pred,ref):
    den=np.sum(np.abs(ref)**2)
    if not np.isfinite(den) or den<=np.finfo(float).tiny:
        return math.nan
    return float(np.sqrt(np.sum(np.abs(pred-ref)**2)/den))

def amp_interp(a,b,target,H):
    w=(LEVEL_FORCE[target]-LEVEL_FORCE[a])/(LEVEL_FORCE[b]-LEVEL_FORCE[a])
    return (1-w)*H[a]+w*H[b]

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
        raise RuntimeError(f"source size changed {len(b)}")
    sha=hashlib.sha256(b).hexdigest()
    if sha!=EXPECTED_SHA256:
        raise RuntimeError(f"source hash changed {sha}")
    with zipfile.ZipFile(zpath,"r") as z:
        z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"

    Hp={}; Hs={}; quality={}; names={}
    for lev in range(1,8):
        candidates=[p for p in root.rglob("*.mat") if "sinesw" in p.name.replace(" ","").lower() and (f"level{lev}" in p.name.replace(" ","").lower() or f"level0{lev}" in p.name.replace(" ","").lower())]
        if len(candidates)!=1:
            raise RuntimeError(f"sine-sweep file identity level {lev}: {candidates}")
        p=candidates[0]; names[str(lev)]=p.name
        d=loadmat(p)
        for key in ["Voltage","Force","Acceleration","Fs"]:
            if key not in d: raise RuntimeError(f"{key} missing {p.name}")
        fs=float(np.asarray(d["Fs"]).squeeze())
        if abs(fs-FS)>1e-9: raise RuntimeError(f"Fs mismatch {fs} {p.name}")
        v=np.asarray(d["Voltage"]).squeeze()
        u=np.asarray(d["Force"]).squeeze()
        y=np.asarray(d["Acceleration"])
        Hp[lev],Hs[lev],quality[str(lev)]=trajectory(v,u,y)

    predp={
      2:amp_interp(1,3,2,Hp),
      4:amp_interp(3,5,4,Hp),
      6:amp_interp(5,7,6,Hp)
    }
    preds={
      2:amp_interp(1,3,2,Hs),
      4:amp_interp(3,5,4,Hs),
      6:amp_interp(5,7,6,Hs)
    }

    scores={}
    ratios=[]
    for lev in TEST:
        ep=normerr(predp[lev],Hp[lev])
        ef=normerr(Hp[1],Hp[lev])
        rp=ep/ef if np.isfinite(ep) and np.isfinite(ef) and ef>0 else math.nan
        ratios.append(rp)
        per={}
        for j in range(3):
            per[str(j+1)]={
              "conditioned":normerr(predp[lev][:,j],Hp[lev][:,j]),
              "fixed":normerr(Hp[1][:,j],Hp[lev][:,j])
            }
        rel_ref=Hp[lev][:,2]-Hp[lev][:,1]
        rel_pred=predp[lev][:,2]-predp[lev][:,1]
        rel_fixed=Hp[1][:,2]-Hp[1][:,1]
        scores[str(lev)]={
          "force_N":LEVEL_FORCE[lev],
          "primary":{"conditioned":ep,"fixed":ef,"ratio":rp},
          "secondary_2p5_14p5":{
             "conditioned":normerr(preds[lev],Hs[lev]),
             "fixed":normerr(Hs[1],Hs[lev])
          },
          "per_output_primary":per,
          "interface_relative_primary":{
             "conditioned":normerr(rel_pred,rel_ref),
             "fixed":normerr(rel_fixed,rel_ref)
          }
        }

    if not all(np.isfinite(r) for r in ratios):
        disp="INDETERMINATE"
    else:
        wins=sum(r<1 for r in ratios)
        if wins==3: disp="SINESWEEP_AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT"
        elif wins==0: disp="SINESWEEP_FIXED_REFERENCE_NOT_OUTPERFORMED"
        else: disp="SINESWEEP_MIXED_ARCHITECTURE"

    peaks={}
    for lev in range(1,8):
        peaks[str(lev)]={}
        for j in range(3):
            idx=int(np.argmax(np.abs(Hp[lev][:,j])))
            peaks[str(lev)][str(j+1)]=float(GRID_PRIMARY[idx])

    out={
      "status":"PUBLIC_EXTERNAL_P0Q",
      "protocol":"F16_GVT_SINESWEEP_ARCHITECTURE_PROTOCOL_v0.1",
      "source_sha256":sha,
      "files":names,
      "sampling_hz":FS,
      "smoothing_seconds":WINDOW_S,
      "monotonicity_gate":MONO_GATE,
      "primary_grid_hz":[float(GRID_PRIMARY[0]),float(GRID_PRIMARY[-1]),0.05],
      "secondary_grid_hz":[float(GRID_SECONDARY[0]),float(GRID_SECONDARY[-1]),0.05],
      "quality":quality,
      "scores":scores,
      "primary_ratios":ratios,
      "primary_peak_frequency_hz":peaks,
      "disposition":disp,
      "architecture_evidence_role":"ARCHITECTURE_SUPPORTING_NATIVE_THIRD_EXCITATION_FAMILY" if disp=="SINESWEEP_AMPLITUDE_CONDITIONED_ARCHITECTURE_SUPPORT" else "MIXED_OR_LIMIT_NATIVE_EVIDENCE",
      "novelty_role":"NATIVE_MODEL_COMPATIBLE_NO_SI_NOVELTY_CLAIM",
      "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED_NATIVE_RESPONSE_TRAJECTORY_USED","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"}
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
