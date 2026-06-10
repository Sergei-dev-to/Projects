# Matrix-Free Parent Local Protocol Prep

## Purpose

Use the small machine to fix the protocol for the larger `k=3` autonomous
sector-parent campaign.

The heavy run should not explore basic choices.  It should test one protocol
against the main question:

```text
Does the time-independent autonomous parent reproduce the sector-model
phenomenology when the radiation phase space is less cramped?
```

## Harness Changes

Benchmark driver:

```text
sim/run_matrix_free_parent_benchmark.py
```

now reports:

```text
resource estimates;
combined per-run summaries;
aggregate means and standard deviations;
energy, thermal-spectrum, and late-power-growth flags.
```

Local protocol scan:

```text
sim/scan_matrix_free_parent_protocol.py
```

scans coupling and time-window choices at laptop scale.

## Resource Estimate For The Next Heavy Run

Planned heavy run:

```text
n = 4..7
q = 2
max emitted quanta = 3
mode copies = 2
mode count = 12
occupation count = 299
basis dimension = 71,760
edge upper bound = 1,224,096
```

The script reports a model-storage scale of about `0.36 GB`, but that is not a
RAM requirement.  It excludes Krylov work vectors, Python build overhead,
allocator overhead, and the rest of the OS.

Practical target:

```text
minimum free RAM:     12 GB
comfortable free RAM: 20 GB or more
```

The 8 GB Surface should be used for `k=2` harness work.  The 32 GB MSI should
be used for the `k=3` campaign if it can boot with about `20 GB` free.

## Local k=2 Protocol Scan

Scan command:

```text
python sim/scan_matrix_free_parent_protocol.py \
  --case-prefix matrix_free_parent_protocol_scan_k2 \
  --n-min 4 --n-max 7 \
  --max-quanta 2 \
  --mode-copies 2 \
  --couplings 0.05,0.08,0.12 \
  --t-max-list 60,80 \
  --time-points 25 \
  --seeds 2468
```

Results:

```text
g      t_max   sqrt P_late/P_early   linear matched   no scramble   mean TV
0.05   60      1.356                 1.367            0.913         0.173
0.05   80      1.275                 1.237            0.898         0.173
0.08   60      1.056                 1.093            0.872         0.181
0.08   80      1.030                 1.023            0.900         0.188
0.12   60      0.913                 0.927            0.882         0.200
0.12   80      0.914                 0.917            0.923         0.207
```

The useful local regimes are `g=0.05` and `g=0.08`.  Coupling `g=0.12` already
loses the late-power growth and has worse flux TV, so it is too strong for the
main campaign.

## Three-Seed Validation At k=2

Validation command:

```text
python sim/run_matrix_free_parent_benchmark.py \
  --case-prefix matrix_free_parent_protocol_g0p05_t80_k2_3seed \
  --n-min 4 --n-max 7 \
  --max-quanta 2 \
  --mode-copies 2 \
  --emission-coupling 0.05 \
  --time-points 25 \
  --t-max 80 \
  --seeds 2468,1357,9753
```

Aggregate result:

```text
case                         <Delta n>   E_rad(final)   P_late/P_early   mean TV
sqrt + scrambling             0.674       2.261          1.248            0.152
linear matched + scrambling   0.672       2.155          1.202            0.182
sqrt, no scrambling           0.652       1.844          0.911            0.164
```

Per-seed behavior:

```text
sqrt + scrambling:           late power grows in all 3 seeds
linear matched + scrambling: late power grows in all 3 seeds
sqrt, no scrambling:         late power decays in all 3 seeds
```

The `sqrt` versus `linear` contrast is positive on average but not large at
`k=2`.  The scrambling contrast is robust.

## Protocol Choice For The k=3 Campaign

Use:

```text
emission coupling g = 0.05
t_max = 80
time points = 25
n = 4..7
max emitted quanta = 3
mode copies = 2
seeds = 2468,1357,9753
```

Reason:

```text
1. g=0.05 has the best thermal flux TV among scanned couplings.
2. g=0.05 preserves late-power growth in the scrambled runs.
3. t=80 is the best scanned window with positive sqrt-minus-linear contrast.
4. no-scrambling loses late power in every validation seed.
5. the run should fit on a 32 GB machine with a clean boot.
```

The larger `k=3` run should decide whether the weak sqrt/linear contrast is a
finite-radiation truncation effect.

## Area-Emission Update

The analytic sector calculation shows that the entropy-energy law gives the
thermal spectrum and negative heat capacity, but the Schwarzschild power law
also requires area-sized emission strength:

```text
rate strength ~ n ~ M^2.
```

The matrix-free parent now includes this through

```text
--emission-area-power 1
```

which is the default.  The fixed-strength control is

```text
--emission-area-power 0
```

The k=2 and k=3 protocol results above were produced before this control was
added.  They remain useful as checks of matrix-free evolution, energy
conservation, finite radiation truncation, and scrambling sensitivity.  They do
not decide the full Hawking-rate mechanism.

The updated benchmark runs four cases by default:

```text
sqrt mass law + scrambling + area emission;
linear mass law + scrambling + area emission;
sqrt mass law + no scrambling + area emission;
sqrt mass law + scrambling + fixed-strength emission.
```

The target bath exponent is now

```text
--ohmic-power 2
```

which represents the 3D massless radiation phase-space factor.  The earlier
runs used `p = 1`; they tested the autonomous machinery but not the 4D
Schwarzschild power-law target.

The corrected summaries include

```text
predicted_power_exponent_m
```

for each case.  The target value is

```text
-2
```

for `P(M)`.  Late-power growth alone is not enough, because fixed-strength
emission with the same entropy law predicts `P(M) ~ M^-4` and can also
accelerate.

## MSI Command

One-seed check:

```text
python sim/run_matrix_free_parent_benchmark.py \
  --case-prefix matrix_free_parent_protocol_g0p05_t80_k3_seed2468 \
  --n-min 4 --n-max 7 \
  --max-quanta 3 \
  --mode-copies 2 \
  --emission-coupling 0.05 \
  --emission-area-power 1 \
  --ohmic-power 2 \
  --time-points 25 \
  --t-max 80 \
  --seeds 2468 \
  --combined-summary-csv sim/data/matrix_free_parent_protocol_g0p05_t80_k3_seed2468_summary.csv \
  --aggregate-summary-csv sim/data/matrix_free_parent_protocol_g0p05_t80_k3_seed2468_aggregate.csv
```

Three-seed campaign:

```text
python sim/run_matrix_free_parent_benchmark.py \
  --case-prefix matrix_free_parent_protocol_g0p05_t80_k3_3seed \
  --n-min 4 --n-max 7 \
  --max-quanta 3 \
  --mode-copies 2 \
  --emission-coupling 0.05 \
  --emission-area-power 1 \
  --ohmic-power 2 \
  --time-points 25 \
  --t-max 80 \
  --seeds 2468,1357,9753 \
  --combined-summary-csv sim/data/matrix_free_parent_protocol_g0p05_t80_k3_3seed_summary.csv \
  --aggregate-summary-csv sim/data/matrix_free_parent_protocol_g0p05_t80_k3_3seed_aggregate.csv
```
