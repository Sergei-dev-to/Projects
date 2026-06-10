# Variable-Length Spin-Chain Robustness Results

## Purpose

This scan tests whether the Track E spin-chain result is robust or just a
two-seed accident.

Question:

```text
Does the variable-length local spin-chain evaporator reliably accelerate for
the sqrt mass law, decelerate for the linear control, and retain a local
removal advantage over scrambled removal?
```

## Implementation

Scripts:

```text
sim/scan_variable_length_spin_chain_robustness.py
figs/generate_variable_length_spin_chain_robustness.py
```

Figure:

```text
variable_length_spin_chain_robustness.pdf
```

Data:

```text
sim/data/variable_length_spin_chain_robustness.csv
sim/data/variable_length_spin_chain_robustness_summary.csv
sim/data/variable_length_spin_chain_robustness_advantage.csv
```

Scan:

```text
seeds = 2468,...,2473
bandwidths = 0.1, 0.25, 0.5
operators = boundary, bulk, scrambled
mass laws = sqrt, linear
n = 4,...,10
```

The scan reuses each Hamiltonian block across removal operators.

## Main Result

The result is robust.

For all 6 seeds and all 3 bandwidths:

```text
sqrt mass + boundary removal:
  acceleration > 1 in 18/18 cases

sqrt mass + bulk removal:
  acceleration > 1 in 18/18 cases

linear mass + boundary removal:
  acceleration > 1 in 0/18 cases

linear mass + bulk removal:
  acceleration > 1 in 0/18 cases
```

Mean acceleration by bandwidth:

```text
bandwidth   boundary sqrt   bulk sqrt   scrambled sqrt
------------------------------------------------------
0.10        1.164           1.163       1.150
0.25        1.162           1.159       1.077
0.50        1.155           1.144       0.897
```

Linear controls:

```text
bandwidth   boundary linear   bulk linear   scrambled linear
------------------------------------------------------------
0.10        0.903             0.902         0.916
0.25        0.906             0.904         0.933
0.50        0.910             0.908         0.950
```

So the key black-hole-like contrast is stable:

```text
sqrt mass accelerates under physical removal;
linear mass decelerates.
```

## Local-Removal Advantage

Boundary and bulk removal beat scrambled removal in every matched sqrt-mass
case:

```text
sqrt boundary advantage over scrambled:
  mean = 0.119
  min  = 0.012
  max  = 0.263
  positive fraction = 1.00

sqrt bulk advantage over scrambled:
  mean = 0.114
  min  = 0.011
  max  = 0.252
  positive fraction = 1.00
```

For the linear controls the sign reverses:

```text
linear boundary advantage over scrambled:
  mean = -0.026
  positive fraction = 0.00

linear bulk advantage over scrambled:
  mean = -0.028
  positive fraction = 0.00
```

This is important. The local-removal advantage is not a generic artifact of
using boundary/bulk maps. It appears in the black-hole-like sqrt-mass case.

## Strongest Stress Point

At bandwidth `0.5`, scrambled sqrt removal actually decelerates:

```text
scrambled sqrt:
  mean acceleration = 0.897
```

while local removal still accelerates:

```text
boundary sqrt:
  mean acceleration = 1.155

bulk sqrt:
  mean acceleration = 1.144
```

This is the clearest evidence that the concrete local Hamiltonian/removal
structure matters.

The result is no longer merely:

```text
dim H_n = 2^n and M_n = sqrt(n) imply acceleration.
```

It is:

```text
with a local spin-chain Hamiltonian, physical removal maps preserve the
favorable W profile better than scrambled removal.
```

## Mechanism

The acceleration remains mostly sector-profile driven:

```text
boundary sqrt:
  W ratio tracks emitted power ratio;
  sector-W ratio is close to actual W ratio.
```

But the local structure affects the sector profile itself. Scrambling the
removal map weakens or destroys acceleration at larger bandwidth.

This differs from the random-block control, where boundary and scrambled
removal were indistinguishable.

## Current Verdict

Track E is now the best candidate model.

It has:

```text
1. area-law state count: dim H_n = 2^n;
2. black-hole-like mass relation: M_n = sqrt(n);
3. negative heat capacity;
4. concrete local Hamiltonian blocks;
5. physical shrinking maps;
6. matrix-element-derived emission;
7. robust acceleration for sqrt mass;
8. robust deceleration for linear mass;
9. a stable local-removal advantage over scrambled controls.
```

It still lacks:

```text
1. derived M_n = sqrt(n);
2. real horizon degrees of freedom;
3. full radiation history / Page turnover;
4. early-late radiation diagnostics.
```

But as a finite quantum evaporator with the thermodynamic black-hole backbone,
this is now much stronger than the earlier Track B area register.

## Recommended Next Step

Stop broadening parameter scans for the moment.

The next useful step is to integrate Track E into the paper-level structure:

```text
1. engineered shell: mechanism control;
2. variable-N Bose-Hubbard: natural shrinkage but wrong state count;
3. area register: right state count but abstract blocks;
4. variable-length spin chain: right state count plus concrete local dynamics.
```

Then decide whether to pursue:

```text
radiation-structure diagnostics
```

or:

```text
an n_max=11 scaling check.
```

