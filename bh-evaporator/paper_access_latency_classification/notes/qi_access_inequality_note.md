# Heisenberg Cut as an Access Profile

Public records, private recovery, and latency.

Date: 2026-06-29

Status: internal formulation note.  This packages standard QI
ingredients into an access-profile statement.

## Purpose

The Heisenberg cut can be treated as an access cut.  A specified record
family makes a commuting label public and leaves a complementary quantum
diary private relative to that same access algebra.

```text
public side:
    redundant fragments recover a classical label X

private side:
    the accessible record channel carries essentially no recoverable
    information about a noncommuting diary D
```

The access inequality quantifies the private side:

```text
|| N_R - K_R ||_diamond <= epsilon
    =>
F_rec^e(D from R) <= 1/d_D^2 + O(epsilon).
```

Here `N_R : D -> R` is the diary-to-record channel and `K_R` is constant
on the diary; `R` is the record set `R_t` of the later sections, so
`N_R = N_t`.  Moving the cut means changing `R`, hence changing the
channel and the recovery bound.

Textbook Heisenberg-cut invariance concerns public outcome statistics:
sliding the von Neumann cut preserves those statistics.  The access cut
adds a second quantity: recoverability of the private complement.  That
quantity genuinely moves with the accessible record/control algebra.

## Layer Separation

The same access language appears in three layers.

```text
QI core:
    nearly constant diary channel => trivial diary recovery.

decoherence / Darwinism application:
    redundant records make X objective while D remains hidden from those
    records.

horizon / Hayden-Preskill landmark:
    enlarged access plus side information can recover D after short
    latency, with possible decoding hardness.
```

The Heisenberg-cut claim uses the first two layers.  A record family
defines an access cut when it has both:

```text
public side:
    P_guess(X | F_i) >= 1 - epsilon_pub
    for many fragments F_i

private side:
    || N_R - K_R ||_diamond <= epsilon_priv
    for the diary-to-accessible-record channel N_R : D -> R
```

where `K_R` is constant on the diary.  The private side is exactly the
hypothesis of the access inequality above, so every decoder using only
the records on that side of the cut obeys the same bound,
`F_rec^e(D from R) <= 1/d_D^2 + O(epsilon_priv)`.

This is the access-cut inequality.  The public records make the
commuting label `X` objective, while the noncommuting diary `D` remains
outside the recovery power of that access algebra.  The horizon material
is only a landmark in the latency/complexity landscape.

## Nearby Literature and Meaning

`Access cut` is local shorthand for a structure assembled from several
modern formulations.

```text
strong Quantum Darwinism / spectrum broadcast structure:
    objectivity means many fragments carry the same classical record
    while nonclassical information is excluded from that public sector.

Wigner-friend erasure / decoherence analyses:
    moving the cut means changing which memory and environment degrees
    are under coherent control, and which have become uncontrolled
    classical records.

observer-algebra language in gravity:
    the operational primitive is the algebra accessible to an observer.

quantum secret sharing / data hiding / noiseless subsystems:
    the private side is defined by what unauthorized access algebras
    fail to decode, even when a larger algebra succeeds.
```

The synthesis used here is:

```text
access cut = specified accessible record algebra
           = public center
             + decoding-limited block
             + private commutant/noiseless complement.
```

Here the `decoding-limited block` means information that has coupled into
the record/control interface and may be recoverable from large, late, or
authorized access, while remaining below the recovery threshold for the
current small fragments.

The newer Wigner-friend and observer-algebra papers sharpen the
interpretation.  They support treating the Heisenberg cut as a statement
about operational access: which records are public, which degrees are
recorded and still below the decoding threshold, and which degrees are
still invisible to the current record algebra.

## Novelty Claim

The conservative novelty claim is an access-profile synthesis of standard
ingredients:

```text
public center:
    what many fragments can redundantly recover.

private hiding:
    what the current record channel makes unrecoverable, quantified
    against the trivial recovery baseline.

access motion:
    how the conclusion changes when the observer/control algebra is
    enlarged.

latency:
    how long physical dynamics need before the private diary can enter
    the authorized algebra.

decoder complexity:
    how hard it is to perform the recovery once recovery is possible in
    principle.
```

