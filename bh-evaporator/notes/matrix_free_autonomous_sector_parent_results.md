# Matrix-Free Autonomous Sector-Parent Results

## Question

Can we directly simulate the autonomous parent of the successful sector model
without building the full Hamiltonian matrix?

The target Hamiltonian is

```text
H_total = H_core + K_scramble + H_rad + H_int .
```

This is the formal autonomous parent of the sector-Hamiltonian model that
already passed the secular tests for hard thermality, acceleration, and
Hamiltonian intra-sector scrambling.

## Build Spec

Specification note:

```text
notes/autonomous_sector_parent_build_spec.md
```

Script:

```text
sim/matrix_free_autonomous_sector_parent.py
```

The script implements `H_total @ psi` as a matrix-free action and wraps it as a
SciPy `LinearOperator` for Krylov evolution with `expm_multiply`.

## Technical Result

The matrix-free refactor works.

The first naive edge-loop action timed out at the smoke-test size.  After
vectorizing the edge action, the same run finished in seconds.

Default smoke parameters:

```text
n = 3..5
q = 2
mass law = sqrt
max emitted quanta = 2
mode x values = 0.5,1,1.5,2,3,5
mode copies = 2
dim = 4424
edges = 49725
emission edges = 34241
```

Summary:

```text
mean n:             5.000 -> 4.406
radiation energy:   0.000 -> 2.260
max outward power:  0.759
mean flux TV:       0.200
min flux TV:        0.157
energy drift:       5.51e-13
```

So the autonomous parent now has a direct time-independent-Hamiltonian smoke
test with:

```text
energy conservation;
sector shrinkage;
radiation energy growth;
outward flux;
flux spectrum close to the thermal x-distribution at small size.
```

## Controls At Same Size

Linear mass-law control:

```text
mean n:             5.000 -> 4.541
radiation energy:   0.000 -> 6.782
max outward power:  4.873
mean flux TV:       0.185
energy drift:       3.54e-12
```

No-scrambling control:

```text
mean n:             5.000 -> 4.347
radiation energy:   0.000 -> 2.170
max outward power:  0.653
mean flux TV:       0.189
energy drift:       6.36e-13
```

These controls do not yet isolate the black-hole-like mechanism.  The linear
case also shrinks, and the no-scrambling case does not fail cleanly in this
small window.

This means the current smoke test validates the autonomous parent embedding,
but not the full phenomenological package.

## Interpretation

This is a meaningful step toward the stronger result.

Before this script, the successful sector model existed at the secular level,
and the direct autonomous test was too tiny.  Now the same abstract sector
parent can be evolved matrix-free with thousands of states and tens of
thousands of transition edges.

The current small run already gets close to the thermal flux diagnostic:

```text
mean TV about 0.20;
best TV about 0.16.
```

That is not yet as good as the sector-isometry result, but it is much better
than the autonomous droplet multiband spectrum.

## What Does Not Yet Work

The square-root versus linear distinction is not established in the autonomous
parent smoke test.  The linear case emits much larger radiation energy because
its sector gaps are larger in the current parameterization.  To compare power
fairly, the next run must normalize the radiation mode scale and diagnostic
window more carefully.

The no-scrambling control is also not decisive.  With only one or two
emissions and a small sector range, the initial Haar state already supplies
some typicality.

Entropy diagnostics are not implemented in this matrix-free script yet.  The
first target was the autonomous thermodynamic/spectral behavior.

## Next Step

The next useful run is not another tiny smoke test.  It is the first
meaningful sector-parent target:

```text
n = 4..7
q = 2
max emitted quanta = 3
mode copies = 2 or 3
matrix-free action
sqrt and linear controls with matched beta*x radiation modes
```

Before that run, improve the comparison setup:

```text
1. choose radiation modes separately for each mass law using local beta_n;
2. normalize time or coupling so early flux is comparable;
3. record early/mid/late power ratios rather than only max power;
4. add a basis-state initial condition to make scrambling controls sharper.
```

## Current Status

The stronger autonomous result is now technically within reach.  The
matrix-free parent simulator has passed the first embedding test:

```text
single H_total;
direct exp(-i H_total t);
energy conservation;
radiation flux;
sector shrinkage;
near-thermal small-size flux spectrum.
```

The remaining question is whether the same implementation can scale to a
window where the square-root mass law, linear control, and scrambling control
separate cleanly.

## First Matched Benchmark

After adding early/mid/late diagnostics, we ran the first meaningful matched
comparison:

```text
n = 4..7
q = 2
max emitted quanta = 2
mode copies = 2
time window = 0..80
seeds = 2468, 1357, 9753
```

The linear control was matched to the square-root case by equating the initial
downward inverse temperature at `n_max = 7`.  With `alpha_sqrt = 8`, this gives

```text
alpha_linear = 1.5700925462513027 .
```

Aggregate results:

```text
case                         <Delta n>   E_rad(final)   P_late/P_early   mean flux TV
sqrt + scrambling             0.919        2.882          1.019            0.165
linear matched + scrambling   0.939        2.847          0.991            0.200
sqrt, no scrambling           0.891        2.484          0.919            0.179
```

Per-seed late/early power ratios:

```text
sqrt + scrambling:           1.043, 1.047, 0.966
linear matched + scrambling: 0.987, 0.975, 1.012
sqrt, no scrambling:         0.899, 0.924, 0.933
```

Energy drift stayed at the `10^-12` level or below.

## Interpretation Of The Matched Benchmark

This is the strongest autonomous-parent evidence so far.

The same time-independent Hamiltonian framework now gives, without a staged
sector map:

```text
energy conservation;
nearly one-sector shrinkage over the window;
radiation energy growth;
hard flux spectrum with TV about 0.16--0.20;
a consistent no-scrambling degradation of late power;
a mild square-root-over-linear power trend after initial-temperature matching.
```

The square-root/linear distinction is not yet decisive.  It appears in the
three-seed average, but one seed weakly flips the ordering.  The no-scrambling
contrast is cleaner: all three no-scrambling runs lose late power.

The current result therefore supports the autonomous parent as a real model,
not merely a formal rewrite of the sector map.  It does not yet establish the
full black-hole-like acceleration package at publication strength.

## Next Large Benchmark

The next run should increase the radiation phase space and diagnostic window,
not add another small variant.  The target is:

```text
n = 4..7 or 5..8
max emitted quanta = 3
mode copies = 2
same matched-alpha comparison
three seeds if runtime allows
```

The purpose is to decide whether the weak square-root/linear separation is a
finite-radiation artifact or a structural limitation of the autonomous parent.
