# Hard/Soft Page Accounting Results

## Purpose

The global hard-density check showed that visible hard bins can be locally
thermal after hidden bath records are traced.

The reference-flow check showed that expelled shell information goes into the
soft/shrink record rather than the hard bin.

This test puts those two facts next to the Page diagnostic:

```text
soft shell records:
  fine-grained radiation degrees used for the Page curve.

hard bins:
  coarse local thermal observer record after hidden bath records are traced.
```

The goal is to avoid confusing coarse hard entropy with fine Page entropy.

## Setup

The soft sector uses the existing stabilizer shell Page diagnostic:

```text
L0 = 8
soft shell records are emitted as L -> L-1
Page capacity = min(soft radiation qubits, remaining core qubits)
```

The hard sector is added as observer entropy:

```text
3 hard emissions per shell
2 coarse hard bins per emission
S_hard += 3 ln 2 per shell
```

This hard entropy is the local coarse entropy of hard bins after hidden bath
records are traced. It is not counted as fine core-radiation entanglement.

Cases:

```text
grid       warmup=16 cycle=8
expander8  warmup=8  cycle=2
complete   warmup=8  cycle=2
```

Five seeds were run for each case.

## Result

For `grid` and `expander8`, all five seeds exactly match the Page capacity:

```text
total soft Page deficit = 0
peak soft entropy       = 28 qubits
final soft entropy      = 0
first old/new soft MI   = 6->5
final hard entropy      = 16.635532
```

For `complete`, four of five seeds exactly match and one seed has deficit 2:

```text
total soft Page deficit = 0,0,0,0,2
first old/new soft MI   = 6->5
final hard entropy      = 16.635532
```

Representative `expander8` trajectory:

```text
L  soft S_rad  Page cap  old/new MI  accumulated hard S
8      15          15        0             2.079
7      28          28        0             4.159
6      25          25       14             6.238
5      16          16       18             8.318
4       9           9       14            10.397
3       4           4       10            12.477
2       1           1        6            14.556
1       0           0        2            16.636
```

## Interpretation

The fine soft-radiation entropy follows the Page curve:

```text
grow before the Page crossing;
turn over;
return to zero when the core is gone.
```

The coarse hard-bin entropy is monotone:

```text
it keeps increasing as local thermal emissions are observed.
```

This is not a contradiction. They are different entropies.

The Page curve is a fine-grained entropy of the radiation subsystem in the
global pure state.

The hard-bin entropy is a coarse local entropy after tracing hidden bath and
soft/shrink records.

## Why This Matters

This clarifies the model's information-flow picture:

```text
hard radiation:
  locally thermal, monotone observer entropy;
  not where shell-label purification appears in the minimal diagnostic.

soft/shrink records:
  carry emitted shell information;
  supply the fine-grained radiation degrees for Page behavior.

scrambling:
  makes emitted shell records behave like typical radiation subsystems,
  producing Page-like entropy and old/new mutual information.
```

This is close to the conceptual separation we wanted:

```text
local Hawking-like thermality does not by itself diagnose information loss;
purification can live in correlations/records invisible to the coarse hard
observer.
```

## What This Strengthens

This strengthens the combined interpretation of:

```text
F8  Page-like radiation entropy
F9  early/late radiation correlations
F15 one repeated update architecture
```

It also prevents an overclaim:

```text
the hard thermal entropy is not the Page entropy.
```

## Remaining Gap

This still uses a hybrid accounting:

```text
stabilizer soft-shell Page dynamics
+ coarse hard entropy from the global hard-bin diagnostic.
```

The next stronger test would put both into one state-vector simulation:

```text
scrambled core
+ explicit hard bins
+ hidden bath records
+ soft/shrink records
+ many-cycle Page/old-new diagnostics.
```

That is the next real F8/F9/F14/F15 merger.

## Files

Script:

```text
sim/hard_soft_page_accounting.py
```

Data:

```text
sim/data/hard_soft_page_accounting_grid.csv
sim/data/hard_soft_page_accounting_expander8.csv
sim/data/hard_soft_page_accounting_complete.csv
sim/data/hard_soft_page_accounting_summary.csv
```
