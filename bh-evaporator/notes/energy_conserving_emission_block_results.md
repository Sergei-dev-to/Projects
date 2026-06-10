# Energy-Conserving Emission Block Results

## Question

Can the Hamiltonian emission block exchange an actual boundary-mode excitation
with a hard bath energy bin, instead of only emitting a hard label?

This is the next upgrade after:

```text
hard/soft isometry
-> Hamiltonian block
-> energy-aware Hamiltonian block.
```

## Script

```text
sim/energy_conserving_emission_block.py
```

Primary outputs:

```text
sim/data/energy_conserving_emission_block.csv
sim/data/energy_conserving_emission_block_summary.csv
sim/data/energy_conserving_emission_block_local_n4.csv
sim/data/energy_conserving_emission_block_local_n4_summary.csv
sim/data/energy_conserving_emission_block_scrambled_n4.csv
sim/data/energy_conserving_emission_block_scrambled_n4_summary.csv
```

## Local Energy-Aware Block

Each microscopic emission uses:

```text
port in {0,1}
edge energy level h in {0,1}
flag in {in,out}
hard bath bin h in {0,1}
soft record in {0,1,2,3}
```

First, the edge mode is prepared in:

```text
sum_h sqrt(p_h) |h>_edge.
```

Then the resonant Hamiltonian couples:

```text
|i>_port |h>_edge |in> |0>_hard |0>_soft
  <->
|0>_port |0>_edge |out> |h>_hard |2i+h>_soft.
```

If the hard bath bin has the same energy as the edge level, this locally
conserves the excitation energy:

```text
edge energy h -> hard bath energy h.
```

The finite pulse is:

```text
U_emit = exp(-i theta H_emit),
theta = pi/2.
```

The block check gives:

```text
local energy-aware block error: 2.567e-16
```

The edge reset diagnostic gives:

```text
p(edge excited after pulse) = 0.0000
```

so the edge excitation is transferred to the hard bath bin.

## Golden Weights

For:

```text
L0 = 20
q = 2
sigma = 1
2D bath
x bins = [0,2], [2,8]
```

the hard-bin weights are:

```text
event 1 p1 = 0.4065, <omega>/T = 1.9878
event 2 p1 = 0.4066, <omega>/T = 1.9879
event 3 p1 = 0.4066, <omega>/T = 1.9879
```

These are still derived from:

```text
d Gamma ~ omega^(d-1) exp[S(M - omega) - S(M)] d omega.
```

## Complete Small Control

For:

```text
n_bulk = 3
n_events = 3
```

the default result is:

```text
variant      D_hard   p(edge*)   I(R:hard)   I(R:record)   I(R:bulk)
none         0.0000    0.0000      0.0000       1.3863      2.7726
local        0.0000    0.0000      0.0000       2.8752      1.2837
scrambled    0.0000    0.0000      0.0000       2.8829      1.2760
```

So the information-flow pattern survives the energy-aware block:

```text
hard radiation is locally thermal;
hard radiation alone carries no reference information;
hard+soft records carry reference information;
local/scrambled mixing moves information from bulk to boundary.
```

## Larger Nontrivial Checks

For:

```text
n_bulk = 4
n_events = 3
```

the nontrivial branches give:

```text
variant      D_hard   p(edge*)   I(R:hard)   I(R:record)   I(R:bulk)
local        0.0000    0.0000      0.0000       2.9859      2.5593
scrambled    0.0000    0.0000      0.0000       2.9385      2.6067
```

These runs are slower because the repeated SVD diagnostics grow quickly with
emitted record dimension.

## What This Fixes

The previous Hamiltonian block emitted a hard label.

This block emits a hard energy bin by draining a boundary edge excitation:

```text
edge h -> hard bath h.
```

So the microscopic emission channel now has:

```text
finite Hamiltonian pulse;
golden-rule hard weights;
local edge-to-bath energy exchange;
soft purifying record;
reference-information diagnostics.
```

This is the most coherent microscopic block so far.

## What This Still Does Not Fix

This is local energy conservation inside the emission block, not yet a full
autonomous evaporator.

Still modular:

```text
edge mode is prepared with golden-rule weights before the decay pulse;
fresh flag/hard/soft ancillas are supplied each event;
the pulse time theta = pi/2 is chosen;
bulk-to-boundary mixing is separate;
the droplet mass is updated externally;
the coarse L register is not dynamically changed.
```

So the remaining hard problem has shifted.

Before:

```text
Can hard/soft emission be Hamiltonian?
```

Now:

```text
Can the boundary edge population and golden-rule weights arise dynamically from
a bath-coupled boundary mode at temperature T_L, rather than being prepared
before each event?
```

## F1-F13 Impact

```text
F2:
  stronger P. The microscopic emission event is unitary under a finite
  Hamiltonian pulse.

F7:
  stronger P. The emitted hard bin is tied to an edge energy level and uses
  golden-rule weights, but the edge population is still prepared modularly.

F8/F9:
  stronger P. The same hard-thermal/global-record information pattern survives
  energy-aware emission.

F13:
  stronger P. The event is local to boundary port + edge mode + fresh bath/soft
  ancillas.
```

Still no clean `Y` upgrade for the partial entries.

## Next Step

The next meaningful target is:

```text
replace explicit edge preparation with thermal/golden-rule edge occupation
from a boundary soft-mode Hamiltonian.
```

In other words, move from:

```text
prepare edge according to p_h, then decay
```

to:

```text
edge mode has its own Hamiltonian and occupation;
weak coupling to the bath produces the same p_h by golden-rule dynamics.
```

That would connect the boundary soft-mode diagnostic to the Hamiltonian block
instead of keeping them adjacent but separate.
