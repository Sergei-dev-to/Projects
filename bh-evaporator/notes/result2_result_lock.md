# Result 2 Result Lock

## Purpose

This note states the current result without draft history and without trying to
polish the paper.  The goal is to identify what is actually supported by the
Hamiltonian calculation and what remains an input.

## Hamiltonian Class

The model is a non-gravitational Hamiltonian

```tex
H_{\rm tot}=H_{\rm B}^{(0)}+H_{\rm mix}+H_{\rm R}+H_I .
```

The black-hole-like subsystem has microcanonical shells

```tex
{\cal H}_{E}, \qquad D_E=\dim{\cal H}_E,
        \qquad S_{\rm micro}(E)=\log D_E\simeq cE^2 .
```

The outgoing radiation is a continuum of modes.  The interaction is weak and
energy conserving in the golden-rule regime.  In the strengthened version, the
Schwarzschild state count is represented by `N(E)` boundary-accessible cells of
local Hilbert-space dimension `q`,

```tex
S_{\rm micro}(E)\simeq N(E)\log q.
```

The interaction is a sum of local weak emission operators on those active
boundary cells,

```tex
H_I =
g\sum_{x=1}^{N(E)}\sum_{\lambda}\int d\omega\, \omega^{p/2}
\left[
O_{x\lambda}(\omega)b^\dagger_{x\lambda}(\omega)
+{\rm h.c.}
\right].
```

Here `lambda` labels outgoing radiation species/channels, while `x` labels
boundary-accessible emission operators.  For four-dimensional Schwarzschild
evaporation,

```tex
S_{\rm micro}(E)\sim A(E)\sim E^2,\qquad p=2.
```

The in-shell mixing is strong enough to supply the required decoupling moments
for the composite emission map.  A sufficient implementation is an approximate
design, tensor-product expander, or a Hamiltonian-design construction on each
active shell.

## Main Conditional Result

Given the Hamiltonian class above, the exterior Schwarzschild evaporation
package follows:

```text
S_micro(E) ~ E^2
    -> beta(E)=dS/dE ~ E
    -> T(E) ~ 1/E
    -> negative heat capacity.
```

The density-of-states ratio gives

```tex
{D_{E-\omega}\over D_E}
=
\exp[S_{\rm micro}(E-\omega)-S_{\rm micro}(E)]
=
\exp[-\beta(E)\omega+c\omega^2+\cdots].
```

Thus the local radiation spectrum is thermal at the instantaneous Hawking
temperature, with the leading finite-energy correction.

The boundary operator count gives the Schwarzschild rate law.  Since

```tex
N(E)\simeq {S_{\rm micro}(E)\over\log q}\propto A(E),
```

the inclusive weak emission strength is area-sized:

```text
Gamma_quanta ~ N(E) T^3 ~ E^2 E^{-3} ~ E^{-1},
P             ~ N(E) T^4 ~ E^2 E^{-4} ~ E^{-2},
tau           ~ int dE E^2 ~ E_0^3.
```

The Page/island entropy formula follows from global purity plus decoupling of
the composite emission isometry:

```tex
S_{\rm vN}(R;E)
=
\min\{S_{\rm micro}(E_0)-S_{\rm micro}(E),\,S_{\rm micro}(E)\}
+O(1).
```

Late radiation is correlated with early radiation after the Page time because
the purifier of a late block is mostly in the early radiation once the
remaining core is the smaller Hilbert-space factor.

## Operator-Counting Form of the Area Rule

The area factor is now an operator-counting consequence of the boundary-access
assumption.

For a microcanonical shell transition `E -> E-omega`, define the inclusive
spectral weight

```tex
{\cal A}_\lambda(E,\omega)
=
{1\over D_E}
\sum_{x=1}^{N(E)}
\operatorname{Tr}\!\left[
\Pi_E O_{x\lambda}^\dagger(\omega)
\Pi_{E-\omega}
O_{x\lambda}(\omega)\Pi_E
\right].
```

If the emission operators are independent in the shell average,

```tex
{1\over D_E}
\operatorname{Tr}\!\left[
\Pi_E O_{x\lambda}^\dagger
\Pi_{E-\omega}
O_{y\lambda}\Pi_E
\right]
\simeq
\delta_{xy}
C_\lambda(E,\omega)
{D_{E-\omega}\over D_E},
```

then

