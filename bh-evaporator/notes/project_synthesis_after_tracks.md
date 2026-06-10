# Project Synthesis After Tracks A and B

## Current situation

The project no longer looks like a single engineered-shell paper.

It now has several related models:

```text
0. Engineered shell evaporator
1. Track A: variable-N Bose-Hubbard evaporator
2. Track B: area-register evaporator
3. Track C: Fibonacci fusion-register pilot
4. Track E: variable-length spin-chain pilot
```

They answer different objections.

The useful synthesis is not:

```text
we found the one true non-gravitational black-hole model
```

but rather:

```text
black-hole-like evaporation decomposes into separable ingredients:

1. entropy law;
2. shrinking Hilbert-space sectors;
3. compatible energy-lowering emission matrix elements;
4. unitary or purifiable radiation channel.
```

Gravity supplies these ingredients in a black hole. The toy models show that
the phenomenology itself is not uniquely gravitational.

The current best candidate for a technical result is the outgoing
phase-space acceleration criterion:

```text
notes/phase_space_acceleration_criterion.md
notes/phase_space_criterion_stress_test.md
notes/sector_phase_space_profile_results.md
notes/fusion_register_pilot_results.md
notes/acceleration_criterion_formal_note.md
notes/variable_length_spin_chain_pilot_results.md
notes/variable_length_spin_chain_robustness_results.md
```

## Main conceptual claim

The strongest defensible claim is:

```text
Negative heat capacity, accelerating evaporation, shrinking internal Hilbert
space, and core-radiation entropy growth can be reproduced in finite quantum
systems without spacetime geometry.
```

The sharper version is:

```text
The black-hole evaporation backbone does not follow from a Page curve alone.
It requires a relation between energy, entropy, shrinking state space, and
emission matrix elements.
```

This is the real result. It separates the lore of black-hole evaporation from
the genuinely gravitational questions:

```text
Why S = A/4G?
Why does a horizon supply the relevant degrees of freedom?
Why do QES/islands/wormholes compute the fine-grained entropy?
How does spacetime encode the unitary radiation map?
```

## Model 0: engineered shell evaporator

Role:

```text
control model / mechanism isolator
```

What it does:

```text
sets a finite density of states S(E)
chooses a convex / negative-heat-capacity profile
builds a collision channel between shrinking shells
shows accelerating emission under suitable multi-channel dynamics
computes core-radiation Renyi-2 entropy
```

Strength:

```text
cleanest way to isolate the mechanism
```

Weakness:

```text
density of states and shell structure are imposed
```

Paper role:

```text
introductory control / benchmark
```

It should not be sold as the final natural core.

## Track A: variable-N Bose-Hubbard

Role:

```text
natural dynamics proof of principle
```

Core:

```text
finite attractive Bose-Hubbard ring
H_core = direct sum over particle-number sectors
emission operator b_i : H_N -> H_{N-1}
```

Key result:

```text
fixed-N relaxation mostly decelerates;
variable-N particle loss accelerates.
```

Reduced-density Kraus result:

```text
mu = 6
max emitted gap = 4
initial N=8 window = [-18.5, -17]

seed 2468:
  mid / early emitted power = 1.364
  peak S2(core) = 3.956

seed 2469:
  mid / early emitted power = 1.340
  peak S2(core) = 3.848
```

Robustness:

```text
targeted Kraus scan:
18 grouped settings
7/18 accelerate in both seeds
6/18 have acceleration > 1.05 in both seeds
5/18 have acceleration > 1.15 in both seeds
```

What Track A shows:

```text
shrinking sectors are dynamically important;
natural many-body particle-loss operators can produce accelerating emission;
core-radiation entropy growth survives a reduced-density Kraus upgrade.
```

What Track A does not show:

```text
S ~ area
S ~ M^2
T ~ 1/M from the natural Hilbert-space count
Page turnover
early/late radiation mutual information
```

Reason:

```text
fixed-site Bose-Hubbard sectors have
dim H_N = binomial(N + L - 1, N)
so S_N ~ (L - 1) log N at large N,
not S ~ M^2.
```

Paper role:

```text
supporting model showing that the shrinking-sector mechanism is not purely
an engineered-shell artifact.
```

## Track B: area-register evaporator

Role:

```text
entropy-correct abstract quantum register
```

Core:

```text
H_n = n qubits
dim H_n = 2^n
S_n = n log 2
M_n = alpha sqrt(n)
```

This gives:

```text
S ~ n ~ M^2
T ~ dM/dS ~ 1/M
C < 0
```

Emission:

```text
X_n : H_n -> H_{n-1}
```

using local removal or scrambled removal.

Rate diagnostic:

```text
Gamma ~ |<f,n-1|X_n|i,n>|^2 J(omega)
```

