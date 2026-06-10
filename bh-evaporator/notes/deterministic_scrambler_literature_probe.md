# Deterministic Scrambler Literature Probe

## Question

Can we replace the abstract shell-scrambling condition with a concrete fixed
Hamiltonian `H_mix`, preferably deterministic, while relying on known
scrambling/design literature rather than proving everything from scratch?

Target property for the evaporator:

```text
For the composed fixed emission map V, the low-order moment errors epsilon_k(V)
are small on the active microcanonical support.
```

For the Page-purity and code-subspace diagnostics, the key case is `k=2`.

## What We Need From H_mix

The shell mixer does not need to be Haar-random.  It needs to make the
composed emission map behave like a low-order design for the diagnostics being
used.

For code dimension `d`, remaining core dimension `b`, and radiation support
dimension `r`, the fixed-map conditions are

```text
r >> d b,     d b epsilon_2(V) << 1
  -> radiation recovers the code,

b >> d r,     d r epsilon_2(V) << 1
  -> early radiation is uninformative.
```

So a concrete `H_mix` would be useful if literature or analysis lets us argue
that its cumulative evolution makes `epsilon_2(V)` small enough on the
evaporation time scale.

## Literature Buckets

### 1. Expander-graph horizon models

Barbon and Magan propose local quantum systems on expander graphs as simple
models of horizon thermalization.  Their claim is directly aligned with our
intuition: bounded-degree expander connectivity can give rapid mixing without
complete all-to-all coupling.

Usefulness:

```text
High conceptual fit.  Supports choosing H_mix on a deterministic expander graph
as a horizon-like non-gravitational mixer.
```

Limitation:

```text
They motivate fast scrambling and horizon thermalization, but they do not give
our fixed-map epsilon_2(V) decoupling bound.
```

Reference:

```text
J. L. F. Barbon and J. M. Magan,
"Fast Scramblers, Horizons and Expander Graphs,"
JHEP 08 (2012) 016, arXiv:1204.6435.
```

### 2. Sparse/small-world graph fast scrambling

Bentsen, Gu, and Lucas analyze scrambling on sparse graphs and show how graph
geometry controls operator growth.  Sparse random graphs and small-world
graphs can support logarithmic scrambling; ordinary finite-dimensional lattices
cannot.

Usefulness:

```text
Strong support for the graph choice.  If we pick an expander or small-world
graph, we are following a known route to fast scrambling.
```

Limitation:

```text
The central diagnostics are operator growth, Lieb-Robinson-style bounds, OTOCs,
and scrambling time.  This is close to, but not identical with, approximate
2-design behavior for the evaporation Stinespring map.
```

Reference:

```text
G. Bentsen, Y. Gu, and A. Lucas,
"Fast scrambling on sparse graphs,"
PNAS 116, 6689 (2019), arXiv:1805.08215.
```

### 3. Deterministic treelike interactions

Bentsen, Hashizume, Buyskikh, Davis, Daley, Gubser, and Schleier-Smith propose
non-random couplings in which sites interact at distances that are powers of
two.  The effective geometry interpolates between a line and an ultrametric
tree.  In the treelike regime, they find exponentially fast spreading of
quantum information and enhanced entanglement growth.

Usefulness:

```text
This is the cleanest deterministic, physically motivated fast-scrambling
candidate.  It gives an explicit coupling pattern rather than a random graph.
```

Limitation:

```text
It is a spin model with nonlocal deterministic couplings, not a proof of
low-order unitary design behavior.  It is still a candidate mechanism, not a
closed derivation of epsilon_2(V).
```

Reference:

```text
G. Bentsen et al.,
"Treelike interactions and fast scrambling with cold atoms,"
Phys. Rev. Lett. 123, 130601 (2019), arXiv:1905.11430.
```

### 4. Minimal global-interaction model

Belyansky, Bienias, Kharkov, Gorshkov, and Swingle argue that a simple global,
spatially homogeneous interaction together with local chaotic dynamics is
sufficient for logarithmic fast scrambling.  Their evidence includes tractable
models and numerical OTOC/entanglement diagnostics.

