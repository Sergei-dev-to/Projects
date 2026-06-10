# Fixed Hamiltonian Mixer Push

## Question

Can the shell-mixing condition in Result 2 be supplied by a simple fixed
Hamiltonian, preferably deterministic, instead of an abstract approximate
design or TPE block?

The relevant target is the information-flow condition needed by the
evaporator:

```tex
I(Q:R_{\rm early})\simeq 0
```

before Page time, and

```tex
I(Q:B_{\rm rem})\simeq 0
```

after Page time, for the code subspace being tested.

## Candidate Hamiltonian

The best fixed-Hamiltonian candidate remains a nonintegrable spin Hamiltonian
on a bounded-degree expander graph:

```tex
K_N
=
\sum_{(ij)\in G_N}
\left(
J_x X_iX_j+J_yY_iY_j+J_zZ_iZ_j
\right)
+\sum_i(h_x X_i+h_z(i)Z_i).
```

Here:

```text
N       = number of active boundary/core degrees of freedom in the shell,
G_N     = fixed bounded-degree expander graph,
h_z(i)  = field pattern; for the clean uniformity argument, prefer a
          symmetry-respecting choice.
```

Earlier we considered a deterministic inhomogeneous choice,

```tex
h_z(i)=h_z\cos(2\pi \varphi i+\phi),
```

with irrational `varphi`, or a fixed algebraic sign pattern on the vertices.
That helps remove obvious degeneracies, but it weakens the cleanest analytical
route to boundary-channel uniformity.  For the bridge lemma, the better
candidate is a homogeneous or symmetry-respecting Hamiltonian on a
vertex-transitive expander, with symmetry sectors treated explicitly.

The shell mixer in the evaporator would be

```tex
H_{\rm mix}
=
\bigoplus_E P_E K_{N(E)} P_E,
```

where

```tex
N(E)\sim A(E)\sim S_{\rm micro}(E).
```

After choosing `G_N`, couplings, and fields, the Hamiltonian is fixed.  No
couplings are resampled during evaporation.

## Why This Candidate Is The Right One To Push

The expander graph has two advantages:

1. It is sparse: every degree of freedom has only `O(1)` neighbors.
2. It has small graph diameter and rapid mixing properties.

This matches the desired black-hole intuition better than a full all-to-all
Hamiltonian.  The graph is nonlocal as a graph on labels, but local on the
chosen expander interaction geometry.

Known literature supports the path:

```tex
{\rm expander/sparse\ connectivity}
\to
{\rm logarithmic\ scrambling\ time}
\to
{\rm operator\ growth/OTOC\ decay}.
```

Barbon and Magan propose expander-graph systems as microscopic models of
horizon thermalization.  Bentsen, Gu, and Lucas analyze fast scrambling on
sparse graphs.  Hosur, Qi, Roberts, and Yoshida connect OTOC decay in a
unitary channel to small mutual information between input subsystems and most
output partitions.  Yoshida and Kitaev connect OTOC decay to
Hayden-Preskill recovery.

Thus the candidate is the most direct fixed-Hamiltonian route to the exact
diagnostic Result 2 needs.

## The Right Lemma

Let the active code subspace have dimension `d` and be purified by a reference
`Q`.  Let one coarse scrambling/emission block define a Stinespring map

```tex
V_{\rm block}: {\cal H}_{B(E)}
\to
{\cal H}_{B(E')}\otimes{\cal H}_{R({\rm block})}.
```

Let the composed map over many blocks be

```tex
V_{E_0\to E}:{\cal C}_d
\to
B_b(E)\otimes R(E_0\to E).
```

The fixed-Hamiltonian result we want is:

```tex
{\bf Lemma\ target.}\quad
K_N{\rm\ generated\ block\ evolution}
\Rightarrow
I_2(Q:X_{\rm wrong})\le \epsilon
```

for the relevant wrong subsystem:

```tex
X_{\rm wrong}=R_{\rm early}\quad{\rm before\ Page\ time},
```

and

```tex
X_{\rm wrong}=B_{\rm rem}\quad{\rm after\ Page\ time}.
```

Here `I_2` can be written using second-Renyi entropies or the channel-state
second moment.  The trace-distance version is:

```tex
\left\|\rho_{QX_{\rm wrong}}
-\rho_Q\otimes\rho_{X_{\rm wrong}}\right\|_1
\le \epsilon'.
```

Once this lemma is available, standard decoupling/recovery logic gives:

```tex
early radiation is uninformative about the code,
late radiation recovers the code after Page time.
```

This is the exact fixed-Hamiltonian replacement for the abstract shell-mixing
assumption.

## What Existing Work Supplies

### Channel scrambling bridge

