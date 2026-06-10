# Naive Hamiltonian Evaporator: First Results

## What was implemented

Script:

```text
sim/hamiltonian_shell_evaporator.py
```

The model uses:

```text
H_total = H_core + H_rad + H_int
```

with:

```text
H_core = direct_sum_m E_m I_{D_m}
H_rad = omega |1><1|                # or several emitted labels
H_int = sum_m g X_m tensor |emitted><0| + h.c.
```

Each step appends a fresh radiation time bin, applies the fixed collision
unitary on `core x new_bin`, then never recouples that bin. The radiation
Renyi-2 entropy is computed from the reduced core state.

This is a genuine Hamiltonian collision model, but still engineered.

## Binary-bin default

Command:

```text
python sim/hamiltonian_shell_evaporator.py
```

Result:

```text
initial energy: 8.000
final energy:   7.334
peak S2_rad:    0.801
peak step:      15
mid/early emitted-power ratio: 0.330
mean emitted-bin probability: 0.044
```

Time series:

```text
E(t):
8.000, 7.837, 7.735, 7.660, 7.602, 7.556, 7.517, 7.483,
7.455, 7.431, 7.409, 7.390, 7.373, 7.359, 7.345, 7.334

P(t):
0.000, 0.163, 0.102, 0.074, 0.058, 0.047, 0.039, 0.033,
0.028, 0.025, 0.022, 0.019, 0.017, 0.015, 0.013, 0.012
```

The system emits initially, then the emission rate decays. There is no
black-hole-like acceleration and no entropy turnover within the simulated
window.

## Linear control

Command:

```text
python sim/hamiltonian_shell_evaporator.py --curvature 1.0 \
  --output sim/data/hamiltonian_shell_evaporator_linear_control.npz
```

Result:

```text
initial energy: 8.000
final energy:   7.106
peak S2_rad:    1.126
peak step:      15
mid/early emitted-power ratio: 0.318
mean emitted-bin probability: 0.060
```

The linear control behaves similarly or even emits slightly more. So the
binary Hamiltonian does not reproduce the convex/control separation seen in
the shell-channel model.

## Main obstruction: dark subspaces

The key problem is rank.

In the convex model the core shell dimensions shrink:

```text
64 -> 24 -> 10 -> 5 -> 3 -> 2 -> 1 -> 1
```

With one emitted radiation label, the transition matrix has the form:

```text
X_m: C^{D_m} -> C^{D_{m+1}}
```

so:

```text
rank X_m <= D_{m+1} < D_m
```

There is therefore a large dark subspace in each high-energy shell. The first
collision emits the bright component, but a large part of the state remains in
directions that the fixed `X_m` does not couple efficiently.

This explains the observed shell populations. In the binary default, after
15 steps about 64 percent of the state still remains in the initial shell.

## Multi-channel attempt

The script was generalized to support multiple emitted labels per bin:

```text
|0>, |1>, ..., |M>
```

This increases the accessible final space:

```text
C^{D_m} -> C^{D_{m+1}} tensor C^M
```

Short runs:

```text
channels = 2, steps = 10:
  final energy: 6.707
  peak S2_rad: 1.665
  acceleration ratio: 0.703

channels = 3, steps = 8:
  final energy: 6.858
  peak S2_rad: 1.772
  acceleration ratio: 0.756
```

Multi-channel emission helps the system lose more energy, but the emitted
power still decays rather than accelerates in these naive runs.

## Intra-shell chaos attempt

Adding weak intra-shell random Hamiltonians:

```text
H_core = direct_sum_m (E_m I + epsilon G_m)
```

with `epsilon = 0.5` improved entropy production but did not fix the basic
issue:

```text
convex, channels = 2, chaos = 0.5:
  final energy: 6.764
  peak S2_rad: 1.870
  acceleration ratio: 0.819

linear, channels = 2, chaos = 0.5:
  final energy: 6.285
  peak S2_rad: 2.709
  acceleration ratio: 0.908
```

Again, the convex model does not outperform the linear control.

## Interpretation

The naive Hamiltonian version fails the desired test.

This is informative. It shows that the shell-channel result was relying on an
effective re-randomization / full-rank Stinespring map. A fixed Hamiltonian
with a single low-rank transition operator does not automatically implement
that map.

The problem is not unitary evolution itself. The problem is that an evaporating
system with shrinking shell dimensions needs enough outgoing channel capacity
and/or internal scrambling to avoid trapping most of the state in dark
subspaces.

## What this teaches us

The next Hamiltonian design cannot be:

```text
one binary emission channel
one fixed low-rank X_m per shell transition
degenerate shell interiors
```

It probably needs at least one of:

```text
many independent outgoing channel labels
time-dependent contact points / repeated random couplings
strong intra-shell scrambling between emissions
larger final spaces through multi-frequency or multi-mode bins
a Lindblad/weak-coupling limit first, then purification
```

The physical version of this statement is reasonable: black holes radiate into
many angular, species, frequency, and time-bin channels. A one-channel
Hamiltonian evaporator is too rank-limited to behave like an evaporating
thermal body.

## Decision

Do not treat the naive Hamiltonian as a success.

But also do not abandon the project yet. The failure identifies a concrete
design constraint:

```text
the Hamiltonian evaporator needs channel capacity and scrambling sufficient to
make the effective emission map high-rank.
```

The next credible attempt should be designed around that constraint rather
than merely tuning `g` or `dt`.
