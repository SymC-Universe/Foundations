#!/usr/bin/env python3
import hashlib, json, math, tempfile, urllib.request, zipfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import hilbert, stft, medfilt

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
EXPECTED_SHA="2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa"
FS=400.0
RATE=-0.05
OUT=Path("stability_inheritance/results/f16_sinesweep_input_coordinate")
OUT.mkdir(parents=True,exist_ok=True)

def linfit(t,f):
    t=np.asarray(t,float); f=np.asarray(f,float)
    mask=np.isfinite(t)&np.isfinite(f)&(f>=2)&(f<=15)
    t=t[mask]; f=f[mask]
    if t.size<5:
        return None
    A=np.column_stack([np.ones(t.size),t])
    coef=np.linalg.lstsq(A,f,rcond=None)[0]
    pred=A@coef
    ssr=float(np.sum((f-pred)**2))
    sst=float(np.sum((f-np.mean(f))**2))
    r2=1-ssr/sst if sst>0 else math.nan
    mono=float(np.mean(np.diff(f)<0)) if f.size>1 else math.nan
    return {
      "slope_hz_s":float(coef[1]),
      "abs_rate_error_hz_s":float(abs(abs(coef[1])-0.05)),
      "r2":float(r2),
      "fmin":float(np.min(f)),
      "fmax":float(np.max(f)),
      "covers_primary":bool(np.min(f)<=6.5 and np.max(f)>=8.2),
      "monotonic_decreasing_fraction":mono,
      "n":int(f.size)
    }

def c1(voltage):
    x=np.asarray(voltage,float).reshape(-1)
    t=np.arange(x.size)/FS
    z=hilbert(x-np.mean(x))
    ph=np.unwrap(np.angle(z))
    f=np.gradient(ph)*FS/(2*np.pi)
    return linfit(t,f)

def c2(voltage):
    x=np.asarray(voltage,float).reshape(-1)
    t=np.arange(x.size)/FS
    z=hilbert(x-np.mean(x))
    ph=np.unwrap(np.angle(z))
    edge=int(2*FS)
    sl=slice(edge,-edge if edge else None)
    tt=t[sl]; pp=ph[sl]
    A=np.column_stack([np.ones(tt.size),tt,tt**2])
    coef=np.linalg.lstsq(A,pp,rcond=None)[0]
    f=(coef[1]+2*coef[2]*tt)/(2*np.pi)
    q=linfit(tt,f)
    if q is not None:
        pred=A@coef
        ssr=float(np.sum((pp-pred)**2)); sst=float(np.sum((pp-np.mean(pp))**2))
        q["phase_fit_r2"]=float(1-ssr/sst if sst>0 else math.nan)
    return q

def c3(voltage):
    x=np.asarray(voltage,float).reshape(-1)-float(np.mean(voltage))
    nper=1600; nover=1200
    f,t,Z=stft(x,fs=FS,window="hann",nperseg=nper,noverlap=nover,boundary=None,padded=False)
    band=(f>=1.5)&(f<=16.5)
    fb=f[band]; mag=np.abs(Z[band,:])
    ridge=fb[np.argmax(mag,axis=0)]
    ridge=medfilt(ridge,kernel_size=5)
    return linfit(t,ridge)

def c4(voltage):
    x=np.asarray(voltage,float).reshape(-1)-float(np.mean(voltage))
    idx=np.where((x[:-1]<0)&(x[1:]>=0))[0]
    if idx.size<10:
        return None
    frac=-x[idx]/(x[idx+1]-x[idx])
    tc=(idx+frac)/FS
    dt=np.diff(tc)
    good=dt>0
    ff=1.0/dt[good]
    tm=(tc[:-1][good]+tc[1:][good])/2
    if ff.size>=11:
        ff=medfilt(ff,kernel_size=11)
    return linfit(tm,ff)

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    zpath=td/"F16GVT_Files.zip"
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0D/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, zpath.open("wb") as f:
        while True:
            b=resp.read(1024*1024)
            if not b: break
            f.write(b)
    raw=zpath.read_bytes()
    if len(raw)!=EXPECTED_SIZE or hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:
        raise RuntimeError("official source identity mismatch")
    with zipfile.ZipFile(zpath,"r") as z:
        z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"
    results={"C1_RAW_HILBERT":{},"C2_QUADRATIC_PHASE":{},"C3_STFT_RIDGE":{},"C4_ZERO_CROSS":{}}
    files={}
    for lev in range(1,8):
        cand=[p for p in root.rglob("*.mat") if "sinesw" in p.name.replace(" ","").lower() and (f"level{lev}" in p.name.replace(" ","").lower() or f"level0{lev}" in p.name.replace(" ","").lower())]
        if len(cand)!=1:
            raise RuntimeError(f"file identity level {lev}: {cand}")
        p=cand[0]; files[str(lev)]=p.name
        d=loadmat(p,variable_names=["Voltage","Force","Fs"])
        fs=float(np.asarray(d["Fs"]).squeeze())
        if abs(fs-FS)>1e-9:
            raise RuntimeError(f"sampling mismatch level {lev}")
        v=np.asarray(d["Voltage"]).squeeze()
        # Force is loaded only to verify same acquisition length; values are not analyzed.
        force=np.asarray(d["Force"]).squeeze()
        if v.size!=force.size:
            raise RuntimeError(f"excitation length mismatch level {lev}")
        for key,fun in [
          ("C1_RAW_HILBERT",c1),
          ("C2_QUADRATIC_PHASE",c2),
          ("C3_STFT_RIDGE",c3),
          ("C4_ZERO_CROSS",c4)
        ]:
            results[key][str(lev)]=fun(v)

    qualification={}
    for key,vals in results.items():
        ok=True; errs=[]; r2s=[]; monos=[]
        for lev in range(1,8):
            q=vals[str(lev)]
            if q is None:
                ok=False; continue
            cond=(np.isfinite(q["slope_hz_s"]) and q["slope_hz_s"]<0 and q["covers_primary"]
                  and q["abs_rate_error_hz_s"]<=0.005 and np.isfinite(q["r2"]) and q["r2"]>=0.98)
            ok=ok and bool(cond)
            errs.append(q["abs_rate_error_hz_s"]); r2s.append(q["r2"]); monos.append(q["monotonic_decreasing_fraction"])
        qualification[key]={
          "all_levels_qualified":bool(ok),
          "median_abs_rate_error_hz_s":float(np.median(errs)) if errs else math.nan,
          "median_r2":float(np.median(r2s)) if r2s else math.nan,
          "median_monotonic_fraction":float(np.median(monos)) if monos else math.nan
        }
    eligible=[k for k,v in qualification.items() if v["all_levels_qualified"]]
    selected=None
    if eligible:
        selected=sorted(eligible,key=lambda k:(
          qualification[k]["median_abs_rate_error_hz_s"],
          -qualification[k]["median_r2"],
          -qualification[k]["median_monotonic_fraction"]
        ))[0]
        disp="INPUT_COORDINATE_QUALIFIED"
    else:
        disp="INPUT_COORDINATE_NOT_QUALIFIED"
    out={
      "status":"P0D_INPUT_ONLY_METHOD_QUALIFICATION",
      "source_sha256":EXPECTED_SHA,
      "files":files,
      "acceleration_loaded":False,
      "published_rate_hz_s":RATE,
      "results":results,
      "qualification":qualification,
      "selected_candidate":selected,
      "disposition":disp
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
