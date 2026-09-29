#!/usr/bin/env python3
import hashlib, json, math, urllib.request
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import find_peaks
from scipy.stats import spearmanr

COMMIT="2d42d3a618206da58642674d3287ae34dfc7d5e5"
URL=f"https://raw.githubusercontent.com/mattiacenedese/BRBtesting/{COMMIT}/ShakerRingdown.mat"
EXPECTED_BLOB="739048b2b1c71839f773ff1aecf4880fda5d62ed"
EXPECTED_SHA256="a62c551e34cc45257257d4e683cc9406beec2cbc1c7270329658fd9033de2f4a"
OUT=Path("stability_inheritance/results/brb_scalar_modal_relation")
OUT.mkdir(parents=True,exist_ok=True)
RAW=OUT/"ShakerRingdown.mat"

def blobsha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()

def field(obj,name):
    if hasattr(obj,name): return getattr(obj,name)
    raise RuntimeError(f"missing field {name}")

def orient(a,npos,ntime,name):
    a=np.asarray(a,dtype=float)
    if a.shape==(npos,ntime): return a
    if a.shape==(ntime,npos): return a.T
    raise RuntimeError(f"{name} shape {a.shape} incompatible with {(npos,ntime)}")

def unit_basis(mat,idx,mask):
    vecs=[]
    for k in idx:
        v=mat[:,k][mask]
        n=np.linalg.norm(v)
        if not np.isfinite(n) or n<=np.finfo(float).tiny:
            return None,math.nan
        vecs.append(v/n)
    X=np.column_stack(vecs)
    U,s,_=np.linalg.svd(X,full_matrices=False)
    frac=float(s[0]**2/np.sum(s**2)) if np.sum(s**2)>0 else math.nan
    return U[:,0],frac

def ols_predict(train_X,train_y,test_X):
    X=np.column_stack([np.ones(len(train_y)),train_X]) if train_X.ndim==2 and train_X.shape[1]>0 else np.ones((len(train_y),1))
    Xt=np.column_stack([np.ones(test_X.shape[0]),test_X]) if test_X.ndim==2 and test_X.shape[1]>0 else np.ones((test_X.shape[0],1))
    beta=np.linalg.lstsq(X,train_y,rcond=None)[0]
    return Xt@beta

def rmse(a,b):
    return float(np.sqrt(np.mean((np.asarray(a)-np.asarray(b))**2)))

req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0D/1.0"})
with urllib.request.urlopen(req,timeout=120) as r:
    b=r.read()
RAW.write_bytes(b)
if blobsha(b)!=EXPECTED_BLOB or hashlib.sha256(b).hexdigest()!=EXPECTED_SHA256:
    raise RuntimeError("source identity mismatch")

