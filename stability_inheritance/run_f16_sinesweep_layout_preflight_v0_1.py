#!/usr/bin/env python3
import hashlib, json, urllib.request, zipfile, tempfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
EXPECTED_SHA256="2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa"
OUT=Path("stability_inheritance/results/f16_gvt_sinesweep_layout")
OUT.mkdir(parents=True,exist_ok=True)

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    zpath=td/"F16GVT_Files.zip"
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, zpath.open("wb") as f:
        while True:
            chunk=resp.read(1024*1024)
            if not chunk: break
            f.write(chunk)
    b=zpath.read_bytes()
    if len(b)!=EXPECTED_SIZE:
        raise RuntimeError(f"source size changed {len(b)}")
    sha=hashlib.sha256(b).hexdigest()
    if sha!=EXPECTED_SHA256:
        raise RuntimeError(f"source hash changed {sha}")
    with zipfile.ZipFile(zpath,"r") as z:
        z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"
    files=sorted([p for p in root.rglob("*.mat") if "sinesw" in p.name.replace(" ","").lower()])
    records=[]
    levels=set()
    for p in files:
        d=loadmat(p,variable_names=["Force","Voltage","Acceleration","Fs","Time","time","Frequency","frequency"])
        arrays={}
        for key,val in d.items():
            if key.startswith("__"): continue
            a=np.asarray(val)
            arrays[key]={"shape":list(a.shape),"dtype":str(a.dtype),"size":int(a.size)}
            if key=="Fs" and a.size==1:
                arrays[key]["scalar"]=float(a.squeeze())
        low=p.name.replace(" ","").lower()
        level=None
        for lev in range(1,8):
            if f"level{lev}" in low or f"level0{lev}" in low:
                level=lev; levels.add(lev); break
        records.append({
          "file":p.name,
          "level_from_name":level,
          "bytes":p.stat().st_size,
          "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
          "arrays":arrays
        })
    all_levels=(levels==set(range(1,8)))
    unique=all(sum(1 for r in records if r["level_from_name"]==lev)==1 for lev in range(1,8))
    core=True
    for r in records:
        a=r["arrays"]
        core=core and ("Force" in a and "Acceleration" in a and "Fs" in a)
    if all_levels and unique and core:
        disp="SINESWEEP_LAYOUT_QUALIFIED"
    elif len(records)>=7 and all_levels:
        disp="SINESWEEP_LAYOUT_NEEDS_MAPPING"
    else:
        disp="SINESWEEP_LAYOUT_INVALID"
    out={
      "status":"P0Q_LAYOUT_PREFLIGHT_ONLY",
      "source_sha256":sha,
      "file_count":len(records),
      "levels_from_filenames":sorted(levels),
      "records":records,
      "disposition":disp,
      "signal_values_scored":False
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