The useful combined statement is:

```text
The same unitary world can contain objective public records of X while
also keeping a noncommuting diary D unrecoverable from those records;
whether D later becomes recoverable is a question about enlarged access,
latency, and decoder resources.
```

The strongest defensible contribution is a representation claim: a
Heisenberg cut can be represented by an access algebra whose public
center, private commutant, decoding-limited block, latency, and decoder cost
are separate operational quantities.  This turns vague cut language into
channel inequalities and diagnostics.

## Prior Art Boundaries

Two of the five axes have close prior art and should be treated as
borrowed structure.

```text
scrambling -> recovery edge:
    Garcia, Bu, and Jaffe introduce a resource theory of scrambling with
    Pauli growth and OTOC magic as monotones, and use those monotones to
    bound decoding fidelity in Yoshida-style black-hole recovery.  This
    note imports the operational link between scrambling resources and
    recovery.

access-relative complexity:
    Python's Lunch defines restricted vs unrestricted decoding complexity
    C_R, C_U and studies when C_R >> C_U.  Decoder complexity as a
    property of the access algebra is imported from that framework.

public/private complementarity:
    Renes' complementarity framework relates classical information
    transmission, privacy, and complementary observables.  This is close
    prior art for the public-label/private-complement axis pair.

Darwinism/scrambling interface:
    Recent Quantum Darwinism work studies accessible information in
    environment fragments and the competition between redundant classical
    records and information scrambling.  This is prior art for connecting
    the decoherence layer to the scrambling/recovery layer.
```

The residual, defensible contribution is packaging plus one diagnostic:

```text
system-general access profile:
    assemble public objectivity, private hiding, private recovery,
    latency, and access-relative complexity into one operational
    statement across decoherence, Wigner-friend, and recovery settings.

frozen-routing test:
    an experimental discriminator between dynamical recovery and
    prearranged or nonlocal access; treat as a candidate diagnostic until
    a closer analogue is found in the scrambling literature.
```

## Added Content Over Standard Decoherence

Standard decoherence supplies the reduced public story:

```text
pointer basis selection;
suppression of interference in the reduced system/apparatus state;
stable classical records after uncontrolled environmental monitoring;
redundant fragments carrying X in Darwinism/SBS regimes.
```

The access-profile formulation adds six pieces:

```text
1. Algebraic location:
       identify the public center, private blocks, and commutant.

2. Private-sector channel test:
       express hidden D as N_R close to a constant channel K_R.

3. Recovery baseline:
       compare every decoder against F_rec^e = 1/d_D^2.

4. Moving cut:
       replace R by enlarged access E R_t and recompute recovery.

5. Latency:
       bound recovery onset from locality, routing, or scrambling.

6. Decoder resources:
       separate information-theoretic recoverability from feasible
       extraction.
```

The added substance is quantitative tracking of the private complement.
The access profile asks which algebra has the diary, when that algebra
gains it, and what resources recover it.  Reduced decoherence mainly says
why `X` looks classical to observers who trace out the rest.

The six additions instantiate the five tracked quantities: public
classical objectivity, private quantum hiding, private quantum recovery,
recovery latency, and decoder complexity.  Moving the cut (item 4) is
what can turn private hiding into private recovery.

## Registers

```text
X      classical public label
D      k-qubit private diary, dim D = d_D = 2^k
A      reference purifying D
B      memory/scrambler
F_i    small public record fragments
R_t    emitted/accessed records up to depth/time t
C_t    inaccessible remainder
E      authorized side information
```

The public layer is a family of fragment channels that redundantly
recover `X`.  The private layer is a diary `D` whose purifier `A` remains
decoupled from unauthorized records and may become recoverable from
`E R_t`.

When public and private conditions are stated together, the fragments
`F_i` are small subregisters or coarse-grained fragments of the same
record family whose accessible part is denoted `R_t`.  Thus the public
and private tests refer to one access profile.

## The Inequality

Let

```text
N_t : D -> R_t
```

be the diary-to-accessed-record channel up to time/depth `t`, and let
`K_t` be a constant channel on `D`.  Define the best diary recovery from
the accessed records by

