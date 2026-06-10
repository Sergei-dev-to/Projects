# Shell-To-Radiation Isometry Results

## Question

Can shell erosion be modeled without a separate hidden soft archive?

The test here uses one outgoing radiation system per removed shell:

```text
H_L = H_{L-1} tensor H_shell(L)
H_shell(L) -> R_out(L)
```

Hard radiation is the energy-bin coarse-graining of `R_out(L)`. Fine-grained
information is the state inside the same outgoing radiation factor.

## Script And Data

Script:

```text
sim/shell_radiation_isometry.py
```

Data:

```text
sim/data/shell_radiation_isometry_timeseries.csv
sim/data/shell_radiation_isometry_summary.csv
```

## Model

For a square droplet:

```text
dim H_L = q^(L^2)
dim H_{L-1} = q^((L-1)^2)
dim H_shell(L) = q^(2L - 1)
```

The shell factorization is exact:

```text
q^(L^2) = q^((L-1)^2) q^(2L-1)
```

Each shell becomes one radiation factor:

```text
R_out(L) = H_shell(L)
```

The radiation factor is partitioned into hard energy bins:

```text
R_out(L) = direct sum_h R_h(L)
```

with integer bin dimensions chosen to approximate:

```text
P_h proportional to integral over bin_h of x^p exp(-x) dx
x = beta omega
```

There is no independent soft register. The fine-grained radiation state within
`R_out(L)` carries the purification data.

## Run

Default:

```text
q = 2
L0 = 4
Lmin = 1
steps: L = 4 -> 3 -> 2
initial dim = 2^16 = 65536
```

Initial state classes:

```text
haar:
  Haar-typical pure state on H_4

basis:
  one basis state

flat_product:
  equal-amplitude product-like state in the shell factorization
```

## Summary

```text
state          Srad_final  Page_est  hardTV  max I(E:L)
basis          0.000       0.693     0.910   0.000
flat_product   0.000       0.693     0.120   0.000
haar           0.693       0.693     0.120   5.414
```

`hardTV` is the mean total-variation distance between the latest shell's hard
energy-bin marginal and the target thermal bin distribution.

`I(E:L)` is the mutual information between earlier and later radiation shell
factors.

## Haar-Typical State

For seed `2468`:

```text
step  removed L  core dim  rad dim  S(core)=S(rad)  Page estimate  hard TV
1     4          512       128      4.727           4.727          0.019
2     3          16        4096     2.771           2.771          0.097
3     2          2         32768    0.693           0.693          0.244
```

Radiation entropy follows the Page estimate for the changing core/radiation
factor dimensions.

Early/late mutual information:

```text
step  S(early)  S(late)  S(early+late)  I(early:late)
1     0.000     4.727    4.727          0.000
2     4.727     3.458    2.771          5.414
3     2.771     2.079    0.693          4.157
```

This is the desired Page-like information pattern at the factor/isometry level:
early and late radiation become strongly correlated after the remaining core
dimension becomes small.

## Controls

### Basis state

The basis state has:

```text
S(rad) = 0
I(early:late) = 0
hardTV about 0.91
```

It fails both information flow and hard thermality.

### Flat product state

The flat product state has:

```text
S(rad) = 0
I(early:late) = 0
hardTV about 0.12
```

It can look fairly thermal in hard-bin measurements while carrying no
fine-grained radiation entanglement. This is an important warning:

```text
hard thermality alone is too weak.
```

The useful diagnostic package must include the fine-grained radiation entropy
and early/late correlations.

## Interpretation

This is a cleaner erosion model than a hard-plus-soft register split.

The outgoing radiation factor itself carries both:

```text
hard data:
  energy-bin marginal

fine-grained data:
  microstate within the outgoing shell/radiation factor
```

So the model avoids a separate hidden archive. The removed shell is the
radiation.

The result also clarifies the role of scrambling/typicality:

```text
Haar-typical shell/core states produce hard thermality, Page-like radiation
entropy, and early/late correlations.

Unentangled product-like states can satisfy one diagnostic while failing the
others.
```

## Remaining Gap

This is still an isometry/factorization diagnostic. The next dynamical task is
to produce the required typical shell states from an actual core Hamiltonian:

```text
intra-droplet scrambling before shell erosion
```

and then combine it with an energy-carrying radiation channel.

The current result gives a better target for that dynamics because the outgoing
system is now a single radiation factor with hard measurements as a
coarse-graining.
