# Step 3 Candidate Assessment

## Question

Which natural finite-system core is most promising for replacing the engineered
shell density of states?

Step 3 needs a Hamiltonian or model whose microcanonical entropy naturally has
a convex window:

```text
S''(E) > 0
```

so that the core has negative microcanonical heat capacity without choosing
shell dimensions by hand.

## Literature signal

The strongest general signal is not from black-hole analogues, but from
finite-system microcanonical thermodynamics:

```text
finite first-order transitions
phase coexistence
interfaces/surface tension
long-range/nonadditive interactions
finite clusters
```

These are the standard places where convex intruders and negative heat capacity
appear.

## Candidate ranking

### 1. Long-range spin model

Verdict:

```text
best first implementation probe
```

Why:

```text
we already have spin exact-diagonalization infrastructure
finite Hilbert spaces are simple
long-range/nonadditive interactions are known to produce ensemble
inequivalence and negative specific heat
coupling operators to radiation bins are straightforward
```

Literature support:

```text
long-range interacting spin chains can show negative specific heat and
temperature jumps in the microcanonical ensemble
```

Risk:

```text
the convex window may be small or binning-sensitive
fully connected spin spectra can have artifacts/symmetries
may look too close to the old XXZ core unless we choose the model carefully
```

Best first model:

```text
long-range transverse-field Ising / XXZ variant
H = -J/N sum_{i<j} sigma_i^z sigma_j^z
    - h sum_i sigma_i^x
    + weak disorder
```

What to test:

```text
N = 10, 12, maybe 14 with sparse methods
scan J, h, disorder
bin eigenvalues
compute S(E), beta(E), S''(E)
check robustness under bin width
```

Assessment:

```text
most practical route to a Step 3 diagnostic, but not the most physically
evaporator-like.
```

### 2. Attractive Bose-Hubbard / dimer aggregate

Verdict:

```text
best quantum-droplet candidate, second implementation priority
```

Why:

```text
standard quantum Hamiltonian
natural bosonic clustering/self-trapping physics
literature explicitly connects Bose-Hubbard dimer aggregates to negative
specific heat / prethermalization
closer to a finite droplet than a spin model
```

Literature support:

```text
Ray, Anglin, and Vardi study prethermalization with negative specific heat in
Bose-Hubbard-type aggregate systems.
```

Risk:

```text
generic small attractive Bose-Hubbard clusters may not show a clean convex
S(E) window
the negative-specific-heat mechanism in the literature may involve
quasiparticles/adiabatic invariants rather than simple DOS convexity
Hilbert spaces grow quickly with particle number and site count
```

Best first model:

```text
few coupled Bose-Hubbard dimers
fixed total particle number
scan interaction/hopping and inter-dimer coupling
```

Alternative:

```text
small attractive Bose-Hubbard ring or cluster with 4-6 sites and 6-10 bosons
```

What to test:

```text
exact diagonalization in fixed-N sector
DOS and microcanonical derivatives
look for convexity stable under binning
```

Assessment:

```text
more work than spins, but more compelling if it works.
```

### 3. Potts / lattice first-order model

Verdict:

```text
best benchmark for convex intruders, weaker as final quantum core
```

Why:

```text
finite first-order Potts models are a textbook microcanonical convex-intruder
example
exact enumeration or Wang-Landau sampling can expose S(E)
excellent sanity check for the entropy-diagnostic pipeline
```

Literature support:

```text
finite 2D nearest-neighbor and mean-field Potts models exhibit convex dips in
S(E) at first-order transitions
```

Risk:

```text
classical model, not a quantum Hamiltonian core
unitary radiation coupling would require a quantum embedding
may become a detour if treated as the main Step 3 route
```

Best use:

```text
validate the microcanonical convexity detector
provide a classical finite-system benchmark
```

Assessment:

```text
high confidence for finding convexity, lower relevance to the quantum
Hamiltonian evaporator.
```

### 4. Finite droplet / atomic cluster model

Verdict:

```text
strongest physical analogy, hardest implementation
```

Why:

```text
negative heat capacity has been experimentally observed in sodium clusters
finite cluster evaporation/melting is physically close to the evaporator story
convex intruders are natural in phase coexistence and finite droplets
```

Literature support:

```text
Schmidt et al. report negative heat capacity for Na_147 clusters.
finite clusters are a canonical setting for microcanonical negative heat
capacity.
```

Risk:

```text
natural implementation is classical molecular dynamics, not finite quantum ED
quantum Hilbert-space model is nontrivial
coupling to radiation bins would be a second modeling layer
```

Best use:

```text
motivation and physical analogy
possible later classical/semiclassical companion model
```

Assessment:

```text
conceptually best, but not the first coding target.
```

## Recommended order

Proceed in this order:

```text
1. Long-range spin ED scan.
2. Attractive Bose-Hubbard / dimer aggregate scan.
3. Potts model as diagnostic benchmark if the entropy detector needs testing.
4. Droplet/cluster model only after deciding whether to invest in a separate
   classical or semiclassical core.
```

## What counts as promising

A candidate is promising only if:

```text
convex S(E) appears over several adjacent bins
the window survives changing the bin width
beta(E) remains physically interpretable in the window
the relevant shell dimensions are not tiny
the model has plausible operators for energy-lowering emission
```

## Probe update

See:

```text
notes/step3_natural_core_probe_results.md
```

Long-range spins were tested first because they were cheap. The simple
long-range transverse-field Ising-like scan did not find a robust convex
window; it produced only isolated or binning-sensitive positive-curvature
patches.

The attractive Bose-Hubbard scan is now the leading Step 3 route. The best
current candidate is:

```text
L=6, N=8, ring, J=0.5, U=-1, V=-0.2
```

In the focused scan this candidate passed 6 of 8 bin choices for two disorder
seeds. That is not yet a result about evaporation, but it is strong enough to
justify the next dynamical coupling test.

That dynamical coupling test has now been run in weak-coupling Markov form.
Using local density and hopping operators, the best DOS candidate usually
emits with decreasing power. A narrow hopping-only pocket shows modest
acceleration, but not robustly enough to call this a natural evaporator.

The current lesson is:

```text
convex DOS is necessary for this route, but not sufficient;
the energy-lowering matrix elements are an independent constraint.
```

Follow-up: the fixed-N probe was too unlike black-hole evaporation, because it
did not shrink the core Hilbert space. A variable-N Bose-Hubbard particle-loss
test has now been run:

```text
H_core = direct sum over N=8,...,3 Bose-Hubbard sectors
b_i : H_N -> H_{N-1}
```

That version does show robust accelerating emission in several scan regions.
Best grouped case:

```text
mu=6, max emitted gap=4, initial N=8 window [-18.5,-17]
mid / early emitted power:
  seed 2468: 1.359
  seed 2469: 1.362
```

See:

```text
notes/variable_n_bose_hubbard_results.md
```

## Current recommendation

Present the fixed-N Bose-Hubbard result as a failure/obstruction, but the
variable-N Bose-Hubbard result as a promising Step 3 lead.

Reason:

```text
The natural model only starts behaving like the black-hole analogue once the
core actually shrinks through particle loss.
```

Do not invest more in generic long-range spins unless there is a sharper model
from the literature.

Next step:

```text
build the reduced-density collision version of the variable-N particle-loss
model and check whether the acceleration survives a more explicitly unitary
radiation-bin formulation.
```

## Sources checked

```text
Schmidt et al., "Negative heat capacity for a cluster of 147 sodium atoms",
Phys. Rev. Lett. 86, 1191 (2001).

Gross and collaborators on microcanonical first-order transitions and convex
intruders in finite systems / Potts models.

Ispolatov and Cohen, "On first-order phase transitions in microcanonical and
canonical non-extensive systems", Physica A 295, 475 (2001).

Ray, Anglin, and Vardi, "Prethermalization with negative specific heat",
Phys. Rev. E 102, 052107 (2020).

Long-range interacting spin-chain work reporting microcanonical negative
specific heat and temperature jumps.
```
