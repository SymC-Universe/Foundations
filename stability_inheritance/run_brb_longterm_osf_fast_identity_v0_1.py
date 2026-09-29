#!/usr/bin/env python3
import json, urllib.request
from pathlib import Path

OUT=Path("stability_inheritance/results/brb_longterm_osf_fast_identity")
OUT.mkdir(parents=True,exist_ok=True)
GUIDS=["ghkj7","fbwhz"]
BASE="https://api.osf.io/v2"

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-Stability-Inheritance-OSF-Fast/1.0","Accept":"application/vnd.api+json,application/json"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))

result={"status":"PUBLIC_OSF_METADATA_ONLY","candidates":{}}
for guid in GUIDS:
    rec={"guid":guid}
    try:
        node=get(f"{BASE}/nodes/{guid}/")
        d=node.get("data",{}); a=d.get("attributes",{}) or {}
        rec["node"]={
          "id":d.get("id"),"title":a.get("title"),"description":(a.get("description") or "")[:2000],
          "public":a.get("public"),"date_created":a.get("date_created"),"date_modified":a.get("date_modified"),
          "links":d.get("links",{})
        }
        providers=get(f"{BASE}/nodes/{guid}/files/").get("data",[])
        rec["providers"]=[]
        rec["root_entries"]=[]
        for p in providers:
            pa=p.get("attributes",{}) or {}; rel=p.get("relationships",{}) or {}
            related=((rel.get("files") or {}).get("links") or {}).get("related",{}).get("href")
            rec["providers"].append({"id":p.get("id"),"name":pa.get("name"),"related":related})
            if related:
                try:
                    root=get(related)
                    for x in root.get("data",[])[:200]:
                        xa=x.get("attributes",{}) or {}
                        rec["root_entries"].append({"provider":p.get("id"),"id":x.get("id"),"kind":xa.get("kind"),"name":xa.get("name"),"path":xa.get("materialized_path"),"size":xa.get("size")})
                except Exception as e:
                    rec.setdefault("root_errors",[]).append(f"{type(e).__name__}: {e}")
        text=((rec["node"].get("title") or "")+" "+(rec["node"].get("description") or "")+" "+" ".join(str(x.get("name") or "") for x in rec["root_entries"])).lower()
        terms=["brb","brake","reuss","reuß","lterm","multiscale","long term","long-term"]
        rec["match_terms"]=[t for t in terms if t in text]
        rec["match_score"]=len(rec["match_terms"])
        rec["accessible"]=True
    except Exception as e:
        rec["accessible"]=False
        rec["match_score"]=-1
        rec["exception_type"]=type(e).__name__
        rec["exception"]=str(e)
    result["candidates"][guid]=rec

acc=[v for v in result["candidates"].values() if v.get("accessible")]
if not acc:
    result["disposition"]="OSF_IDENTITY_AMBIGUOUS"
    result["canonical_guid"]=None
else:
    ranked=sorted(acc,key=lambda x:x.get("match_score",-1),reverse=True)
    if len(ranked)==1 or ranked[0].get("match_score",-1)>ranked[1].get("match_score",-1):
        result["disposition"]="CANONICAL_OSF_IDENTITY_RESOLVED"
        result["canonical_guid"]=ranked[0]["guid"]
    elif len(ranked)>=2 and ranked[0].get("match_score",0)>0 and ranked[1].get("match_score",0)>0:
        result["disposition"]="OSF_IDS_LINKED_OR_DUPLICATE"
        result["canonical_guid"]=None
    else:
        result["disposition"]="OSF_IDENTITY_AMBIGUOUS"
        result["canonical_guid"]=None

(OUT/"result.json").write_text(json.dumps(result,indent=2))
print(json.dumps({
  "disposition":result["disposition"],
  "canonical_guid":result.get("canonical_guid"),
  "candidates":{k:{"accessible":v.get("accessible"),"title":(v.get("node") or {}).get("title"),"match_score":v.get("match_score"),"match_terms":v.get("match_terms"),"root_entries":len(v.get("root_entries",[]))} for k,v in result["candidates"].items()}
},indent=2))
