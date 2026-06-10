# Phenomenology Requirements Review

## Purpose

State the project requirements from first principles.

The goal is:

```text
Find a finite non-gravitational quantum system that reproduces the usual
black-hole evaporation phenomenology package closely enough to separate
generic quantum/statistical mechanisms from genuinely gravitational issues.
```

Out of scope:

```text
derive general relativity;
derive the Bekenstein-Hawking coefficient;
solve the information paradox;
reproduce islands or wormholes.
```

The target is a non-gravitational toy model.

Terminology from nearby literature:

- `toy model`: used for simple quantum-mechanical models of black-hole
  evaporation, e.g. Avery, "Qubit Models of Black Hole Evaporation."
- `toy qubit model`: used for explicit qubit-transport models, e.g.
  Osuga and Page, "Qubit Transport Model for Unitary Black Hole Evaporation
  without Firewalls."
- `qubit model`: used for black-hole evaporation models with multiple qubits,
  e.g. Hotta, Nambu, and Yamaguchi, "Soft-Hair-Enhanced Entanglement Beyond
  Page Curves in a Black-hole Evaporation Qubit Model."
- `quantum simulation`: used when implementing these toy/qubit models on
  quantum hardware.
- `analogue model`: reserve for physical analogue-gravity systems.
- `phenomenological model`: appropriate when emphasizing fitted or effective
  modeling assumptions.

## Entropy Terminology

Several different entropies appear in the project.

- Microcanonical entropy / Boltzmann entropy:
  `S_micro(L) = log Omega_L`, where `Omega_L = dim B_L` is the number of
  core microstates in the remaining droplet sector. In the current model,
  `S_micro(L) = log dim B_L = L^2 log q`.
- Bekenstein-Hawking entropy:
  `S_BH(M)`, the black-hole thermodynamic entropy used as the target scaling.
  The toy model aims for `S_micro ~ S_BH ~ M^2`, with the coefficient outside
  the target.
- von Neumann entropy:
  `S_vN(A) = -Tr rho_A log rho_A` for a quantum subsystem `A`.
- Second Rényi entropy:
  `S_2(A) = -log Tr rho_A^2`. This is the only Rényi entropy we currently
  care about, because it is standard in numerics and quantum-simulation
  protocols and is easier to estimate than `S_vN(A)`.
- Page-curve entropy:
  the von Neumann entropy of the emitted radiation subsystem,
  `S_vN(R)`, as a function of evaporation time. A Page-like curve for
  `S_2(R)` is a useful companion diagnostic, but the default Page curve means
  von Neumann entropy.
- Hard-radiation entropy:
  `S_vN(R_hard)`, the von Neumann entropy of the visible hard radiation
  register after hidden bath/purifier records are traced out. When the hard
  register is diagonal in energy-bin records, this equals the Shannon entropy
  of the hard-bin probability distribution.
- Soft-record entropy:
  `S_vN(R_soft)`, the von Neumann entropy of the soft/shrink radiation records.
  In the current model these records carry much of the purification
  information.
- Quantum mutual information:
  `I(A:B) = S_vN(A) + S_vN(B) - S_vN(AB)`, used for old/new radiation
  correlation diagnostics.

The main thermodynamic requirement concerns the microcanonical entropy
`S_micro(L)`.

The Page-curve requirement concerns the von Neumann entropy of the emitted
radiation, `S_vN(R)`, approximated in the current finite diagnostics by
soft/global radiation entropies.

Second Rényi entropy `S_2(R)` is an acceptable secondary diagnostic for the
same turnover/correlation structure. It should be labeled explicitly.

The hard-radiation thermality requirement concerns the reduced hard-radiation
state `rho_hard` and its von Neumann/Shannon entropy, depending on whether the
hard register is treated quantum mechanically or as classical energy-bin data.

## Model Setup

The minimum concrete object is:

- Hilbert space.
- Evolution rule: a Hamiltonian-realizable unitary cycle or a time-independent
  Hamiltonian.
- Initial state class.
- Observable split into core, radiation, bath/purifier, and records.

This setup turns the project from thermodynamic analogy into a testable quantum
model.

## Target Phenomenology

These are the things the model is supposed to reproduce.

### Model Specification

- Finite Hilbert space and subsystem split.
- Explicit evolution rule.
- Initial state class.
- Unitary or explicitly purifiable global evolution.

This is the minimum for having a real quantum model.

### Schwarzschild-Like Thermodynamics

- Shrinking internal capacity.
- Microcanonical core entropy/mass relation `S_micro ~ M^2`.
- Temperature `T ~ 1/M`.
- Negative heat capacity.
- Power law `P ~ M^-2`.
- Lifetime `tau ~ M0^3`.

This is the classical/statistical evaporation package.

### Information-Flow Phenomenology

- Hard radiation is locally thermal.
- Radiation von Neumann entropy `S_vN(R)` is Page-like, with `S_2(R)` used as
  an explicitly labeled secondary diagnostic.
