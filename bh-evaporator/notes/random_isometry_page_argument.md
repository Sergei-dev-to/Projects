# Random-Isometry Page Argument

## Question

Can the Page-style capacity curve in the many-cycle tracker be promoted from
bookkeeping to a quantum-information statement?

The cleanest conditional answer is yes:

```text
if each shrink step behaves like a sufficiently scrambling isometry, then the
usual Page theorem gives the radiation entropy and early/late correlations.
```

This does not derive the scrambling isometry from a local Hamiltonian. It says
exactly what has to be true for F8 and F9.

## Hilbert-Space Setup

For the finite-gauge droplet:

```text
dim H_L = q^(L^2).
```

One coarse shrink step has the exact dimension factorization:

```text
H_L ~= H_(L-1) tensor H_shell(L),
dim H_shell(L) = q^(2L - 1).
```

The random-isometry idealization is:

```text
V_L: H_L -> H_(L-1) tensor H_shell(L),
```

with `V_L` typical enough that a generic initial state becomes Page-typical
with respect to the remaining/internal split.

After shrinking from `L0` to `L`, the dimensions are:

```text
dim H_BH(L)  = q^(L^2),
dim H_rad(L) = q^(L0^2 - L^2).
```

So Page's theorem predicts:

```text
S_rad(L) ~= min(L^2, L0^2 - L^2) log q
```

up to the usual Page correction.

The turnover occurs at:

```text
L ~= L0 / sqrt(2).
```

That is the same crossing seen in the many-cycle tracker.

## Diagnostic Script

```text
sim/random_isometry_page_curve.py
```

Outputs:

```text
sim/data/random_isometry_page_curve_L40.csv
sim/data/random_isometry_page_curve_L80.csv
sim/data/random_isometry_shell_mi_L40.csv
sim/data/random_isometry_shell_mi_L80.csv
```

The script evaluates the asymptotic Page formula:

```text
<S_A> = H_(mn) - H_n - (m - 1)/(2n)
      ~= log m - m/(2n),
```

where:

```text
m = min(dim A, dim B),
n = max(dim A, dim B).
```

For these enormous droplet dimensions, the correction is negligible except at
an exactly balanced split. Because `L` is integer, the curve is almost exactly
the capacity curve.

## Results

For `L0 = 40`:

```text
crossing L = 28
radiated entropy fraction = 0.510000
peak Page entropy = 543.427390
```

For `L0 = 80`:

```text
crossing L = 57
radiated entropy fraction = 0.492344
peak Page entropy = 2184.106766
```

The slight offset around one half is just the integer shell spacing.

## Early/Late Radiation Correlations

To test F9, split the radiation after a step into:

```text
R_old = previously emitted radiation,
R_new = newly emitted shell record,
B     = remaining droplet.
```

For a typical pure state on:

```text
R_old tensor R_new tensor B,
```

estimate:

```text
I(R_old : R_new)
  = S(R_old) + S(R_new) - S(R_old R_new)
```

with the same Page formula.

The result:

```text
L0 = 40:
  first strong old/new mutual information at L = 28 -> 27

L0 = 80:
  first strong old/new mutual information at L = 57 -> 56
```

So the random-isometry model gives the expected qualitative behavior:

```text
before Page time:
  newly emitted radiation is almost independent of old radiation;

after Page time:
  newly emitted radiation is correlated with old radiation.
```

This is the standard Page-theorem mechanism. It does not need gravity.

## What This Buys Us

This upgrades the many-cycle capacity result into a conditional
quantum-information result:

```text
F8:
  Page-like radiation entropy follows from the finite droplet dimensions plus
  typical isometric shrinkage.

F9:
  early/late radiation correlations turn on after the same Page crossing.
```

But it is still conditional:

```text
the physical droplet dynamics must approximate these random isometries well
enough.
```

## What Remains Nontrivial

The random-isometry result is not yet a microscopic Hamiltonian derivation.

The remaining hard question is:

```text
Can a reasonably natural finite-gauge droplet Hamiltonian generate enough
scrambling during evaporation to justify the random-isometry approximation?
```

If yes, F8 and F9 can probably move from `P` to `Y`.

If no, the model still has the right thermodynamic trajectory, but the Page
behavior remains imposed through typicality rather than dynamically produced.

## Current Assessment

This is a meaningful step forward.

The Page curve is no longer just:

```text
we drew min(S_remaining, S_emitted).
```

It is now:

```text
given the exact sector dimensions, Page's theorem predicts that curve for
typical shrinkage isometries, and it also predicts the early/late correlation
turn-on.
```

The next step should not be another thermodynamic calculation. The next step is
to test or justify the scrambling/isometry assumption.
