#!/usr/bin/env python3
import hashlib, json, os, subprocess, sys, tempfile, textwrap, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"stability_inheritance"/"results"/"pyfbs_svt_compatibility_v0_2"
RAW=OUT/"raw"
OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)
BASE="https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/"
EXPECTED={
 "Y_B.p":"2e4a83f4ce1b87e773c5872764c4e4bd11f71b256a11964ac7574a81feeeed12",
 "Y_AB.p":"197deff3bc1f546bc1653ecb877d34dece01dfc1d360217dc903f4d1a694d4d7",
 "decoupling_example.xlsx":"20d246430c163c5abd935d71f36a65b470fd3b0fff6243a81d1e2cc0099a04a9"
}
VERSIONS=["1.0.0","1.0.4","1.0.5","1.0.6"]
hashes={}
for name,exp in EXPECTED.items():
    p=RAW/name
    urllib.request.urlretrieve(BASE+name,p)
    h=hashlib.sha256(p.read_bytes()).hexdigest(); hashes[name]=h
    if h!=exp:
        raise RuntimeError(f"hash mismatch {name}: expected {exp}, got {h}")

worker=textwrap.dedent(r'''
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd
import pyfbs
raw=Path(sys.argv[1])
def load(name):
    obj=np.load(raw/name,allow_pickle=True)
    f=np.asarray(obj[0],float).reshape(-1)
    a=np.asarray(obj[1])
    if a.ndim!=3 or a.shape[2]!=f.size:
        raise RuntimeError(f"unexpected {name} shape {a.shape}")
    return f,np.transpose(a,(2,0,1)).astype(complex)
fB,YB=load("Y_B.p"); fAB,YAB=load("Y_AB.p")
if not np.allclose(fB,fAB,rtol=0,atol=1e-12):
    raise RuntimeError("frequency mismatch")
xlsx=raw/"decoupling_example.xlsx"
chnB=pd.read_excel(xlsx,sheet_name="Channels_B")
impB=pd.read_excel(xlsx,sheet_name="Impacts_B")
chnAB=pd.read_excel(xlsx,sheet_name="Channels_AB")
impAB=pd.read_excel(xlsx,sheet_name="Impacts_AB")
out={"version":getattr(pyfbs,"__version__","unknown"),"raw_shapes":{"B":list(YB.shape),"AB":list(YAB.shape)}}
try:
    SVT=getattr(getattr(pyfbs,"interface",pyfbs),"SVT",None)
    if SVT is None: SVT=getattr(pyfbs,"SVT")
    svt=SVT(chnB,impB,freq=fB,frf=YB,grouping_no=[1,10],no_svs=6)
    out["constructor"]="PASS"
    apply=getattr(svt,"apply_svt",None) or getattr(svt,"apply_SVT",None)
    if apply is None: raise RuntimeError("no SVT apply method")
    retB=apply(chnB,impB,freq=fB,frf=YB)
    FB=np.asarray(retB[2])
    out["apply_B"]="PASS"; out["B_shape"]=list(FB.shape); out["B_finite"]=bool(np.isfinite(FB).all())
    retAB=apply(chnAB,impAB,freq=fAB,frf=YAB)
    FAB=np.asarray(retAB[2])
    out["apply_AB"]="PASS"; out["AB_shape"]=list(FAB.shape); out["AB_finite"]=bool(np.isfinite(FAB).all())
    ok=(FB.shape==(fB.size,6,6) and FAB.shape==(fB.size,12,12) and out["B_finite"] and out["AB_finite"])
    out["disposition"]="SVT_ROUTE_EXECUTABLE" if ok else "SVT_ROUTE_NOT_EXECUTABLE"
except Exception as e:
    out.setdefault("constructor","FAIL" if "svt" not in locals() else out.get("constructor","PASS"))
    out["disposition"]="SVT_ROUTE_NOT_EXECUTABLE"
    out["exception_type"]=type(e).__name__
    out["exception"]=str(e)
print(json.dumps(out))
''')

results=[]
for v in VERSIONS:
    with tempfile.TemporaryDirectory() as td:
        venv=Path(td)/"venv"
        subprocess.run([sys.executable,"-m","venv",str(venv)],check=True)
        py=venv/"bin"/"python"
        pip=venv/"bin"/"pip"
        install=subprocess.run([str(pip),"install","--disable-pip-version-check",f"pyFBS=={v}","openpyxl==3.1.5"],text=True,capture_output=True)
        if install.returncode!=0:
            results.append({"requested_version":v,"disposition":"SVT_ROUTE_NOT_EXECUTABLE","install_failure":install.stderr[-3000:]})
            continue
        p=Path(td)/"worker.py"; p.write_text(worker)
        run=subprocess.run([str(py),str(p),str(RAW)],text=True,capture_output=True)
        if run.returncode!=0:
            results.append({"requested_version":v,"disposition":"SVT_ROUTE_NOT_EXECUTABLE","worker_failure":run.stderr[-3000:]})
            continue
        try:
            obj=json.loads(run.stdout.strip().splitlines()[-1])
        except Exception:
            obj={"requested_version":v,"disposition":"SVT_ROUTE_NOT_EXECUTABLE","parse_failure":run.stdout[-3000:]}
        obj["requested_version"]=v
        results.append(obj)

exe=[r["requested_version"] for r in results if r.get("disposition")=="SVT_ROUTE_EXECUTABLE"]
overall="COMPATIBLE_RELEASE_FOUND" if exe else "RELEASE_COMPATIBILITY_NOT_FOUND"
out={"status":"PUBLIC_EXTERNAL_P0Q_PREFLIGHT","protocol":"PYFBS_SVT_API_COMPATIBILITY_PREFLIGHT_v0.2","hashes":hashes,"versions":results,"executable_versions":exe,"disposition":overall}
(OUT/"result.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
for p in RAW.iterdir(): p.unlink()
RAW.rmdir()
