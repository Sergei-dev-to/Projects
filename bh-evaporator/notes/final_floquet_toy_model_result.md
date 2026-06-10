# Final Floquet toy-model result

## Purpose

This note states the current result under the Floquet toy-model standard.

The standard is:

```text
finite Hilbert space;
explicit repeated update rule;
unitary or purifiable records;
analytic thermodynamic scaling;
finite quantum diagnostics for hard thermality, soft information flow, and
scrambling comparisons.
```

The stronger simple time-independent autonomous-Hamiltonian standard is a
separate follow-up.

## Claim

A finite non-gravitational Floquet evaporator can reproduce the mapped
Schwarzschild evaporation package at the thermodynamic and finite-diagnostic
level.

More concretely:

```text
area-like constrained entropy
+ boundary-tension energy
+ 2D bath phase space
+ weighted hard emissions
+ hidden bath purifiers
+ emitted-energy accumulation
+ threshold-triggered shell transfer
+ soft/shrink records
+ scrambling comparisons
```

are sufficient to reproduce:

```text
S_micro ~ M^2;
T ~ 1/M;
negative heat capacity;
P ~ M^-2;
tau ~ M0^3;
shrinking internal state space;
hard-local thermality;
soft/global purification channel;
Page-like fine-grained soft/global radiation entropy;
old/new radiation correlations under scrambling;
failure of Page-like soft entropy without scrambling.
```

## Model

Droplet sectors:

```text
dim B_L = q^(L^2)
S_micro(L) = log dim B_L = L^2 log q
M_L = 4 sigma L
```

Shell factorization:

```text
B_L ~= B_(L-1) tensor Shell_L
dim Shell_L = q^(2L - 1)
```

Temperature:

```text
T_L = (dS_micro/dM)^(-1)
    = 2 sigma / (L log q)
    ~ 1/M.
```

For a 2D bath:

```text
P ~ boundary * T^3
  ~ L * L^-3
  ~ M^-2.
```

Floquet cycle:

```text
scramble active core;
emit hard quantum and hidden bath purifier;
add emitted energy to accumulator;
if accumulator crosses threshold, transfer next shell to soft record;
repeat.
```

Hard radiation is the visible local channel.

Soft/shrink records are the fine information-carrying radiation channel.

Hidden bath records purify the local hard channel.

## Final Diagnostic

The current best single finite diagnostic is:

```text
script: sim/final_floquet_candidate_scan.py
note:   notes/final_floquet_candidate_scan_results.md
```

The current fused time-resolved diagnostic is:

```text
script: sim/fused_floquet_time_resolved_scan.py
note:   notes/fused_floquet_time_resolved_results.md
```

The final Floquet cycle is specified in:

```text
notes/final_floquet_cycle_spec.md
```

The threshold/seeds robustness check is:

```text
script: sim/fused_floquet_robustness_scan.py
note:   notes/fused_floquet_robustness_results.md
```

The rate-scale scan is:

```text
script: sim/fused_floquet_rate_scale_scan.py
note:   notes/fused_floquet_rate_scale_results.md
```

The fused Page probe is:

```text
script: sim/fused_floquet_page_probe.py
note:   notes/fused_floquet_page_probe_results.md
```

The hard-alphabet stress test is:

```text
script: sim/fused_floquet_multibin_scan.py
note:   notes/fused_floquet_multibin_results.md
```

The threshold-rule variant test is:

```text
script: sim/fused_floquet_threshold_variant_scan.py
note:   notes/fused_floquet_threshold_variant_results.md
```

This fused diagnostic uses microcanonical/golden-rule hard weights generated
from the same entropy curve:

```text
Gamma(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)].
```

Best case:

```text
L0 = 3
threshold = 5
micro emissions = 6
P(hard energy 2) = 0.35
scramblers = margulis, grid, none
```

Results:

```text
mean transferred shells = 1.117
P(done)                 = 0
max basis terms         = 32768
```

Reduced-density results:

```text
scrambler   S_soft   S_hard  target hard S  hard error   soft-none gap
margulis    2.636    3.885      3.885        8.9e-16       2.274
grid        2.647    3.885      3.885        4.4e-16       2.286
none        0.362    3.885      3.885        4.4e-16       0
```

Here:

```text
S_hard:
  von Neumann entropy of the visible hard radiation register after hidden
  bath/purifier records are traced out. If the hard register is diagonal in
  hard-bin records, this equals the Shannon entropy of the hard-bin
  distribution.

S_soft:
  von Neumann entropy of the soft/shrink records that carry fine purification
  information in this finite diagnostic.

S_micro:
  microcanonical/Boltzmann entropy of the remaining droplet sector.
```

Interpretation:

```text
hard thermality:
  exact relative to the chosen finite hard distribution.

soft information:
  large only when scrambling is present.

no-scrambling comparison:
  hard radiation remains thermal, but soft radiation entropy is small.
```

Thus local hard thermality does not by itself generate Page-like information
flow. Scrambling of the shrinking core is doing real work.

The fused time-resolved diagnostic adds an early/late radiation split and
microcanonical/golden-rule hard weights to the selected candidate trajectory.
With the first three emissions treated as old radiation and the last three as
new radiation, the full-radiation mutual information is:

```text
scrambler   I(old:new full radiation)
margulis             2.615
grid                 2.624
none                 1.988
```

The old/new mutual information is larger with scrambling by about `0.63` nats
in this small run.

The same fused script writes a weighted-power schedule. For the edge-tension
entropy curve and a 2D bath:

```text
L    M^2 W_L
8    3232.647
20   3062.824
40   3040.064
```

This is the finite diagnostic version of `P ~ M^-2`.

