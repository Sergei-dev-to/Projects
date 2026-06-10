# Result 2 Analytical Push: Replica Structure, Spectrum Origin, and Mixing

## Purpose

This note records the current analytical push on Result 2.  The target is a
non-gravitational Hamiltonian class that reproduces the exterior black-hole
evaporation package once the Schwarzschild density of states and the needed
mixing condition are supplied.  The present pass asks whether three pieces can
be strengthened without new numerics:

1. the replica/island correspondence;
2. the origin of the boundary-accessible entropy law;
3. the replacement of abstract shell mixing by a more concrete Hamiltonian
condition.

## 1. Replica/Island Correspondence

### What The Flat Page Calculation Misses

The paper currently uses an effective radiation dimension

```tex
r=\exp\Delta S_{\rm rad}(E)
```

and applies the standard Haar/Page moment

```tex
\mathbb E\,{\rm Tr}\rho_R^n
=
{1\over (br)_n}
\sum_{\sigma\in S_n} b^{C(\sigma)}r^{C(\tau\sigma)} .
```

This is the right warmup, but the Hamiltonian does not produce a flat ensemble
of radiation histories.  A radiation history carries emitted energies,
channels, and time bins, and the weak-coupling calculation assigns it a
probability

```tex
p_\alpha=\prod_{\rm steps}p({\rm step}\mid{\rm previous\ shell}).
```

The weights are fixed by the same density-of-states ratio and boundary
operator count that give Hawking thermality and the Schwarzschild rate law.
The island comparison should therefore use the weighted history distribution,
not only the flat support size.

### Weighted Replica Moment

Let `B` be the remaining core with dimension

```tex
b=\dim{\cal H}_B(E)=\exp S_{\rm micro}(E),
```

and let radiation histories be labelled by `alpha` with probabilities
`p_alpha`.  A large-dimension random purification model is

```tex
|\psi\rangle=\sum_{a,\alpha}X_{a\alpha}|a\rangle_B|\alpha\rangle_R,
\qquad
\mathbb E\,X_{a\alpha}X^*_{b\beta}
={\delta_{ab}\delta_{\alpha\beta}p_\alpha\over b}.
```

The Gaussian/Wishart contraction expansion gives

```tex
\mathbb E\,{\rm Tr}\rho_R^n
\simeq
\sum_{\sigma\in S_n}
b^{C(\sigma)-n}
\prod_{c\in{\rm cycles}(\tau\sigma)}
{\rm Tr}\,p^{|c|}.
```

This reduces to the usual Page formula when `p_alpha=1/r`, since then

```tex
\prod_c{\rm Tr}\,p^{|c|}
=r^{C(\tau\sigma)-n}.
```

The two leading branches are:

```tex
\sigma=1:
\qquad
\mathbb E\,{\rm Tr}\rho_R^n\simeq{\rm Tr}\,p^n,
```

and

```tex
\sigma=\tau^{-1}:
\qquad
\mathbb E\,{\rm Tr}\rho_R^n\simeq b^{1-n}.
```

Thus the no-island branch is the emitted radiation Renyi entropy,

```tex
S_n^{\rm rad}
={1\over 1-n}\log{\rm Tr}\,p^n,
```

while the island branch is the remaining core entropy,

```tex
\log b=S_{\rm micro}(E).
```

At second Renyi order,

```tex
\mathbb E\,{\rm Tr}\rho_R^2
\simeq
{\rm Tr}\,p^2+e^{-S_{\rm micro}(E)}.
```

This is a stronger statement than the flat-support formula.  It says the
island/no-island contraction exchange survives the Hawking branching weights.
The radiation branch is the entropy of the actual emitted ensemble, while the
post-Page branch is still the remaining core state count.

### Code-Subspace Information Flow

For information transfer, choose a code subspace

```tex
{\cal C}\subset{\cal H}_{E_0},\qquad d=\dim{\cal C},
```

and purify it by a reference `Q`.  In the uniform-support case, a Haar-random
isometry

```tex
V:{\cal C}_d\to B_b\otimes R_r
```

gives the standard decoupling thresholds

```tex
b\gg dr
\quad\Rightarrow\quad
Q \ {\rm decouples\ from}\ R,
```

and

```tex
r\gg db
\quad\Rightarrow\quad
Q \ {\rm decouples\ from}\ B.
```

Equivalently, early radiation is uninformative about the code before the Page
transition, and late enough radiation can recover the code after the remaining
core is the smaller factor.

