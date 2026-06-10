# Explicit Bath-Hamiltonian Emission Results

## Purpose

Replace the assigned bath-degeneracy table with a concrete finite bath
Hamiltonian spectrum.

Previous step:

```text
choose integer bath degeneracies N_h to approximate the target hard-bin
distribution.
```

This diagnostic:

```text
constructs explicit finite bath spectra;
counts bath states in energy bins;
multiplies those counts by the core microcanonical entropy ratio;
compares the resulting emission distribution to the golden-rule target.
```

## Script

```text
sim/explicit_bath_hamiltonian_emission.py
```

Output:

```text
sim/data/explicit_bath_hamiltonian_bins.csv
sim/data/explicit_bath_hamiltonian_summary.csv
```

## Key Correction

The bath does not need to reproduce the whole emission distribution by itself.

The golden-rule structure is:

```text
Gamma(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)].
```

So the bath Hamiltonian supplies:

```text
rho_bath(omega),
```

while the core supplies:

```text
exp[Delta S_core].
```

An initial version that asked bath counts alone to reproduce the full target
badly overweighted high energies. After applying the core entropy-ratio
factor, the bath-spectrum test becomes meaningful.

## Spectra Tested

```text
linear oscillator:
  many-occupation states built from equally spaced modes.

quadratic oscillator:
  many-occupation states built from quadratic mode energies.

box2d:
  one-particle two-dimensional box / momentum-lattice spectrum
  E_n ~ sqrt(nx^2 + ny^2).
```

The `box2d` case is the physically closest to an emitted hard quantum in a
2D exterior bath.

## Results

For `L = 8,16,32,64`, `bin_count = 8`, `bath_dim = 2`:

```text
spectrum    L1 error       mean omega / target   P / target     logP/logM slope
--------------------------------------------------------------------------------
linear      0.43-0.46      1.47-1.49             3.17-3.33      -2.073
quadratic   0.34           0.80                  0.51           -2.049
box2d       0.027-0.029    0.970-0.975           0.914-0.928    -2.043
```

The 2D-box bath is the useful case:

```text
L=8:
  L1 = 0.029, max error = 0.014, P/target = 0.914

L=64:
  L1 = 0.027, max error = 0.013, P/target = 0.928

logP/logM slope:
  -2.043
```

## Interpretation

This is a real F7 improvement.

The emission distribution can be generated from:

```text
explicit one-particle 2D bath spectrum
+ core entropy-ratio factor
```

rather than from a hand-built degeneracy table.

The result is not perfect:

```text
the finite 2D box slightly underestimates the mean emitted energy;
P/target is about 0.92 rather than 1;
the slope is -2.043 rather than exactly -2.
```

But those errors are small compared with the oscillator alternatives, and the
scaling law is intact.

## Explicit-Hard Register Check

The explicit hard-register simulator was also run with this `box2d` bath
source.

Aggregate results:

```text
bath source       scrambler   deficit   max D_hard   hard-S error   first old/new MI
------------------------------------------------------------------------------------
finite degeneracy margulis    0.876     1.77e-02     8.21e-04       3->2
finite degeneracy grid        0.874     1.54e-02     5.71e-04       3->2
finite degeneracy none        9.011     2.59e-01     1.87e-01       none

box2d             margulis    0.876     1.66e-02     7.16e-04       3->2
box2d             grid        0.874     1.43e-02     5.09e-04       3->2
box2d             none        9.011     2.40e-01     1.66e-01       none
```

This says:

```text
1. replacing the degeneracy table by a 2D-box bath spectrum does not break
   the explicit-hard-register result;
2. scrambled runs remain close to hard-local thermality;
3. no-scrambling still fails.
```

## What This Does Not Yet Prove

Remaining caveats:

```text
1. The bath Hamiltonian is still chosen to be a 2D one-particle box.
2. The level spacing is chosen proportional to T_L.
3. The hard-register test still uses compressed d_hard = 2.
4. This is not a full bath interacting autonomously over time.
```

The main gain is narrower but important:

```text
the bath density can come from an explicit finite spectrum rather than an
assigned degeneracy table.
```

## Status Change

Before:

```text
F7 = P:
  finite bath degeneracies approximate the desired weights.
```

After:

```text
F7 = stronger P:
  a concrete 2D-box bath Hamiltonian spectrum produces the weights with small
  finite-size error and preserves the M^-2 power law.
```

Do not upgrade to `Y` yet, because the bath is still inserted as a designed
external module.

## Next Step

The next natural target is not another bath-density fit.

It is:

```text
make the shell shrinkage trigger less staged.
```

Reason:

```text
emission is now supported by an explicit bath spectrum;
hard radiation is now explicit at small size;
the remaining unnatural piece is the threshold L -> L-1 update.
```

