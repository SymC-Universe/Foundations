#!/usr/bin/env python3
import hashlib, json, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import pyfbs

BASE="https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/"
EXPECTED={
 "Y_A.p":"3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4",
 "Y_B.p":"2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12",
 "AM_Measurements.xlsx":"b70f1abcf9f64cdd02140380fa6fc25a27d1ad463a734bf0346f316140acc4c8"
}
OUT=Path("stability_inheritance/results/pyfbs_vpt_identity_v0_2")
RAW=OUT/"raw"
OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)
hashes={}
for name,exp in EXPECTED.items():
    p=RAW/name
    urllib.request.urlretrieve(BASE+name,p)
    h=hashlib.sha256(p.read_bytes()).hexdigest(); hashes[name]=h
    if h!=exp:
        raise RuntimeError(f"hash mismatch {name}: expected {exp}, got {h}")

def load(name):
    obj=np.load(RAW/name,allow_pickle=True)
    f=np.asarray(obj[0],float).reshape(-1)
    raw=np.asarray(obj[1])
    if raw.ndim!=3 or raw.shape[2]!=f.size:
        raise RuntimeError(f"unexpected {name} shape {raw.shape}, freq={f.shape}")
    return f,np.transpose(raw,(2,0,1)).astype(complex)

fA,YA=load("Y_A.p"); fB,YB=load("Y_B.p")
if not np.allclose(fA,fB,rtol=0,atol=1e-12):
    raise RuntimeError("INVALID_DATA_ALIGNMENT")
freq=fA
xlsx=RAW/"AM_Measurements.xlsx"
chnA=pd.read_excel(xlsx,sheet_name="Channels_A")
impA=pd.read_excel(xlsx,sheet_name="Impacts_A")
chnB=pd.read_excel(xlsx,sheet_name="Channels_B")
impB=pd.read_excel(xlsx,sheet_name="Impacts_B")
vp=pd.read_excel(xlsx,sheet_name="VP_Channels")
vpref=pd.read_excel(xlsx,sheet_name="VP_RefChannels")
if (len(chnA),len(impA),len(chnB),len(impB))!=(6,6,21,21):
    raise RuntimeError(f"metadata identity mismatch {(len(chnA),len(impA),len(chnB),len(impB))}")

VPT=getattr(getattr(pyfbs,"interface",pyfbs),"VPT",None)
if VPT is None: VPT=getattr(pyfbs,"VPT")
out={"status":"PUBLIC_EXTERNAL_P0Q_PREFLIGHT","protocol":"PYFBS_MEASURED_VPT_IDENTITY_PREFLIGHT_v0.2","hashes":hashes}
try:
    vA=VPT(chnA,impA,vp,vpref)
    vB=VPT(chnB,impB,vp,vpref)
    vA.apply_vpt(freq,YA)
    vB.apply_vpt(freq,YB)
    A=np.asarray(vA.frf); B=np.asarray(vB.frf)
    finite=bool(np.isfinite(A).all() and np.isfinite(B).all())
    preserved=bool(A.shape[0]==freq.size and B.shape[0]==freq.size)
    disp="VPT_ROUTE_EXECUTABLE" if finite and preserved else "VPT_ROUTE_NOT_EXECUTABLE"
    out.update({
      "raw_shapes":{"A":list(YA.shape),"B":list(YB.shape)},
      "metadata_counts":{"channels_A":len(chnA),"impacts_A":len(impA),"channels_B":len(chnB),"impacts_B":len(impB),"vp":len(vp),"vpref":len(vpref)},
      "transform_shapes":{"tu_A":list(np.asarray(vA.tu).shape),"tf_A":list(np.asarray(vA.tf).shape),"tu_B":list(np.asarray(vB.tu).shape),"tf_B":list(np.asarray(vB.tf).shape)},
      "transformed_shapes":{"A":list(A.shape),"B":list(B.shape)},
      "finite":finite,"frequency_preserved":preserved,"disposition":disp
    })
except Exception as e:
    out.update({"disposition":"VPT_ROUTE_NOT_EXECUTABLE","exception_type":type(e).__name__,"exception":str(e)})

(OUT/"result.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
for p in RAW.iterdir(): p.unlink()
RAW.rmdir()
