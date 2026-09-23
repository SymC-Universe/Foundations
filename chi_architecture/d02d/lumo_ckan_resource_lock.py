from __future__ import annotations

import hashlib
import json
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "D02D_LUMO_CKAN_RESOURCE_LOCK_v0.1.json"
API = "https://data.uni-hannover.de/api/3/action/package_show"
DATASET_ID = "93b52576-6a5a-4ce9-8c27-a0372590f7b0"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

TARGET_NAMES = {
    "README.pdf",
    "exemplary Datasets healthy and DAM6 111",
    "exemplary Datasets healthy and DAM4 111",
    "exemplary Datasets healthy and DAM3 111",
    "exemplary Datasets healthy and DAM6 010",
    "exemplary Datasets healthy and DAM4 010",
    "exemplary Datasets healthy and DAM3 010",
}


def main() -> None:
    r = requests.get(API, params={"id": DATASET_ID}, headers=HEADERS, timeout=120)
    r.raise_for_status()
    payload = r.json()
    if payload.get("success") is not True:
        raise RuntimeError("CKAN package_show returned success=false")
    pkg = payload["result"]

    selected = []
    for item in pkg.get("resources", []):
        name = str(item.get("name", "")).strip()
        if name in TARGET_NAMES:
            selected.append({
                "name": name,
                "id": item.get("id"),
                "format": item.get("format"),
                "mimetype": item.get("mimetype"),
                "size": item.get("size"),
                "hash": item.get("hash"),
                "url": item.get("url"),
                "url_type": item.get("url_type"),
                "created": item.get("created"),
                "last_modified": item.get("last_modified"),
            })

    names = {x["name"] for x in selected}
    missing = sorted(TARGET_NAMES - names)
    all_resource_names = [str(x.get("name", "")).strip() for x in pkg.get("resources", [])]

    raw = json.dumps(payload["result"], sort_keys=True, separators=(",", ":")).encode()
    result = {
        "schema": "d02d-lumo-ckan-resource-lock-v0.1",
        "status": "RESOURCE_METADATA_ONLY_NO_ARCHIVE_CONTENT_OPENED",
        "dataset": {
            "doi": "10.25835/0027803",
            "package_id": DATASET_ID,
            "title": pkg.get("title"),
            "metadata_modified": pkg.get("metadata_modified"),
            "license_title": pkg.get("license_title"),
            "package_metadata_sha256": hashlib.sha256(raw).hexdigest(),
        },
        "selected_resources": sorted(selected, key=lambda x: x["name"]),
        "missing_requested_names": missing,
        "all_resource_names": all_resource_names,
        "guard": "Only CKAN metadata were read. ZIP/PDF source bytes were not opened.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "selected_resource_count": len(selected),
        "missing_requested_count": len(missing),
        "metadata_modified": result["dataset"]["metadata_modified"],
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
