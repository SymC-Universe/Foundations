#!/usr/bin/env python3
"""Prepare the exact DESI DR1 full-shape confirmatory environment.

Default behavior downloads and hash-verifies only compact official chain
metadata. Large likelihood products and ~993 MB posterior chains are opt-in.

This script only transports and verifies frozen official chain families; interpretation is performed by separate DM/DE analysis scripts.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = PROJECT_ROOT / "cosmology_desi" / "data" / "desi_dr1_fullshape_upstream_provenance.json"
BASE_RELEASE = "https://data.desi.lbl.gov/public/dr1/vac/dr1/full-shape-cosmo-params/v1.0"
UPSTREAM_GIT = "https://github.com/cosmodesi/desi-kp-cosmological-likelihoods.git"

COMPACT = (
    "chain.input.yaml",
    "chain.updated.yaml",
    "chain.covmat",
    "chain.checkpoint",
    "chain.margestats",
)
FULL_CHAINS = ("chain.1.txt", "chain.2.txt", "chain.3.txt", "chain.4.txt")
DEPENDENCIES = ("numpy", "scipy", "cobaya", "camb", "cosmoprimo", "velocileptors", "lsstypes")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_resume(url: str, target: Path, expected_bytes: int | None = None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    start = target.stat().st_size if target.exists() else 0
    if expected_bytes is not None and start == expected_bytes:
        return
    headers = {"User-Agent": "SymC-DESI-reproduction/1.0"}
    if start:
        headers["Range"] = f"bytes={start}-"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=120) as r:
        status = getattr(r, "status", None)
        if start and status != 206:
            # Server ignored Range. Restart cleanly rather than appending duplicate bytes.
            start = 0
            target.unlink(missing_ok=True)
            return download_resume(url, target, expected_bytes)
        mode = "ab" if start else "wb"
        with target.open(mode) as f:
            while True:
                block = r.read(8 * 1024 * 1024)
                if not block:
                    break
                f.write(block)
    if expected_bytes is not None and target.stat().st_size != expected_bytes:
        raise RuntimeError(
            f"size mismatch for {target.name}: {target.stat().st_size} != {expected_bytes}"
        )


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_upstream(workspace: Path, prov: dict) -> Path:
    dst = workspace / "upstream" / "desi-kp-cosmological-likelihoods"
    commit = prov["implementation"]["commit"]
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--filter=blob:none", UPSTREAM_GIT, str(dst)])
    run(["git", "fetch", "--all", "--tags"], cwd=dst)
    run(["git", "checkout", "--detach", commit], cwd=dst)
    got = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=dst, text=True).strip()
    if got != commit:
        raise RuntimeError(f"upstream commit mismatch: {got} != {commit}")
    return dst


def dependency_receipt() -> dict:
    return {name: importlib.util.find_spec(name) is not None for name in DEPENDENCIES}


def fetch_chain_files(workspace: Path, chain: dict, names: tuple[str, ...]) -> list[dict]:
    rel = chain["relative_directory"]
    meta = chain["files"]
    out = []
    for name in names:
        if name not in meta:
            print(f"skip {name}: no verified receipt pinned for this chain set", flush=True)
            continue
        spec = meta[name]
        url = f"{BASE_RELEASE}/{rel}/{name}"
        target = workspace / "official_chain" / name
        print(f"fetch {name}", flush=True)
        download_resume(url, target, spec.get("bytes"))
        digest = sha256(target)
        if digest != spec["sha256"]:
            raise RuntimeError(f"SHA-256 mismatch for {name}: {digest} != {spec['sha256']}")
        out.append({
            "name": name,
            "url": url,
            "path": str(target),
            "bytes": target.stat().st_size,
            "sha256": digest,
            "verified": True,
        })
    return out


def fetch_likelihood_data(workspace: Path, upstream: Path) -> Path:
    target = workspace / "likelihood"
    script = upstream / "dr1" / "cobaya" / "download.py"
    run([sys.executable, str(script), "--data-dir", str(target)])
    return target


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--workspace",
        default=str(PROJECT_ROOT / "cosmology_desi" / ".external" / "dr1_fullshape"),
        help="Untracked workspace for official DESI inputs.",
    )
    ap.add_argument(
        "--chain-key",
        choices=("baseline", "modified_gravity", "w0wa_desi_only_stress", "de_pantheonplus", "de_union3", "de_desy5"),
        default="baseline",
        help="Pinned released chain family to prepare. DE suite members are co-equal sensitivity comparators.",
    )
    ap.add_argument("--clone-implementation", action="store_true")
    ap.add_argument("--likelihood-data", action="store_true",
                    help="Download official packaged DR1 FS+BAO likelihood HDF5 files.")
    ap.add_argument("--full-chains", action="store_true",
                    help="Also download and verify the four posterior chains for the selected chain set.")
    ap.add_argument("--dependency-check", action="store_true")
    args = ap.parse_args()

    prov = json.loads(PROVENANCE.read_text())
    chain = prov["chain_sets"][args.chain_key]
    workspace = Path(args.workspace).resolve() / args.chain_key
    workspace.mkdir(parents=True, exist_ok=True)

    receipt = {
        "prepared_at_unix": time.time(),
        "workspace": str(workspace),
        "scientific_status": "transport_and_reproduction_preparation_only",
        "chain_key": args.chain_key,
        "scientific_role": chain["scientific_role"],
        "chain_directory": chain["relative_directory"],
        "compact_files": [],
        "full_chain_files": [],
        "implementation": None,
        "likelihood_data": None,
        "dependencies": dependency_receipt() if args.dependency_check else None,
    }

    receipt["compact_files"] = fetch_chain_files(workspace, chain, COMPACT)

    upstream = None
    if args.clone_implementation or args.likelihood_data:
        upstream = ensure_upstream(workspace, prov)
        receipt["implementation"] = {
            "repository": UPSTREAM_GIT,
            "commit": prov["implementation"]["commit"],
            "path": str(upstream),
            "verified": True,
        }

    if args.likelihood_data:
        if upstream is None:
            upstream = ensure_upstream(workspace, prov)
        likelihood = fetch_likelihood_data(workspace, upstream)
        receipt["likelihood_data"] = str(likelihood)

    if args.full_chains:
        print(
            f"Downloading the four official posterior chains for {args.chain_key}. "
            "Downloads are resumable and hash-verified.",
            flush=True,
        )
        receipt["full_chain_files"] = fetch_chain_files(workspace, chain, FULL_CHAINS)

    receipt_path = workspace / "prepare_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    print(f"receipt: {receipt_path}")


if __name__ == "__main__":
    main()