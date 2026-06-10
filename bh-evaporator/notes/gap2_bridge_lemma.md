# Gap 2 Bridge Lemma

## Purpose

Gap 2 is the attempt to replace the abstract in-shell mixer by a fixed
Hamiltonian.  The fixed Hamiltonian does not need to generate a full Haar
design on each shell.  The evaporation problem only needs a channel statement:
the radiation histories selected by the weak boundary coupling must decouple
from the wrong reference subsystem on the two sides of the Page time.

This note isolates the statement we need and separates the standard literature
inputs from the project-specific input.

## Setup

Inside an area shell, take a fixed Hamiltonian

```tex
K_N =
\sum_{(ij)\in G_N}
(J_xX_iX_j+J_yY_iY_j+J_zZ_iZ_j)
+\sum_i(h_xX_i+h_z(i)Z_i),
```

or a closely related sparse/treelike fast-scrambling Hamiltonian.  The full
evaporation Hamiltonian contains the weak boundary coupling

```tex
H_I =
g\sum_{\mu=1}^{N(E)}
\sum_\lambda\int d\omega\,
\omega^{p/2}
\left[
O_{\mu\lambda}(\omega)b^\dagger_{\mu\lambda}(\omega)
+{\rm h.c.}
\right].
```

The label `mu` runs over the area-sized boundary-accessible emission algebra.
A radiation history over `m` emissions is

```tex
\boldsymbol\mu=(\mu_1,\ldots,\mu_m),
```

with probability measure `P_m` induced by the golden-rule rates.

Let `Q` purify the code subspace initially placed in the shell.  Let
`R_{\boldsymbol\mu}` denote the radiation subsystem associated with an emitted
history, and let `B_{\rm rem}(\boldsymbol\mu)` denote the remaining core after
that history.

The Page decoupling targets are

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:R_{\boldsymbol\mu})
\le \epsilon_{\rm early},
```

before the Page time, and

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:B_{\rm rem}(\boldsymbol\mu))
\le \epsilon_{\rm late},
```

after the Page time.

Here `I_2` can be written using second-Renyi channel states.  A trace-distance
version follows from standard decoupling inequalities.

## Lemma Target

The useful fixed-Hamiltonian bridge is:

```text
Assume:
  1. K_N has channel scrambling on time t_scr = O(log N).
  2. The boundary emission operators obey ETH-like channel uniformity.
  3. Emissions are dilute relative to mixing: t_scr << t_emit.

Then:
  typical radiation histories selected by H_I satisfy the Page decoupling
  conditions for the composed evaporation channel.
```

This is the statement that would convert the abstract shell-mixing condition
into a fixed-Hamiltonian condition.

## Input 1: Channel Scrambling

The imported statement is the one used in the OTOC/channel literature:

```text
OTOC decay for the unitary channel
    -> small mutual information between input subsystems and almost all
       output partitions.
```

Hosur, Qi, Roberts, and Yoshida show this in the channel-state language.  Their
result is the right object because the evaporation map is also a Stinespring
channel.  Yoshida and Kitaev use the same OTOC condition in the
Hayden-Preskill recovery problem.

For our purposes, this supplies a statement of the schematic form

```tex
\mathbb E_{C\sim{\rm typ}(m)}
I_2(Q:C)
\le \epsilon_{\rm scr}(N,m,t),
```

where `C` is a typical output subsystem of size `m`.  The exact norm and
averaging convention should be matched to the channel-scrambling theorem being
used.  The important point is that the theorem speaks about most output
partitions, not about a special fixed region.

## Input 2: Boundary-Channel Uniformity

The project-specific condition is that the weak emission Hamiltonian samples
the boundary algebra without repeatedly selecting special channels.

Define

```tex
{\cal A}_{\mu\lambda}(E,\omega)
=
{1\over D_E}
\operatorname{Tr}\!\left[
\Pi_E O_{\mu\lambda}^\dagger(\omega)
\Pi_{E-\omega}O_{\mu\lambda}(\omega)\Pi_E
\right].
```

The required uniformity condition is

```tex
{\cal A}_{\mu\lambda}(E,\omega)
=
{1\over N(E)}{\cal A}_\lambda(E,\omega)
\left[1+o(1)\right],
```

after coarse graining over the relevant microcanonical window.

This is the ETH/subsystem-ETH part of the bridge.  ETH gives smooth local
matrix elements in energy eigenstates and in narrow energy windows.
Subsystem ETH phrases the analogous condition as equality of reduced density
matrices for subsystems at fixed energy.  Applied to equivalent boundary
operators, it supports the claim that no boundary channel is parametrically
preferred.

