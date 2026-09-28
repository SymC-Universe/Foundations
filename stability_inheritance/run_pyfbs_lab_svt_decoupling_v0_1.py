#!/usr/bin/env python3
import hashlib, json, math, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import pyfbs

BASE="https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/"
EXPECTED={
 "Y_A.p":"3b8ece8b2b80b63e209427518cd6521c8028042ff1d79ff04e5de5f657a13db4",
 "Y_B.p":"2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12",
 "Y_AB.p":"197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7",
 "decoupling_example.xlsx":"20d246430c163c5abd935d71f36a65b470fd3b0fff6243a81d1e2cc0099a04a9"
}
OUT=Path("stability_inheritance/results/pyfbs_lab_svt_decoupling")
RAW=OUT/"raw"
OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)
hashes={}
for name,exp in EXPECTED.items():
    p=RAW/name; urllib.request.urlretrieve(BASE+name,p)
    h=hashlib.sha256(p.read_bytes()).hexdigest(); hashes[name]=h
    if h!=exp: raise RuntimeError(f"hash mismatch {name}: {h}")

def load(name):
    obj=np.load(RAW/name,allow_pickle=True)
    f=np.asarray(obj[0],float).reshape(-1)
    raw=np.asarray(obj[1])
    if raw.ndim!=3 or raw.shape[2]!=f.size:
        raise RuntimeError(f"unexpected {name} shape {raw.shape}, freq={f.shape}")
    return f,np.transpose(raw,(2,0,1)).astype(complex)

fA,YA=load("Y_A.p"); fB,YB=load("Y_B.p"); fAB,YAB=load("Y_AB.p")
if not (np.allclose(fA,fB,rtol=0,atol=1e-12) and np.allclose(fA,fAB,rtol=0,atol=1e-12)):
    raise RuntimeError("INVALID_DATA_ALIGNMENT")
freq=fA
if YA.shape[1:]!=(6,6) or YB.shape[1:]!=(21,21) or YAB.shape[1:]!=(27,27):
    raise RuntimeError(f"identity mismatch A={YA.shape} B={YB.shape} AB={YAB.shape}")

xlsx=RAW/"decoupling_example.xlsx"
chnB=pd.read_excel(xlsx,sheet_name="Channels_B")
impB=pd.read_excel(xlsx,sheet_name="Impacts_B")
chnAB=pd.read_excel(xlsx,sheet_name="Channels_AB")
impAB=pd.read_excel(xlsx,sheet_name="Impacts_AB")
if (len(chnB),len(impB),len(chnAB),len(impAB))!=(21,21,27,27):
    raise RuntimeError("metadata count mismatch")

SVT=getattr(getattr(pyfbs,"interface",pyfbs),"SVT",None)
if SVT is None: SVT=getattr(pyfbs,"SVT")
k=6
svt=SVT(chnB,impB,freq,YB,[1,10],k)
apply=getattr(svt,"apply_svt",getattr(svt,"apply_SVT",None))
if apply is None: raise RuntimeError("SVT apply method unavailable")
retB=apply(chnB,impB,freq,YB)
retAB=apply(chnAB,impAB,freq,YAB)
FB=np.asarray(retB[2],complex)
FAB=np.asarray(retAB[2],complex)
if FB.shape[1:]!=(6,6) or FAB.shape[1:]!=(12,12):
    raise RuntimeError(f"unexpected transformed dimensions B={FB.shape} AB={FAB.shape}")

def decouple(perm):
    n=freq.size
    blk=np.zeros((n,18,18),complex)
    blk[:,:12,:12]=FAB
    # Apply no permutation to B data; wrong correspondence is encoded in B map.
    blk[:,12:,12:]=-FB
    Bu=np.zeros((6,18),float)
    for r in range(6):
        Bu[r,r]=1.0
        Bu[r,12+perm[r]]=-1.0
    Bf=Bu.copy()
    out=np.empty_like(blk)
    cond=np.empty(n,float)
    nonfinite=0
    for q in range(n):
        Yint=Bu@blk[q]@Bf.T
        cond[q]=np.linalg.cond(Yint)
        out[q]=blk[q]-blk[q]@Bf.T@np.linalg.pinv(Yint)@Bu@blk[q]
        nonfinite += int(out[q].size-np.isfinite(out[q]).sum())
    Ahat=out[:,6:12,6:12]
    return Ahat,cond,nonfinite

