# Fresh c1-corrected displacement-map test v0.1 result

Status: `SELECTION_HOLD`

Canonical run: `33266791185`
Execution commit: `357054975733e9443a322c240f549e467dada029`
Artifact: `9718882791`
Artifact ZIP SHA-256: `dd359f0097f8023e54bcee5c8eebd84ab394bd0b8ca67051a35429f453301075`

## Frozen design

Fresh seed `2026082912` generated exactly 500000 broad measured-qubit candidates. Stage A was allowed to use only the exact physical/record c3 quadratics and the separately derived exact physical c1 formula. No A, B, G, c2, final Hurwitz margin, eigenvalue, or full class was available before the selection was frozen.

The registered corrected destabilizing class required robust `I_destab` plus `c1_phys/R > 1e-8`. The opposite `I_stab` class was retained as a fresh replication lane.

## Result

Stage-A available counts:

- `I_destab_c1`: `0`;
- `I_stab`: `90161`.

Because the preregistration required at least 128 cases in both classes, the scientific phase returned `SELECTION_HOLD` before Stage B scoring.

No H7D PASS or FAIL is licensed. The printed H7S precision value in the implementation is not a scientific result because the overall preregistered selection requirement failed and Stage B scientific scoring was not admissible.

The candidate selection, hashes, and empty corrected-destabilizing set are preserved as evidence.

## Immediate interpretation

This result says only that the registered broad state generator, whose Bloch radius was restricted to `r in [0.05,0.98]`, produced no robust `I_destab` cases with positive physical c1 in 500000 draws.

It does not establish that such cases are impossible in the measured-qubit model. Prior independently preserved target-family crossings occupy a different, near-pure-state sampling geometry. That distinction requires a fresh geometry-stratified audit rather than more draws from the same truncated radial frame.
