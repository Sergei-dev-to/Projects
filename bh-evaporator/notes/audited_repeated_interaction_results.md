# Audited Repeated-Interaction Evaporator Results

## Purpose

Test a cleaner version of the stitched architecture in which the same audited
cycle combines:

```text
deterministic expander interacting-spin scrambling;
finite bath-density microscopic emission;
reversible shrinkage bookkeeping;
shell transfer to radiation;
Page and old/new radiation diagnostics.
```

This is not a single autonomous Hamiltonian. It is a single repeated-
interaction update rule with all modules visible in one simulation.

## Script

```text
sim/audited_repeated_interaction_evaporator.py
```

Output:

```text
sim/data/audited_repeated_interaction_evaporator_*_seed*.csv
sim/data/audited_repeated_interaction_evaporator_summary.csv
```

## Setup

Default run:

```text
L0 = 4
q = 2
sigma = 1
bath dimension d = 2
bin count = 8
bath microstates = 2048
deterministic interacting-spin expander dynamics
warmup time = 8
cycle time = 2
dt = 0.2
seeds = 0,...,4
```

Each shell cycle applies:

```text
1. deterministic expander interacting-spin scrambling on active qubits;
2. finite bath-density approximation to golden-rule emission weights;
3. microscopic emissions until the shell gap is crossed;
4. reversible shrinkage check;
5. shell transfer to radiation;
6. radiation entropy and old/new mutual information diagnostics.
```

## Initial Margulis Results

```text
seed  micro emissions  entropy deficit  max bath L1   Page L  first old/new MI  lifetime scale
-----------------------------------------------------------------------------------------------
0     10               0.368            1.189e-03     2       3->2              0.333333
1     10               0.158            1.189e-03     2       3->2              0.333333
2     10               0.160            1.189e-03     2       3->2              0.333333
3     10               0.303            1.189e-03     2       3->2              0.333333
4     10               0.144            1.189e-03     2       3->2              0.333333
```

For `L0=4`, the Page crossing expected from dimension competition is:

```text
L ~= L0 / sqrt(2) ~= 2.8,
```

so the discrete crossing at:

```text
L = 2
```

is the expected small-system result after shell transfer.

The continuum lifetime normalization also matches the `d=2` law:

```text
tau / M0^3 = 1/3.
```

## Scrambling Controls

The script now compares three update rules:

```text
margulis:
  deterministic algebraic expander interacting-spin dynamics.

grid:
  deterministic nearest-neighbor grid interacting-spin dynamics.

none:
  no internal entangling dynamics.
```

Aggregate results over five seeds:

```text
scrambler   mean entropy deficit   min deficit   max deficit   first old/new MI
--------------------------------------------------------------------------------
margulis    0.227                  0.144         0.368         3->2
grid        0.219                  0.149         0.353         3->2
none        8.318                  8.318         8.318         none
```

Interpretation:

```text
1. No-scrambling fails badly.
2. Entangling dynamics is genuinely doing work; Page behavior is not produced
   by shell bookkeeping alone.
3. At L0=4, grid and Margulis are not distinguishable by this Page diagnostic.
```

This validates the need for scrambling in the combined update, but it does not
prove that the expander is necessary.

## One Example Trajectory

Seed 0:

```text
L: 4 -> 3
  micro emissions = 3
  first omega/T = 2.25
  bath L1 error = 1.189e-03
  rad qubits = 7
  remaining qubits = 9

L: 3 -> 2
  micro emissions = 3
  first omega/T = 2.25
  bath L1 error = 1.079e-03
  rad qubits = 12
  remaining qubits = 4

L: 2 -> 1
  micro emissions = 2
  first omega/T = 1.733
  bath L1 error = 1.028e-03
  rad qubits = 15
  remaining qubits = 1

L: 1 -> 0
  micro emissions = 2
  first omega/T = 0.953
  bath L1 error = 1.161e-03
  rad qubits = 16
  remaining qubits = 0
```

## Interpretation

This is the first test where the relevant modules are stitched into one
audited update rule rather than only compared across separate diagnostics.

What it supports:

```text
F2  purifiable/reversible update structure
F3  shrinking internal state space
F6  lifetime scaling under the d=2 power law
F7  finite bath-density emission
F8  Page-like radiation entropy at small size
F9  old/new radiation mutual information near Page crossing
F14 deterministic expander interacting-spin scrambling module
F15 one explicit repeated-interaction rule
```

The important upgrade is F15:

```text
from "stitched architecture described across modules"
to "single audited repeated-interaction simulator."
```

The important F14 lesson is narrower:

```text
some entangling scrambling is necessary;
the present small Page diagnostic does not separate grid from expander.
```

## Limitations

This does not prove the strong result.

Remaining limitations:

```text
1. L0=4 is small.
2. The spin dynamics is deterministic but still Trotterized.
3. The bath density is finite and accurate, but its spectrum is still assigned.
4. The shell threshold remains a designed bookkeeping rule.
5. The emitted hard bins are tracked statistically, not as a large explicit
   hard-radiation Hilbert space entangled with the spin state.
6. This is not one autonomous time-independent Hamiltonian.
7. The L0=4 Page diagnostic is too small to distinguish local grid
   scrambling from expander scrambling.
```

## Status Change

Before this test:

```text
F15 = P+:
  explicit stitched architecture, but mostly described across separate tests.
```

After this test:

```text
F15 = P+ stronger:
  one audited repeated-interaction simulator combines the current modules at
  the largest feasible exact-state size.
```

It should not be upgraded to `Y` unless we either:

```text
1. derive a less modular global Floquet rule; or
2. produce an autonomous Hamiltonian embedding.
```

## Next Test

The no-scrambling control has now been run. The next useful pressure test is
not another identical `L0=4` repeat.

It is one of:

```text
1. replace assigned bath degeneracies with a simple explicit bath Hamiltonian;
2. make the hard radiation bins part of the explicit quantum state;
3. push the scrambling control to a diagnostic that separates grid from
   expander;
4. search for a less modular global Floquet embedding of the threshold rule.
```

My preference:

```text
make the hard radiation bins part of the explicit quantum state.
```

Reason:

```text
The current simulation tracks hard emission statistically. Explicit hard-bin
registers would make the radiation side less bookkeeping-like and would be
the next real F2/F8/F9 upgrade.
```
