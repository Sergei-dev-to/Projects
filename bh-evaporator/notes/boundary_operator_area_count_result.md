# Boundary Operator Count Result

Successor correction (2026-07-09): this note supplies a preferred local
boundary-cell decomposition and orthogonal/incoherent exterior coupling as
model structure.  Its `N_A ~ A` count is valid within that canonical
realization, but it is not reconstructed from exterior data and is not
invariant under arbitrary compensating refactorizations of source and exterior
operators.  See `source_gram_invariance_audit.md`.  An anomalous parametric
channel also supplies a Hawking-flux mimic outside the passive local-emitter
class; see `anomalous_parametric_channel_result.md`.

## Question

Can the area-sized emission strength

```tex
N_A(E)\sim A(E)
```

be obtained from a simple Hamiltonian structure, rather than inserted as an
independent total-rate rule?

## Short Answer

Yes, if the Schwarzschild state count is realized by boundary-accessible
degrees of freedom.

The useful structure is:

```text
microcanonical entropy = number of active boundary cells,
emission Hamiltonian   = sum of local weak emitters on those cells,
outgoing modes         = independent or incoherently summed channels.
```

Then the inclusive golden-rule rate automatically carries one power of the
number of boundary cells.  Since the boundary cell count is proportional to
area, the area emission factor follows from operator counting.

This does not derive the existence of the boundary-cell Hilbert space from a
deeper non-gravitational system.  It reduces the previous two macroscopic
inputs,

```text
S(E) ~ A(E),        N_A(E) ~ A(E),
```

to one stronger microscopic-looking input:

```text
the entropy is stored in area-many boundary-accessible degrees of freedom,
and each active boundary degree has O(1) weak access to radiation.
```

## Boundary Hilbert-Space Realization

Let the active shell at energy `E` be represented, up to subexponential factors,
by `N(E)` boundary cells of local Hilbert-space dimension `q`:

```tex
{\cal H}_E \simeq {\cal K}_E \otimes
\bigotimes_{x=1}^{N(E)}{\cal h}_x,
\qquad \dim{\cal h}_x=q.
```

The leading entropy is

```tex
S_{\rm micro}(E)=\log\dim{\cal H}_E
\simeq N(E)\log q.
```

If this is the Schwarzschild entropy, then

```tex
N(E)\simeq {S_{\rm micro}(E)\over\log q}\propto A(E).
```

For four-dimensional Schwarzschild scaling,

```tex
S_{\rm micro}(E)\sim A(E)\sim E^2,
```

so

```tex
N(E)\sim E^2.
```

This is the familiar horizon-qubit picture, stated as a Hamiltonian
bookkeeping assumption rather than as a literal geometric claim.

## Local Boundary Emission Hamiltonian

Couple each active boundary cell to outgoing radiation through local operators
`O_{x\lambda}`:

```tex
H_I
=
g\sum_{x=1}^{N(E)}
\sum_\lambda\int_0^\infty d\omega\,
\omega^{p/2}
\left[
O_{x\lambda}(\omega)b^\dagger_{x\lambda}(\omega)
+{\rm h.c.}
\right].
```

Here:

```text
x       = active boundary cell,
lambda  = species/angular/polarization label,
b_x     = outgoing channel associated with boundary cell x, or an orthogonal
          wavepacket/channel basis whose inclusive sum resolves the boundary.
```

The model only needs the inclusive weak-coupling rate.  The emitted channels
may be spatial wavepackets, partial-wave combinations, or any orthogonal
outgoing lead basis.  The key condition is that probabilities from different
boundary cells add in the inclusive rate.

## Inclusive Spectral Weight

Define the shell spectral weight

```tex
{\cal A}_{\lambda}(E,\omega)
=
{1\over D_E}
\sum_{x=1}^{N(E)}
\operatorname{Tr}\!\left[
\Pi_E O^\dagger_{x\lambda}(\omega)
\Pi_{E-\omega}
O_{x\lambda}(\omega)\Pi_E
\right].
```

For a scrambled shell, local boundary operators have ETH-like shell-averaged
matrix elements.  If the active boundary cells are statistically equivalent,

```tex
{1\over D_E}
\operatorname{Tr}\!\left[
\Pi_E O^\dagger_{x\lambda}
\Pi_{E-\omega}
O_{x\lambda}\Pi_E
\right]
\simeq
C_\lambda(E,\omega)
{D_{E-\omega}\over D_E}.
```

Then

```tex
{\cal A}_{\lambda}(E,\omega)
\simeq
N(E) C_\lambda(E,\omega)
{D_{E-\omega}\over D_E}.
```

Since `N(E) proportional A(E)`, this gives the desired area-sized inclusive
emission strength.

Equivalently,

