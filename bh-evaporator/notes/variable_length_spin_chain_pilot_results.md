# Variable-Length Spin-Chain Pilot Results

## Purpose

This pilot tests the missing bridge:

```text
right state count
concrete quantum Hamiltonian
shrinking sectors
matrix-element-derived emission
```

It asks whether a variable-length many-body system can reproduce the
area-register acceleration without using fully random Hamiltonian blocks.

Design note:

```text
notes/variable_length_spin_chain_pilot.md
```

## Why a spin chain?

A spin chain is not meant as a literal horizon model.

It is the simplest quantum setup where:

```text
H_n = (C^2)^{tensor n}
dim H_n = 2^n
S_n = n log 2
```

so the black-hole-like area count is natural rather than assigned as an
arbitrary shell degeneracy.

Compared with earlier tracks:

```text
Track A variable-N Bose-Hubbard:
  concrete dynamics, wrong entropy scaling.

Track B area register:
  right entropy scaling, random/abstract dynamics.

Track E variable-length spin chain:
  right entropy scaling, concrete local Hamiltonian blocks.
```

## Implementation

Script:

```text
sim/variable_length_spin_chain_pilot.py
```

Figure:

```text
variable_length_spin_chain_pilot.pdf
```

Data:

```text
sim/data/variable_length_spin_chain_pilot.csv
sim/data/variable_length_spin_chain_random_pilot.csv
```

Sectors:

```text
H_n = n-spin Hilbert space
n = 4,...,10
dim H_n = 2^n
M_n = alpha sqrt(n) or alpha n
```

Local Hamiltonian block:

```text
H_n = M_n I + bandwidth * h_n
```

with:

```text
h_n =
  Jx sum_i X_i X_{i+1}
  + Jz sum_i Z_i Z_{i+1}
  + hx sum_i X_i
  + random z fields.
```

Removal maps:

```text
boundary:
  remove the last spin.

bulk:
  remove any one spin, averaged over sites.

scrambled:
  orthogonally scrambled boundary-removal control.
```

## Main local-Hamiltonian result

Two seeds were run:

```text
2468, 2469
```

Mean results:

```text
block   operator    mass      accel   W ratio   sector-W   selection
---------------------------------------------------------------------
local   boundary    sqrt      1.162   1.158     1.159      0.998
local   bulk        sqrt      1.159   1.154     1.159      0.996
local   scrambled   sqrt      1.077   1.079     1.128      0.956

local   boundary    linear    0.905   0.898     0.898      1.000
local   bulk        linear    0.904   0.896     0.897      1.000
local   scrambled   linear    0.932   0.927     0.928      0.998
```

The result is positive:

```text
1. sqrt mass accelerates;
2. linear mass decelerates;
3. boundary and bulk removal accelerate more strongly than scrambled removal;
4. W tracks emitted power;
5. S2(core) grows to about 5.3-5.7.
```

## Random-block comparison

A random-block comparison was also run with the same sector dimensions and mass
laws.

Mean results:

```text
block    operator    mass      accel   W ratio   sector-W   selection
----------------------------------------------------------------------
random   boundary    sqrt      1.085   1.086     1.136      0.955
random   scrambled   sqrt      1.085   1.086     1.136      0.955

random   boundary    linear    0.917   0.911     0.912      0.998
random   scrambled   linear    0.917   0.911     0.912      0.998
```

In the random-block model, boundary and scrambled removal are indistinguishable.

In the local spin-chain model, boundary/bulk removal outperform scrambled
removal:

```text
local boundary sqrt accel  ~ 1.162
local scrambled sqrt accel ~ 1.077
```

This is the first sign that the concrete Hamiltonian/removal structure is doing
dynamical work beyond pure sector counting.

## Mechanism

The local spin-chain result is mostly sector-profile acceleration:

```text
boundary sqrt:
  sector-W mid/early ~ 1.159
  actual W mid/early ~ 1.158
  selection mid/early ~ 0.998
```

So it is not Track A-style intrasection selection.

Instead:

```text
the local Hamiltonian plus physical removal map gives a stronger favorable
sector-W profile than the scrambled/random controls.
```

This is encouraging because it means the model is not only reproducing Track B
with different notation.

## Interpretation

This is the best bridge model so far.

It has:

```text
right area-law state count;
concrete many-body Hamiltonian blocks;
shrinking Hilbert-space sectors;
matrix-element-derived emission;
accelerating sqrt-mass evaporation;
decelerating linear-mass control;
some sensitivity to local vs scrambled removal.
```

It still does not have:

```text
a derived gravitational horizon;
Page turnover;
early/late radiation structure;
a natural derivation of M_n = sqrt(n).
```

But it is closer to the original target than the fusion pilot:

```text
fusion pilot:
  right state count, but no clear dynamical advantage.

spin-chain pilot:
  right state count and a concrete Hamiltonian/removal structure that changes
  the W profile.
```

## Current verdict

Track E is worth pursuing further.

Next useful tests:

```text
1. scan local Hamiltonian parameters;
2. test n_max=11 if dense diagonalization remains tolerable;
3. compare boundary vs bulk vs scrambled across more seeds;
4. check whether the local advantage survives smaller/larger bandwidth;
5. add the result to the paper spine as the current best bridge model.
```