Hosur, Qi, Roberts, and Yoshida study unitary channels as states.  Their result
is the right bridge: generic OTOC decay implies that input subsystems have near
vanishing mutual information with most output partitions.  Yoshida and Kitaev
then use OTOC decay in Hayden-Preskill decoding.

This supplies:

```tex
{\rm channel\ OTOC\ decay}
\to
{\rm mutual\ information\ decoupling}
\to
{\rm recovery}.
```

### Expander/sparse graph bridge

Barbon and Magan motivate expander graphs as horizon fast scramblers.  Bentsen,
Gu, and Lucas show that sparse graph connectivity can support logarithmic
scrambling and operator growth.

This supplies:

```tex
{\rm expander/sparse\ geometry}
\to
{\rm plausible\ O(\log N)\ operator\ spreading}.
```

### Treelike deterministic alternative

The treelike cold-atom model gives a deterministic nonrandom coupling pattern:
sites interact at distances that are powers of two.  In the treelike regime the
model shows very fast spreading of information.

This supplies a backup Hamiltonian family:

```tex
K_N^{\rm tree}
=
\sum_i\sum_{m=0}^{\log N}
J_m O_iO_{i+2^m}
+H_{\rm local}.
```

It is less naturally tied to area-cell expander intuition, but it is more
explicitly deterministic.

## The Remaining Gap

No cited result appears to prove the needed lemma for the exact Hamiltonian
above:

```tex
K_N{\rm\ on\ a\ deterministic\ expander}
\to
I_2(Q:X_{\rm wrong})\le\epsilon
```

for the evaporation partitions.

The missing proof would have to control four things:

1. operator support becomes area-wide in time `O(log N)`;
2. the spreading is sufficiently uniform over the boundary emission channels;
3. no conserved quantity or approximate symmetry preserves code information in
   `X_wrong`;
4. the composed block map has small channel mutual information for the chosen
   code size.

This is narrower than proving an approximate unitary design for the whole
shell.  It is still a real dynamical theorem.

## Possible Way To Close The Gap

The evaporation partition is special in a helpful way.  The radiation is not a
fixed spatial region of the expander graph.  Each emitted quantum is created by
the interaction

```tex
H_I
=
\sum_{\mu=1}^{N(E)} O_\mu b^\dagger_\mu+{\rm h.c.},
```

where `mu` labels an area-sized set of boundary emission channels.  Along a
radiation history, the emitted channel labels

```tex
\mu_1,\mu_2,\ldots,\mu_m
```

sample this area-sized boundary algebra.

This matters because the strongest channel-scrambling statements say that OTOC
decay makes input subsystems nearly uncorrelated with most output partitions.
If the emission channel labels sample typical boundary partitions after each
scrambling block, then the relevant radiation subsystem is not an adversarially
chosen output partition.  It is a typical sampled output subsystem.

This suggests a sharper route:

```tex
K_N{\rm\ gives\ OTOC/channel\ scrambling}
```

plus

```tex
{\rm boundary\ emission\ channels\ sample\ typical\ output\ partitions}
```

implies

```tex
I_2(Q:R_{\rm sampled})\ll1
```

in the early regime, and the corresponding post-Page decoupling of `Q` from
the smaller remaining core.

The new condition is a typical-partition condition:

```tex
\Pr_{\mu_1,\ldots,\mu_m}
\left[
I_2(Q:R_{\mu_1\cdots\mu_m})>\epsilon
\right]\ll1.
```

This is close to the literature because Hosur-Qi-Roberts-Yoshida already
phrase the channel-scrambling consequence in terms of most output partitions.

### What Must Still Be Shown

Two facts would close this route:

1. The expander Hamiltonian gives the OTOC/channel-scrambling condition after
   `O(log N)` shell time.
2. The boundary emission process samples the output partitions in the sense
   required by the channel-scrambling theorem.

The second fact is plausible in the area-emission Hamiltonian because the
inclusive rate sums over `O(A)` weak boundary channels and the shell dynamics
mixes local operators across the active boundary algebra.  It should be stated
as a condition unless a theorem is proved.

This route is better than demanding decoupling for an arbitrary fixed
partition.  It uses the actual structure of evaporation: radiation is a
sampled sequence of weak boundary probes.

### Formal Sampled-Partition Criterion

Let `P_m` be the probability distribution on `m` emitted boundary-channel
histories induced by the golden-rule emission rates and shell mixing.  Let
`R_{\boldsymbol\mu}` be the radiation subsystem labelled by

```tex
\boldsymbol\mu=(\mu_1,\ldots,\mu_m).
```

