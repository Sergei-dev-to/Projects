# Revision Memo: `bh-evaporator`

## Current best positioning

The strongest pitch is:

```text
We construct a non-gravitational quantum evaporator that combines
negative microcanonical heat capacity with unitary scrambling/emission,
thereby reproducing black-hole-like thermodynamic scalings and Page-like
information recovery in a controlled finite quantum system.
```

The paper should not be positioned primarily as:

```text
Page curve without gravity
```

because that literature is now crowded.

The differentiator is the combination:

```text
convex intruder / negative C_mu
accelerating evaporation
T(E) and P(E) black-hole-like scalings
unitary Page-like information flow
operational diagnostics for thermality, memory, and recovery
```

The clean category is:

```text
quantum simulation / control-model paper
```

not:

```text
black-hole information puzzle solution paper
```

## Literature positioning

### 1. Gravitational Page curve and islands

Use as background, not competition:

```text
Engelhardt-Wall QES
Penington 2019
Almheiri-Engelhardt-Marolf-Maxfield 2019
Almheiri-Hartman-Maldacena-Shaghoulian-Tajdini RMP
```

Our distinction:

```text
Gravity supplies the semiclassical entropy prescription:
  area term, QES extremization, islands, replica wormholes.

Our model supplies a non-gravitational control:
  what Page-like recovery and thermal-looking radiation look like
  in manifestly unitary finite quantum mechanics.
```

### 2. Page curves without gravity

This is crowded. Need cite and differentiate:

```text
Page 1993:
  random pure-state benchmark.

Nakata et al.:
  random unitary circuit model for black-hole evaporation.

Pastawski et al.:
  tensor-network models of unitary black-hole evaporation.

Liu-Vardhan:
  quantum-chaotic mechanism for Page curve.

Blake-Thompson:
  entanglement membrane Page curve in chaotic systems.

de Boer-Hollander-Rolph:
  Page curves and replica-wormhole-like contractions from random dynamics.

Glatthard:
  Page-curve-like dynamics in open quantum systems.

Kehrein:
  analytically solvable Page-curve entanglement dynamics.

Recent XXZ/bath work:
  Page-like behavior in spin chains/baths.
```

Our differentiation:

```text
Most of these isolate Page-like entanglement dynamics.
This manuscript tries to bind Page-like dynamics to a black-hole-like
thermodynamic engine: negative microcanonical heat capacity and accelerating
evaporation.
```

That should be stated explicitly in the introduction.

### 3. Negative heat capacity and convex intruders

This is the paper's most important non-Page literature base:

```text
Gross microcanonical thermodynamics
Schmidt et al. Na clusters negative heat capacity
D'Agostino nuclear multifragmentation
Campisi microcanonical phase transitions in small systems
Thirring/Hertel finite-system negative heat capacity
Ray-Anglin-Vardi negative-specific-heat/prethermal Bose-Hubbard context
```

Our differentiation:

```text
Finite-system negative heat capacity is known.
The contribution is using it as the thermodynamic engine for a unitary
black-hole-like evaporator.
```

### 4. Analogue gravity / quantum simulation

Existing analogues often probe kinematics:

```text
acoustic horizons
dynamical Casimir / moving mirrors
membrane paradigm analogies
photonic/cQED implementations
```

Our differentiation:

```text
focus on dynamical information flow and microcanonical thermodynamics,
not horizon kinematics.
```

## Main manuscript risks

### Risk 1: Overclaiming "information-theoretic universals"

Current text repeatedly says:

```text
generic
universal
information-theoretic universals
demonstrating sufficiency
```

This is too strong for:

```text
small N
synthetic Page proxy
engineered spectral density
assumption-heavy monotonicity diagnostics
```

Recommended wording:

```text
replace "universals" with "generic mechanisms" or "non-gravitational mechanisms"
replace "demonstrates sufficiency" with "provides a controlled example"
replace "core phenomenology" with "selected thermodynamic and information-flow phenomenology"
```

### Risk 2: Abstract overstates the Page calculation

Current abstract says:

```text
we calculate the entanglement entropy of emitted radiation
```

But figure generation shows the Page-like curve is synthetic/illustrative:

```text
figs/generate.py::gen_page_curve uses a hand-built smooth curve
```

The manuscript elsewhere admits:

```text
synthetic radiation record
Renyi-2 Page-like turnover lower bound
```

Recommended fix:

```text
state clearly that ED validates the thermodynamic/spectral ingredients,
while Page-like radiation dynamics is a design-rule/synthetic proxy under
the stated scrambling assumptions.
```

