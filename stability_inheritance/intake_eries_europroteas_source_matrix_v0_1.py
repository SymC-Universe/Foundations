#!/usr/bin/env python3
import json, urllib.request
from pathlib import Path

OUT=Path("stability_inheritance/results/eries_europroteas_source_matrix")
OUT.mkdir(parents=True,exist_ok=True)

SOURCES={
  "RESPOND_CANONICAL":{"record_id":"15518567","role":"canonical_numeric_archive","title_terms":["real scale experimental assessment","pile group","respond"]},
  "RESPOND_POINTER":{"record_id":"21354286","role":"pointer_or_alias","title_terms":["real scale experimental assessment","pile group","respond"]},
  "POLIS":{"record_id":"15575887","role":"eps_substrate","title_terms":["polystyrene","seismic isolation","polis"]},
  "GISIS":{"record_id":"17721150","role":"rubber_isolator_micropiles","title_terms":["geotechnical innovative seismic isolation","gisis"]}
}

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-Stability-Inheritance-ERIES-Intake/1.0","Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def slim_file(f):
    links=f.get("links") or {}
    return {
      "id":f.get("id"),
      "key":f.get("key"),
      "size":f.get("size"),
      "checksum":f.get("checksum"),
      "links":{k:v for k,v in links.items() if k in ("self","download")}
    }

def norm_title(rec):
    return ((rec.get("metadata") or {}).get("title") or rec.get("title") or "").strip()

result={
  "status":"METADATA_ONLY_NO_NUMERIC_RESPONSE_ACCESS",
  "sources":{},
  "numeric_response_opened":False
}

for key,spec in SOURCES.items():
    rec={"record_id":spec["record_id"],"role":spec["role"]}
    try:
        obj=get_json("https://zenodo.org/api/records/"+spec["record_id"])
        md=obj.get("metadata") or {}
        title=norm_title(obj)
        low=title.lower()
        rec.update({
          "accessible":True,
          "id":str(obj.get("id")),
          "doi":obj.get("doi") or md.get("doi"),
          "conceptdoi":obj.get("conceptdoi") or md.get("conceptdoi"),
          "title":title,
          "publication_date":md.get("publication_date"),
          "access_right":md.get("access_right"),
          "access_status":obj.get("access") or {},
          "resource_type":md.get("resource_type"),
          "license":md.get("license"),
          "description":(md.get("description") or "")[:3000],
          "related_identifiers":md.get("related_identifiers") or [],
          "files":[slim_file(f) for f in (obj.get("files") or [])]
        })
        rec["title_terms_present"]={term:(term in low) for term in spec["title_terms"]}
        rec["title_consistent"]=sum(rec["title_terms_present"].values())>=2
        rec["file_count"]=len(rec["files"])
        rec["zip_files"]=[f for f in rec["files"] if str(f.get("key") or "").lower().endswith(".zip")]
        rec["pointer_files"]=[f for f in rec["files"] if "pointer" in str(f.get("key") or "").lower()]
    except Exception as e:
        rec.update({"accessible":False,"exception_type":type(e).__name__,"exception":str(e)})
    result["sources"][key]=rec

r=result["sources"]
accessible=[x for x in r.values() if x.get("accessible")]
if not accessible:
    disposition="ERIES_EUROPROTEAS_SOURCE_BLOCKED"
else:
    rc=r.get("RESPOND_CANONICAL",{})
    rp=r.get("RESPOND_POINTER",{})
    po=r.get("POLIS",{})
    gi=r.get("GISIS",{})
    canonical_ok=rc.get("accessible") and rc.get("title_consistent") and len(rc.get("zip_files",[]))>=1
    polis_ok=po.get("accessible") and po.get("title_consistent") and len(po.get("zip_files",[]))>=1
    pointer_distinct=(rp.get("accessible") and rp.get("title_consistent")
                      and str(rp.get("id"))!=str(rc.get("id"))
                      and len(rp.get("pointer_files",[]))>=1
                      and len(rp.get("zip_files",[]))==0)
    gisis_identity=gi.get("accessible") and gi.get("title_consistent")
    if canonical_ok and polis_ok and pointer_distinct and gisis_identity:
        disposition="ERIES_EUROPROTEAS_SOURCE_MATRIX_QUALIFIED"
    elif canonical_ok and polis_ok:
        disposition="ERIES_EUROPROTEAS_SOURCE_MATRIX_PARTIAL"
    elif (rc.get("accessible") and rp.get("accessible") and not pointer_distinct):
        disposition="ERIES_EUROPROTEAS_SOURCE_IDENTITY_AMBIGUOUS"
    else:
        disposition="ERIES_EUROPROTEAS_SOURCE_BLOCKED"

result["disposition"]=disposition
result["qualification"]={
  "respond_canonical_has_zip":bool(r.get("RESPOND_CANONICAL",{}).get("zip_files")),
  "respond_pointer_is_metadata_only":bool(r.get("RESPOND_POINTER",{}).get("pointer_files")) and not bool(r.get("RESPOND_POINTER",{}).get("zip_files")),
  "polis_has_zip":bool(r.get("POLIS",{}).get("zip_files")),
  "gisis_identity_resolved":bool(r.get("GISIS",{}).get("accessible") and r.get("GISIS",{}).get("title_consistent")),
  "numeric_response_opened":False
}

(OUT/"result.json").write_text(json.dumps(result,indent=2))
summary={
  "disposition":disposition,
  "qualification":result["qualification"],
  "sources":{k:{
    "id":v.get("id"),
    "doi":v.get("doi"),
    "title":v.get("title"),
    "access_right":v.get("access_right"),
    "file_count":v.get("file_count"),
    "files":[{"key":f.get("key"),"size":f.get("size"),"checksum":f.get("checksum")} for f in v.get("files",[])]
  } for k,v in r.items()}
}
print(json.dumps(summary,indent=2))
