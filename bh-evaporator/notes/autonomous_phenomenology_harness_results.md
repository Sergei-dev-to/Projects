# Autonomous Phenomenology Harness Results

## Purpose

The goal of this step was to stop testing isolated pieces and measure the black-hole-like phenomenology directly in the autonomous droplet Hamiltonian.

The harness builds:

```text
H_total = H_drop + H_hard + H_hop + H_scr + H_erosion
```

then evolves an initial state under:

```text
|psi(t)> = exp(-i H_total t) |psi(0)> .
```

It measures thermodynamic proxies, evaporation, radiation propagation, core/radiation entanglement, Renyi-2 entropy, hard-chain entropy, and emitted-shell mutual information.

Script:

```text
sim/autonomous_phenomenology_harness.py
```

Data:

```text
sim/data/autonomous_phenomenology_summary_main.csv
sim/data/autonomous_phenomenology_timeseries_main.csv
sim/data/autonomous_phenomenology_summary_controls.csv
sim/data/autonomous_phenomenology_timeseries_controls.csv
sim/data/autonomous_phenomenology_summary_basis_controls.csv
sim/data/autonomous_phenomenology_timeseries_basis_controls.csv
```

## Entropy Split

The autonomous Hilbert space is a direct sum over droplet-size sectors:

```text
H = direct_sum_L H_core(L) tensor H_rad_shells(L) tensor H_hard
```

The harness uses the natural coarse-grained split:

```text
core label      = (sector, core index)
radiation label = (sector, shell-radiation index, hard-chain state)
```

This treats the droplet-size sector as a macro record in the reduced entropy calculation. The resulting entropy is the sector-aware core/radiation von Neumann entropy. The corresponding Renyi-2 entropy is also recorded.

For the final two-shell sector, the shell radiation factor is split into:

```text
early shell = shell emitted in the first erosion event
late shell  = shell emitted in the second erosion event
```

and the harness computes the postselected mutual information:

```text
I(R_early : R_late)
```

inside the final sector.

## Main Result

Main case:

```text
L0 = 3
Lmin = 1
q = 2
chain length = 14
max hard quanta = 2
scramble mode = sparse
scramble strength = 0.25
erosion coupling = 0.50
chain hopping = 1.20
hard quantum energy = 4 sigma
initial state = Haar in the initial core
```

Summary:

```text
basis dimension                 162816
final mean L                    1.228
final final-sector probability  0.811
final hard energy               7.086
maximum hard energy             7.087
target two-shell hard energy    8.000
final far-chain occupation      0.862
maximum energy drift            2.9e-13
```

Entropy and information diagnostics:

```text
max core/radiation entropy      2.381
final core/radiation entropy    1.553
final core/radiation Renyi-2    1.103
final hard-chain entropy        3.828
final hard-chain Renyi-2        3.610
final postselected shell MI     1.334
maximum postselected shell MI   3.279
```

Time series:

```text
time    Lmean   Ehard   p(final)  S(core:rad)  S2(core:rad)  S(hard)  I(shells)  far occ.
0.000   3.000   0.000   0.000     0.000        0.000         0.000    0.000      0.000
13.333  1.321   6.715   0.746     1.740        1.255         3.467    1.652      0.945
26.667  1.237   7.053   0.808     1.557        1.110         3.712    1.435      0.916
40.000  1.253   6.989   0.791     1.617        1.149         3.790    1.359      0.868
80.000  1.228   7.086   0.811     1.553        1.103         3.828    1.334      0.862
```

Interpretation:

```text
autonomous two-shell evaporation: yes
outgoing hard radiation: yes
energy conservation: yes
core/radiation entanglement: yes
Renyi-2 diagnostic: yes
early/late shell correlation: yes
Page-like turnover: partial
hard spectral thermality: unresolved in this fixed-omega version
```

