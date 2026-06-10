# Weak-Emission ETH Bridge

## Purpose

Replace the abstract decoupling input by a sharper analytical condition for a
fixed shell Hamiltonian.

The target is a bridge from fixed-Hamiltonian data to the decoupling statement
used in the evaporation argument:

```text
sectorwise ETH properties of the weak-emission record algebra
    -> second-moment decoupling for the shrinking evaporation channel.
```

This bridge does not establish ETH for a specific sparse Hamiltonian.  It
states the channel-level properties that such a Hamiltonian would need to
provide.

## Setup

Work in one fixed symmetry sector of one shell

```tex
\mathcal H_E,\qquad \dim\mathcal H_E=D.
```

Let

```tex
K|\nu\rangle=\theta_\nu|\nu\rangle
```

be the in-shell Hamiltonian.  One conditioned emission has normalized jump
operators

```tex
\widehat K_m:\mathcal H_E\to\mathcal H_{E-\omega_m},
\qquad
\sum_m \widehat K_m^\dagger\widehat K_m=I
```

in the shell-averaged Markov limit.  Here

```tex
m=(\omega,\lambda,\mu)
```

collects energy, species/partial-wave labels, and boundary channel labels.

The effective no-jump Hamiltonian is

```tex
H_{\rm eff}=K-\frac{i}{2}J,
\qquad
J=\sum_m L_m^\dagger L_m.
```

When the total decay operator is shell-smooth,

```tex
J=\Gamma(I+F),
\qquad \|F\|_{\rm shell}\ll1,
```

the leading calculation uses `F=0`; corrections are recorded below.
In the flat-rate limit, the physical jump operators can be written as

```tex
L_m=\sqrt{\Gamma}\,\widehat K_m,
\qquad
\sum_m\widehat K_m^\dagger\widehat K_m=I .
```

For `F\ne0`, the exact conditioned channel should be written using the
physical `L_m` and `H_{\rm eff}`.  The normalized `\widehat K_m` description is
the flat-rate leading channel plus controlled smoothness corrections.

## Waiting-Time Dephasing

With `F=0`, the Stinespring isometry for one conditioned emission is

```tex
V|\psi\rangle
=
\sum_m\int_0^\infty dt\,
\sqrt{\Gamma}\,e^{-\Gamma t/2}
\widehat K_m e^{-iKt}|\psi\rangle\otimes |m,t\rangle_R,
```

with

```tex
\langle m,t|m',t'\rangle=\delta_{mm'}\delta(t-t')
```

in the Markov continuum idealization.  This gives

```tex
V^\dagger V=I.
```

Tracing the radiation gives the remaining-core channel

```tex
\Phi^B=\mathcal E\circ\mathcal D_\Gamma,
\qquad
\mathcal E(\sigma)=\sum_m\widehat K_m\sigma\widehat K_m^\dagger,
```

where the waiting-time average is the dephasing channel

```tex
(\mathcal D_\Gamma\sigma)_{\nu\nu'}
=
{\Gamma\over \Gamma+i(\theta_\nu-\theta_{\nu'})}\,
\sigma_{\nu\nu'} .
```

Thus the physical emission process supplies a temporal average.  It does not
project only onto exact resonances; near-resonant coherences with

```tex
|\theta_\nu-\theta_{\nu'}|\lesssim \Gamma
```

survive with order-one weight.

## Remaining-Core Branch

Let `Q` purify the input code state.  Decompose

```tex
\mathcal D_\Gamma(\rho_{QB})=\bar\rho_{QB}+\rho_w,
```

where

```tex
\bar\rho_{QB}
=
\sum_\nu \rho^Q_{\nu\nu}\otimes|\nu\rangle\langle\nu|
```

is diagonal in the `K` eigenbasis, and `\rho_w` is the Lorentzian-filtered
coherence part.

The coherence contribution is controlled by

```tex
\|\rho_w\|_2^2
=
\sum_{\nu\ne\nu'}
{\Gamma^2\over \Gamma^2+(\theta_\nu-\theta_{\nu'})^2}
\|\rho^Q_{\nu\nu'}\|_2^2 .
```

For a code class `\mathcal C`, define the near-resonance weight

```tex
\eta_\Gamma(\mathcal C)
=
\sup_{\rho_{QB}\in\mathcal C}
{
\sum_{\nu\ne\nu'}
{\Gamma^2\over \Gamma^2+(\theta_\nu-\theta_{\nu'})^2}
\|\rho^Q_{\nu\nu'}\|_2^2
\over
\sum_{\nu\ne\nu'}\|\rho^Q_{\nu\nu'}\|_2^2
}.
```

