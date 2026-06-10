# Many-Cycle Evaporation Tracker Results

## Question

Can we track the full evaporation trajectory over many shrink cycles without a
dense state-vector simulation?

This is needed for:

```text
ordinary evolution:
  M(t), T(t), number of emissions, shell timings, lifetime;

information capacity:
  remaining internal entropy, external record capacity, Page-style estimate.
```

## Script

```text
sim/many_cycle_evaporation_tracker.py
```

Outputs:

```text
sim/data/many_cycle_evaporation_tracker.csv
sim/data/many_cycle_evaporation_tracker_summary.csv
sim/data/many_cycle_evaporation_tracker_L80.csv
sim/data/many_cycle_evaporation_tracker_L80_summary.csv
sim/data/many_cycle_evaporation_tracker_3d.csv
sim/data/many_cycle_evaporation_tracker_3d_summary.csv
```

## Model

For each shell:

```text
M_L = 4 sigma L
S_L = L^2 log q
Delta M = 4 sigma
Delta S = (2L - 1) log q
```

Microscopic emissions are generated using:

```text
p_h(M) ~ int_bin d omega omega^(d-1) exp[S(M - omega) - S(M)].
```

Emissions continue until:

```text
sum omega >= Delta M.
```

Then the coarse shell update is applied at the capacity level:

```text
H_L -> H_(L-1) tensor H_shell(L).
```

The Page-style estimate is the random/typical capacity bound:

```text
S_Page_est(L) = min(S_remaining_internal, S_external_records).
```

This is not a dense Page-curve simulation. It is a compressed many-cycle
trajectory and capacity tracker.

## Main Result: L0 = 40

For:

```text
L0 = 40
q = 2
sigma = 1
2D bath
```

summary:

```text
total emissions = 576
page cross L = 28
page fraction evaporated = 0.300
normalized lifetime = 1365312.000
lifetime / M0^3 = 0.333328
```

Representative cycles:

```text
cycle L->L' events T_start first_w/T ext_cap page_est
    1 40->39     28   0.0721     1.981   54.759   54.759
    2 39->38     27   0.0740     1.981  108.131  108.131
    3 38->37     27   0.0759     1.981  160.117  160.117
   20 21->20     15   0.1374     1.987  831.777  277.259
   37  4-> 3      3   0.7213     2.268 1102.797    6.238
   38  3-> 2      2   0.9618     2.606 1106.263    2.773
   39  2-> 1      1   1.4427     2.779 1108.342    0.693
```

## Size Control: L0 = 80

For:

```text
L0 = 80
```

summary:

```text
total emissions = 2276
page cross L = 56
page fraction evaporated = 0.300
normalized lifetime = 10922645.333
lifetime / M0^3 = 0.333333
```

The Page crossing occurs near:

```text
L = L0 / sqrt(2).
```

For `L0 = 40`:

```text
40 / sqrt(2) = 28.3.
```

For `L0 = 80`:

```text
80 / sqrt(2) = 56.6.
```

This is exactly what the capacity estimate predicts from:

```text
S_L = L^2 log q.
```

## Lifetime Scaling

The tracker uses normalized power:

```text
dM/dt = - M^(-d).
```

For a 2D bath:

```text
d = 2,
tau ~ M0^3 / 3.
```

The runs give:

```text
L0 = 40: lifetime / M0^3 = 0.333328
L0 = 80: lifetime / M0^3 = 0.333333
```

So the many-cycle trajectory reproduces the expected cubic lifetime scaling.

## 3D Bath Control

For a 3D bath:

```text
lifetime / M0^4 = 0.250000
```

which matches:

```text
tau ~ M0^4 / 4.
```

This confirms that the tracker is sensitive to bath dimension in the expected
way.

## Interpretation

This is the first full-history result.

It connects:

```text
microscopic golden-rule emissions;
many emissions per shell at large L;
finite-gauge shell shrinkage;
M(t), T(t), lifetime scaling;
Page-style capacity estimate.
```

For large `L`, the number of microscopic emissions per shell grows:

```text
L = 40: 28 emissions for first shell
L = 80: 56 emissions for first shell
```

So the model now has the intended separation:

```text
microscopic emissions are small;
coarse shrinkage happens after many emissions.
```

## What This Does Not Prove

The Page-style curve here is a capacity/typicality estimate:

```text
S_Page_est = min(S_remaining, S_external).
```

It is not a direct density-matrix Page curve from a large quantum simulation.

The result assumes:

```text
sufficient scrambling/typicality between cycles;
unitary transfer of shell capacity into records;
the repeated-interaction emission mechanism already tested in smaller modules.
```

So it should be read as:

```text
the many-cycle architecture has the right trajectory and capacity structure.
```

not:

```text
we have numerically simulated a full large-L Page curve.
```

## F1-F13 Impact

This strengthens:

```text
F2:
  the process can now be followed through many repeated cycles at the
  trajectory/capacity level.

F3:
  shrinking internal capacity is tracked over the whole evaporation history.

F6:
  accelerating evaporation and lifetime scaling are tracked over many cycles.

F8/F9:
  the Page-style capacity turnover appears at the expected point, but remains a
  typicality estimate rather than a direct quantum Page curve.
```

No clean `Y` flip is forced by this, but the model is now much closer to a full
phenomenology tracker.

## Current Bottleneck

The remaining hard gap is:

```text
large-L quantum information dynamics.
```

The compressed tracker says what should happen if the small-module information
mechanism and typicality assumptions continue over many cycles.

To go beyond that, we need either:

```text
1. a random-isometry/Page theorem calculation tailored to the shell sequence;
2. a tensor-network or stabilizer-like simulation of many cycles;
3. acceptance that the many-cycle Page behavior is an analytical capacity
   estimate, not a direct simulation.
```