The early-time condition can be stated as

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:R_{\boldsymbol\mu})
\le \epsilon_{\rm early}.
```

Markov's inequality then gives

```tex
\Pr_{\boldsymbol\mu}
\left[
I_2(Q:R_{\boldsymbol\mu})>\delta
\right]
\le {\epsilon_{\rm early}\over \delta}.
```

Thus the sampled radiation histories are typically uninformative whenever the
average channel mutual information is small.

The post-Page condition is similar, with the sampled radiation history replaced
by the remaining core:

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:B_{\rm rem}(\boldsymbol\mu))
\le \epsilon_{\rm late}.
```

This is the precise theorem target for a fixed expander mixer.  A sufficient
route is:

```tex
P_m{\rm\ is\ close\ to\ uniform\ over\ boundary\ samples}
```

and

```tex
\mathbb E_{C:\ |C|=m} I_2(Q:C)\le\epsilon
```

from channel-scrambling/OTOC decay.  Then the sampled evaporation histories
inherit the same decoupling bound, up to the mismatch between `P_m` and the
uniform typical-partition measure.

## A Useful Intermediate Criterion

Define the channel state of a unitary block by applying the block unitary to a
maximally entangled input-reference state:

```tex
|\Psi_U\rangle_{Q\,{\rm out}}
=
(I_Q\otimes U)|\Phi\rangle_{Q\,{\rm in}}.
```

For an input code subsystem `A` and an output subsystem `C`, require

```tex
I_2(A:C)_{\Psi_U}\le \epsilon
```

for all `C` of the type that will become `X_wrong` in the evaporation map.
Hosur-Qi-Roberts-Yoshida relate this kind of channel mutual information to
averaged OTOCs.  So a concrete analytical target is:

```tex
{\rm prove\ averaged\ OTOCs\ are\ small\ for\ }K_N
{\rm\ on\ the\ relevant\ input/output\ partitions}.
```

That would close the fixed-Hamiltonian route without proving a full design
theorem.

## Can We Get A Good Fixed Hamiltonian Now?

We can write down a good candidate now:

```tex
H_{\rm tot}
=
H_{\rm B}^{(0)}
+\bigoplus_E P_E K_{N(E)}P_E
+H_{\rm R}
+H_I,
```

with

```tex
K_N
=
\sum_{(ij)\in G_N}
\left(
J_x X_iX_j+J_yY_iY_j+J_zZ_iZ_j
\right)
+\sum_i(h_x X_i+h_z(i)Z_i),
```

and `G_N` a fixed deterministic expander.

What we cannot yet claim from citations alone is:

```tex
K_N{\rm\ proves\ the\ required\ decoupling}.
```

The most promising refinement is:

```tex
K_N{\rm\ gives\ channel\ scrambling}
+{\rm typical\ boundary\ channel\ sampling}
\Rightarrow
{\rm evaporation\ decoupling}.
```

The strongest current fixed-Hamiltonian statement is:

```text
This is the leading concrete autonomous mixer candidate.  Existing
fast-scrambling and channel-scrambling results support the route, and they
identify the right diagnostic.  The quantitative decoupling theorem for this
specific evaporation partition remains open.
```

## Does This Help The Paper?

Yes. It should supplement the theorem-backed mixer in Result 2.

The paper can say:

```text
The theorem-backed version uses approximate designs, TPEs, or Hamiltonian
design constructions.  A natural fixed-Hamiltonian realization would be a
nonintegrable expander or treelike spin Hamiltonian.  The required diagnostic
is decoupling of the evaporation code, equivalently channel mutual information,
with OTOC decay as a standard route.
```

This turns the fixed-Hamiltonian issue into a precise future theorem rather
than a vague naturalness complaint.

## Current Verdict

There is a good fixed Hamiltonian to push:

```tex
{\rm nonintegrable\ deterministic\ expander\ spin\ Hamiltonian}.
```

There is also a precise target:

```tex
I_2(Q:X_{\rm wrong})\ll1
```

for the composed evaporation channel.

What is missing is a proof that the chosen fixed Hamiltonian satisfies that
target.  The route is plausible and literature-backed, but not closed.

## Sources

- Hosur, Qi, Roberts, Yoshida, "Chaos in quantum channels,"
  arXiv:1511.04021.
- Yoshida, Kitaev, "Efficient decoding for the Hayden-Preskill protocol,"
  arXiv:1710.03363.
- Barbon, Magan, "Fast Scramblers, Horizons and Expander Graphs,"
  arXiv:1204.6435.
- Bentsen, Gu, Lucas, "Fast scrambling on sparse graphs,"
  arXiv:1805.08215.
- Bentsen et al., "Treelike interactions and fast scrambling with cold atoms,"
  arXiv:1905.11430.
- Belyansky et al., "Minimal Model for Fast Scrambling,"
  arXiv:2005.05362.