try:
    d=loadmat(RAW,squeeze_me=True,struct_as_record=False,variable_names=["SRDdataDIC"])
    dic=d.get("SRDdataDIC")
    time=np.ravel(np.asarray(field(dic,"time"),dtype=float))
    pos=np.ravel(np.asarray(field(dic,"position"),dtype=float))
    above=orient(field(dic,"deflection_above"),pos.size,time.size,"above")
    below=orient(field(dic,"deflection_below"),pos.size,time.size,"below")
    if not np.all(np.diff(time)>0): raise RuntimeError("time not increasing")
    dt=float(np.median(np.diff(time)))
    ref=0.5*(above[184,:]+below[184,:])
    full=np.vstack([above,below])
    finite_mask=np.all(np.isfinite(full),axis=1)
    if finite_mask.sum()<4: raise RuntimeError("insufficient finite spatial coordinates")

    duration=0.25
    step=0.125
    starts=[]
    t=time[0]
    while t+duration <= time[-1]+1e-12:
        starts.append(t); t+=step
    min_dist=max(1,int(round(0.4/(80.0*dt))))
    windows=[]
    for wi,start in enumerate(starts):
        stop=start+duration
        inds=np.where((time>=start)&(time<stop if stop<time[-1] else time<=stop))[0]
        if inds.size<10:
            continue
        local=ref[inds]
        pk_local,_=find_peaks(np.abs(local),distance=min_dist)
        pk=inds[pk_local]
        rec={"window":wi,"start_s":float(start),"end_s":float(stop),"peak_count":int(pk.size)}
        if pk.size<10:
            rec["chi_status"]="REFUSED_INSUFFICIENT_PEAKS"; windows.append(rec); continue
        amp=np.abs(ref[pk])
        good=np.isfinite(amp)&(amp>0)
        pk=pk[good]; amp=amp[good]
        if pk.size<10:
            rec["chi_status"]="REFUSED_INSUFFICIENT_POSITIVE_PEAKS"; windows.append(rec); continue
        tt=time[pk]
        x=tt-tt.mean()
        y=np.log(amp)
        beta=np.linalg.lstsq(np.column_stack([np.ones_like(x),x]),y,rcond=None)[0]
        yhat=np.column_stack([np.ones_like(x),x])@beta
        slope=float(beta[1]); sigma=-slope
        ssres=float(np.sum((y-yhat)**2)); sstot=float(np.sum((y-y.mean())**2))
        r2=float(1-ssres/sstot) if sstot>0 else math.nan
        rmslog=float(np.sqrt(np.mean((y-yhat)**2)))
        deltas=np.diff(tt)
        deltas=deltas[np.isfinite(deltas)&(deltas>0)]
        omega_d=float(np.pi/np.median(deltas)) if deltas.size else math.nan
        chi=float(sigma/math.sqrt(sigma*sigma+omega_d*omega_d)) if sigma>0 and omega_d>0 and np.isfinite(sigma+omega_d) else math.nan
        phi,rank1=unit_basis(full,pk,finite_mask)
        rec.update({
          "median_peak_amplitude_mm":float(np.median(amp)),
          "sigma_per_s":float(sigma),
          "omega_d_rad_s":float(omega_d),
          "chi_ring":chi,
          "envelope_r2":r2,
          "envelope_rms_log_residual":rmslog,
          "rank1_fraction":rank1
        })
        if not np.isfinite(chi) or phi is None:
            rec["chi_status"]="REFUSED_NONPOSITIVE_OR_NONFINITE"
        else:
            rec["chi_status"]="LOCAL_EFFECTIVE_CHI_ADMITTED"
            rec["_phi"]=phi
        windows.append(rec)

    valid=[w for w in windows if w.get("chi_status")=="LOCAL_EFFECTIVE_CHI_ADMITTED" and "_phi" in w]
    out={
      "status":"P0D_POST_RESULT_SCALAR_MODAL_RELATION",
      "promotion_debt":True,
      "window_duration_s":duration,
      "window_step_s":step,
      "window_count_total":len(windows),
      "window_count_valid":len(valid),
      "source_reference_position_cm":float(pos[184]),
      "finite_spatial_coordinates":int(finite_mask.sum()),
      "chi_admission":"LOCAL_EFFECTIVE_CONDITIONAL_ONLY",
      "Chi_admission":"ADMITTED_NATIVE_MODAL_SUBSPACE_FROM_PARENT_TEST",
      "Chi_arc":"NOT_IDENTIFIED"
    }
    if len(valid)<8:
        out["disposition"]="CHI_RELATION_INDETERMINATE"
        out["windows"]=[{k:v for k,v in w.items() if k!="_phi"} for w in windows]
    else:
        ref_phi=valid[-1]["_phi"]
        for w in valid:
            dot=abs(float(np.dot(w["_phi"],ref_phi)))
            dot=min(1.0,max(0.0,dot))
            w["mac_to_final"]=dot*dot
            w["theta_to_final_deg"]=float(np.degrees(np.arccos(dot)))
        chi=np.array([w["chi_ring"] for w in valid],float)
        amp=np.array([w["median_peak_amplitude_mm"] for w in valid],float)
        logamp=np.log(amp)
        theta=np.array([w["theta_to_final_deg"] for w in valid],float)
        rho_chi_theta,p_chi_theta=spearmanr(chi,theta)
        rho_amp_theta,p_amp_theta=spearmanr(logamp,theta)
        rho_chi_amp,p_chi_amp=spearmanr(chi,logamp)
        N=len(valid); ntr=int(np.floor(2*N/3))
        if ntr<3 or N-ntr<2 or np.std(chi[:ntr])<=1e-15 or np.std(logamp[:ntr])<=1e-15:
            disposition="CHI_RELATION_INDETERMINATE"
            rmses={}
        else:
            mu_chi,sd_chi=float(np.mean(chi[:ntr])),float(np.std(chi[:ntr],ddof=0))
            mu_amp,sd_amp=float(np.mean(logamp[:ntr])),float(np.std(logamp[:ntr],ddof=0))
            zchi=(chi-mu_chi)/sd_chi
            zamp=(logamp-mu_amp)/sd_amp
            ytr=theta[:ntr]; yte=theta[ntr:]
            pred0=np.repeat(np.mean(ytr),len(yte))
            predA=ols_predict(zamp[:ntr,None],ytr,zamp[ntr:,None])
            predC=ols_predict(zchi[:ntr,None],ytr,zchi[ntr:,None])
            predB=ols_predict(np.column_stack([zamp[:ntr],zchi[:ntr]]),ytr,np.column_stack([zamp[ntr:],zchi[ntr:]]))
            rmses={"M0":rmse(yte,pred0),"M_amp":rmse(yte,predA),"M_chi":rmse(yte,predC),"M_both":rmse(yte,predB),"train_windows":ntr,"test_windows":N-ntr}
            if rmses["M_chi"] < rmses["M0"]:
                disposition="CHI_ADDS_BEYOND_AMPLITUDE_FOR_DECLARED_TASK" if rmses["M_both"] < rmses["M_amp"] else "CHI_TRACKS_BUT_IS_REDUNDANT_WITH_AMPLITUDE"
            else:
                disposition="CHI_NOT_OPERATIONALLY_PREDICTIVE_OF_MODAL_GEOMETRY"
        out.update({
          "chi_range":[float(np.min(chi)),float(np.max(chi))],
          "theta_range_deg":[float(np.min(theta)),float(np.max(theta))],
          "amplitude_range_mm":[float(np.min(amp)),float(np.max(amp))],
          "spearman":{
            "chi_vs_theta":{"rho":float(rho_chi_theta),"p":float(p_chi_theta)},
            "logamp_vs_theta":{"rho":float(rho_amp_theta),"p":float(p_amp_theta)},
            "chi_vs_logamp":{"rho":float(rho_chi_amp),"p":float(p_chi_amp)}
          },
          "prediction_rmse":rmses,
          "envelope_r2_median":float(np.nanmedian([w["envelope_r2"] for w in valid])),
          "envelope_r2_min":float(np.nanmin([w["envelope_r2"] for w in valid])),
          "rank1_fraction_median":float(np.nanmedian([w["rank1_fraction"] for w in valid])),
          "rank1_fraction_min":float(np.nanmin([w["rank1_fraction"] for w in valid])),
          "disposition":disposition,
          "windows":[{k:v for k,v in w.items() if k!="_phi"} for w in windows]
        })
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
finally:
    RAW.unlink(missing_ok=True)