Usefulness:

```text
Very compact H_mix candidate:
local chaotic dynamics + one global homogeneous coupling.
```

Limitation:

```text
The most analytic model uses random circuit ingredients, and the Hamiltonian
evidence is based on OTOCs and entanglement growth rather than a direct
decoupling/design theorem.
```

Reference:

```text
R. Belyansky et al.,
"Minimal Model for Fast Scrambling,"
Phys. Rev. Lett. 125, 130601 (2020), arXiv:2005.05362.
```

### 5. Random local circuit design results

Brandao, Harrow, and Horodecki prove that local random quantum circuits form
approximate unitary designs after polynomially many gates.  This is the right
kind of mathematics for `epsilon_k`, but it is a random circuit result rather
than a deterministic time-independent Hamiltonian result.

Usefulness:

```text
Gives the clean design/decoupling benchmark.  Helps specify what H_mix must
imitate.
```

Limitation:

```text
Does not itself supply the deterministic time-independent H_mix we want.
```

Reference:

```text
F. G. S. L. Brandao, A. W. Harrow, and M. Horodecki,
"Local random quantum circuits are approximate polynomial-designs,"
Commun. Math. Phys. 346, 397 (2016), arXiv:1208.0692.
```

### 6. Hamiltonian design no-go / cautionary literature

Recent work on random unitaries from Hamiltonian dynamics emphasizes an
important obstruction: a single time-independent, constant-local Hamiltonian
does not generally generate a full unitary design in the strongest global
sense.  Related newer works use multiple Hamiltonians, quenches, random times,
or random operations to obtain full design behavior.

Usefulness:

```text
Explains why the exact off-the-shelf result is rare.  Full unitary-design
behavior from one fixed local Hamiltonian is too strong.
```

Limitation for us:

```text
Our requirement is weaker.  We need low-order moment behavior for selected
evaporation diagnostics on an active support, not a full global unitary design
over the entire Hilbert space.
```

Representative recent references:

```text
"Random unitaries from Hamiltonian dynamics," arXiv:2510.08434.

"Three Hamiltonians are Sufficient for Unitary k-Design in Temporal Ensemble,"
arXiv:2604.04205.
```

## Candidate H_mix Choices

### Candidate A: deterministic expander spin Hamiltonian

```text
H_mix(E) =
  sum_{(ij) in G_E} [
    J_x X_i X_j + J_y Y_i Y_j + J_z Z_i Z_j
  ]
  + sum_i (h_x X_i + h_z Z_i),
```

where `G_E` is a deterministic bounded-degree expander graph on the active
area/core degrees of freedom.

Pros:

```text
fixed Hamiltonian;
bounded degree;
nonrandom graph possible;
closest to expander-horizon literature;
plausibly fast operator spreading.
```

Cons:

```text
known literature supports fast scrambling, not directly epsilon_2(V);
graph geometry is chosen as an input;
proving design-like behavior is hard.
```

Assessment:

```text
Best fit for a time-independent Hamiltonian route.
```

### Candidate B: deterministic treelike / power-of-two coupling Hamiltonian

```text
H_mix =
  sum_i sum_{m=0}^{log N}
    J_m O_i O_{i+2^m}
  + local noncommuting fields.
```

Pros:

```text
explicit deterministic coupling pattern;
directly backed by treelike fast-scrambling literature;
physically motivated by cold-atom/cavity implementations.
```

Cons:

```text
less horizon-cell/area-channel-like than an expander graph;
still gives scrambling diagnostics, not a design theorem.
```

Assessment:

```text
Best concrete deterministic pattern if we want to avoid random graph language.
```

### Candidate C: local chaotic chain plus global homogeneous coupling

```text
H_mix =
  H_local chaotic
  + (J/N) sum_{ij} O_i O_j.
```

Pros:

```text
compact;
directly motivated by minimal fast-scrambling work;
easy to describe.
```

Cons:

