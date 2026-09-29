#!/usr/bin/env python3
import hashlib, json, math, tempfile, urllib.request, zipfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import hilbert, fftconvolve, windows

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
EXPECTED_SHA="2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa"
OUT=Path("stability_inheritance/results/f16_gvt_sinesweep_architecture_v0_2")
OUT.mkdir(parents=True,exist_ok=True)

FS=400.0
LEVEL_FORCE={1:4.8,2:19.2,3:28.8,4:57.6,5:67.0,6:86.0,7:95.6}
TEST=[2,4,6]
WINDOW_S=4.0
NWIN=int(WINDOW_S*FS)
HALF=NWIN//2
GRID_P=np.arange(6.5,8.2+1e-12,0.05)
GRID_S=np.arange(2.5,14.5+1e-12,0.05)

def smooth(x,w):
    return fftconvolve(x,w,mode="same")

def coordinate(voltage):
    x=np.asarray(voltage,float).reshape(-1)
    t=np.arange(x.size)/FS
    ph=np.unwrap(np.angle(hilbert(x-np.mean(x))))
    edge=int(2*FS)
    tt=t[edge:-edge]
    pp=ph[edge:-edge]
    A=np.column_stack([np.ones(tt.size),tt,tt**2])
    coef=np.linalg.lstsq(A,pp,rcond=None)[0]
    fit=A@coef
    ssr=float(np.sum((pp-fit)**2)); sst=float(np.sum((pp-np.mean(pp))**2))
    phase_r2=1-ssr/sst if sst>0 else math.nan
    f=(coef[1]+2*coef[2]*t)/(2*np.pi)
    slope=float(2*coef[2]/(2*np.pi))
    return t,f,{"slope_hz_s":slope,"phase_fit_r2":float(phase_r2)}

def trajectory(voltage,force,acc):
    voltage=np.asarray(voltage,float).reshape(-1)
    force=np.asarray(force,float).reshape(-1)
    acc=np.asarray(acc,float)
    if acc.ndim!=2: raise RuntimeError("acc ndim")
    if acc.shape[0]!=3 and acc.shape[1]==3: acc=acc.T
    if acc.shape[0]!=3 or acc.shape[1]!=voltage.size or force.size!=voltage.size:
        raise RuntimeError(f"shape mismatch {voltage.shape} {force.shape} {acc.shape}")
    t,fcoord,q=coordinate(voltage)
    u=hilbert(force-np.mean(force))
    y=np.vstack([hilbert(acc[j]-np.mean(acc[j])) for j in range(3)])
    w=windows.hann(NWIN,sym=True); w=w/np.sum(w)
    den=smooth(np.abs(u)**2,w).real
    H=np.empty((voltage.size,3),complex)
    for j in range(3):
        H[:,j]=smooth(y[j]*np.conj(u),w)/np.maximum(den,np.finfo(float).tiny)
    valid=np.isfinite(fcoord)&np.isfinite(den)
    valid[:HALF]=False; valid[-HALF:]=False
    valid &= (fcoord>=2)&(fcoord<=15)
    maxden=float(np.max(den[valid])) if np.any(valid) else 0.0
    valid &= den>1e-12*maxden
    fv=fcoord[valid]; Hv=H[valid]
    if fv.size<10: raise RuntimeError("insufficient valid samples")
    order=np.argsort(fv)
    x=fv[order]; Y=Hv[order]
    xu,idx=np.unique(x,return_index=True); Yu=Y[idx]
    def interp(grid):
        if xu.min()>grid.min() or xu.max()<grid.max():
            raise RuntimeError(f"coverage {xu.min()}-{xu.max()} for {grid.min()}-{grid.max()}")
        out=np.empty((grid.size,3),complex)
        for j in range(3):
            out[:,j]=np.interp(grid,xu,Yu[:,j].real)+1j*np.interp(grid,xu,Yu[:,j].imag)
        return out
    q.update({"valid_samples":int(fv.size),"fmin":float(xu.min()),"fmax":float(xu.max()),"force_energy_max":maxden})
    return interp(GRID_P),interp(GRID_S),q

def normerr(a,b):
    den=np.sum(np.abs(b)**2)
    if den<=np.finfo(float).tiny: return math.nan
    return float(np.sqrt(np.sum(np.abs(a-b)**2)/den))

def amp_interp(a,b,t,H):
    w=(LEVEL_FORCE[t]-LEVEL_FORCE[a])/(LEVEL_FORCE[b]-LEVEL_FORCE[a])
    return (1-w)*H[a]+w*H[b]

