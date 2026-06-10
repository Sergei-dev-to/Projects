# Phenomenology Gap Audit

## Purpose

Collect what is still missing in the current evaporator program, using the
target categories, diagnostics, and model comparisons from:

```text
notes/phenomenology_requirements_review.md
```

The standard used here is the current Floquet toy-model standard:

```text
finite Hilbert space;
explicit repeated update rule;
unitary or purifiable records;
analytic thermodynamic scaling;
finite quantum diagnostics for hard thermality, soft information flow,
scrambling diagnostics, and threshold-triggered shrinkage.
```

The stronger simple time-independent autonomous-Hamiltonian standard is a
separate follow-up.

## Compact Status

```text
Requirement                         Status   Main remaining gap
---------------------------------------------------------------------------
model specification                 Y        final unitary cycle written
shrinking internal capacity          Y-       threshold values and variants stress-tested
microcanonical entropy/mass relation Y        coefficient is outside the target
temperature and heat capacity        Y        none under toy-model standard
evaporation power and lifetime       Y        exact state-vector scan is small
local hard thermality                Y-       multi-bin checked, still compact
Page-like fine-grained rad entropy   Y-       small fused S_vN turnover probe
early/late radiation correlations    Y-       threshold/seeds stress-tested, still small
gravity-free comparison             Y        none
weighted-power diagnostic            Y-       rate-scale separation characterized
mass-law and bath comparisons        Y        integrate into final narrative
scrambling diagnostics/comparisons   Y-       threshold/seeds stress-tested, still small
fast-scrambling proxy                P+       larger Hamiltonian evidence
driven-cycle realization             Y        final cycle written as Floquet update
time-independent autonomous H        N/P      harder follow-up
```

## Details

### Model Specification

What we have:

```text
finite droplet sectors;
finite hard radiation registers;
finite soft/shrink records;
finite hidden bath/purifier records;
explicit branch/state-vector simulations;
injective finite-register maps;
state-vector lift with coherent amplitudes.
```

What is missing:

```text
optional stroboscopic effective-Hamiltonian or clock embedding;
run a larger all-in density diagnostic with more seeds.
```

Current cycle specification:

```text
notes/final_floquet_cycle_spec.md
```

This closes the model-specification gap under the Floquet toy-model standard.

### Shrinking Internal Capacity

What we have:

```text
B_L ~= B_(L-1) tensor Shell_L;
dim Shell_L = q^(2L-1);
threshold-triggered shell transfer;
accumulator-driven shrinkage rather than an externally fixed shell schedule.
threshold stress test over Delta = 4, 5, 6 in the fused diagnostic.
threshold update variant test comparing carry-over and reset rules.
```

What is missing:

```text
the threshold rule is still a designed update;
the shrink trigger is still not derived from one autonomous Hamiltonian;
the exact stress tests are still small.
```

Shrinkage can be unitary. The open issue is why this shrink rule is
dynamically selected.

### Entropy/Mass Relation

What we have:

```text
dim B_L = q^(L^2);
S_micro(L) = log dim B_L = L^2 log q;
M_L = 4 sigma L;
therefore S_micro ~ M^2.
```

What is missing:

```text
the Bekenstein-Hawking coefficient is outside the target.
```

That is acceptable because the project is a non-gravitational toy model.
The target is scaling and phenomenology.

### Temperature And Heat Capacity

What we have:

```text
T_L = (dS_micro/dM)^(-1) = 2 sigma / (L log q);
T ~ 1/M;
C = dM/dT < 0.
```

What is missing:

```text
nothing essential for the toy model.
```

### Evaporation Power And Lifetime

What we have:

```text
2D bath phase space;
P ~ boundary * T^3;
P ~ L * L^-3 ~ L^-2 ~ M^-2;
tau ~ M0^3.
```

What is missing:

```text
the exact all-in quantum scan is too small to display a clean long power law;
the large-L acceleration result is mostly analytic/trajectory-level.
```

### Local Hard Thermality

What we have:

```text
hard radiation matches the chosen finite hard distribution;
hidden bath records purify the hard-local channel;
hard thermality survives in the final threshold scan.
hard thermality and soft-information split survive d_hard = 2, 3, 4.
```

What is missing:

```text
the exact scans still use compact hard alphabets;
the fuller 2D-box bath spectrum is not fully integrated into the final
thresholded density scan.
```

Current multi-bin result:

```text
notes/fused_floquet_multibin_results.md
```

### Page-Like Fine-Grained Radiation Entropy

What we have:

```text
Page theorem capacity argument;
stabilizer shell Page diagnostics;
hard/soft accounting;
integrated state-vector tests;
thresholded soft entropy gap under scrambling.
small fused full-radiation von Neumann entropy turnover probe.
```

What is missing:

```text
larger fused `S_vN(R)` or explicitly labeled `S_2(R)` Page-like curve;
more seeds and longer trajectories.
```

Current fused Page probe:

```text
notes/fused_floquet_page_probe_results.md
```

