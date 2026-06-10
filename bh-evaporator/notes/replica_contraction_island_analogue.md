# Replica Contraction Analogue of the Island Saddle

## Question

Can the Hamiltonian model be given a replica interpretation that is closer to
the replica-wormhole story than a verbal comparison of entropy formulas?

## Setup

For a fixed narrow evaporation trajectory, the composed emission map is an
isometry

```text
V : H_0 -> H_B(E) \otimes H_R(E)
```

on the active microcanonical support.  Let

```text
b = dim H_B(E),   r = dim H_R(E).
```

If the composed map is Haar-typical on this support, then for a fixed initial
state the final state is a Haar-random pure state on
`H_B(E) \otimes H_R(E)`, up to the energy-trajectory weights already fixed by
the emission calculation.

Equivalently, if the composite evaporation map is a Haar-random isometry from
the initial active support into `H_B(E) \otimes H_R(E)`, then applying it to a
fixed normalized input vector produces a Haar-random output vector on the
codomain support.  The entropy calculation below is therefore the fixed-input,
random-composite-map version of Page's theorem.

The radiation entropy is computed from

```text
rho_R = Tr_B |psi><psi|.
```

The replica object is

```text
E_Haar Tr rho_R^n.
```

## Exact Haar Moment

Let `D=br`.  For a Haar-random pure state `|psi>` on
`H_B \otimes H_R`,

```text
E |psi><psi|^{\otimes n}
  = 1/(D)_n  sum_{sigma in S_n} P_sigma,
```

where

```text
(D)_n = D(D+1)...(D+n-1)
```

and `P_sigma` permutes the `n` copies of `H_B \otimes H_R`.

The moment of the radiation density matrix is

```text
Tr rho_R^n = Tr[ |psi><psi|^{\otimes n} (I_B^{\otimes n} \otimes P_tau^R) ],
```

with `tau=(12...n)`.  Taking the Haar average gives

```text
E Tr rho_R^n
  = 1/(br)_n sum_{sigma in S_n}
        b^{C(sigma)} r^{C(tau sigma)}
```

where `C(sigma)` is the number of cycles of the permutation `sigma`, and
`tau=(12...n)` is the cyclic gluing imposed by `Tr rho_R^n`.

For fixed `n` and large `b,r`, `(br)_n=(br)^n[1+O((br)^(-1))]`, so

```text
E Tr rho_R^n
  ~= (br)^(-n) sum_{sigma in S_n}
        b^{C(sigma)} r^{C(tau sigma)}.
```

For `n=2`, this reduces to

```text
E Tr rho_R^2 = (b+r)/(br+1) = 1/r + 1/b + O((br)^(-1)).
```

That already displays the Page transition: before Page time `r << b`, the
radiation purity is `1/r`; after Page time `b << r`, it is `1/b`.

## Two Leading Contractions

For general `n`, two contractions dominate in the two regimes.

### Radiation/no-island contraction

Take `sigma = identity`.  Then

```text
C(sigma)=n,   C(tau sigma)=1,
```

so

```text
E Tr rho_R^n ~= r^{1-n}.
```

This gives

```text
S_n(R) ~= log r.
```

This is the no-island/Hawking branch: the radiation entropy is the size of the
emitted radiation support.

### Core/island contraction

Take `sigma = tau^{-1}`.  Then

```text
C(sigma)=1,   C(tau sigma)=n,
```

so

```text
E Tr rho_R^n ~= b^{1-n}.
```

This gives

```text
S_n(R) ~= log b.
```

This is the island branch in the Hamiltonian model: the radiation entropy is
controlled by the smaller remaining core Hilbert space.

The exact statement is a large-dimension saddle statement for fixed replica
index `n`.  Other permutations are subleading away from `b ~ r`.  At the Page
transition several contractions can be comparable, giving the usual finite
rounding of the transition rather than a sharp thermodynamic singularity.

## Weighted Radiation Histories

The uniform-support calculation is the cleanest Page-theorem limit, but the
evaporator does not emit all radiation histories with equal probability.
Along a coarse trajectory, let the radiation histories be labelled by `alpha`
with probabilities

```text
p_alpha,     sum_alpha p_alpha = 1.
```

The no-island branch should then be the entropy of this emitted radiation
distribution, not simply the logarithm of the number of allowed histories.

A useful large-dimension model is a random purification of this radiation
distribution:

```text
|psi> = sum_{a,alpha} X_{a alpha} |a>_B |alpha>_R,
E X_{a alpha} X^*_{b beta}
    = delta_ab delta_{alpha beta} p_alpha / b.
```

