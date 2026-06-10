# Majorana Hamiltonian Page Results

## Question

Can we replace the random Clifford/Floquet dynamics with a genuine
time-independent Hamiltonian on the deterministic algebraic expander graph?

This is the next naturalness target after fixing the graph.

## Script

```text
sim/majorana_hamiltonian_page.py
```

Outputs:

```text
sim/data/majorana_hamiltonian_page_*.csv
```

## Model

Use the deterministic Margulis/Gabber-Galil-style graph from the algebraic
expander test.

Put one fermionic mode on each graph vertex and evolve a pure Gaussian state
with a quadratic Majorana Hamiltonian:

```text
H = (i/4) sum_ab A_ab gamma_a gamma_b.
```

Two couplings were tested:

```text
hopping:
  number-conserving edge hopping.

generic:
  generic quadratic Majorana couplings on graph edges, including pairing-like
  terms.
```

At each shell step:

```text
1. evolve the remaining active droplet under the restricted Hamiltonian;
2. move the outer shell into radiation;
3. compute Gaussian entropies from the covariance matrix.
```

This is a real Hamiltonian test, but it is an integrable/free Hamiltonian test.

## Results

Five seeds were run for each baseline case.

```text
case                                      mean total deficit   max total deficit
hopping L0=8,  warmup 4, cycle 1              67.928              67.928
hopping L0=8,  warmup 8, cycle 2              67.928              67.928
generic L0=8,  warmup 4, cycle 1              17.464              17.822
generic L0=8,  warmup 8, cycle 2              17.512              17.671
generic L0=12, warmup 4, cycle 1              60.487              61.134
```

Here:

```text
total deficit = sum over shell steps max(0, S_Page_capacity - S_rad).
```

The hopping case fails trivially for the vacuum initial state, because
number-conserving evolution does not create excitations from the vacuum.

The generic quadratic Majorana Hamiltonian does create entanglement, but it
does not saturate the Page-capacity curve.

## Time Scan

For `L0 = 8`, generic Majorana coupling was scanned over:

```text
warmup time = 1, 2, 4, 8, 16, 32
cycle time  = 0.25, 0.5, 1, 2, 4, 8, 16
```

The best cases still had:

```text
mean total deficit ~= 17.1 nats.
```

So the failure is not just a bad time choice.

Representative best-ish case:

```text
generic L0=8, warmup 16, cycle 8, seed 0

L->L'   rad  rem   capacity   S_rad   deficit   I(old:new)
8->7     15   49    10.397    8.559    1.838      0.000
7->6     28   36    19.408   12.292    7.117      3.938
6->5     39   25    17.329   11.749    5.580      7.273
5->4     48   16    11.090    9.074    2.016      8.259
4->3     55    9     6.238    5.622    0.616      7.953
3->2     60    4     2.773    2.715    0.057      6.225
2->1     63    1     0.693    0.693    0.000      4.070
1->0     64    0     0.000    0.000   -0.000      1.386
```

The entropy is below the Page bound during the important middle part of the
evaporation.

The old/new mutual information also turns on too early:

```text
generic Majorana:
  first MI often appears at L = 7 -> 6 for L0 = 8.

Page crossing:
  expected around L = 6 -> 5 for L0 = 8.
```

## Interpretation

This is a useful negative result.

The deterministic algebraic expander graph by itself is not enough.

```text
sparse nonlocal connectivity:
  necessary or helpful for fast spreading;

quadratic/free Hamiltonian dynamics:
  not enough to reproduce Page-typical shell evaporation.
```

The Clifford/Floquet expander worked because it generated much more typical
many-body scrambling. A free Majorana Hamiltonian remains too structured.

## Consequence for the Program

This narrows the next target.

We should not merely ask for:

```text
a Hamiltonian on an expander graph.
```

We need:

```text
an interacting chaotic Hamiltonian on an expander-like graph.
```

Candidate next tests:

```text
1. small exact diagonalization of interacting spins on the algebraic graph;
2. random sparse k-local Hamiltonian on the algebraic graph;
3. Clifford circuit as the scalable proxy, plus a small non-Clifford Hamiltonian
   check for chaos/scrambling.
```

## Status

F14 remains:

```text
P
```

but the reason is now sharper.

The graph naturalness problem is mostly addressed at circuit level. The
dynamics naturalness problem is not solved by free Hamiltonians.
