# DVV/BFK Same-Sector Test

## Purpose

The demarcation question is whether one controlled matrix/string sector does
all of the black-hole substrate jobs:

```text
A. Entropy count:
   the sector accounts for the black-hole entropy scaling.

B. Softness:
   typical excitation spacing is Hawking-scale.

C. Emission channel:
   the sector has a microscopic splitting/emission process.

D. Hawking rate:
   the inclusive emission rate has the semiclassical scaling.

E1. Microscopic unitarity:
   the full microscopic evolution is unitary.

E2. Operational export:
   radiation records purify the shrinking sector in a Page/recovery sense.
```

The point is to avoid treating "matrix dynamics", "long strings", and
"evaporation" as separate slogans. The same-sector test asks whether the same
degrees of freedom carry the entropy, are soft, split, radiate, and export
generic information.

## Sources Compared

```text
DVV matrix string theory:
  R. Dijkgraaf, E. Verlinde, H. Verlinde,
  "Matrix String Theory",
  https://arxiv.org/abs/hep-th/9703030.

BFK Schwarzschild Matrix evaporation:
  T. Banks, W. Fischler, I. R. Klebanov,
  "Evaporation of Schwarzschild Black Holes in Matrix Theory",
  https://arxiv.org/abs/hep-th/9712236.

DVV 5D black holes and matrix strings:
  R. Dijkgraaf, E. Verlinde, H. Verlinde,
  "5D Black Holes and Matrix Strings",
  https://arxiv.org/abs/hep-th/9704018.

BFKS Matrix Schwarzschild state count:
  T. Banks, W. Fischler, I. R. Klebanov, L. Susskind,
  "Schwarzschild Black Holes from Matrix Theory",
  https://arxiv.org/abs/hep-th/9709091.

KS dimensional extension:
  I. R. Klebanov, L. Susskind,
  "Schwarzschild Black Holes in Various Dimensions from Matrix Theory",
  https://arxiv.org/abs/hep-th/9709108.

Black-zero-brane Page-curve model:
  A. Choudhury, D. Laurenzano,
  "Entanglement Entropy for the Black 0-Brane",
  https://arxiv.org/abs/2407.13336.

Boltzmann D0 Matrix black holes:
  T. Banks, W. Fischler, I. R. Klebanov, L. Susskind,
  "Schwarzschild Black Holes in Matrix Theory II",
  https://arxiv.org/abs/hep-th/9711005.

D0 statistical mechanics:
  H. Liu, A. A. Tseytlin,
  "Statistical mechanics of D0-branes and black hole thermodynamics",
  https://arxiv.org/abs/hep-th/9712063.
```

## DVV Matrix String Theory

### What It Gives

DVV derive the matrix-string long-string sector explicitly.

In the IR limit, commuting matrices reduce to eigenvalue fields. Gauge
invariance allows eigenvalues to be permuted around the spatial circle, so the
Hilbert space decomposes into twisted sectors labeled by partitions of `N`.
Cycles of length `n` become strings of length `n`.

The key softening fact is:

```text
oscillator modes on a length-n string have fractional 1/n moding.
```

In the large-`N` string limit, long cycles survive as finite-energy string
states. String interactions arise when eigenvalues coincide; a transposition
of eigenvalues joins or splits cycles.

### Same-Sector Grid

| Criterion | Status | Reading |
| --- | --- | --- |
| A. Entropy count | partial | Twisted sectors and symmetric-product counting give the string Hilbert-space structure. The paper is not a Schwarzschild entropy derivation by itself. |
| B. Softness | yes | Long cycles have fractional modes, giving low-energy excitations. |
| C. Emission/splitting | yes | String joining/splitting is represented by eigenvalue transpositions. |
| D. Hawking rate | outside scope | The paper derives string interactions rather than a Schwarzschild Hawking rate. |
| E1. Microscopic unitarity | yes | It is a matrix/string quantum theory. |
| E2. Operational export | outside scope | No Page/recovery-style radiation export analysis. |

## BFK Schwarzschild Matrix Evaporation

### What It Gives

BFK model a Schwarzschild black hole in Matrix theory as a metastable bound
state of many D0-branes. Hawking radiation is described as emission of small
D0 clusters.

The entropy and energy scalings are taken from the earlier Matrix-theory
Schwarzschild model. In the evaporation note they compute the Hawking rate by
assuming an `N`-independent liberation amplitude for a D0-brane or small
cluster and integrating over the light-cone phase space. The resulting rate
matches the semiclassical Hawking scaling up to an order-one coefficient.

