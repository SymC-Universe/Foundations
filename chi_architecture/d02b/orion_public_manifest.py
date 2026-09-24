from __future__ import annotations

import hashlib
import json
import re
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "D02B_ORION_PUBLIC_MANIFEST_v0.1.json"
PAGE_URL = "https://data.mendeley.com/datasets/p4fg6snh3r/1"
DATASET_ID = "p4fg6snh3r"
HEADERS = {
    "User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)",
    "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get(url: str, accept: str | None = None) -> dict:
    headers = dict(HEADERS)
    if accept:
        headers["Accept"] = accept
    try:
        r = requests.get(url, headers=headers, timeout=90, allow_redirects=True)
        return {
            "url": url,
            "final_url": r.url,
            "status_code": r.status_code,
            "content_type": r.headers.get("content-type"),
            "content_length": len(r.content),
            "sha256": sha256_bytes(r.content),
            "text": r.text if "text" in (r.headers.get("content-type") or "") or "json" in (r.headers.get("content-type") or "") else "",
        }
    except Exception as exc:
        return {"url": url, "error": type(exc).__name__ + ": " + str(exc), "text": ""}


def extract_public_metadata(html: str) -> dict:
    hrefs = []
    for m in re.finditer(r'''href=["']([^"']+)["']''', html, flags=re.I):
        href = unescape(m.group(1))
        if any(k in href.lower() for k in ["download", "file", DATASET_ID, "api"]):
            hrefs.append(urljoin(PAGE_URL, href))
    hrefs = sorted(set(hrefs))

    # Metadata-only textual clues. Do not emit numeric scientific cell data.
    file_tokens = sorted(set(re.findall(
        r'''[A-Za-z0-9_ .()/+-]+\.(?:mat|m|txt|csv|zip|rar|xlsx|xls|dat|ascii|mph)''',
        html,
        flags=re.I,
    )))
    file_tokens = [x.strip() for x in file_tokens if 1 < len(x.strip()) < 220]

    script_clues = []
    for m in re.finditer(r'''<script[^>]*>(.*?)</script>''', html, flags=re.I | re.S):
        block = m.group(1)
        low = block.lower()
        if DATASET_ID in low or "download" in low or '"files"' in low or "'files'" in low:
            cleaned = re.sub(r"\s+", " ", block).strip()
            if cleaned:
                script_clues.append(cleaned[:4000])

    return {
        "candidate_links": hrefs,
        "filename_tokens": file_tokens,
        "script_clues_truncated": script_clues[:20],
    }


def main() -> None:
    page = get(PAGE_URL)
    html = page.pop("text", "")
    page["metadata_extract"] = extract_public_metadata(html)

    api_attempts = []
    candidates = [
        f"https://api.mendeley.com/datasets/{DATASET_ID}",
        f"https://api.mendeley.com/datasets/{DATASET_ID}?version=1",
        f"https://api.mendeley.com/datasets/{DATASET_ID}/1",
        f"https://data.mendeley.com/api/datasets/{DATASET_ID}/1",
        f"https://data.mendeley.com/api/datasets/{DATASET_ID}",
    ]
    accepts = [
        "application/vnd.mendeley-public-dataset.1+json",
        "application/json",
    ]
    for url in candidates:
        for accept in accepts:
            item = get(url, accept=accept)
            text = item.pop("text", "")
            item["accept"] = accept
            if text:
                item["body_prefix"] = re.sub(r"\s+", " ", text)[:8000]
            api_attempts.append(item)

    out = {
        "schema": "d02b-orion-public-manifest-v0.1",
        "status": "PUBLIC_METADATA_ONLY_NO_SCIENTIFIC_RESPONSE_VALUES_PARSED",
        "dataset": {
            "id": DATASET_ID,
            "version": 1,
            "doi": "10.17632/p4fg6snh3r.1",
            "page": page,
        },
        "api_attempts": api_attempts,
        "guard": "This diagnostic records page/API/file metadata only. It does not open MAT/ASCII response data.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "page_status": out["dataset"]["page"].get("status_code"),
        "candidate_link_count": len(out["dataset"]["page"]["metadata_extract"]["candidate_links"]),
        "filename_token_count": len(out["dataset"]["page"]["metadata_extract"]["filename_tokens"]),
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