Normalization fluctuations are suppressed at large `b`.  The radiation density
matrix is the correlated Wishart matrix

```text
rho_R = X^\dagger X.
```

The Gaussian contraction expansion gives

```text
E Tr rho_R^n
  ~= sum_{sigma in S_n}
      b^{C(sigma)-n}
      prod_{c in cycles(tau sigma)} Tr p^{|c|}.
```

Here `p` denotes the diagonal matrix with entries `p_alpha`, and `|c|` is the
length of a cycle.

This formula reduces to the uniform-support formula when `p_alpha=1/r`, since

```text
prod_c Tr p^{|c|}
  = prod_c r^{1-|c|}
  = r^{C(tau sigma)-n}.
```

The two leading contractions become:

```text
sigma = identity:
E Tr rho_R^n ~= Tr p^n
```

and

```text
sigma = tau^{-1}:
E Tr rho_R^n ~= b^{1-n}.
```

Thus the no-island branch is the emitted radiation Renyi entropy

```text
S_n^rad = (1/(1-n)) log Tr p^n,
```

while the island branch remains

```text
log b = S_micro(E).
```

For `n=2`,

```text
E Tr rho_R^2 ~= Tr p^2 + 1/b.
```

For the von Neumann entropy, the corresponding large-dimension Page/island
statement is

```text
S_vN(R) ~= min{ H(p), log b } + O(1),
```

where

```text
H(p) = - sum_alpha p_alpha log p_alpha
```

is the coarse emitted radiation entropy.  In the evaporation model this is
`Delta S_rad(E)` along the trajectory.

This weighted calculation is the physically relevant one.  It shows that the
replica-contraction exchange survives the Hawking weights; the radiation-side
branch becomes the thermal/Renyi entropy of the emitted ensemble, while the
post-Page branch is still controlled by the remaining core state count.

## Connection Back to the Hamiltonian

The weak-coupling Hamiltonian supplies the weights `p_alpha`.  For a sequence
of emissions, `alpha` denotes a coarse radiation history: emitted energies,
channels, angular labels, and time-bin labels.  The product of Fermi's
golden-rule branching probabilities along the trajectory gives

```text
p_alpha = product over emission steps of p(step | previous core energy).
```

The density-of-states ratio and the area-strength inclusive coupling determine
these probabilities.  Their Shannon entropy is the emitted thermodynamic
entropy:

```text
H(p) = Delta S_rad(E)
```

within the quasi-stationary approximation.

The mixing term supplies the typicality assumption.  If in-sector scrambling
is fast compared with the evaporation time, the composite emission map can be
treated as a random purification of the radiation-history distribution on the
active support.  Then the weighted replica calculation applies.

This gives a clean division:

```text
H_I and rho_B(E)  -> branch weights p_alpha
H_mix             -> random orientation / typical purification
replica moment    -> no-island/island contraction exchange
```

For a fixed typical initial pure state in the initial shell, this is the
direct version of the argument.  A stronger code-subspace statement, valid
uniformly for all initial microstates in a large subspace, would require a
random-isometry or decoupling version of the same weighted calculation.  The
entropy curve for typical initial states does not require that stronger
statement.

## Current Status

This branch now has a positive result, conditional on the same typicality
assumption already used for the Page curve.

Established:

1. For a Haar-random final state on `H_B x H_R`, the replica moment has
   competing no-island and island contractions.
2. For weighted Hawking radiation histories, the no-island branch becomes the
   emitted radiation Renyi/Shannon entropy rather than a flat support entropy.
3. The post-Page branch remains `S_micro(E) = log dim H_B(E)`.
4. The contraction `sigma=tau^{-1}` is a precise non-geometric analogue of the
   replica-wormhole contribution at the level of `E Tr rho_R^n`.
5. The Hamiltonian ingredients map cleanly onto the calculation:
   emission gives `p_alpha`, mixing gives typical purification, state count
   gives the island/QES term.

Conditional:

1. The random purification is assumed as the effective outcome of cumulative
   scrambling.  It is not derived from a concrete local `H_mix`.
2. The moment calculation is annealed.  Concentration/Page typicality gives
   the typical entropy statement at large dimension.
3. The result is for entropy and replica moments.  It does not give
   entanglement-wedge reconstruction, interior operators, or a geometric
   replica wormhole.

Result-level conclusion:

```text
The non-gravitational Hamiltonian class reproduces not only the exterior
Schwarzschild evaporation phenomenology and the Page/island entropy formula,
but also the replica-contraction mechanism behind the island/no-island
saddle exchange, in a non-geometric random-matrix sense.
```

