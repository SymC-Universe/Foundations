from pathlib import Path
import json
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
PROV = ROOT / "data" / "desi_dr1_fullshape_upstream_provenance.json"
MANIFEST = ROOT / ".external" / "dr1_fullshape" / "dr1_v1.0.sha256sum"
BASE = "https://data.desi.lbl.gov/public/dr1/vac/dr1/full-shape-cosmo-params/v1.0"
CMB = (
    "planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_"
    "planck2018-highl-plik-TTTEEE_planck-act-dr6-lensing"
)
SN = {
    "pantheonplus": "pantheonplus",
    "union3": "union3",
    "desy5": "desy5sn",
}
TARGETS = {
    "cmb_fixed_mnu": (
        "fixed_mnu_CMB_reference",
        f"cobaya/base/desi-reptvelocileptors-fs-bao-all_{CMB}",
    ),
    "cmb_free_mnu": (
        "free_mnu_CMB_adversary",
        f"cobaya/base_mnu/desi-reptvelocileptors-fs-bao-all_{CMB}",
    ),
}
for key, sn in SN.items():
    TARGETS[f"de_mnu_{key}"] = (
        f"w0wa_plus_free_mnu_{key}",
        f"cobaya/base_mnu_w_wa/desi-reptvelocileptors-fs-bao-all_{sn}_{CMB}",
    )
def remote_size(url):
    req = Request(url, method="HEAD", headers={"User-Agent": "SymC-DMDE/1.0"})
    with urlopen(req, timeout=60) as r:
        n = r.headers.get("Content-Length")
    if n is None:
        raise RuntimeError(f"no Content-Length: {url}")
    return int(n)

manifest = {}
for line in MANIFEST.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    digest, rel = line.split(None, 1)
    manifest[rel] = digest

prov = json.loads(PROV.read_text(encoding="utf-8"))
required = {
    "chain.1.txt", "chain.2.txt", "chain.3.txt", "chain.4.txt",
    "chain.input.yaml", "chain.updated.yaml", "chain.covmat", "chain.checkpoint",
}
for key, (role, rel) in TARGETS.items():
    prefix = rel + "/"
    names = {
        path[len(prefix):]: digest
        for path, digest in manifest.items()
        if path.startswith(prefix) and "/" not in path[len(prefix):]
    }
    missing = sorted(required - set(names))
    if missing:
        raise RuntimeError(f"{key}: missing {missing}")

    files = {}
    for name, digest in sorted(names.items()):
        url = f"{BASE}/{rel}/{name}"
        files[name] = {"sha256": digest, "bytes": remote_size(url)}

    full_bytes = sum(files[f"chain.{i}.txt"]["bytes"] for i in range(1, 5))
    prov["chain_sets"][key] = {
        "scientific_role": role,
        "model": "base_mnu_w_wa" if key.startswith("de_mnu_")
                 else ("base_mnu" if key == "cmb_free_mnu" else "base"),
        "relative_directory": rel,
        "files": files,
        "full_chain_bytes": full_bytes,
        "note": (
            "Neutrino-adversarial lane. CMB fixed/free pair tests mass freedom; "
            "DE+mnu members test whether free neutrino mass absorbs w0-wa behavior."
        ),
    }

prov["neutrino_adversary_suite"] = {
    "status": "sha256_pinned_runner_ready",
    "cmb_pair": ["cmb_fixed_mnu", "cmb_free_mnu"],
    "de_robustness_members": [f"de_mnu_{x}" for x in SN],
    "rule": (
        "Do not reinterpret the CMB-combined free-mnu chain as a DESI-only result. "
        "Compare each free-mnu result only to a dataset-matched fixed-mnu reference."
    ),
}
PROV.write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: prov["chain_sets"][k] for k in TARGETS}, indent=2))