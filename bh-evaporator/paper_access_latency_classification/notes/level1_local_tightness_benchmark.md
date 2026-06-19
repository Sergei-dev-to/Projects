# Level 1 Local Tightness Benchmark

Date: 2026-06-18

Role: result stack

Status: conditional theorem module with concrete witnesses; chaotic export remains open

## Question

Can the source-local latency lower bound be tight in a local chaotic
model?

The target is not horizon-fast recovery. A one-dimensional or finite
dimensional local system still has a ballistic routing cost. The target
is the two-sided local statement:

```text
before the diary reaches the access region:
    no record decoder can recover it

after the diary reaches the access region and the boundary-active block
has mixed/exported it:
    records plus allowed side information recover it
```

The theorem module below shows this conditionally: once arrival and
export are supplied, the recovery time is routing/collection time plus
export budget. The remaining local-chaos question is which dynamics
actually supplies arrival and export with small overhead.

## Model Class

Use a finite one-dimensional chain of qudits with a left boundary access
region `X`.

Ingredients:

```text
source:
    qudit chain Lambda = {1,...,N}

access region:
    X = {1,...,w} near the left boundary

diary:
    k qudits deposited in a region Y at graph distance L from X

dynamics:
    finite-depth nearest-neighbor circuit layers U_t

records:
    at each step, boundary degrees in X couple to fresh record qudits
    or are swapped/emitted into R_t

side information:
    optional early reference E, independent of the diary at deposit time,
    as in the Hayden-Preskill regime
```

The record subsystem must be defined explicitly. Export means the diary
reference decouples from the remaining source:

```text
rho_{R_D C_t} approx rho_{R_D} tensor rho_{C_t}
```

so that `R_t E` admits a recovery map for the diary.

## Theorem Module

### Definition: Arrival/Collection Time

For a diary region `Y` and access region `X`, define `t_arr(Y -> X)` to
be the first time at which the diary-bearing subsystem is contained in a
boundary-active block to which the subsequent export channel applies.

This is a model-dependent upper-bound quantity. The LR theorem gives the
universal lower bound:

```text
t_arr(Y -> X) >= dist(Y,X)/v - logarithmic LR corrections.
```

For a directed conveyor, `t_arr = dist(Y,X)/v`. For an unbiased
reversible local circuit, first light-cone contact does not by itself
imply arrival/collection; `t_arr` may include a return or collection
time.

### Definition: Export Window

An export window of duration `Delta` begins at `t_arr` and implements an
isometry

```text
W: D B -> R_Delta C,
```

where:

```text
D:
    the diary subsystem at arrival

B:
    boundary-active degrees, possibly entangled with admissible side
    information E

R_Delta:
    emitted/accessed record subsystem during the export window

C:
    remaining source after the export window.
```

The export condition is:

```text
|| rho_{R_D C} - rho_{R_D} tensor rho_C ||_1 <= epsilon_exp,
```

where `R_D` purifies the diary.

### Theorem: Local Recovery Window

In a source-local finite-velocity boundary-emission model, let `D` be a
`k`-qudit diary deposited a distance `L` from the access region `X`.
Let `N_t` be the diary-to-record channel through time `t`, and let
`C_t` be the corresponding constant channel obtained from a fixed diary
preparation.

For times before the LR light cone reaches the access region,

```text
|| N_t - C_t ||_diamond <= epsilon_LR(t),
```

with

```text
epsilon_LR(t) <= C |X| |Y| t exp[-mu(L - v t)].
```

Therefore no decoder acting on the records can recover the diary with
order-one entanglement fidelity before the routing scale.

If, after an arrival/collection time `t_arr`, an export window satisfies
the export condition with error `epsilon_exp`, then there exists a
decoder

```text
R_Delta E -> D_hat
```

with entanglement-fidelity loss `O(epsilon_exp)`. If the export window is
implemented by a Haar-random unitary, approximate two-design, or any
channel satisfying the standard second-moment decoupling estimate, then
with probability at least `1-delta` the export condition holds once

```text
log d_R >= k + 2 log(1/epsilon) + log(1/delta) + O(1).
```

Consequently,

```text
t_rec <= t_arr + Delta_export,
```

where `Delta_export` is the time needed to implement the export channel
and emit a record of the displayed size.