## Code-Subspace Version

The fixed-state Page curve does not by itself say where information about a
family of initial black-hole microstates goes.  To test information transfer,
choose a code subspace

```text
C subset H_{E0},      d = dim C,
```

and entangle it with a reference system `Q`:

```text
|Phi>_{QC} = d^{-1/2} sum_i |i>_Q |i>_C.
```

After the composite emission map,

```text
|Psi>_{QBR} = (I_Q \otimes V)|Phi>_{QC}.
```

The code information is in the radiation when `Q` is decoupled from the
remaining core `B`.  Because `QBR` is pure, this is equivalent to recoverability
from `R` by the usual decoupling logic.

### Uniform-Support Thresholds

First ignore Hawking weights and take the radiation support dimension to be
`r`.  For a Haar-random encoding into

```text
H_Q \otimes H_B \otimes H_R
```

with dimensions

```text
d, b, r,
```

Page estimates give

```text
S(Q)  ~= log d,
S(B)  ~= min(log b, log d + log r),
S(QB) ~= min(log d + log b, log r).
```

Thus

```text
I(Q:B) = S(Q) + S(B) - S(QB).
```

There are three regimes.

The second-moment calculation gives a sharper version.  For a Haar-random
isometry

```text
V : C_d -> B_b \otimes R_r
```

and a maximally entangled reference `Q`, the final state is

```text
|Psi>_{QBR} = d^{-1/2} sum_i |i>_Q V|i>_C.
```

The exact Haar averages of the two relevant purities are

```text
E Tr rho_QB^2
  = [ b(r^2-1) + d r(b^2-1) ] / [ d((br)^2-1) ]
  ~= 1/(db) + 1/r,

E Tr rho_QR^2
  = [ r(b^2-1) + d b(r^2-1) ] / [ d((br)^2-1) ]
  ~= 1/(dr) + 1/b.
```

The first expression controls recovery from radiation: `Q` is decoupled from
the remaining core `B` when `rho_QB` is close to
`I_Q/d \otimes I_B/b`.  The second controls whether early radiation is
uninformative: `Q` is decoupled from `R` when `rho_QR` is close to
`I_Q/d \otimes I_R/r`.

Early:

```text
r << b/d
```

Then

```text
S(B) ~= log d + log r,
S(QB) ~= log r,
I(Q:B) ~= 2 log d.
```

The reference is still in the remaining core.  The radiation is approximately
uninformative about the code.

Late:

```text
r >> b d
```

Then

```text
S(B) ~= log b,
S(QB) ~= log d + log b,
I(Q:B) ~= 0.
```

The reference is decoupled from the core.  By decoupling/recovery, the code is
recoverable from the radiation.

The maximally decoupled target has purity `1/(db)`.  Hence, using the
second-moment estimate above,

```text
E || rho_QB - I_Q/d \otimes I_B/b ||_2^2 ~= 1/r,
```

and the trace-distance error is bounded by

```text
E || rho_QB - I_Q/d \otimes I_B/b ||_1
  lesssim sqrt(db/r).
```

Thus recovery from radiation is parametrically good when

```text
r >> d b.
```

Similarly, early radiation is decoupled from the reference when

```text
E || rho_QR - I_Q/d \otimes I_R/r ||_1
  lesssim sqrt(d r/b),
```

so early radiation is uninformative when

```text
b >> d r.
```

Middle:

```text
b/d lesssim r lesssim b d
```

The information is shared between core and radiation.  The width of this
transition region is set by the code size.  For a one-dimensional "code"
(`d=1`) it collapses to the ordinary Page crossing `r ~ b`.

### Weighted Version

For Hawking radiation histories, replace `log r` by an effective radiation
entropy.  At the entropy level the thresholds become

```text
early-uninformative:  H(p) << log b - log d,
late-recoverable:    H(p) >> log b + log d.
```

The recovery side has a clean second-Renyi diagnostic.  Let

```text
S_2^rad = -log Tr p^2
```

be the collision entropy of the radiation-history distribution.  The weighted
analogue of the `QB` purity is

```text
E Tr rho_QB^2 ~= 1/(db) + Tr p^2.
```

Therefore

```text
radiation recovery:
  error lesssim exp[ (log d + log b - S_2^rad)/2 ].
```

This reduces to the uniform-support estimate when `S_2^rad=log r`.

The early-radiation estimate needs one extra specification.  The target state
is the radiation-history state `p`, so the decoupled target is

```text
I_Q/d \otimes p_R.
```

