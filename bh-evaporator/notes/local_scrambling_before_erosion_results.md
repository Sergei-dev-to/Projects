# Local Scrambling Before Erosion: First Results

## Purpose

Test whether the product-state failures in the erosion channel can be repaired
by local plaquette-flux dynamics before each shell is emitted.

This is the practical version of:

```text
the shell should become locally mixed before erosion.
```

## Script

```text
sim/local_scrambling_before_erosion.py
```

Outputs:

```text
sim/data/local_scrambling_before_erosion.csv
sim/data/local_scrambling_before_erosion_summary.csv
sim/data/local_scrambling_before_erosion_L4check.csv
sim/data/local_scrambling_before_erosion_L4check_summary.csv
```

Main run:

```text
python sim/local_scrambling_before_erosion.py --seeds 4
```

Larger spot check:

```text
python sim/local_scrambling_before_erosion.py --seeds 1 --include-L4 \
  --out sim/data/local_scrambling_before_erosion_L4check.csv \
  --summary-out sim/data/local_scrambling_before_erosion_L4check_summary.csv
```

## Setup

The droplet is represented as `L0^2` plaquette-flux `q`-dits ordered by square
shells:

```text
shell L has 2L - 1 plaquettes.
```

Before each erosion step, the current `L x L` plaquette grid is evolved by a
nearest-neighbor local random circuit of depth:

```text
D = 0, 1, 2, 4, 8.
```

Two local scramblers were tested:

```text
generic:
  Haar-random two-qdit gates on neighboring plaquettes.

flux_conserving:
  two-qdit gates block diagonal in total flux mod q.
```

The erosion channel is then one of:

```text
shift_minimal
clock_minimal
```

The important initial states are the ones that previously exposed failures:

```text
basis_all
uniform_all
factor_haar
```

## Main Result

Local scrambling repairs the initial-state dependence.

At depth zero, the known basis-dependence appears:

```text
basis_all + clock:
  fails;

uniform_all + shift:
  fails;

factor_haar:
  only moderately close to thermal.
```

After a small amount of local mixing:

```text
D = 1:
  most failures are strongly reduced;

D = 4:
  hard radiation is close to thermal in all tested cases;
  hard+soft early/late correlations become nonzero.
```

This holds for both generic local gates and the stricter flux-conserving local
gates.

## Representative `L0 = 3`, `d_hard = 2` Numbers

Previously failing case:

```text
initial      scrambler        channel  D  maxD   I_pair  S_h/thermal
basis_all    flux_conserving  clock    0  0.443   0.000  0.000/0.582
basis_all    flux_conserving  clock    1  0.147   2.804  0.559/0.582
basis_all    flux_conserving  clock    4  0.021   3.864  0.582/0.582

uniform_all  flux_conserving  shift    0  0.443   0.000 -0.000/0.582
uniform_all  flux_conserving  shift    1  0.114   1.765  0.561/0.582
uniform_all  flux_conserving  shift    4  0.041   3.822  0.581/0.582
```

For `d_hard = 3`, the same pattern holds:

```text
initial      scrambler        channel  D  maxD   I_pair  S_h/thermal
basis_all    flux_conserving  clock    0  0.546   0.000  0.000/0.832
basis_all    flux_conserving  clock    4  0.032   3.864  0.830/0.832

uniform_all  flux_conserving  shift    0  0.546  -0.000  0.000/0.832
uniform_all  flux_conserving  shift    4  0.043   3.822  0.830/0.832
```

## `L0 = 4` Spot Check

The one-seed `L0 = 4` check is consistent and cleaner.

For `d_hard = 2`:

```text
initial      scrambler        channel  D  maxD   I_pair  S_h/thermal
basis_all    flux_conserving  clock    0  0.443   0.000  0.000/0.582
basis_all    flux_conserving  clock    4  0.003   2.654  0.582/0.582

uniform_all  flux_conserving  shift    0  0.443  -0.000  0.000/0.582
uniform_all  flux_conserving  shift    4  0.009   2.617  0.582/0.582

factor_haar  generic          clock    0  0.342  -0.000  0.297/0.582
factor_haar  generic          clock    4  0.006   2.670  0.582/0.582
```

The local circuit drives the shell entropy up and the shell purity down before
erosion. In the `L0 = 4` depth-4 cases:

```text
mean shell entropy ~ 3.4
mean shell purity  ~ 0.056
```

which is close to the locally mixed shell behavior seen in the earlier
Haar/outer-maxmix tests.

## Interpretation

The erosion channel itself does not thermalize arbitrary states.

But it does not require global Haar scrambling either.

A modest-depth local circuit on neighboring plaquette-flux variables is enough
to make the outer shell locally mixed, after which the structured shift/clock
erosion maps produce:

```text
thermal-looking hard radiation;
nonzero hard+soft early/late correlations;
nearzero hard-only early/late correlations.
```

The flux-conserving local circuit is important because it shows the effect does
not rely only on completely unconstrained two-site gates.

## Naturalness Assessment

This improves the model, but it is still a circuit diagnostic.

What is better:

```text
scrambling is local on the plaquette grid;
the circuit acts before erosion rather than hiding information in the erosion
map itself;
the flux-conserving variant respects a simple constrained-sector structure.
```

What remains imposed:

```text
the local gates are random gates, not generated by one fixed Hamiltonian;
the circuit depth is chosen externally;
the flux-conserving condition is only a toy proxy for true gauge-local
dynamics.
```

So the current status is:

```text
local constrained scrambling is sufficient in small exact tests.
```

Not yet:

```text
a specific natural Hamiltonian produces the scrambling.
```

## Consequence For The Program

This is a meaningful improvement over assuming a scrambled initial state.

The needed assumption is now narrower:

```text
the constrained droplet has ordinary local chaotic dynamics fast enough to mix
the next shell before it erodes.
```

That is plausible because the one-shell erosion time scales as:

```text
t_shell ~ R^2.
```

The next step is therefore clear:

```text
replace the random local circuit with a fixed local constrained Hamiltonian or
Floquet gate set, then repeat the same depth/erosion diagnostic.
```

