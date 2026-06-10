# Removing The Entropy Input: Review

## Question

Can we remove the remaining imposed input

```text
S_micro(M) ~ M^2
```

and still get a non-gravitational autonomous quantum evaporator?

## Short Answer

Not with anything we currently have.

The literature and our probes give three partial routes:

```text
1. natural negative heat capacity;
2. natural shrinking dynamics;
3. natural area-like state counting.
```

No current route gives all three plus autonomous radiation and information-flow
diagnostics.

## What The Literature Gives

### Long-range and nonadditive systems

Long-range systems are known to have ensemble inequivalence, convex entropy
regions, temperature jumps, and negative microcanonical heat capacity.

Relevant source:

```text
Campa, Dauxois, and Ruffo,
"Statistical mechanics and dynamics of solvable models with long-range
interactions", arXiv:0907.0323 / Physics Reports 480 (2009).
```

Useful for us:

```text
negative heat capacity can be non-gravitational;
microcanonical convexity is a standard phenomenon in nonadditive systems.
```

Weak for us:

```text
generic long-range systems do not naturally give S ~ M^2;
our simple long-range spin exact-diagonalization scan did not find a robust
convex window.
```

Local result:

```text
notes/step3_natural_core_probe_results.md
```

### Long-range quantum spins

Kastner studies long-range quantum spin systems in optical-lattice language and
finds microcanonical/canonical nonequivalence for a Curie-Weiss-type quantum
Heisenberg model.

Useful for us:

```text
the phenomenon is not restricted to classical gravitational systems.
```

Weak for us:

```text
ensemble inequivalence is not the same as a black-hole-like density of states;
our cheap spin route did not produce the needed robust evaporator core.
```

### Atomic clusters

Finite atomic clusters have experimental negative heat capacity near melting or
phase coexistence.

Relevant source:

```text
Schmidt et al.,
"Negative Heat Capacity for a Cluster of 147 Sodium Atoms",
Phys. Rev. Lett. 86, 1191 (2001).
```

Useful for us:

```text
small non-gravitational systems can really have negative microcanonical heat
capacity;
evaporation and finite-droplet thermodynamics are physically natural there.
```

Weak for us:

```text
cluster entropy is not naturally S ~ M^2;
the natural implementation is molecular/semiclassical, not a compact quantum
Hilbert-space evaporator with Page diagnostics.
```

### Matrix models

Matrix models have the most black-hole-like natural mechanism:

```text
matrix eigenvalue clump;
flat directions;
one eigenvalue escapes;
remaining clump heats;
off-diagonal modes decouple.
```

Relevant source:

```text
"Chaos in Matrix Models and Black Hole Evaporation", arXiv:1602.01473.
```

Useful for us:

```text
geometry/separation can emerge from matrices;
evaporation is not imposed as site removal;
negative heat capacity is tied to clump dynamics.
```

Weak for us:

```text
this is already black-hole/holography-adjacent;
the clean mechanism may rely on BFSS/D0-brane structure;
we do not yet have a small quantum finite-Hilbert-space implementation.
```

Local branch:

```text
notes/stripped_matrix_clump_program.md
```

## What Our Own Models Give

### Variable-N Bose-Hubbard

Local result:

```text
notes/variable_n_bose_hubbard_results.md
```

What it gives:

```text
natural shrinking sectors;
physical particle-loss operators;
robust accelerating emission in some windows;
Kraus upgrade with growing core-radiation Renyi-2 entropy.
```

What it lacks:

```text
black-hole entropy scaling.
```

The sector dimensions are Bose-Hubbard combinatorics:

```text
dim H_N = binomial(N + L - 1, N),
```

not area-like entropy.

Verdict:

```text
best natural-dynamics model;
wrong entropy law.
```

### Area register

Local result:

```text
notes/track_b_area_register_results.md
```

What it gives:

```text
correct S ~ M^2 by construction;
negative heat capacity;
matrix-element-derived acceleration;
Kraus upgrade with shrinking effective core dimension and growing S2.
```

What it lacks:

```text
natural derivation of the sector density of states.
```

Verdict:

```text
best entropy-correct model;
still imposes the entropy law.
```

### Connector-mode skeleton

Local result:

```text
notes/connector_mode_skeleton_results.md
```

This is the most interesting route for reducing the imposed entropy law.

Counting:

```text
N sites;
one connector mode per pair;
number of connectors ~ N^2;
M ~ N;
therefore S ~ N^2 ~ M^2.
```

What it gives:

```text
area-like entropy from pairwise degrees of freedom;
T ~ 1/M;
negative heat capacity at counting level;
clear heating condition.
```

What it lacks:

```text
an autonomous Hamiltonian;
emission matrix elements;
hard radiation spectrum;
Page diagnostics.
```

Verdict:

```text
best candidate for softening the entropy-input objection.
```

It does not magically remove engineering, because choosing pairwise connector
degrees is itself a model choice. But it is less direct than assigning
`dim B_n = exp(alpha M_n^2)`.

## Current Ranking

```text
1. Area-sector DOS Hamiltonian:
   fastest route to the holy-grail standard except for deriving S ~ M^2.

2. Connector-mode Hamiltonian:
   best route to reducing the S ~ M^2 input, but currently only counting-level.

3. Variable-N Bose-Hubbard:
   best natural evaporating dynamics, wrong entropy law.

4. Matrix clump:
   most natural evaporation/separation mechanism, but hard and
   black-hole/holography-adjacent.

5. Long-range spins / atomic clusters:
   support negative heat capacity, not enough for the full model.
```

## What This Means For The "NO"

The `NO` is not gone.

The best immediate paper-level target remains:

```text
Input S(M) ~ M^2.
Measure everything else from one simple autonomous Hamiltonian.
```

The best longer route to reduce the `NO` is:

```text
build the connector-mode Hamiltonian.
```

That would try to replace:

```text
dim B_n = exp(alpha M_n^2)
```

with:

```text
ordinary pairwise connector degrees among N active sites.
```

If that works dynamically, it would move the entropy law from direct input to
model architecture.

## Recommended Next Decision

There are two serious directions:

```text
A. Finish the area-sector DOS Hamiltonian.
   This tests whether S(M) alone generates the rest of the evaporation package.

B. Build the connector-mode Hamiltonian.
   This attacks the entropy-input objection directly, but the risk is higher.
```

Given the original goal, the best sequence is:

```text
1. finish A enough to know the separation result;
2. then use B as the route toward reducing the remaining imposed input.
```

Trying B first may be more satisfying, but it risks losing the clearer result
we are now close to formulating.