The weighted `QR` purity is

```text
E Tr rho_QR^2 ~= (1/d) Tr p^2 + 1/b.
```

Since

```text
Tr (I_Q/d \otimes p_R)^2 = (1/d) Tr p^2,
```

the second-moment calculation gives

```text
E || rho_QR - I_Q/d \otimes p_R ||_2^2 ~= 1/b.
```

A trace-norm bound also depends on the effective number of radiation histories
being tested.  A conservative statement uses the support size

```text
S_0^rad = log rank(p)
```

and gives

```text
early radiation uninformative:
  error lesssim exp[ (log d + S_0^rad - log b)/2 ].
```

For a thermal distribution one normally restricts to a typical radiation set.
If the typical set has size `exp(H(p)+o(S))`, the same estimate becomes

```text
early radiation uninformative:
  error lesssim exp[ (log d + H(p) - log b + o(S))/2 ].
```

Thus the Shannon-threshold statement is an entropy-level, typical-subspace
statement.  A fully one-shot trace-norm theorem should be written with support,
min-, or smooth max-entropy parameters rather than with `H(p)` alone.

In evaporation variables,

```text
H(p) = Delta S_rad(E),
log b = S_micro(E),
```

so the code-subspace thresholds are

```text
Delta S_rad(E) << S_micro(E) - log d   -> early radiation uninformative,
Delta S_rad(E) >> S_micro(E) + log d   -> radiation recovers the code.
```

For a fixed finite code subspace, the transition sharpens on the
Schwarzschild entropy scale.  For a large code subspace, the Page transition
is broadened by `2 log d`.

### Meaning

This is stronger than the Page entropy curve.  It says:

1. before the Page transition, early radiation is locally thermal and carries
   essentially no information about the chosen code subspace;
2. after enough radiation is emitted, the remaining core decouples from the
   reference;
3. the initial code information is then recoverable from the radiation by
   standard decoupling/recovery theorems.

This is the gravity-free analogue of the information-transfer part of the
island story.  It is still not entanglement-wedge reconstruction, because
there is no geometric interior algebra.  It is a code-subspace recovery
statement for the non-gravitational evaporation map.

### Code-Subspace Status

The code-subspace result is now sharp in the uniform-support model:

```text
b >> d r   -> early radiation is decoupled from the reference,
r >> d b   -> the remaining core is decoupled from the reference.
```

Equivalently, the Page transition for a code of dimension `d` is broadened
from `r ~ b` to the window

```text
b/d lesssim r lesssim b d.
```

For weighted Hawking histories, the recovery side is also sharp at the
second-Renyi level:

```text
S_2^rad >> log b + log d
  -> recovery from radiation.
```

The early-radiation side is sharp after choosing the radiation support being
tested.  With a thermal typical set this gives

```text
H(p) << log b - log d
  -> early radiation carries negligible code information.
```

The remaining technical caveat is therefore narrow: a fully one-shot weighted
statement should be phrased with smooth entropy support parameters.  The
entropy-scale conclusion used for black-hole phenomenology already follows
from the typical-set version.

## Entropy Consequence

The annealed Renyi entropy is

```text
S_n^ann(R) = (1/(1-n)) log E Tr rho_R^n.
```

Away from the transition,

```text
S_n^ann(R) = min(S_n^rad, log b) + O(1).
```

The von Neumann entropy follows by the standard Page result rather than by
blindly analytically continuing a saddle expression:

```text
E S_vN(R) = min(H(p), log b) + O(1).
```

The `O(1)` term is the Page correction.  It is small compared with the
Schwarzschild entropy scale.

There is an annealed/quenched distinction:

```text
annealed:  log E Tr rho_R^n
quenched:  E log Tr rho_R^n
```

The displayed replica moment is annealed.  Page's theorem and concentration of
measure give the corresponding typical, or quenched, entropy statement at
large dimensions.  Near `b ~ r`, the transition is rounded by finite-size
corrections, so the saddle language should be read as a large-entropy
asymptotic statement.

## Correspondence

Gravity language:

```text
S(R) = min over saddles [ A(QES)/(4G) + S_bulk(R union I) ].
```

Hamiltonian replica language:

```text
S(R) ~= min { H(p), log b }.
```

The identifications are:

```text
H(p)   = Delta S_rad(E)        no-island/Hawking branch
log b  = S_micro(E)            island/QES branch
```

The replica-wormhole analogue is not a geometric saddle.  It is the
non-geometric contraction pattern `sigma=tau^{-1}` in the Haar/random-matrix
average.  This contraction routes the replicas through the smaller remaining
core factor, just as the island saddle routes the gravitational replica
calculation through the QES contribution.

