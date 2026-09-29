#!/usr/bin/env python3
import hashlib, json, math, urllib.request
from pathlib import Path
import numpy as np
from scipy.io import loadmat
from scipy.signal import find_peaks

COMMIT="2d42d3a618206da58642674d3287ae34dfc7d5e5"
URL=f"https://raw.githubusercontent.com/mattiacenedese/BRBtesting/{COMMIT}/ShakerRingdown.mat"
EXPECTED_BLOB="739048b2b1c71839f773ff1aecf4880fda5d62ed"
EXPECTED_SHA256="a62c551e34cc45257257d4e683cc9406beec2cbc1c7270329658fd9033de2f4a"
OUT=Path("stability_inheritance/results/brb_ringdown_modal_geometry")
OUT.mkdir(parents=True,exist_ok=True)
RAW=OUT/"ShakerRingdown.mat"

def blobsha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()

def field(obj,name):
    if hasattr(obj,name):
        return getattr(obj,name)
    raise RuntimeError(f"missing field {name}")

def orient(a,npos,ntime,name):
    a=np.asarray(a,dtype=float)
    if a.shape==(npos,ntime):
        return a
    if a.shape==(ntime,npos):
        return a.T
    raise RuntimeError(f"{name} shape {a.shape} does not match positions/time {(npos,ntime)}")

def unit_vectors(mat,idx,mask):
    out=[]
    for k in idx:
        v=mat[:,k][mask]
        n=np.linalg.norm(v)
        if not np.isfinite(n) or n<=np.finfo(float).tiny:
            raise RuntimeError("zero/nonfinite spatial vector")
        out.append(v/n)
    return out

def basis(vecs):
    X=np.column_stack(vecs)
    U,s,_=np.linalg.svd(X,full_matrices=False)
    phi=U[:,0]
    frac=float((s[0]**2)/np.sum(s**2)) if np.sum(s**2)>0 else math.nan
    return phi,frac

def mac(a,b):
    return float(abs(np.dot(a,b))**2)

def errs(vecs,phi):
    e=[]
    for v in vecs:
        q=abs(float(np.dot(phi,v)))
        q=min(1.0,max(0.0,q))
        e.append(math.sqrt(max(0.0,1-q*q)))
    return np.asarray(e,float)

def ratio(a,b):
    if not np.isfinite(a) or not np.isfinite(b):
        return math.nan
    if b==0:
        return 0.0 if a==0 else math.inf
    return float(a/b)

req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
with urllib.request.urlopen(req,timeout=120) as r:
    b=r.read()
RAW.write_bytes(b)
if blobsha(b)!=EXPECTED_BLOB:
    raise RuntimeError("source Git blob mismatch")
if hashlib.sha256(b).hexdigest()!=EXPECTED_SHA256:
    raise RuntimeError("source SHA-256 mismatch")

