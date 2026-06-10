# Microscopic Golden Boundary Emission Results

## Question

Merge the three separate ingredients:

```text
1. golden-rule hard weights from the droplet entropy curve;
2. boundary microscopic emissions;
3. hard/soft information-flow diagnostic.
```

The goal is to remove the artificial fixed hard probability used in the first
microscopic boundary-emission test.

## Script

The existing script was upgraded:

```text
sim/microscopic_boundary_emission.py
```

It now supports:

```text
--weight-model golden
--weight-model fixed
```

The default is:

```text
--weight-model golden
```

Golden weights use two hard bins in:

```text
x = beta omega.
```

Default bins:

```text
x_edges = 0, 2, 8.
```

For each event, the hard-bin probabilities are computed from:

```text
d Gamma ~ omega^(d-1) exp[S(M - omega) - S(M)] d omega.
```

The mean emitted energy is then subtracted from the effective mass for the next
event.

## Run

Default single-seed smoke run:

```text
python sim/microscopic_boundary_emission.py
```

Eight-seed ensemble runs were split by variant to avoid memory/thread pressure:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python sim/microscopic_boundary_emission.py \
  --variants local --n-bulk 4 --n-events 3 --seeds 8 \
  --out sim/data/microscopic_boundary_emission_golden_local.csv \
  --summary-out sim/data/microscopic_boundary_emission_golden_local_summary.csv

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python sim/microscopic_boundary_emission.py \
  --variants scrambled --n-bulk 4 --n-events 3 --seeds 8 \
  --out sim/data/microscopic_boundary_emission_golden_scrambled.csv \
  --summary-out sim/data/microscopic_boundary_emission_golden_scrambled_summary.csv
```

The no-scrambling branch is deterministic and was run with one seed:

```text
python sim/microscopic_boundary_emission.py \
  --variants none --n-bulk 4 --n-events 3 --seeds 1 \
  --out sim/data/microscopic_boundary_emission_golden_none.csv \
  --summary-out sim/data/microscopic_boundary_emission_golden_none_summary.csv
```

## Golden Weights

For:

```text
L0 = 20
q = 2
sigma = 1
2D bath
```

the event weights were:

```text
event 1: p1 = 0.4065, <omega>/T = 1.9878
event 2: p1 = 0.4066, <omega>/T = 1.9879
event 3: p1 = 0.4066, <omega>/T = 1.9879
```

So the hard probabilities are no longer chosen by hand. They come from the
same entropy-ratio calculation that gave the power law.

## Result

After three microscopic emissions:

```text
variant      D_hard   I(R:hard_all)   I(R:pair_all)   I(R:bulk)
none         0.0000      0.0000          1.3863        4.1589
local        0.0000      0.0000          2.5099        3.0353
scrambled    0.0000     -0.0000          2.9261        2.6191
```

The hard entropy changed because the hard-bin distribution changed:

```text
S_latest_hard = 0.6756
```

instead of the previous fixed-probability value:

```text
S_latest_hard = 0.5623.
```

But the information-flow pattern is unchanged:

```text
hard radiation alone stays locally thermal;
hard radiation alone carries essentially no reference information;
hard+soft records carry reference information out;
scrambling controls how much bulk information reaches the boundary.
```

## Interpretation

This is a real merge of the previous diagnostics.

Before:

```text
the information-flow channel had fixed hard probabilities.
```

Now:

```text
the information-flow channel uses hard probabilities derived from the
microcanonical droplet entropy curve and bath density of states.
```

That strengthens the case that the boundary-emission picture is not just a
stack of unrelated toy assumptions.

## What Still Remains Artificial

The diagnostic is still not one autonomous Hamiltonian.

Still inserted:

```text
hard/soft isometry;
soft record dimension;
bulk-to-boundary mixing rule;
two hard energy bins;
coarse mass update by mean emitted energy.
```

Also, with only three microscopic emissions and four bulk qubits, this is not a
Page-curve calculation. It is an information-flow compatibility test.

## F1-F13 Impact

This mainly strengthens partial entries:

```text
F7:
  hard probabilities in the microscopic information channel are now
  golden-rule weights, not fixed by hand.

F8:
  radiation entropy bookkeeping remains compatible with derived hard weights.

F9:
  reference information still appears in hard+soft records, not hard marginals.

F13:
  boundary-port emission plus local/scrambled bulk dynamics now tests the
  boundary-local route more directly.
```

No entry should become a clean `Y` yet.

## Next Missing Link

The next genuine upgrade would be:

```text
replace the hard/soft isometry with a finite Hamiltonian coupling:

bulk boundary port + soft boundary mode + bath mode
```

whose weak-coupling/golden-rule limit produces the same channel.

That would connect:

```text
F2: unitary microscopic evaporation
F7: rates from matrix elements
F8/F9: information flow
F13: boundary-local emission
```

in one construction.
