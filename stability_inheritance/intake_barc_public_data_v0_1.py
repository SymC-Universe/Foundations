#!/usr/bin/env python3
import json, re, urllib.request
from pathlib import Path
from html import unescape

OUT=Path("stability_inheritance/results/barc_public_intake")
OUT.mkdir(parents=True,exist_ok=True)

URLS={
 "wiki":"https://wiki.sem.org/wiki/BARC",
 "challenge_pdf_share":"https://byu.box.com/s/w2aivpyq1r9gvvd916vkj80j7c4h5i42",
 "random_vibration_share":"https://byu.box.com/s/a16vknrscqt2ukp786a0j9yyqrhydsec",
 "test_data_share":"https://byu.box.com/s/gbu486g0chzvzkw64mf53kfjocdthaqn",
 "hardware_models_share":"https://byu.box.com/s/zi6ntcjfdsi0uc1o2e8bf7g3iq82wrnv"
}

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0","Accept":"text/html,application/xhtml+xml"})
    with urllib.request.urlopen(req,timeout=60) as r:
        b=r.read(2_000_000)
        txt=b.decode("utf-8",errors="replace")
        m=re.search(r"<title[^>]*>(.*?)</title>",txt,re.I|re.S)
        title=unescape(re.sub(r"\s+"," ",m.group(1)).strip()) if m else None
        plain=re.sub(r"<script.*?</script>"," ",txt,flags=re.I|re.S)
        plain=re.sub(r"<style.*?</style>"," ",plain,flags=re.I|re.S)
        plain=re.sub(r"<[^>]+>"," ",plain)
        plain=unescape(re.sub(r"\s+"," ",plain)).strip()
        return {
          "requested_url":url,
          "final_url":r.geturl(),
          "status":getattr(r,"status",None),
          "content_type":r.headers.get("Content-Type"),
          "bytes_read":len(b),
          "title":title,
          "text_preview":plain[:1200]
        }

res={"status":"P0Q_SOURCE_METADATA_ONLY","numeric_test_data_downloaded":False,"sources":{}}
for key,url in URLS.items():
    try:
        res["sources"][key]=fetch(url)
    except Exception as e:
        res["sources"][key]={"requested_url":url,"error_type":type(e).__name__,"error":str(e)}

wiki_ok=res["sources"]["wiki"].get("status")==200
test_ok=res["sources"]["test_data_share"].get("status")==200
hardware_ok=res["sources"]["hardware_models_share"].get("status")==200
if wiki_ok and test_ok and hardware_ok:
    res["disposition"]="BARC_PUBLIC_INDEX_PASS"
elif wiki_ok:
    res["disposition"]="BARC_PUBLIC_INDEX_PARTIAL"
else:
    res["disposition"]="BARC_PUBLIC_INDEX_BLOCKED"

(OUT/"result.json").write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