```tex
{\cal A}_\lambda(E,\omega)
\simeq
N(E) C_\lambda(E,\omega)
{D_{E-\omega}\over D_E}.
```

The golden-rule spectrum is therefore

```tex
{d\Gamma\over d\omega}
\propto
g^2\omega^p
N(E) C_\lambda(E,\omega)
\exp[S_{\rm micro}(E-\omega)-S_{\rm micro}(E)].
```

Because the entropy is stored in boundary-accessible cells,

```text
N(E) ~ S_micro(E) ~ A(E)
```

and the area emission factor follows from the Hamiltonian operator count.
The rate law follows from this operator count, ordinary phase space, and the
DOS ratio.

If only order-one boundary cells couple efficiently, the same calculation in
three spatial dimensions
gives

```text
P ~ T^4 ~ E^-4,
```

so the Schwarzschild power law needs area-sized inclusive emission strength.

## Renyi-2 Island/Replica Structure

For a narrow trajectory from `E_0` to `E`, define

```tex
b=D_B(E)=\exp S_{\rm micro}(E),
\qquad
r=D_R(E)=\exp\Delta S_{\rm rad}(E),
```

where

```tex
\Delta S_{\rm rad}(E)=S_{\rm micro}(E_0)-S_{\rm micro}(E).
```

Under the shell-decoupling/design condition, the composite map is typical on

```tex
{\cal H}_{E_0}\to{\cal H}_B(E)\otimes{\cal H}_R(E).
```

For a Haar-typical pure state on `B R`,

```tex
\mathbb E\,{\rm Tr}\,\rho_R^2
=
{b+r\over br+1}
=
{1\over r}+{1\over b}+O((br)^{-1}).
```

Thus

```tex
S_2(R)
=
-\log{\rm Tr}\rho_R^2
\simeq
-\log\left(e^{-\Delta S_{\rm rad}(E)}
          +e^{-S_{\rm micro}(E)}\right).
```

Away from the Page crossing,

```tex
S_2(R)
=
\min\{\Delta S_{\rm rad}(E),S_{\rm micro}(E)\}
+O(1).
```

Interpretation:

```text
e^{-Delta S_rad}       = no-island/Hawking contraction,
e^{-S_micro(E)}        = island/QES contraction.
```

The post-Page contribution is a non-geometric replica contraction through the
smaller remaining core Hilbert space.  This reproduces the algebraic island
saddle exchange for the radiation entropy.  It does not produce a geometric
replica wormhole or an interior.

## Fixed Higher Renyi Moments

For a Haar-typical pure state on `B R`,

```tex
\mathbb E\,{\rm Tr}\rho_R^n
=
{1\over (br)_n}
\sum_{\sigma\in S_n}
b^{C(\sigma)}r^{C(\tau\sigma)},
```

where `tau=(12...n)` is the cyclic permutation imposed by
`Tr rho_R^n`.  The two leading contractions are:

```text
sigma = identity
    -> r^{1-n}
    -> S_n(R) ~ log r
    -> no-island branch.

sigma = tau^{-1}
    -> b^{1-n}
    -> S_n(R) ~ log b
    -> island branch.
```

For fixed `n`, an approximate unitary `n`-design or corresponding
tensor-product-expander moment reproduces this leading moment calculation up
to design error.  The second-Renyi/Page-purity statement only needs the second
moment.

## Weighted Hawking Histories

The flat radiation-support formula is the equiprobable special case.  In the
Hamiltonian, a radiation history `alpha` includes emitted energies, channels,
and time bins, with probability

```tex
p_\alpha=\prod_{\rm steps}p({\rm step}\mid{\rm previous\ shell}).
```

The probabilities are supplied by the weak-coupling rates: the density-of-states
ratio fixes the Boltzmann weight and finite-energy correction, while the
boundary operator count fixes the inclusive channel strength.

For a random purification of this weighted history distribution,

```tex
\mathbb E\,{\rm Tr}\rho_R^n
\simeq
\sum_{\sigma\in S_n}
b^{C(\sigma)-n}
\prod_{c\in{\rm cycles}(\tau\sigma)}
{\rm Tr}\,p^{|c|}.
```

The leading contractions are:

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

Thus the no-island branch is the Renyi entropy of the emitted Hawking history
distribution, and the island branch is still the remaining core state count.
At second Renyi order,

