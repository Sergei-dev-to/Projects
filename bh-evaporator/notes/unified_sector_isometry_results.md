# Unified Sector-Isometry Evaporator Results

## Question

Can we remove the split between the sector-rate calculation and the separate
unitary record model?

The target here is one finite state-vector evolution that measures, in the same
run:

```text
hard spectrum;
emitted power;
full radiation von Neumann entropy;
early/late radiation mutual information;
shrinking core support.
```

## Script

```text
sim/unified_sector_isometry_evaporator.py
```

Main outputs:

```text
sim/data/unified_sector_isometry_trajectory.csv
sim/data/unified_sector_isometry_summary.csv
sim/data/unified_sector_isometry_large_window_trajectory.csv
sim/data/unified_sector_isometry_large_window_summary.csv
```

## Model

The model starts from the energy-resolved sector-Hamiltonian kernel.  Core
sectors have

```text
dim B_n = q^n
S_micro(n) = n log q
```

and the tested mass laws are

```text
M_n = alpha sqrt(n)
M_n = alpha n
```

For each downward sector transition, the script builds the golden-rule kernel

```text
Gamma_fi proportional to |<f,n-1|X_n|i,n>|^2 omega_fi^p
```

from the same energy-resolved sector spectra used in the sector-rate
calculation.  It then bins the emitted hard energy in

```text
x = beta omega
```

and uses the resulting hard distribution as the hard branch of a unitary
emission isometry.

The emission map has the schematic form

```text
V_n : B_n -> B_{n-1} x R_hard x A_soft .
```

The soft register is the Stinespring record that makes the coarse shrinkage map
norm-preserving and column-orthogonal.  It is not a separate companion model.
The hard weights come from the sector transition kernel.

The current implementation uses an equilibrated sector emission rule: the hard
branch distribution is the sector-averaged golden-rule distribution.  This is
the unified-state-vector analogue of the intra-sector equilibration step in
the rate calculation.

## Default Exact Endpoint Run

Command:

```text
python bh-evaporator/sim/unified_sector_isometry_evaporator.py
```

Parameters:

```text
q = 2
n_max = 5
n_min = 2
seed = 2468
DOS = exponential
width_x = 4
```

Summary:

```text
mass    mapping      P_last/P_first   TV      Srad_max   Srad_final   I_early_late
sqrt    scrambled        1.684        0.197     2.648       1.321         5.229
sqrt    noscramble       1.684        0.197     2.732       1.386         5.446
linear  scrambled        0.852        0.181     2.664       1.351         5.274
linear  noscramble       0.852        0.181     2.734       1.386         5.461
```

This run reaches the small final sector.  It shows the unified package:

```text
sqrt mass law accelerates;
linear control decelerates;
full radiation entropy rises and turns over;
early/late radiation mutual information is nonzero.
```

The hard-spectrum TV distance is worse than the earlier sector-rate table
because the final small-sector transitions are visibly finite-size distorted.

## Larger-Sector Window

Command:

```text
python bh-evaporator/sim/unified_sector_isometry_evaporator.py \
  --n-max 7 --n-min 4 --seeds 2468 --mappings scrambled,noscramble \
  --trajectory-csv bh-evaporator/sim/data/unified_sector_isometry_large_window_trajectory.csv \
  --summary-csv bh-evaporator/sim/data/unified_sector_isometry_large_window_summary.csv
```

Summary:

```text
mass    mapping      P_last/P_first   TV      Srad_max   Srad_final   I_early_late
sqrt    scrambled        1.402        0.087     4.077       2.729         7.894
sqrt    noscramble       1.402        0.087     4.128       2.772         7.678
linear  scrambled        0.938        0.078     4.075       2.730         7.877
linear  noscramble       0.938        0.078     4.127       2.772         7.633
```

This is the cleaner thermality window.  In the same unitary isometry model:

```text
sqrt mass law gives accelerating power;
linear mass law does not;
hard spectrum remains close to x^p exp(-x);
full radiation entropy is measured from the same state vector.
```

The step-by-step powers in the larger-window run are:

```text
sqrt:   0.168 -> 0.198 -> 0.235
linear: 0.884 -> 0.869 -> 0.828
```

So the acceleration/deceleration contrast survives after unifying the
thermodynamic and information-flow diagnostics.

## What Improved

The old paper draft had two linked diagnostics:

```text
sector-rate model for spectrum and acceleration;
separate repeated-interaction model for Page-like information flow.
```

This script replaces that split with one state-vector model.  The same emitted
hard records used to compute the spectrum are part of the radiation subsystem
used to compute

```text
S_vN(R_full)
I(R_early : R_late).
```

This is the main improvement.

## What Remains Imposed

The model is still a sector isometry, not an autonomous time-independent
Hamiltonian evolved as

```text
exp(-i H_total t).
```

The current isometry also uses sector-averaged equilibrated hard probabilities.
That is the unified version of the intra-sector equilibration assumption.  It
removes the two-model split, but it does not derive equilibration from
microscopic chaotic dynamics.

The soft register is explicit.  This is standard Stinespring bookkeeping for
unitarity, but a more microscopic model would identify the soft record with
actual outgoing or internal degrees of freedom.

## Computational Limitation

The exact entropy calculation scales quickly with the number of emissions.  A
four-event run from

```text
n = 7 -> 3
```

timed out with the current dense partition-entropy routine.  This is a
computational limitation of the implementation, not evidence against the
model.  The next implementation improvement would compute reduced entropies
with sparse Gram matrices or sampling over trajectories.

## Current Interpretation

This is a real strengthening of the result.  We can now say:

```text
There is a single finite sector-isometry evaporator whose hard emission
weights are derived from an energy-resolved golden-rule kernel.  In that one
state-vector model, the square-root mass law gives near-thermal hard radiation,
accelerating power, shrinking core support, Page-like radiation entropy
turnover, and early/late radiation mutual information.  The linear mass-law
control gives a similar hard spectrum but does not accelerate.
```

The remaining gap is no longer the split between thermodynamics and
information flow.  The remaining gap is microscopic origin: deriving the
sector count, mass law, equilibration, and isometry from one recognizable
autonomous Hamiltonian.