### Same-Sector Grid

| Criterion | Status | Reading |
| --- | --- | --- |
| A. Entropy count | yes, by imported Matrix-BH model | The black-hole states obey the entropy/area and energy/entropy relations, but the evaporation note imports this structure. |
| B. Softness | yes, kinematically | The emitted D0-branes have Hawking-scale momenta in the boosted frame. The soft scale comes from the Matrix-BH kinematics rather than a DVV long-string sector. |
| C. Emission/splitting | yes | Hawking radiation is D0-brane or small-cluster liberation from the bound state. |
| D. Hawking rate | yes, conditional | The rate has the semiclassical scaling given assumptions about the matrix element. |
| E1. Microscopic unitarity | expected | Matrix theory is the microscopic unitary framework. |
| E2. Operational export | absent | No Page/recovery-style accounting of generic information in emitted records. |

## DVV 5D Black Holes and Matrix Strings

### What It Gives

DVV's 5D black-hole/matrix-string paper is the closest bridge on the
string side. It constructs effective string descriptions of extremal and
near-extremal black strings/holes within matrix theory. The relevant
state-counting sectors are symmetric products such as `S^{Nk} T^4`, with
left- and right-moving excitations reproducing black-hole entropy formulae.

The non-extremal discussion explicitly says that the description can in
principle study excitation spectra, absorption, and emission processes.

### Same-Sector Grid

| Criterion | Status | Reading |
| --- | --- | --- |
| A. Entropy count | yes | Effective string ensembles reproduce extremal and near-extremal entropy formulae. |
| B. Softness | yes | Long effective strings allow low-energy modes, with continuous spectrum in the decompactification limit. |
| C. Emission/splitting | plausible | The setup is designed for absorption/emission dynamics, but the checked sections do not give a full evaporation calculation. |
| D. Hawking rate | not in checked sections | Related D-brane absorption/emission results are cited, but this source does not by itself give the Schwarzschild rate. |
| E1. Microscopic unitarity | yes | It is a matrix-string/D-brane microscopic description. |
| E2. Operational export | absent | No Page/recovery-style generic export analysis. |

## BFKS/KS Matrix Schwarzschild State Count

### What It Gives

The BFKS state-count paper is the missing bridge between the evaporation
paper and the long-string story.

Its central move is to choose the DLCQ longitudinal momentum cutoff `N` at
the minimal value needed to resolve the black hole. Kinematics gives

```text
N_min ~ M R_s ~ S_BH.
```

The Matrix Hamiltonian at fixed `N` then gives an energy-entropy relation
`E(N,S)`, and the DLCQ relation `E = M^2 R/N` converts this into the
Schwarzschild mass-entropy relation after setting `N ~ S`.

For the controlled eight-dimensional case, the required low-temperature
equation of state is supplied by a multiply wound 3-brane sector. The
important point for this note is the softening mechanism. The multiply wound
brane has interconnected sheets encoded by holonomies. After T-duality it is
an array of 0-branes, and strings between them carry fractional winding. In
the original variables this means momenta quantized in units

```text
2 pi / (N_i Sigma_i)
```

rather than `2 pi / Sigma_i`. The thermal equation of state remains valid
down to

```text
T_crit ~ (N V_d)^(-1/3),
```

where the entropy is of order `N`. This is the same structural mechanism as
long-string softness: connectivity spreads modes over an enlarged effective
length/volume and lowers their gap.

The same paper also gives the evaporation picture used by BFK: the black hole
is a metastable bound state of `N` 0-branes spread over the torus; large
oscillations allow small clusters to break off. Boosting a Hawking quantum
back to the Matrix frame gives `p_- ~ 1/R`, so emission occurs a few 0-branes
at a time.

The KS extension applies the same strategy in other dimensions by importing
equations of state from near-extremal Dirichlet branes. In some cases the
effective description becomes explicitly string-like; for `d=5`, the entropy
has the form of dynamical strings with an effective tension

```text
T_eff ~ 1/(N g^2),
```

consistent with fractional instanton number `1/N`.

### Same-Sector Grid

