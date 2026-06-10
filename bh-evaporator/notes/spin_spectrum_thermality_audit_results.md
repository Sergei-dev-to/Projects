# Spin-Spectrum Thermality Audit Results

## Purpose

The autonomous spin-spectrum model emitted a hard-radiation spectrum that looked
too hard when compared with a pure Boltzmann target. This audit checks whether
that was a model failure or a target/diagnostic mismatch.

Script:

```text
sim/spin_spectrum_thermality_audit.py
```

The audit compares:

```text
1. final radiation-chain occupation;
2. time-integrated outward erosion current;
3. time-integrated matrix-element tendency;
4. pure Boltzmann target;
5. phase-space corrected Boltzmann targets;
6. first-step spin-spectrum density-of-states target;
7. first-step spin-spectrum matrix-element target.
```

The important change is item 2. Final occupation in a finite radiation chain can
be distorted by propagation and reabsorption. The outward-current diagnostic
measures the band-resolved erosion flow through the droplet/radiation coupling.

## Main Chain-3 Audit

Run:

```text
python sim/spin_spectrum_thermality_audit.py --case-name chain3_audit
```

Output:

```text
sim/data/spin_spectrum_thermality_audit.csv
```

Setup:

```text
L0 = 3
bands = 2, 3, 4, 5, 6
chain length = 3
basis dim = 185856
erosion edges = 1163295
overlap degree = 16
```

Measured distributions:

```text
quantity         omega=2  omega=3  omega=4  omega=5  omega=6
final occ        0.150    0.242    0.247    0.227    0.133
outward flux     0.151    0.206    0.245    0.229    0.170
matrix tendency  0.180    0.171    0.288    0.181    0.181
```

Comparison targets:

```text
target                 omega=2  omega=3  omega=4  omega=5  omega=6
Boltzmann p=0          0.650    0.230    0.081    0.029    0.010
phase-space p=1        0.516    0.274    0.129    0.057    0.024
phase-space p=2        0.369    0.293    0.184    0.102    0.052
spin DOS first-step    0.094    0.297    0.263    0.220    0.127
spin matrix first-step 0.094    0.299    0.275    0.212    0.120
```

Total-variation distances:

```text
diagnostic       Boltz p=0  phase p=1  phase p=2  spin DOS  spin matrix
final occ        0.500      0.398      0.270      0.070     0.085
outward flux     0.523      0.433      0.306      0.109     0.123
matrix tendency  0.529      0.439      0.311      0.165     0.160
```

## Overlap-Truncation Control

Run:

```text
python sim/spin_spectrum_thermality_audit.py \
  --case-name chain3_overlap32 \
  --overlap-degree 32 \
  --summary-csv sim/data/spin_spectrum_thermality_audit_chain3_overlap32.csv
```

Setup:

```text
basis dim = 185856
erosion edges = 1773645
```

Total-variation distances:

```text
diagnostic       phase p=2  spin DOS  spin matrix
final occ        0.265      0.069     0.081
outward flux     0.296      0.097     0.109
matrix tendency  0.313      0.169     0.166
```

Increasing the overlap degree changes the numbers mildly and preserves the main
ordering. The conclusion is not an artifact of keeping only 16 overlaps.

## Short-Chain Control

Run:

```text
python sim/spin_spectrum_thermality_audit.py \
  --case-name chain2_audit \
  --chain-length 2 \
  --summary-csv sim/data/spin_spectrum_thermality_audit_chain2.csv
```

Setup:

```text
basis dim = 86016
erosion edges = 775530
```

Total-variation distances:

```text
diagnostic       phase p=2  spin DOS  spin matrix
final occ        0.284      0.099     0.097
outward flux     0.307      0.095     0.097
matrix tendency  0.317      0.133     0.128
```

The shorter waveguide is less clean, but it gives the same qualitative answer.
The band distribution is much closer to the finite spin-spectrum prediction
than to the continuum thermal targets.

## Interpretation

The previous phrase "the spectrum is too hard" was incomplete. The emitted
spectrum is too hard relative to a continuum Boltzmann target at the
Schwarzschild-like temperature proxy. It is fairly close to the finite
spin-spectrum transition weights actually present in the Hamiltonian.

That means the current bottleneck is sharper:

```text
The autonomous Hamiltonian is generating the spectrum of its own finite droplet.
The finite droplet spectrum is not yet close to the continuum Hawking-like
thermal target.
```

This is good news for the Hamiltonian construction. The spectral failure is not
random and is not mainly a finite-chain occupation artifact. It is tied to the
finite internal density of states and transition matrix elements.

## What This Changes

Before this audit, the remaining thermality problem had several possible
causes:

```text
1. final-chain occupation was a bad proxy for emission;
2. finite waveguide reabsorption distorted the spectrum;
3. overlap truncation biased high-energy bands;
4. the erosion operator generated the wrong spectrum;
5. the pure Boltzmann comparison was the wrong benchmark;
6. the spin droplet was too small or too crude.
```

The audit largely weakens 1, 2, 3, and 4.

The live possibilities are now:

```text
1. pure Boltzmann is too austere a benchmark for this finite emitter;
2. the finite spin droplet has insufficient density-of-states resolution;
3. the sector spectra need a scaling limit before Hawking-like thermality
   appears;
4. the chosen spin Hamiltonian gives the wrong density-of-states shape.
```

## Next Large Step

The next useful step is not another occupation plot. It is a scaling audit of
the droplet spectrum:

```text
1. compute density-of-states slopes for each L sector;
2. measure whether those slopes approach the target beta(L);
3. test whether changing internal spectral scaling moves the spin target toward
   phase-space-corrected thermality;
4. run the same flux audit across a small parameter/seed grid.
```

If the spin-sector DOS target moves toward the thermal curve under a controlled
scaling, the autonomous route remains promising. If it does not, the model needs
a different internal Hamiltonian, not more radiation-chain tuning.