```text
F_rec^e(t)
= sup_Dec F_e[
    (id_A tensor Dec o N_t)(Phi_AD),
    Phi_A Dhat
  ].
```

For this entanglement-fidelity normalization,

```text
F_triv^e = 1 / d_D^2.
```

For average pure-state fidelity, the corresponding trivial baseline is
`1/d_D`, with the usual relation
`F_avg = (d_D F_e + 1)/(d_D + 1)`.

The core access inequality is:

```text
if || N_t - K_t ||_diamond <= epsilon(t),
then
F_rec^e(t) <= 1/d_D^2 + O(epsilon(t)).
```

For source-local finite-velocity access, Lieb-Robinson locality gives

```text
epsilon(t)
<= C_LR |X_acc| |Y_D| t exp[-mu (L - v t)]
```

for `t < L/v`, up to the usual Lieb-Robinson prefactors.  Here
`X_acc` is the access/emission support, `Y_D` is the diary support, and
the vertical bars denote their support sizes in the chosen local
factorization.  Hence

```text
F_rec^e(D from R_t)
<= 1/d_D^2 + O(C_LR |X_acc| |Y_D| t exp[-mu (L - v t)]).
```

The public/private access separation is the simultaneous profile

```text
P_guess(X | F_i) >= 1 - epsilon_pub       for many fragments F_i
F_rec^e(D from R_t) <= 1/d_D^2 + O(epsilon(t))
```

The first line is Darwinian public objectivity.  The second line is the
private-recovery obstruction.

## Discrimination Power

The inequality discriminates operational channel classes.  The basic
test statistic is the recovery excess

```text
Delta_rec(t) = F_rec^e(t) - 1/d_D^2.
```

For a source-local finite-velocity record channel, the predicted envelope
is

```text
Delta_rec(t)
<= O(C_LR |X_acc| |Y_D| t exp[-mu (L - v t)])
```

before the diary light cone reaches the access region.  An observed
recovery excess above this envelope, after statistical and calibration
errors are included, rejects that source-local finite-velocity access
model only when `v`, `L`, and the relevant supports are fixed by an
independent handle.  If the velocity and geometry are free fit
parameters, the latency envelope has limited falsification force and
serves mainly as classification language.

The most useful discrimination targets are:

```text
public-objective / private-hidden:
    P_guess(X | F_i) high
    Delta_rec(F_i) near zero

irreversible-erasure:
    P_guess(X | F_i) high
    Delta_rec(E R_t) near zero for every enlarged access tested

unitary-hidden / later-recoverable:
    P_guess(X | F_i) high
    Delta_rec(E R_t) order one after the access threshold

source-local finite-velocity routing:
    recovery onset time T_eta(L) grows at least as L/v

fast-routing or fast-scrambling:
    T_eta(N) grows logarithmically or polylogarithmically after
    coherent export is available

nonlocal, dressed, or pre-encoded access:
    recovery survives the frozen-routing test

complexity-limited recovery:
    information-theoretic F_rec^e is high while restricted-decoder
    F_rec^{e,(d)} remains low
```

Equivalently, define

```text
T_eta = min_t { F_rec^e(t) >= 1/d_D^2 + eta }.
```

Then the latency scaling of `T_eta` separates source-local routing,
fast-routing/scrambling, and pre-encoded or dressed-access mechanisms
when the geometry and velocity scale are independently specified.  The
frozen-routing test below carries the sharper burden when those
parameters cannot be pinned down.  The inequality has no direct power
against interpretations that predict the same access-channel data.  Its
force is against concrete channel stories: early source-local recovery,
irreversible diary erasure, missing coherent export, or a
decoder-complexity bottleneck.

## Interpretation

The inference rule is:

```text
high public objectivity of X
leaves open
destruction, leakage, or recovery of the private diary D.
```

More operationally:

```text
For source-local finite-velocity access, any emitted-record channel that
is still diamond-close to a constant channel on D has only trivial diary
recovery, regardless of decoder power, even if many fragments already
carry the public label X.
```

Thus the pair of observations

```text
I(X : F_i) high for many fragments
F_rec^e(D from R_t) near trivial
```