### Proof

The lower bound is the reduced-record LR theorem. Before the access
region can be influenced by the diary, the record channel is
diamond-close to a constant channel on the diary. Post-processing cannot
increase diamond distance, and a constant channel produces a product
state across `R_D | D_hat`; its entanglement fidelity with a
`d_D`-dimensional maximally entangled diary is at most `1/d_D` up to the
LR error.

For the upper bound, consider the state at `t_arr`, when the diary is in
the boundary-active block to which the export channel applies. The export
window is an isometry

```text
W: D B -> R_Delta C.
```

If

```text
|| rho_{R_D C} - rho_{R_D} tensor rho_C ||_1 <= epsilon_exp,
```

then information-disturbance / decoupling recovery gives a decoder from
`R_Delta E` to `D_hat` with entanglement fidelity `1 - O(epsilon_exp)`.
When `W` is Haar-random, a two-design, or a channel with the same
second-moment decoupling bound,

```text
E_W || rho_{R_D C} - rho_{R_D} tensor rho_C ||_1
    <= O(d_D / d_R).
```

Markov's inequality gives the high-probability version with the usual
overhead

```text
log d_R >= k + 2 log(1/epsilon) + log(1/delta) + O(1).
```

This gives the stated recovery window.

### Interpretation

The theorem proves the local branch in conditional-export form:

```text
local finite-velocity dynamics
=> recovery time = routing time + export budget
```

The statement is tight when `t_arr = L/v + O(1)` and the export window
has size `O(k + log(1/epsilon) + log(1/delta))`.

It does not prove horizon-fast recovery on a large spatial lattice.
For a `d`-dimensional local reservoir with diameter `S^{1/d}`, the
worst-case latency remains power-law. The value of the benchmark is that
it identifies the additive term that must be carried over to a
logarithmic-diameter graph.

## Solvable Witnesses

### Corollary 1: Conveyor / Shift Circuit

A directed nearest-neighbor shift circuit with boundary emission gives
an exact sanity witness:

```text
diary at distance L
=> emitted exactly after L steps
=> perfect recovery from records
```

This saturates the latency lower bound but has no chaotic
de-protection. It is useful only as a causality/export check.

Precise version:

```text
source at time t:
    q_1(t),...,q_N(t)

one step:
    emit q_1(t) into record r_{t+1}
    shift q_{j+1}(t) -> q_j(t+1)
    inject a fixed blank state into q_N(t+1)
```

This step is an isometry from source plus a fresh blank ancilla to
source plus record. A diary initially occupying site `j` appears
unchanged in record `r_j`. Before step `j`, the record channel is exactly
constant on that diary. At step `j`, recovery is exact by reading
`r_j`.

For a width-`k` diary occupying sites `j,...,j+k-1`, exact recovery
requires records `r_j,...,r_{j+k-1}`. Thus

```text
t_rec = L + k - 1
```

in lattice units. This is the sharpest possible local upper bound for a
directed finite-velocity channel, but it carries no claim of chaotic
scrambling.

This is Corollary 1 of the theorem with:

```text
t_arr = L
Delta_export = k - 1
epsilon_exp = 0.
```

### Corollary 2: Directed Drift-Scrambler

The first nontrivial tight witness is a conveyor with internal
scrambling in the drifting cells.

Model:

```text
each site j carries a cell H_j of dimension Q;
one step applies a fixed or random unitary S_j inside each cell,
or inside a bounded comoving packet,
then shifts every cell one site left and emits the left boundary cell.
```

If the diary is deposited in cell `j`, then the full diary-bearing cell
is emitted after `j` steps. The pre-emission scrambling can be chosen to
be a two-design on the cell or packet before emission. The record then
contains the entire scrambled output, so recovery is exact from the
emitted cell if the decoder knows the circuit, or HP-style if only a
subsystem of the cell is emitted after mixing with an old entangled
block.

Result shape:

```text
before j:
    record channel is exactly constant on the diary

at/after j:
    emitted records contain the diary-bearing output
```

If the emitted subsystem has dimension `d_R` and the in-cell dynamics
satisfies the decoupling condition, then

```text
t_rec = L + O(k + log(1/epsilon) + log(1/delta)).
```