| Criterion | Status | Reading |
| --- | --- | --- |
| A. Entropy count | yes, at scaling level | `N_min ~ S_BH`; SYM/brane equations of state reproduce Schwarzschild mass-entropy scaling. |
| B. Softness | yes, through winding/fractionation | Multiply wound branes and fractional momentum/winding keep the thermal description valid at `S ~ N`. |
| C. Emission/splitting | yes, in D0-cluster variables | Hawking emission is small 0-brane cluster liberation from the metastable bound state. |
| D. Hawking rate | in companion BFK paper | The state-count paper sets the kinematics; BFK estimates the rate from cluster emission. |
| E1. Microscopic unitarity | expected | Matrix theory is the unitary microscopic framework. |
| E2. Operational export | absent | No Page/recovery-style argument that emitted clusters carry generic microstate information. |

### Dictionary Reading

BFKS/KS do narrow the dictionary gap. The Schwarzschild Matrix state-count
sector lands as a hybrid matrix/brane thermodynamic sector whose
low-temperature validity relies on winding, holonomy, and fractionated
momentum.

The dictionary to DVV is structural:

```text
DVV long cycle:
  permutation-connected eigenvalue sheets,
  fractional 1/n oscillator modes,
  splitting/joining by transpositions.

BFKS multiply wound brane:
  holonomy-connected brane sheets,
  fractional momentum/winding units,
  evaporation as small D0-cluster liberation.
```

The common mechanism is connectivity-induced fractionation. The remaining
weak link is the emission variable. DVV splitting is naturally a cycle/string
operation. BFKS/BFK Schwarzschild evaporation is formulated as liberation of
small 0-brane clusters from a metastable Matrix bound state. The checked
sources do not give a single variable-level derivation identifying those two
descriptions in the Schwarzschild evaporation channel.

## Comparison

| Source | A entropy | B softness | C emission | D rate | E1 unitary | E2 export |
| --- | --- | --- | --- | --- | --- | --- |
| DVV matrix string | partial | yes | yes | outside scope | yes | outside scope |
| BFK Schwarzschild evaporation | yes/imported | yes/kinematic | yes | yes/conditional | expected | no |
| DVV 5D matrix strings | yes | yes | plausible | not here | yes | no |
| BFKS/KS Matrix Schwarzschild | yes/scaling | yes/fractionated | yes/D0 clusters | yes via BFK | expected | no |

## Verdict

The bridge is closer than the first pass suggested. The open part is the
emission/export dictionary.

```text
DVV gives a precise long-string/matrix-string sector with softness and
splitting.

BFK gives Schwarzschild Matrix-theory evaporation rates through D0-cluster
liberation.

DVV 5D matrix strings give a controlled effective-string black-hole sector
with entropy and near-extremal dynamics.

BFKS/KS show that the Schwarzschild Matrix state-count argument already uses
a fractionated, multiply wound brane sector; the relevant Schwarzschild
states are closer to long-string physics than to a gas of independent D0
particles.
```

The missing same-sector statement is:

```text
the long-string/matrix-string sector that gives Schwarzschild entropy and
softness is also the sector whose microscopic splitting/emission channel gives
the Hawking rate and exports generic information.
```

The closest bridge is the chain:

```text
DVV matrix-string long sectors
  -> DVV black-hole effective strings
  -> BFKS/KS fractionated Schwarzschild Matrix state count
  -> BFK Schwarzschild Matrix-theory evaporation
```

The weak link is the dictionary between BFKS/BFK's emitted D0-cluster
variables and DVV's long-string/symmetric-product splitting variables.

## Demarcation Consequence

This is useful for the original program.

```text
ordinary quantum information supplies Page/recovery once a channel is supplied;
matrix theory supplies relation dynamics and D0-cluster emission;
matrix string theory supplies long-string softness and string splitting;
the controlled unity of Schwarzschild entropy, softness, Hawking-rate emission,
generic export, and geometry remains the holographic/string-theory substrate
question.
```

The demarcation boundary is now sharper:

```text
Can one identify the same microscopic sector across the entropy calculation,
the softness mechanism, and the evaporation channel?
```

If yes, the black-hole substrate mechanism is already present in Matrix/string
theory. If no, the need for the full holographic dictionary is the boundary.

## Next Narrowing Step

The next useful step is no longer a broad read. It is a dictionary test:

```text
Can the small D0-cluster emission channel in BFKS/BFK be rewritten as a
splitting/joining process of the fractionated/wound sector that supplies the
entropy and softness?
```

That is the two-end gap:

```text
left end:
  fractionated/wound Matrix sector gives S_BH and T_H.

right end:
  small D0 clusters carry Hawking radiation away.

missing middle:
  a controlled map from the fractionated sector's microscopic labels to the
  emitted cluster channel, with enough information-flow control to discuss
  generic export rather than only energy and rate.
```

That is the exact dictionary issue left by this pass.

