#!/usr/bin/env python3
import hashlib, json, urllib.request, zipfile, tempfile
from pathlib import Path
import numpy as np
from scipy.io import loadmat

URL="https://data.4tu.nl/file/b6dc643b-ecc6-437c-8a8a-1681650ec3fe/5414dfdc-6e8d-4208-be6e-fa553de9866f"
EXPECTED_SIZE=148455295
EXPECTED_SHA="2278429b1f15f15448e6f101d395a5587d58ac23d32052fd42f8b33a894c0afa"
OUT=Path("stability_inheritance/results/f16_gvt_specialodd_layout")
OUT.mkdir(parents=True,exist_ok=True)

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    zpath=td/"F16GVT_Files.zip"
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
    with urllib.request.urlopen(req,timeout=120) as resp, zpath.open("wb") as f:
        while True:
            chunk=resp.read(1024*1024)
            if not chunk:
                break
            f.write(chunk)
    b=zpath.read_bytes()
    if len(b)!=EXPECTED_SIZE:
        raise RuntimeError(f"source size changed {len(b)}")
    sha=hashlib.sha256(b).hexdigest()
    if sha!=EXPECTED_SHA:
        raise RuntimeError(f"source hash changed {sha}")
    with zipfile.ZipFile(zpath,"r") as z:
        if z.testzip() is not None:
            raise RuntimeError("archive integrity failed")
        z.extractall(td/"unz")
    root=td/"unz"/"F16GVT_Files"/"BenchmarkData"
    files=sorted([p for p in root.rglob("*.mat") if "specialoddmsine" in p.name.replace(" ","").lower()])
    records=[]
    levels=set()
    expected_total=10*3*16384
    for p in files:
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        d=loadmat(p,variable_names=["Force","Voltage","Acceleration","Fs"])
        arrs={}
        fs_value=None
        for key in ["Force","Voltage","Acceleration","Fs"]:
            if key in d:
                a=np.asarray(d[key])
                arrs[key]={"shape":list(a.shape),"dtype":str(a.dtype),"size":int(a.size)}
                if key=="Fs" and a.size==1:
                    fs_value=float(a.squeeze())
        name=p.name.replace(" ","").lower()
        level=None
        for lev in range(1,8):
            if f"level{lev}" in name or f"level0{lev}" in name:
                level=lev
                levels.add(lev)
                break
        records.append({
          "file":p.name,
          "level_from_name":level,
          "bytes":p.stat().st_size,
          "sha256":h,
          "Fs_scalar":fs_value,
          "arrays":arrs
        })
    reconcile={}
    for rec in records:
        force=rec["arrays"].get("Force",{})
        acc=rec["arrays"].get("Acceleration",{})
        fsize=force.get("size")
        asize=acc.get("size")
        reconcile[rec["file"]]={
          "force_matches_10x3x16384": fsize==expected_total,
          "acc_matches_3_outputs_x_10x3x16384": asize==3*expected_total,
          "force_size":fsize,
          "acc_size":asize
        }
    present=len(records)>0
    exactly_three_levels=(len(levels)==3)
    direct=present and exactly_three_levels and all(
        v["force_matches_10x3x16384"] and v["acc_matches_3_outputs_x_10x3x16384"]
        for v in reconcile.values()
    )
    if direct:
        disp="SPECIALODD_LAYOUT_QUALIFIED"
    elif present and exactly_three_levels:
        disp="SPECIALODD_LAYOUT_NEEDS_MAPPING"
    else:
        disp="SPECIALODD_LAYOUT_INVALID"
    out={
      "status":"P0Q_LAYOUT_PREFLIGHT_ONLY",
      "source_sha256":sha,
      "source_size_bytes":len(b),
      "file_count":len(records),
      "levels_from_filenames":sorted(levels),
      "records":records,
      "reconciliation":reconcile,
      "disposition":disp,
      "signal_values_scored":False,
      "mechanical_revision":"v0.1a removes ephemeral prior-workflow manifest dependency only"
    }
    (OUT/"result.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
