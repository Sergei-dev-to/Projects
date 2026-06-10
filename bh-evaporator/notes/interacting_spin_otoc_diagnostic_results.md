# Interacting Spin OTOC Diagnostic Results

## Question

The entanglement-growth diagnostic showed that the Margulis algebraic graph
scrambles faster than a local grid.

The next check is an operator-spreading diagnostic:

```text
C_ij(t) = (1 - Re F_ij(t)) / 2,
```

where `F_ij(t)` is the Pauli OTOC for:

```text
W_i = Z_i,
V_j = Z_j.
```

Plainly:

```text
kick one qubit and ask when another qubit notices.
```

## Script

```text
sim/interacting_spin_otoc_diagnostic.py
```

Outputs:

```text
sim/data/interacting_spin_otoc_rows.csv
sim/data/interacting_spin_otoc_summary.csv
```

## Method

The diagnostic estimates the infinite-temperature OTOC using random state
sampling:

```text
F_ij(t) ~= <psi| U^dag Z_i U Z_j U^dag Z_i U Z_j |psi>.
```

The same Trotterized random Heisenberg dynamics is used as in the interacting
spin Page test.

Because this is expensive, the cleaned first pass uses:

```text
L0 = 4
three seeds
one random state sample
dt = 0.5
targets = {1, 2, 3, 5, 10, 15}
source = 0
```

So this is a coarse OTOC probe, not a precision chaos calculation.

## Results

```text
grid
t=0     mean=0.000   max=0.000   opposite=0.000   frac>0.25=0.000
t=0.5   mean=0.016   max=0.098   opposite=0.000   frac>0.25=0.000
t=1     mean=0.076   max=0.222   opposite=0.000   frac>0.25=0.000
t=2     mean=0.208   max=0.388   opposite=0.000   frac>0.25=0.500

margulis
t=0     mean=0.000   max=0.000   opposite=0.000   frac>0.25=0.000
t=0.5   mean=0.054   max=0.181   opposite=0.000   frac>0.25=0.000
t=1     mean=0.150   max=0.331   opposite=0.056   frac>0.25=0.333
t=2     mean=0.376   max=0.450   opposite=0.363   frac>0.25=1.000

complete
t=0     mean=0.000   max=0.000   opposite=0.000   frac>0.25=0.000
t=0.5   mean=0.056   max=0.110   opposite=0.110   frac>0.25=0.000
t=1     mean=0.245   max=0.302   opposite=0.237   frac>0.25=0.333
t=2     mean=0.473   max=0.484   opposite=0.458   frac>0.25=1.000
```

Here `opposite` means the target qubit in the opposite corner of the `4 x 4`
label grid.

## Interpretation

The ordering is the expected one:

```text
grid:
  slowest operator spreading;

margulis:
  faster than grid, including to the opposite corner;

complete:
  fastest control.
```

The opposite-corner diagnostic is especially clean:

```text
t=1:
  grid      0.000
  margulis  0.056
  complete  0.237

t=2:
  grid      0.000
  margulis  0.363
  complete  0.458
```

So the Margulis graph is not only producing faster entanglement growth; it also
spreads local operators faster across the system.

## Caveats

This is a first-pass OTOC:

```text
three seeds;
one random-state sample per seed;
coarse Trotter step;
six targets.
```

It should not be read as a Lyapunov exponent calculation.

But it is enough to support the qualitative F14 claim:

```text
the algebraic graph gives faster operator spreading than the local grid under
the same interacting spin dynamics.
```

## Status

This strengthens F14 further:

```text
F14 = P, but now supported by Page behavior, entanglement growth, and OTOC-like
operator spreading.
```

The remaining work is scaling and naturalness, not the existence of a
scrambling signal.
