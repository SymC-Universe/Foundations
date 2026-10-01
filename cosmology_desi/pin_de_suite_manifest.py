from pathlib import Path
import json
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
PROV = ROOT / "data" / "desi_dr1_fullshape_upstream_provenance.json"
MANIFEST = ROOT / ".external" / "dr1_fullshape" / "dr1_v1.0.sha256sum"
BASE = "https://data.desi.lbl.gov/public/dr1/vac/dr1/full-shape-cosmo-params/v1.0"

TARGETS = {
    "de_pantheonplus": (
        "pantheonplus",
        "cobaya/base_w_wa/desi-reptvelocileptors-fs-bao-all_pantheonplus_"
        "planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_"
        "planck2018-highl-plik-TTTEEE_planck-act-dr6-lensing",
    ),
    "de_union3": (
        "union3",
        "cobaya/base_w_wa/desi-reptvelocileptors-fs-bao-all_union3_"
        "planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_"
        "planck2018-highl-plik-TTTEEE_planck-act-dr6-lensing",
    ),
    "de_desy5": (
        "desy5",
        "cobaya/base_w_wa/desi-reptvelocileptors-fs-bao-all_desy5sn_"
        "planck2018-lowl-TT-clik_planck2018-lowl-EE-clik_"
        "planck2018-highl-plik-TTTEEE_planck-act-dr6-lensing",
    ),
}
def remote_size(url):
    req = Request(url, method="HEAD", headers={"User-Agent": "SymC-DMDE/1.0"})
    with urlopen(req, timeout=60) as r:
        value = r.headers.get("Content-Length")
    if value is None:
        raise RuntimeError(f"missing Content-Length: {url}")
    return int(value)

lines = MANIFEST.read_text(encoding="utf-8").splitlines()
prov = json.loads(PROV.read_text(encoding="utf-8"))

for key, (member, rel) in TARGETS.items():
    prefix = rel + "/"
    matches = {}
    for line in lines:
        if "  " not in line:
            continue
        digest, path = line.split(None, 1)
        if path.startswith(prefix):
            name = path[len(prefix):]
            if "/" not in name:
                matches[name] = digest
    required = {
        "chain.1.txt", "chain.2.txt", "chain.3.txt", "chain.4.txt",
        "chain.input.yaml", "chain.updated.yaml", "chain.covmat",
        "chain.checkpoint",
    }
    missing = sorted(required - set(matches))
    if missing:
        raise RuntimeError(f"{key}: manifest missing {missing}")
    files = {}
    for name, digest in sorted(matches.items()):
        url = f"{BASE}/{rel}/{name}"
        files[name] = {"sha256": digest, "bytes": remote_size(url)}

    expected = prov["de_comparator_suite"]["members"][member]["chain_bytes"]
    got = [files[f"chain.{i}.txt"]["bytes"] for i in range(1, 5)]
    if got != expected:
        raise RuntimeError(f"{key}: chain-size identity mismatch {got} != {expected}")

    prov["chain_sets"][key] = {
        "scientific_role": f"physical_dark_energy_sensitivity_suite_member_{member}",
        "model": "base_w_wa",
        "relative_directory": rel,
        "files": files,
        "full_chain_bytes": sum(got),
        "note": (
            "One member of the frozen three-supernova sensitivity suite. "
            "No member is primary and no member may be selected by outcome."
        ),
    }

prov["de_comparator_suite"]["status"] = "sha256_receipts_pinned_runner_ready"
prov["de_comparator_suite"]["rule"] = (
    "Report whether the dark-energy inference is shared across Pantheon+, "
    "Union3 and DESY5, subset-only, or materially supernova-sample-dependent; "
    "do not select a supernova sample by outcome."
)
PROV.write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: prov["chain_sets"][k] for k in TARGETS}, indent=2))