is consistent with ordinary unitary access dynamics.  It may simply mean
the private information has not reached the authorized access algebra.

Conversely, the pair

```text
I(X : F_i) high
F_rec^e(D from enlarged access E R_t) high
```

rules out any effective description in which the public-record formation
irreversibly erased `D` from the enlarged access model under test.  This
is compatible with an entanglement-breaking reduced public pointer
channel; reduced classical records often have that form.  The full
physical channel whose outputs include `E R_t` retained enough diary
information for authorized recovery.  The ruled-out operational model is:

```text
public record formed
=> private quantum complement was actually destroyed.
```

The operational role is modest: a vague claim about decoherence becomes
an experimentally checkable channel statement.

## Public Objectivity Condition

For many disjoint fragments `F_i`, require either a guessing condition

```text
P_guess(X | F_i) >= 1 - epsilon_pub
```

or a mutual-information condition

```text
I(X : F_i) >= H(X) - delta_pub.
```

Exact redundant broadcasting of noncommuting information is impossible.
The single-system statement is the no-broadcasting theorem; the
fragment/redundancy version is closer to no-local-broadcasting of quantum
correlations.  Approximate public objectivity is the Quantum Darwinism /
spectrum-broadcast-structure stability input.

Operational reading:

```text
the public part is a commuting center;
private blocks may remain outside that center.
```

## Private Hiding Condition

For an unauthorized fragment or small record algebra `F`, require

```text
|| rho_AF - rho_A tensor rho_F ||_1 <= epsilon_priv.
```

In particular, no decoder on `F` has more than trivial entanglement
fidelity, up to `O(epsilon_priv)`:

```text
F_rec^e(D from F) <= 1/d_D^2 + O(epsilon_priv).
```

In average-fidelity language, replace the trivial baseline by `1/d_D`.
The important point is that unauthorized records cannot carry order-one
coherent diary recovery.

## Source-Local Latency Inequality

Let `N_t : D -> R_t` be the diary-to-record channel induced by the
allowed records up to time/depth `t`.  Let `K_t` be a constant channel
that produces the same record state for a reference diary preparation.

For source-local emission with finite Lieb-Robinson velocity, if the
diary support is distance `L` from the access/emission region, then
standard locality estimates give

```text
|| N_t - K_t ||_diamond
<= epsilon_LR(t)
<= C_LR |X_acc| |Y_D| t exp[-mu (L - v t)]
```

for `t < L/v`, up to model-dependent constants and standard
Lieb-Robinson prefactors.

Since trace distance and diamond distance cannot be increased by a
decoder, every recovery map `Dec` obeys

```text
F_rec^e(D from R_t)
<= 1/d_D^2 + O(epsilon_LR(t)).
```

This is the access-inequality form of a standard Lieb-Robinson
consequence:

```text
before the diary light cone reaches the access channel,
the record channel is nearly constant on the diary,
and every decoder remains near trivial recovery.
```

## Fast-Scrambler Upper Bound Template

The complementary upper-bound template is Hayden-Preskill / decoupling.
Let `C_t` denote the inaccessible remainder after applying a mixing
channel and emitting `m` record qubits into `R_m`.  Recovery from
`E R_m` is possible when `A` is decoupled from `C_t`:

```text
delta(t,m)
= || rho_{A C_t} - rho_A tensor rho_{C_t} ||_1.
```

Under a reasonable design/mixing assumption,

```text
delta(t,m)
<= eta_mix(t) + c 2^{-(m-k)/2}.
```

Here:

```text
eta_mix(t)       design/mixing/export error
m                fresh emitted/accessed qubits
k                diary size in qubits
```

Then information-disturbance / decoupling gives a recovery map from
`E R_m` with fidelity loss `O(delta)`.

If

```text
eta_mix(t) <= c1 exp[-gamma (t - tau_geo)_+],
```

then a compact threshold estimate is

```text
t_rec(epsilon)
approx
tau_geo
+ max[
    gamma^{-1} log(2 c1 / epsilon),
    (k + 2 log2(2 c / epsilon)) / r
  ],
```

where `r` is the coherent record emission rate in qubits per unit time.

Geometry enters through `tau_geo`:

```text
local d-dimensional circuit/reservoir:
    tau_geo ~ L/v ~ N^(1/d)

expander or all-to-all fast-scrambling circuit:
    tau_geo ~ a log N, or polylog N with overheads

arbitrary global Haar unitary:
    tau_geo ~ O(1); nonlocality is supplied as an assumption
```

## Decoder Complexity (Assumption-Relative)

The fifth axis is computational.  Once the diary information is present in
the authorized algebra, whether it can be *extracted* is a separate
resource question from whether it is *there*.  The note tags this as
complexity-limited recovery:

```text
decoder complexity (assumption-relative):
    information-theoretic recovery fidelity is order one,
    while every decoder within a fixed resource budget stays near trivial;
    "hard" names a stated cryptographic assumption,
    and "budget" names a concrete resource such as gate or query count.
```

Two caveats keep this axis honest.

First, the hardness is conditional.  Current tools provide no
unconditional complexity lower bound on diary decoding; such a bound
would require complexity-class separations beyond current reach.  The
firmest statements are assumption-relative: Harlow and Hayden argued that
reconstructing the relevant post-Page correlations is computationally
intractable, and Aaronson sharpened the obstruction to a hardness
conditional on the existence of quantum-secure one-way functions.  So
"hard decoding" in the black-hole endpoint means *hard under standard
cryptographic assumptions*.  Where the table says "potentially
exponential," it means conjectured exponential under such assumptions.

Second, the budget must name a resource.  The obstruction concerns total
computational work, that is circuit size or query complexity to the
scrambling dynamics.  The depth-restricted proxy in the numerical
diagnostics is a convenient stand-in for a recovery-versus-resource
tradeoff; it is separate from the Harlow-Hayden / Aaronson barrier.  A
shallow-depth restriction can fail to recover for reasons unrelated to
genuine hardness.  Any complexity-barrier claim should state which
resource is bounded and under which assumption.

With both caveats, the axis is well-posed and modest: it asserts a
*separation*, namely that presence of information can coexist with
infeasible extraction, without asserting a universal latency x
decoder-complexity product law.

## When The Tradeoff Is Real

The original motivation for this note was a product law of the form
`latency x decoder complexity >= constant`.  The useful replacement is a
regime-restricted resource curve.
Yoshida-Kitaev efficient decoding is the counterexample in a controlled
scrambler/HP setting: given the access dynamics `U` and the ability to
apply its inverse `U^\dagger`, recovery is both fast (available at the
scrambling time) and cheap relative to the reservoir (polynomial in
`d_D`, hence exponential in the diary qubit count `k`, with no
reservoir-entropy scaling).  Ordinary decoherence lacks
`U^\dagger`; reversing a decohering interaction would require coherent
control of the system, apparatus, environment, and their phases.  The
counterexample shows that latency and complexity are independent axes in
some access models.

A genuine tradeoff appears in a restricted regime, fixed by one shortcut
exclusion and one structural condition.  The shortcut exclusion is:

```text
no free inverse dynamics:
    the decoder cannot apply U^\dagger for free
    (it does not know U, or cannot implement it).
```

With `U^\dagger` available the axes decouple.  In ordinary decoherence or
uncontrolled environments, latency and complexity can recouple when they
share a common cause.  Writing `C_R` and `C_U` for the restricted and
unrestricted decoding complexities (the access-relative pair of Python's
Lunch), there are three such couplings:

```text
1. time-parametrized access:
       waiting enlarges the accessible algebra,
       so C_R falls toward C_U as time increases.
       (waiting lowers complexity)

2. time-parametrized knowledge of U:
       without a U-oracle the decoder must learn U by observation;
       process-learning lower bounds tie accuracy to observation time,
       so less time forces more brute force.
       (waiting lowers complexity)

3. time-accumulated scrambling depth:
       without U^\dagger the decoder must invert U(t),
       whose circuit complexity grows with t until saturation.
       (waiting raises complexity)
```

In each case complexity is a function of latency because access,
knowledge, or inversion depth is.  A fixed agent and a fixed task are also
required: comparing `C_R` across differently situated agents gives two
separate facts.