```tex
\mathbb E\,{\rm Tr}\rho_R^2
\simeq
{\rm Tr}\,p^2+e^{-S_{\rm micro}(E)}.
```

This is the strongest current island/replica statement: the algebraic
island/no-island contraction exchange survives the nonuniform Hawking weights.

## What Is Still Input

The current result does not derive:

```text
S_micro(E) ~ E^2,
the boundary-accessible realization of that state count,
the required shell decoupling from a simple deterministic constant-local Hamiltonian.
```

It does show that, once the Schwarzschild state count is boundary-accessible,
the area emission law follows from local weak coupling.  With shell decoupling, the exterior evaporation
phenomenology follows by standard weak-coupling, microcanonical, and
decoupling arguments.

## What Would Be More Interesting

The next possible improvements are:

1. Derive boundary-accessible `S_micro(E) ~ E^2` from a simpler
   non-gravitational many-body spectrum.
2. Replace the design/TPE shell mixer by a simple deterministic many-body
   Hamiltonian with a cited or proven decoupling property for the evaporation
   partitions.

The first is the hard microscopic-origin problem.  The second is attractive
but currently lacks a direct off-the-shelf theorem for a simple deterministic
expander-spin Hamiltonian.

The spectrum problem has been narrowed.  A plausible microscopic target is:

```tex
E\sim K,\qquad S_{\rm accessible}(K)\sim K^2,
```

with the `K^2` states carried by connector or matrix-block labels and with
emission branches of energy

```tex
\omega\sim 1/K.
```

This avoids treating one Hawking quantum as a whole `K -> K-1` clump-removal
event.  One typical quantum removes order-one entropy/area, while the
macroscopic size changes by order `1/K`.

The mixer problem has also been narrowed.  The direct target is not a full
global design; it is decoupling:

```tex
I(Q:R_{\rm early})\simeq 0
```

before Page time, and

```tex
I(Q:B_{\rm rem})\simeq 0
```

after Page time, for the code subspace being tested.  Approximate designs and
TPEs are sufficient.  Expander or treelike fast-scrambling Hamiltonians are
the leading deterministic candidates, but the needed quantitative decoupling
bound for the evaporation partitions is still open.

The most promising fixed-Hamiltonian route is a deterministic expander mixer

```tex
K_N
=
\sum_{(ij)\in G_N}
\left(J_xX_iX_j+J_yY_iY_j+J_zZ_iZ_j\right)
+\sum_i(h_xX_i+h_z(i)Z_i),
```

with `G_N` a fixed bounded-degree expander on the active boundary degrees of
freedom.  Existing fast-scrambling work supports the route

```tex
{\rm expander/sparse\ graph}
\to
{\rm OTOC/operator\ spreading}
\to
{\rm channel\ scrambling}.
```

The useful extra observation is that the radiation subsystem is sampled by the
emission channel labels, not selected as an arbitrary fixed graph region.  If
the area-sized boundary channels sample typical output partitions after each
scrambling block, the channel-scrambling literature's "most output partitions"
statements may apply directly to the evaporation map.  The remaining theorem
would be:

```tex
K_N{\rm\ gives\ channel\ scrambling}
+{\rm typical\ boundary\ channel\ sampling}
\Rightarrow
I_2(Q:X_{\rm wrong})\ll1.
```

Equivalently, if `P_m` is the distribution of emitted boundary-channel
histories, the target is

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:R_{\boldsymbol\mu})\ll1
```

before Page time, and

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:B_{\rm rem}(\boldsymbol\mu))\ll1
```

after Page time.  Typical-history decoupling then follows by Markov's
inequality.

This is the sharpest current fixed-Hamiltonian target.

Current property check:

```text
fixed Hamiltonian status                  passes
expander fast graph geometry              passes at graph level
absence of obvious integrability          plausible by construction
fast OTOC/operator spreading for K_N       supported, not proved
OTOC to channel decoupling                 supplied by channel-scrambling literature
boundary-channel sampling                  promising and specific to this model
uniformity of sampled boundary channels    open
many-block error composition               open
```

Thus the fixed-Hamiltonian program has two concrete analytical gaps:

```tex
K_N\to{\rm OTOC/channel\ scrambling},
```

and

```tex
H_I{\rm\ samples\ typical\ boundary\ partitions}
```

under shell averaging.  Closing both would replace the abstract mixing
assumption by the deterministic expander Hamiltonian.