If the goal is a publishable numerical paper, this is the biggest gap:

```text
need an actual unitary evaporation simulation producing the Page-like curve
from the model, not just a synthetic proxy.
```

### Risk 3: N mismatch

The manuscript repeatedly says:

```text
ED at N=16
```

But `sim/README.md` and `sim/generate_data.py` default to:

```text
N=12
```

Dense diagonalization at `N=16` means dimension `65536`, which is much harder
than the README's laptop-scale `N=12` dense diagonalization.

Action:

```text
verify what generated the published figures
either regenerate/record N=16 data or change the manuscript to N=12
```

### Risk 4: Figure-generation reproducibility bug

`figs/generate.py::gen_p_of_e` appears to use `P` in the plot/residuals even
when simulation data exists, but `P` is only defined in the synthetic branch.

Current data branch:

```text
Pn = beta * (wstar * J)
```

but later:

```text
ax.plot(E, P, ...)
resid = log(Pn) - log(P)
```

Action:

```text
define P = beta / E**2 in the data branch or revise the plotting logic.
```

### Risk 5: Surface-gravity/KMS inverse mismatch

Appendix A defines:

```text
kappa_resp = d/domega log[A(omega)/A(-omega)] = 1/T_mu(E)
```

But the main text wants:

```text
T_mu(E) ~ 1/E
kappa(E) ~ 1/E
```

In black-hole thermodynamics:

```text
T_H proportional to kappa
beta proportional to 1/kappa
```

So the KMS log-ratio slope is `beta`, not `kappa`.

Action:

```text
define beta_resp from the KMS slope
then define kappa_resp proportional to 1/beta_resp = T_mu(E)
```

Otherwise the appendix implies `kappa ~ E`, contradicting the figures and
black-hole scaling analogy.

### Risk 6: Theorem language may be too strong

The monotonicity results rely on:

```text
fixed emissions
unitality
CP-divisibility
support invariance
2-design averaging
concentration assumptions
```

This is fine as a diagnostic proposition, but risky as a central theorem unless
fully proved and carefully scoped.

Specific caution:

```text
entropy is not monotone under arbitrary CPTP maps; unitality is doing the work.
R'enyi-2 monotonicity under the averaged construction needs a precise proof.
```

Recommended fix:

```text
rename as "Proposition" or "Diagnostic lemma" unless the appendix is expanded.
Emphasize that turnover witnesses breakdown of the stated sufficient
Markovian/unital model, not non-Markovianity in every possible definition.
```

### Risk 7: "Radiation-only decoding" is under-supported

The manuscript discusses Petz/variational decoders and mutual information, but
the current figures/protocols appear illustrative.

Action:

```text
either provide actual decoding numerics,
or demote to an experimental/theoretical protocol rather than a finding.
```

### Risk 8: Tone around islands/wormholes

Some sentences are too dismissive:

```text
island formula is gravity's bookkeeping, not fundamentally different physics
wormholes are not required for quantum mechanics itself
```

The second sentence is true but obvious; the first may irritate gravity readers.

Recommended framing:

```text
Our model does not address why semiclassical gravity computes entropy through
QES/island saddles. It shows only that the Page-like outcome is not diagnostic
of gravity by itself.
```

## Recommended rewrite strategy

### New title direction

Current title:

```text
A Unitary Toy Model of Black Hole Evaporation: Information Recovery without Geometry
```

Better:

```text
A Geometry-Free Quantum Evaporator with Negative Heat Capacity
```

or:

```text
Black-Hole-Like Evaporation from a Convex-Intruder Quantum System
```

or:

```text
A Negative-Heat-Capacity Quantum Evaporator as a Control Model for Black-Hole Information Flow
```

These foreground the differentiator.

### New abstract shape

Recommended abstract:

```text
Black-hole evaporation combines two features that are often studied
separately: negative heat capacity and unitary information recovery. We
construct a non-gravitational finite quantum evaporator designed to combine
both. The core is a fast-scrambling finite system with a convex
microcanonical entropy window, weakly coupled to an engineered radiation
channel. In the calibrated window the microcanonical temperature rises as
the core loses energy, and an Ohmic passband gives an evaporation law
P(E) ~ E^{-2}. Under a unitary scrambling/emission model, the radiation
entropy follows a Page-like Renyi-2 turnover once the radiation Hilbert
space competes with the remaining core, and the turnover coincides with
the breakdown of a CP-divisible unital description of the radiation.
Exact diagonalization of a small fully connected XXZ core illustrates the
convex-intruder and transition-frequency ingredients; the full evaporation
record is a design-rule/synthetic proxy to be tested in larger simulators.
The model does not contain a metric, horizon, area law, QES, islands, or
replica wormholes. Its purpose is to isolate which parts of black-hole
evaporation phenomenology follow from finite-dimensional unitary quantum
statistical mechanics and which remain genuinely gravitational.
```