This is the correct place for level statistics and code-class restrictions.
A code deliberately supported on near-resonant pairs can evade dephasing.

For the diagonal part, define the emission image of an eigenstate:

```tex
\rho'(\nu)
=
\mathcal E(|\nu\rangle\langle\nu|)
=
\sum_m\widehat K_m|\nu\rangle\langle\nu|\widehat K_m^\dagger .
```

Then

```tex
\operatorname{Tr}[\mathcal E(\bar\rho_{QB})^2]
=
\sum_{\nu\nu'}
\operatorname{Tr}_Q[\rho^Q_{\nu\nu}\rho^Q_{\nu'\nu'}]\,
G_{\nu\nu'},
```

where the emission-image overlap kernel is

```tex
G_{\nu\nu'}
=
\operatorname{Tr}_{B'}[\rho'(\nu)\rho'(\nu')].
```

The post-Page remaining-core decoupling condition is that, after exact charges
are fixed or recorded, the kernel is close to its microcanonical value:

```tex
G_{\nu\nu'}=
G_{\rm mc}+\delta G_{\nu\nu'},
\qquad
G_{\rm mc}\simeq \operatorname{Tr}\bar\rho_{B'}^2 .
```

This is operational/subsystem ETH for the weak-emission channel.  It says that
same-shell eigenstates are not distinguishable through their remaining-core
emission images.

## Complementary Radiation Branch

The complementary channel keeps the radiation record:

```tex
\Phi^R(\sigma)
=
\operatorname{Tr}_{B'}[V\sigma V^\dagger].
```

On eigenbasis matrix units,

```tex
\Phi^R(|\nu\rangle\langle\nu'|)
=
\sum_{mm'}\int dt\,dt'\,
\Gamma e^{-\Gamma(t+t')/2}
e^{-i\theta_\nu t+i\theta_{\nu'}t'}
\langle\nu'|\widehat K_{m'}^\dagger\widehat K_m|\nu\rangle
|m,t\rangle\langle m',t'|.
```

For a purified input, the second purity has the form

```tex
\operatorname{Tr}\rho_{QR}^2
=
\sum_{\nu_1\nu_2\nu_3\nu_4}
\mathcal L(\theta_{\nu_4}-\theta_{\nu_1})
\mathcal L(\theta_{\nu_2}-\theta_{\nu_3})
\operatorname{Tr}_Q[
\rho^Q_{\nu_1\nu_2}\rho^Q_{\nu_3\nu_4}]
\sum_{mm'}
M_{\nu_2\nu_1}^{m'm}M_{\nu_4\nu_3}^{mm'},
```

with

```tex
\mathcal L(\Delta)={\Gamma\over \Gamma+i\Delta},
\qquad
M_{\nu'\nu}^{m'm}
=
\langle\nu'|\widehat K_{m'}^\dagger\widehat K_m|\nu\rangle .
```

The Lorentzian pairings are complementary to the remaining-core branch.  The
same kernel appears:

```tex
\sum_{mm'}
\left|
\langle\nu'|\widehat K_{m'}^\dagger\widehat K_m|\nu\rangle
\right|^2
=
\operatorname{Tr}[\rho'(\nu)\rho'(\nu')]
=
G_{\nu\nu'}.
```

Thus `G_{\nu\nu'}` is the shared second-moment object.  On the remaining-core
side, its eigenstate-independence gives post-Page decoupling of `Q` from
`B'`.  On the radiation side, its smallness controls how much coherence of the
input can be imprinted in early radiation.

## Record-Signature Leakage

The radiation branch also contains diagonal record signatures

```tex
a_{mm'}(\nu)
=
\langle\nu|\widehat K_{m'}^\dagger\widehat K_m|\nu\rangle .
```

Early radiation can distinguish code states if these vectors vary across
`\nu`.  The smoothness condition is

```tex
\|a(\nu)-a(\nu')\|^2 \ll 1
```

in the code-relevant shell window, with the cumulative pre-Page budget

```tex
\sum_{j<j_{\rm Page}}
\operatorname{Var}_{\rm code,j}[a_j]
\ll 1.
```

The timing-record condition is the diagonal subcase.  If

```tex
\Gamma_\nu=\Gamma(1+F_{\nu\nu}),
```

then one arrival time has

```tex
D_{\rm KL}(\nu\|\nu')
=
\log{\Gamma_\nu\over\Gamma_{\nu'}}
 +{\Gamma_{\nu'}\over\Gamma_\nu}-1
\simeq
{1\over2}(F_{\nu\nu}-F_{\nu'\nu'})^2 .
```

