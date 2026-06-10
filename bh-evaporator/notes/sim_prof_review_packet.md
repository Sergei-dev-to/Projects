# Review Packet: Geometry-Free Floquet Evaporator

## Purpose

We would like feedback on a finite non-gravitational quantum toy model for
black-hole evaporation phenomenology.

The question is not whether this is a model of gravity. It is not. The question
is whether a finite quantum system with no spacetime, no horizon, and no
gravitational path integral can reproduce the usual evaporation phenomenology
package:

```text
negative heat capacity;
increasing temperature during evaporation;
Schwarzschild-like power law;
locally thermal hard radiation;
shrinking internal state space;
Page-like radiation entropy;
late/early radiation correlations;
unitary global evolution.
```

If yes, then that package should not be treated as uniquely gravitational. The
remaining gravitational questions become sharper: what supplies the state
count, what selects the purification channel, and how islands/wormholes encode
the fine-grained bookkeeping.

## Proposal

Use a finite repeated-interaction / Floquet quantum model.

The core has droplet sectors:

```text
dim B_L = q^(L^2)
S_micro(L) = log dim B_L = L^2 log q
M_L = 4 sigma L
```

Therefore:

```text
T_L = (dS_micro/dM)^(-1)
    = 2 sigma / (L log q)
    ~ 1/M,
```

so the core has negative heat capacity.

The model uses the shell factorization:

```text
B_L ~= B_(L-1) tensor Shell_L
dim Shell_L = q^(2L - 1).
```

One Floquet cycle is:

```text
1. scramble the active core;
2. emit a hard quantum and hidden bath purifier;
3. add emitted hard energy to an accumulator;
4. if the accumulator crosses a threshold, transfer the next shell label to a
   soft radiation record;
5. repeat.
```

Subsystems:

```text
core:
  remaining active core plus accumulator;

hard radiation:
  visible emitted hard quanta;

bath purifier:
  hidden purifier records for the hard channel;

soft radiation:
  shell-transfer records carrying fine information;

full radiation:
  hard + bath purifier + soft records.
```

The final cycle is written explicitly in:

```text
notes/final_floquet_cycle_spec.md
```

## Emission Weights And Power

Hard-emission probabilities are generated from the same entropy curve:

```text
Gamma(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)].
```

For a 2D bath:

```text
P ~ boundary * T^3
  ~ L * L^-3
  ~ M^-2.
```

The weighted-power diagnostic gives:

```text
L    M^2 W_L
8    3232.647
20   3062.824
40   3040.064
```

So `M^2 W_L` approaches a constant at large `L`.

## Current Exact Diagnostics

The exact fused state-vector runs are small:

```text
L0 = 3
rate L0 = 20 in the default golden-rule emission schedule
```

The rate-scale separation is tested by varying `rate L0`:

```text
rate L0   p1 first   soft gap   old/new gap   hard error   <shells>
8          0.419       2.076       0.684       ~0           1.210
12         0.411       2.103       0.637       ~0           1.195
20         0.407       2.114       0.616       0            1.188
40         0.405       2.119       0.608       ~0           1.186
```

The diagnostics are stable over this range.

## Page-Like Entropy Probe

The fused Page probe uses the von Neumann entropy of the full radiation
subsystem:

```text
S_full_rad = S_vN(hard + bath purifier + soft records).
```

Scrambled run:

```text
emissions      2      4      6      8
S_full_rad   1.427  3.799  2.612  1.900
```

No-scrambling comparison:

```text
emissions      2      4      6      8
S_full_rad   1.017  1.384  1.592  1.698
```

The scrambled model shows a small radiation-entropy rise and turnover. The
no-scrambling comparison does not show the same turnover over this window.

## Robustness Checks

### Threshold Values

```text
threshold  soft gap  old/new gap  hard error  <shells>  P(done)
4            1.076      2.678      0          1.781     0.005
5            2.114      0.616      0          1.188     0
6            2.438      0.022      0          1.005     0
```

The threshold changes which behavior is most visible:

```text
lower threshold:
  more shrinkage and stronger old/new correlations;

higher threshold:
  stronger soft entropy gap but less old/new enhancement in the short run.
```

### Threshold Update Rule

Two accumulator conventions were tested:

```text
carry:
  after crossing threshold, A -> A - Delta;

reset:
  after crossing threshold, A -> 0.
```