with tempfile.TemporaryDirectory() as td:
    td=Path(td); zpath=td/"F16.zip"
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0D/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, zpath.open("wb") as f:
        while True:
            b=resp.read(1024*1024)
            if not b: break
            f.write(b)
    raw=zpath.read_bytes()
    if len(raw)!=EXPECTED_SIZE or hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:
        raise RuntimeError("source identity mismatch")
    with zipfile.ZipFile(zpath,"r") as z: z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"
    Hp={}; Hs={}; quality={}; names={}
    for lev in range(1,8):
        cand=[p for p in root.rglob("*.mat") if "sinesw" in p.name.replace(" ","").lower() and (f"level{lev}" in p.name.replace(" ","").lower() or f"level0{lev}" in p.name.replace(" ","").lower())]
        if len(cand)!=1: raise RuntimeError(f"file identity {lev}: {cand}")
        p=cand[0]; names[str(lev)]=p.name
        d=loadmat(p)
        fs=float(np.asarray(d["Fs"]).squeeze())
        if abs(fs-FS)>1e-9: raise RuntimeError("sampling mismatch")
        Hp[lev],Hs[lev],quality[str(lev)]=trajectory(np.asarray(d["Voltage"]).squeeze(),np.asarray(d["Force"]).squeeze(),np.asarray(d["Acceleration"]))

    predp={2:amp_interp(1,3,2,Hp),4:amp_interp(3,5,4,Hp),6:amp_interp(5,7,6,Hp)}
    preds={2:amp_interp(1,3,2,Hs),4:amp_interp(3,5,4,Hs),6:amp_interp(5,7,6,Hs)}
    scores={}; ratios=[]
    for lev in TEST:
        ec=normerr(predp[lev],Hp[lev]); ef=normerr(Hp[1],Hp[lev])
        r=ec/ef if np.isfinite(ec) and np.isfinite(ef) and ef>0 else math.nan
        ratios.append(r)
        per={}
        for j in range(3):
            per[str(j+1)]={"conditioned":normerr(predp[lev][:,j],Hp[lev][:,j]),"fixed":normerr(Hp[1][:,j],Hp[lev][:,j])}
        rel=Hp[lev][:,2]-Hp[lev][:,1]
        relc=predp[lev][:,2]-predp[lev][:,1]
        relf=Hp[1][:,2]-Hp[1][:,1]
        scores[str(lev)]={
          "force_N":LEVEL_FORCE[lev],
          "primary":{"conditioned":ec,"fixed":ef,"ratio":r},
          "secondary":{"conditioned":normerr(preds[lev],Hs[lev]),"fixed":normerr(Hs[1],Hs[lev])},
          "per_output_primary":per,
          "interface_relative_primary":{"conditioned":normerr(relc,rel),"fixed":normerr(relf,rel)}
        }
    if not all(np.isfinite(r) for r in ratios): disp="INDETERMINATE"
    else:
        w=sum(r<1 for r in ratios)
        if w==3: disp="SINESWEEP_P0D_AMPLITUDE_CONDITIONED_SUPPORT"
        elif w==0: disp="SINESWEEP_P0D_FIXED_NOT_OUTPERFORMED"
        else: disp="SINESWEEP_P0D_MIXED"
    peaks={}
    for lev in range(1,8):
        peaks[str(lev)]={}
        for j in range(3):
            peaks[str(lev)][str(j+1)]=float(GRID_P[int(np.argmax(np.abs(Hp[lev][:,j])))])
    out={
      "status":"PUBLIC_EXTERNAL_P0D_POST_RESULT",
      "protocol":"F16_GVT_SINESWEEP_ARCHITECTURE_PROTOCOL_v0.2",
      "source_sha256":EXPECTED_SHA,
      "selected_input_coordinate":"C2_QUADRATIC_PHASE",
      "promotion_debt":True,
      "quality":quality,
      "scores":scores,
      "primary_ratios":ratios,
      "peak_frequency_hz":peaks,
      "disposition":disp,
      "architecture_evidence_role":"ARCHITECTURE_SUPPORTING_NATIVE_EXPLORATORY" if disp=="SINESWEEP_P0D_AMPLITUDE_CONDITIONED_SUPPORT" else "MIXED_OR_LIMIT_NATIVE_EXPLORATORY",
      "novelty_role":"NO_CONFIRMATORY_PROMOTION",
      "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"}
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