A concrete provable form uses the locality machinery above.  In a local
geometry, before the diary light cone arrives, the record channel is
`epsilon(t) ~ exp[-mu (L - v t)]`-close to constant.  Single-shot this is
a wall: the core inequality bounds every decoder regardless of resources,

```text
F_rec^e(t) <= 1/d_D^2 + O(epsilon(t))   for t < L/v,
```

so complexity cannot help before arrival.  With many independent uses,
channel discrimination gives a regime-restricted resource curve.  Since
diamond distance is subadditive under sequential/adaptive channel uses,
an `epsilon`-sized deviation cannot be resolved with order-one advantage
until the number of uses satisfies `n epsilon = Omega(1)`.  Thus the
strategy-independent repeated-use lower bound is

```text
n >= Omega(1 / epsilon(t))
  ~ exp[mu (L - v t)].
```

For product-input, incoherent estimation strategies, the usual
shot-noise scaling gives the stronger cost

```text
n ~ 1 / epsilon(t)^2
  ~ exp[2 mu (L - v t)].
```

Each unit of earliness costs exponentially more channel uses to resolve
the leakage.  This is a repeated-use discrimination/estimation proxy; it
is separate from single-shot recovery of an unknown quantum diary.  It
replaces the abandoned product law with a regime-restricted statement:
`complexity >= f(latency)` under stated conditions.

The boundary cases, where there is no tradeoff, sharpen the claim:

```text
U^\dagger available (Yoshida-Kitaev):  fast and easy; axes decoupled.
single-shot sub-light-cone:            near-trivial recovery at any complexity.
fixed-restricted remainder:            constant-hard, time-independent.
constant channel:                      only trivial recovery.
```

## Scope And Landmarks

Core claims:

```text
1. Public objectivity is an access property of a commuting center.
2. Private quantum recovery is a separate access property.
3. Source-local finite-velocity access gives a latency lower bound.
4. Fast scrambling lowers access latency only when paired with coherent
   export/decoupling.
5. Decoder complexity is a further resource barrier after information is
   present in the authorized algebra; the barrier is assumption-relative.
```

Guardrails:

```text
1. The Lieb-Robinson recovery bound is standard locality machinery.
2. Hayden-Preskill recovery is standard decoupling machinery.
3. Quantum Darwinism already supplies the public-objectivity input.
4. The note avoids a universal time x hardness uncertainty relation.
```

The contribution is the access-profile packaging:

```text
public center
+ private hiding
+ latency lower bound
+ fast-scrambler recovery upper bound
+ decoder complexity tag.
```

Known examples support a qualitative landscape without a universal product
law like

```text
latency x decoder complexity >= constant.
```

Yoshida-Kitaev efficient decoding is an explicit counterexample, and the
conditions under which a genuine tradeoff does hold are stated in When The
Tradeoff Is Real above.

The following examples are useful landmarks.

| system | latency to authorized recovery | decoder complexity | lesson |
| --- | --- | --- | --- |
| static quantum one-time pad / secret sharing | none once authorized shares are present | simple if key/shares are labeled | static authorization |
| local reservoir or spin chain with source-local output | `L/v` up to LR tails; worst-case power law in system size | often simple once signal reaches output | waiting dominates |
| all-to-all or expander random circuit | logarithmic/polylogarithmic depth under mixing assumptions | feasible for small systems; grows with circuit/inverse description | pure-QI fast recovery |
| global Haar encoder/oracle | `O(1)` by assumption | arbitrary/global inverse may be huge or externally specified | nonlocal access assumed for free |
| post-Page black-hole / HP model | `t_scr ~ beta log S` plus `O(k)` record budget | potentially exponential or otherwise infeasible in `S` | fast access, hard decoding |

The black-hole/HP row serves as an endpoint in the access/complexity
landscape.

This table is a diagnostic guide.  The clean theorem-like content
remains:

```text
before access:
    no decoder helps;

after access and decoupling:
    a decoder exists in principle;

after complexity restrictions:
    operational recovery may still fail.
```

## Frozen-Routing Diagnostic

A useful discriminator, when the controls allow it, is the
frozen-dynamics test:

```text
normal run:
    measure private recovery from E R_t;

frozen-routing run:
    freeze internal dynamics that transports D to the access region,
    keep the record coupling fixed,
    measure private recovery again.
```

