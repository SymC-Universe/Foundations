from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "results" / "d02c_candidate_probe"
ARCHIVE = CACHE / "Hyun_CoFeBYIG_Phys_Rev_Applied_2026_pre.zip"
OUT = ROOT / "results" / "D02C_CANDIDATE_HYUN_SCHEMA_v0.1.json"
URL = "https://zenodo.org/records/21370159/files/Hyun_CoFeBYIG_Phys_Rev_Applied_2026_pre.zip?download=1"
EXPECTED_MD5 = "7cf837b09acefa5a8d7586cb155e64dc"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    if ARCHIVE.exists() and digest(ARCHIVE, "md5") == EXPECTED_MD5:
        return
    with requests.get(URL, headers=HEADERS, stream=True, timeout=300) as r:
        r.raise_for_status()
        with ARCHIVE.open("wb") as f:
            for chunk in r.iter_content(chunk_size=4 * 1024 * 1024):
                if chunk:
                    f.write(chunk)


def text_schema(data: bytes, name: str) -> dict:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        return {"path": name, "text_probe": "UNDECODABLE"}

    lines = text.splitlines()
    header_like = []
    for line in lines[:80]:
        line = line.strip()
        if not line:
            continue
        # Emit only lines containing alphabetic metadata/headers; suppress numeric-only result rows.
        if re.search(r"[A-Za-z]", line):
            header_like.append(line[:240])
        if len(header_like) >= 25:
            break

    return {
        "path": name,
        "line_count": len(lines),
        "header_like_lines_only": header_like,
    }


def main() -> None:
    download()
    md5 = digest(ARCHIVE, "md5")
    if md5 != EXPECTED_MD5:
        raise RuntimeError(f"MD5 mismatch {md5}")

    files = []
    with zipfile.ZipFile(ARCHIVE) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            item = {
                "path": info.filename,
                "size_bytes": info.file_size,
                "crc32": f"{info.CRC:08x}",
                "extension": Path(info.filename).suffix.lower(),
            }
            ext = item["extension"]
            if info.file_size <= 2_000_000 and ext in {".txt",".csv",".dat",".tsv",".md",".py",".m"}:
                item["text_schema"] = text_schema(zf.read(info.filename), info.filename)
            files.append(item)

    result = {
        "schema": "d02c-hyun-candidate-schema-v0.1",
        "status": "CANDIDATE_STRUCTURE_ONLY_NO_DECISIVE_RESULT_INTERPRETATION",
        "source": {
            "url": URL,
            "md5": md5,
            "sha256": digest(ARCHIVE, "sha256"),
            "size_bytes": ARCHIVE.stat().st_size,
        },
        "file_count": len(files),
        "files": files,
        "eligibility_keywords_to_verify": [
            "linewidth", "damping", "quality factor", "Q", "FWHM",
            "field", "diameter", "period", "mode", "hybrid", "MOKE", "frequency"
        ],
        "guard": "Probe reports file names and text headers/metadata only. It does not summarize the direction/order of scientific outcomes.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "file_count": result["file_count"],
        "sha256": result["source"]["sha256"],
        "output": str(OUT),
    }, indent=2))


if __name__ == "__main__":
    main()