- Late radiation is correlated with early radiation.
- Purification is carried by global/soft records, not by hard-local radiation
  alone.

This is the information-puzzle phenomenology.

Important distinction:

```text
hard-radiation Shannon/von Neumann entropy and Page-curve von Neumann entropy
are different quantities.
```

The Page entropy is `S_vN(R)`, the von Neumann entropy of the emitted radiation
sector under the full purification.

### Gravity-Free Comparison

- The model contains no gravity.
- The same phenomenology package still appears.
- Therefore the package is not by itself diagnostic of gravity.

This is the point of the project.

## Diagnostics And Model Comparisons

These checks identify which model ingredients generate the target behavior.

### Emission-Rate Diagnostics

The evaporation power should come from weighted outgoing channels:

- Bath density of states.
- Transition matrix elements.
- Microcanonical state-count ratios.
- Emitted energy.

The corresponding weighted-power diagnostic is:

```text
W_L = sum_omega rho_bath(omega)
                |g_L(omega)|^2
                exp[S(L, E-omega) - S(L, E)]
                omega.
```

For the edge-tension model, this means checking that the explicit finite
emission channel reproduces:

```text
P_L ~ boundary * T_L^3 ~ M^-2.
```

This diagnostic connects the thermodynamic temperature to an actual emission
rate.

### Mass-Law And Bath Comparisons

The model should show which assumptions produce the Schwarzschild-like
exponents.

Useful comparison cases:

- Change the mass law.
- Change the bath dimension.
- Change the emission spectrum.
- Check which versions keep or lose `T ~ 1/M` and `P ~ M^-2`.

These comparisons show which assumptions produce the observed scaling.

### Scrambling Diagnostics And Comparisons

The model should show that Page-like information flow depends on real
scrambling or typicality.

Useful diagnostics and comparison cases:

- Scrambling dynamics.
- No-scrambling dynamics.
- Local scrambling.
- Expander-like scrambling.
- Operator-spreading or entanglement-growth diagnostics.

The strongest black-hole analogy wants fast scrambling. The finite toy model
requires enough scrambling to support the information-flow diagnostics.

### Naturalness And Autonomy

Literature check:

```text
notes/floquet_hamiltonian_literature_check.md
```

There are two different naturalness standards:

```text
Hamiltonian-realizable driven/stroboscopic cycle:
  repeat the same unitary cycle, U_cycle.

natural time-independent autonomous Hamiltonian:
  choose one H_total and let exp(-i H_total t) run.
```

A repeated unitary cycle is already Hamiltonian evolution in the stroboscopic
sense:

```text
|psi_{n+1}> = U_cycle |psi_n>
U_cycle = exp(-i H_eff T)
```

up to the usual choice of logarithm for `H_eff`.

The remaining naturalness issue is whether the same behavior follows from a
simple time-independent microscopic Hamiltonian without an engineered sequence
of stages.

The current project targets the driven/stroboscopic standard. The
time-independent autonomous standard is a harder follow-up.

## Current Status And Next Steps

Under the Floquet toy-model standard, the current model plausibly has:

```text
model specification:
  achieved under the Floquet toy-model standard;

Schwarzschild-like thermodynamics:
  achieved;

information-flow phenomenology:
  achieved-minus, because early/late mutual information and a small Page-like
  fused entropy turnover are present but still need larger runs;

gravity-free comparison:
  achieved;

rate-generation diagnostic:
  achieved-minus, because microcanonical/golden-rule weights and large-L
  weighted-power scaling are now computed, but the exact state-vector run still
  uses a smaller register scale;

scrambling diagnostics/comparisons:
  achieved-minus, because the fused diagnostic has threshold/seeds comparisons
  but remains small;

naturalness/autonomy:
  achieved for a Hamiltonian-realizable driven cycle;
  open for a simple time-independent autonomous Hamiltonian.
```

The most important next technical improvements are:

```text
1. final unitary cycle; done in notes/final_floquet_cycle_spec.md;
2. early-late mutual information; done in the fused diagnostics, now needs
   larger exact runs;
3. fused Page-like entropy probe; done in notes/fused_floquet_page_probe_results.md,
   now needs larger exact runs;
4. hard-alphabet stress test; done in notes/fused_floquet_multibin_results.md;
5. threshold-rule variants; done in notes/fused_floquet_threshold_variant_results.md;
6. weighted-power diagnostic; done in notes/fused_floquet_time_resolved_results.md,
   now needs larger exact runs;
7. keep the time-independent autonomous-Hamiltonian version as a harder
   follow-up.
```

The clean conceptual claim is:

```text
A non-gravitational finite quantum toy model can reproduce the usual
thermodynamic and information-flow phenomenology bundled with black-hole
evaporation. Therefore that phenomenology alone does not isolate the
gravitational part of the black-hole information problem.
```