try:
    d=loadmat(RAW,squeeze_me=True,struct_as_record=False,variable_names=["SRDdataDIC"])
    dic=d.get("SRDdataDIC")
    if dic is None:
        raise RuntimeError("missing SRDdataDIC")
    time=np.ravel(np.asarray(field(dic,"time"),dtype=float))
    pos=np.ravel(np.asarray(field(dic,"position"),dtype=float))
    if time.size<10 or pos.size<185:
        raise RuntimeError(f"insufficient time/position sizes {time.size}, {pos.size}")
    if not np.all(np.diff(time)>0):
        raise RuntimeError("time not strictly increasing")
    above=orient(field(dic,"deflection_above"),pos.size,time.size,"deflection_above")
    below=orient(field(dic,"deflection_below"),pos.size,time.size,"deflection_below")
    ref=0.5*(above[184,:]+below[184,:])
    dt=float(np.median(np.diff(time)))
    min_distance=max(1,int(round(0.4/(80.0*dt))))
    peaks,_=find_peaks(np.abs(ref),distance=min_distance)
    peaks=np.asarray(peaks,dtype=int)

    base={
      "source_commit":COMMIT,
      "source_sha256":EXPECTED_SHA256,
      "time_samples":int(time.size),
      "position_count":int(pos.size),
      "time_start_s":float(time[0]),
      "time_end_s":float(time[-1]),
      "dt_s":dt,
      "peak_min_distance_samples":min_distance,
      "detected_peak_count":int(peaks.size),
      "source_reference_index_python":184,
      "source_reference_position_cm":float(pos[184]),
      "chi":"NOT_ADMITTED",
      "Chi":"CANDIDATE_MODAL_VECTOR_ADMISSION",
      "Chi_arc":"NOT_IDENTIFIED"
    }

    if peaks.size<8:
        base["disposition"]="INSUFFICIENT_RINGDOWN_PEAKS"
        (OUT/"result.json").write_text(json.dumps(base,indent=2))
        print(json.dumps(base,indent=2))
        raise SystemExit(0)

    amps=np.abs(ref[peaks])
    order=np.argsort(amps)
    n=max(3,int(peaks.size//3))
    low=np.sort(peaks[order[:n]])
    high=np.sort(peaks[order[-n:]])
    hf,ht=high[::2],high[1::2]
    lf,lt=low[::2],low[1::2]
    if min(hf.size,ht.size,lf.size,lt.size)<1:
        base["disposition"]="MODAL_RANK1_NOT_QUALIFIED"
        (OUT/"result.json").write_text(json.dumps(base,indent=2))
        print(json.dumps(base,indent=2))
        raise SystemExit(0)

    full=np.vstack([above,below])
    selected=np.concatenate([hf,ht,lf,lt])
    finite_mask=np.all(np.isfinite(full[:,selected]),axis=1)
    if finite_mask.sum()<4:
        base["disposition"]="MODAL_RANK1_NOT_QUALIFIED"
        base["finite_spatial_coordinates"]=int(finite_mask.sum())
        (OUT/"result.json").write_text(json.dumps(base,indent=2))
        print(json.dumps(base,indent=2))
        raise SystemExit(0)

    Vhf=unit_vectors(full,hf,finite_mask)
    Vht=unit_vectors(full,ht,finite_mask)
    Vlf=unit_vectors(full,lf,finite_mask)
    Vlt=unit_vectors(full,lt,finite_mask)
    phiH,fracH=basis(Vhf)
    phiL,fracL=basis(Vlf)
    phiHt,fracHt=basis(Vht)
    phiLt,fracLt=basis(Vlt)

    E_HH=float(np.median(errs(Vht,phiH)))
    E_LH=float(np.median(errs(Vht,phiL)))
    E_LL=float(np.median(errs(Vlt,phiL)))
    E_HL=float(np.median(errs(Vlt,phiH)))
    RH=ratio(E_HH,E_LH)
    RL=ratio(E_LL,E_HL)
    mac_hw=mac(phiH,phiHt)
    mac_lw=mac(phiL,phiLt)
    mac_cross=mac(phiH,phiL)
    angle=float(np.degrees(np.arccos(np.clip(math.sqrt(mac_cross),0.0,1.0))))

    cond=(E_HH<E_LH and E_LL<E_HL and mac_cross<mac_hw and mac_cross<mac_lw)
    stable=(mac_cross>=mac_hw or mac_cross>=mac_lw) and not (E_HH<E_LH and E_LL<E_HL)
    if cond:
        disp="AMPLITUDE_CONDITIONED_MODAL_GEOMETRY"
        role="ARCHITECTURE_SUPPORTING_NATIVE_MODAL_REORGANIZATION"
        chi_status="ADMITTED_NATIVE_MODAL_SUBSPACE_FOR_DECLARED_TASK"
    elif stable:
        disp="MODAL_GEOMETRY_STABLE_WITHIN_REPEATABILITY"
        role="ARCHITECTURE_SUPPORTING_NATIVE_MODAL_STABILITY"
        chi_status="ADMITTED_NATIVE_MODAL_SUBSPACE_FOR_DECLARED_TASK"
    else:
        disp="MIXED_MODAL_GEOMETRY"
        role="MIXED_NATIVE_MODAL_EVIDENCE"
        chi_status="CANDIDATE_MODAL_SUBSPACE_MIXED"

    # Secondary above/below, same peaks/splits.
    secondary={}
    for name,mat in [("above",above),("below",below)]:
        mask=np.all(np.isfinite(mat[:,selected]),axis=1)
        ahf=unit_vectors(mat,hf,mask); aht=unit_vectors(mat,ht,mask)
        alf=unit_vectors(mat,lf,mask); alt=unit_vectors(mat,lt,mask)
        pH,fH=basis(ahf); pL,fL=basis(alf)
        pHt,_=basis(aht); pLt,_=basis(alt)
        secondary[name]={
          "E_HH":float(np.median(errs(aht,pH))),
          "E_LH":float(np.median(errs(aht,pL))),
          "E_LL":float(np.median(errs(alt,pL))),
          "E_HL":float(np.median(errs(alt,pH))),
          "MAC_H_within":mac(pH,pHt),
          "MAC_L_within":mac(pL,pLt),
          "MAC_cross":mac(pH,pL),
          "rank1_fraction_H_fit":fH,
          "rank1_fraction_L_fit":fL,
          "coordinate_count":int(mask.sum())
        }

    out=base | {
      "high_peak_count":int(high.size),
      "low_peak_count":int(low.size),
      "high_fit_count":int(hf.size),
      "high_test_count":int(ht.size),
      "low_fit_count":int(lf.size),
      "low_test_count":int(lt.size),
      "high_reference_peak_median_mm":float(np.median(np.abs(ref[high]))),
      "low_reference_peak_median_mm":float(np.median(np.abs(ref[low]))),
      "finite_spatial_coordinates":int(finite_mask.sum()),
      "E_HH":E_HH,"E_LH":E_LH,"E_LL":E_LL,"E_HL":E_HL,
      "R_H":RH,"R_L":RL,
      "MAC_H_within":mac_hw,"MAC_L_within":mac_lw,"MAC_cross":mac_cross,
      "principal_angle_high_low_deg":angle,
      "rank1_fraction_H_fit":fracH,
      "rank1_fraction_L_fit":fracL,
      "rank1_fraction_H_test":fracHt,
      "rank1_fraction_L_test":fracLt,
      "secondary":secondary,
      "disposition":disp,
      "architecture_evidence_role":role,
      "Chi":chi_status,
      "novelty_role":"KNOWN_NATIVE_AMPLITUDE_DEPENDENT_MODE_SHAPE_NO_SI_NOVELTY"
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
finally:
    RAW.unlink(missing_ok=True)
