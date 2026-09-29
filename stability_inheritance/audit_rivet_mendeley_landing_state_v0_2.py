#!/usr/bin/env python3
import hashlib, json, re, urllib.request
from pathlib import Path
from html.parser import HTMLParser

OUT=Path("stability_inheritance/results/rivet_mendeley_landing_state")
OUT.mkdir(parents=True,exist_ok=True)
DATASETS={
  "small":"https://data.mendeley.com/datasets/sgmxhdc599/1",
  "large":"https://data.mendeley.com/datasets/dy66vm8t95/1"
}
UUID_RE=re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
URL_RE=re.compile(r"https?://[^\s\"'<>]+")
HINTS=("data.h5","structure_images.jpg","public-files","file_download","download")

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script=False
        self.attrs={}
        self.buf=[]
        self.scripts=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()=="script":
            self.in_script=True
            self.attrs=dict(attrs)
            self.buf=[]
    def handle_data(self,data):
        if self.in_script:
            self.buf.append(data)
    def handle_endtag(self,tag):
        if tag.lower()=="script" and self.in_script:
            self.scripts.append({"attrs":self.attrs,"text":"".join(self.buf)})
            self.in_script=False
            self.attrs={}
            self.buf=[]

def get(url,method="GET"):
    req=urllib.request.Request(url,method=method,headers={"User-Agent":"SymC-Stability-Inheritance-Landing-Audit/1.0","Accept":"text/html,*/*"})
    try:
        with urllib.request.urlopen(req,timeout=45) as r:
            body=b"" if method=="HEAD" else r.read()
            return {"ok":True,"status":getattr(r,"status",None),"final_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length"),"body":body}
    except Exception as e:
        return {"ok":False,"exception_type":type(e).__name__,"exception":str(e),"body":b""}

result={"status":"PUBLIC_LANDING_STATE_ONLY","datasets":{}}
for key,url in DATASETS.items():
    rr=get(url)
    body=rr.pop("body",b"")
    rec={"page":url,"request":rr,"script_count":0,"hits":[],"candidate_urls":[],"head_checks":[]}
    if body:
        html=body.decode("utf-8","replace")
        p=Scripts(); p.feed(html)
        rec["script_count"]=len(p.scripts)
        blocks=[{"source":"html","text":html}]+[{"source":f"script[{i}]","attrs":s["attrs"],"text":s["text"]} for i,s in enumerate(p.scripts)]
        seen=set()
        for blk in blocks:
            txt=blk["text"]
            low=txt.lower()
            if not any(h in low for h in HINTS):
                continue
            for hint in HINTS:
                pos=0
                hl=hint.lower()
                while True:
                    i=low.find(hl,pos)
                    if i<0: break
                    frag=txt[max(0,i-800):min(len(txt),i+1400)]
                    keyhit=(blk["source"],hint,hashlib.sha256(frag.encode("utf-8","replace")).hexdigest())
                    if keyhit not in seen:
                        seen.add(keyhit)
                        urls=[u.rstrip(".,;)]}") for u in URL_RE.findall(frag)]
                        uuids=UUID_RE.findall(frag)
                        rec["hits"].append({"source":blk["source"],"hint":hint,"fragment":frag,"urls":urls,"uuids":uuids})
                        for u in urls:
                            if u not in rec["candidate_urls"]:
                                rec["candidate_urls"].append(u)
                    pos=i+len(hint)
        official=[u for u in rec["candidate_urls"] if "mendeley" in u.lower() or "elsevier" in u.lower()]
        for u in official[:20]:
            h=get(u,method="HEAD"); h["url"]=u; rec["head_checks"].append(h)
    route=False
    descriptor=False
    for h in rec["hits"]:
        frag=h["fragment"].lower()
        if "data.h5" in frag:
            descriptor=True
            if any(x in frag for x in ("public-files","file_download","http")) and (h["urls"] or h["uuids"]):
                route=True
    if route:
        rec["disposition"]="OFFICIAL_FILE_ROUTE_DISCOVERED"
    elif descriptor:
        rec["disposition"]="FILE_DESCRIPTOR_WITHOUT_ROUTE"
    else:
        rec["disposition"]="LANDING_STATE_INSUFFICIENT"
    result["datasets"][key]=rec

disps=[v["disposition"] for v in result["datasets"].values()]
if "OFFICIAL_FILE_ROUTE_DISCOVERED" in disps:
    result["disposition"]="OFFICIAL_FILE_ROUTE_DISCOVERED"
elif "FILE_DESCRIPTOR_WITHOUT_ROUTE" in disps:
    result["disposition"]="FILE_DESCRIPTOR_WITHOUT_ROUTE"
else:
    result["disposition"]="LANDING_STATE_INSUFFICIENT"

(OUT/"result.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
