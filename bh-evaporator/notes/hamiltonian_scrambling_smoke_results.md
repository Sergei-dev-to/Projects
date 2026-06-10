# Hamiltonian Scrambling Before Erosion: Smoke Results

## Purpose

Test the next naturalness step:

```text
fixed local Floquet circuit -> fixed local Hamiltonian
```

The question is whether a time-independent nearest-neighbor Hamiltonian can mix
the shell enough before erosion, at least in the small cases where the previous
product-state failures were clear.

## Script

```text
sim/hamiltonian_scrambling_before_erosion.py
```

Smoke outputs:

```text
sim/data/hamiltonian_scrambling_before_erosion_smoke.csv
sim/data/hamiltonian_scrambling_before_erosion_smoke_summary.csv
sim/data/hamiltonian_scrambling_before_erosion_smoke4.csv
sim/data/hamiltonian_scrambling_before_erosion_smoke4_summary.csv
```

Commands:

```text
python sim/hamiltonian_scrambling_before_erosion.py --smoke --seeds 1 \
  --out sim/data/hamiltonian_scrambling_before_erosion_smoke.csv \
  --summary-out sim/data/hamiltonian_scrambling_before_erosion_smoke_summary.csv

python sim/hamiltonian_scrambling_before_erosion.py --smoke --seeds 4 \
  --out sim/data/hamiltonian_scrambling_before_erosion_smoke4.csv \
  --summary-out sim/data/hamiltonian_scrambling_before_erosion_smoke4_summary.csv
```

## Setup

The smoke test uses:

```text
L0 = 3
d_hard = 2
q = 2
layout = edge_fixed
term_kind = flux_conserving
times = 0, 4
```

The Hamiltonian is:

```text
H_mix = sum_<ij> h_ij
```

where each `h_ij` is a fixed random Hermitian two-plaquette term, block diagonal
in total flux mod `q`.

Before each erosion step:

```text
|psi> -> exp(-i H_mix t) |psi>.
```

Then the usual structured erosion channel is applied.

This is still in plaquette-flux variables, not link variables.

## Result

The smoke test is positive.

For the two known failure modes:

```text
basis_all + clock
uniform_all + shift
```

the Hamiltonian evolution makes the shell locally mixed enough that the hard
radiation becomes close to thermal and hard+soft early/late correlations become
nonzero.

Four-seed summary:

```text
initial      channel  t    S_shell  purity  maxD   I_pair  S_h/thermal
basis_all    clock    0.0   0.000   1.000   0.443   0.000  0.000/0.582
basis_all    clock    4.0   2.162   0.136   0.071   3.634  0.571/0.582

uniform_all  shift    0.0   0.000   1.000   0.443   0.000 -0.000/0.582
uniform_all  shift    4.0   2.099   0.153   0.039   3.525  0.580/0.582
```

The complementary non-failing channels remain fine:

```text
basis_all + shift:
  maxD 0.029 at t = 4

uniform_all + clock:
  maxD 0.069 at t = 4
```

So the result is not only that the entropy increases; the hard marginal is also
close to the intended thermal distribution.

## Interpretation

This passes the immediate Hamiltonian smoke test.

The previous positive result did not require:

```text
fresh random gates each layer;
or even a fixed Floquet circuit.
```

At least in the smallest exact system, a fixed local flux-conserving Hamiltonian
can do the required shell mixing.

This further narrows the scrambling assumption:

```text
old:
  assume a locally mixed shell.

then:
  a fixed local Floquet circuit can make the shell locally mixed.

now:
  a fixed local flux-conserving Hamiltonian can make the shell locally mixed in
  the smoke test.
```

## What This Does Not Yet Prove

This is not yet a full Hamiltonian evaporator.

Limitations:

```text
1. The scan is a smoke test, not a broad parameter study.
2. It uses L0 = 3 only.
3. The Hamiltonian terms are random Hermitian local terms.
4. The Hamiltonian is local in plaquette-flux variables, not derived from link
   operators.
5. The hard emission probabilities are still imposed thermally.
6. The boundary tension energy and H_mix energy are not yet one unified
   microscopic Hamiltonian.
```

The result is therefore:

```text
fixed local Hamiltonian scrambling is sufficient in the smallest exact failure
test.
```

Not:

```text
the full evaporator follows from a natural Hamiltonian.
```

## Computational Note

Dense Hamiltonian exponentiation is much more expensive than fixed Floquet
gates. The broad scan timed out. The useful next computational improvement is
to cache/eigendecompose `H_mix` once per seed and apply multiple times, or to
move to sparse/Krylov evolution.

## Next Step

There are two sensible options:

```text
1. Optimize the Hamiltonian script and run a broader time/seed/size scan.
2. Move from plaquette-flux Hamiltonian terms toward link-variable local
   gauge dynamics.
```

The pragmatic next step is option 1, because it tells us whether the smoke test
survives before we invest in the more microscopic link-variable model.

