#!/usr/bin/env python3
import hashlib, json, math, tempfile, urllib.request, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

try:
    import pyfbs
except ModuleNotFoundError:
    subprocess.run([sys.executable,"-m","pip","install","--disable-pip-version-check","pyFBS==1.0.6"],check=True)
    import pyfbs

BASE="https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/"
EXPECTED={
 "Y_A.p":"3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4",
 "Y_B.p":"2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12",
 "Y_AB.p":"197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7",
 "decoupling_example_SVT.xlsx":"a8fd8d0e42a85b0bd0837b9b54bf235ab2d489114e1b9c680f7a42184a59dd08"
}
OUT=Path("stability_inheritance/results/pyfbs_conditioning_audit_v0_1")
OUT.mkdir(parents=True,exist_ok=True)

def load(p):
    obj=np.load(p,allow_pickle=True)
    f=np.asarray(obj[0],float).reshape(-1)
    a=np.asarray(obj[1])
    return f,np.transpose(a,(2,0,1)).astype(complex)

def nerr(x,y):
    num=np.sqrt(np.sum(np.abs(x-y)**2,axis=(1,2)))
    den=np.sqrt(np.sum(np.abs(y)**2,axis=(1,2)))
    return num/np.maximum(den,np.finfo(float).tiny)

def rho(x,y):
    m=np.isfinite(x)&np.isfinite(y)&(x>0)&(y>0)
    if np.sum(m)<3: return math.nan
    return float(spearmanr(np.log10(x[m]),np.log10(y[m])).statistic)

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    for name,exp in EXPECTED.items():
        p=td/name
        urllib.request.urlretrieve(BASE+name,p)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=exp:
            raise RuntimeError(f"hash mismatch {name}")
    f,YA=load(td/"Y_A.p"); fB,YB=load(td/"Y_B.p"); fAB,YAB=load(td/"Y_AB.p")
    if not (np.allclose(f,fB,atol=1e-12,rtol=0) and np.allclose(f,fAB,atol=1e-12,rtol=0)):
        raise RuntimeError("frequency mismatch")
    meta=td/"decoupling_example_SVT.xlsx"
    chB=pd.read_excel(meta,sheet_name="Channels_B"); imB=pd.read_excel(meta,sheet_name="Impacts_B")
    chAB=pd.read_excel(meta,sheet_name="Channels_AB"); imAB=pd.read_excel(meta,sheet_name="Impacts_AB")
    SVT=getattr(getattr(pyfbs,"interface",pyfbs),"SVT",None) or getattr(pyfbs,"SVT")
    svt=SVT(chB,imB,f,YB,[1,10],6)
    apply=getattr(svt,"apply_svt",None) or getattr(svt,"apply_SVT")
    _,_,Bsv=apply(chB,imB,f,YB); _,_,ABsv=apply(chAB,imAB,f,YAB)
    Bsv=np.asarray(Bsv); ABsv=np.asarray(ABsv)
    Y=np.zeros((f.size,18,18),complex)
    Y[:,:12,:12]=ABsv; Y[:,12:,12:]=-Bsv
    Bu=np.zeros((6,18),float); Bu[:,0:6]=np.eye(6); Bu[:,12:18]=-np.eye(6)
    Yint=Bu@Y@Bu.T
    Ydec=Y-Y@Bu.T@np.linalg.pinv(Yint)@Bu@Y
    Ahat=Ydec[:,6:12,6:12]; base=ABsv[:,6:12,6:12]
    P=np.eye(6); P[[0,1]]=P[[1,0]]
    BuS=np.zeros((6,18),float); BuS[:,0:6]=np.eye(6); BuS[:,12:18]=-P
    YintS=BuS@Y@BuS.T
    YdecS=Y-Y@BuS.T@np.linalg.pinv(YintS)@BuS@Y
    shuf=YdecS[:,6:12,6:12]

    mask=f>0
    ff=f[mask]
    cond=np.array([np.linalg.cond(z) for z in Yint[mask]],float)
    d=nerr(Ahat[mask],YA[mask]); b=nerr(base[mask],YA[mask]); s=nerr(shuf[mask],YA[mask])
    r=d/np.maximum(b,np.finfo(float).tiny)
    q=d/np.maximum(s,np.finfo(float).tiny)
    amp=np.sqrt(np.sum(np.abs(YA[mask])**2,axis=(1,2)))

    corr={
      "log_condition_vs_log_DEC_over_BASE":rho(cond,r),
      "log_condition_vs_log_DEC_error":rho(cond,d),
      "log_condition_vs_log_DEC_over_SHUFFLED":rho(cond,q),
      "log_target_norm_vs_log_DEC_error":rho(amp,d),
      "log_target_norm_vs_log_DEC_over_BASE":rho(amp,r)
    }

    order=np.argsort(cond)
    splits=np.array_split(order,4)
    quart=[]
    for i,idx in enumerate(splits,1):
        quart.append({
          "quartile":i,
          "n":int(idx.size),
          "condition_min":float(np.min(cond[idx])),
          "condition_median":float(np.median(cond[idx])),
          "condition_max":float(np.max(cond[idx])),
          "frequency_min":float(np.min(ff[idx])),
          "frequency_max":float(np.max(ff[idx])),
          "DEC_error_median":float(np.median(d[idx])),
          "BASE_error_median":float(np.median(b[idx])),
          "DEC_over_BASE_median":float(np.median(r[idx])),
          "DEC_over_SHUFFLED_median":float(np.median(q[idx])),
          "fraction_DEC_lt_BASE":float(np.mean(d[idx]<b[idx])),
          "fraction_DEC_lt_SHUFFLED":float(np.mean(d[idx]<s[idx])),
          "target_norm_median":float(np.median(amp[idx]))
        })

    def rows(idx):
        return [{
          "frequency":float(ff[i]),"condition":float(cond[i]),
          "DEC_error":float(d[i]),"BASE_error":float(b[i]),
          "DEC_over_BASE":float(r[i]),"DEC_over_SHUFFLED":float(q[i]),
          "target_norm":float(amp[i])
        } for i in idx]
    highest=order[-20:][::-1]; lowest=order[:20]

    groups={}
    for name,g in [("DEC_BETTER",d<b),("DEC_NOT_BETTER",d>=b)]:
        idx=np.where(g)[0]
        groups[name]={
          "n":int(idx.size),
          "condition_median":float(np.median(cond[idx])),
          "condition_p90":float(np.quantile(cond[idx],0.9)),
          "frequency_median":float(np.median(ff[idx])),
          "DEC_error_median":float(np.median(d[idx])),
          "BASE_error_median":float(np.median(b[idx])),
          "DEC_over_BASE_median":float(np.median(r[idx])),
          "target_norm_median":float(np.median(amp[idx]))
        }

    out={
      "status":"P0D_POST_RESULT_LIMIT_MAP",
      "parent_disposition":"NATIVE_FRAMEWORK_EQUIVALENT",
      "parent_disposition_changed":False,
      "correlations":corr,
      "conditioning_quartiles":quart,
      "groups":groups,
      "highest_condition_bins":rows(highest),
      "lowest_condition_bins":rows(lowest),
      "disposition":"CONDITIONING_ERROR_MAP_COMPLETE"
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
