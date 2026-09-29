#!/usr/bin/env python3
import hashlib, json, re, urllib.request
from pathlib import Path
from html import unescape

OUT=Path("stability_inheritance/results/rivet_mendeley_source_discovery")
OUT.mkdir(parents=True,exist_ok=True)

DATASETS={
  "small":{
    "doi":"10.17632/sgmxhdc599.1",
    "slug":"sgmxhdc599",
    "version":"1",
    "page":"https://data.mendeley.com/datasets/sgmxhdc599/1"
  },
  "large":{
    "doi":"10.17632/dy66vm8t95.1",
    "slug":"dy66vm8t95",
    "version":"1",
    "page":"https://data.mendeley.com/datasets/dy66vm8t95/1"
  }
}

API_TEMPLATES=[
  "https://api.mendeley.com/datasets/{slug}",
  "https://api.mendeley.com/datasets/{slug}/versions/{version}",
  "https://data.mendeley.com/api/datasets/{slug}",
  "https://data.mendeley.com/api/datasets/{slug}/{version}",
  "https://data.mendeley.com/api/datasets/{slug}/versions/{version}"
]

URL_RE=re.compile(r"https?://[^\\s\\\"'<>]+")
FILE_HINT_RE=re.compile(r"[^\\s\\\"'<>]*(?:data\\.h5|Structure_images\\.jpg|public-files|file_download|download)[^\\s\\\"'<>]*",re.I)

def fetch(url,method="GET"):
    req=urllib.request.Request(url,method=method,headers={"User-Agent":"SymC-Stability-Inheritance-Metadata-Discovery/1.0","Accept":"*/*"})
    try:
        with urllib.request.urlopen(req,timeout=45) as r:
            body=b"" if method=="HEAD" else r.read()
            return {
              "ok":True,
              "status":getattr(r,"status",None),
              "final_url":r.geturl(),
              "content_type":r.headers.get("Content-Type"),
              "content_length_header":r.headers.get("Content-Length"),
              "body_len":len(body),
              "sha256":hashlib.sha256(body).hexdigest() if body else None,
              "body":body
            }
    except Exception as e:
        return {"ok":False,"exception_type":type(e).__name__,"exception":str(e)}

result={"status":"PUBLIC_METADATA_DISCOVERY_ONLY","datasets":{}}

for key,d in DATASETS.items():
    rec={"doi":d["doi"],"page":d["page"],"requests":[],"candidates":[],"head_checks":[]}
    urls=[d["page"]]+[x.format(**d) for x in API_TEMPLATES]
    seen=set()
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        rr=fetch(url)
        body=rr.pop("body",b"")
        rr["requested_url"]=url
        rec["requests"].append(rr)
        if not body:
            continue
        txt=unescape(body.decode("utf-8","replace"))
        cands=set()
        for m in URL_RE.finditer(txt):
            u=m.group(0).replace("\\/", "/")
            if any(h in u.lower() for h in ["data.h5","structure_images","public-files","file_download","download"]):
                cands.add(u.rstrip(".,;)]}"))
        for m in FILE_HINT_RE.finditer(txt):
            x=m.group(0).replace("\\/", "/")
            if x.startswith("http"):
                cands.add(x.rstrip(".,;)]}"))
        for cand in sorted(cands):
            if cand not in rec["candidates"]:
                rec["candidates"].append(cand)
    for cand in rec["candidates"][:30]:
        h=fetch(cand,method="HEAD")
        h["url"]=cand
        rec["head_checks"].append(h)
    page_ok=any(x.get("ok") for x in rec["requests"] if x.get("requested_url")==d["page"])
    file_route=False
    for cand in rec["candidates"]:
        lc=cand.lower()
        if "data.h5" in lc or "public-files" in lc or "file_download" in lc:
            file_route=True
    if file_route:
        rec["disposition"]="OFFICIAL_FILE_ROUTE_DISCOVERED"
    elif page_ok:
        rec["disposition"]="METADATA_ROUTE_ONLY"
    else:
        rec["disposition"]="SOURCE_DISCOVERY_BLOCKED"
    result["datasets"][key]=rec

disps=[x["disposition"] for x in result["datasets"].values()]
if "OFFICIAL_FILE_ROUTE_DISCOVERED" in disps:
    result["disposition"]="OFFICIAL_FILE_ROUTE_DISCOVERED"
elif "METADATA_ROUTE_ONLY" in disps:
    result["disposition"]="METADATA_ROUTE_ONLY"
else:
    result["disposition"]="SOURCE_DISCOVERY_BLOCKED"

(OUT/"result.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
