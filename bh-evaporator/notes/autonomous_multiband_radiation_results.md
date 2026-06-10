# Autonomous Multiband Radiation Results

## Purpose

The previous autonomous droplet Hamiltonian used monoenergetic hard quanta. That was enough to test autonomous shrinkage and information flow, but it could not test hard spectral thermality.

This step adds a multiband hard-radiation sector:

```text
hard mode = (band, position)
H_rad = sum_b omega_b n_b + band-preserving hopping
```

and an erosion coupling:

```text
stage L -> stage L-1 + shell record + one hard quantum in band b .
```

The coupling is filtered by energy detuning:

```text
exp[-(Delta E)^2 / (2 width^2)]
```

It does not use a Boltzmann factor. Therefore the hard spectrum is measured rather than imposed.

Script:

```text
sim/autonomous_multiband_radiation.py
```

Data:

```text
sim/data/autonomous_multiband_summary_main.csv
sim/data/autonomous_multiband_summary_wide_detuning.csv
sim/data/autonomous_multiband_summary_low_energy.csv
sim/data/autonomous_multiband_summary_inverse_omega.csv
sim/data/autonomous_multiband_summary_inverse_sqrt.csv
```

## Model

The current runs use:

```text
L0 = 3
Lmin = 1
q = 2
bands omega = 2, 3, 4, 5, 6
chain length per band = 3
max hard quanta = 2
basis dimension = 185856
```

The droplet sectors retain:

```text
E_L = 4 sigma L
S_micro(L) = L^2 log q
```

To make multiple emitted energies possible while keeping energy conservation meaningful, each droplet sector also has a small internal energy ladder assigned across core microstates. A transition can emit different `omega_b` by changing the internal droplet energy.

## Main Flat-Coupling Result

Main case:

```text
detuning width = 0.75
band coupling profile = flat
initial state = Haar over the initial core
```

Summary:

```text
final mean L                    1.834
final final-sector probability  0.373
final hard energy               5.146
final chain-far occupation      0.714
energy drift                    9.2e-14
TV to thermal target            0.497
```

Measured band probabilities:

```text
omega:      2        3        4        5        6
measured:   0.081    0.172    0.250    0.244    0.252
thermal:    0.491    0.260    0.138    0.073    0.039
```

The model emits and shrinks, but the spectrum is too hard. It puts too much weight in the high-energy bands.

## Controls

```text
case             final L  p(final)  Ehard  TV     min TV  far occ.  drift
main_flat        1.834    0.373     5.146  0.497  0.480   0.714     9.2e-14
wide_detuning    1.612    0.496     6.157  0.455  0.453   0.889     8.7e-14
low_energy_init  1.567    0.560     5.927  0.384  0.384   0.897     2.3e-13
inverse_omega    2.182    0.217     3.050  0.322  0.233   0.457     2.4e-13
inverse_sqrt     1.876    0.357     4.499  0.390  0.362   0.657     2.5e-13
```

What the controls show:

```text
wide detuning:
  improves evaporation but keeps the spectrum too hard;

low internal-energy initialization:
  improves both evaporation and spectral TV, but the spectrum remains too hard;

inverse-omega coupling:
  improves spectral TV, but substantially weakens evaporation;

inverse-sqrt coupling:
  gives an intermediate tradeoff.
```

The inverse-omega case is diagnostic rather than a claimed success. It shows that a low-energy bias in the coupling can move the spectrum toward the thermal target, but the current minimal model does not generate the thermal spectrum from flat local couplings alone.

## Interpretation

This is a useful partial result.

The multiband autonomous Hamiltonian successfully tests something the monoenergetic model could not test:

```text
autonomous multiband radiation: yes
energy-conserving spectral emission: yes
droplet shrinkage with multiband radiation: yes
measured hard spectrum: yes
thermal hard spectrum from flat coupling: no
thermal hard spectrum with simple low-energy bias: improved but incomplete
```

The main lesson is that hard spectral thermality is a real constraint. It does not automatically follow from:

```text
area entropy,
perimeter energy,
sparse scrambling,
outgoing radiation phase space,
and autonomous erosion.
```

The minimal multiband model emits a spectrum that is too hard. Getting closer to thermal requires either a better internal density of states, a more physical radiation density of states, or a coupling profile with low-energy preference.

## Consequence For The Project

The current autonomous model can honestly claim:

```text
autonomous non-gravitational evaporation,
negative heat capacity,
shrinking state count,
outgoing radiation,
unitary evolution,
finite-size Page-like information diagnostics.
```

It cannot yet honestly claim:

```text
Hawking-like hard spectral thermality.
```

That is now the main remaining physics gap.

## Next Large Step

The next large step should target the source of the spectrum, not the erosion bookkeeping.

The best options are:

```text
1. Replace the artificial internal energy ladder with a controlled many-body
   droplet density of states and rerun the multiband spectral test.

2. Add a radiation density of states appropriate to a 2D boundary emitter,
   so the number of outgoing modes grows with energy in a specified way.

3. Derive or motivate a simple local coupling profile and test whether it
   gives a near-thermal spectrum without fitting band-by-band probabilities.
```

The pass condition should remain strict:

```text
thermal-looking hard radiation should be measured from H_total, not assigned
through a Boltzmann coupling.
```
