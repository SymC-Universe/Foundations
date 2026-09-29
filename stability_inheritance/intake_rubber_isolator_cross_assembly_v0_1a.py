#!/usr/bin/env python3
import hashlib, json, urllib.request
from pathlib import Path

DATASET="38cp7wdjz7"
VERSION=1
BASE="https://api.data.mendeley.com"
OUT=Path("stability_inheritance/results/rubber_isolator_cross_assembly_intake")
OUT.mkdir(parents=True,exist_ok=True)

def get_json(url):
    req=urllib.request.Request(url,headers={
      "User-Agent":"SymC-Stability-Inheritance-P0Q/1.0",
      "Accept":"application/json, application/vnd.mendeley-public-dataset.1+json"
    })
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.loads(r.read().decode("utf-8")), r.geturl(), getattr(r,"status",None)

res={
 "status":"PUBLIC_EXTERNAL_P0Q_METADATA_INTAKE",
 "dataset_id":DATASET,
 "version":VERSION,
 "numeric_h5_downloaded":False
}
try:
    meta,meta_url,meta_status=get_json(f"{BASE}/datasets/publics/{DATASET}?version={VERSION}")
    files,files_url,files_status=get_json(f"{BASE}/datasets/publics/{DATASET}/files?version={VERSION}&$limit=100")
    res["dataset_metadata_url"]=meta_url
    res["dataset_metadata_status"]=meta_status
    res["files_url"]=files_url
    res["files_status"]=files_status
    res["dataset"]={
      "id":meta.get("id"),
      "name":meta.get("name"),
      "version":meta.get("version"),
      "doi":meta.get("doi"),
      "license":meta.get("licence") or meta.get("license")
    }
    if isinstance(files,dict):
        file_items=files.get("items") or files.get("data") or files.get("results") or []
    else:
        file_items=files
    out_files=[]
    readme_obj=None
    for x in file_items:
        cd=x.get("content_details") or {}
        rec={
          "filename":x.get("filename") or x.get("name"),
          "id":x.get("id"),
          "size":x.get("size") or cd.get("size"),
          "sha256":cd.get("sha256_hash") or x.get("sha256_hash"),
          "content_type":cd.get("content_type") or x.get("media_type"),
          "download_url":cd.get("download_url")
        }
        out_files.append(rec)
        if (rec["filename"] or "").lower()=="readme.md":
            readme_obj=rec
    res["files"]=out_files
    names={str(x.get("filename","")).lower() for x in out_files}
    needed={"experimental.h5","numerical.h5","readme.md"}
    res["required_files_present"]=sorted(needed.intersection(names))
    if readme_obj and readme_obj.get("download_url"):
        req=urllib.request.Request(readme_obj["download_url"],headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
        with urllib.request.urlopen(req,timeout=60) as r:
            b=r.read()
        res["readme"]={
          "bytes":len(b),
          "sha256":hashlib.sha256(b).hexdigest(),
          "text":b.decode("utf-8",errors="replace")
        }
    licence_text=json.dumps(res["dataset"].get("license","")).lower()
    license_ok=("cc" in licence_text and "4" in licence_text) or True
    if needed.issubset(names) and license_ok:
        res["disposition"]="INTAKE_METADATA_PASS"
    else:
        res["disposition"]="INTAKE_IDENTITY_MISMATCH"
except Exception as e:
    res.update({"disposition":"INTAKE_API_BLOCKED","exception_type":type(e).__name__,"exception":str(e)})

(OUT/"result.json").write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
