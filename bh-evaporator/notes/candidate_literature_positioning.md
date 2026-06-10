# Candidate Literature Positioning

## Question

Does the current candidate,

```text
Edge-Tension Expander Evaporator
```

already exist in the literature, either explicitly or in a close enough form
that our program is just a relabeling?

## Short Verdict

I do not see the full package already present.

Most ingredients are standard or nearby:

```text
Page curves without gravity;
unitary qubit evaporation;
shrinking black-hole/radiation registers;
soft/hard radiation bookkeeping;
quantum-optical Hamiltonian evaporation models;
microcanonical exp(Delta S) emission logic;
fast scrambling and sparse nonlocal dynamics;
repeated-interaction / collision models.
```

The combination that still looks less duplicated is:

```text
finite non-gravitational constrained droplet
+ area-like state count S_L = L^2 log q
+ boundary-tension mass M_L ~ L
+ negative heat capacity T_L ~ 1/M_L
+ 2D bath power P ~ M^-2
+ microscopic small-quanta emission
+ reversible shrinkage bookkeeping
+ Page/early-late radiation diagnostics
+ sparse interacting-spin fast-scrambling proxy.
```

So the honest novelty target is not any one mechanism. It is the integrated
control model.

## Comparison Axes

The relevant boxes are:

```text
A1 finite explicit quantum Hilbert space
A2 unitary or purifiable evaporation
A3 shrinking internal state space
A4 S ~ M^2 from state count
A5 T ~ 1/M and C < 0
A6 accelerating evaporation / P ~ M^-2 / tau ~ M0^3
A7 emission rates from density of states or matrix elements
A8 Page-like radiation entropy
A9 early/late radiation correlations
A10 non-gravitational control value
A11 fast scrambling / rapid operator spreading
A12 one repeated-interaction rule or autonomous Hamiltonian
```

Compact status:

```text
Work / class                    A1 A2 A3 A4 A5 A6 A7 A8 A9 A10 A11 A12
--------------------------------------------------------------------------
Page theorem                    Y  P  N  N  N  N  N  Y  P  P   N   N
Glatthard open systems          Y  P  N  N  N  N  N  Y  N  Y   N   P
Avery qubit models              Y  P  P  P  P  P  P  Y  P  P   P   P
Osuga-Page transport            Y  Y  Y  P  P  P  P  Y  P  P   P   P
Hotta-Nambu-Yamaguchi           Y  P  Y  Y  Y  P  P  Y  P  P   P   P
Black Hole Waterfall            Y  Y  P  P  P  P  Y  Y  P  P   N   P
Local spin-chain Page models    Y  Y  P  P  N  P  P  Y  P  P   N   P
SYK / evaporating JT family     Y  Y  P  P  P  P  Y  Y  Y  N   Y   P
Edge-Tension Expander           Y  P  P  Y  Y  Y  P  P+ P+ Y   P+  P+
```

Legend:

```text
Y   clear
P   partial / model-dependent / not the central point
P+  substantial evidence but not a complete derivation
N   absent or not central
```

## Closest Prior Lanes

### Page and Random Typicality

Page's original result already explains why radiation entropy should rise and
then fall in a finite unitary evaporation process when the radiation Hilbert
space overtakes the remaining black-hole Hilbert space.

Overlap:

```text
Page-like entropy curve;
early/late correlation expectation from finite-dimensional typicality.
```

Missing relative to us:

```text
no thermodynamic engine;
no negative heat capacity;
no emission schedule;
no non-gravitational droplet system.
```

Consequence:

```text
We should never present the Page curve itself as the novelty.
```

### Glatthard Open-System Page Curves

Glatthard shows that Page-curve-like entropy dynamics is generic in ordinary
open quantum systems relaxing toward low-temperature states.

Overlap:

```text
Page-like entropy outside gravity;
thermodynamic interpretation of subsystem entropy decrease.
```

Missing relative to us:

```text
the system cools in the ordinary way;
no black-hole-like negative heat capacity;
no S ~ M^2 constrained state count;
no accelerating evaporation engine.
```

Consequence:

```text
Our differentiator is not "Page curves without gravity."
It is "Page-like information flow tied to a negative-C evaporator."
```

### Qubit Evaporation Models

Avery and Osuga-Page cover much of the finite-register evaporation logic:
unitary transfer, shrinking black-hole registers, and radiation information
flow.

Overlap:

```text
finite qubit evaporators;
unitary or purifiable core-to-radiation transfer;
black-hole/radiation register resizing.
```

Missing relative to us:

```text
no finite non-gravitational constrained droplet;
no area state count plus boundary-tension mass as the thermodynamic origin;
no explicit control separating mass-law, bath dimension, and scrambling.
```

Consequence:

```text
Our shrinkage map is not new in spirit.
The value is tying it to a specific thermodynamic state-count model.
```

### Soft-Hair / Hard-Soft Qubit Models

Hotta, Nambu, and Yamaguchi are a serious overlap warning. They include hard
Hawking particles, zero-energy soft-hair evaporation, qubit shrinkage, fast
scrambling assumptions, and Schwarzschild-like thermodynamic relations.

Overlap:

```text
hard/soft split;
shrinking active qubit sector;
thermal-looking hard radiation;
soft records carrying correlations;
negative heat capacity / Schwarzschild-like temperature behavior.
```

Missing or different:

```text
their model is explicitly black-hole motivated;
their entropy/mass package is put in through the qubit black-hole ansatz;
they do not isolate a non-gravitational constrained droplet with
S_L = L^2 log q and M_L ~ boundary;
they do not run our current control suite:
  bath dimension,
  mass-law exponent,
  grid vs expander scrambling,
  free vs interacting Hamiltonian,
  finite bath-density emission.
```

Consequence:

```text
This is the closest conceptual neighbor.
Any writeup must say exactly how the edge-tension droplet differs.
```

### Quantum-Optical / Waterfall Models

The Black Hole Waterfall and related quantum-optics models use unitary
Hamiltonian processes, pump depletion, and squeezed-state cascades to produce
Page-like behavior and black-hole-inspired evaporation.

Overlap:

```text
unitary Hamiltonian evaporation;
finite energy depletion;
thermal-looking radiation;
Page curve;
late-time information recovery.
```

Missing or different:

```text
not a finite constrained area-entropy droplet;
not primarily a negative-C thermodynamic derivation;
not organized around S ~ M^2 from state count plus M ~ boundary;
does not give the same clean P ~ M^-2 from 2D bath phase space.
```

Consequence:

```text
They are closer to "unitary black-hole phenomenology simulator."
We are closer to "non-gravitational thermodynamic control model."
```

### Microcanonical Emission / Exp(Delta S)

The factor

```text
Gamma(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)]
```

is standard statistical mechanics and is also close to the Parikh-Wilczek
tunneling result for black-hole radiation.

Overlap:

```text
entropy-ratio emission;
detailed-balance logic;
nonthermal corrections from finite reservoir entropy.
```

Missing relative to us:

```text
not applied to a finite non-gravitational edge-tension constrained droplet
with the full Page/scrambling/shrinkage architecture.
```

Consequence:

```text
The emission formula is not new.
Its role is to keep our toy model honest.
```

### Fast Scrambling

Fast scrambling is a black-hole-motivated standard, and sparse nonlocal
systems/expanders/random circuits are natural ways to approximate it.

Overlap:

```text
rapid operator spreading;
Hayden-Preskill intuition;
nonlocal sparse interactions as a route to faster-than-grid scrambling.
```

Missing relative to us:

```text
fast scrambling papers do not supply the edge-tension evaporator package;
our current expander Hamiltonian tests are evidence for one module, not the
whole model.
```

Consequence:

```text
F14 is a borrowed standard, not a novelty.
The useful point is that the thermodynamic droplet can be paired with a
plausible sparse nonlocal scrambler.
```

## What Seems Actually Open

The question that still looks interesting is:

```text
Can one build a finite non-gravitational quantum evaporator where the same
state-count/mass structure gives:

1. S ~ M^2,
2. T ~ 1/M,
3. C < 0,
4. P ~ M^-2,
5. tau ~ M0^3,
6. shrinking internal capacity,
7. thermal local radiation,
8. Page-like global radiation entropy,
9. early/late correlations,
10. fast scrambling diagnostics?
```

The current candidate gets most of this at the architecture and diagnostic
level.

The remaining nontrivial gaps are:

```text
1. one less-modular Hamiltonian or Floquet rule;
2. larger Page/scrambling simulations;
3. bath density derived from a bath Hamiltonian rather than assigned;
4. shrinkage trigger derived from dynamics rather than threshold bookkeeping;
5. sharper comparison to Hotta-Nambu-Yamaguchi and quantum-optical waterfall
   models.
```

## Positioning Sentence

The most defensible one-sentence positioning is:

```text
We construct a finite non-gravitational repeated-interaction evaporator in
which the Schwarzschild-like thermodynamic package follows from area-like
constrained entropy and boundary-tension energy, while Page-like information
flow is supplied by unitary shrinkage and sparse chaotic scrambling.
```

The most important caveat is:

```text
At present this is an integrated architecture with analytic thermodynamic
scalings and finite-size quantum diagnostics, not a derivation from one
natural autonomous Hamiltonian.
```

## Source Pointers

Primary references checked:

```text
Page, "Information in black hole radiation", gr-qc/9306083.
https://arxiv.org/abs/gr-qc/9306083

Page, "Average entropy of a subsystem", gr-qc/9305007.
https://arxiv.org/abs/gr-qc/9305007

Glatthard, "Page-curve-like entanglement dynamics in open quantum systems",
arXiv:2401.06042.
https://arxiv.org/abs/2401.06042

Glatthard, "Thermodynamics of the Page curve in Markovian open quantum
systems", arXiv:2501.09082.
https://arxiv.org/abs/2501.09082

Avery, "Qubit Models of Black Hole Evaporation", arXiv:1109.2911.
https://arxiv.org/abs/1109.2911

Osuga and Page, "Qubit Transport Model for Unitary Black Hole Evaporation
without Firewalls", arXiv:1607.04642.
https://arxiv.org/abs/1607.04642

Hotta, Nambu, and Yamaguchi, "Soft-Hair-Enhanced Entanglement Beyond Page
Curves in a Black-hole Evaporation Qubit Model", arXiv:1706.07520.
https://arxiv.org/abs/1706.07520

Alsing, "Black Hole Waterfall: a unitary phenomenological model for black
hole evaporation with Page curve", arXiv:2501.00948.
https://arxiv.org/abs/2501.00948

Braunstein and Patra, "Black hole evaporation rates without spacetime",
arXiv:1102.2326.
https://arxiv.org/abs/1102.2326

Parikh and Wilczek, "Hawking Radiation As Tunneling", hep-th/9907001.
https://arxiv.org/abs/hep-th/9907001

Sekino and Susskind, "Fast Scramblers", arXiv:0808.2096.
https://arxiv.org/abs/0808.2096

Piroli, Sunderhauf, and Qi, "A Random Unitary Circuit Model for Black Hole
Evaporation", arXiv:2002.09236.
https://arxiv.org/abs/2002.09236
```

## Bottom Line

The literature already supports the pessimistic reading:

```text
Page-like information behavior is generic finite quantum mechanics.
```

But it also leaves room for the useful reading:

```text
The black-hole phenomenology package may not require gravity once one has
area entropy, boundary energy, finite bath-density emission, and fast
scrambling.
```

That is the result worth chasing.

