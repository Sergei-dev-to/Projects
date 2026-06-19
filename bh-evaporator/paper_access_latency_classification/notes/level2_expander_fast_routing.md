# Level 2 Expander Fast-Routing Module

Date: 2026-06-18

Role: result stack

Status: conditional theorem module; deterministic expander export remains open

## Question

Can the fast-routing branch be made nonempty without giving up finite
degree locality?

The clean proxy is:

```text
bounded-degree expander graph
+ graph-local chaotic/design dynamics
+ explicit record/export channel
=> location-uniform recovery in O(log S) plus export budget.
```

This is not yet a black-hole model. It is the first controlled setting
where the Level 1 recovery-window theorem can produce horizon-like
logarithmic latency.

## Main Lesson

The expander changes the routing geometry, not the information theory.

Level 1 gave:

```text
t_rec <= t_arr + Delta_export.
```

On a `d`-dimensional lattice:

```text
t_arr ~ diameter ~ S^{1/d}.
```

On a bounded-degree expander with access radius `O(log S)`:

```text
t_arr ~ O(log S)
```

provided the dynamics actually collects the diary into an export-active
block and the export channel decouples it from the remaining source.

## Definitions

Let `G_S = (V_S,E_S)` be a bounded-degree graph with `|V_S| = S` and
maximum degree independent of `S`. Each vertex carries a fixed local
Hilbert space.

Let `X_S subset V_S` be the access/emission set. Define the access radius

```text
R_X(S) = max_{y in V_S} dist_G(y, X_S).
```

For a diary region `Y`, the LR theorem gives a lower routing scale

```text
dist_G(Y,X_S)/v.
```

Define `t_arr(Y -> X_S)` as in Level 1: the first time at which the
diary-bearing subsystem is in a boundary/export-active block to which
the export condition applies.

Let the record channel have emission capacity `c_R` qudits per step.
The export budget must include the time needed to emit a record large
enough for recovery:

```text
Delta_export >= ceil((k + 2 log(1/epsilon) + log(1/delta) + O(1))/c_R)
```

plus whatever mixing/design time is needed by the active block.

## Theorem: Expander Fast-Routing Recovery

Assume:

```text
1. Graph-local finite-speed dynamics on G_S.

2. Logarithmic access radius:
       R_X(S) = O(log S).

3. Logarithmic collection:
       for every k-qudit diary region Y,
       t_arr(Y -> X_S) <= C_arr log S + O(k).

4. Export:
       after arrival, an export window satisfies
       ||rho_{R_D C} - rho_{R_D} tensor rho_C||_1 <= epsilon,
       or satisfies a second-moment decoupling/design condition implying
       the same bound after the HP record budget.
```

Then the diary is recoverable from records plus admissible side
information after

```text
t_rec <= C_arr log S
       + Delta_export
       + O(k + log(1/epsilon) + log(1/delta)).
```

If the export window emits `c_R = O(1)` qudits per step and has
constant-size local mixing overhead for a fixed-size diary, this is:

```text
t_rec = O(log S + k + log(1/epsilon) + log(1/delta)).
```

If the export window has area-sized capacity, the HP record budget is
even less constraining. If the access set or export channel has a small
throughput bottleneck, that bottleneck must be included in
`Delta_export`.

## Proof

The lower side is the same reduced-record LR statement as in Level 1:
before the diary's graph light cone reaches the access set, the
diary-to-record channel is close to a constant channel and no record
decoder can recover the diary.

For the upper side, assumption 3 supplies

```text
t_arr <= C_arr log S + O(k).
```

At arrival, assumption 4 is exactly the Level 1 export condition. By
information-disturbance / decoupling recovery, records plus admissible
side information recover the diary after the export window. Adding the
two times gives the displayed bound.

## What Is Proved And What Is Not

This theorem proves the conditional fast-routing module:

```text
log-diameter graph geometry
+ collection into an export-active block
+ decoupling export
=> logarithmic location-uniform recovery.
```

It does not prove that an arbitrary deterministic expander Hamiltonian
has the needed export property. That remains the hard deterministic
scrambling problem.

## Access-Capacity Caveat

A bounded-degree expander with a single emitting vertex has small graph
distance but can still have an export throughput bottleneck. For a fixed
small diary this may only add the HP record budget. For many diaries or
large code subspaces, the bottleneck matters.

The horizon-like version should therefore specify one of:

```text
1. an extensive or sufficiently large access/emission set X_S;
2. a record channel with enough capacity during the export window;
3. a code-subspace size small enough for the available export capacity.
```