```tex
N_A(E)=N(E)\simeq {S_{\rm micro}(E)\over\log q}\propto A(E).
```

## Rate Law

The golden-rule spectrum becomes

```tex
{d\Gamma\over d\omega}
\propto
g^2
N(E)
\omega^p
C_\lambda(E,\omega)
\exp[S_{\rm micro}(E-\omega)-S_{\rm micro}(E)].
```

In the local thermal limit,

```tex
{d\Gamma\over d\omega}
\propto
N(E)\omega^p e^{-\beta(E)\omega}.
```

For a four-dimensional Schwarzschild evaporator,

```tex
N(E)\sim A(E)\sim E^2,\qquad
\beta(E)\sim E,\qquad
p=2.
```

Thus

```tex
\Gamma_{\rm quanta}
\sim
N(E)\int d\omega\,\omega^2 e^{-\beta\omega}
\sim
E^2 E^{-3}
\sim
E^{-1},
```

and

```tex
P
\sim
N(E)\int d\omega\,\omega^3 e^{-\beta\omega}
\sim
E^2 E^{-4}
\sim
E^{-2}.
```

The lifetime is

```tex
\tau\sim\int^{E_0} dE\,E^2\sim E_0^3.
```

## What Was Improved

Before this step, the model had two explicit black-hole-like inputs:

```text
1. S_micro(E) ~ E^2,
2. N_A(E) ~ A(E).
```

After this step, the area emission rule can be replaced by a more microscopic
boundary-access condition:

```text
1. the entropy is carried by N(E) boundary cells,
2. each active boundary cell has an O(1) weak emission operator,
3. the inclusive rate sums probabilities over cells.
```

Then

```tex
N_A(E)\sim N(E)\sim S_{\rm micro}(E)\sim A(E).
```

This is a real strengthening because the Schwarzschild power law no longer
requires assigning the total rate.  It follows from local weak coupling to an
area-sized boundary operator algebra.

## Conditions That Matter

### Independent or Incoherent Inclusive Sum

The area scaling requires probabilities to add:

```tex
\sum_x |M_x|^2.
```

This holds if the outgoing channels are orthogonal, if phases are effectively
random under shell averaging, or if one computes the inclusive absorption rate
in an orthogonal channel basis.

If all boundary cells couple coherently to the same outgoing mode with locked
phases, the amplitude sum

```tex
\left|\sum_x M_x\right|^2
```

can scale differently.  That is a different coupling regime.

### O(1) Local Spectral Weight

Each active boundary cell must have shell-averaged matrix elements of comparable
size.  If only `O(1)` cells couple efficiently, the power law returns to

```tex
P\sim E^{-4}
```

in three spatial dimensions.

### Boundary Accessibility

The state count must be accessible to the emission operators.  A system can
have `S(E)~E^2` but hide most states in modes that do not couple to the
radiation channel.  Then the rate law need not be Schwarzschild-like.

Thus the strengthened input is not merely large entropy.  It is large entropy
stored in boundary-accessible degrees of freedom.

## Relation to Black-Hole Literature

The gravitational fact being mirrored is the low-energy absorption result:
for minimally coupled massless scalars, the low-frequency absorption
cross-section equals the horizon area.  In the Hamiltonian model, the analogue
is that the inclusive low-energy spectral weight of the boundary emission
operators is proportional to the number of active boundary cells.

The membrane-paradigm intuition is similar: exterior fields interact with an
effective stretched-horizon surface, so low-energy absorption is governed by a
surface response rather than a volume response.  The present model does not
use a geometric horizon.  It uses a boundary operator algebra whose size scales
like the entropy.

## Result-Level Status

This does not solve the hardest microscopic problem:

```text
derive S_micro(E) ~ E^2 from a simple non-gravitational Hamiltonian.
```

It does reduce the number of independent black-hole-like inputs.  If the
Schwarzschild entropy is represented as boundary-cell state count, and those
boundary cells are the weak emitters, the area emission law follows.

The remaining main inputs become:

```text
1. boundary-cell density of states with S(E) ~ E^2,
2. local weak coupling of active boundary cells to outgoing modes,
3. shell mixing/decoupling.
```

Compared with the previous result lock, item 2 is now a locality/operator
access assumption rather than an independent rate-scaling assumption.

## Next Possible Push

The next question is whether the boundary-cell density of states itself can be
made less imposed.  The most plausible routes are:

```text
1. constrained boundary Hilbert spaces with N(E)~E^2 active cells,
2. long-range/nonadditive systems whose microcanonical entropy grows as E^2,
3. matrix/fuzzy-boundary systems where the number of accessible boundary
   operators grows as the matrix size squared.
```

This is harder than the operator-counting step.  The operator-counting step
does, however, make clear what such a microscopic model must produce: not just
a large state count, but a boundary-accessible state count.
