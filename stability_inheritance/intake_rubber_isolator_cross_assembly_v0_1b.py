#!/usr/bin/env python3
import hashlib, json, urllib.parse, urllib.request
from pathlib import Path

SLUG="38cp7wdjz7"
BASE="https://data.mendeley.com/public-files/datasets"
OUT=Path("stability_inheritance/results/rubber_isolator_cross_assembly_intake")
OUT.mkdir(parents=True,exist_ok=True)

FILES=["experimental.h5","numerical.h5","README.md"]

def public_url(name):
    return f"{BASE}/{SLUG}/files/{urllib.parse.quote(name)}/download"

res={
  "status":"PUBLIC_EXTERNAL_P0Q_METADATA_INTAKE",
  "dataset_slug":SLUG,
  "numeric_h5_downloaded":False,
  "route":"official_public_filename_download"
}

head_results={}
for name in ["experimental.h5","numerical.h5"]:
    url=public_url(name)
    try:
        req=urllib.request.Request(url,method="HEAD",headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
        with urllib.request.urlopen(req,timeout=60) as r:
            head_results[name]={
              "requested_url":url,
              "final_url":r.geturl(),
              "status":getattr(r,"status",None),
              "content_type":r.headers.get("Content-Type"),
              "content_length":r.headers.get("Content-Length"),
              "etag":r.headers.get("ETag"),
              "last_modified":r.headers.get("Last-Modified")
            }
    except Exception as e:
        head_results[name]={
          "requested_url":url,
          "error_type":type(e).__name__,
          "error":str(e)
        }
res["head"]=head_results

readme_url=public_url("README.md")
try:
    req=urllib.request.Request(readme_url,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read()
        res["readme"]={
          "requested_url":readme_url,
          "final_url":r.geturl(),
          "status":getattr(r,"status",None),
          "content_type":r.headers.get("Content-Type"),
          "bytes":len(b),
          "sha256":hashlib.sha256(b).hexdigest(),
          "text":b.decode("utf-8",errors="replace")
        }
except Exception as e:
    res["readme_error"]={"type":type(e).__name__,"error":str(e)}

readme_ok="readme" in res and (res["readme"].get("status") in (200,206,None))
heads_ok=True
for name in ["experimental.h5","numerical.h5"]:
    x=head_results[name]
    if x.get("status") not in (200,204,206,302,303,307,308):
        heads_ok=False

if readme_ok and heads_ok:
    res["disposition"]="INTAKE_METADATA_PASS"
elif readme_ok:
    res["disposition"]="INTAKE_PUBLIC_ROUTE_PARTIAL"
else:
    res["disposition"]="INTAKE_PUBLIC_ROUTE_BLOCKED"

(OUT/"result.json").write_text(json.dumps(res,indent=2))
print(json.dumps({k:v for k,v in res.items() if k!="readme" or not isinstance(v,dict) or "text" not in v},indent=2))