Control:

```text
linear mass law M_n ~ n
```

Track B rate result:

```text
sqrt mass, gap >= 4:
  acceleration about 1.125

linear mass, open transitions:
  acceleration about 0.60 to 0.91
```

Track B Kraus result:

```text
n = 4,...,10
M_n = 8 sqrt(n)
gap = 4

local removal:
  seed 2468: mid / early = 1.123
  seed 2469: mid / early = 1.124

scrambled removal:
  seed 2468: mid / early = 1.124
  seed 2469: mid / early = 1.124

peak S2(core) = about 5.34
dimension entropy: 6.93 -> about 4.21-4.26
effective dimension: 1024 -> about 140-146
```

What Track B shows:

```text
the BH entropy/mass scaling can be built into a finite register;
matrix-element-derived shrinkage rates can produce modest acceleration;
the linear mass-law control decelerates;
the result survives a reduced-density Kraus upgrade.
```

What Track B does not show:

```text
natural microscopic Hamiltonian
derived horizon degrees of freedom
strong dependence on local vs scrambled removal
Page turnover
early/late radiation mutual information
```

Paper role:

```text
entropy-correct complement to Track A.
```

## Comparison table

```text
Model                 Natural dynamics   BH entropy law   Acceleration   S2 growth
----------------------------------------------------------------------------------
Engineered shell      no                 imposed          yes            yes
Variable-N BHubbard   yes-ish            no               yes            yes
Area register         abstract           yes              yes, modest    yes
```

More detailed:

```text
Engineered shell:
  best control; weakest naturalness.

Variable-N Bose-Hubbard:
  best concrete many-body dynamics; wrong entropy scaling.

Area register:
  best entropy scaling; abstract microscopic origin.
```

Mechanism comparison:

```text
Model                 How <W> increases
---------------------------------------------------------------
Engineered shell      imposed convex shell/channel profile
Variable-N BHubbard   transition-induced selection of high-W states
Area register         coarse sector profile from M ~ sqrt(area)
```

## Where we are vs where we want to be

```text
Requirement                         Current status                         Target
--------------------------------------------------------------------------------------------------
Negative heat capacity              yes, in shell and area register         keep as core diagnostic
Accelerating emission               yes, strongest in shell/Track A         show robust but not universal
Shrinking internal state space       yes, Track A and Track B               make this central
S ~ M^2 entropy scaling              yes in Track B only                    connect to dynamics cleanly
Natural microscopic dynamics         best in Track A                        improve or clearly bracket
Concrete Hamiltonian / channel       yes, reduced Kraus channels            add tiny full-radiation test
Core-radiation entropy growth        yes                                    keep, but avoid Page overclaim
Early/late radiation structure       tiny test inconclusive                 needs compressed/trajectory test
Page turnover                        not yet                                optional, later
Derived horizon degrees of freedom   no                                     outside current claim
Gravity/islands/wormholes            no                                     explicitly separated
```

Short version:

```text
We have the thermodynamic backbone.
We do not yet have a positive radiation-structure backbone.
```

## What we should not claim

Do not claim:

```text
1. This solves the black-hole information problem.
2. This models a real horizon.
3. This derives S = A/4G.
4. This reproduces islands or replica wormholes.
5. This proves Page curves are generic in all evaporators.
6. This gives a full Page turnover or early/late radiation mutual information.
```

Also avoid:

```text
black-hole core
literal Hawking mechanism
realistic microscopic black hole
```

Use instead:

```text
geometry-free evaporator
finite quantum evaporator
shrinking Hilbert-space model
area-register model
control model
```

## What we can claim

A defensible abstract-level claim:

```text
We construct finite, geometry-free evaporators that reproduce the thermodynamic
backbone of black-hole evaporation: negative heat capacity, shrinking state
space, accelerating emission, and core-radiation entropy growth.
```

A more precise claim:

```text
The simulations show that no single ingredient is sufficient. Fixed-sector
relaxation can fail even with a convex density of states. Shrinking sectors
plus compatible emission operators can produce acceleration. Correct
black-hole entropy scaling can be represented by an area register, but the
emission matrix elements and passband still matter.
```

This is probably the central message:

```text
black-hole-like evaporation is a conjunction of entropy law, shrinking Hilbert
space, and emission coupling, not a consequence of information-theoretic
unitarity alone.
```

The sharper mechanistic statement is:

```text
In the secular models, emitted power is the state average of

  W_i = sum_f Gamma_{f i} omega_{f i}.

Acceleration occurs when the shrinking trajectory moves the state into regions
with larger outgoing weighted phase space W_i.
```

Follow-up diagnostics refine this:

```text
Track B area register:
  acceleration is mostly sector-profile acceleration.
  The coarse sector average bar W_n predicts the trajectory well.

Track A variable-N Bose-Hubbard:
  acceleration is mostly selection-driven acceleration.
  Uniform lower-N sectors do not have larger W, but particle-loss dynamics
  selects high-W subregions inside those sectors.

Track C Fibonacci fusion register:
  the minimal fusion-path pilot behaves like another sector-profile area
  register. Fusion-prefix removal and scrambled removal are nearly
  indistinguishable, so fusion constraints do not yet add dynamical content.

Track E variable-length spin chain:
  the spin-chain pilot keeps the area-law state count while replacing random
  blocks with concrete local Hamiltonian blocks. Boundary/bulk removal
  accelerate more strongly than scrambled removal, suggesting the local
  Hamiltonian/removal structure changes the W profile.

  Robustness scan:
    sqrt mass + boundary/bulk removal accelerates in all tested seeds and
    bandwidths;
    linear mass controls decelerate in all tested seeds and bandwidths;
    boundary/bulk removal beat scrambled removal in every matched sqrt-mass
    case.
```

So the common diagnostic is `W`, but the mechanism that makes `<W>` increase
differs across models.

## Paper restructuring

The old `paper_v2` title and abstract are now too narrow.

Current title:

```text
A Geometry-Free Quantum Evaporator with Negative Heat Capacity and Page-Like
Information Flow
```

Possible revised title:

```text
Geometry-Free Quantum Evaporators with Shrinking Hilbert Space
```

or:

```text
Shrinking Hilbert Spaces and Black-Hole-Like Evaporation Without Gravity
```

Suggested paper structure:

```text
1. Introduction
   Page curves are not enough; BH evaporation has a thermodynamic backbone.

2. Mechanism
   Entropy law, shrinking Hilbert space, emission matrix elements.

3. Engineered shell control
   Clean minimal evaporator.

4. Variable-N Bose-Hubbard evaporator
   Natural shrinking dynamics; fixed-N failure; variable-N success.

5. Area-register evaporator
   Correct S~M^2 scaling; matrix-element-derived rates; controls.

6. Information diagnostics
   Core-radiation S2 growth; what is and is not Page-like.

7. Comparison with black holes
   What phenomenology is reproduced; what remains gravitational.

8. Limitations and next steps
   early/late radiation, MPS/full tracking, anyonic fusion register.
```

## Next technical steps

Most useful next steps, in order:

```text
1. Create one comparison figure/table across the three models.

2. Replace naive exact full-history tracking with a cheaper radiation
   diagnostic:

   a. trajectory sampling of emitted energy/time records; or
   b. compressed exact radiation labels.

3. Explore replacing the area-register qubits with anyonic/fusion dimensions
   dim H_n ~ d^n.

4. Broaden finite-size robustness only if the paper becomes centered on one
   model rather than the decomposition.
```

Completed radiation-tracking note:

```text
notes/track_b_full_radiation_tiny_results.md
notes/spin_chain_trajectory_radiation_results.md
```

Planning note:

```text
notes/next_diagnostic_radiation_tracking.md
```

Latest radiation-structure status:

```text
Track E trajectory sampler:
  preserves thermodynamic acceleration/deceleration;
  shows nonzero classical early/late radiation-record correlations;
  does not prove quantum Page/early-late entanglement.

Naive compressed exact radiation:
  computationally feasible at small n;
  not dynamically faithful, because coarse energy-bin labels merge Kraus
  branches coherently and change the reduced core dynamics.

Track E exact-label Stinespring:
  faithful by construction and validated numerically at n=4,...,5;
  tracing radiation reproduces the reduced core channel to ~1e-15 errors;
  branch growth is severe, so this gives F2 but not scalable F8/F9.

Option C1 detached-qubit radiation:
  explicit emitted radiation qubit chain;
  gives Page-like S2(core) and nonzero early/late radiation mutual information;
  sqrt power accelerates while linear power is flat;
  but radiation entropy structure is identical across mass laws, so the
  information result is kinematic rather than thermodynamic.

Option C2 energy-filtered detached-qubit radiation:
  first naive implementation gives probabilistic emission and explicit
  radiation bins;
  early/late structure is nonzero;
  but power decelerates for both sqrt and linear mass laws, so it does not yet
  recover Track E thermodynamics.
```

Do not keep adding broad scans until the paper framing is updated.

## Current recommendation

Rewrite the manuscript around the decomposition.

The strongest paper is not:

```text
here is one perfect toy black hole
```

It is:

```text
here is a controlled decomposition of black-hole-like evaporation into
finite-system ingredients, with explicit models showing which ingredients
matter and which are insufficient alone.
```

That framing makes the limitations part of the result rather than a weakness.