For Hawking-weighted histories, the recovery side has a second-Renyi
form:

```tex
\left\|\rho_{QB}-{I_Q\over d}\otimes {I_B\over b}\right\|_1
\lesssim
\exp\left[{ \log d+\log b-S_2^{\rm rad}\over 2}\right],
```

with

```tex
S_2^{\rm rad}=-\log{\rm Tr}\,p^2.
```

The early-radiation side should be stated on a typical radiation set.  If the
typical set has size `exp(H(p)+o(S))`, then

```tex
\left\|\rho_{QR}-{I_Q\over d}\otimes p_R\right\|_1
\lesssim
\exp\left[{ \log d+H(p)-\log b+o(S)\over 2}\right].
```

Thus, on the entropy scale,

```tex
H(p)\ll S_{\rm micro}(E)-\log d
\quad\Rightarrow\quad
{\rm early\ radiation\ carries\ negligible\ code\ information},
```

and

```tex
S_2^{\rm rad}\gg S_{\rm micro}(E)+\log d
\quad\Rightarrow\quad
{\rm radiation\ recovers\ the\ code}.
```

The transition is broadened by `2 log d`.  For a fixed finite code subspace,
this broadening is small on the Schwarzschild entropy scale.

### Relation To Known Work

The relevant known ingredients are:

- Page's theorem and decoupling theory for typical states and random
  isometries;
- Urbach's discussion of typical pure states and replica-wormhole-like Page
  behavior;
- de Boer, Hollander, and Rolph's derivation of Page curves and
  replica-wormhole-like contributions from random dynamics;
- Basu, Wen, and Zhou's Hilbert-space-reduction island formula.

The point supplied by our Hamiltonian class is the weighted evaporation
assembly:

```tex
{\rm density\ of\ states}+{\rm boundary\ operator\ count}
\quad\Rightarrow\quad p_\alpha,
```

and

```tex
S_{\rm micro}(E)
\quad\Rightarrow\quad
{\rm the\ post\mbox{-}Page\ contraction}.
```

So the correct claim is:

```text
The Hamiltonian class reproduces the replica-contraction structure of the
island saddle at fixed Renyi order.  The contraction is algebraic: replicas connect through the smaller remaining core factor.
```

This exceeds a plain Page-curve statement.  It does not produce a spacetime
replica wormhole, QES extremization, or an interior reconstruction map.

## 2. Boundary-Accessible `S(E) ~ E^2`

### What Must Be Generated

The current Hamiltonian requires an energy-resolved subsystem with

```tex
S_{\rm micro}(E)\simeq cE^2,
```

and the states counted by this entropy must be accessible to the emission
operators.  Merely having many hidden states is insufficient, because the rate
law uses the inclusive boundary spectral weight.

The strengthened target is therefore:

```tex
S_{\rm accessible}(E)\sim E^2,
\qquad
N_{\rm emit}(E)\sim S_{\rm accessible}(E).
```

### Why Ordinary Additive Systems Do Not Help

For a conventional many-body system with an extensive energy and an extensive
number of active degrees of freedom,

```tex
E\sim N,\qquad S\sim N,
```

so `S(E)` is approximately linear over thermodynamic ranges.  Negative
microcanonical heat capacity can occur in nonadditive or phase-separating
systems, and that phenomenon is well documented in long-range systems and
finite clusters.  The stronger Schwarzschild scaling

```tex
S(E)\sim E^2
```

is a sharper requirement.  It asks for an effective number of accessible states
that grows faster than the energy.

### Candidate Mechanism A: Pair/Connector Degrees

Suppose a clump has `K` primary constituents and an active boundary Hilbert
space carried by pairwise connector modes.  The number of pair labels is

```tex
N_{\rm conn}(K)\sim K^2.
```

If the clump energy scales as

```tex
E(K)\sim K,
```

and each connector carries an order-one finite Hilbert space, then

```tex
S_{\rm accessible}(K)\sim K^2,
\qquad
S_{\rm accessible}(E)\sim E^2.
```

This is the strongest non-geometric counting mechanism we have found.  It
turns the entropy law into pairwise state counting plus a linear energy cost
for the primary clump size.

The hard part is dynamics.  One still has to build a Hamiltonian where:

```tex
K
```

is an emergent or at least dynamical clump size, the connector modes are
physical states, and the emitted radiation couples to those connectors with
area-sized inclusive strength.