More explicitly:

```text
identity contraction
  -> replicas glued only by radiation cyclicity
  -> Hawking/no-island answer

cyclic core contraction
  -> replicas effectively connected through the traced core indices
  -> Page/island answer
```

This is a precise non-gravitational counterpart of the replica-wormhole
calculation at the level of the replica observable.  It is not a spacetime
solution.

## What This Adds

This improves the result over a plain Page-theorem statement.

The entropy min formula is not only a dimension-counting slogan.  In the
random composite-emission version of the Hamiltonian, the replica moments have
the same structural ingredients as the gravitational calculation:

1. a replica observable `Tr rho_R^n`;
2. competing contributions to that observable;
3. a Page-time exchange of dominance;
4. a post-Page contribution that connects replicas through the smaller
   remaining system;
5. a non-geometric counterpart of the island/QES term.

This does not produce spacetime wormholes.  It gives a precise random-matrix
analogue of the replica-wormhole contribution.

It also separates three layers:

1. black-hole thermodynamics comes from `S_micro(E)` and the area-strength
   emission rule;
2. the Page/island entropy curve comes from the shrinking dimension pair
   `(b,r)`;
3. the replica-wormhole-like mechanism comes from the Haar/random-matrix
   contraction expansion of `E Tr rho_R^n`.

The third layer is stronger than saying "the entropy has the same min form."
It says the non-gravitational replica calculation has two competing
contributions with the same dominance pattern as the gravitational calculation.

## Relation to Existing Literature

This point is close to existing work:

- Page's theorem gives the smaller-factor entropy for typical pure states.
- Urbach studies typical pure states and replica-wormhole-like Page behavior.
- de Boer, Hollander, and Rolph explicitly derive Page curves and
  replica-wormhole-like contributions from random dynamics with GUE statistics
  in microcanonical windows.
- Basu, Wen, and Zhou discuss island formulas from Hilbert-space reduction and
  self-encoding.

The closest paper is de Boer, Hollander, and Rolph.  They evolve within a
microcanonical window using a GUE-random Hamiltonian and show that Haar
averaging produces connected matrix-index contractions that act like
replica-wormhole contributions.  Their model is designed to capture the
unitary and non-unitary Page curves, not the full Schwarzschild evaporation
package.  They explicitly list missing features such as intermediate
partially evaporated states and a realistic local evaporation process.

Our specific assembly is different in three ways:

1. the core has a Schwarzschild microcanonical state count
   `S_micro(E) ~ E^2`;
2. weak emission gives Hawking weights and the finite-energy correction from
   density-of-states ratios;
3. the area-strength inclusive coupling gives the Schwarzschild quanta rate,
   power, and lifetime scalings.

The weighted replica calculation above is therefore not a new invention of
replica-wormhole-like contractions.  It is the application of that random
replica logic to the energy-resolved evaporation Hamiltonian.  The potential
value is the combination:

```text
Schwarzschild thermodynamics and rates
  + ordinary unitary evaporation
  + Page/island entropy
  + replica-wormhole-like contraction exchange
```

inside one non-gravitational Hamiltonian class.

## Consequence for the Paper

The paper should not say that it derives geometric replica wormholes.

It can say:

```text
For a Haar-random composite emission map, the replica moments have two leading
contraction patterns.  Their exchange gives the Page/island min formula.  The
post-Page contraction is the non-geometric random-matrix analogue of a replica
wormhole saddle.
```

That is a real strengthening of the island comparison and a useful bridge to
the literature on Page curves from random dynamics.

## Possible Strong Claim

The strongest accurate claim seems to be:

```text
The model reproduces the exterior Schwarzschild evaporation package and,
under the same Haar-typical composite emission assumption used for the Page
curve, its replica moments contain a non-geometric analogue of the
replica-wormhole saddle.  The post-Page contribution is a contraction through
the smaller remaining core Hilbert space, whose entropy is S_micro(E).
```

This is not "replica wormholes without gravity" in the geometric sense.  It is
"replica-wormhole logic without gravity" in the random-matrix sense.

## What Would Make It More Interesting

The next level would be to replace the Haar assumption by dynamics:

```text
H_mix + weak emission -> effective random composite map
```

Then the replica-contraction result would follow from the Hamiltonian dynamics
rather than from an ensemble assumption.  That is the harder result.  For the
current conditional Hamiltonian class, the replica calculation is already a
useful and standard consequence of the stated typicality assumption.
