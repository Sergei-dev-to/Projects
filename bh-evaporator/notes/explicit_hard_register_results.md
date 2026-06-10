# Explicit Hard-Register Evaporator Results

## Purpose

Upgrade the audited repeated-interaction model by making the emitted hard
radiation bins part of the explicit quantum state.

Previous audited simulator:

```text
shell qubits were transferred explicitly;
hard-bin emissions were tracked statistically.
```

This diagnostic:

```text
adds one explicit hard quantum register per shell emission;
keeps the emitted shell qubits as the soft radiation record;
computes hard-local thermality, full radiation entropy, and old/new MI from
the same pure state.
```

## Script

```text
sim/explicit_hard_register_evaporator.py
```

Output:

```text
sim/data/explicit_hard_register_evaporator_*_seed*.csv
sim/data/explicit_hard_register_evaporator_summary.csv
```

## Setup

Default run:

```text
L0 = 4
q = 2
sigma = 1
bath dimension d = 2
d_hard = 2
bath microstates = 2048
warmup time = 8
cycle time = 2
dt = 0.2
bath sources = finite_degeneracy, box2d
scramblers = margulis, grid, none
seeds = 0,1,2
```

The shell emission map is:

```text
|psi>_shell -> sum_h sqrt(p_h) |h>_hard Shift_h |psi>_soft.
```

Here:

```text
p_h
```

comes from finite bath degeneracies approximating the golden-rule bin weights.

This is a minimal-soft structured hard/soft map:

```text
hard:
  energy/bin register;

soft:
  emitted shell qubits after a reversible shift conditioned on h.
```

## Aggregate Results

Using the finite-degeneracy target bath:

```text
scrambler   total deficit   max D_hard   max hard-S error   final hard S   first old/new MI
------------------------------------------------------------------------------------------------
margulis    0.876           1.77e-02     8.21e-04           1.826          3->2
grid        0.874           1.54e-02     5.71e-04           1.826          3->2
none        9.011           2.59e-01     1.87e-01           1.537          none
```

Using the explicit `box2d` bath-Hamiltonian spectrum:

```text
scrambler   total deficit   max D_hard   max hard-S error   final hard S   first old/new MI
------------------------------------------------------------------------------------------------
margulis    0.876           1.66e-02     7.16e-04           1.440          3->2
grid        0.874           1.43e-02     5.09e-04           1.440          3->2
none        9.011           2.40e-01     1.66e-01           1.196          none
```

Definitions:

```text
total deficit:
  sum of positive Page-capacity deficits across shell steps.

D_hard:
  trace distance between the latest hard-register reduced state and the
  target diagonal bin distribution.

hard-S error:
  |S(latest hard) - S(target hard distribution)|.
```

## One Margulis Trajectory

Seed 0:

```text
L: 4 -> 3
  p_hard = (0.964, 0.036)
  S_hard = 0.155
  S_target = 0.155
  D_hard = 1.03e-02

L: 3 -> 2
  p_hard = (0.882, 0.118)
  S_hard = 0.361
  S_target = 0.362
  D_hard = 1.75e-02

L: 2 -> 1
  p_hard = (0.571, 0.429)
  S_hard = 0.682
  S_target = 0.683
  D_hard = 1.90e-02

L: 1 -> 0
  p_hard = (0.320, 0.680)
  S_hard = 0.625
  S_target = 0.627
  D_hard = 2.96e-02
```

The hard bin is explicitly present in the state, and its local reduced density
matrix is close to the finite-bath target distribution when the shell has been
scrambled.

## What This Shows

The good news:

```text
1. Explicit hard radiation registers are feasible at L0=4.
2. Hard-local thermality is not just assigned as a classical log.
3. With entangling dynamics, latest hard-bin entropy matches the target
   distribution to ~1e-3.
4. No-scrambling fails both the Page deficit and hard-local thermality tests.
5. Old/new radiation MI again turns on at 3->2 for scrambled runs.
6. Replacing the fitted finite-degeneracy bath with an explicit 2D-box bath
   spectrum does not break the result.
```

This strengthens:

```text
F2:
  the emitted hard register is now part of the pure quantum state.

F8:
  radiation entropy is computed from explicit hard+soft radiation axes.

F9:
  old/new MI is computed with explicit hard+soft latest radiation.

F14:
  scrambling is needed not only for Page behavior but also for hard-local
  thermality in this structured emission map.
```

## What It Does Not Show

It still does not prove the strong model.

Limitations:

```text
1. d_hard = 2 is a very compressed hard spectrum.
2. There is one hard register per shell, not one per microscopic emission.
3. L0=4 is still small.
4. Grid and Margulis remain indistinguishable by this small Page diagnostic.
5. The hard/soft map is structured and reversible, but still a chosen channel.
6. This is not one autonomous Hamiltonian.
7. The `box2d` bath spectrum is explicit, but still supplied as an external
   bath module.
```

## Interpretation

This closes one important bookkeeping concern:

```text
hard radiation is no longer only a statistical emission log.
```

But it opens a sharper next question:

```text
Can the same explicit-hard construction be pushed toward microscopic emission
events rather than one compressed hard register per shell?
```

For now the result is enough to upgrade the model from:

```text
explicit soft/shell radiation plus statistical hard bins
```

to:

```text
explicit hard+soft radiation at small size.
```

## Next Step

The best next pressure test is:

```text
increase hard-radiation resolution without exploding the Hilbert space.
```

Options:

```text
1. d_hard = 4 at smaller L0;
2. one hard register per coarse energy packet instead of per shell;
3. sparse/history-state representation for microscopic hard emissions;
4. explicit bath Hamiltonian whose degenerate levels generate the hard bins.
```

My preference:

```text
d_hard = 4 at L0=3 or sparse microscopic-history representation.
```

Reason:

```text
The next weakness is spectral compression, not the existence of an explicit
hard register.
```
