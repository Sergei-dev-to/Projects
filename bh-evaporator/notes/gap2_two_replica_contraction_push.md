# Gap 2 Two-Replica Contraction Push

## Purpose

Push the deterministic mixer gap one level further without adding numerics.

The target is no longer a full design statement.  The target is a
second-moment contraction statement for the composed evaporation channel:

```tex
V_{0\to m}:{\cal C}\to B_m\otimes R_{\le m}.
```

We want the wrong subsystem to decouple from the reference `Q`:

```tex
I_2(Q:B_m)\ll1
```

after the Page time, and analogously `I_2(Q:R_{\le m})\ll1` before the Page
time for code information not yet radiated.

## The Second-Moment Object

Let the initial code state be purified by `Q`.  For one coarse evaporation
block,

```tex
{\cal M}_j:\rho_{QB_j}\mapsto \rho_{QB_{j+1}R_j}.
```

The post-Page wrong subsystem is `B_{j+1}`.  The second-Renyi decoupling
diagnostic can be taken as a collision-norm deviation from product form:

```tex
\Delta_{j+1}^{(2)}
=
\left\|
\rho_{QB_{j+1}}
-\rho_Q\otimes\rho_{B_{j+1}}
\right\|_2^2 .
```

Equivalently, in channel-state language this is controlled by traces of
two-copy swap operators:

```tex
\Tr\rho_{QB_{j+1}}^2,\qquad
\Tr\rho_Q^2,\qquad
\Tr\rho_{B_{j+1}}^2 .
```

Thus only the second moment of the block dynamics is needed.

## Contraction Shape

The desired estimate is

```tex
\Delta_{j+1}^{(2)}
\le
\kappa_j\Delta_j^{(2)}
+\varepsilon_{{\rm mix},j},
\qquad
\kappa_j<1.
```

The contraction factor has a kinematic part and a mixing part.

If the core factor changes as

```tex
B_j\simeq B_{j+1}\otimes S_j,
```

with shell dimension `s_j=dim S_j`, then an exactly scrambled state distributes
reference correlations over `B_{j+1}S_j`.  Tracing out the emitted shell gives
a contraction of order

```tex
\kappa_j^{\rm Haar}
\sim
{d_{B_{j+1}}\over d_{B_j}}
=
{1\over s_j},
```

up to the usual finite-dimension Page corrections and code-size factors.  In
the real model the emitted shell is a weighted energy/channel factor, so this
should be read as the corresponding second-moment contraction of the actual
block Stinespring map.

The error term

```tex
\varepsilon_{{\rm mix},j}
```

is the failure of the fixed Hamiltonian evolution over the mixing window to
match the Haar/two-design second moment on the relevant sector.

After iteration,

```tex
\Delta_m^{(2)}
\le
\left(\prod_{j<m}\kappa_j\right)\Delta_0^{(2)}
+\sum_{j<m}\varepsilon_{{\rm mix},j}
\prod_{\ell>j}\kappa_\ell .
```

This is the mathematically clean form of "many scrambling windows."  The
paper does not need each step to be Haar-random; it needs the composed channel
to make the accumulated second-moment error small.

## Two-Replica Object

Let

```tex
U_j(t)=e^{-iK_{N_j}t}
```

be the in-shell mixing unitary.  Its second moment acts on two copies as

```tex
{\cal T}_j^{(2)}(t)
=
U_j(t)^{\otimes 2}\otimes U_j(t)^{*\otimes 2}.
```

This closed-system object is unitary on the doubled space.  It is useful for
tracking phases and invariants, but it cannot by itself be the contraction
operator for Page decoupling.  The contraction appears only after the physical
emission block is included: weak emission, radiation recording/tracing, and any
waiting-time or energy-window coarse graining present in the Markov limit.

For an ensemble of random circuits, the averaged second-moment operator is a
linear map whose spectral gap controls convergence to the Haar second moment.
Brown-Fawzi and the random-circuit design literature prove decoupling by
bounding this kind of moment operator.

For one deterministic Hamiltonian there is no ensemble average over gates.
The possible replacements are:

1. time averaging over a window,
   ```tex
   {1\over T}\int_0^T dt\,{\cal T}^{(2)}(t);
   ```
2. energy-window averaging in the microcanonical shell;
3. coarse graining over emission times and channel histories.

The deterministic theorem must specify which open-channel or averaging
operation is physically present.  In the evaporator, the natural averaging is
not arbitrary: weak emission
samples waiting times, energies, and boundary channels.  Therefore the correct
second-moment object is the one induced by the actual coarse block map,
including the weak emission channel.

The open-channel version is written in
`notes/gap2_open_channel_contraction.md`.

## Comparison With Random-Circuit Proofs

Random-circuit decoupling proofs use randomness in two places.

### Random local gates

The circuit ensemble directly defines a second-moment Markov operator.  Its
fixed points are the Haar second-moment invariants, and the spectral gap gives
the mixing rate.

For the Cayley Hamiltonian, local gates are replaced by coherent evolution
under fixed interactions.  The missing step is to show that the induced
two-replica dynamics has a comparable contraction on the non-invariant sector.

### Random edge choice or architecture mixing

Random circuits often choose edges or layers randomly.  On an expander
architecture, graph expansion helps spread information rapidly.

For the Cayley Hamiltonian, all edges act coherently and homogeneously.  The
graph expansion is still present, but there is no stochastic edge refresh.  The
new theorem would need to show that coherent expander dynamics does not leave
large non-decaying two-replica modes beyond symmetry-sector invariants.

## Role Of Cayley Symmetry

The Cayley symmetry solves boundary-channel equality:

```tex
{\cal A}_{g,\lambda}(E,\omega)
=
{\cal A}_{g',\lambda}(E,\omega).
```

In the two-replica problem it also introduces exact invariant sectors.  The
second-moment contraction should therefore be stated after projecting out the
invariants associated with symmetry charges.

Let `P_ch` project onto the exact charge/symmetry data retained by the channel.
The theorem target is not

```tex
{\cal T}^{(2)}\to{\cal T}_{\rm Haar}^{(2)}
```

globally.  It is

```tex
(1-P_{\rm ch}){\cal T}^{(2)}(1-P_{\rm ch})
\quad{\rm contracts}.
```

If the radiation modes transform covariantly and the full interaction
satisfies

```tex
[U_a^B\otimes U_a^R,H_I]=0,
```

then charge information can be carried by radiation records.  Otherwise the
charge sector must be treated as a superselection label excluded from the code.

## What Would Close The Gap

The deterministic Cayley theorem would look like this:

```text
For a family of homogeneous nonintegrable spin Hamiltonians K_N on Cayley
expanders, and for code subspaces inside a fixed symmetry sector, the
two-replica block map induced by mixing plus weak boundary emission obeys

    Delta_{j+1}^{(2)} <= kappa_j Delta_j^{(2)} + epsilon_j

with kappa_j<1 and sum_j epsilon_j small over the evaporation window.
```

This is weaker than proving a unitary design and better matched to the Page
calculation.

## What Existing Literature Supplies

The literature supplies the template, not the final theorem:

```text
Brown-Fawzi:
    decoupling from random circuits via second moments.

Brandao-Harrow-Horodecki and successors:
    moment-operator spectral gaps for random circuits.

Mittal-Hunter-Jones:
    random circuits on arbitrary graph architectures.

Nakata-Wakakuwa-Koashi:
    symmetry-aware Hayden-Preskill and charge-sector effects.

Barbon-Magan / Bentsen-Gu-Lucas:
    expander/sparse graph motivation for fast scrambling.
```

The original work is the deterministic replacement:

```text
random second-moment Markov gap
    -> two-replica contraction of the weak-emission block generated by a fixed
       Cayley Hamiltonian.
```

## Current Status

This push makes the remaining gap more precise and smaller:

```text
sectorwise two-replica contraction for the composed evaporation channel,
with exact charges tracked separately.
```

I do not see a way to claim this theorem from existing literature alone.  The
next analytical move would be to derive the explicit two-replica open-channel
map for a simple Cayley Hamiltonian and identify its invariant subspace and
possible gap estimate.
