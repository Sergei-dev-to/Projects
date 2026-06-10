# Autonomous Spin-Spectrum Multiband Results

## Purpose

The previous multiband model used an artificial internal energy ladder inside each droplet sector. It tested spectral emission, but the density of states was still engineered.

This step replaces that ladder with an actual spin-droplet Hamiltonian:

```text
H_total =
  direct_sum_L [4 sigma L + H_spin(L)]
  + H_rad_multiband
  + H_erosion .
```

The spin Hamiltonian is:

```text
H_spin(L) =
  h sum_i Z_i
  + J sum_<ij> Z_i Z_j
  + lambda sum_i X_i
  + small random Z fields .
```

Shell erosion is defined in the site basis:

```text
L x L sites = (L-1) x (L-1) inner core + shell sites
```

and then transformed into the energy eigenbasis of `H_spin(L)`. This is the important naturalness improvement: the erosion matrix is inherited from shell removal, not assigned as random eigenstate-to-eigenstate coupling.

Script:

```text
sim/autonomous_spin_spectrum_multiband.py
```

## Model

Default run:

```text
L0 = 3
Lmin = 1
q = 2
bands omega = 2, 3, 4, 5, 6
max hard quanta = 2
chain length per band = 2
initial state = Haar in a low internal-energy window
```

The spin spectra are centered and rescaled to a controlled internal width. The perimeter energy remains:

```text
E_L = 4 sigma L
```

so the black-hole-like equation of state still comes primarily from:

```text
S_micro(L) ~ L^2
E_L ~ L .
```

## Results

```text
case           dim     chain  final L  p(final)  Ehard  TV     minTV  Srad   S2     far   drift
main           86016   2      1.785    0.428     4.832  0.365  0.337  2.120  1.738  0.643 1.6e-13
low_window     86016   2      1.786    0.419     4.702  0.339  0.302  1.931  1.541  0.647 2.8e-13
wide_internal  86016   2      1.898    0.390     4.591  0.451  0.438  1.979  1.573  0.567 2.1e-13
integrable     86016   2      1.852    0.417     4.694  0.420  0.380  2.072  1.636  0.631 2.9e-13
chain3         185856  3      1.526    0.580     5.537  0.246  0.246  1.832  1.247  0.928 4.5e-13
```

The best case is `chain3`, which gives:

```text
final mean L                    1.526
final final-sector probability  0.580
final hard energy               5.537
TV to thermal target            0.246
core/radiation entropy          1.832
core/radiation Renyi-2          1.247
far-chain occupation            0.928
energy drift                    4.5e-13
```

Measured spectrum for `chain3`:

```text
omega:      2        3        4        5        6
measured:   0.198    0.258    0.239    0.197    0.107
thermal:    0.442    0.261    0.154    0.090    0.053
```

## Comparison To Artificial Ladder

The artificial-ladder multiband model gave:

```text
best untuned TV ~ 0.384
main flat-coupling TV ~ 0.497
```

The spin-spectrum model gives:

```text
main TV    = 0.365
chain3 TV  = 0.246
```

So the natural spin spectrum improves the hard-radiation spectrum without adding a Boltzmann coupling factor.

The spectrum is still too hard. High-energy bands remain overweighted compared with the thermal target. But the direction is clearly better:

```text
artificial ladder:
  high-energy dominated;

spin spectrum:
  lower-energy bands gain weight;

spin spectrum plus larger waveguide:
  substantially closer to thermal.
```

## Controls

The `integrable` control sets the transverse field and random fields to zero. It performs worse than the main chaotic spin case:

```text
main TV       = 0.365
integrable TV = 0.420
```

That supports the idea that noncommuting many-body dynamics helps, though the present test is too small to make a strong chaos claim.

The `wide_internal` control broadens the internal spectrum and worsens the result:

```text
wide_internal TV = 0.451
```

This tells us that merely adding a larger internal energy range is not enough. The location of the initial energy window and the shape of the density of states matter.

## Interpretation

This is a meaningful improvement over the artificial-ladder spectral model.

Achieved:

```text
actual spin-droplet spectrum: yes
site-basis shell-removal operator: yes
autonomous multiband radiation: yes
energy conservation: yes
shrinking: yes
emitted spectrum measured: yes
hard spectrum improved without Boltzmann coupling: yes
core/radiation entropy measured: yes
Renyi-2 measured: yes
```

Remaining gap:

```text
hard spectral thermality is improved but not solved.
```

The model still emits a spectrum hotter than the thermal target. This suggests that spectral thermality requires a better density of states, a larger droplet, a more physical radiation density of states, or all three.

## Why This Matters

The failure of the artificial-ladder model could have been dismissed as an artifact. The spin-spectrum model shows a more specific story:

```text
natural many-body structure helps,
chaotic/noncommuting structure helps,
larger outgoing phase space helps,
but the current finite droplet is still too small or too crude
to fully reproduce Hawking-like spectral thermality.
```

That is useful information. The autonomous model is no longer failing because the spectrum was assigned badly. It is now testing whether a simple many-body droplet spectrum is enough.

## Next Large Step

Update after the thermality audit:

```text
notes/spin_spectrum_thermality_audit_results.md
```

The "too hard" spectrum is now better understood. The emitted bands are far
from pure Boltzmann and phase-space-corrected Boltzmann targets, but they are
close to the actual finite spin-spectrum transition weights. For the chain-3
case:

```text
diagnostic       phase p=2  spin DOS  spin matrix
final occ        0.270      0.070     0.085
outward flux     0.306      0.109     0.123
matrix tendency  0.311      0.165     0.160
```

So the autonomous Hamiltonian is not producing a random hard spectrum. It is
approximately producing the spectrum implied by its finite internal density of
states and erosion matrix elements.

The next large step is therefore a scaling audit of the droplet spectrum:

```text
1. compute density-of-states slopes for each L sector;
2. check whether those slopes approach beta(L);
3. vary internal spectral scaling and spin parameters;
4. rerun the flux audit across seeds and parameters.
```

If the spin-sector DOS target approaches the thermal target under controlled
scaling, the autonomous route remains promising. If it does not, the internal
Hamiltonian is the thing to replace.
