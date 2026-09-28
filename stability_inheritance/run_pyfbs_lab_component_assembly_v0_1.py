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
 "coupling_example.xlsx":"44df97fd4f97e2bcce122afd6578113c23e2820a32f957baaeb5b4c8a4162ad4"
}
OUT=Path("stability_inheritance/results/pyfbs_lab_component_assembly")
RAW=OUT/"raw"
OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)

hashes={}
for name,exp in EXPECTED.items():
    p=RAW/name
    urllib.request.urlretrieve(BASE+name,p)
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    hashes[name]=h
    if h != exp:
        raise RuntimeError(f"hash mismatch for {name}: expected {exp}, got {h}")

def load_frf(name):
    obj=np.load(RAW/name,allow_pickle=True)
    freq=np.asarray(obj[0],dtype=float).reshape(-1)
    arr=np.asarray(obj[1])
    if arr.ndim != 3:
        raise RuntimeError(f"{name} unexpected FRF ndim {arr.ndim}")
    # Documented pyFBS measured-data convention stores response x input x frequency.
    if arr.shape[2] == freq.size:
        y=np.transpose(arr,(2,0,1))
    elif arr.shape[0] == freq.size:
        y=arr
    else:
        raise RuntimeError(f"{name} no dimension matches frequency length: {arr.shape}, {freq.size}")
    return freq,np.asarray(y,dtype=complex)

fA,YA0=load_frf("Y_A.p")
fB,YB0=load_frf("Y_B.p")
fR,YR=load_frf("Y_AB.p")
if not (fA.shape==fB.shape==fR.shape and np.allclose(fA,fB,rtol=0,atol=1e-12) and np.allclose(fA,fR,rtol=0,atol=1e-12)):
    raise RuntimeError("INVALID_DATA_ALIGNMENT: frequency vectors differ")
freq=fA

xlsx=RAW/"coupling_example.xlsx"
chnA=pd.read_excel(xlsx,sheet_name="Channels_A")
impA=pd.read_excel(xlsx,sheet_name="Impacts_A")
chnB=pd.read_excel(xlsx,sheet_name="Channels_B")
impB=pd.read_excel(xlsx,sheet_name="Impacts_B")
vp=pd.read_excel(xlsx,sheet_name="VP_Channels")
vpref=pd.read_excel(xlsx,sheet_name="VP_RefChannels")

# Current pyFBS API; mechanical alias fallback preserves identical VPT operation.
VPT = getattr(getattr(pyfbs,"interface",pyfbs),"VPT",None)
if VPT is None:
    VPT=getattr(pyfbs,"VPT")
vA=VPT(chnA,impA,vp,vpref)
vB=VPT(chnB,impB,vp,vpref)
applyA=getattr(vA,"apply_vpt",getattr(vA,"apply_VPT",None))
applyB=getattr(vB,"apply_vpt",getattr(vB,"apply_VPT",None))
if applyA is None or applyB is None: raise RuntimeError("VPT apply method unavailable")
applyA(freq,YA0); applyB(freq,YB0)
YA=getattr(vA,"frf",getattr(vA,"vptData",None))
YB=getattr(vB,"frf",getattr(vB,"vptData",None))
YA=np.asarray(YA,dtype=complex); YB=np.asarray(YB,dtype=complex)

nf,nAr,nAc=YA.shape
nf2,nBr,nBc=YB.shape
if not (nf==nf2==freq.size and nAr==nAc and nBr==nBc):
    raise RuntimeError(f"INVALID_TEST transformed dimensions A={YA.shape} B={YB.shape}")
if nAr < 12 or nBr < 18:
    raise RuntimeError(f"INVALID_TEST transformed source too small A={YA.shape} B={YB.shape}")

def couple(perm):
    Yblk=np.zeros((nf,nAr+nBr,nAc+nBc),dtype=complex)
    Yblk[:,:nAr,:nAc]=YA
    Yblk[:,nAr:,nAc:]=YB
    k=6
    Bu=np.zeros((k,nAr+nBr))
    Bf=np.zeros((k,nAc+nBc))
    for r in range(k):
        Bu[r,6+r]=1.0; Bf[r,6+r]=1.0
        Bu[r,nAr+perm[r]]=-1.0; Bf[r,nAc+perm[r]]=-1.0
    pred=np.empty_like(Yblk)
    cond=np.empty(nf,float)
    nonfinite=0
    for q in range(nf):
        Yi=Bu@Yblk[q]@Bf.T
        cond[q]=np.linalg.cond(Yi)
        Pi=np.linalg.pinv(Yi)
        pred[q]=Yblk[q]-Yblk[q]@Bf.T@Pi@Bu@Yblk[q]
        nonfinite += int(np.size(pred[q])-np.isfinite(pred[q]).sum())
    ext=list(range(0,6))+list(range(nAr+6,nAr+nBr))
    return pred[:,ext,:][:,:,ext],cond,nonfinite