The robustness scan over thresholds `4, 5, 6` and seeds `0, 1` gives:

```text
threshold  soft gap  old/new gap  hard error  <shells>
4            1.076      2.678      0          1.781
5            2.114      0.616      0          1.188
6            2.438      0.022      0          1.005
```

The threshold changes which diagnostic is most visible, but the fused behavior
is not confined to one threshold.

The rate-scale scan varies the microcanonical rate-generation scale while
holding the exact state-vector register fixed:

```text
rate L0   soft gap   old/new gap   <shells>
8           2.076       0.684       1.210
12          2.103       0.637       1.195
20          2.114       0.616       1.188
40          2.119       0.608       1.186
```

Thus the `L0 = 3` / `rate L0 = 20` separation is still a finite-size caveat,
but the fused diagnostic is stable when the rate scale is varied.

The fused Page probe at threshold `4` shows a small von Neumann entropy
turnover in the scrambled model:

```text
emissions      2      4      6      8
S_full_rad   1.427  3.799  2.612  1.900
```

The no-scrambling comparison over the same window is:

```text
emissions      2      4      6      8
S_full_rad   1.017  1.384  1.592  1.698
```

So the Page-like turnover now appears inside the fused model, with the usual
small-size caveats.

The multi-bin hard-spectrum scan gives:

```text
d_hard  soft gap  old/new gap  hard error
2         0.766      0.000      ~0
3         1.678      0.003      ~0
4         2.099      0.067      ~0
```

This shows that the hard/soft split is not an artifact of a two-bin hard
alphabet.

The threshold-rule variant scan gives:

```text
mode    threshold  soft gap  old/new gap  <shells>
carry       4        1.076      2.678      1.781
carry       5        2.114      0.616      1.188
reset       4        1.221      2.522      1.699
reset       5        2.216      0.488      1.131
```

The qualitative result survives both accumulator update conventions.

## Status Under Floquet toy-model standard

Detailed remaining gaps are collected in:

```text
notes/phenomenology_gap_audit.md
```

A first-principles requirements review is collected in:

```text
notes/phenomenology_requirements_review.md
```

```text
model specification                 Y
shrinking internal capacity          Y-
microcanonical entropy/mass relation Y
temperature and heat capacity        Y
evaporation power and lifetime       Y
local hard thermality                Y-
Page-like fine-grained rad entropy   Y-
early/late radiation correlations    Y-
gravity-free comparison             Y
weighted-power diagnostic            Y-
mass-law and bath comparisons        Y
scrambling diagnostics/comparisons   Y-
fast-scrambling proxy                P+
driven-cycle Hamiltonian realization Y
time-independent autonomous H        P/N
```

Meaning:

```text
Y:
  achieved cleanly for the Floquet toy-model standard.

Y-:
  achieved in small finite diagnostics, with engineering/scale caveats.

P:
  partially present or superseded by a newer diagnostic.

P+:
  substantial evidence, but not a final theorem.
```

For autonomy:

```text
Y-:
  one explicit repeated unitary cycle, Hamiltonian-realizable in the
  stroboscopic sense.

P:
  if the standard is one simple time-independent autonomous Hamiltonian.
```

## What Is New Enough To Be Interesting

Not new individually:

```text
Page curves without gravity;
unitary qubit evaporation;
collision models;
hard/soft bookkeeping;
clock/Floquet protocols;
fast-scrambling diagnostics.
```

Potentially interesting as an integrated toy-model result:

```text
The same finite non-gravitational architecture contains:

1. Schwarzschild-like thermodynamic scaling from microcanonical entropy and
   boundary energy;
2. negative heat capacity and accelerated evaporation;
3. threshold-driven shrinking internal capacity;
4. locally thermal hard radiation;
5. soft/global purification records;
6. Page-like soft entropy and old/new correlations under scrambling;
7. explicit no-scrambling comparisons.
```

The conceptual message is:

```text
The usual black-hole evaporation phenomenology package is not, by itself,
diagnostic of gravity.
```

The gravitational problem is then sharpened:

```text
What selects this purification channel in spacetime?
Why does horizon physics supply the required state count?
How do islands/wormholes encode the same fine-grained bookkeeping?
```

## What We Should Not Claim

Do not claim:

```text
this solves the black-hole information paradox;
this derives Hawking radiation from semiclassical gravity;
this derives the Bekenstein-Hawking coefficient;
this proves fast scrambling asymptotically;
this gives a simple time-independent autonomous Hamiltonian;
this reproduces islands or wormholes.
```

The model is valuable precisely because it lacks gravity.

It is a non-gravitational toy model.

## Remaining Weaknesses

The main remaining weaknesses are:

```text
small-size final diagnostic, L0=3;
one seed in the final scan;
one seed in the fused time-resolved scan;
rate-generation scale separated from exact state-vector register size, but
rate-scale dependence has been tested;
engineered Floquet ordering;
finite hard alphabet;
threshold rule still selected as part of the model, though value and update
variants have been stress-tested;
fast scrambling supported numerically, not proven;
no simple time-independent autonomous Hamiltonian.
```

These are real caveats, but they no longer block the Floquet toy-model result.

They define follow-up work.

## Decision

Under the Floquet toy-model standard, the project has reached a coherent result:

```text
all central non-gravitational black-hole evaporation phenomenology has a
finite quantum toy-model realization, with explicit caveats.
```

The next step should be writing, not more exploratory simulation:

```text
1. state the model;
2. state the mapping to black-hole observables;
3. present the final diagnostics and model comparisons;
4. separate generic quantum/statistical mechanisms from genuinely
   gravitational questions.
```