This witness is still directed and engineered. Its role is to prove that
the upper-bound branch is not empty once export is included. It is not a
claim about generic reversible local chaos.

This is Corollary 2 of the theorem with:

```text
t_arr = L
Delta_export = HP/export budget inside the emitted packet.
```

The point is not the shift itself. The point is that a finite-velocity
model can have both:

```text
constant record channel before routing
and
actual diary recovery immediately after routing plus export.
```

### Candidate 3: Dual-Unitary Local Circuit

A dual-unitary or Clifford-dual-unitary circuit is the more interesting
benchmark:

```text
finite light cone:
    no recovery before L/v

exact operator dynamics:
    candidate for computing de-protection and export after arrival
```

Dual-unitary dynamics is still ballistic, so it is not the horizon-fast
mechanism. Its role is to provide a solvable local chaotic upper bound.

Relevant literature anchors:

```text
Bertini, Kos, Prosen:
    Exact dynamics in dual-unitary quantum circuits
    arXiv:1911.11175

Rampp, Moessner, Claeys:
    From Dual Unitarity to Generic Quantum Operator Spreading
    arXiv:2210.13490

Prosen et al. / related work:
    operator entanglement and exact correlators in dual-unitary circuits
```

The needed calculation is not just an OTOC. It must show record export:

```text
remaining source C decouples from diary reference R_D.
```

Important warning:

```text
first boundary contact != diary recovery.
```

In an unbiased reversible local circuit, the diary's operator support may
spread both toward and away from the emitting boundary. Boundary OTOCs
can become order one when the left-moving light cone first reaches the
access region, while the remaining source still carries the complementary
right-moving information. Then the emitted boundary records are not a
recovering subsystem; they are only a subsystem correlated with the
diary. Full recovery from a single boundary requires either:

```text
1. a directed/drift geometry, as in the conveyor witness;
2. records that capture a complete spacetime cut of the diary's future;
3. emission from enough boundaries to collect the full causal cone; or
4. later finite-size mixing that returns the right-moving component to
   the emitting boundary.
```

Dual-unitarity may be ideal for proving statements about complete
spacetime cuts, because dual-unitary tensor networks are unitary along
tilted directions. But that is a different statement from recovery from
a single early boundary time strip. The exact export question is:

```text
which emitted record region forms a reconstructing cut for the diary,
and what remains in C?
```

If exact dual-unitary export is too rigid or model-dependent, use it as
the operator-spreading benchmark and use a random local circuit or local
design condition for the decoupling upper bound.

### Corollary 3: Local Random Circuit / Design Upper Bound

There is a second, more theorem-ready but less tight, upper-bound
route:

```text
after the diary is collected into an active block B,
run a local random circuit on that block until it forms an approximate
2-design, then emit enough qudits.
```

Known random-circuit results can supply the decoupling/export step:

```text
Brown-Fawzi:
    decoupling with random quantum circuits

Brandao-Harrow-Horodecki / later improvements:
    local random circuits form approximate t-designs
```

This gives a rigorous upper bound of the form

```text
t_rec <= t_arr + t_design(B) + O(k + log(1/epsilon)).
```

For a one-dimensional nearest-neighbor active block, `t_design(B)` may
scale with the size of `B`; this is therefore not automatically a tight
`L/v + O(1)` upper bound. It is still useful because it proves the
export/recovery half in a local model without relying on Haar randomness
as an axiom.

For the later expander version, the same design route becomes more
interesting: local random circuits on a logarithmic-diameter interaction
graph can mix much faster than a one-dimensional nearest-neighbor
architecture. This is one bridge from Level 1 to Level 2.

This is Corollary 3 of the theorem with:

```text
Delta_export = t_design(B) + emitted-record budget.
```

It supplies a rigorous export upper bound whenever the relevant active
block can be driven to a suitable approximate design.

Literature anchors:

```text
Brown and Fawzi:
    Decoupling with random quantum circuits
    arXiv:1307.0632

Brandao, Harrow, Horodecki:
    Local random quantum circuits are approximate polynomial-designs
    arXiv:1208.0692

Harrow and Mehraban:
    Approximate unitary t-designs by short random quantum circuits using
    nearest-neighbor and long-range gates
    arXiv:1809.06957

Haferkamp:
    Random quantum circuits are approximate unitary t-designs in depth
    O(n t^{5+o(1)})
    arXiv:2203.16571
```