If recovery disappears, the original protocol used internal
routing/scrambling.  If recovery remains, the recovering algebra was
already nonlocal relative to the chosen source factorization, the
encoding was prearranged, or the supplied side information already
contained the diary.

This diagnostic assumes the transport dynamics can be varied
independently from the record coupling.  In systems where the same terms
both route the diary and emit the record, frozen-routing is a theoretical
comparison or a protocol-engineering target.

## Numerical Diagnostics

The note suggests four small numerical checks.

### 1. Public/private separation

Track:

```text
I(X : F_i)
```

for public fragments, and

```text
|| rho_{A F_i} - rho_A tensor rho_{F_i} ||_1
```

for private diary hiding.

Goal:

```text
public X turns on early and redundantly;
private D remains hidden from small fragments.
```

### 2. Recovery heatmap

Compute:

```text
delta(t,m)
= || rho_{A C_t} - rho_A tensor rho_{C_t} ||_1
```

over circuit depth `t` and emitted record size `m`.

Goal:

```text
show a recovery threshold surface.
```

### 3. Geometry scaling

Compare:

```text
1D chain
2D grid
expander
all-to-all random circuit
```

using

```text
tau_epsilon = min_t { delta(t,m) <= epsilon }.
```

Goal:

```text
local geometries show routing delay;
expander/all-to-all geometries show logarithmic or small-depth onset.
```

### 4. Restricted-decoder proxy

For decoder depth `d`, define

```text
F_d(t,m) = best recovery fidelity using decoder circuits of depth <= d.
```

Then plot a Pareto front:

```text
latency tau_epsilon versus decoder depth d_epsilon.
```

Depth `d` is a heuristic resource axis chosen for tractability.  The
genuine complexity obstruction is total computational work (gate or query
count) under cryptographic assumptions; see Decoder Complexity
(Assumption-Relative).  This is a diagnostic probe with no universal
theorem asserted.

## Citation Anchors

No-broadcasting and classical public information:

- H. Barnum, C. M. Caves, C. A. Fuchs, R. Jozsa, and B. Schumacher,
  "Noncommuting Mixed States Cannot Be Broadcast," Phys. Rev. Lett. 76,
  2818 (1996), arXiv:quant-ph/9511010.
- M. Piani, P. Horodecki, and R. Horodecki, "No-local-broadcasting
  theorem for quantum correlations," Phys. Rev. Lett. 100, 090502
  (2008), arXiv:0707.0848.

Classical information, privacy, and complementarity:

- J. M. Renes, "Duality of privacy amplification against quantum
  adversaries and data compression with quantum side information,"
  arXiv:1003.0703.

Quantum Darwinism and spectrum broadcast structure:

- H. Ollivier, D. Poulin, and W. H. Zurek, "Environment as a Witness:
  Selective Proliferation of Information and Emergence of Objectivity in
  a Quantum Universe," Phys. Rev. A 72, 042113 (2005),
  arXiv:quant-ph/0408125.
- W. H. Zurek, "Quantum Darwinism," Nature Physics 5, 181 (2009),
  arXiv:0903.5082.
- F. G. S. L. Brandao, M. Piani, and P. Horodecki, "Generic emergence of
  classical features in quantum Darwinism," Nature Communications 6,
  7908 (2015), arXiv:1310.8640.
- J. K. Korbicz, "Roads to objectivity: Quantum Darwinism, Spectrum
  Broadcast Structures, and Strong Quantum Darwinism," Quantum 5, 571
  (2021), arXiv:2007.04276.
- T. P. Le and A. Olaya-Castro, "Strong Quantum Darwinism and Strong
  Independence are Equivalent to Spectrum Broadcast Structure," Phys.
  Rev. Lett. 122, 010403 (2019), arXiv:1803.08936.

Quantum Darwinism, accessible information, and scrambling:

- A. Touil, B. Yan, D. Girolami, S. Deffner, and W. H. Zurek,
  "Eavesdropping on the Decohering Environment: Quantum Darwinism,
  Amplification, and the Origin of Objective Classical Reality,"
  arXiv:2107.00035.
