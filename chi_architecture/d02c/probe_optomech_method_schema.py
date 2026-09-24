from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "D02C_OPTOMECH_METHOD_SCHEMA_v0.1.json"
HEADERS = {"User-Agent": "SymC-reproducibility/1.0 (+https://github.com/SymC-Universe/Foundations)"}

FILES = {
    "readme": {
        "url": "https://ndownloader.figshare.com/files/54013754",
        "md5": "98ccce53fc1ccdf1233e550325d9106d",
    },
    "strong_coupling": {
        "url": "https://ndownloader.figshare.com/files/53674550",
        "md5": "568d9fa1efdff96c6fce8ebdcd084ac6",
    },
    "processing_5p24mW": {
        "url": "https://ndownloader.figshare.com/files/53674535",
        "md5": None,
    },
    "detuning_5p24mW": {
        "url": "https://ndownloader.figshare.com/files/53674640",
        "md5": None,
    },
}


def md5_bytes(data: bytes) -> str:
    h = hashlib.md5()
    h.update(data)
    return h.hexdigest()


def decode(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    raise RuntimeError("unable to decode text file")


def safe_text_schema(text: str) -> dict:
    lines = text.splitlines()
    header_like = []
    for line in lines[:120]:
        s = line.strip()
        if not s:
            continue
        # Preserve labels/method text but suppress rows that are numeric-only.
        if re.search(r"[A-Za-z]", s):
            header_like.append(s[:400])
        if len(header_like) >= 50:
            break

    delimiters = {
        "tab": sum("\t" in line for line in lines[:20]),
        "comma": sum("," in line for line in lines[:20]),
        "semicolon": sum(";" in line for line in lines[:20]),
    }
    return {
        "line_count": len(lines),
        "header_like_lines_only": header_like,
        "delimiter_clues": delimiters,
    }


def main() -> None:
    result = {
        "schema": "d02c-optomech-method-schema-v0.1",
        "status": "METHOD_AND_HEADER_SCHEMA_ONLY_NO_ORDERING_INTERPRETATION",
        "files": {},
    }

    for role, spec in FILES.items():
        r = requests.get(spec["url"], headers=HEADERS, timeout=120)
        r.raise_for_status()
        data = r.content
        actual = md5_bytes(data)
        expected = spec["md5"]
        if expected is not None and actual != expected:
            raise RuntimeError(f"MD5 mismatch for {role}: {actual}")

        text = decode(data)
        result["files"][role] = {
            "url": spec["url"],
            "size_bytes": len(data),
            "md5": actual,
            "schema": safe_text_schema(text),
        }

    result["guard"] = (
        "Only readme/method text and header-like lines are emitted. "
        "Numeric result rows are not emitted and no ordering is evaluated."
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
