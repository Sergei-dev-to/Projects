# Relaxing the Haar and Area-Strength Inputs

## Question

Can two of the main model inputs be weakened?

1. Replace a Haar-random composite emission map by a standard scrambling or
   design condition.
2. Replace an imposed area-strength emission rate by many weak emission
   channels whose rates add incoherently.

The answer is mostly yes.  The result still needs the Schwarzschild density of
states as an input, but the fine-grained information flow does not require full
Haar randomness, and the Schwarzschild rate law does not require a single
matrix element whose strength is set by hand to be proportional to area.

## 1. Haar Typicality Can Be Replaced by Low-Order Design Conditions

### What the Haar assumption was doing

The earlier calculation used a composite map

```text
V : H_initial -> H_B(E) tensor H_R(E)
```

and treated it as Haar-typical on the active microcanonical support.  That
assumption was used for three related statements:

1. Page entropy:

```text
S(R) ~= min{ log dim H_R, log dim H_B }.
```

2. Code-subspace decoupling:

```text
b >> d r   -> early radiation is decoupled from the reference,
r >> d b   -> remaining core is decoupled from the reference.
```

3. Replica moments:

```text
E Tr rho_R^n
```

has competing contractions, with a post-Page contraction through the smaller
remaining core factor.

These uses do not all require the same amount of randomness.

### Second moments only require a 2-design

The Page purity, the code-subspace decoupling bounds, and the second Renyi
version of the island/Page transition use only fourth moments of the amplitudes,
or equivalently second moments of the unitary/isometry channel.

Thus full Haar randomness can be replaced by an exact unitary 2-design on the
active microcanonical shell.  For an approximate 2-design, the same estimates
hold with an additive design error.

For the uniform-support code calculation, the Haar result was

```text
E Tr rho_QB^2 ~= 1/(db) + 1/r,
E Tr rho_QR^2 ~= 1/(dr) + 1/b.
```

Let `epsilon_2` denote the effective second-moment error of the scrambling
ensemble or dynamics on the active shell.  Then the working estimates become

```text
E ||rho_QB - I_Q/d tensor I_B/b||_1
  lesssim sqrt{ db (1/r + epsilon_2) },

E ||rho_QR - I_Q/d tensor I_R/r||_1
  lesssim sqrt{ dr (1/b + epsilon_2) }.
```

Therefore the same code-subspace thresholds survive provided

```text
db/r << 1,        db epsilon_2 << 1
```

for recovery from radiation, and

```text
dr/b << 1,        dr epsilon_2 << 1
```

for early radiation to be uninformative.

For weighted Hawking histories, the recovery estimate becomes

```text
E ||rho_QB - I_Q/d tensor I_B/b||_1
  lesssim sqrt{ db (Tr p^2 + epsilon_2) }.
```

Thus recovery from radiation follows when

```text
S_2^rad = -log Tr p^2 >> log d + log b
```

and the design error is small on the same scale:

```text
db epsilon_2 << 1.
```

For early radiation, the 2-norm excess around the decoupled target
`I_Q/d tensor p_R` is of order `1/b + epsilon_2`.  Converting to trace norm
requires specifying the effective radiation support.  On a thermal typical set
of size `exp(H(p)+o(S))`, the estimate is

```text
error lesssim exp[(log d + H(p) - log b + o(S))/2]
              + sqrt{ d exp(H(p)) epsilon_2 }.
```

So the entropy-level early condition is

```text
H(p) << log b - log d,
```

again with the design error small on the tested support.

### Higher replica moments need higher designs

The full `n`th replica moment

```text
E Tr rho_R^n
```

uses `n` copies of the state and therefore needs an `n`-design, or a dynamical
assumption strong enough to reproduce the relevant `n`th moment.  A 2-design is
enough for purity and decoupling.  It is not enough for every replica index.

This gives a useful hierarchy:

```text
Page purity / second Renyi / decoupling:
  approximate 2-design is enough.

Fixed Renyi-n island/no-island contraction:
  approximate n-design is enough.

Von Neumann entropy with concentration:
  needs either Haar/Page concentration, sufficiently high design, or a separate
  decoupling/typical-subspace theorem.
```

The paper should therefore avoid saying that the dynamics must be Haar random.
The sharper condition is:

```text
The cumulative in-sector dynamics must act as an approximate low-order design
on the active microcanonical shell, to the order required by the diagnostic
being computed.
```

This is standard black-hole information language.  Hayden-Preskill assume
rapidly mixing unitary dynamics; fast-scrambling and random-circuit models are
ways to justify design-like behavior.  The present model can inherit that
standard condition rather than postulating a full Haar map.

### What remains assumed

This does not derive fast scrambling from a concrete local Hamiltonian.  It
relaxes the assumption from

```text
the composite map is Haar random
```

to

```text
the cumulative shell dynamics reaches the low-order design/decoupling regime
needed for the Page, code-subspace, and replica diagnostics.
```

That is a real weakening.  A concrete `H_mix` would still need to be checked if
we wanted a fully dynamical scrambling result.

