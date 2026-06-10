# Interacting Spin Hamiltonian Page Results

## Question

The free Majorana Hamiltonian on the deterministic algebraic graph failed to
produce Page-typical shell evaporation.

The next question is:

```text
Does an interacting spin Hamiltonian on the same algebraic graph do better?
```

This tests whether the missing ingredient is genuine many-body chaos rather
than connectivity alone.

## Scripts

Exact sparse exponential, small default:

```text
sim/interacting_spin_hamiltonian_page.py
```

Trotterized interacting spin evolution, main diagnostic:

```text
sim/interacting_spin_trotter_page.py
```

Outputs:

```text
sim/data/interacting_spin_page_*.csv
sim/data/interacting_spin_trotter_page_*.csv
```

## Model

Use qubits on the deterministic Margulis/Gabber-Galil-style algebraic graph.

The interacting spin Hamiltonian is:

```text
H = sum_i (h_x,i X_i + h_z,i Z_i)
  + sum_(ij in E) (J_x,ij X_i X_j + J_y,ij Y_i Y_j + J_z,ij Z_i Z_j).
```

Two versions were tested:

```text
random_heisenberg:
  random fields and random edge couplings.

deterministic:
  fixed quasirandom-looking couplings generated from vertex labels.
```

The main `L0 = 4` runs use a Trotterized Hamiltonian evolution. This is not a
random Clifford circuit. It is an interacting spin dynamics approximating the
Hamiltonian above.

## Results: Trotterized L0 = 4

Five seeds were run for each case.

```text
case                                      mean total deficit   max total deficit
random_heisenberg warmup 4,  cycle 1          0.169               0.214
random_heisenberg warmup 8,  cycle 2          0.168               0.217
random_heisenberg warmup 12, cycle 3          0.163               0.207
deterministic     warmup 8,  cycle 2          0.227               0.368
```

Here:

```text
total deficit = sum over shell steps max(0, S_Page_capacity - S_rad).
```

These deficits are small. The interacting spin Hamiltonian nearly saturates the
Page-capacity curve at this size.

Representative run:

```text
random_heisenberg L0=4, warmup 12, cycle 3, seed 0

L->L'   rad  rem   capacity   S_rad   deficit   I(old:new)
4->3      7    9     4.852    4.723    0.129      0.000
3->2     12    4     2.773    2.770    0.003      5.409
2->1     15    1     0.693    0.693    0.000      4.156
1->0     16    0     0.000    0.000    0.000      1.386
```

For `L0 = 4`, the Page crossing is around:

```text
L ~= 4 / sqrt(2) ~= 2.8,
```

so the old/new mutual information turning on at:

```text
L = 3 -> 2
```

is the expected discrete location.

## Exact Sparse Exponential Check

The exact sparse exponential script is expensive at `L0 = 4`, so the default
check is `L0 = 3`.

Two seeds:

```text
random_heisenberg L0=3:
  mean total deficit = 0.370

deterministic L0=3:
  mean total deficit = 0.460
```

This is only a tiny-size sanity check, but it is consistent with the Trotter
result: interacting spin dynamics performs much better than the free Majorana
Hamiltonian.

## Comparison with Majorana Failure

Free Majorana on the same algebraic graph:

```text
generic Majorana L0=8:
  best scanned total deficit ~= 17.1 nats.
```

Interacting spin Trotter at `L0 = 4`:

```text
random Heisenberg:
  total deficit ~= 0.16-0.17 nats.
```

The sizes are not directly comparable, but the qualitative distinction is
clear:

```text
free/integrable dynamics:
  too structured;

interacting spin dynamics:
  close to Page-typical at accessible size.
```

## Interpretation

This is the first positive Hamiltonian-like F14 result.

It suggests that the right fast-scrambling module is:

```text
deterministic algebraic expander graph
plus
interacting chaotic spin dynamics.
```

That is much cleaner than:

```text
fresh random Haar/isometry at each shell.
```

It is also less black-hole-adjacent than SYK.

## Caveats

The result is still limited.

```text
1. L0 = 4 is small.
2. The main run is Trotterized, not an exact continuous-time exponential.
3. Random couplings remain in the strongest case.
4. Shell erosion is still an external update rule.
```

But the failure mode moved:

```text
we are no longer stuck at "can any Hamiltonian-like dynamics do this?"
```

The answer appears to be yes, at least at small size.

## Status

F14 remains:

```text
P
```

but stronger than before.

The next useful tests are:

```text
1. scan more deterministic coupling patterns;
2. try slightly larger approximate/tensor simulations;
3. check chaos diagnostics for the same Hamiltonian;
4. integrate this Hamiltonian-like scrambling module with the thermodynamic
   multi-cycle tracker at the level of assumptions.
```