## Pushed Dictionary Pass

The bridge can be pushed further using two additional facts from the checked
sources.

### 1. The Middle Bridge Exists Structurally

BFK's evaporation paper says more than "a D0-brane leaves." In the
eight-dimensional BFKS background, the typical black hole is a lattice of
D0-branes connected by strings on a 3-torus, and energetic considerations
leave only `O(1)` nearest-neighbor strings attached to a given D0-brane. The
liberation amplitude is therefore argued to be `N`-independent: a finite
number of connecting degrees fluctuate off, and the D0-brane or finite
D0-cluster becomes a Hawking quantum.

DVV matrix string theory supplies the matching string-language object. A
finite D-particle charge `q_0` is represented by electric flux and breaks

```text
U(N) -> U(N - q_0) x U(q_0).
```

The finite `U(q_0)` sector becomes a short-string sector whose oscillations
decouple at large `N`; its constant modes describe D-particles and their bound
states. DVV also explain how such D-particles acquire finite light-cone
momentum: the short string is attached to a long string. In that description,
the attachment is represented by a transposition between a long-string
eigenvalue and a short-string eigenvalue, with local `U(2)` enhancement at the
meeting point.

So the best current dictionary is:

```text
BFKS fractionated/wound sector:
  connected N-sheet Matrix/brane sector with soft fractional modes.

DVV D-particle sector:
  finite-rank U(q_0) short-string/electric-flux sector.

BFK emitted cluster:
  the same finite-rank sector after the connecting strings to the large
  fractionated sector have decoupled.

Emission:
  detachment of a short-string/D-particle sector from a long/fractionated
  sector, equivalently block splitting
      U(N) -> U(N-q_0) x U(q_0)
  with q_0 finite as N -> infinity.
```

This is a substantial bridge. It places the emitted D0 cluster inside a known
finite-rank sector of matrix string theory.

### 2. The Exact Schwarzschild Calculation Is Still Missing

The bridge is structural because the papers use adjacent regimes and adjacent
variables:

```text
DVV:
  controlled matrix-string sector;
  explicit long/short string dictionary;
  explicit splitting/joining twist operator.

BFKS:
  Schwarzschild Matrix state count;
  multiply wound/fractionated soft sector;
  D0 lattice picture in the controlled D=8 case.

BFK:
  Schwarzschild Hawking rate from finite D0-cluster liberation;
  N-independent liberation amplitude assumed from finite local attachment.
```

The missing exact step is a single Schwarzschild-sector operator calculation:

```text
V_{q_0}:
  H_frac(N, E)
    -> H_frac(N-q_0, E-omega) tensor H_short(q_0, omega, p)
```

where `V_{q_0}` is obtained from the Matrix Hamiltonian or from the
matrix-string twist/electric-flux detachment vertex. The rate condition is

```text
microcanonical average of V_{q_0}^\dagger V_{q_0}
  = BFK/Hawking inclusive rate.
```

This would turn BFK's liberation amplitude into a derived splitting amplitude
of the fractionated sector.

### 3. The Export Endpoint Has a New Support But Not a Closure

Choudhury--Laurenzano (2024) analyze entanglement entropy for the black
0-brane and obtain a Page curve for emitted D0-brane radiation. The useful
ingredient for this note is their Hilbert-space decomposition for a partially
evaporated black hole:

```text
H_E = direct sum over E'
        H_BH(E-E') tensor H_rad(E').
```

They justify the factorization by the same flat-direction decoupling: once
D0-branes have separated, they are radiation degrees of freedom. Their
calculation then tracks emission-number probabilities `p_m(t)` and obtains a
Page-curve profile for the radiation entropy.

For the same-sector test this is evidence that the D0-emission picture can be
put into Page-curve bookkeeping. The microstate-resolving Kraus map from the
BFSS Hamiltonian remains the export calculation. The remaining export
condition is:

```text
the detachment operators V_{q_0} must be typical enough on H_frac(N,E)
that repeated emissions transfer generic microstate information beyond
energy, D0 number, and momentum.
```

Equivalently, one needs a second-moment statement for `V_{q_0}` on the
microcanonical fractionated sector. A useful target is:

```text
rate:
  first moment / inclusive norm reproduces Hawking power.

export:
  second moment is close to a smooth ETH or two-design form on H_frac(N,E).
```

If the second moment is generic after scrambling, Page/Hayden-Preskill export
follows by standard decoupling. If it is low-rank or tied only to a few
collective labels, the Matrix/string sector gives Hawking thermodynamics
without a microscopic export proof.