### Early/Late Radiation Correlations

What we have:

```text
old/new mutual information in stabilizer shell diagnostics;
reference-flow diagnostics;
integrated state-vector old/new mutual information in small runs;
soft records carry purification while hard records remain locally thermal.
time-resolved old/new full-radiation mutual information in the fused final
candidate diagnostic.
threshold/seeds stress test in the fused robustness scan.
```

What is missing:

```text
larger early/late runs with more seeds and a longer evaporation trajectory.
```

Current fused result:

```text
notes/fused_floquet_time_resolved_results.md
notes/fused_floquet_robustness_results.md
```

### Gravity-Free Comparison

What we have:

```text
no gravity;
finite quantum registers;
ordinary statistical mechanics;
black-hole-like thermodynamics and information diagnostics.
```

What is missing:

```text
nothing essential.
```

This is the conceptual point of the project.

### Weighted-Power Audit

What we have:

```text
old weighted-channel diagnostic in the earlier spin-chain track;
newer bath-density / boundary*T^3 scaling;
weighted hard emissions in the final scan.
microcanonical/golden-rule hard weights in the fused time-resolved scan;
large-L weighted-power schedule showing M^2 W_L approaches a constant.
rate-scale scan showing fused diagnostics stable for rate L0 = 8, 12, 20, 40.
```

What is missing:

```text
larger exact state-vector run where the rate-generation scale and register
scale are closer, if computationally feasible;
larger hard alphabet;
matrix-element model beyond smooth/flat golden-rule weights.
```

Modern target:

```text
W_L = sum_omega rho_bath(omega)
                |g_L(omega)|^2
                exp[S(L, E-omega) - S(L, E)]
                omega.
```

This diagnostic checks whether the power law follows from the outgoing channel
weights.

Current fused result:

```text
notes/fused_floquet_time_resolved_results.md
notes/fused_floquet_rate_scale_results.md
```

### Mass-Law And Bath Comparisons

What we have:

```text
comparisons showing that the Schwarzschild-like exponents select M ~ L;
linear/sqrt alternatives fail to give the same full package;
bath-dimension comparisons for lifetime scaling.
```

What is missing:

```text
mostly integration into the final narrative.
```

### Scrambling Diagnostics And Comparisons

What we have:

```text
no-scrambling comparison cases;
grid/Margulis/none comparisons;
scrambled soft entropy much larger than no-scrambling soft entropy;
hard thermality alone does not generate information flow.
threshold/seeds robustness scan: the soft entropy gap persists for thresholds
4, 5, and 6.
threshold variant scan: carry-over and reset accumulator rules both preserve
the fused behavior.
```

What is missing:

```text
larger comparison matrix;
more seeds beyond the current two-seed robustness run;
more explicit local-removal stress tests inside the final thresholded model.
```

The current comparisons already show that scrambling is doing real work.

### Fast-Scrambling Proxy

What we have:

```text
expander/interacting-spin diagnostics;
entanglement-growth tests;
coarse operator-spreading tests;
Margulis faster than local grid;
complete graph fastest;
quadratic Majorana comparison case fails.
```

What is missing:

```text
larger-system Hamiltonian evidence;
an asymptotic scrambling theorem;
proof that the chosen interacting expander Hamiltonian is a genuine fast
scrambler in the required sense.
```

This is a natural follow-up branch.

### Naturalness And Autonomy

Literature check:

```text
notes/floquet_hamiltonian_literature_check.md
```

What we have:

```text
one repeated-interaction/Floquet cycle;
final cycle specification;
global register rule;
state-vector lift;
hard-density check;
reference-flow check;
thresholded integrated state-vector diagnostics.
```

A repeated unitary cycle is Hamiltonian-realizable in the stroboscopic sense:

```text
|psi_{n+1}> = U_cycle |psi_n>;
U_cycle = exp(-i H_eff T)
```

so the current gap is naturalness.

What is missing:

```text
one simple time-independent autonomous Hamiltonian whose ordinary dynamics
produces scrambling, emission, energy accumulation, and shell shrinkage without
an engineered sequence of stages.
```

Current specification:

```text
notes/final_floquet_cycle_spec.md
```

## Overall Assessment

Under the Floquet toy-model standard, the project is close to the intended
target:

```text
the remaining weaknesses are mostly scale, integration, and autonomy.
```

Under the simple time-independent autonomous-Hamiltonian standard, the project
has major open gaps:

```text
the shrink trigger, detailed rate generation, fast scrambling, and autonomy
remain hard gaps.
```

The clean strategic choice is:

```text
1. treat the current result as a finite non-gravitational toy model;
2. enlarge the fused Page-curve diagnostic beyond one seed / L0 = 3 if
   feasible;
3. enlarge the fused diagnostic beyond the current exact sizes if feasible;
4. optionally write a stroboscopic effective-Hamiltonian or clock embedding;
5. leave the time-independent autonomous-Hamiltonian version as the next,
   harder project.
```
