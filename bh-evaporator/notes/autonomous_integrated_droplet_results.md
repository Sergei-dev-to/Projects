# Autonomous Integrated Droplet: First Result

## Question

Can we replace the staged synthetic evaporation rule with one time-independent Hamiltonian that contains the droplet, the emitted radiation, and the erosion channel in the same Hilbert space?

The answer is yes. We can now write and simulate such a Hamiltonian. A short radiation chain gives only partial shrinkage. Enlarging the outgoing radiation waveguide gives robust autonomous two-shell evaporation in the current `L0 = 3` test.

## Hilbert space

For an initial square droplet of side length `L0`, the model uses staged sectors

```text
stage 0: H_L0
stage 1: H_(L0-1) tensor R_L0
stage 2: H_(L0-2) tensor R_L0 tensor R_(L0-1)
...
```

Each stage is a different factorization of the same original droplet information. The core dimension is

```text
dim H_L = q^(L^2)
```

and the already-emitted shell register has the complementary dimension. The hard radiation is an occupation chain. In the current exact simulation the chain supports up to `L0 - Lmin` emitted hard quanta. Increasing the chain length increases the available outgoing phase space and delays coherent return to the droplet.

## Hamiltonian

The simulated Hamiltonian is

```text
H_total = H_drop + H_hard + H_hop + H_scr + H_erosion .
```

The pieces are:

```text
H_drop:
  boundary-tension energy E_L = 4 sigma L

H_hard:
  one hard-radiation quantum costs omega = 4 sigma

H_hop:
  emitted hard quanta hop along the radiation chain

H_scr:
  sparse random Hermitian intra-core mixing inside each fixed droplet stage

H_erosion:
  couples stage L to stage L-1 and creates one hard quantum at the emission site
```

The default choice `omega = 4 sigma` makes one shell-eroding transition resonant:

```text
E_L = E_(L-1) + omega .
```

This removes the earlier detuning problem where the Hamiltonian had an erosion operator but did not actually transfer much amplitude.

## What changed from the previous autonomous test

The previous script allowed only one hard excitation. After one erosion event, further evaporation was structurally blocked. The current version uses hard-chain occupation states, so repeated erosion events are present in the Hilbert space.

The current version also uses sparse intra-core scrambling. Dense scrambling was useful for small smoke tests and scales poorly once the hard-radiation waveguide is enlarged.

This is the relevant file:

```text
sim/autonomous_integrated_droplet.py
```

## Numerical runs

### Two-shell short-chain run

Parameters:

```text
L0 = 3
Lmin = 1
q = 2
chain length = 5
max hard quanta = 2
omega = 4 sigma
```

Moderate erosion coupling:

```text
erosion coupling = 0.12
chain hopping = 0.8

dimension = 24576
final mean L = 2.448
final hard energy = 2.210
final-sector probability = 0.039
Hamiltonian energy drift = 1.44e-13
```

Stronger erosion coupling:

```text
erosion coupling = 0.50
chain hopping = 1.2

dimension = 24576
best mean L = 2.021 at t = 74
best hard energy = 3.917 at t = 74
maximum final-sector probability = 0.279 at t = 63
final mean L = 2.061
final hard energy = 3.758
final-sector probability = 0.268
Hamiltonian energy drift = 1.55e-13
```

Interpretation: the autonomous Hamiltonian produces a clean first erosion event. The emitted hard energy approaches one shell quantum, and the droplet shrinks from `L = 3` to about `L = 2`. The second erosion event appears only partially.

### Two-shell long-waveguide run

The same model was then run with sparse scrambling and longer radiation chains.

Parameters:

```text
L0 = 3
Lmin = 1
q = 2
max hard quanta = 2
omega = 4 sigma
erosion coupling = 0.50
chain hopping = 1.2
scramble mode = sparse
```

Comparison:

```text
chain  dimension  final L  p(final)  hard energy  far-chain occ.  H drift
5      24576      1.936    0.335     4.254        0.630           1.1e-13
10     86016      1.349    0.718     6.605        0.834           4.3e-14
14     162816     1.228    0.811     7.086        0.862           3.0e-14
```

For the chain-14 run:

```text
time    mean L   hard energy  p(initial)  p(mid)  p(final)  far-chain occ.
0.000   3.000    0.000        1.000       0.000   0.000     0.000
13.333  1.321    6.715        0.067       0.188   0.746     0.945
26.667  1.237    7.053        0.045       0.148   0.808     0.916
80.000  1.228    7.086        0.039       0.150   0.811     0.862
```

The full two-shell hard-energy target is `8 sigma`. The chain-14 run reaches about `7.09 sigma`, with more than 80 percent of the probability in the final droplet sector.

Interpretation: the obstruction seen in the short-chain model was mainly finite outgoing phase space. A larger radiation waveguide makes the same autonomous Hamiltonian behave much more like an evaporator.

### One-shell sanity check

Parameters:

```text
L0 = 2
Lmin = 1
chain length = 8
max hard quanta = 1
```

For stronger coupling:

```text
erosion coupling = 0.50
chain hopping = 1.2

dimension = 288
final mean L = 1.477
final hard energy = 2.093
final-sector probability = 0.523
Hamiltonian energy drift = 6.93e-14
```

Even the one-shell model does not become fully irreversible on a finite closed chain. It reaches substantial transfer and then remains coherently mixed between pre- and post-emission sectors.

## What this means

This is a real step toward the autonomous Hamiltonian version:

```text
single Hilbert space: yes
single time-independent Hamiltonian: yes
energy conservation: yes, numerically stable
autonomous erosion: yes
hard radiation propagation: yes
one-shell shrinkage: yes, partial but clear
two-shell shrinkage: yes in the enlarged-waveguide run
Page-curve diagnostics in the autonomous model: open
```

The synthetic effective model already shows the desired droplet thermodynamics, shell-as-radiation bookkeeping, local scrambling, approximate hard thermality, and Page-like entropy behavior. The autonomous model now reproduces the shell-erosion part of that mechanism over two shells. The information-flow diagnostics still have to be lifted into this autonomous setting.

## Main obstruction

A candidate `H_total` now exists. The short-chain obstruction was real but not fatal. Hermitian coupling always allows reverse transfer, so a very small radiation chain leaves too much amplitude near the droplet. A longer chain gives enough outgoing phase space for the two-shell run to proceed.

This is exactly where black-hole evaporation uses the large exterior field Hilbert space. For a non-gravitational model, the corresponding ingredient is a large radiation waveguide, bath, or continuum limit. That can be generated by a time-independent Hamiltonian, but exact state-vector simulation becomes the bottleneck quickly.

## Next useful step

The larger radiation sector is now implemented for the two-shell test. The next model improvement should be diagnostics rather than another erosion mechanism.

The clean target is:

```text
H_total = H_drop + H_scr + H_rad + H_erosion
```

with `H_rad` a larger tight-binding waveguide or many-mode radiation band. The current chain version already shows that enlarging `H_rad` improves evaporation. The next test is whether the same autonomous run also gives:

```text
E ~ L
S ~ L^2
T increases as E decreases
emitted hard energy grows as the droplet shrinks
early radiation is locally thermal
global evolution remains unitary
early-late radiation correlations appear after the Page turnover
```

That would be the autonomous version of the result we actually want.
