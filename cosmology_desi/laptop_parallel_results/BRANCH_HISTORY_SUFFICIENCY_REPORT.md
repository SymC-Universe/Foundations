# Branch-History Sufficiency Audit

The root-count class was already found to be exactly redundant with sign(q0).
This audit asks whether branch locations retain history beyond present state,
and whether that history is absorbed by the native CPL parameter wa.

## branch_separation

q0 only held-out R2: 0.44040160
q0 + zchi held-out R2: 0.44534720
q0 + wa held-out R2: 0.50069961
Omega_m + w0 held-out R2: 0.82073950
Omega_m + w0 + wa held-out R2: 0.91820498
native quadratic held-out R2: 0.99334947

Increment from adding wa to q0: 0.06029802
Increment from adding wa to present native variables: 0.09746547

## recent_minus_chi

q0 only held-out R2: 0.71801892
q0 + zchi held-out R2: 0.95572363
q0 + wa held-out R2: 0.84703895
Omega_m + w0 held-out R2: 0.86592067
Omega_m + w0 + wa held-out R2: 0.97044269
native quadratic held-out R2: 0.99862891

Increment from adding wa to q0: 0.12902003
Increment from adding wa to present native variables: 0.10452202

## earlier_minus_chi

q0 only held-out R2: 0.34071728
q0 + zchi held-out R2: 0.74349463
q0 + wa held-out R2: 0.91647350
Omega_m + w0 held-out R2: 0.33646514
Omega_m + w0 + wa held-out R2: 0.93129561
native quadratic held-out R2: 0.99543883

Increment from adding wa to q0: 0.57575622
Increment from adding wa to present native variables: 0.59483047

## Interpretation

The branch geometry contains history that q0 alone discards, but the history is almost completely recovered by the native CPL variables once modest nonlinearity is allowed. This supports using branch geometry as a descriptive compression of native model history, but does not support treating it as an independent cosmological degree of freedom.