Results:

```text
mode    threshold  soft gap  old/new gap  <shells>
carry       4        1.076      2.678      1.781
carry       5        2.114      0.616      1.188
reset       4        1.221      2.522      1.699
reset       5        2.216      0.488      1.131
```

The qualitative behavior survives both conventions.

### Hard Alphabet

The hard channel was tested with `d_hard = 2, 3, 4` bins:

```text
d_hard  soft gap  old/new gap  hard error  <shells>
2         0.766      0.000      ~0          0.076
3         1.678      0.003      ~0          0.110
4         2.099      0.067      ~0          0.087
```

Hard-local thermality remains exact relative to the golden-rule distribution.
The soft entropy gap persists and grows with a richer hard alphabet. Old/new
correlations are weak in this short four-emission run because little shell
transfer occurs.

## What We Think Is Achieved

Under the Floquet toy-model standard:

```text
finite Hilbert space and subsystem split:
  achieved;

explicit repeated update rule:
  achieved;

purifiable global evolution:
  achieved;

S_micro ~ M^2:
  achieved by model state count;

T ~ 1/M and negative heat capacity:
  achieved;

P ~ M^-2:
  achieved at weighted-power / rate-diagnostic level;

hard-local thermality:
  achieved in compact finite alphabets;

shrinking internal capacity:
  achieved through threshold-triggered shell transfer;

Page-like entropy turnover:
  achieved in a small fused exact diagnostic;

old/new radiation correlations:
  achieved in the fused exact diagnostic;

scrambling dependence:
  demonstrated with no-scrambling comparisons.
```

## Main Caveats

```text
exact fused runs are small: L0 = 3;
few seeds;
hard alphabet remains compact;
rate-generation scale is separated from exact register scale;
threshold rule is selected as a model ingredient;
the state count dim B_L = q^(L^2) is model input;
matrix elements are treated as smooth/flat in the golden-rule weights;
the model is driven/stroboscopic, not a simple time-independent autonomous
Hamiltonian.
```

## Nonclaims

We do not claim:

```text
this solves the black-hole information paradox;
this derives Hawking radiation from semiclassical gravity;
this derives the Bekenstein-Hawking coefficient;
this derives the area state count;
this proves fast scrambling asymptotically;
this gives a simple autonomous Hamiltonian;
this reproduces islands or wormholes.
```

## Questions For Review

1. Is the repeated-interaction / Floquet standard acceptable for the proposed
   comparison-model claim?

2. Are the diagnostics sufficient to say that the model reproduces the mapped
   black-hole evaporation phenomenology package at small finite size?

3. Which caveat is most serious from a simulation / quantum dynamics
   perspective:

```text
small exact L0;
rate L0 separated from exact L0;
threshold rule as model input;
compact hard alphabet;
absence of a time-independent autonomous Hamiltonian?
```

4. Is the hard/soft/bath split a reasonable finite Stinespring bookkeeping, or
   does it look too engineered?

5. What would be the strongest next simulation target:

```text
larger exact L0;
compressed / second Rényi Page diagnostic;
larger hard alphabet and longer trajectory;
more physical bath Hamiltonian;
autonomous Hamiltonian embedding?
```

6. Are there known models or papers that already do essentially this
   combination:

```text
negative heat capacity
+ unitary evaporation
+ Page-like turnover
+ locally thermal hard radiation
+ gravity-free finite quantum dynamics?
```

## Files To Inspect

Core model and status:

```text
notes/final_floquet_cycle_spec.md
notes/final_floquet_toy_model_result.md
notes/phenomenology_requirements_review.md
notes/phenomenology_gap_audit.md
```

Key diagnostics:

```text
notes/fused_floquet_time_resolved_results.md
notes/fused_floquet_robustness_results.md
notes/fused_floquet_rate_scale_results.md
notes/fused_floquet_page_probe_results.md
notes/fused_floquet_multibin_results.md
notes/fused_floquet_threshold_variant_results.md
```

Scripts:

```text
sim/fused_floquet_time_resolved_scan.py
sim/fused_floquet_robustness_scan.py
sim/fused_floquet_rate_scale_scan.py
sim/fused_floquet_page_probe.py
sim/fused_floquet_multibin_scan.py
sim/fused_floquet_threshold_variant_scan.py
```