### Candidate Mechanism B: Matrix Block Size

A matrix block of size `K` has `K^2` matrix entries.  If the physical
boundary-accessible excitations in a block scale as `K^2`, while the block
energy scales as `K`, then again

```tex
S(E)\sim E^2.
```

This is conceptually attractive because matrix models can also produce
emergent separation: eigenvalue clumps, off-diagonal modes, and escaping
eigenvalues.  Matrix black-hole models use precisely this broad mechanism.

The catch is physical state counting.  Gauge constraints and dynamics can
remove large parts of the naive `K^2` matrix-entry count.  Finite matrix
Chern-Simons and quantum Hall droplet models teach the same lesson: matrix
variables can supply finite noncommutative geometry and edge labels, but raw
matrix-algebra dimension is not automatically thermodynamic entropy.

Thus the matrix route is promising only if one can identify a
boundary-accessible algebra whose physical state count scales as `K^2`.

### Candidate Mechanism C: Long-Range/Nonadditive Systems

Long-range systems naturally support ensemble inequivalence and negative
microcanonical heat capacity.  This makes them relevant to the thermodynamic
side of the project.

They do not by themselves generate `S(E)~E^2`.  They solve the easier problem:

```tex
C_{\rm micro}<0
```

in a non-gravitational setting.  Our target also needs the specific
Schwarzschild entropy-energy scaling and boundary-accessible emission strength.

### Current Assessment For Input 1

There is a useful reduction:

```tex
{\rm derive\ }S(E)\sim E^2
```

can be replaced by the more concrete model-building target

```tex
{\rm find\ a\ clump\ with\ }E(K)\sim K
{\rm\ and\ }O(K^2){\rm\ accessible\ boundary/connector\ states}.
```

That is real progress because it identifies the microscopic shape required by
the density of states.  It is not closed.  The most promising analytic branch
is the connector/matrix-block route, not ordinary local spins or finite
clusters.

## 3. Deterministic Mixing

### Direct Condition

The fine-grained result does not require a named random ensemble.  For a fixed
Hamiltonian and a coarse evaporation trajectory, the weak-coupling reduction
gives a composed Stinespring map

```tex
V:{\cal H}_{E_0}\to{\cal H}_B(E)\otimes{\cal H}_R(E).
```

For a code subspace with reference `Q`, the direct conditions are:

```tex
I(Q:R_{\rm early})\simeq 0
```

before Page time, and

```tex
I(Q:B_{\rm rem})\simeq 0
```

after Page time.  These are standard decoupling/Hayden-Preskill information
conditions.

Approximate low-order design behavior is a sufficient route.  It is not the
only route.

### Useful Weaker Target

Define an error `epsilon_2(V)` measuring the deviation of the fixed composed
map from the Haar second moment on the active support for the relevant
partitions.  Then the uniform code estimates become

```tex
\left\|\rho_{QB}-{I_Q\over d}\otimes {I_B\over b}\right\|_1
\lesssim
\sqrt{db(1/r+\epsilon_2(V))},
```

and

```tex
\left\|\rho_{QR}-{I_Q\over d}\otimes {I_R\over r}\right\|_1
\lesssim
\sqrt{dr(1/b+\epsilon_2(V))}.
```

For Hawking-weighted histories, replace `1/r` by `Tr p^2` on the recovery
side and use a typical-set support on the early-radiation side.

This makes the deterministic target precise:

```tex
{\rm find\ }H_{\rm mix}{\rm\ such\ that\ }\epsilon_2(V)
{\rm\ is\ small\ on\ the\ evaporation\ support}.
```

Fixed higher Renyi replica moments require the corresponding higher moment
condition.

### What Known Fast-Scrambling Results Give

The strongest nearby literature gives:

```tex
{\rm operator\ growth / OTOC\ decay}
\quad\Rightarrow\quad
{\rm channel\ scrambling / small\ mutual\ information}
```

in the unitary-channel state.  Hosur, Qi, Roberts, and Yoshida state this
connection directly.  Yoshida-Kitaev and Hayden-Preskill decoding results
then connect such scrambling to recoverability of a thrown-in code.

Expander-graph and sparse-graph fast-scrambling papers support concrete
Hamiltonian candidates:

```tex
H_{\rm mix}
=
\sum_{(ij)\in G_E}J_{ab}\sigma_i^a\sigma_j^b
+\sum_i h_a\sigma_i^a,
```

