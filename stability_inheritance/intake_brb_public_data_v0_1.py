#!/usr/bin/env python3
import hashlib, io, json, re, urllib.request, zipfile
from pathlib import Path
import numpy as np

COMMIT="2d42d3a618206da58642674d3287ae34dfc7d5e5"
BASE=f"https://raw.githubusercontent.com/mattiacenedese/BRBtesting/{COMMIT}/"
FILES={
 "ForcedFrequencyResponses.mat":{"size":12527,"blob":"466a68a7655f344c753625a1f5a3b02ef365bb40"},
 "HammerImpact.mat":{"size":979254,"blob":"aba81f3d9b2a62a9a43782da51585e0780ad959d"},
 "ShakerRingdown.mat":{"size":56919612,"blob":"739048b2b1c71839f773ff1aecf4880fda5d62ed"},
 "showData.mlx":{"size":1756787,"blob":"2cc7f972823328d6ace9b3ec957147a221ae4b09"}
}
OUT=Path("stability_inheritance/results/brb_public_intake")
RAW=OUT/"raw"
OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)

def git_blob_sha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

res={"status":"PUBLIC_EXTERNAL_P0Q_METADATA_INTAKE","source_commit":COMMIT,"numeric_values_scored":False,"files":{}}
identity_ok=True
for name,exp in FILES.items():
    p=RAW/name
    req=urllib.request.Request(BASE+name,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
    with urllib.request.urlopen(req,timeout=120) as r:
        b=r.read()
    p.write_bytes(b)
    rec={
      "bytes":len(b),
      "expected_bytes":exp["size"],
      "git_blob_sha":git_blob_sha(b),
      "expected_git_blob_sha":exp["blob"],
      "sha256":hashlib.sha256(b).hexdigest()
    }
    rec["identity_match"]=(rec["bytes"]==exp["size"] and rec["git_blob_sha"]==exp["blob"])
    identity_ok &= rec["identity_match"]
    res["files"][name]=rec

if not identity_ok:
    res["disposition"]="BRB_SOURCE_IDENTITY_MISMATCH"
else:
    # MAT metadata without reading numerical values.
    try:
        import scipy.io
        import h5py
        for name in ["ForcedFrequencyResponses.mat","HammerImpact.mat","ShakerRingdown.mat"]:
            p=RAW/name
            header=p.read_bytes()[:128]
            rec=res["files"][name]
            rec["mat_header"]=header.decode("latin1",errors="replace").strip("\x00 ")
            try:
                vars=scipy.io.whosmat(p)
                rec["mat_format"]="classic"
                rec["variables"]=[{"name":n,"shape":list(s),"class":c} for n,s,c in vars]
            except Exception as e:
                if h5py.is_hdf5(p):
                    rec["mat_format"]="v7.3_hdf5"
                    meta=[]
                    with h5py.File(p,"r") as h:
                        def visitor(n,o):
                            item={"path":n,"type":"group" if isinstance(o,h5py.Group) else "dataset"}
                            if isinstance(o,h5py.Dataset):
                                item["shape"]=list(o.shape); item["dtype"]=str(o.dtype)
                            meta.append(item)
                        h.visititems(visitor)
                    rec["hdf5_items"]=meta
                else:
                    rec["mat_format"]="unparsed"
                    rec["metadata_error"]=f"{type(e).__name__}: {e}"

        # MLX is a zip package. Extract code/document XML text only, never embedded binary data.
        mlx=RAW/"showData.mlx"
        texts=[]
        with zipfile.ZipFile(mlx,"r") as z:
            for info in z.infolist():
                low=info.filename.lower()
                if low.endswith((".xml",".m",".txt")) and info.file_size < 5_000_000:
                    t=z.read(info).decode("utf-8",errors="replace")
                    # retain code-like snippets and variable/token names, strip long numeric runs
                    t=re.sub(r"(?<![A-Za-z_])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![A-Za-z_])","<NUM>",t)
                    texts.append({"path":info.filename,"text":t[:30000]})
        res["mlx_text_items"]=texts
        combined="\n".join(x["text"] for x in texts).lower()
        required_terms=["ringdown","dic","hammer","forced"]
        res["semantic_terms_present"]={k:(k in combined) for k in required_terms}

        ring=res["files"]["ShakerRingdown.mat"]
        has_layout=(ring.get("mat_format") in ("classic","v7.3_hdf5"))
        semantic=sum(res["semantic_terms_present"].values())>=2
        res["disposition"]="BRB_LAYOUT_QUALIFIED" if has_layout and semantic else "BRB_LAYOUT_NEEDS_MAPPING"
    except Exception as e:
        res["disposition"]="BRB_LAYOUT_INVALID"
        res["exception_type"]=type(e).__name__
        res["exception"]=str(e)

(OUT/"result.json").write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
# Do not persist third-party raw files as workflow artifacts.
for p in RAW.iterdir(): p.unlink()
RAW.rmdir()