```text
all-to-all/global term may look inserted;
less naturally tied to area-channel picture;
literature evidence is not a design theorem.
```

Assessment:

```text
Good backup if expander/treelike constructions are too cumbersome.
```

### Candidate D: SYK or sparse SYK shell mixer

Pros:

```text
strongest standard black-hole-adjacent scrambler;
well-studied chaos.
```

Cons:

```text
random couplings;
large black-hole-model baggage;
does not help remove randomness from the model.
```

Assessment:

```text
Useful comparison/control, not the best route for the deterministic goal.
```

## How Hard Is This?

There are three levels.

### Level 1: choose a literature-backed H_mix candidate

Difficulty:

```text
low.
```

We can choose deterministic expander or treelike spin dynamics and explain why
it is the most natural candidate mechanism for the low-order moment condition.

What it buys:

```text
replaces "some scrambler" by an explicit candidate class.
```

What it does not buy:

```text
does not prove epsilon_2(V) is small.
```

### Level 2: give an analytic plausibility chain

Use literature to argue:

```text
expander / treelike graph
  -> logarithmic operator spreading / fast scrambling
  -> local information becomes delocalized before enough radiation escapes
  -> low-order decoupling condition is plausible.
```

Difficulty:

```text
medium.
```

This is probably reachable without new numerics.  It is not a proof, but it is
an informed reduction to known scrambling results.

What it buys:

```text
turns the scrambling assumption into a concrete dynamical route.
```

### Level 3: prove epsilon_2(V) for the chosen H_mix

Difficulty:

```text
high.
```

This would require a real result connecting Hamiltonian fast scrambling on the
chosen graph to approximate 2-design or decoupling behavior for the composed
evaporation map.  Existing literature does not appear to give this exact
bridge off the shelf.

What it buys:

```text
would substantially strengthen the paper beyond Result 2.
```

## Recommendation

Use the deterministic expander or treelike Hamiltonian as the leading route,
but do not make Result 2 depend on proving it.

Best next model statement:

```text
The ideal Hamiltonian result requires a small fixed-map moment error
epsilon_k(V).  A deterministic nonintegrable Hamiltonian on an expander or
treelike interaction graph is a natural candidate mechanism for producing this
condition, supported by the fast-scrambling literature.  Proving the
epsilon_k(V) bound for that Hamiltonian is a separate dynamical problem.
```

If we push further analytically, start with Candidate A or B and try to prove a
weaker statement:

```text
operator support reaches O(N) degrees of freedom in O(log N) shell time,
and no obvious conserved quantity prevents decoupling.
```

That would not close the gap completely, but it would tell us whether the
deterministic scrambler direction is worth deeper investment.

## Requirement-Matching Update

The search above suggests that `epsilon_2(V)` is a useful sufficient condition,
but it may be too strong as the primary target.  The literature we want to use
usually does not prove that a fixed many-body Hamiltonian forms a unitary
2-design.  It more often proves or diagnoses scrambling through operator
growth, OTOC decay, channel mutual information, or Hayden-Preskill recovery.

So the sharper target should be stated in layers.

### Layer A: the actual information-flow target

For the evaporation result, the direct object is not a global design norm.  It
is decoupling of the reference from the wrong subsystem:

```text
early time:
  I(Q:R) small, or ||rho_QR - rho_Q tensor rho_R||_1 small;

late time:
  I(Q:B) small, or ||rho_QB - rho_Q tensor rho_B||_1 small.
```

Here `Q` purifies the code subspace, `B` is the remaining core, and `R` is the
emitted radiation.  This is the standard Hayden-Preskill/decoupling language.
The Page and code-subspace statements only need enough scrambling to make these
two mutual-information or trace-distance statements true for the chosen code
subspace.

This is weaker than requiring the whole active-shell unitary to be an
approximate 2-design.

### Layer B: a standard sufficient condition

Approximate 2-design behavior on the active shell remains a clean sufficient
condition:

```text
epsilon_2(V) small
  -> Page-purity estimates and code-subspace decoupling bounds.
```

