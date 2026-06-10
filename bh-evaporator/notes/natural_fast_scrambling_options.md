# Natural Fast-Scrambling Options

## Purpose

After the initial-state dependence test, the erosion channel needs one more
ingredient:

```text
the shell should be locally mixed before it is emitted.
```

This note asks what a more natural source of that scrambling could be.

## Constraint From Our Model

The edge-tension droplet has:

```text
S ~ R^2
M ~ R
T ~ 1/R
P ~ 1/R^2
```

One lattice-thick shell has:

```text
Delta M ~ O(1)
Delta S ~ O(R).
```

The time to erode one shell is therefore roughly:

```text
t_shell ~ Delta M / P ~ R^2.
```

That matters. We do not necessarily need black-hole-optimal scrambling

```text
t_scr ~ beta log S.
```

For the current droplet, it may be enough that:

```text
t_mix << R^2.
```

So ordinary local chaotic dynamics in 2D might be adequate, even if it is not a
fast scrambler in the Sekino-Susskind sense.

## Literature Landmarks

### Fast scrambling on sparse graphs

Bentsen, Gu, and Lucas argue that logarithmic scrambling can be achieved in
many quantum systems with sparse connectivity, using Lieb-Robinson bounds,
generalized SYK models, and random circuits.

Relevance:

```text
sparse nonlocal graph connectivity can give fast scrambling without complete
all-to-all coupling.
```

This is attractive if the constrained droplet's effective interaction graph is
allowed to be an expander rather than a 2D lattice.

Source:

```text
Gregory Bentsen, Yingfei Gu, Andrew Lucas,
"Fast scrambling on sparse graphs",
PNAS 116, 6689 (2019);
arXiv:1805.08215.
```

### Expander horizons

Barbon and Magan propose local quantum systems on expander graphs as simple
microscopic models for horizon thermalization. The key point is that bounded
degree plus expander connectivity can produce rapid mixing without a complete
graph.

Relevance:

```text
closest conceptual match to "horizon-like fast scrambling without gravity."
```

Weakness:

```text
an expander graph is a chosen nonlocal geometry, not the ordinary geometry of
the 2D droplet.
```

Source:

```text
Jose L. F. Barbon, Javier M. Magan,
"Fast Scramblers, Horizons and Expander Graphs",
JHEP 08 (2012) 016;
arXiv:1204.6435.
```

### Minimal global-coupling model

Belyansky et al. show that a simple global, spatially homogeneous interaction,
combined with local chaotic dynamics, can give logarithmic fast scrambling.

Relevance:

```text
we could add one collective gauge-invariant mixer to an otherwise local
constrained droplet.
```

This is less artificial than Haar scrambling but more artificial than purely
local plaquette dynamics.

Source:

```text
Ron Belyansky et al.,
"Minimal Model for Fast Scrambling",
Phys. Rev. Lett. 125, 130601 (2020);
arXiv:2005.05362.
```

### SYK / sparse SYK

SYK is the standard non-gravitational fast-scrambling model, with all-to-all
random few-body interactions. Sparse SYK variants reduce the number of
interactions.

Relevance:

```text
excellent fast-scrambling benchmark;
bad fit to a geometric edge-tension droplet unless used only as an internal
scrambler control.
```

It would make the model less natural, not more natural, if inserted directly.

### ETH in constrained Hilbert spaces

Chandran, Schulz, and Burnell studied ETH in a pinned Fibonacci anyon chain,
showing that constrained Hilbert spaces can still admit locality and
thermalization under generic nonintegrable dynamics.

Relevance:

```text
constraints are not automatically an obstacle to thermalization.
```

Weakness:

```text
ETH/local thermalization is not the same as logarithmic fast scrambling.
```

Source:

```text
A. Chandran, M. D. Schulz, F. J. Burnell,
"The eigenstate thermalization hypothesis in constrained Hilbert spaces",
Phys. Rev. B 94, 235122 (2016);
arXiv:1607.00388.
```

### Quantum link models

Quantum link models give finite-dimensional Hamiltonian lattice gauge theories.
They are a natural setting for local gauge-invariant dynamics in a finite
Hilbert space.

Relevance:

```text
good microscopic language for constrained local dynamics and gauge-invariant
scrambling tests.
```

Weakness:

```text
generic local gauge dynamics is not automatically fast; it may be ballistic or
diffusive.
```

Source:

```text
S. Chandrasekharan, U.-J. Wiese,
"Quantum Link Models: A Discrete Approach to Gauge Theories",
Nucl. Phys. B492, 455-474 (1997);
arXiv:hep-lat/9609042.
```

### Scars and fragmentation as warnings

Constrained systems can fail to thermalize because of scars or Hilbert-space
fragmentation. PXP/Fibonacci-chain physics is the cautionary example: a
constrained Hilbert space can have mostly thermalizing behavior but special
states with anomalous revivals.

Relevance:

```text
we cannot assume "constrained" means "scrambling."
```