with `G_E` a bounded-degree expander or treelike/small-world graph.  These
models are good candidates for logarithmic operator growth.

The missing theorem is narrower than before:

```tex
{\rm chosen\ deterministic\ }H_{\rm mix}
\quad\Rightarrow\quad
{\rm decoupling\ for\ the\ evaporation\ partitions}.
```

Known OTOC/channel results give the bridge in form; they do not supply the
required bound for a specific deterministic expander Hamiltonian.

Recent Hayden-Preskill recovery work in Hamiltonian systems sharpens the
warning.  Nakata and Tezuka study time-independent Hamiltonians and find that
information recovery can occur in some chaotic models and fail in others.  They
also emphasize that recovery probes information-theoretic features of the
dynamics beyond spectral chaos or basic OTOC behavior.  This supports our
choice of target:

```tex
{\rm recovery/decoupling\ of\ the\ evaporation\ code}
```

is the property to demand from `H_mix`.  Fast scrambling is a route toward that
property, not the property itself.

### Current Assessment For Input 2

The abstract design condition can be replaced by a direct decoupling condition
on the fixed evaporation map.  That is the right standard language and it
reduces unnecessary randomness in the statement.

For a theorem-backed Result 2, approximate designs/TPEs remain sufficient.
For a more microscopic deterministic Hamiltonian, the best analytical route is

```tex
{\rm expander/treelike\ fast\ scrambling}
\to
{\rm OTOC/channel\ scrambling}
\to
{\rm code\ decoupling}.
```

The first two arrows are supported by existing work in nearby settings.  The
last quantitative step for our exact evaporation partitions remains open.

### What Can Be Closed Analytically Now

There are two analytical closures available immediately.

First, for Result 2 itself, use a sufficient mixing condition:

```tex
V{\rm\ has\ the\ required\ low\mbox{-}order\ moments}
```

or, equivalently for the information-flow statement,

```tex
Q{\rm\ decouples\ from\ the\ wrong\ subsystem}
```

at the appropriate stage of evaporation.  This is standard decoupling
language.  It is stronger than a vague scrambling assumption and weaker than
asking for Haar randomness of the full unitary.

Second, give a Hamiltonian route to that condition:

```tex
H_{\rm mix}{\rm\ on\ an\ expander/treelike\ graph}
\to
{\rm logarithmic\ operator\ spreading}
\to
{\rm channel\ scrambling}
\to
{\rm decoupling}.
```

The first arrow is supported by the expander and sparse-graph fast-scrambling
literature.  The second and third arrows are the content of channel-scrambling
and Hayden-Preskill-style results.  This gives a well-motivated route for a
fixed many-body Hamiltonian.

The step that is not available as a direct citation is:

```tex
{\rm this\ specific\ deterministic\ }H_{\rm mix}
\to
\epsilon_2(V){\rm\ small\ for\ the\ evaporation\ partitions}.
```

So the paper can close Result 2 using the stated low-order moment/decoupling
condition, and it can identify deterministic expander or treelike Hamiltonians
as the next microscopic realization problem.  It should not present that last
problem as solved by existing OTOC results.

Brown and Fawzi give another useful guidepost.  Their random-circuit result
proves decoupling directly and notes that approximate two-designs were the
standard known route to decoupling, while their proof analyzes decoupling
without first proving an ordinary two-design.  This reinforces the formulation
above: for the evaporator, the primary object is decoupling of `Q` from the
wrong output subsystem; a design condition is one sufficient method.

### Candidate Deterministic Mixer Class

The most economical candidate class is

```tex
K_E =
P_E\left[
\sum_{(ij)\in G_E}
\sum_{a,b=x,y,z}J_{ab}\sigma_i^a\sigma_j^b
+
\sum_i\sum_{a=x,y,z}h_a\sigma_i^a
\right]P_E,
```

where `G_E` is a deterministic bounded-degree expander on the active
boundary-accessible degrees of freedom.  A treelike/power-of-two interaction
graph is the nearest deterministic alternative:

```tex
K_E =
P_E\left[
\sum_i\sum_{m=0}^{\log N(E)}
J_m\,O_iO_{i+2^m}
 + H_{\rm local}
\right]P_E.
```

The expander version fits the horizon-cell picture better.  The treelike
version has a more explicit deterministic coupling pattern.  Both target fast
operator spreading; neither automatically proves the fixed-map decoupling
bound.

### Does This Remove Randomness?