### 3a. Conditional Export Lemma

This can be stated as a conditional theorem in the language already used in
the Hamiltonian draft.

Let `H_N` be the microcanonical fractionated Schwarzschild Matrix sector and
let

```text
V_m: H_N -> H_{N-q_m} tensor R_m
```

be the detachment map for a resolvable emitted record `m`, including D0
cluster number, momentum, and energy bin. Suppose:

```text
1. inclusive rate:
   sum_m V_m^\dagger V_m is smooth on H_N and reproduces the BFK/Hawking
   rate after microcanonical averaging;

2. scrambling between emissions:
   the remaining fractionated sector mixes on the emission time scale or
   before the next information-bearing emission;

3. second moment:
   the centered matrix elements of V_m between microcanonical bases have an
   ETH/two-design second moment, with no large protected subspace invisible
   to all emitted records.
```

Then the emitted D0 records implement the usual Page/Hayden-Preskill export
channel: after the emitted record entropy exceeds the diary size plus the
remaining decoupling budget, the diary is recoverable from the radiation
records. In this formulation:

```text
first moment  -> Hawking thermodynamics;
second moment -> generic information export.
```

So the same-sector program has one sharp mathematical target: compute or
justify the second moment of the finite-rank detachment vertex in the
fractionated Schwarzschild Matrix sector.

### 4. Current Best Answer

The strongest statement now available is:

```text
Schwarzschild Matrix theory already contains a fractionated soft state-count
sector, and matrix string theory already contains finite-rank D-particle
short-string sectors that attach to and detach from long strings. BFK's
finite D0-cluster Hawking emission fits that structure as detachment of a
finite-rank sector from the large fractionated sector.
```

The remaining calculation is sharply localized:

```text
derive the detachment vertex V_{q_0} in the Schwarzschild Matrix sector and
check its first and second moments.
```

That is how the demarcation question becomes technical. The state count,
softness, and emission channel are now plausibly in one Matrix/string
substrate. The open part is the strength of the emission channel as an
information-export map.

### Source Added

```text
Choudhury, Laurenzano,
"Entanglement Entropy for the Black 0-Brane",
https://arxiv.org/abs/2407.13336.
```

## Terminal Push: What the Literature Actually Leaves Open

The additional pass through BFKS II and Liu--Tseytlin changes the status of
the problem from "find the bridge" to "compute one hard vertex."

### BFKS II: The Evaporation Vertex Was Already the Open Problem

BFKS II is the clearest statement of the Boltzmann D0 picture. Its ingredients
are:

```text
black hole:
  Boltzmann gas of distinguishable D0-brane variables;

distinguishability:
  a metastable classical Matrix background breaks the permutation gauge
  symmetry and tethers each D0-brane to a background cell;

entropy:
  the D0 gas gives S ~ N;

size:
  virial balance gives R_s^(D-2) ~ G_D N;

Hawking quantum:
  a single D0-brane has the boosted Hawking kinematics.
```

In the controlled `D=8` example, the background is a D0 lattice on a 3-torus.
Off-diagonal charged fields connect nearby sites. The low-energy background
has `O(1)` links per D0-brane, each at the Hawking scale, giving background
entropy of order `N`. This is the same local attachment picture used by BFK.

BFKS II also identifies the missing calculation: Hawking emission should be a
quantum fluctuation erasing the `O(1)` strings/background links that interact
with a given D0-brane. They state that they cannot estimate the probability
for those strings to disappear. BFK later assumes the resulting liberation
amplitude is `N`-independent and fixes its dimensional size.

So the old literature already localizes the vertex:

```text
local background-link deletion around one D0 site
  = finite-rank D0 detachment
  = Hawking emission candidate.
```

### Liu--Tseytlin: First-Moment Support

Liu--Tseytlin supply the most useful Hamiltonian-level support for the
inclusive thermodynamics. They replace the leading D0 interaction

```text
v^2 + v^4/r^(D-4)
```

by a Born--Infeld-type all-loop effective D0 action/Hamiltonian. In the
mean-field/statistical-mechanics treatment this produces:

```text
effective absorbing center for D > 5;
temperature-dependent size b ~ (N beta^-1)^(1/(D-4));
Boltzmann partition function behaving like distinguishable particles on a
transverse space of Schwarzschild size;
S ~ N and the Schwarzschild mass-entropy relation.
```

This supports the first moment of the detachment channel: the D0 interaction
Hamiltonian has the right scaling structure to reproduce Schwarzschild
thermodynamics and to make finite-D0 liberation a plausible Hawking process.

