# Energy-Resolved Sector-Hamiltonian Results

## Question

The first sector-Hamiltonian evaporator generated acceleration, but its hard
emission spectrum was too narrow. The question here is whether an explicit
internal sector spectrum can fix the hard-radiation thermality problem while
preserving acceleration.

## Scripts And Data

Script:

```text
sim/sector_hamiltonian_energy_resolved.py
```

Main data:

```text
sim/data/sector_hamiltonian_energy_resolved_exp_seed2468.csv
sim/data/sector_hamiltonian_energy_resolved_exp_uniform_seed2468.csv
sim/data/sector_hamiltonian_energy_resolved_exp_uniform_two_seed.csv
sim/data/sector_hamiltonian_energy_resolved_flat_semicircle_seed2468.csv
```

## Model

The sector Hilbert space is unchanged:

```text
H_core = direct sum_n H_n
dim H_n = q^n
S_micro(n) = n log q
```

The mass laws are:

```text
M_n = alpha sqrt(n)
M_n = alpha n
```

The new ingredient is an internal spectrum inside each sector:

```text
E_{n,a} = M_n + epsilon_{n,a}
```

with three tested density-of-states profiles:

```text
flat
exponential
semicircle
```

The exponential profile is the important one. It gives each sector a local
density of states approximately proportional to:

```text
exp(beta_n epsilon)
```

over an energy window of order:

```text
width_x * T_n
```

Transition rates are still generated from matrix elements:

```text
Gamma_fi proportional to |<f,n-1|X_n|i,n>|^2 omega_fi^p
omega_fi = E_i^(n) - E_f^(n-1)
```

The hard-spectrum diagnostic bins:

```text
x = beta_n omega
```

and compares to:

```text
P(x) proportional to x^p exp(-x)
```

## First Result: Broad Spectrum Alone Is Insufficient

With exponential sector DOS and no within-sector rethermalization, the hard
spectrum becomes close to thermal, but the evaporation decelerates.

For seed `2468`, scrambled shrinkage:

```text
mass   DOS           width_x   power   jump    omega   TV
sqrt   exponential   2         0.656   0.673   0.974   0.094
sqrt   exponential   4         0.663   0.662   1.002   0.036
sqrt   exponential   8         0.664   0.661   1.003   0.036
```

Here:

```text
power = mid/early emitted power
TV    = total-variation distance from the thermal x spectrum
```

So the internal DOS can fix the hard-spectrum shape, but the state falls into
lower-emission parts of the sector spectrum and the power drops.

## Second Result: Rethermalization Restores Acceleration

The next diagnostic applies complete within-sector mixing after each emission
step:

```text
p_n(a) -> P_n / dim H_n
```

This is a simple stand-in for fast scrambling / rethermalization inside the
remaining core sector.

With exponential DOS plus within-sector mixing, the square-root mass law gives
both acceleration and a near-thermal hard spectrum.

Two seeds, local and scrambled shrinkage, `width_x = 4`:

```text
seed   operator    mass   power   jump    omega   TV
2468   local       sqrt   1.094   1.044   1.048   0.054
2468   scrambled   sqrt   1.108   1.049   1.056   0.054
2469   local       sqrt   1.102   1.047   1.053   0.055
2469   scrambled   sqrt   1.087   1.041   1.044   0.054
```

Grouped over two seeds:

```text
operator    mass     width_x   power   jump    omega   TV
local       sqrt     2         1.104   1.046   1.056   0.078
scrambled   sqrt     2         1.101   1.045   1.054   0.079
local       sqrt     4         1.098   1.045   1.051   0.055
scrambled   sqrt     4         1.097   1.045   1.050   0.054
local       sqrt     8         1.097   1.045   1.050   0.055
scrambled   sqrt     8         1.096   1.045   1.049   0.055
```

The linear mass-law control stays close to non-accelerating while also having a
good spectrum:

```text
operator    mass     width_x   power   jump    omega   TV
local       linear   4         0.988   0.995   0.993   0.051
scrambled   linear   4         0.988   0.995   0.993   0.049
local       linear   8         0.987   0.995   0.992   0.049
scrambled   linear   8         0.987   0.995   0.992   0.048
```

## Interpretation

This gives a sharper mechanism:

```text
1. The black-hole-like mass law supplies negative heat capacity.
2. The energy-resolved sector DOS supplies a thermal hard spectrum.
3. Fast within-sector mixing prevents emission from cooling the sector into
   low-rate states.
4. The square-root mass law then accelerates; the linear control remains near
   flat or mildly decelerating.
```

This is the strongest version of the sector-Hamiltonian branch so far.

The result can now be stated as:

```text
energy-resolved sectors plus rethermalization generate local hard thermality
and accelerating evaporation for the black-hole-like mass law.
```

## Remaining Caveat

The within-sector mixing step is still a modeled ingredient.

In a fully microscopic Hamiltonian, this should arise from chaotic/scrambling
intra-sector dynamics. The current diagnostic replaces that dynamics by the
idealized map:

```text
p_n(a) -> P_n / dim H_n
```

So the next natural target is:

```text
replace the explicit within-sector mixing map with Hamiltonian scrambling
inside each H_n and check whether the same acceleration and thermal spectrum
survive.
```

That is now a well-posed next step, because we know exactly what the scrambling
has to accomplish.