## Attack Map For Gap 2

Gap 2 should be split into two dynamical questions.

### 1. Boundary-channel thermality and uniformity

This is the ETH part.

For each boundary operator `O_mu`, we need shell-averaged matrix elements

```tex
{\cal A}_\mu(E,\omega)
=
{1\over D_E}
\operatorname{Tr}\!\left[
\Pi_E O_\mu^\dagger
\Pi_{E-\omega}O_\mu\Pi_E
\right]
```

to be smooth in `E,omega` and roughly independent of `mu`:

```tex
{\cal A}_\mu(E,\omega)
\simeq
{1\over N(E)}{\cal A}(E,\omega).
```

This is close to standard ETH and subsystem ETH.  ETH gives local thermality
and smooth matrix elements for few-body operators in chaotic many-body systems.
Subsystem ETH states the analogous condition using reduced density matrices of
subsystems.

This part supports:

```text
local emission spectrum,
microcanonical detailed-balance factor,
rough equality of boundary-channel weights.
```

It does not by itself prove Page-like information flow.

### 2. Page decoupling and information hiding

This is the scrambling/OTOC part.

The Page/Hayden-Preskill condition depends on whether an initial reference is
hidden from the wrong output subsystem after the dynamics.  That depends on
higher correlations, equivalently channel OTOCs or a decoupling statement.

The imported route is:

```text
operator spreading / OTOC decay
    -> channel scrambling
    -> small mutual information with most output partitions
    -> Page-like decoupling for emitted histories.
```

This is why ETH is helpful but insufficient.  ETH gives local thermality and
typical matrix elements.  OTOCs/channel scrambling give information hiding.

### 3. The special advantage of the evaporation channel

The radiation subsystem is not a fixed contiguous region of the expander graph.
It is a history of emitted boundary labels,

```tex
\boldsymbol\mu=(\mu_1,\ldots,\mu_m),
```

sampled by the weak interaction `H_I`.  If the ETH/uniformity condition above
holds, the emitted labels approximate a typical sample from the boundary
operator algebra.  Then the "most output partitions" statement in
channel-scrambling results becomes relevant to the actual radiation.

This gives the bridge lemma we should try to prove:

```text
Assume:
  (i) K_N has OTOC/channel scrambling by time t_scr = O(log N);
 (ii) boundary operators satisfy ETH-like channel uniformity;
(iii) emissions occur after enough in-shell mixing, t_scr << t_emit.

Then:
  the composed evaporation map satisfies the Page decoupling conditions
  for typical radiation histories.
```

### 4. Candidate Hamiltonian ranking

```text
deterministic expander spin Hamiltonian
    Best match to the model.  The cleanest version uses a vertex-transitive
    expander and symmetry-related boundary operators; proof of channel
    scrambling is hardest.

treelike deterministic Hamiltonian
    Strong deterministic fast-spreading evidence; less naturally tied to
    area-cell boundary sampling.

sparse random regular graph Hamiltonian, chosen once
    Easier to support statistically; less satisfying than a deterministic
    graph, but still a fixed Hamiltonian after the draw.

Hamiltonian-design / TPE construction
    Theorem-backed and already enough for Result 2; physically abstract.
```

### 5. Non-micro next move

The next useful step is the bridge lemma.  A first version is written in
`notes/gap2_bridge_lemma.md`.  The target estimate is:

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:R_{\boldsymbol\mu})
\le \epsilon_{\rm early},
\qquad
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:B_{\rm rem}(\boldsymbol\mu))
\le \epsilon_{\rm late}.
```

The proof should use:

```text
boundary-channel ETH       -> P_m is close to typical boundary sampling,
channel OTOC scrambling    -> most sampled outputs decouple,
Markov/concentration       -> typical radiation histories decouple.
```

This would not prove fast scrambling for the expander Hamiltonian from first
principles.  It would isolate exactly what the sparse/expander scrambling
literature must supply.

## Current Direction 1 Candidate

The deterministic version should now be a Cayley-expander mixer, written in
`notes/direction1_cayley_expander_candidate.md`.

The point of using a Cayley expander is that it is vertex-transitive.  If the
spin Hamiltonian is homogeneous under the left group action and the boundary
emission operators are related by that action, then the shell-averaged
boundary-channel weights are equal by symmetry:

```tex
{\cal A}_{g,\lambda}(E,\omega)
=
{\cal A}_{g',\lambda}(E,\omega).
```

This closes the boundary-uniformity part of Gap 2 much better than the earlier
inhomogeneous-field proposal.  The remaining hard input is then only:

```text
channel scrambling / OTOC decay for the homogeneous Cayley-expander
Hamiltonian.
```
