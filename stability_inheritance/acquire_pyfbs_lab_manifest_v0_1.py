#!/usr/bin/env python3
import hashlib, json, urllib.request
from pathlib import Path

BASE="https://gitlab.com/pyFBS/pyFBS_data/-/raw/master/lab_testbench/Measurements/"
FILES=["Y_A.p","Y_B.p","Y_AB.p","coupling_example.xlsx"]
OUT=Path("stability_inheritance/results/pyfbs_lab_intake")
TMP=OUT/"raw"
OUT.mkdir(parents=True,exist_ok=True)
TMP.mkdir(parents=True,exist_ok=True)

manifest={
  "status":"ACQUISITION_ONLY_NO_SCIENTIFIC_VALUES_INSPECTED",
  "base_url":BASE,
  "files":[]
}
for name in FILES:
    url=BASE+name
    path=TMP/name
    urllib.request.urlretrieve(url,path)
    b=path.read_bytes()
    manifest["files"].append({
      "name":name,
      "url":url,
      "size_bytes":len(b),
      "sha256":hashlib.sha256(b).hexdigest()
    })

(OUT/"manifest.json").write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