This is much safer and clearer.

### Recommended contribution list

Use:

```text
1. Convex-intruder evaporator architecture.
2. Thermodynamic scaling dictionary: T(E), P(E), E(t).
3. Small-ED validation of density-of-states and edge spectral ingredients.
4. Markovian/unital monotonicity diagnostic for Page-like turnover.
5. Experimental measurement protocol.
6. Demarcation from gravitational mechanisms.
```

Avoid:

```text
universal resolution
information puzzle solved
ETH as lab equivalence principle
precisely matches black-hole thermodynamics
```

## What would make the paper substantially stronger

### Minimal must-do before submission

```text
fix N=12 vs N=16 provenance
fix figure-generation bug
fix kappa/beta KMS definition
downgrade Page/decoding claims to match actual evidence
expand/downgrade monotonicity theorem proof
add missing non-gravitational Page-curve literature
```

### Best technical upgrade

Run an actual unitary evaporation simulation:

```text
finite core Hilbert space with shrinking energy window
emission qubits/modes appended stepwise
scrambling unitary between emissions
energy-dependent emission probabilities from S(E)
compute S2_rad(t) directly
compute distinguishability/BLP proxy directly
attempt simple recovery/decoding
```

This need not use the full XXZ Hamiltonian initially. A constrained random
unitary/isometry model calibrated to the convex-intruder `S(E)` would already
make the Page-like result much less synthetic.

### Stronger but harder upgrade

Replace the engineered/synthetic convex intruder with a more physically
standard finite bosonic model:

```text
Bose-Hubbard cluster
finite droplet/cluster phase-coexistence model
long-range interacting finite system
```

This would improve physical plausibility.

## Publication path

Most plausible venues/categories:

```text
quantum simulation / quantum thermodynamics journal
PRD if black-hole analogy is carefully controlled
CQG if positioned as an analogue/control model
SciPost/Entropy style venue if framed conceptually
```

Avoid aiming at a high-energy gravity audience with strong claims about
islands/wormholes. The most receptive audience may be:

```text
quantum thermodynamics
open quantum systems
quantum simulation of black-hole analogues
```

## Current verdict

This project is worth pushing, but only after reframing.

The paper is strongest as:

```text
a control model showing that black-hole-like thermodynamic and information
flow phenomenology can coexist in a finite non-gravitational quantum system
```

It is weakest as:

```text
a claim that the black-hole information puzzle is resolved by generic
unitary quantum mechanics
```

The key editorial move is to reduce the philosophical volume and increase the
engineering precision.

## Updated go/no-go decision

The literature check sharpened the decision.

Already covered elsewhere:

```text
Page-like entanglement dynamics without gravity.
Open-system thermodynamic interpretations of Page-like entropy decrease.
Negative heat capacity in finite and gravitational systems.
```

Not obviously covered:

```text
a non-gravitational unitary evaporator in which negative microcanonical heat
capacity dynamically controls the emission schedule while the radiation entropy
is computed from emitted quantum time bins.
```

Therefore the immediate next step is not more abstract writing. It is a small
technical kill test:

```text
build a shell-resolved unitary evaporation model where D(E), beta(E), emission
rates, E(t), and S_rad(t) are all tied together.
```

Decision rule:

```text
If this works:
  continue paper_v2 around the narrow claim "geometry-free negative-C_mu
  quantum evaporator".

If this does not work:
  archive the project as useful conceptual notes, because the remaining
  claim is too close to existing Page-curve-without-gravity work.
```

## Update after Hamiltonian density-channel result

The kill test now has a positive Hamiltonian version.

See:

```text
notes/current_status_review.md
notes/hamiltonian_density_channel_results.md
```

Current best evidence:

```text
curvature 3, channels 8, g = 0.5:
  acceleration ratio: 1.138

linear control, channels 8, g = 0.5:
  acceleration ratio: 0.912
```

Interpretation:

```text
a fixed multi-mode collision Hamiltonian can exhibit a weak-coupling
accelerating window controlled by convex S(E), while still producing radiation
Renyi-2 entropy from the unitary emitted-bin dynamics.
```

This upgrades the project from:

```text
interesting but missing dynamical evidence
```

to:

```text
technically alive, pending robustness scans.
```

Next required step before manuscript writing:

```text
scan coupling, channel count, convexity, and seeds to check robustness.
```
