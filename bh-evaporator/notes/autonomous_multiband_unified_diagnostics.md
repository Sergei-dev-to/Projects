# Autonomous Multiband Hamiltonian With Unified Diagnostics

## Question

Can the autonomous time-independent Hamiltonian branch be pushed toward the
same standard as the unified sector-isometry model?

The target is one autonomous run measuring:

```text
evaporation;
hard spectrum;
core/radiation entropy;
Renyi-2 entropy;
early/late shell mutual information;
energy conservation.
```

## Script Updated

```text
sim/autonomous_multiband_radiation.py
```

This script already used one time-independent Hamiltonian:

```text
H_total = H_drop + H_hard + H_hop + H_scr + H_erosion .
```

The update adds the missing information-flow diagnostics directly to the
multiband autonomous run:

```text
core/radiation von Neumann entropy;
core/radiation Renyi-2 entropy;
hard-radiation entropy;
hard-radiation Renyi-2 entropy;
postselected early/late shell mutual information.
```

This means the multiband autonomous Hamiltonian now reports both spectral and
information-flow observables in the same evolution.

## Main Chain-3 Run

Command:

```text
python bh-evaporator/sim/autonomous_multiband_radiation.py \
  --case-name autonomous_multiband_entropy_chain3 \
  --chain-length 3 \
  --time-points 25 \
  --t-max 60 \
  --summary-csv bh-evaporator/sim/data/autonomous_multiband_entropy_chain3_summary.csv \
  --timeseries-csv bh-evaporator/sim/data/autonomous_multiband_entropy_chain3_timeseries.csv
```

Setup:

```text
L0 = 3
Lmin = 1
q = 2
bands = 2,3,4,5,6
chain length = 3 per band
max quanta = 2
basis dimension = 185856
flat band coupling
```

Summary:

```text
final mean L                    1.834
final final-sector probability  0.373
final hard energy               5.146
maximum hard energy             5.202
energy drift                    9.24e-14

final core/radiation entropy    2.432
maximum core/radiation entropy  2.467
final Renyi-2                   2.044
final hard entropy              3.505
final hard Renyi-2              2.705
final shell mutual information  1.201
maximum shell mutual information 1.412
```

Band spectrum:

```text
omega       2      3      4      5      6
emitted     0.081  0.172  0.250  0.244  0.252
thermal     0.491  0.260  0.138  0.073  0.039
```

Total-variation distance to the thermal target:

```text
TV = 0.497
```

The autonomous Hamiltonian evaporates and entangles, but the emitted spectrum
is much too hard relative to the Schwarzschild-like thermal target.

## Coupling-Profile Checks

The band-coupling profile was changed to see whether a simple softening of the
erosion matrix element fixes the spectrum without killing evaporation.

```text
profile             final L   p(final)  Ehard   TV     S_core:rad  shell MI
flat                1.834     0.373     5.146   0.497  2.432       1.201
inverse_sqrt_omega  2.126     0.201     3.690   0.471  2.439       1.767
inverse_omega       2.354     0.131     2.602   0.434  2.093       1.992
```

Softer couplings move the spectrum modestly toward the thermal target, but
they substantially suppress evaporation.  The improvement is not enough to
make the autonomous multiband spectrum thermal.

## What This Achieves

The autonomous branch now has one run with:

```text
one fixed Hilbert space;
one time-independent Hamiltonian;
unitary evolution exp(-i H_total t);
energy conservation;
autonomous erosion;
hard multiband radiation;
core/radiation entropy;
Renyi-2 entropy;
early/late shell mutual information;
band-resolved emitted spectrum.
```

So the old objection that the autonomous model lacked information-flow
diagnostics is addressed.

## What Fails

The autonomous multiband Hamiltonian does not yet reproduce the thermal hard
spectrum.  The emitted distribution is close to the finite droplet's own
matrix-element/DOS target found in the earlier thermality audit, and far from
the continuum thermal target.

This confirms the sharper diagnosis:

```text
The autonomous Hamiltonian can evaporate and carry information, but its current
finite droplet spectrum does not have the local microcanonical density-of-states
profile needed for Hawking-like thermality.
```

The obstruction is not simply lack of autonomy, lack of radiation propagation,
or lack of entropy diagnostics.  The obstruction is the microscopic spectrum
and transition structure of the active core.

## Comparison With Unified Sector-Isometry Model

The unified sector-isometry model has stronger phenomenology:

```text
near-thermal hard spectrum;
accelerating square-root case;
linear control without acceleration;
Page-like radiation entropy;
early/late mutual information.
```

The autonomous multiband Hamiltonian has stronger microscopic status:

```text
one time-independent H_total;
actual exp(-i H_total t) evolution;
energy conservation;
outgoing waveguide radiation.
```

The gap between the two is now precise:

```text
derive an autonomous core Hamiltonian whose finite-sector density of states and
transition matrix elements reproduce the sector-isometry emission kernel.
```

## Next Model-Level Direction

The next autonomous attempt should not tune the radiation waveguide again.  The
waveguide is working.  The hard problem is the active-core spectrum.

The useful directions are:

```text
1. Replace the current droplet internal spectrum with an explicit sector DOS
   engineered to have the microcanonical slope beta(L), then embed it in the
   autonomous Hamiltonian.  This tests whether the autonomous radiation sector
   can reproduce the sector-isometry result once the core DOS is correct.

2. Search for a less artificial core Hamiltonian whose measured sector DOS has
   the needed local exponential slope.  The relational connector/matrix-clump
   ideas belong here.

3. Improve entropy computation so larger autonomous runs with more shells can
   be measured without dense reduced matrices.
```

The immediate conclusion is that the autonomous route is viable but not yet at
the unified-isometry phenomenology level.  Its missing ingredient is a core
with the right density-of-states structure, not another radiation-chain fix.
