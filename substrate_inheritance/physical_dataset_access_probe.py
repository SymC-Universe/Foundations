#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import urllib.error
import urllib.request

OUT = pathlib.Path("substrate_inheritance/results/SI_PHYSICAL_DATASET_ACCESS_PROBE_v0.1.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

DATASET = "2wdk4m5n97"
VERSION = 1
WEB = f"https://data.mendeley.com/datasets/{DATASET}/{VERSION}"
API = f"https://api.data.mendeley.com/datasets/{DATASET}"
FILES_API = f"https://api.data.mendeley.com/datasets/{DATASET}/files?version={VERSION}"

def fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent":"SymC-SI-physical-access-probe/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return {
                "ok": True,
                "status": getattr(r, "status", 200),
                "final_url": r.geturl(),
                "content_type": r.headers.get("content-type"),
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                "body": body,
            }
    except urllib.error.HTTPError as e:
        return {"ok":False,"status":e.code,"error":repr(e),"body":b""}
    except Exception as e:
        return {"ok":False,"status":None,"error":repr(e),"body":b""}

web = fetch(WEB)
api = fetch(API)
files = fetch(FILES_API)

record = {
    "schema":"si-physical-dataset-access-probe-v0.1",
    "stage":"P0_MECHANICAL_ACCESS_ONLY",
    "dataset":"Korbar 2026 dynamic joint identification",
    "doi":"10.17632/2wdk4m5n97.1",
    "dataset_id":DATASET,
    "version":VERSION,
    "firewall":{
        "experimental_Y_AJB_values_opened":False,
        "modal_or_carrier_outcomes_computed":False,
        "physical_threshold_frozen":False,
        "physical_inheritance_claim":False,
    },
    "endpoints":{},
}

for name, item in [("web",web),("dataset_api",api),("files_api",files)]:
    record["endpoints"][name] = {k:v for k,v in item.items() if k != "body"}

# Metadata-only extraction. Do not download HDF5 file contents here.
if files.get("ok"):
    try:
        obj = json.loads(files["body"].decode("utf-8"))
        inventory = []
        if isinstance(obj, dict):
            iterable = obj.get("data") or obj.get("files") or obj.get("items") or []
        else:
            iterable = obj
        for x in iterable:
            if not isinstance(x, dict):
                continue
            cd = x.get("content_details") or {}
            inventory.append({
                "filename":x.get("filename") or x.get("name"),
                "id":x.get("id"),
                "size":x.get("size") or cd.get("size"),
                "sha256_hash":cd.get("sha256_hash"),
                "content_type":cd.get("content_type"),
                "download_url_present":bool(cd.get("download_url")),
            })
        record["public_file_inventory"] = inventory
    except Exception as e:
        record["files_api_parse_error"] = repr(e)

if web.get("ok"):
    text = web["body"].decode("utf-8", errors="replace")
    record["web_mentions"] = {
        "experimental_h5": "experimental.h5" in text,
        "numerical_h5": "numerical.h5" in text,
        "cc_by_4_0": bool(re.search(r"CC\s*BY\s*4\.0", text, flags=re.I)),
    }

OUT.write_text(json.dumps(record, indent=2), encoding="utf-8")
print(json.dumps(record, indent=2))