This is mathematically convenient and matches the decoupling/design literature.
It should be presented as a sufficient condition, not as the only possible
mechanism.

### Layer C: the literature-backed dynamical route

The fast-scrambling Hamiltonian literature mostly gives:

```text
operator growth / OTOC decay / channel scrambling
  -> information delocalization.
```

This is closer to the result of Hosur-Qi-Roberts-Yoshida: treating a unitary
channel as a state, generic OTOC decay implies that input subsystems have
nearly vanishing mutual information with most output partitions.  Yoshida and
Kitaev then connect OTOC decay to faithful Hayden-Preskill recovery.

Thus the route should be:

```text
expander or treelike H_mix
  -> logarithmic operator growth / OTOC decay
  -> channel mutual-information decoupling
  -> Hayden-Preskill-style recovery and Page-level information flow.
```

This route uses what the literature actually proves.  It avoids demanding an
off-the-shelf deterministic Hamiltonian 2-design theorem.

## Practical Tweak to the Paper Target

The paper should not make the concrete deterministic `H_mix` section hinge on
proving

```text
epsilon_2(V) << 1.
```

Instead, it should phrase the fine-grained scrambling requirement as:

```text
The composed emission channel must decouple the reference from the subsystem
that is supposed to be ignorant of the code.
```

Then it can say:

```text
Approximate 2-design behavior is one sufficient condition.  Fast-scrambling
Hamiltonians on expander or treelike graphs are a plausible deterministic route
because their standard diagnostics are operator growth and OTOC decay, and
these diagnostics are known to imply information-theoretic channel scrambling
in the Hayden-Preskill setting.
```

This is a real improvement over the previous target.  It narrows the hard
unproved part from

```text
prove a fixed Hamiltonian is a low-order design
```

to

```text
show the composed evaporation channel satisfies the decoupling condition needed
for the code subspace.
```

The latter is still hard for a specific deterministic Hamiltonian, but it is
the standard quantity in the field.

## Consequences for Candidate H_mix

### Expander graph

The expander route improves under the weaker target.  Barbon-Magan already
connect expander locality to horizon thermalization and fast scrambling, while
Bentsen-Gu-Lucas analyze how graph connectivity controls operator growth and
OTOC spreading.  That evidence speaks directly to Layer C.

What remains open:

```text
turn the operator-growth/OTOC statement for the chosen expander Hamiltonian
into a quantitative decoupling bound for the evaporation code subspace.
```

### Treelike deterministic couplings

The treelike route also improves.  The Bentsen et al. cold-atom model gives a
specific non-random coupling pattern and reports exponentially fast spreading
of quantum information.  This is closer to a concrete Hamiltonian than a random
graph ensemble.

What remains open:

```text
prove or numerically establish the reference/core and reference/radiation
mutual-information bounds along the evaporation channel.
```

### Random circuits

Random circuits remain the strongest theorem source.  Brown-Fawzi is especially
important because it proves decoupling directly, rather than only proving
ordinary 2-design behavior.  This supports our decision to state decoupling as
the primary condition.

What remains open:

```text
replace the random-circuit proof source by a deterministic Hamiltonian source,
or keep the deterministic Hamiltonian as a motivated candidate rather than a
closed theorem.
```

## Updated Hard-Part Assessment

The hardest part is not "find a Hamiltonian with OTOC decay."  Several
reasonable candidates exist.  The hardest part is the bridge:

```text
specific time-independent H_mix
  -> quantitative decoupling of the evaporation code subspace.
```

This bridge is narrower than the original `epsilon_2(V)` demand and is closer
to known Hayden-Preskill/channel-scrambling results.  It is still a real
research step.

The most useful next analytical move is therefore:

```text
Rewrite the scrambling assumption in the main draft as a decoupling condition,
with approximate 2-design behavior listed as one sufficient condition and
OTOC/operator-growth scrambling listed as the literature-backed Hamiltonian
route.
```

That lets us use known results honestly, and it makes clear exactly where a
future deterministic-Hamiltonian proof would have to land.
