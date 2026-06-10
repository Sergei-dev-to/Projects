# Variable-N Bose-Hubbard Secular Kraus Results

## Synthesis note

The Track A result is summarized in the broader project synthesis:

```text
notes/project_synthesis_after_tracks.md
```

## Purpose

The variable-N population diagnostic showed accelerating particle-loss
evaporation. The next question was whether the result survives a
reduced-density quantum channel and whether core-radiation entropy grows.

This test does not track the full radiation history. It evolves the reduced
core density matrix using Kraus operators. If the global state is purified by
fresh emitted bins, then:

```text
S2(core) = S2(all radiation)
```

## Model

Script:

```text
sim/variable_n_bose_hubbard_kraus.py
```

Figure:

```text
step3_variable_n_kraus.pdf
```

Data:

```text
sim/data/variable_n_bose_hubbard_kraus_seed2468.npz
sim/data/variable_n_bose_hubbard_kraus_seed2469.npz
```

The core is the same variable-N Bose-Hubbard system:

```text
H_core = direct sum over N=8,7,6,5,4,3
```

with particle-loss transitions:

```text
b_i : H_N -> H_{N-1}
```

The Kraus channel is the secular dilation of the Markov rate process:

```text
K_0 = no emission
K_{N,alpha -> N-1,beta} = one particle-loss emission
```

The initial state is pure, supported on the same N=8 internal-energy window:

```text
[-18.5, -17]
```

Parameters:

```text
mu = 6
max emitted gap = 4
steps = 80
```

## Result

The acceleration survives.

Seed 2468:

```text
early emitted power  = 0.05376
middle emitted power = 0.07334
late emitted power   = 0.07698
mid / early          = 1.364
final mean N         = 5.567
peak S2(core)        = 3.956
```

Seed 2469:

```text
early emitted power  = 0.05251
middle emitted power = 0.07035
late emitted power   = 0.07458
mid / early          = 1.340
final mean N         = 5.640
peak S2(core)        = 3.848
```

The accessible core size also shrinks:

```text
effective dimension:
  initial = 1287
  final   = about 476-493

dimension entropy:
  initial = 7.160
  final   = about 5.80-5.85
```

The coarse path-temperature diagnostic is positive and finite at late time:

```text
T_path final = about 4.3
```

This is only a trajectory derivative of dimension entropy versus energy. It
should be treated as an interpretive diagnostic, not a full microcanonical
temperature theorem.

## Interpretation

This is the strongest Step 3 result so far.

The model now has:

```text
1. a natural many-body core;
2. a shrinking Hilbert space;
3. physical particle-loss operators;
4. decreasing energy;
5. accelerating emitted power;
6. growing core-radiation Renyi-2 entropy.
```

That is much closer to the desired black-hole phenomenology than the engineered
shell model alone.

## Caveats

Important limitations remain:

```text
1. The Kraus channel is secular. Each allowed transition is effectively a
   distinct emitted radiation label.

2. Full radiation history is not tracked, so this does not compute early/late
   mutual information.

3. The Page curve does not turn over in this 80-step run; S2(core) keeps rising.

4. The mass offset mu is still scanned/tuned.

5. Finite-size robustness remains open.
```

## Next Step

There are two sensible next tests:

```text
1. Run a parameter/size robustness check for the Kraus model.

2. Build a tiny full-radiation-tracking version to measure early/late
   correlations directly.
```

The first is cheaper and should come before tensor-network or full-history
tracking.

## Targeted robustness scan

Script:

```text
sim/scan_variable_n_kraus.py
```

Figure:

```text
step3_variable_n_kraus_scan.pdf
```

Data:

```text
sim/data/variable_n_bose_hubbard_kraus_scan.csv
```

Scan:

```text
mu in {5, 6, 7}
max emitted gap in {3, 4, 5}
initial windows [-18.5,-17] and [-20,-18]
seeds 2468 and 2469
```

Result:

```text
18 grouped settings across two seeds
7/18 have acceleration > 1.00 in both seeds
6/18 have acceleration > 1.05 in both seeds
5/18 have acceleration > 1.15 in both seeds
```

Best grouped case:

```text
mu=6, gap=4, init=[-18.5,-17]
min acceleration over seeds = 1.340
mean acceleration = 1.352
mean peak S2(core) = 3.90
mean final effective dimension = 484
mean final N = 5.60
```

Other robust cases:

```text
mu=5, gap=3, init=[-18.5,-17]:
  min acceleration = 1.271

mu=7, gap=5, init=[-18.5,-17]:
  min acceleration = 1.167

mu=6, gap=4, init=[-20,-18]:
  min acceleration = 1.161

mu=6, gap=3, init=[-20,-18]:
  min acceleration = 1.160
```

Interpretation:

```text
The effect is not a single-row accident. It survives nearby parameter choices,
but it is not universal across the scanned region.
```

The result is strongest near a matching between the mass offset and the allowed
emitted-energy bandwidth. Too narrow or mismatched emission windows decelerate.
That is physically reasonable: the particle-loss operator must expose the
growing lower-sector phase space instead of dumping the state too fast into
poorly connected regions.