## Failure / Control Models

The foil should be phrased in terms of generated algebra and export, not
linear Krylov span alone.

Bad wording:

```text
small operator-Krylov span => large commutant
```

Reason:

```text
the record algebra is the generated *-algebra, and a small set of
operators can generate a full matrix algebra.
```

Better failure mechanisms:

```text
symmetry or selection rule:
    generated algebra is reducible

fragmentation:
    generated algebra preserves many invariant sectors

localized single-particle dynamics:
    record orbit never reaches the diary support

collective/abelian monitoring:
    record algebra has a large commutant

Gaussian-restricted access:
    full microscopic algebra may be irreducible, but the allowed decoder
    remains inside a restricted Gaussian subtheory
```

Free fermions are not automatically a failure witness. A single Majorana
orbit that explores all Majoranas can generate the full Clifford/Majorana
algebra, up to parity-sector caveats. A free-fermion foil requires either
localized single-particle dynamics or an explicitly restricted decoder
class.

## Remaining Work

The theorem module and the directed witnesses settle the conditional
Level 1 structure. The unresolved part is not the decoupling implication
itself; it is instantiating arrival and export in a less engineered local
chaotic model.

Immediate options:

```text
dual-unitary / Clifford-dual-unitary:
    identify reconstructing spacetime cuts and test single-boundary
    export

random local circuit / local design:
    prove decoupling upper bound with standard design estimates,
    accepting a possibly larger t_design(B)

failure/control models:
    specify the access and decoder class before claiming protected or
    deep private information
```

## Immediate Decision Tree

The Level 1 proof should now be pursued as three distinct claims, not
one blurred claim.

### A. Exact Directed Tightness

Status:

```text
essentially proved by the conveyor witness
```

Content:

```text
finite velocity lower bound is saturated exactly when the dynamics
routes the diary directly into the record channel.
```

This is useful as the causality/export sanity check, but it is not
chaotic.

### B. Local Chaotic Cut Reconstruction

Status:

```text
open, dual-unitary is the natural test
```

Question:

```text
For a dual-unitary circuit, which boundary/spacetime record regions form
a reconstructing cut for a local diary?
```

Possible outcome:

```text
complete causal-cut records reconstruct exactly;
single-boundary early records do not.
```

This would be a good result. It would separate:

```text
operator visibility at the boundary
from
quantum recovery from the boundary records.
```

### C. Local Chaotic Boundary Export

Status:

```text
open, likely requires either drift, finite-size return, or a design
condition on the boundary-active block.
```

Question:

```text
When does a single emitting boundary actually decouple the diary from
the remaining source?
```

Possible upper bounds:

```text
directed/drift circuit:
    t_arr = L/v + O(k)

unbiased finite chain:
    t_arr may include return/mixing time across the remaining system

active block with local random/design dynamics:
    t_arr plus t_design(B)
```

This is the genuine export problem for local chaos.

## Relation To Level 2

Level 2 replaces the spatial lattice by a logarithmic-diameter graph:

```text
bounded-degree expander + local chaotic gates
```

The same theorem should become:

```text
t_rec = O(log S) + export budget.
```

So Level 1 supplies the local upper-bound module. Level 2 changes the
routing geometry.

### Corollary 4: Log-Diameter Transfer

Let the same boundary-emission theorem hold on a bounded-degree
interaction graph `G_S` with `S` active degrees of freedom and graph
diameter

```text
diam(G_S) = O(log S).
```

For worst-case diary deposits,

```text
dist(Y,X)/v <= O(log S).
```

The LR theorem forbids recovery before the distance-dependent routing
scale. Any model that achieves

```text
t_arr = O(log S)
```

plus an export window of size

```text
Delta_export = O(k + log(1/epsilon) + log(1/delta))
```

has location-uniform recovery latency

```text
t_rec = O(log S + k + log(1/epsilon) + log(1/delta)).
```

This is the clean Level 2 target. The expander does not remove locality;
it changes the graph diameter. The remaining dynamical task is the same
as in Level 1: prove arrival/collection and export for the chosen local
chaotic gates.
