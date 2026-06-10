# Tiny Autonomous Sector-Evaporator Results

## Question

Can the successful sector-Hamiltonian ingredients be embedded in one
time-independent Hamiltonian and evolved directly?

## Script And Data

Script:

```text
sim/tiny_autonomous_sector_evaporator.py
```

Data:

```text
sim/data/tiny_autonomous_sector_evaporator_t60_summary.csv
sim/data/tiny_autonomous_sector_evaporator_t60_timeseries.csv
```

## Hamiltonian

The simulated Hamiltonian is:

```text
H_total = H_core + K_scramble + H_rad + H_int
```

with:

```text
H_core:
  energy-resolved sectors n = 2,3,4
  dim H_n = 2^n
  M_n = alpha sqrt(n)

K_scramble:
  none, dense random, or expander-like intra-sector mixer

H_rad:
  six one-particle radiation modes

H_int:
  shrinkage coupling |n,a> -> |n-1,b> + one radiation quantum
  with a smooth resonance window
```

The total Hilbert-space dimension in the default run is:

```text
124
```

## Result

Short-window run:

```text
t_max = 60
time points = 81
seed = 2468
```

Summary:

```text
mixer      dim  Erad    Nrad   <n>    TV     dE late/early  H drift
none       124  2.562   0.545  3.455  0.275  0.329         1.7e-13
dense      124  1.969   0.471  3.529  0.199  0.335         1.5e-13
expander   124  1.246   0.350  3.650  0.384  0.056         1.4e-13
```

Here:

```text
Erad = final radiation energy
Nrad = final expected number of emitted radiation quanta
<n>  = final mean core sector
TV   = final radiation-spectrum distance from thermal beta omega bins
H drift = max-min expectation value of H_total
```

The dense-mixer trajectory illustrates the behavior:

```text
time   core energy   rad energy   <n>     Nrad   p(top sector)
0      15.982        0.000        4.000   0.000  1.000
15     13.622        2.592        3.442   0.558  0.499
30     14.356        1.698        3.582   0.418  0.651
60     14.050        1.969        3.529   0.471  0.608
```

## Interpretation

The tiny autonomous test succeeds at the basic embedding check:

```text
H_total is time independent;
H_total energy is conserved to numerical precision;
radiation modes become populated;
the mean core sector decreases;
the hard spectrum is finite and measurable.
```

The run also shows the expected limitation of a tiny closed radiation bath:

```text
coherent reabsorption and recurrences appear quickly.
```

That is why the tiny run should be read as a smoke test for the autonomous
Hamiltonian construction. The final evaporation-curve diagnostic needs a
larger or effectively absorbing radiation bath.

## Current Status

This gives the chain:

```text
autonomous Hamiltonian candidate
  -> weak-coupling/secular reduction
  -> successful sector-Hamiltonian model
```

and one direct tiny simulation showing that the autonomous Hamiltonian can be
assembled and evolved.

The next technical obstacle is the radiation bath. A larger or effectively
absorbing bath is needed before the autonomous simulation can show a clean
multi-step evaporation curve without coherent returns.
