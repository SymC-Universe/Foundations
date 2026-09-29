#!/usr/bin/env python3
import hashlib, json, re, urllib.request, zipfile, tempfile
from pathlib import Path

COMMIT="2d42d3a618206da58642674d3287ae34dfc7d5e5"
URL=f"https://raw.githubusercontent.com/mattiacenedese/BRBtesting/{COMMIT}/showData.mlx"
EXPECTED_BLOB="2cc7f972823328d6ace9b3ec957147a221ae4b09"
OUT=Path("stability_inheritance/results/brb_ringdown_code_audit")
OUT.mkdir(parents=True,exist_ok=True)

def blobsha(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()

req=urllib.request.Request(URL,headers={"User-Agent":"SymC-Stability-Inheritance-P0Q/1.0"})
with urllib.request.urlopen(req,timeout=60) as r:
    b=r.read()
sha=blobsha(b)
if sha!=EXPECTED_BLOB:
    raise RuntimeError(f"source blob mismatch {sha}")

with tempfile.TemporaryDirectory() as td:
    p=Path(td)/"showData.mlx"; p.write_bytes(b)
    with zipfile.ZipFile(p,"r") as z:
        xml=z.read("matlab/document.xml").decode("utf-8",errors="replace")

blocks=[part.split("]]>",1)[0] for part in xml.split("<![CDATA[")[1:] if "]]>" in part]
ring=[x.strip() for x in blocks if "ShakerRingdown.mat" in x]
out={
  "status":"SOURCE_CODE_SEMANTICS_ONLY",
  "source_blob":sha,
  "source_sha256":hashlib.sha256(b).hexdigest(),
  "ringdown_code_blocks":ring,
  "response_data_accessed":False,
  "disposition":"BRB_RINGDOWN_CODE_QUALIFIED" if len(ring)>=2 else "BRB_RINGDOWN_CODE_INCOMPLETE"
}
(OUT/"result.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
