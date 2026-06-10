# Integrated Droplet Evaporator Results

## Question

Can the pieces be fused into one effective droplet evaporator?

The integrated model combines:

```text
boundary-tension equation of state
local scrambling before shell removal
shell-as-radiation erosion
hard energy-bin coarse-graining
Page and early/late diagnostics
```

## Script And Data

Script:

```text
sim/integrated_droplet_evaporator.py
```

Main data:

```text
sim/data/integrated_droplet_evaporator_summary.csv
sim/data/integrated_droplet_evaporator_timeseries.csv
sim/data/integrated_droplet_evaporator_thermo.csv
sim/data/integrated_droplet_evaporator_depth8_summary.csv
sim/data/integrated_droplet_evaporator_depth8_timeseries.csv
sim/data/integrated_droplet_evaporator_depth8_thermo.csv
```

## Model

Droplet:

```text
q = 2
L0 = 4
initial dimension = 2^(L0^2) = 65536
```

Equation of state:

```text
area A_L = L^2
perimeter P_L = 4L
core energy E_L = sigma P_L
entropy S_L = A_L log q
```

Therefore:

```text
S(E) = (log q / 16 sigma^2) E^2
T_L = 2 sigma / (L log q)
C_L < 0
```

Erosion:

```text
H_L = H_(L-1) tensor H_shell(L)
dim H_shell(L) = 2^(2L - 1)
```

The removed shell is the outgoing radiation factor:

```text
H_shell(L) -> R_out(L)
```

Hard radiation is an energy-bin coarse-graining of `R_out(L)`. The bin
dimensions approximate:

```text
P(x) proportional to x^p exp(-x)
x = beta omega
```

Scrambling:

Before each shell removal, the current core qubits are scrambled by a depth-`d`
random two-qubit circuit. Three circuit geometries are tested:

```text
grid:
  nearest-neighbor layers on the square droplet

expander:
  sparse long-range expander-like pairings

random:
  random pair matchings
```

Controls:

```text
none:
  no scrambling

basis:
  one basis initial state

flat:
  equal-amplitude product-like initial state

haar:
  Haar-typical initial state benchmark
```

## Thermodynamics

For the `L = 4,3,2` shells:

```text
L  area  perimeter  energy  entropy  temperature  heat capacity  E^2 P
4  16    16         16      11.090   0.721       -22.181        1537.424
3   9    12         12       6.238   0.962       -12.477        1537.424
2   4     8          8       2.773   1.443        -5.545        1537.424
```

The proxy:

```text
P_2d ~ perimeter * T^3
```

has:

```text
E^2 P_2d = constant
```

so the effective power law is:

```text
P ~ E^-2
```

within the boundary-tension droplet thermodynamics.

## Depth-4 Result

The first integrated run used circuit depth `4`.

No-scramble controls:

```text
state  scrambler  Srad_final  hardTV  max I(E:L)
basis  none       0.000       0.910   0.000
flat   none       0.000       0.120   0.000
```

This separates the diagnostics:

```text
basis/no-scramble:
  fails hard thermality and information flow

flat/no-scramble:
  has decent hard thermality but fails information flow
```

Scrambled basis states:

```text
state  scrambler  Srad_final  Page_est  hardTV  max I(E:L)
basis  grid       0.693       0.693     0.143   4.221
basis  expander   0.693       0.693     0.151   4.245
basis  random     0.693       0.693     0.140   4.440
```

So even moderate scrambling turns a basis initial state into a Page-like
evaporation history.

## Depth-8 Result

Depth `8` gives a stronger integrated result.

Grouped over two seeds:

```text
state  scrambler  Srad_final  Page_est  hardTV  max I(E:L)
basis  grid       0.693       0.693     0.120   5.361
basis  expander   0.693       0.693     0.128   5.229
basis  random     0.693       0.693     0.120   5.389
flat   grid       0.693       0.693     0.121   5.329
flat   expander   0.693       0.693     0.121   5.331
flat   random     0.693       0.693     0.120   5.385
```

For `basis + grid`, seed `2468`, the time series is:

```text
step  L removed  S(rad)  Page est  hardTV  I(early:late)
1     4          4.669   4.727     0.018   0.000
2     3          2.770   2.771     0.098   5.357
3     2          0.693   0.693     0.242   4.156
```

The radiation entropy tracks the Page estimate, and early/late mutual
information appears once the remaining core becomes small.

## Interpretation

This is the first integrated effective droplet evaporator that clears the main
non-gravitational phenomenology checks in one model:

```text
1. S(E) ~ E^2 from area entropy plus perimeter energy.
2. T ~ 1/E and C < 0 from the same equation of state.
3. P ~ E^-2 from 2D boundary radiation scaling.
4. The shell factorization is geometric.
5. The removed shell is the outgoing radiation system.
6. Hard thermality is a coarse-graining of that radiation system.
7. Local/expander/random scrambling produces Page-like radiation entropy.
8. Early/late radiation correlations appear.
9. No-scrambling controls fail.
```

This is a real consolidation. It replaces several abstract ingredients with a
single effective droplet picture.

## Remaining Gaps

The model is still an effective shell-eroding model.

The two main remaining issues are:

```text
1. Energy-carrying hard radiation is represented by bin dimensions, not by an
   autonomous outgoing field or chain.

2. Shell removal is a discrete isometry, not yet generated by one autonomous
   Hamiltonian with an escaping radiation bath.
```

The next meaningful step is therefore:

```text
add an outgoing radiation chain / bath to the integrated droplet model, so
energy-carrying radiation propagates away while the shell factor supplies the
fine-grained outgoing state.
```

That is the correct next jump after integration. More shell bookkeeping would
have diminishing value.