This is the expander analogue of boundary saturation. Fast graph
diameter is not by itself enough; the private information must also be
exported into records at adequate capacity.

## Candidate Instantiations

### 1. Theorem-Backed Mixer

Concrete module:

```text
level2_expander_mixer_theorem.md
```

Choose the active-block dynamics from a known decoupling-capable class:

```text
approximate unitary two-design
random circuit with a decoupling theorem
quantum tensor-product expander
```

Then the export step follows from standard decoupling. This is the
cleanest way to prove the Level 2 branch without solving deterministic
Hamiltonian chaos.

The claim should be made construction-by-construction. A generic phrase
such as "random local circuits on expanders form designs in `O(log S)`"
is too imprecise unless tied to a specific theorem and architecture. The
safe theorem-backed route is:

```text
choose an explicit sparse/log-diameter random circuit, design, or
tensor-product-expander construction with a cited moment/decoupling
bound;

verify that its record/export partition matches the diary recovery
channel;

apply the HP/decoupling budget.
```

With that choice made, the expander geometry is the non-tautological
ingredient: it gives logarithmic access radius while retaining bounded
degree.

Literature anchors:

```text
Brown and Fawzi:
    Decoupling with random quantum circuits
    arXiv:1307.0632

Brandao, Harrow, Horodecki:
    Local random quantum circuits are approximate polynomial-designs
    arXiv:1208.0692

Harrow and Low:
    Random quantum circuits are approximate 2-designs
    arXiv:0802.1919

Harrow and Mehraban:
    Approximate unitary t-designs by short random quantum circuits using
    nearest-neighbor and long-range gates
    arXiv:1809.06957
```

This route is rigorous but partly engineered. It is the first existence
proof to write down: it proves the fast-routing mechanism is nonempty in
the logarithmic, location-uniform sense. It does not prove that a simple
fixed Hamiltonian realizes it.

### 2. Deterministic Expander Hamiltonian

Use a fixed nonintegrable local Hamiltonian or Floquet circuit on a
bounded-degree expander.

Known motivation:

```text
Barbon and Magan:
    Fast Scramblers, Horizons and Expander Graphs
    arXiv:1204.6435

Bentsen, Gu, Lucas:
    Fast scrambling on sparse graphs
    arXiv:1805.08215
```

Expected chain:

```text
bounded-degree expander
  -> operator support reaches O(S) sites in O(log S)
  -> OTOCs / operator-spreading diagnostics show fast scrambling
  -> channel decoupling/export for the diary code
  -> HP recovery from records.
```

The last arrow is the open step. OTOC growth does not automatically
prove reference-core decoupling for the emitted channel. This is the
deterministic Level 2 research target.

### 3. Expander Drift-Scrambler

A more explicit but engineered witness is a directed routing scheme on a
bounded-degree logarithmic-depth network, with local scrambling/export at
the access set.

This proves the same shape as the Level 1 directed drift-scrambler:

```text
t_arr = O(log S)
t_rec = O(log S) + export budget.
```

The caveat is reversibility and congestion. A fixed unitary permutation
cannot funnel all `S` qudits into one small access vertex in `O(log S)`
without paying capacity costs. This witness is clean only when the
access set and record channel have enough capacity, or when the claim is
restricted to a fixed small diary and a routing schedule with adequate
ancillas/records.

## Failure Modes

The expander theorem can fail even with logarithmic diameter:

```text
small access capacity:
    graph distance is small but export throughput is insufficient

operator growth without decoupling:
    OTOCs become large but R_D remains correlated with the source C

symmetry / fragmentation:
    generated record algebra remains reducible

localized or scarred dynamics on the graph:
    collection fails despite small graph diameter

oversized code subspace:
    the emitted record budget is too small for the diary/code dimension
```

These are not defects of the latency theorem. They are the conditions
under which the fast-routing branch is not realized.

## Result Shape

The clean publishable theorem, once moved into TeX, should read:

```text
Expander recovery theorem.

For a family of bounded-degree graphs with access radius O(log S),
finite-speed source-local dynamics, logarithmic collection into an
export-active block, and a decoupling-sufficient export window, any
k-qudit diary is recoverable from records plus admissible side
information in

    O(log S + k + log(1/epsilon) + log(1/delta))

steps.

Conversely, before the graph light cone reaches the access set, the
record channel is close to constant on the diary, so no decoder can
recover it.
```

This is the first controlled realization of the fast-routing branch in
the classification. The deterministic expander Hamiltonian version is
the next strengthening, not part of the conditional theorem.