This input gives

```tex
P_m(\boldsymbol\mu)
\simeq
P_m^{\rm typ}(\boldsymbol\mu),
```

where `P_m^{typ}` is the typical boundary-subsystem sampling measure used in
the channel-scrambling statement.

A sharper way to supply this input is written in
`notes/boundary_channel_uniformity_eth.md`.  The cleanest analytical route is
to choose the boundary labels to be symmetry-related operators in a homogeneous
chaotic shell Hamiltonian.  If

```tex
O_{\mu\lambda}=U_\mu O_{0\lambda}U_\mu^\dagger,
\qquad
[U_\mu,K_N]=0,
```

then `[U_mu,\Pi_E]=0`, and the channel weights are exactly equal:

```tex
{\cal A}_{\mu\lambda}(E,\omega)
=
{\cal A}_{0\lambda}(E,\omega).
```

ETH is then needed only for the common local spectral envelope and the
microcanonical detailed-balance factor.  This is stronger than assuming
uniformity directly.

## Proof Sketch

Let `P_m` be the actual emission-history measure and let `U_m` be the ideal
typical boundary sampling measure.  Suppose

```tex
\|P_m-U_m\|_{\rm TV}\le \delta_m.
```

Then, for any nonnegative bounded information diagnostic `F(mu)`, such as a
normalized second-Renyi mutual information,

```tex
\left|
\mathbb E_{P_m}F-\mathbb E_{U_m}F
\right|
\le
2\|F\|_\infty\delta_m.
```

Channel scrambling gives

```tex
\mathbb E_{U_m} I_2(Q:C_{\boldsymbol\mu})
\le \epsilon_{\rm scr}.
```

Therefore

```tex
\mathbb E_{P_m} I_2(Q:R_{\boldsymbol\mu})
\le
\epsilon_{\rm scr}
+2\|I_2\|_\infty\delta_m.
```

The same argument applies after Page time with the wrong subsystem taken to be
the remaining core:

```tex
\mathbb E_{P_m} I_2(Q:B_{\rm rem}(\boldsymbol\mu))
\le
\epsilon_{\rm scr}^{\rm late}
+2\|I_2\|_\infty\delta_m^{\rm late}.
```

Markov's inequality then gives a typical-history statement.  For example,

```tex
{\rm Prob}\left[
I_2(Q:R_{\boldsymbol\mu})>\eta
\right]
\le
{\epsilon_{\rm scr}+2\|I_2\|_\infty\delta_m\over \eta}.
```

Thus the actual weak-emission histories inherit the channel-scrambling
decoupling theorem when the boundary-channel sampling is close enough to the
typical output sampling measure.

## What This Achieves

This closes the conceptual bridge from fixed Hamiltonian dynamics to
evaporation decoupling, conditional on two recognizable inputs:

```text
channel scrambling for K_N,
ETH-like boundary-channel uniformity for H_I.
```

It avoids requiring `K_N` to be a full approximate design.  The Hamiltonian only
has to scramble the information strongly enough that the emitted boundary
histories are typical output samples.

## What Remains Open

Two technical claims remain.

First, choose a concrete homogeneous `K_N` and cite or prove the required
channel-scrambling bound:

```tex
K_N
\Rightarrow
\epsilon_{\rm scr}(N,m,t_{\rm scr})\to0
```

for `t_scr=O(log N)`.

Second, establish boundary-channel uniformity for the chosen `K_N` and
emission operators:

```tex
{\cal A}_{\mu\lambda}(E,\omega)
\simeq
{1\over N(E)}{\cal A}_\lambda(E,\omega).
```

The second claim is closed if the boundary operators are exactly
symmetry-related; otherwise it is an ETH/subsystem-ETH plus approximate
homogeneity condition.  This split is important: ETH gives local thermality and
channel weights, while OTOC/channel scrambling gives information hiding.

## Literature Inputs

- Hosur, Qi, Roberts, Yoshida, "Chaos in quantum channels,"
  arXiv:1511.04021.
- Yoshida, Kitaev, "Efficient decoding for the Hayden-Preskill protocol,"
  arXiv:1710.03363.
- Dymarsky, Lashkari, Liu, "Subsystem ETH," arXiv:1611.08764.
- D'Alessio, Kafri, Polkovnikov, Rigol, "From quantum chaos and eigenstate
  thermalization to statistical mechanics," Advances in Physics 2016.
- Bentsen, Gu, Lucas, "Fast scrambling on sparse graphs," arXiv:1805.08215.
- Barbon, Magan, "Fast Scramblers, Horizons and Expander Graphs,"
  arXiv:1204.6435.
