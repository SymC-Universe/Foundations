#!/usr/bin/env python3
import hashlib, json, subprocess, sys, tempfile, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd

try:
    import pyfbs
except Exception:
    subprocess.run([sys.executable,"-m","pip","install","--disable-pip-version-check","pyFBS==1.0.6"],check=True)
    import pyfbs

BASE="https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/"
FILES={
 "Y_B.p":"2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12",
 "Y_AB.p":"197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7"
}
META="decoupling_example_SVT.xlsx"
OUT=Path("stability_inheritance/results/pyfbs_current_svt_preflight_v0_3")
OUT.mkdir(parents=True,exist_ok=True)
res={
 "status":"P0Q_PRETARGET_COMPATIBILITY",
 "protocol":"PYFBS_CURRENT_METADATA_SVT_PREFLIGHT_v0.3",
 "package_requested":"pyFBS==1.0.6",
 "target_Y_A_downloaded":False
}

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    hashes={}
    for name,exp in FILES.items():
        p=td/name
        urllib.request.urlretrieve(BASE+name,p)
        h=hashlib.sha256(p.read_bytes()).hexdigest(); hashes[name]=h
        if h!=exp:
            res.update({"disposition":"INVALID_TEST","reason":f"hash mismatch {name}","hashes":hashes})
            (OUT/"result.json").write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2)); raise SystemExit(0)
    mp=td/META
    urllib.request.urlretrieve(BASE+META,mp)
    hashes[META]=hashlib.sha256(mp.read_bytes()).hexdigest()
    res["hashes"]=hashes

    def load(name):
        obj=np.load(td/name,allow_pickle=True)
        f=np.asarray(obj[0],float).reshape(-1)
        a=np.asarray(obj[1])
        if a.ndim!=3 or a.shape[2]!=f.size: raise RuntimeError(f"shape {name} {a.shape}")
        return f,np.transpose(a,(2,0,1)).astype(complex)

    fB,YB=load("Y_B.p"); fAB,YAB=load("Y_AB.p")
    if not np.allclose(fB,fAB,rtol=0,atol=1e-12):
        res.update({"disposition":"INVALID_TEST","reason":"frequency mismatch"})
    else:
        try:
            chB=pd.read_excel(mp,sheet_name="Channels_B")
            imB=pd.read_excel(mp,sheet_name="Impacts_B")
            chAB=pd.read_excel(mp,sheet_name="Channels_AB")
            imAB=pd.read_excel(mp,sheet_name="Impacts_AB")
            res["metadata_counts"]={
              "Channels_B":len(chB),"Impacts_B":len(imB),
              "Channels_AB":len(chAB),"Impacts_AB":len(imAB)
            }
            SVT=getattr(getattr(pyfbs,"interface",pyfbs),"SVT",None)
            if SVT is None: SVT=getattr(pyfbs,"SVT")
            svt=SVT(chB,imB,fB,YB,[1,10],6)
            apply=getattr(svt,"apply_svt",None) or getattr(svt,"apply_SVT",None)
            if apply is None: raise RuntimeError("SVT apply method absent")
            _,_,Bsv=apply(chB,imB,fB,YB)
            _,_,ABsv=apply(chAB,imAB,fAB,YAB)
            Bsv=np.asarray(Bsv); ABsv=np.asarray(ABsv)
            res["transformed_shapes"]={"B":list(Bsv.shape),"AB":list(ABsv.shape)}
            res["finite"]={"B":bool(np.isfinite(Bsv).all()),"AB":bool(np.isfinite(ABsv).all())}
            ok=(Bsv.shape==(fB.size,6,6) and ABsv.shape==(fB.size,12,12) and res["finite"]["B"] and res["finite"]["AB"])
            res["disposition"]="CURRENT_SVT_ROUTE_EXECUTABLE" if ok else "CURRENT_SVT_ROUTE_NOT_EXECUTABLE"
        except Exception as e:
            res.update({"disposition":"CURRENT_SVT_ROUTE_NOT_EXECUTABLE","exception_type":type(e).__name__,"exception":str(e)})
(OUT/"result.json").write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