Source:

```text
C. J. Turner et al.,
"Weak ergodicity breaking from quantum many-body scars",
Nature Physics 14, 745-749 (2018).
```

## Candidate Mechanisms For Us

### A. Local chaotic constrained dynamics

Use a generic nonintegrable Hamiltonian inside the constrained gauge/ice
manifold:

```text
H_mix = sum local plaquette/ring-exchange terms
      + noncommuting local defect/flux terms
```

Pros:

```text
most natural;
keeps the 2D droplet picture;
connects to ETH in constrained spaces;
no extra graph geometry.
```

Cons:

```text
not true fast scrambling;
may be ballistic or diffusive;
can have scars or fragmentation if chosen poorly.
```

Why it may be enough:

```text
t_shell ~ R^2.
```

If local constrained dynamics mixes shell observables in time `R` or even
somewhat below `R^2`, the shell can be locally mixed before erosion completes.

Status:

```text
best "least imposed" next diagnostic.
```

### B. Expander-coupled constrained droplet

Keep the same plaquette/shell Hilbert space, but let soft plaquette variables
interact on a fixed bounded-degree expander graph rather than only nearest
neighbors on the 2D lattice.

Pros:

```text
logarithmic scrambling is structurally motivated;
bounded degree, not all-to-all;
literature directly connects expanders to horizons.
```

Cons:

```text
the expander is extra emergent geometry;
the droplet is no longer purely local in its visible 2D geometry.
```

This is useful as a fast-scrambling control, but less natural than option A.

### C. Local dynamics plus one global gauge-invariant mixer

Add a simple collective interaction:

```text
H = H_local_constrained + lambda H_global
```

where `H_global` is homogeneous and gauge-invariant, e.g. a collective flux or
ring-exchange mixer.

Pros:

```text
matches the "minimal model for fast scrambling" literature;
less arbitrary than Haar steps;
can be tested with small exact circuits.
```

Cons:

```text
global interaction is still an added ingredient;
may look like a disguised scrambling oracle.
```

This is a good intermediate diagnostic if option A is too slow.

### D. SYK-like internal scrambler

Attach an SYK/sparse-SYK Hamiltonian to the soft plaquette labels.

Pros:

```text
known fast scrambler;
clear benchmark.
```

Cons:

```text
least natural for a gauge/ice droplet;
random all-to-all few-body couplings obscure the physical point.
```

Use only as a control, not as the main model.

## What We Should Not Do

Do not simply insert Haar scrambling between erosion steps and declare victory.

That would prove only:

```text
if the droplet is scrambled, the erosion channel works.
```

We already know that.

The next step must test whether a plausible Hamiltonian or structured circuit
can produce the required shell mixing.

## Recommended Next Diagnostic

Start with option A:

```text
local chaotic constrained dynamics on the plaquette-flux shell decomposition.
```

Minimal implementation:

```text
1. Represent the droplet as L^2 q-dits in plaquette-flux variables.
2. Use local two-plaquette or plaquette-ring gates preserving the total sector
   if needed.
3. Evolve for a depth D before each erosion step.
4. Start from product/basis states that previously failed.
5. Measure whether the outer shell becomes locally mixed enough for
   shift/clock erosion to produce thermal hard radiation.
```

Depth scan:

```text
D = 0, 1, 2, 4, 8, 16, ...
```

Diagnostics:

```text
outer-shell entropy and purity before erosion;
latest hard trace distance from thermal;
hard-hard early/late mutual information;
hard+soft early/late mutual information.
```

If local depth `D ~ L` works, that is already enough for the current droplet,
because:

```text
L << t_shell ~ L^2.
```

If only expander/global depth `D ~ log L` works, then we have a choice:

```text
accept an extra fast-scrambler ingredient,
or weaken the claim to ordinary local pre-thermalization before slow erosion.
```

## Current Verdict

The most natural path is not to force black-hole-optimal fast scrambling.

For this non-gravitational droplet, the more defensible claim is:

```text
ordinary constrained chaotic dynamics can make each shell locally typical before
the much slower boundary-erosion process removes it.
```

Expander/global/SYK mechanisms are useful controls, but if we use them as the
main mechanism, the model becomes less natural.

## First Diagnostic Completed

Relevant note:

```text
notes/local_scrambling_before_erosion_results.md
```

Result:

```text
modest-depth local plaquette-flux circuits repair the product-state failures in
the structured erosion channel.
```

In small exact tests, depth `D = 4` local circuits make the formerly failing
`basis_all`, `uniform_all`, and `factor_haar` initial states emit
thermal-looking hard radiation while recovering nonzero hard+soft early/late
correlations.

The effect survives a stricter flux-conserving two-site circuit, so it is not
only a consequence of arbitrary unconstrained two-qdit gates.

This supports the claim:

```text
local constrained scrambling is sufficient.
```

It does not yet establish:

```text
a specific local Hamiltonian naturally produces the scrambling.
```
