# Fused Floquet Page Probe Results

## Purpose

Probe the Page-like entropy trajectory inside the fused Floquet model.

This addresses the remaining review gap:

```text
the final fused model should show more than a soft entropy gap and old/new
mutual information; it should show a radiation-entropy rise and turnover.
```

## Setup

Script:

```text
sim/fused_floquet_page_probe.py
```

Data:

```text
sim/data/fused_floquet_page_probe.csv
```

Parameters:

```text
L0 = 3
rate L0 = 20
threshold = 4
emission counts = 2, 4, 6, 8
scramblers = margulis, none
seed = 0
hard weights = microcanonical/golden-rule schedule
```

The threshold `4` case is used because the robustness scan showed it produces
enough shrinkage over a short trajectory to make old/new and turnover behavior
visible.

## Result

```text
scrambler  emissions  S_full_rad  S_core_acc  S_soft  I_old:new  <shells>
margulis       2        1.427       1.427      0.859     0.609     0.165
margulis       4        3.799       3.799      3.428     1.645     1.027
margulis       6        2.612       2.612      2.915     4.755     1.781
margulis       8        1.900       1.900      2.877     6.778     2.421

none           2        1.017       1.017      0.448     0.609     0.165
none           4        1.384       1.384      0.992     1.520     1.027
none           6        1.592       1.592      1.829     2.029     1.781
none           8        1.698       1.698      2.478     2.404     2.421
```

`S_full_rad` is the von Neumann entropy of the full radiation subsystem:

```text
hard records + hidden bath purifier records + time-resolved soft records.
```

Because the global state is pure, this equals the entropy of the remaining
core/accumulator subsystem in the exact diagnostic.

## Interpretation

The scrambled fused run shows a Page-like turnover:

```text
S_full_rad:
  1.427 -> 3.799 -> 2.612 -> 1.900.
```

The no-scrambling run does not show the same turnover over this window:

```text
S_full_rad:
  1.017 -> 1.384 -> 1.592 -> 1.698.
```

This is the desired qualitative pattern:

```text
scrambling + shrinking core capacity:
  radiation entropy rises and then falls;

no scrambling:
  radiation entropy grows more weakly and does not show the same Page-like
  turnover in the probed window.
```

The old/new mutual information also grows strongly in the scrambled run:

```text
I_old:new:
  0.609 -> 1.645 -> 4.755 -> 6.778.
```

## What This Closes

This improves the Page-like entropy status from:

```text
separate Page-like diagnostics plus fused soft entropy gaps
```

to:

```text
an explicit small fused-model radiation entropy rise and turnover.
```

## Remaining Limits

This is still a small exact diagnostic:

```text
one seed;
threshold = 4 only;
emission counts only up to 8;
L0 = 3;
two-bin hard alphabet;
rate L0 separated from exact L0.
```

It should be read as a proof-of-concept fused Page probe, not as a robust
large-system Page curve.

