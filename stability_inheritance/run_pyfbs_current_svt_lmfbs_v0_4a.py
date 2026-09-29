#!/usr/bin/env python3
import hashlib, json, math, tempfile, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import subprocess, sys
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
OUT=Path("stability_inheritance/results/pyfbs_current_svt_lmfbs_v0_4")
OUT.mkdir(parents=True,exist_ok=True)

def load_frf(p):
    obj=np.load(p,allow_pickle=True)
    f=np.asarray(obj[0],float).reshape(-1)
    a=np.asarray(obj[1])
    if a.ndim!=3 or a.shape[2]!=f.size:
        raise RuntimeError(f"unexpected FRF shape {a.shape} frequency {f.shape}")
    return f,np.transpose(a,(2,0,1)).astype(complex)

def global_err(x,y,mask):
    xx=x[mask]; yy=y[mask]
    den=float(np.sum(np.abs(yy)**2))
    if not np.isfinite(den) or den<=np.finfo(float).tiny:
        return math.nan
    return float(np.sqrt(np.sum(np.abs(xx-yy)**2)/den))

def pf_err(x,y,mask):
    xx=x[mask]; yy=y[mask]
    num=np.sqrt(np.sum(np.abs(xx-yy)**2,axis=(1,2)))
    den=np.sqrt(np.sum(np.abs(yy)**2,axis=(1,2)))
    return num/np.maximum(den,np.finfo(float).tiny)

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    hashes={}
    for name,exp in EXPECTED.items():
        p=td/name
        urllib.request.urlretrieve(BASE+name,p)
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        hashes[name]=h
        if h!=exp:
            out={"disposition":"INVALID_TEST","reason":f"hash mismatch {name}","hashes":hashes}
            (OUT/"result.json").write_text(json.dumps(out,indent=2))
            print(json.dumps(out,indent=2))
            raise SystemExit(0)

    fA,YA=load_frf(td/"Y_A.p")
    fB,YB=load_frf(td/"Y_B.p")
    fAB,YAB=load_frf(td/"Y_AB.p")
    if not (np.allclose(fA,fB,rtol=0,atol=1e-12) and np.allclose(fA,fAB,rtol=0,atol=1e-12)):
        out={"disposition":"INVALID_TEST","reason":"frequency mismatch","hashes":hashes}
        (OUT/"result.json").write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2)); raise SystemExit(0)

    meta=td/"decoupling_example_SVT.xlsx"
    chB=pd.read_excel(meta,sheet_name="Channels_B")
    imB=pd.read_excel(meta,sheet_name="Impacts_B")
    chAB=pd.read_excel(meta,sheet_name="Channels_AB")
    imAB=pd.read_excel(meta,sheet_name="Impacts_AB")

    SVT=getattr(getattr(pyfbs,"interface",pyfbs),"SVT",None)
    if SVT is None:
        SVT=getattr(pyfbs,"SVT")
    svt=SVT(chB,imB,fB,YB,[1,10],6)
    apply=getattr(svt,"apply_svt",None) or getattr(svt,"apply_SVT",None)
    if apply is None:
        raise RuntimeError("SVT apply method unavailable")
    _,_,Bsv=apply(chB,imB,fB,YB)
    _,_,ABsv=apply(chAB,imAB,fAB,YAB)
    Bsv=np.asarray(Bsv); ABsv=np.asarray(ABsv)
    if Bsv.shape!=(fA.size,6,6) or ABsv.shape!=(fA.size,12,12):
        out={"disposition":"INVALID_TEST","reason":"transformed shape mismatch","B_shape":list(Bsv.shape),"AB_shape":list(ABsv.shape),"hashes":hashes}
        (OUT/"result.json").write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2)); raise SystemExit(0)
    if not (np.isfinite(Bsv).all() and np.isfinite(ABsv).all() and np.isfinite(YA).all()):
        out={"disposition":"INVALID_TEST","reason":"nonfinite source/transform","hashes":hashes}
        (OUT/"result.json").write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2)); raise SystemExit(0)

    nf=fA.size
    Y=np.zeros((nf,18,18),dtype=complex)
    Y[:,:12,:12]=ABsv
    Y[:,12:,12:]=-Bsv

    Bu=np.zeros((6,18),dtype=float)
    Bu[:,0:6]=np.eye(6)
    Bu[:,12:18]=-np.eye(6)
    Bf=Bu.copy()

    Yint=Bu@Y@Bf.T
    Ydec=Y - Y@Bf.T@np.linalg.pinv(Yint)@Bu@Y
    Ahat=Ydec[:,6:12,6:12]
    base=ABsv[:,6:12,6:12]

    # deterministic wrong reduced-coordinate correspondence: swap B-side coordinates 0 and 1
    P=np.eye(6)
    P[[0,1]]=P[[1,0]]
    BuS=np.zeros((6,18),dtype=float)
    BuS[:,0:6]=np.eye(6)
    BuS[:,12:18]=-P
    BfS=BuS.copy()
    YintS=BuS@Y@BfS.T
    YdecS=Y - Y@BfS.T@np.linalg.pinv(YintS)@BuS@Y
    Ashuf=YdecS[:,6:12,6:12]

    mask=fA>0
    Edec=global_err(Ahat,YA,mask)
    Ebase=global_err(base,YA,mask)
    Eshuf=global_err(Ashuf,YA,mask)

    if not all(np.isfinite(v) for v in [Edec,Ebase,Eshuf]):
        disp="INVALID_TEST"
    else:
        tol=10*np.finfo(float).eps*max(1.0,abs(Edec),abs(Ebase))
        if Edec < Ebase-tol:
            disp="NATIVE_FRAMEWORK_EQUIVALENT"
        elif Ebase < Edec-tol:
            disp="NATIVE_MODEL_NOT_QUALIFIED_FOR_THIS_IMPLEMENTATION"
        else:
            disp="INDETERMINATE"

    ed=pf_err(Ahat,YA,mask); eb=pf_err(base,YA,mask); es=pf_err(Ashuf,YA,mask)
    cond=np.array([np.linalg.cond(z) for z in Yint[mask]],float)
    finite_count=int(np.isfinite(Ahat).sum()+np.isfinite(base).sum()+np.isfinite(Ashuf).sum())
    total_count=int(Ahat.size+base.size+Ashuf.size)

    out={
      "status":"PUBLIC_EXTERNAL_P0Q_MEASURED_HIERARCHICAL_TRANSFORMATION",
      "protocol":"PYFBS_CURRENT_METADATA_SVT_LMFBS_PROTOCOL_v0.4",
      "hashes":hashes,
      "frequency_bins_total":int(fA.size),
      "frequency_bins_primary":int(mask.sum()),
      "frequency_min_positive":float(np.min(fA[mask])),
      "frequency_max":float(np.max(fA[mask])),
      "raw_shapes":{"A":list(YA.shape),"B":list(YB.shape),"AB":list(YAB.shape)},
      "transformed_shapes":{"B":list(Bsv.shape),"AB":list(ABsv.shape),"A_hat":list(Ahat.shape)},
      "primary":{"E_DEC":Edec,"E_BASE":Ebase,"E_SHUFFLED":Eshuf},
      "improvement_DEC_vs_BASE_fraction":float((Ebase-Edec)/Ebase) if Ebase>0 else math.nan,
      "mapping_specificity":"MAPPING_SPECIFICITY_SUPPORTED" if Edec<Eshuf else "MAPPING_SPECIFICITY_NOT_SHOWN",
      "per_frequency":{
        "fraction_DEC_lt_BASE":float(np.mean(ed<eb)),
        "fraction_DEC_lt_SHUFFLED":float(np.mean(ed<es)),
        "DEC_median":float(np.median(ed)),
        "DEC_p90":float(np.quantile(ed,0.90)),
        "BASE_median":float(np.median(eb)),
        "BASE_p90":float(np.quantile(eb,0.90)),
        "SHUFFLED_median":float(np.median(es)),
        "SHUFFLED_p90":float(np.quantile(es,0.90))
      },
      "interface_condition_number":{
        "median":float(np.median(cond[np.isfinite(cond)])),
        "p90":float(np.quantile(cond[np.isfinite(cond)],0.90)),
        "max":float(np.max(cond[np.isfinite(cond)])),
        "nonfinite_count":int(np.sum(~np.isfinite(cond)))
      },
      "finite_output_fraction":float(finite_count/total_count),
      "disposition":disp,
      "architecture_evidence_role":"ARCHITECTURE_SUPPORTING_NATIVE_HIERARCHICAL_TRANSFORMATION" if disp=="NATIVE_FRAMEWORK_EQUIVALENT" else "LIMIT_OR_NATIVE_IMPLEMENTATION_EVIDENCE",
      "novelty_role":"NATIVE_FRAMEWORK_EQUIVALENT" if disp=="NATIVE_FRAMEWORK_EQUIVALENT" else "NO_SI_NOVELTY_PROMOTION",
      "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_AUTOMATICALLY_ASSIGNED_NATIVE_FRFS","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"}
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
