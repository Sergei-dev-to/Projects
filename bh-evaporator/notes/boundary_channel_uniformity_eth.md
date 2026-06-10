# Boundary-Channel Uniformity From ETH

## Purpose

The fixed-Hamiltonian bridge needs the weak emission channel to sample the
area-sized boundary algebra without repeatedly selecting special channels.
The target condition is

```tex
{\cal A}_{\mu\lambda}(E,\omega)
\simeq
{1\over N(E)}{\cal A}_{\lambda}(E,\omega),
```

where

```tex
{\cal A}_{\mu\lambda}(E,\omega)
=
{1\over D_E}
\operatorname{Tr}\!\left[
\Pi_E O_{\mu\lambda}^{\dagger}(\omega)
\Pi_{E-\omega}O_{\mu\lambda}(\omega)\Pi_E
\right].
```

This note checks how much of this follows from ETH and what extra structure is
needed.

## What Standard ETH Gives

For a physical few-body operator `O_mu`, the ETH ansatz in the energy basis is

```tex
\langle a|O_\mu|b\rangle
=
O_\mu(\bar E)\delta_{ab}
+e^{-S(\bar E)/2}
f_\mu(\bar E,\omega)R^{(\mu)}_{ab},
```

with

```tex
\bar E={E_a+E_b\over 2},
\qquad
\omega=E_a-E_b.
```

Here `f_mu` is a smooth spectral function and `R_ab` is an order-one erratic
matrix.  The standard ETH review literature treats this as the mechanism by
which local observables relax to microcanonical values.  Subsystem ETH states
the same idea at the level of reduced density matrices of small subsystems.

For a transition `E -> E-omega`, ETH therefore gives the shell-averaged
spectral weight

```tex
{\cal A}_{\mu\lambda}(E,\omega)
\sim
e^{S(E-\omega)-S(\bar E)}
\left|f_{\mu\lambda}(\bar E,\omega)\right|^2,
```

up to smooth prefactors and coarse-graining conventions.  Since
`S(\bar E)=S(E-\omega/2)`, expanding at small `omega/E` gives the usual
density-of-states factor:

```tex
{\cal A}_{\mu\lambda}(E,\omega)
\propto
e^{S(E-\omega)-S(E)}
\times
{\rm smooth}(E,\omega).
```

Thus ETH supplies:

```text
smooth transition weights,
microcanonical detailed balance,
the DOS-ratio thermal factor,
small fluctuations after shell averaging.
```

This is exactly the part needed for local thermality.

## What ETH Does Not Give By Itself

ETH does not automatically imply

```tex
f_{\mu\lambda}(E,\omega)
\simeq
f_{\nu\lambda}(E,\omega)
```

for every pair of boundary labels `mu,nu`.

The reason is simple: ETH applies to a chosen physical operator.  Different
operators can have different spectral functions.  Therefore ETH alone gives

```tex
{\cal A}_{\mu\lambda}(E,\omega)
\simeq
C_{\mu\lambda}(E,\omega)
{D_{E-\omega}\over D_E},
```

with smooth `C_{\mu\lambda}`, but it does not force
`C_{\mu\lambda}` to be independent of `mu`.

So boundary-channel uniformity needs one additional ingredient.

## Three Ways To Get Uniformity

### Option A: Exact boundary homogeneity

Choose `K_N` and the emission operators so that the boundary labels are related
by an exact automorphism or group action:

```tex
O_{\mu\lambda}=U_\mu O_{0\lambda}U_\mu^\dagger,
\qquad
[U_\mu,K_N]=0.
```

Then the microcanonical projector commutes with the same action,

```tex
[U_\mu,\Pi_E]=0,
```

and all channel weights are equal:

```tex
{\cal A}_{\mu\lambda}(E,\omega)
=
{\cal A}_{0\lambda}(E,\omega).
```

This is the strongest route.  A Cayley expander or other vertex-transitive
expander is a natural graph candidate.

Cost: exact homogeneity introduces symmetry sectors.  The model must either
work inside fixed symmetry sectors or include a symmetry-respecting chaotic
Hamiltonian.  Symmetry is not fatal, but it has to be tracked.

### Option B: Approximate boundary homogeneity

Use a deterministic expander with local environments that become
asymptotically equivalent as `N` grows, and choose boundary operators of the
same local form.  Then require

```tex
\max_\mu
\left|
{C_{\mu\lambda}(E,\omega)\over \bar C_\lambda(E,\omega)}
-1
\right|
\to 0
```

after microcanonical coarse graining.

This is weaker than exact symmetry and more compatible with generic
nonintegrability.  It is also less theorem-backed.  It would likely need a
separate ETH-plus-graph-homogeneity argument.

### Option C: Uniform operator basis coupling

Instead of coupling radiation to geometrically named sites, couple it to an
orthonormal set of boundary operators with equal Hilbert-Schmidt norm:

```tex
\operatorname{Tr}(O_\mu^\dagger O_\nu)\propto\delta_{\mu\nu}.
```

The inclusive emission channel is then uniform by construction over an operator
basis of the boundary algebra, while ETH supplies the common smooth
microcanonical envelope.

Cost: this is more abstract.  It is still Hamiltonian and non-gravitational,
but it is closer to the theorem-backed model than to a simple spatial spin
Hamiltonian.

## Best Choice For Gap 2

For a fixed deterministic Hamiltonian, Option A is the sharpest analytical
route:

```text
vertex-transitive expander / Cayley graph
    -> exact equality of boundary-channel weights by symmetry,
chaotic homogeneous spin Hamiltonian
    -> ETH for the common local boundary operator,
OTOC/channel scrambling
    -> Page decoupling for typical emitted histories.
```

This replaces the loose condition

```text
boundary channels are roughly uniform
```

with a structural condition:

```text
boundary channels are symmetry-related operators in a homogeneous chaotic
Hamiltonian.
```

That is much better.  It also identifies the fixed-Hamiltonian candidate more
precisely:

```tex
K_N
=
\sum_{(ij)\in G_N}
(J_xX_iX_j+J_yY_iY_j+J_zZ_iZ_j)
+\sum_i(h_xX_i+h_zZ_i),
```

where `G_N` is a vertex-transitive expander and the fields are homogeneous or
otherwise symmetry-respecting.  Any remaining global symmetry sectors should be
projected out or treated explicitly.

The earlier idea of adding arbitrary deterministic inhomogeneous fields helps
break accidental degeneracies, but it weakens the cleanest uniformity
argument.  For this gap, homogeneity is more valuable than arbitrary
inhomogeneity.

## Consequence For The Bridge Lemma

The bridge lemma can now use the following stronger hypothesis:

```text
Boundary-channel uniformity follows from symmetry-related emission operators
plus ETH for the common local operator.
```

Then the only genuinely hard part left in Gap 2 is:

```text
prove or cite channel scrambling / OTOC decay for the chosen homogeneous
expander Hamiltonian.
```

## Sources

- Srednicki, "Chaos and quantum thermalization," Phys. Rev. E 1994.
- D'Alessio, Kafri, Polkovnikov, Rigol, "From quantum chaos and eigenstate
  thermalization to statistical mechanics," Advances in Physics 2016.
- Dymarsky, Lashkari, Liu, "Subsystem ETH," arXiv:1611.08764.
- Bentsen, Gu, Lucas, "Fast scrambling on sparse graphs," arXiv:1805.08215.
