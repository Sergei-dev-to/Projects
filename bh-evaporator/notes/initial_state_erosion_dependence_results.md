# Initial-State Dependence Of The Erosion Channel

## Purpose

Test whether the structured erosion channel produces thermal-looking hard
radiation by itself, or whether the previous positive results depend on the
droplet state already being typical/scrambled.

## Script

```text
sim/initial_state_erosion_dependence.py
```

Outputs:

```text
sim/data/initial_state_erosion_dependence.csv
sim/data/initial_state_erosion_dependence_summary.csv
```

Command:

```text
python sim/initial_state_erosion_dependence.py --seeds 8
```

## Initial States Tested

```text
haar_full:
  Haar-random state on the full droplet Hilbert space.

outer_maxmix:
  outer shell maximally entangled with the interior, up to the finite-size
  Schmidt-rank limit.

factor_haar:
  product of independent Haar states on each shell factor.

outer_basis:
  Haar-random interior tensor one outer-shell basis state.

outer_uniform:
  Haar-random interior tensor uniform outer-shell superposition.

basis_all:
  global computational-basis product state.

uniform_all:
  product of uniform superpositions on all factors.
```

Models tested:

```text
shift_minimal
clock_minimal
flux_partition
```

## Key Result

The channel does not thermalize arbitrary initial states.

The strong hard/soft result holds for typical or locally mixed shells:

```text
initial        model          maxD range      I_pair
haar_full      shift/clock     ~0.002-0.029   nonzero
outer_maxmix   shift/clock     ~0.002-0.017   nonzero
```

It weakens or fails for low-entanglement product states:

```text
initial        typical behavior
factor_haar    hard radiation only moderately close to thermal;
               early/late pair mutual information near zero

basis_all      shift works, clock fails
uniform_all    clock works, shift fails
```

So the previous positive result should be read as a scrambled-state result, not
as a state-independent channel property.

## Representative Numbers

For `L0 = 3`, `d_hard = 2`:

```text
model          initial        maxD    I_hh    I_pair  S_h/thermal
clock_minimal  haar_full      0.025   0.0009   3.856  0.581/0.582
clock_minimal  outer_maxmix   0.015   0.0008   4.159  0.582/0.582
clock_minimal  basis_all      0.443   0.0000   0.000  0.000/0.582
clock_minimal  uniform_all    0.000   0.0000   0.000  0.582/0.582

shift_minimal  haar_full      0.025   0.0007   3.856  0.582/0.582
shift_minimal  outer_maxmix   0.011   0.0007   4.159  0.582/0.582
shift_minimal  basis_all      0.000   0.0000   0.000  0.582/0.582
shift_minimal  uniform_all    0.443   0.0000   0.000 -0.000/0.582
```

For `L0 = 4`, `d_hard = 2`, the same qualitative pattern remains:

```text
haar_full / outer_maxmix:
  maxD ~ 0.002 for shift/clock;

basis_all:
  clock maxD ~ 0.443, shift maxD ~ 0;

uniform_all:
  clock maxD ~ 0, shift maxD ~ 0.443.
```

## Interpretation

The hard marginal is controlled by overlaps of the form:

```text
rho_hh' ~ sqrt(p_h p_h') Tr(rho_shell U_h^dagger U_h').
```

For a locally mixed shell, shift and clock operations look orthogonal, so the
hard marginal becomes diagonal with the chosen thermal weights.

For a pure structured shell, the answer is basis-dependent:

```text
shift operations are orthogonal on basis states but not on uniform states;
clock operations are orthogonal on uniform states but not on basis states.
```

This is exactly what the scan finds.

## Consequence For The F-Table

No feature changes are needed, but the meaning of `F8 = P` and `F9 = P` is now
sharper.

```text
F8:
  thermal-looking hard radiation is robust for typical/scrambled shells, not
  arbitrary shells.

F9:
  early/late hard+soft correlations require initial inter-shell scrambling or
  entanglement. Product shell states do not generate them by magic.
```

This is not a fatal problem. It is close to the black-hole expectation that the
interior has scrambled before significant evaporation. But it must be included
as a model assumption or derived from an internal Hamiltonian.

## What This Fixes

The test prevents an overclaim.

Bad claim:

```text
the erosion channel itself produces Page-like information flow.
```

Better claim:

```text
given a scrambled residual-entropy droplet, structured shell erosion produces
locally thermal hard radiation while preserving information in hard+soft
correlations.
```

## Next Question

The next missing ingredient is therefore not another erosion map.

It is:

```text
What internal dynamics makes the shell locally mixed before erosion?
```

Possible minimal versions:

```text
1. assume fast scrambling within the constrained droplet;
2. insert a constrained internal scrambling unitary between erosion steps;
3. construct a local plaquette/edge Hamiltonian and test whether it scrambles
   shell observables fast enough.
```

Option 2 is the next practical diagnostic. Option 3 is the real Hamiltonian
target.

Follow-up note:

```text
notes/natural_fast_scrambling_options.md
```

The important refinement is that the edge-tension droplet may not need
black-hole-optimal logarithmic scrambling. Since one-shell erosion takes
`t_shell ~ R^2`, ordinary local constrained chaotic dynamics may be enough if
it mixes shell observables on a time scale shorter than `R^2`.