- F. Tian, J. Zou, H. Li, and B. Shao, "Relevance between Information
  scrambling and quantum Darwinism," arXiv:2205.06939.
- P. Duruisseau, A. Touil, and S. Deffner, "Pointer states and quantum
  Darwinism with 2-body interactions," Entropy 25, 1573 (2023),
  arXiv:2309.03299.

Moving cuts, Wigner-friend records, and observer algebras:

- C. Elouard, P. Lewalle, S. K. Manikandan, S. Rogers, A. Frank, and
  A. N. Jordan, "Quantum erasing the memory of Wigner's friend,"
  Quantum 5, 498 (2021), arXiv:2009.09905.
- A. Relano, "Decoherence framework for Wigner's friend experiments,"
  arXiv:1908.09737.
- E. Witten, "Algebras, Regions, and Observers,"
  arXiv:2303.02837.
- L. Hausmann and R. Renner, "The firewall paradox is Wigner's friend
  paradox," arXiv:2504.03835.
- L. Walleghem, "Wigner's friend's black hole adventure: an argument for
  complementarity?", arXiv:2507.05369.

Lieb-Robinson locality and information propagation:

- E. H. Lieb and D. W. Robinson, "The finite group velocity of quantum
  spin systems," Communications in Mathematical Physics 28, 251 (1972).
- S. Bravyi, M. B. Hastings, and F. Verstraete, "Lieb-Robinson bounds and
  the generation of correlations and topological quantum order," Phys.
  Rev. Lett. 97, 050401 (2006), arXiv:quant-ph/0603121.

Hayden-Preskill recovery and decoupling:

- P. Hayden and J. Preskill, "Black holes as mirrors: quantum information
  in random subsystems," JHEP 09, 120 (2007), arXiv:0708.4025.
- F. Dupuis, M. Berta, J. Wullschleger, and R. Renner, "One-shot
  decoupling," Communications in Mathematical Physics 328, 251 (2014),
  arXiv:1012.6044.

Fast scrambling and random-circuit decoupling:

- Y. Sekino and L. Susskind, "Fast Scramblers," JHEP 10, 065 (2008),
  arXiv:0808.2096.
- W. Brown and O. Fawzi, "Decoupling with random quantum circuits,"
  Communications in Mathematical Physics 340, 867 (2015),
  arXiv:1307.0632.

Decoding and complexity:

- B. Yoshida and A. Kitaev, "Efficient decoding for the Hayden-Preskill
  protocol," arXiv:1710.03363.
- R. J. Garcia, K. Bu, and A. Jaffe, "Resource theory of quantum
  scrambling," Proceedings of the National Academy of Sciences 120,
  e2217031120 (2023), arXiv:2208.10477.
- D. Harlow and P. Hayden, "Quantum Computation vs. Firewalls," JHEP 06,
  085 (2013), arXiv:1301.4504.
- S. Aaronson, "The Complexity of Quantum States and Transformations: From
  Quantum Money to Black Holes," arXiv:1607.05256.
- A. R. Brown, H. Gharibyan, G. Penington, and L. Susskind, "The Python's
  Lunch: geometric obstructions to decoding Hawking radiation," JHEP 08,
  121 (2020), arXiv:1912.00228.
- A. R. Brown and L. Susskind, "Second law of quantum complexity," Phys.
  Rev. D 97, 086015 (2018), arXiv:1701.01107.

Recent recovery-versus-dynamics literature to check before external use:

- Y. Nakata and M. Tezuka, "Hayden-Preskill Recovery in Hamiltonian
  Systems," arXiv:2303.02010.
- M. Rampp and P. W. Claeys, "Hayden-Preskill recovery in chaotic and
  integrable unitary circuit dynamics," Quantum 8, 1434 (2024).

## Bottom Line

Keep this as a note because it states the access separation cleanly:

```text
Public objectivity is a redundancy statement.
Private recovery is a decoupling/access statement.
Latency is a geometry/routing statement.
Decoder hardness is a complexity statement.
```

The mathematical ingredients are standard.  The useful contribution is
to put them in one operational framework and use that framework
to prevent overinterpretation of decoherence or Quantum Darwinism.