The Hamiltonian can be fixed once and for all.  Randomness may enter only as a
proof tool or as a sufficient ensemble statement.  The physical evolution is
deterministic after choosing the Hamiltonian and the initial state.

There are three levels:

```text
Level A:
  abstract fixed-map decoupling condition.
  Result 2 uses this.

Level B:
  theorem-backed approximate design/TPE mixer.
  This gives a rigorous sufficient construction, with engineered mixing.

Level C:
  simple deterministic expander/treelike many-body Hamiltonian.
  This is the more natural microscopic target, with the direct decoupling
  theorem still missing.
```

This hierarchy is useful because it prevents one unproved deterministic
Hamiltonian claim from contaminating the result already obtained at Level A/B.

## Current Result After This Push

### Strengthened

The replica/island comparison is no longer only a flat Page theorem statement.
For Hawking-weighted radiation histories,

```tex
\mathbb E\,{\rm Tr}\rho_R^n
\simeq
\sum_{\sigma\in S_n}
b^{C(\sigma)-n}
\prod_{c\in{\rm cycles}(\tau\sigma)}
{\rm Tr}\,p^{|c|},
```

with leading branches

```tex
{\rm Tr}\,p^n
```

and

```tex
b^{1-n}.
```

This gives the weighted no-island/island saddle exchange directly.

### Reduced

The area emission law is no longer a separate rate assignment.  It follows
from local weak emission by `O(A)` boundary-accessible emitters.

### Still Open

Two inputs remain real:

```tex
S_{\rm accessible}(E)\sim E^2,
```

and a concrete deterministic `H_mix` satisfying the required decoupling
condition for the composed evaporation map.

The first is best attacked through connector/matrix-block state counting.  The
second is best attacked through expander/treelike fast scrambling plus
channel-scrambling decoupling.

## Further Probe Of Input 1: The Smooth Energy Problem

The connector and matrix-block routes are attractive because they explain why
the number of accessible labels could scale quadratically in a size variable.
They do not automatically explain the Hawking quantum scale.

Let `K` be a clump-size variable.  The desired counting is

```tex
S(K)\sim K^2.
```

If the mass-equivalent energy is

```tex
E(K)\sim K,
```

then

```tex
S(E)\sim E^2,\qquad T(E)\sim {1\over E}.
```

This is exactly the black-hole thermodynamic scaling.  The danger is to model
evaporation as

```tex
K\to K-1.
```

That jump releases

```tex
\Delta E\sim O(1),
```

while a typical Hawking quantum has

```tex
\omega\sim T\sim {1\over K}.
```

For a black hole, one typical quantum changes the entropy or area by order one:

```tex
\Delta S\simeq {dS\over dE}\omega\sim K\,{1\over K}\sim O(1).
```

Since `S~K^2`, this corresponds to

```tex
\Delta K\sim {1\over K}.
```

Thus a microscopic model with `K^2` connector states should not treat a single
emission as the loss of one primary constituent.  A better large-`K` picture is:

```text
one Hawking quantum removes O(1) entropy/area labels;
O(K) quanta are needed to change the macroscopic size K by order one.
```

This is the first real constraint on a microscopic connector model.

### Candidate Hamiltonian Shape

A useful abstract Hamiltonian shape is:

```tex
{\cal H}_{\rm core}
=
\bigoplus_K {\cal H}_{K,\rm coll}\otimes{\cal H}_{K,\rm conn},
\qquad
\dim{\cal H}_{K,\rm conn}\sim \exp(\alpha K^2).
```

The collective factor supplies a dense energy coordinate in a narrow band near
`E~K`, while the connector factor supplies the large degeneracy:

```tex
H_{\rm core}
=
\sum_K P_K\left[H_{K,\rm coll}+E_K\right]P_K
+H_{\rm conn\ split}.
```

The required density of states is

```tex
\rho(E)\sim \exp(cE^2)
```

after summing over nearby `K` sectors and the collective levels.  The
Hamiltonian may be abstract, but the required structure is now specific:

1. `K^2` boundary-accessible connector labels;
2. a collective energy coordinate with level spacings fine compared with
   `T~1/K`;
3. emission operators that remove order-one connector entropy while lowering
   the collective energy by `O(1/K)`;
4. slow drift of `K` over `O(K)` emissions.

This is closer to a black-hole evaporation trajectory than a one-shell-removal
rule.

### Minimal Abstract Connector-Core Construction

The smallest formal construction that implements this idea is:

```tex
{\cal H}_{\rm core}
=
\bigoplus_{K=1}^{K_{\max}}
{\cal H}_{K,\rm coll}\otimes
\bigotimes_{a=1}^{N_K}{\cal h}_a,
\qquad
N_K=\lfloor \alpha K^2\rfloor,\quad \dim{\cal h}_a=q.
```

Choose a collective spectrum in each `K` sector,

```tex
H_{K,\rm coll}|m\rangle
=
\left(K+{m\over K}\right)|m\rangle,
\qquad
m=0,1,\ldots,O(K).
```

Then the level spacing relevant for emission is

```tex
\omega_K\sim {1\over K},
```

while the leading degeneracy at energy `E~K` is

```tex
\log\dim{\cal H}_{K,\rm conn}
=
N_K\log q
\sim \alpha K^2\log q
\sim \alpha E^2\log q.
```

An emission operator can lower `m` by one and transfer energy `1/K` to an
outgoing mode.  After `O(K)` such emissions, the collective coordinate moves
from the `K` sector to the neighboring `K-1` sector.  The entropy lost per
typical emission is

```tex
\Delta S
\simeq {dS\over dE}{1\over K}
\sim O(1),
```

as in Schwarzschild evaporation.

This construction is useful because it proves consistency of the ingredients:

```text
quadratic connector degeneracy,
linear macroscopic energy,
small Hawking-scale quanta,
order-one entropy loss per quantum.
```

It remains a structured realization of the density-of-states input.  A deeper
model would have to generate the connector degeneracy and the collective
energy coordinate from simpler degrees of freedom.

### Does This Remove The Entropy Input?

Partially.

The quadratic state count can be generated by pair/connector labels:

```tex
\#({\rm connector\ labels})\sim K^2.
```

The remaining input is the relation

```tex
E\sim K
```

and the existence of a dense collective spectrum whose shell count is dominated
by the connector degeneracy.  This is milder than directly assigning

```tex
\dim{\cal H}_E=\exp(cE^2),
```

but it is still a model-building assumption.

### Best Version Of The Spectrum Route

The strongest analytic route now looks like this:

```text
primary clump size K
  -> O(K^2) pair/connector boundary labels
  -> S_accessible(K) ~ K^2
  -> collective energy E ~ K
  -> S_accessible(E) ~ E^2
  -> DOS-ratio thermality and negative heat capacity
  -> boundary connector operators give area-sized emission.
```

The unresolved step is the collective Hamiltonian:

```tex
H_{\rm core}
```

must make `E~K` and the `K^2` connector degeneracy simultaneous physical
features, with small-energy emission branches available at `\omega\sim1/K`.

### Why This Is Still Worth Pushing

This route converts the hardest input into a concrete design criterion for a
non-gravitational many-body system.  It says exactly what an acceptable
microscopic origin of the Schwarzschild density of states must look like:

```text
linear energy in a size variable,
quadratic accessible degeneracy in the same size variable,
small energy-changing branches that remove order-one entropy at a time.
```

That is narrower than the original search over arbitrary long-range systems or
matrix clumps.

## References Used In This Pass

- Page theorem and standard random-isometry decoupling.
- Urbach, "The entanglement entropy of typical pure states and replica
  wormholes," arXiv:2105.15059.
- de Boer, Hollander, and Rolph, "Page curves and replica wormholes from random
  dynamics," arXiv:2311.07655.
- Basu, Wen, and Zhou, "Entanglement Islands from Hilbert Space Reduction,"
  arXiv:2211.17004.
- Hosur, Qi, Roberts, and Yoshida, "Chaos in quantum channels,"
  arXiv:1511.04021.
- Bentsen, Gu, and Lucas, "Fast scrambling on sparse graphs,"
  arXiv:1805.08215.
- Brown and Fawzi, "Decoupling with random quantum circuits,"
  arXiv:1307.0632.
- Nakata and Tezuka, "Hayden-Preskill Recovery in Hamiltonian Systems,"
  arXiv:2303.02010.
- Barbon and Magan, "Fast Scramblers, Horizons and Expander Graphs,"
  arXiv:1204.6435.
- Campa, Dauxois, and Ruffo, "Statistical mechanics and dynamics of solvable
  models with long-range interactions," Physics Reports 480 (2009).
- Hanada et al., "Chaos in Matrix Models and Black Hole Evaporation,"
  arXiv:1602.01473.
