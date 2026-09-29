#!/usr/bin/env python3
import json, urllib.request
from pathlib import Path

OUT=Path("stability_inheritance/results/brb_longterm_osf_intake")
OUT.mkdir(parents=True,exist_ok=True)
GUIDS=["ghkj7","fbwhz"]
BASE="https://api.osf.io/v2"

def get_json(url):
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-Stability-Inheritance-OSF-Intake/1.0","Accept":"application/vnd.api+json,application/json"})
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def slim_node(obj):
    d=obj.get("data",{})
    a=d.get("attributes",{}) or {}
    rel=d.get("relationships",{}) or {}
    return {
      "id":d.get("id"),
      "type":d.get("type"),
      "title":a.get("title"),
      "description":(a.get("description") or "")[:1000],
      "description_length":len(a.get("description") or ""),
      "public":a.get("public"),
      "date_created":a.get("date_created"),
      "date_modified":a.get("date_modified"),
      "category":a.get("category"),
      "current_user_permissions":a.get("current_user_permissions"),
      "links":d.get("links",{}),
      "relationship_keys":sorted(rel.keys())
    }

def list_paginated(url,max_pages=200):
    out=[]
    page=0
    while url and page<max_pages:
        obj=get_json(url)
        out.extend(obj.get("data",[]))
        url=(obj.get("links") or {}).get("next")
        page+=1
    return out

def recurse_files(url,prefix="",depth=0,max_depth=8):
    if depth>max_depth:
        return []
    rows=[]
    for d in list_paginated(url):
        a=d.get("attributes",{}) or {}
        links=d.get("links",{}) or {}
        kind=a.get("kind")
        name=a.get("name")
        path=a.get("materialized_path") or (prefix+"/"+str(name) if name else prefix)
        rec={
          "id":d.get("id"),
          "type":d.get("type"),
          "kind":kind,
          "name":name,
          "path":path,
          "size":a.get("size"),
          "date_modified":a.get("date_modified"),
          "extra":a.get("extra"),
          "links":{k:v for k,v in links.items() if k in ("download","info","move","delete","new_folder","upload")}
        }
        rows.append(rec)
        if kind=="folder":
            info=links.get("info")
            children=None
            try:
                detail=get_json(info) if info and info.startswith("http") else None
                relationships=((detail or {}).get("data") or {}).get("relationships",{})
                children=((relationships.get("files") or {}).get("links") or {}).get("related",{}).get("href")
            except Exception:
                children=None
            if children:
                rows.extend(recurse_files(children,path,depth+1,max_depth))
    return rows

def classify(paths):
    txt="\n".join((p.get("path") or p.get("name") or "") for p in paths).lower()
    return {
      "randfrf_before":("randfrf_before" in txt or ("randfrf" in txt and "before" in txt)),
      "randfrf_after":("randfrf_after" in txt or ("randfrf" in txt and "after" in txt)),
      "stepsine_before":("stepsine_before" in txt or ("stepsine" in txt and "before" in txt)),
      "stepsine_after":("stepsine_after" in txt or ("stepsine" in txt and "after" in txt)),
      "single_frequency":("singfreq" in txt or ("single" in txt and "freq" in txt)),
      "impact":("impact" in txt or "hammer" in txt),
      "interface_scan":("scan" in txt or "keyence" in txt or "interfac" in txt),
      "first_round":("firstround" in txt or "first_round" in txt or "16dec" in txt),
      "second_round":("secondround" in txt or "second_round" in txt or "17dec" in txt),
      "third_round":("thirdround" in txt or "third_round" in txt or "18dec" in txt)
    }

result={"status":"PUBLIC_OSF_METADATA_ONLY","candidates":{}}

for guid in GUIDS:
    rec={"guid":guid}
    try:
        node=get_json(f"{BASE}/nodes/{guid}/")
        rec["node"]=slim_node(node)
        providers=list_paginated(f"{BASE}/nodes/{guid}/files/")
        rec["providers"]=[]
        all_files=[]
        for p in providers:
            pa=p.get("attributes",{}) or {}
            prel=p.get("relationships",{}) or {}
            related=((prel.get("files") or {}).get("links") or {}).get("related",{}).get("href")
            pr={"id":p.get("id"),"name":pa.get("name"),"node":pa.get("node"),"path":pa.get("path"),"files_related":related}
            rec["providers"].append(pr)
            if related:
                try:
                    all_files.extend(recurse_files(related))
                except Exception as e:
                    pr["listing_exception"]=f"{type(e).__name__}: {e}"
        rec["file_count"]=len(all_files)
        rec["files"]=all_files
        rec["layout_hints"]=classify(all_files)
        title=(rec["node"].get("title") or "").lower()
        desc=(rec["node"].get("description") or "").lower()
        score=0
        for term in ["brb","brake","reuss","reuß","lterm","multiscale","long term","long-term"]:
            if term in title or term in desc:
                score+=1
        score+=sum(bool(v) for v in rec["layout_hints"].values())
        rec["identity_match_score"]=score
        rec["accessible"]=True
    except Exception as e:
        rec["accessible"]=False
        rec["exception_type"]=type(e).__name__
        rec["exception"]=str(e)
        rec["identity_match_score"]=-1
    result["candidates"][guid]=rec

accessible=[r for r in result["candidates"].values() if r.get("accessible")]
if not accessible:
    result["disposition"]="OSF_SOURCE_BLOCKED"
    result["canonical_guid"]=None
else:
    ranked=sorted(accessible,key=lambda x:x.get("identity_match_score",-1),reverse=True)
    top=ranked[0]
    unique=(len(ranked)==1 or top.get("identity_match_score",-1)>ranked[1].get("identity_match_score",-1))
    if unique and top.get("identity_match_score",0)>0:
        result["identity_disposition"]="CANONICAL_OSF_IDENTITY_RESOLVED"
        result["canonical_guid"]=top["guid"]
        h=top.get("layout_hints",{})
        state_ok=all(h.get(k) for k in ("randfrf_before","randfrf_after","first_round","second_round","third_round"))
        supporting=bool(h.get("impact") or h.get("interface_scan"))
        result["layout_disposition"]="LONG_TERM_LAYOUT_QUALIFIED" if state_ok and supporting else "LONG_TERM_LAYOUT_PARTIAL"
        result["disposition"]=result["layout_disposition"]
    else:
        result["identity_disposition"]="OSF_IDENTITY_AMBIGUOUS"
        result["canonical_guid"]=None
        result["disposition"]="OSF_IDENTITY_AMBIGUOUS"

(OUT/"result.json").write_text(json.dumps(result,indent=2))
summary={
 "disposition":result.get("disposition"),
 "identity_disposition":result.get("identity_disposition"),
 "canonical_guid":result.get("canonical_guid"),
 "candidates":{k:{
    "accessible":v.get("accessible"),
    "title":(v.get("node") or {}).get("title"),
    "identity_match_score":v.get("identity_match_score"),
    "file_count":v.get("file_count"),
    "layout_hints":v.get("layout_hints")
 } for k,v in result["candidates"].items()}
}
print(json.dumps(summary,indent=2))