It does not supply the microcanonical matrix elements of the local link
deletion operator. It gives the effective mechanics and the thermodynamic
phase-space measure.

### Minimal Moment Calculation

Let `a = 1,...,N` label the background-tethered D0 sites and let `m` label
the resolvable emitted record: D0-cluster size `q`, momentum bin, and energy
bin. A finite-rank detachment channel has local pieces

```text
V_{a,m}: H_frac(N,E)
  -> H_frac(N-q,E-omega_m) tensor R_m.
```

The inclusive channel is

```text
V_m = sum_a V_{a,m}
```

or, after the BFK incoherence assumption,

```text
Gamma_m = sum_a V_{a,m}^\dagger V_{a,m}.
```

Locality of the background attachment gives

```text
||V_{a,m}||^2 = O(1) in N
```

for fixed `q` and Hawking-scaled momentum. Summing over sites gives the BFK
factor `N`. With the phase-space integral and the dimensional estimate

```text
|A(q,y)|^2 ~ G_D
```

one recovers the light-cone Hawking emission scaling quoted by BFK:

```text
dN_emit/dx^+ ~ R (G_D N)^(-2/(D-2)).
```

This is the first moment:

```text
microcanonical average of sum_m Gamma_m
  = Hawking inclusive rate.
```

The second moment is the export question. Define centered matrix elements
between microcanonical bases

```text
(V_m)_{beta r, alpha}
  = <beta; r_m | V_m | alpha>.
```

The Page/export condition is an ETH-like statement:

```text
E[(V_m)_{beta r, alpha}
  overline{(V_n)_{beta' r', alpha'}}]

  ~ delta_mn delta_{rr'} delta_{alpha alpha'} delta_{beta beta'}
    F_m(E,omega)/dim H_frac(N,E)
```

up to smooth energy dependence and symmetry constraints. This condition says
that the emitted D0 records sample the microcanonical sector like generic
few-body operators after scrambling. With the usual decoupling theorem, it
gives Page/Hayden-Preskill export.

The first moment follows from rate and phase space. The second moment remains
uncomputed in the checked Matrix/string literature.

### Why the Page-Curve Source Does Not Close the Vertex

The 2024 black-zero-brane Page-curve paper gives a consistent factorized
Hilbert-space bookkeeping for already emitted D0-branes:

```text
H_E = direct sum_E' H_BH(E-E') tensor H_rad(E').
```

Its entropy is controlled by the emission-number probabilities `p_m(t)`.
That confirms that the D0-emission picture can be organized into Page-curve
bookkeeping once a unitary emission process and factorization are assumed.

The vertex-level question is finer:

```text
which initial microstate components control the emitted D0 record?
```

The Page-curve bookkeeping tracks the probability distribution over emitted
D0 number and momenta. The detachment-vertex second moment tracks whether
those records carry a generic purification of the initial microstate.

### Current Endpoint

There is no broader literature gap left to search before doing real work. The
searched chain now says:

```text
BFKS/KS:
  fractionated Schwarzschild Matrix state count and soft scale.

BFKS II:
  tethered Boltzmann D0 variables and local background-link attachment.

DVV:
  finite-rank D-particle short-string sectors and long/short attachment.

BFK:
  finite D0-cluster liberation gives Hawking rate if |A|^2 ~ G_D.

Liu--Tseytlin:
  effective D0 Hamiltonian/stat mech supports Schwarzschild first-moment
  thermodynamics.

Choudhury--Laurenzano:
  emitted D0-brane Hilbert-space bookkeeping gives a Page-curve model.
```

The remaining daylight is one calculation:

```text
derive or numerically test the second moment of the local D0 detachment
operator in a chaotic Matrix black-hole sector.
```

Possible attacks:

```text
1. Analytic:
   start from the DVV twist/electric-flux long-short attachment operator,
   dress it by the BFKS background, and estimate its ETH second moment.

2. Numerical:
   in BFSS/BMN truncations, identify escaping-eigenvalue events and measure
   whether the outgoing eigenvalue/cluster records distinguish random initial
   microstates beyond energy and conserved charges.

3. Demarcation:
   state the boundary as first-moment thermodynamics versus second-moment
   export. The former is supported by Matrix/string literature; the latter is
   the unresolved microscopic information-flow question.
```

At this point I do not see another literature-only move that would materially
advance the result. The next advance needs either the analytic vertex estimate
or a numerical proxy for the second moment.