DEC,condD,nfD=decouple([0,1,2,3,4,5])
SHF,condS,nfS=decouple([1,0,2,3,4,5])
BASE=FAB[:,6:12,6:12]

mask=freq>0
R=YA[mask]; D=DEC[mask]; S=SHF[mask]; B=BASE[mask]; F=freq[mask]
def ge(X,R):
    den=np.sum(np.abs(R)**2)
    return float(np.sqrt(np.sum(np.abs(X-R)**2)/den)) if den>0 else math.nan
def pf(X,R):
    den=np.sum(np.abs(R)**2,axis=(1,2))
    num=np.sum(np.abs(X-R)**2,axis=(1,2))
    return np.sqrt(num/np.maximum(den,np.finfo(float).tiny))
eD,eB,eS=ge(D,R),ge(B,R),ge(S,R)
pD,pB,pS=pf(D,R),pf(B,R),pf(S,R)
if nfD or not np.isfinite(eD): disp="INVALID_TEST"
elif eD < eB: disp="NATIVE_FRAMEWORK_EQUIVALENT"
else: disp="NATIVE_MODEL_NOT_QUALIFIED_FOR_THIS_IMPLEMENTATION"
mapspec="MAPPING_SPECIFICITY_SUPPORTED" if np.isfinite(eS) and eD<eS else "MAPPING_SPECIFICITY_NOT_SHOWN"

out={
 "status":"PUBLIC_EXTERNAL_P0Q",
 "protocol":"PYFBS_LAB_SVT_DECOUPLING_PROTOCOL_v0.1",
 "hashes":hashes,
 "versions":{"pyfbs":getattr(pyfbs,"__version__","unknown"),"numpy":np.__version__,"pandas":pd.__version__},
 "shapes":{"A":list(YA.shape),"B":list(YB.shape),"AB":list(YAB.shape),"B_SVT":list(FB.shape),"AB_SVT":list(FAB.shape),"A_recovered":list(DEC.shape)},
 "frequency":{"n_total":int(freq.size),"n_positive":int(mask.sum()),"min_positive_hz":float(F.min()),"max_hz":float(F.max())},
 "primary":{"E_DEC":eD,"E_BASE":eB},
 "mapping_control":{"E_SHUFFLED":eS,"disposition":mapspec},
 "secondary":{
  "fraction_bins_DEC_better_BASE":float(np.mean(pD<pB)),
  "fraction_bins_DEC_better_SHUFFLED":float(np.mean(pD<pS)),
  "DEC_median":float(np.median(pD)),"DEC_p90":float(np.quantile(pD,.9)),
  "BASE_median":float(np.median(pB)),"BASE_p90":float(np.quantile(pB,.9)),
  "SHUFFLED_median":float(np.median(pS)),"SHUFFLED_p90":float(np.quantile(pS,.9))
 },
 "conditioning":{
  "correct_median":float(np.median(condD[mask])),"correct_p90":float(np.quantile(condD[mask],.9)),
  "correct_max":float(np.max(condD[mask])),"nonfinite_correct":int(nfD),"nonfinite_shuffled":int(nfS)
 },
 "disposition":disp,
 "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED_NATIVE_FRF_USED","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"},
 "claim_ceiling":"measured native decoupling / independent-target workflow qualification only; not inheritance novelty"
}
(OUT/"result.json").write_text(json.dumps(out,indent=2))
with (OUT/"summary.md").open("w") as f:
    f.write("# pyFBS measured SVT decoupling frozen result\n\n")
    f.write(f"Disposition: **{disp}**\n\n")
    f.write(f"Mapping diagnostic: **{mapspec}**\n\n")
    f.write("| Route | Global normalized complex error | Median per-frequency | P90 per-frequency |\n|---|---:|---:|---:|\n")
    f.write(f"| Native SVT+LM-FBS decoupling | {eD:.10g} | {np.median(pD):.10g} | {np.quantile(pD,.9):.10g} |\n")
    f.write(f"| No-decoupling baseline | {eB:.10g} | {np.median(pB):.10g} | {np.quantile(pB,.9):.10g} |\n")
    f.write(f"| Wrong reduced correspondence | {eS:.10g} | {np.median(pS):.10g} | {np.quantile(pS,.9):.10g} |\n")
print(json.dumps(out,indent=2))
for p in RAW.iterdir(): p.unlink()
RAW.rmdir()