## 2. Area-Strength Emission Can Be Replaced by Many Weak Channels

### The issue

The rate calculation needs the inclusive low-frequency emission strength to
scale like horizon area.  Written as a single matrix-element normalization,
that looks imposed.

A more physical Hamiltonian form introduces many weak channels:

```text
mu = 1, ..., N_A(E),
N_A(E) proportional to A(E).
```

Each channel has an ordinary weak coupling of the same microscopic size.  The
total rate gets its area factor because rates add after summing over channels.

### Hamiltonian form

Use

```text
H_I =
  sum_{mu=1}^{N_A(E)} sum_{lambda,a,b}
  int d omega [
    g omega^{p/2} u^{mu lambda}_{ba}(omega)
    |b><a| b_lambda^dagger(omega,mu)
    + h.c.
  ].
```

The label `mu` may be carried either by an explicit outgoing channel, by an
orthogonal boundary operator, or by an internal channel label that is summed
inclusively.  What matters for the rate is that different `mu` channels add
incoherently.

The ETH/random-matrix normalization per channel is

```text
u^{mu lambda}_{ba} = D_E^{-1/2} r^{mu lambda}_{ba},
overline{|r^{mu lambda}_{ba}|^2} = C_lambda(E,omega).
```

Then, for one channel,

```text
sum_{b in E-omega} |u^{mu lambda}_{ba}|^2
  ~= C_lambda(E,omega) D_{E-omega}/D_E.
```

Summing over channels gives

```text
sum_mu sum_b |u^{mu lambda}_{ba}|^2
  ~= N_A(E) C_lambda(E,omega) D_{E-omega}/D_E.
```

The golden-rule rate is therefore

```text
d Gamma / d omega
  ~= 2 pi g^2 N_A(E) omega^p C_lambda(E,omega)
      exp[S_micro(E-omega)-S_micro(E)].
```

If

```text
N_A(E) proportional to A(E),
```

this is exactly the area factor needed for Schwarzschild emission.

### Why incoherent addition matters

If all area channels coupled to the same final radiation state with identical
phases, amplitudes could add before squaring, giving

```text
Gamma proportional to N_A(E)^2.
```

That would be the wrong scaling.  The model needs the physically standard
inclusive case:

```text
different channels are orthogonal, independently phased, or separately
resolved in the outgoing continuum.
```

Then cross terms vanish under channel resolution, shell averaging, or random
phase averaging, and the rate scales as `N_A(E)`.

### Schwarzschild scaling

With three spatial radiation dimensions,

```text
p = 2.
```

The number flux scales as

```text
Gamma_quanta(E) ~ A(E) int d omega omega^2 exp[-beta(E) omega]
                ~ A(E) T(E)^3.
```

The power scales as

```text
P(E) ~ A(E) int d omega omega^3 exp[-beta(E) omega]
     ~ A(E) T(E)^4.
```

For Schwarzschild input

```text
A(E) ~ E^2,
T(E) ~ E^{-1},
```

this gives

```text
Gamma_quanta ~ E^{-1},
P ~ E^{-2},
t_evap ~ E_0^3.
```

The area rate law is therefore generated by channel multiplicity plus standard
weak-coupling emission.  The remaining input is the channel count
`N_A(E) ~ A(E)`, not an area-sized coupling constant.

### What remains assumed

This upgrade does not derive the area channel count from simpler microscopic
degrees of freedom.  It changes the assumption from

```text
the matrix element strength is proportional to area
```

to

```text
there are A(E)-many independent weak emission channels.
```

That is closer to the horizon-cell intuition and to an inclusive absorption
cross-section.  It also makes the Hamiltonian more ordinary: many weak
couplings with fixed microscopic strength produce a large inclusive rate.

## Combined Result

After these two upgrades, the model assumptions are:

```text
1. S_micro(E) ~ E^2.
2. N_A(E) ~ A(E) independent weak emission channels.
3. Weak coupling to an outgoing continuum.
4. Cumulative in-sector dynamics reaches the required low-order design regime.
```

The consequences are:

```text
S_micro(E) ~ E^2
  -> T(E) ~ E^{-1}, negative heat capacity, DOS-ratio thermality.

N_A(E) ~ A(E)
  -> Schwarzschild number flux, power, and lifetime.

low-order design / decoupling
  -> Page curve, code-subspace information transfer, and low-order replica
     contraction structure.
```

The largest remaining explicit black-hole input is the density of states

```text
S_micro(E) ~ E^2.
```

The area factor is now a channel-count input rather than a rate-strength input.
The Haar input is now a standard low-order design/decoupling condition rather
than full Haar randomness.

## Immediate Strengthening: Fixed-Map Moment Bounds

The next improvement is to state the fine-grained part without ensemble
language.  Fix the Hamiltonian, fix the initial energy shell, and fix a coarse
evaporation trajectory.  The weak-coupling reduction gives a composed
Stinespring map

```text
V : H_{E0} -> H_B(E) tensor H_R(E).
```