correct,cond_correct,nf_correct=couple([0,1,2,3,4,5])
shuffled,cond_shuffled,nf_shuffled=couple([1,0,2,4,3,5])

unc=np.zeros_like(correct)
unc[:,:6,:6]=YA[:,:6,:6]
unc[:,6:,6:]=YB[:,6:18,6:18]

if YR.shape != correct.shape:
    raise RuntimeError(f"INVALID_TEST target dimension {YR.shape} != predicted {correct.shape}")

mask=freq>0
if not np.any(mask): raise RuntimeError("no positive frequencies")
R=YR[mask]; C=correct[mask]; S=shuffled[mask]; U=unc[mask]
F=freq[mask]

def global_err(X,R):
    den=np.sum(np.abs(R)**2)
    if den<=0: return math.nan
    return float(np.sqrt(np.sum(np.abs(X-R)**2)/den))
def per_freq(X,R):
    num=np.sum(np.abs(X-R)**2,axis=(1,2))
    den=np.sum(np.abs(R)**2,axis=(1,2))
    return np.sqrt(num/np.maximum(den,np.finfo(float).tiny))

eC=global_err(C,R); eS=global_err(S,R); eU=global_err(U,R)
pC=per_freq(C,R); pS=per_freq(S,R); pU=per_freq(U,R)

valid=np.isfinite([eC,eS,eU]).all() and nf_correct==0 and nf_shuffled==0
if not valid:
    disp="INVALID_TEST"
elif eC < eU and eC < eS:
    disp="NATIVE_FRAMEWORK_EQUIVALENT"
else:
    disp="NATIVE_MODEL_NOT_QUALIFIED_FOR_THIS_IMPLEMENTATION"

out={
 "status":"PUBLIC_EXTERNAL_P0Q",
 "protocol":"PYFBS_LAB_COMPONENT_ASSEMBLY_PROTOCOL_v0.1",
 "hashes":hashes,
 "versions":{"pyfbs":getattr(pyfbs,"__version__","unknown"),"numpy":np.__version__,"pandas":pd.__version__},
 "shapes":{"raw_A":list(YA0.shape),"raw_B":list(YB0.shape),"raw_AB":list(YR.shape),"vpt_A":list(YA.shape),"vpt_B":list(YB.shape),"predicted_AB":list(correct.shape)},
 "frequency":{"n_total":int(freq.size),"n_positive":int(mask.sum()),"min_positive_hz":float(F.min()),"max_hz":float(F.max())},
 "primary":{"E_FBS":eC,"E_UNCOUPLED":eU,"E_SHUFFLED":eS},
 "secondary":{
   "fraction_bins_FBS_better_than_uncoupled":float(np.mean(pC<pU)),
   "fraction_bins_FBS_better_than_shuffled":float(np.mean(pC<pS)),
   "FBS_median":float(np.median(pC)),"FBS_p90":float(np.quantile(pC,.9)),
   "UNC_median":float(np.median(pU)),"UNC_p90":float(np.quantile(pU,.9)),
   "SHUFFLED_median":float(np.median(pS)),"SHUFFLED_p90":float(np.quantile(pS,.9))
 },
 "conditioning":{
   "correct_interface_cond_median":float(np.median(cond_correct[mask])),
   "correct_interface_cond_p90":float(np.quantile(cond_correct[mask],.9)),
   "correct_interface_cond_max":float(np.max(cond_correct[mask])),
   "shuffled_interface_cond_median":float(np.median(cond_shuffled[mask])),
   "nonfinite_correct":int(nf_correct),"nonfinite_shuffled":int(nf_shuffled)
 },
 "disposition":disp,
 "notation":{"chi":"NOT_ADMITTED","Chi":"NOT_FORCED_NATIVE_FRF_USED","Chi_arc":"NOT_AUTOMATICALLY_ASSIGNED"},
 "claim_ceiling":"source/correspondence/transform/independent-target workflow qualification only; native FBS owns component-to-assembly physics"
}
(OUT/"result.json").write_text(json.dumps(out,indent=2))
with (OUT/"summary.md").open("w") as f:
    f.write("# pyFBS measured component-to-assembly frozen result\n\n")
    f.write(f"Disposition: **{disp}**\n\n")
    f.write("| Route | Global normalized complex error | Median per-frequency error | P90 per-frequency error |\n|---|---:|---:|---:|\n")
    f.write(f"| Correct LM-FBS | {eC:.10g} | {np.median(pC):.10g} | {np.quantile(pC,.9):.10g} |\n")
    f.write(f"| Uncoupled baseline | {eU:.10g} | {np.median(pU):.10g} | {np.quantile(pU,.9):.10g} |\n")
    f.write(f"| Wrong correspondence | {eS:.10g} | {np.median(pS):.10g} | {np.quantile(pS,.9):.10g} |\n")
print(json.dumps(out,indent=2))
# Do not retain raw files as artifacts.
for p in RAW.iterdir(): p.unlink()
RAW.rmdir()
