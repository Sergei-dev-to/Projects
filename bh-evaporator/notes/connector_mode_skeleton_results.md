# Connector-Mode Skeleton Results

## Files

Design note:

```text
bh-evaporator/notes/connector_mode_evaporator.md
```

Counting script:

```text
bh-evaporator/sim/connector_mode_skeleton.py
```

## What Was Tested

This is not a Hamiltonian simulation.

It tests the thermodynamic skeleton:

```text
N sites;
one connector mode for each pair of sites;
S_N = N log d_site + N(N-1)/2 log d_conn;
M_N = mu N;
T_N = (dS/dM)^-1;
epsilon_N = eta T_N;
gamma_N ~ N^p T_N^q;
P_N = gamma_N epsilon_N.
```

The main questions:

```text
1. Does connector counting naturally give S ~ M^2?
2. Does it naturally give T ~ 1/M?
3. Does the core heat after one emission?
4. What rate exponents are needed for accelerating power?
```

## Main Counting Result

For connector-dominated entropy:

```text
S_N ~ N^2
```

and site-count mass:

```text
M_N ~ N.
```

Therefore:

```text
S ~ M^2
T ~ 1/M.
```

This is the first clean improvement over Track E.

Track E used:

```text
S_n ~ n
M_n ~ sqrt(n)
```

Connector model uses:

```text
S_N ~ N^2
M_N ~ N.
```

So the square moves from an imposed mass law into the active state count.

## Heating Condition

After:

```text
N -> N-1,
E_(N-1) = E_N - epsilon_N,
q_N -> q_(N-1),
```

the core heats if:

```text
epsilon_N / E_N < 1 - q_(N-1)/q_N.
```

For connector-dominated systems:

```text
1 - q_(N-1)/q_N ~ 2/N.
```

So the emitted subsystem can carry a thermal amount of energy and the core
still heats, because the mode count drops by order `N` connectors.

## Representative Runs

Command:

```text
python bh-evaporator/sim/connector_mode_skeleton.py --n-min 8 --n-max 128 --eta 1 --p-area 2 --q-temp 3
```

Result:

```text
S/M^2 relative variation = 2.15e-2
T*M relative variation   = 1.06e-2
heating holds for all N  = True
power smallN/largeN      = 204
```

Interpretation:

```text
Schwarzschild-like p=2, q=3 flux gives strong acceleration as N shrinks.
```

Larger emitted energy:

```text
eta = 10
```

still gives:

```text
heating holds for all N = True
```

on the tested range `N=8..128`.

## Acceleration Is Not Automatic

If the emission rate has too weak a temperature dependence:

```text
gamma ~ N^2 T
```

then:

```text
power smallN/largeN = 0.893
```

so power does not accelerate as `N` shrinks.

This is useful. The connector count naturally gives:

```text
S ~ M^2
T ~ 1/M
negative heat capacity
```

but the accelerating Hawking-like power law still requires a flux mechanism:

```text
gamma ~ area * T^3
epsilon ~ T
P ~ area * T^4 ~ 1/M^2.
```

So the next Hamiltonian question is precise:

```text
Can an incidence-local connector Hamiltonian plus radiation modes produce a
rate with sufficiently strong temperature dependence?
```

## What This Means

The connector model is not just another patch.

It gives a more natural architecture for the thermodynamic backbone:

```text
mass variable       = number of visible sites N;
entropy variable    = number of active connector modes ~ N^2;
evaporation step    = remove one site and decouple O(N) connectors;
heating mechanism   = lose fewer energy units than active modes;
radiation subsystem = emitted site plus connector cloud.
```

This directly addresses the matrix-literature lesson:

```text
emission dynamically reduces many off-diagonal connector degrees of freedom.
```

## Current Status

Established at counting level:

```text
S ~ M^2;
T ~ 1/M;
negative heat capacity along evaporation;
clear condition for heating;
clear condition for accelerating power.
```

Not established:

```text
Hamiltonian dynamics;
matrix-element-derived rates;
Page-like radiation entropy;
early/late radiation correlations;
whether the connector cloud makes radiation too large/trivial.
```

## Next Step

Do not immediately build a large simulation.

First define the smallest incidence-local Hamiltonian:

```text
site qubits;
connector qubits;
connector ij couples only to sites i and j;
emission separates site N plus connectors iN into radiation.
```

Then test one question:

```text
Does the spectrum / emission operator naturally make emitted energies scale
like T_N ~ 1/N?
```

If not, the connector model reproduces thermodynamics only at the counting
level.