The information-flow calculation only needs finite moment information about
this fixed map.  For a diagnostic using `k` copies, define a moment error

```text
epsilon_k(V)
```

as the maximum deviation, on the active support, between the `k`-copy
contractions generated by `V` and the corresponding Haar or design
contractions.  The exact norm can be chosen to match the application:
diamond norm for a channel statement, trace norm on the Choi state for a
code-subspace statement, or operator norm against a specified replica
observable.

With this notation, the fine-grained conclusions become deterministic
conditional statements about the fixed map `V`.

### Page purity

The second-Renyi/Page-purity diagnostic uses `k=2`.  In the uniform-support
case,

```text
Tr rho_R^2 = 1/r + 1/b + O(epsilon_2(V))
```

instead of the Haar-averaged expression.  The Page crossing is unchanged when

```text
epsilon_2(V) << min{1/r, 1/b}
```

away from the transition.  Near `r ~ b`, finite rounding is already present, so
the relevant condition is that `epsilon_2(V)` is small compared with the
entropy-scale separation being claimed.

For weighted histories,

```text
Tr rho_R^2 = Tr p^2 + 1/b + O(epsilon_2(V)).
```

The second-Renyi island/no-island exchange therefore survives if the moment
error is smaller than the dominant branch away from the Page crossing.

### Code-subspace decoupling

For a code subspace of dimension `d`,

```text
V : C_d -> B_b tensor R_r,
```

the fixed-map estimates are

```text
||rho_QB - I_Q/d tensor I_B/b||_1
  lesssim sqrt{ db (1/r + epsilon_2(V)) },

||rho_QR - I_Q/d tensor I_R/r||_1
  lesssim sqrt{ dr (1/b + epsilon_2(V)) }.
```

Thus the uniform code thresholds become

```text
r >> d b      and      db epsilon_2(V) << 1
  -> radiation recovers the code,

b >> d r      and      dr epsilon_2(V) << 1
  -> early radiation is uninformative.
```

For weighted Hawking histories,

```text
||rho_QB - I_Q/d tensor I_B/b||_1
  lesssim sqrt{ db (Tr p^2 + epsilon_2(V)) },
```

so late recovery follows when

```text
S_2^rad >> log d + log b,
db epsilon_2(V) << 1.
```

For early radiation on a thermal typical set of size `exp(H(p)+o(S))`,

```text
error lesssim exp[(log d + H(p) - log b + o(S))/2]
              + sqrt{ d exp(H(p)+o(S)) epsilon_2(V) }.
```

This gives the same entropy-level early condition,

```text
H(p) << log b - log d,
```

with the fixed-map moment error small on the tested typical support.

### Replica moments

For a fixed Renyi index `n`, the replica observable uses `n` copies.  The
moment statement is

```text
Tr rho_R^n =
  [Haar/design contraction sum at order n]
  + O(epsilon_n(V)).
```

The no-island/island contraction exchange survives whenever `epsilon_n(V)` is
small compared with the leading branch away from the Page crossing.  This is a
stronger and cleaner statement than requiring the full map to be Haar-random:
only the `n`th moment relevant to the chosen diagnostic is needed.

### Interpretation

This removes random sampling from the result statement.  Random matrices,
random circuits, or chaotic ensembles are sufficient ways to argue that
`epsilon_k(V)` is small.  The actual evaporation model can be a fixed
Hamiltonian whose composed map satisfies the required moment bounds.

The improved assumption is therefore:

```text
For each diagnostic of order k, the composed fixed emission map has
epsilon_k(V) small on the active microcanonical support.
```

This is the strongest near-term version of Result 2.  It preserves
deterministic unitary evolution after the Hamiltonian is fixed and makes the
randomness issue quantitative.

## Paper-Level Wording

The paper should say:

```text
The fine-grained statements require only the low-order moments relevant to the
diagnostic.  The second-Renyi Page curve and code-subspace decoupling follow
from an approximate 2-design on the active shell; fixed Renyi-n replica
moments require the corresponding n-design.  We therefore formulate the
scrambling assumption as cumulative low-order design behavior rather than full
Haar randomness.
```

For the rate:

```text
The area dependence enters as an inclusive channel count.  The Hamiltonian has
N_A(E) independent weak emission channels, with N_A(E) proportional to the
area.  Since the channels are orthogonal or independently phased, the
golden-rule rates add incoherently.  This produces the same area factor as the
low-frequency absorption cross-section without assigning an area-sized
coupling to a single channel.
```

## Status

This is a positive result for assumptions 1 and 2 from the relaxation list.

Relaxed:

```text
Haar random composite map
  -> approximate low-order design / decoupling condition.

area-sized matrix element
  -> A(E)-many ordinary weak channels.
```

Still open:

```text
derive S_micro(E) ~ E^2 from simpler non-gravitational microscopic degrees of
freedom;

derive N_A(E) ~ A(E) from a specific boundary or horizon-cell model;

prove that a chosen concrete H_mix reaches the needed low-order design regime
on the evaporation time scale.
```
