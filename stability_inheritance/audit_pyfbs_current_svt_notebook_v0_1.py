#!/usr/bin/env python3
import hashlib, json, urllib.request
from pathlib import Path

URL="https://gitlab.com/pyFBS/pyFBS/-/raw/master/examples/09_FBS_decoupling_SVT.ipynb"
OUT=Path("stability_inheritance/results/pyfbs_current_notebook_audit")
OUT.mkdir(parents=True,exist_ok=True)
tokens=[
 "pos_xlsx","Channels_B","Impacts_B","Channels_AB","Impacts_AB",
 "grouping_no","group","no_svs","SVT(","apply_SVT","apply_svt",
 "Y_A.p","Y_B.p","Y_AB.p","Y_AB_un","arr_","read_excel"
]
res={"status":"P0Q_SOURCE_CODE_AUDIT","source_url":URL,"target_data_downloaded":False}
try:
    req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-Audit/1.0"})
    with urllib.request.urlopen(req,timeout=60) as r:
        raw=r.read()
        res["final_url"]=r.geturl()
        res["http_status"]=getattr(r,"status",None)
except Exception as e:
    res.update({"disposition":"SOURCE_AUDIT_BLOCKED","exception_type":type(e).__name__,"exception":str(e)})
    (OUT/"result.json").write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))
    raise SystemExit(0)
res["bytes"]=len(raw)
res["sha256"]=hashlib.sha256(raw).hexdigest()
try:
    nb=json.loads(raw)
    hits=[]
    for i,cell in enumerate(nb.get("cells",[])):
        if cell.get("cell_type")!="code":
            continue
        src="".join(cell.get("source",[]))
        if any(tok in src for tok in tokens):
            hits.append({"cell_index":i,"source":src})
    res["matching_code_cells"]=hits
    res["matching_cell_count"]=len(hits)
    joined="\n".join(h["source"] for h in hits)
    required=[
      ("B metadata","Channels_B" in joined and "Impacts_B" in joined),
      ("AB metadata","Channels_AB" in joined and "Impacts_AB" in joined),
      ("SVT","SVT(" in joined),
      ("apply","apply_SVT" in joined or "apply_svt" in joined)
    ]
    res["route_checks"]={k:v for k,v in required}
    res["disposition"]="CURRENT_NOTEBOOK_ROUTE_IDENTIFIED" if all(v for _,v in required) else "CURRENT_NOTEBOOK_ROUTE_INCOMPLETE"
except Exception as e:
    res.update({"disposition":"SOURCE_AUDIT_BLOCKED","exception_type":type(e).__name__,"exception":str(e)})
(OUT/"result.json").write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