The core/radiation entropy rises and then decreases as the final sector becomes dominant. This is the right qualitative Page direction. It is still a small two-shell signal, so it should be described as Page-like behavior rather than a full Page curve.

## Controls

All controls use `L0 = 3`, `Lmin = 1`, `q = 2`, and `erosion coupling = 0.50`.

```text
case                    dim     chain  scramble  omega  final L  p(final)  Ehard  Smax   Sfinal  S2final  Shard  Ifinal
main_chain14            162816  14     sparse    4.0    1.23     0.811     7.09   2.38   1.55    1.10     3.83   1.33
short_chain5             24576   5     sparse    4.0    1.96     0.333     4.18   2.41   2.32    1.89     2.08   2.89
no_scramble_chain10      86016  10     none      4.0    1.70     0.541     5.21   2.23   1.98    1.58     2.85   2.02
weak_scramble_chain10    86016  10     sparse    4.0    1.63     0.580     5.50   2.23   1.95    1.54     2.93   2.01
wrong_energy_chain10     86016  10     sparse    2.0    1.82     0.354     2.37   2.52   2.52    2.20     2.34   2.80
```

The controls say:

```text
larger radiation waveguide:
  strongly improves evaporation;

resonant hard quantum energy:
  strongly improves evaporation;

scrambling for Haar initial states:
  has a modest effect on coarse evaporation, because the initial state already
  contains typicality;

wrong hard energy:
  suppresses final-sector transfer and emitted hard energy.
```

## Basis-State Scrambling Controls

The Haar controls do not strongly isolate scrambling because the initial state is already typical. A structured basis initial state gives a cleaner scrambling comparison:

```text
case                       dim    chain  scramble  final L  p(final)  Ehard  Sfinal  Ifinal
basis_sparse_chain10       86016  10     sparse    1.313    0.733     6.750  1.815   1.794
basis_no_scramble_chain10  86016  10     none      1.731    0.524     5.076  1.976   1.942
```

Sparse scrambling improves actual autonomous evaporation for the structured initial state:

```text
final L drop improvement: 1.731 -> 1.313
final-sector probability: 0.524 -> 0.733
hard energy:              5.076 -> 6.750
```

The entropy and shell-MI diagnostics are more subtle, because sector mixing and final-sector postselection contribute strongly at this small size.

## Current Status

The autonomous model now reaches the main target at a finite two-shell level:

```text
explicit Hilbert space: yes
time-independent H_total: yes
unitary evolution: yes
energy conservation: yes
shrinking state count: yes
S_micro ~ E^2 equation of state: yes
T ~ 1/E and C < 0: yes
autonomous outgoing hard radiation: yes
two-shell evaporation: yes
larger radiation phase space improves evaporation: yes
hard quantum resonance matters: yes
core/radiation entropy measured: yes
Renyi-2 entropy measured: yes
early/late shell mutual information measured: yes
```

The remaining important gaps are:

```text
1. Hard spectral thermality.
   The current autonomous radiation carries fixed-energy quanta. It can test
   emission, propagation, and information flow, but it cannot yet test a
   thermal energy spectrum. A multiband radiation waveguide is needed.

2. Larger size or scaling support.
   The strongest autonomous result is `L0 = 3`. The effective model already
   supports larger bookkeeping, but exact autonomous state-vector simulation
   becomes expensive quickly.

3. Stronger Page-curve evidence.
   The current entropy signal rises and falls over two shells. That is a
   Page-like turnover, not a full many-step Page curve.

4. Cleaner subsystem split.
   The sector-aware entropy split is physically natural for this staged
   Hamiltonian, but a cleaner fixed tensor-product embedding would make the
   entanglement diagnostics easier to defend.
```

## Bottom Line

This is now an autonomous non-gravitational quantum model where a substantial part of the black-hole evaporation phenomenology is measured rather than imposed.

The result is not yet the full goal. The missing piece is no longer autonomous shrinkage. The missing piece is spectral radiation thermality plus stronger finite-size/Page-curve support.