Since there are `O(S)` microscopic emissions before Page time in the
Schwarzschild scaling, a sufficient timing-smoothness condition is

```tex
\operatorname{Var}_{\rm shell}(F_{\nu\nu})\ll {1\over S}.
```

For coarse-grained emission blocks, `S` should be replaced by the number of
recorded blocks before Page time.

## Conditions Produced By The Calculation

The one-step analysis reduces the deterministic mixing input to three
sectorwise conditions.

### 1. Diagonal ETH of the record algebra

The operators

```tex
\widehat K_{m'}^\dagger\widehat K_m
```

must have smooth diagonal matrix elements in the `K` eigenbasis, within each
fixed symmetry sector and after exact charges are accounted for.  This controls
branch weights, channel-coherence signatures, and timing leakage.

### 2. Second-moment smoothness of the same algebra

The emission-image overlap kernel must satisfy

```tex
G_{\nu\nu'}
=
G_{\rm mc}+\delta G_{\nu\nu'},
\qquad
|\delta G_{\nu\nu'}|\le \epsilon_2
```

for code-relevant eigenstates.  This is the shared condition for the two Page
branches.

### 3. Lorentzian near-resonance control

The code class transported through the evaporation should not concentrate its
coherences in pairs with

```tex
|\theta_\nu-\theta_{\nu'}|\lesssim \Gamma .
```

This is quantified by `\eta_\Gamma(\mathcal C)`.  Iteration requires the
output code distribution in shell `j+1` to remain non-concentrated on the
near-resonant subspace of `K_{j+1}`.

## Iteration Target

For the remaining-core branch after Page time, the desired iterative estimate
has the form

```tex
I_2(Q:B_{j+1})
\le
\kappa_j I_2(Q:B_j)
+ C_1\epsilon_{2,j}
+ C_2\eta_{\Gamma,j}
+ C_3\epsilon_{F,j}.
```

Here:

```text
kappa_j
    is the dimension-drop/Haar benchmark factor, corrected by the
    microcanonical shell weights;

epsilon_2,j
    measures the deviation of G_{\nu\nu'} and record signatures from their
    microcanonical values;

eta_Gamma,j
    measures near-resonant coherent weight surviving waiting-time dephasing;

epsilon_F,j
    measures total-rate roughness and off-diagonal decay-operator corrections.
```

For the pre-Page radiation branch, the estimate is cumulative rather than
contractive:

```tex
I_2(Q:R_{\le j})
\le
\sum_{\ell\le j}
\left(
C_1'\epsilon_{{\rm rec},\ell}
+ C_2'\eta_{\Gamma,\ell}
+ C_3'\epsilon_{F,\ell}
\right),
\qquad j<j_{\rm Page}.
```

This reflects the fact that early radiation records accumulate and are not
re-suppressed by later dimension drops.

## Role Of Cayley Symmetry

For symmetry-related boundary operators,

```tex
O_{ag,\lambda}=U_aO_{g,\lambda}U_a^\dagger,
```

the total decay operator and record algebra are group-invariant sums.  They lie
in the commutant of the group action.  By Schur decomposition,

```tex
J=\bigoplus_\alpha I_{d_\alpha}\otimes \widetilde J_\alpha,
\qquad
K=\bigoplus_\alpha I_{d_\alpha}\otimes \widetilde K_\alpha .
```

Thus symmetry removes systematic variation along irrep dimensions and reduces
the problem to multiplicity spaces.  It does not prove ETH in those
multiplicity spaces.  The chaotic part remains a dynamical condition on
`\widetilde K_\alpha` and the projected record algebra.

## Remaining Technical Items

Before this is paper-ready, four details need a clean pass.

1. Markov record orthogonality:
   bound corrections to
   `\langle m,t|m',t'\rangle=\delta_{mm'}\delta(t-t')`
   from finite bath correlation time.

2. Off-diagonal decay operator:
   write an explicit norm estimate for `F_{\rm od}` in the effective
   Hamiltonian expansion.

3. Constants:
   define the effective record dimension and microcanonical benchmark
   `G_{\rm mc}` precisely for energy-resolved channels.

4. Iteration:
   assemble the one-step estimates into a shrinking-shell theorem with
   explicit `\kappa_j` and accumulated pre-Page leakage.

## Current Status

For a fixed shell Hamiltonian, the same information-flow result has a
sufficient route: sectorwise diagonal ETH for the weak-emission record algebra,
sectorwise second-moment smoothness for the emission-image kernel, and
near-resonance control in the relevant code class.

This does not prove that a specific Cayley-expander Hamiltonian has those
properties.  It identifies the concrete conditions to prove analytically or
test by scaling analysis.
