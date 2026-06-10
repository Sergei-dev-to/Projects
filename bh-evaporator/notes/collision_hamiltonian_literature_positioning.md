# Collision Hamiltonian Literature Positioning

## Question

Before building further on the collision Hamiltonian,

```text
H_coll = g (V + V^\dagger),
```

check whether this has already been analyzed in the literature for the purpose
we care about:

```text
a non-gravitational finite quantum system reproducing the black-hole
evaporation package, especially shrinking state count, S ~ M^2,
negative heat capacity, accelerating evaporation, and unitary radiation.
```

## Short Verdict

The Hamiltonian trick itself is not new.

It is a standard way to realize an isometric channel by coherent unitary
evolution in a larger space. It belongs naturally to:

```text
Stinespring dilation / quantum channels;
collision models / repeated-interaction models;
Wigner-Weisskopf / Friedrichs-Lee decay models;
quantum optical emission models.
```

The microcanonical emission factor is also not new in isolation:

```text
Gamma(omega) ~ rho(omega) exp[S(M - omega) - S(M)]
```

is the usual entropy-ratio / detailed-balance logic, and in black-hole
language is very close to the Parikh-Wilczek tunneling correction
`Gamma ~ exp(Delta S_BH)`.

What may still be nontrivial is the combined package:

```text
finite non-gravitational constrained droplet
+ exact area-like state count
+ boundary-tension mass
+ negative heat capacity
+ accelerated evaporation into a 2D bath
+ microcanonical hard emission weights
+ Hamiltonian-generated hard/soft erosion
+ explicit comparison against black-hole phenomenology.
```

That package is not obviously present in the first-pass literature check.

## What Is Definitely Standard

### 1. Channel to isometry

Any completely positive quantum channel can be represented by a Stinespring
isometry,

```text
rho -> Tr_env[V rho V^\dagger].
```

So writing an erosion step as an isometry is not novel.

### 2. Isometry to finite Hamiltonian block

Given an isometry `V`, the block Hamiltonian

```text
H = g(V + V^\dagger)
```

coherently rotates an input sector into an output sector. This is a finite
Hamiltonian realization of the channel, not a new dynamical principle.

Our contribution cannot be:

```text
we found that H = V + V^\dagger generates a channel.
```

It can only be:

```text
this standard channel realization closes a specific weak point in the
edge-tension evaporator.
```

### 3. Collision / repeated-interaction models

The idea of a system interacting sequentially with fresh ancillas is a mature
open-systems framework. It is used to model dissipation, thermalization,
quantum trajectories, non-equilibrium thermodynamics, and Markovian limits.

Our erosion steps are best read as a collision model unless we later replace
them with one autonomous Hamiltonian containing all droplet sectors and the
external bath.

### 4. Decay into a continuum

The older Wigner-Weisskopf, Friedrichs, and Lee models already describe a
discrete unstable state coupled to outgoing continuum modes. They are the
natural Hamiltonian benchmark for emission rates from matrix elements and
density of states.

This means the next real F7 upgrade is not another abstract isometry. It is a
Fermi-golden-rule calculation for a droplet sector coupled to bath modes.

## What Is Close In Black-Hole Toy Models

### Avery

Avery gives a broad class of qubit evaporation models, including unitary and
nonunitary cases, and emphasizes how large the departure from Hawking's
nonunitary model must be.

Overlap:

```text
finite qubit evaporation;
unitary channel logic;
information transfer constraints.
```

Missing relative to our target:

```text
non-gravitational thermodynamic engine;
S ~ M^2 from state count;
negative heat capacity and acceleration as derived scalings.
```

### Osuga-Page

Osuga and Page give an explicit unitary qubit transport model transferring
information from black-hole degrees of freedom to Hawking radiation.

Overlap:

```text
shrinking black-hole/radiation split;
unitary information transfer;
qualitative evaporation model.
```

Missing relative to our target:

```text
detailed thermodynamic spectrum;
negative heat capacity as the driver;
non-gravitational control system with explicit state-count/mass law.
```

### Hotta-Nambu-Yamaguchi and later soft-hair qubit models

These are very close to our hard/soft split conceptually: hard Hawking
particles plus soft/zero-energy records or hair carrying additional
correlations.

Overlap:

```text
hard/soft radiation bookkeeping;
shrinking active qubit sector;
Page-curve-adjacent entanglement diagnostics.
```

Missing relative to our target:

```text
finite constrained droplet count;
boundary-tension mass;
clean non-gravitational thermodynamic control.
```

### Black Hole Waterfall / quantum optical models

These use quantum-optical Hamiltonians, squeezed states, beam splitters, and
pump depletion to build unitary evaporation models with Page-like behavior.

Overlap:

```text
Hamiltonian / optical implementation;
unitarity;
thermal-looking radiation;
Page curve;
finite mass depletion.
```

Missing or different:

```text
not a constrained gauge droplet;
not obviously S ~ M^2 from finite internal state count;
not centered on negative heat capacity from area entropy vs boundary energy.
```

## Microcanonical Emission Is Also Not New

The factor

```text
exp[S(M - omega) - S(M)]
```

should be treated as standard physics.

In ordinary statistical mechanics it is the final-state density divided by the
initial-state density. In black-hole tunneling literature it is essentially the
Parikh-Wilczek result:

```text
Gamma ~ exp(Delta S_BH).
```

Therefore our use of it is not a novelty claim. Its role is to make the
evaporator less arbitrary:

```text
hard probabilities are no longer chosen as Boltzmann weights;
they arise from the droplet entropy curve plus bath phase space.
```

## What May Remain Interesting

The possible result is not a new Hamiltonian form. It is a control construction:

```text
Black-hole-like evaporation thermodynamics can be reproduced by a finite
non-gravitational quantum droplet if:

1. entropy is extensive in area;
2. energy is dominated by boundary tension;
3. radiation phase space is effectively 2D;
4. emission weights follow microcanonical detailed balance;
5. erosion is represented by a purifiable hard/soft channel.
```

This separates a large amount of black-hole phenomenology from gravity:

```text
S ~ M^2,
T ~ 1/M,
C < 0,
accelerating evaporation,
thermal-looking local radiation,
global purification in correlations.
```

The real gravitational residue would then be:

```text
why horizons realize those ingredients;
how islands/wormholes encode the purification mechanism;
what replaces the non-gravitational droplet channel in actual semiclassical
gravity.
```

## Literature Check Outcome

First-pass status:

```text
H_coll form: already standard.
microcanonical exp(Delta S): already standard.
hard/soft qubit bookkeeping: already nearby in soft-hair models.
Page-like unitary evaporation: heavily studied.
negative heat capacity + accelerating finite non-grav droplet with exact
constrained state count: not found yet in the same package.
```

So the next step should not be to sell the Hamiltonian as new.

The next step should be to test whether the edge-tension droplet package is
robust enough to survive more physical Hamiltonian choices:

```text
1. replace the modular collision pulse with a golden-rule bath coupling;
2. derive erosion rates from matrix elements and bath density of states;
3. check whether the same S~M^2, T~1/M, P~1/M^2, and hard/soft information
   pattern remain.
```

If yes, there is likely an interesting result.

If no, the failure will identify which part of the black-hole package was being
put in by hand.

## Has The Golden-Rule Upgrade Already Been Done?

Partly, but not for our exact target.

The closest prior step is Braunstein and Patra's "Black hole evaporation rates
without spacetime." They derive black-hole evaporation rates from a Hilbert-space
description, high-dimensional symmetry, conservation of no-hair quantities, and
Penrose-process logic, rather than from a local spacetime QFT calculation. That
is very close in spirit to:

```text
derive rates from Hilbert-space structure rather than prescribe Hawking
thermality.
```

But it is still a black-hole/event-horizon argument. It does not give a concrete
non-gravitational finite droplet Hamiltonian with:

```text
dim H_L = q^(L^2),
M_L ~ L,
T_L ~ 1/L,
P_L ~ 1/L^2.
```

The Parikh-Wilczek tunneling calculation also covers a key part of the same
rate logic. It gives an emission probability governed by the black-hole entropy
change:

```text
Gamma ~ exp(Delta S_BH).
```

So our microcanonical factor is not new:

```text
Gamma_L(omega) ~ rho_bath(omega) exp[S(M_L - omega) - S(M_L)].
```

The useful role of this step is not novelty. It ties the toy evaporator to
standard black-hole emission logic.

Quantum-optical black-hole evaporation models are also close. The Black Hole
Waterfall model uses a fully quantized trilinear/SPDC Hamiltonian, pump
depletion, unitary evolution, and a Page-like curve. That is a genuine
Hamiltonian evaporation model. But its thermodynamic engine is different from
ours: it does not appear to derive the Schwarzschild-like package from an exact
finite constrained state count plus boundary-tension mass.

Therefore the honest answer is:

```text
The golden-rule / entropy-ratio step has been done in black-hole and generic
open-system settings.

Hamiltonian unitary evaporation models have also been done.

What I have not found is this step done for a non-gravitational finite
edge-tension constrained droplet, where the same rate calculation preserves
S~M^2, T~1/M, C<0, P~1/M^2, and hard/soft purification diagnostics.
```

This makes the next calculation worthwhile as a diagnostic, but not because the
method is new. It is worthwhile because it tests whether our candidate survives
when moved from a collision-channel construction to the standard rate-calculus
language used in black-hole and open-system physics.

## Sources Checked

```text
Ciccarello et al., "Quantum collision models: Open system dynamics from
repeated interactions", arXiv:2106.11974.

Attal and Pautrat, "From repeated to continuous quantum interactions",
arXiv:math-ph/0311002.

Avery, "Qubit Models of Black Hole Evaporation", arXiv:1109.2911.

Osuga and Page, "Qubit Transport Model for Unitary Black Hole Evaporation
without Firewalls", arXiv:1607.04642.

Hotta, Nambu, and Yamaguchi, "Soft-Hair-Enhanced Entanglement Beyond Page
Curves in a Black-hole Evaporation Qubit Model", arXiv:1706.07520.

Alsing, "Black Hole Waterfall: a unitary phenomenological model for black hole
evaporation with Page curve", arXiv:2501.00948.

Alsing, "Quantum Optical Inspired Models for Unitary Black Hole Evaporation",
arXiv:2601.09820.

Parikh and Wilczek, "Hawking Radiation As Tunneling", Phys. Rev. Lett. 85,
5042.

Hategan, "Entanglement Entropy in Pure Z2 Gauge Lattices", arXiv:1705.10474.

Buividovich and Polikarpov, "Entanglement entropy in lattice gauge theories",
arXiv:0811.3824.

Glatthard, "Page-curve-like entanglement dynamics in open quantum systems",
arXiv:2401.06042.

Glatthard, "Thermodynamics of the Page curve in Markovian open quantum
systems", arXiv:2501.09082.
```
