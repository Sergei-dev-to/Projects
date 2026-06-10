# Gap 2 Reduced Target

## Purpose

The deterministic fixed-Hamiltonian gap should not be phrased as:

```text
find a simple Hamiltonian that generates a full unitary design.
```

That is too strong for the result we need.  The useful target is:

```text
second-moment, cumulative, symmetry-sector decoupling for the composed
evaporation map.
```

This note records the sharper target suggested by the latest review.

## Reduced Target 1: Second Moment, Not Full Design

The Page-purity diagnostic and the second-Renyi island calculation are
second-moment statements.  Code-subspace decoupling can also be phrased at
the level of second moments or trace-distance bounds derived from them.

Thus the fixed Hamiltonian does not need to generate a full Haar design on the
active shell.  It needs enough second-moment mixing to make the wrong subsystem
decouple:

```tex
I_2(Q:X_{\rm wrong})\ll 1,
```

where

```tex
X_{\rm wrong}=R_{\rm early}
\quad{\rm before\ Page\ time},
\qquad
X_{\rm wrong}=B_{\rm rem}
\quad{\rm after\ Page\ time}.
```

Fixed higher Renyi moments still require higher moments.  They are useful for
replica diagnostics, but they should not be mixed into the minimal condition
needed for the Page-purity and code-decoupling result.

## Reduced Target 2: Cumulative Decoupling

The physical condition is not that every emission step independently behaves
like a design.  The black hole has many scrambling windows over a macroscopic
evaporation time.  The target is a composed-channel statement:

```tex
V_{E_0\to E}:
{\cal C}\to B(E)\otimes R(E_0\to E),
```

with

```tex
I_2(Q:X_{\rm wrong})\ll1
```

for the composed map.

A useful theorem shape is a contraction-and-iterate inequality:

```tex
I_2(Q:B_{j+1})
\le
\kappa_j I_2(Q:B_j)+\varepsilon_{{\rm mix},j},
\qquad
\kappa_j<1.
```

The contraction has two sources:

1. the dimension drop from removing an emitted factor;
2. in-shell mixing, which spreads the reference information so the emitted
   factor carries a representative part.

After iteration,

```tex
I_2(Q:B_m)
\lesssim
\left(\prod_{j<m}\kappa_j\right)I_2(Q:B_0)
+\sum_{j<m}\varepsilon_{{\rm mix},j}
\prod_{\ell>j}\kappa_\ell .
```

This is better matched to evaporation than a one-shot design statement.

## Reduced Target 3: Symmetry Sectors

The Cayley construction uses symmetry to make the boundary-channel weights
equal.  The same symmetry gives conserved labels.  The decoupling statement
should therefore be sectorwise:

```text
within each fixed symmetry sector, the non-charge information decouples.
```

If the radiation modes also transform covariantly under the group action, the
emission map can carry the symmetry label into the radiation.  The clean
condition is not automatic from covariance of the core operator alone; it is a
condition on the full interaction:

```tex
[U_a^{B}\otimes U_a^{R},H_I]=0.
```

Under this condition, total symmetry charge is conserved while charge can be
distributed between the remaining core and radiation.  Then the Page claim can
be stated either:

1. sectorwise, with charge treated as a superselection label; or
2. including radiation charge records, if the emitted modes carry the charge
   labels.

This is the right way to avoid pretending that exact symmetry charges are
scrambled.

## Reduced Target 4: Open-Channel Replica-Gap Form

Second-moment mixing is governed by a doubled evolution on

```tex
{\cal H}^{\otimes 2}.
```

For random circuits, Brown-Fawzi-style analyses reduce second-moment
convergence to a gap of a local Markov generator on the doubled system.  The
analogous deterministic-expander target must be stated for the open emission
block, not for closed Hamiltonian evolution alone.  A unitary map
`\rho\mapsto U\rho U^\dagger` preserves Hilbert-Schmidt distances, so its
two-copy representation cannot supply a dissipative contraction by itself.

The target is:

```text
the two-replica completely positive map induced by in-shell evolution with K_N
and weak boundary emission has a gap large enough to give O(log N)
second-moment mixing inside each symmetry sector.
```

This is a more precise problem than generic fast scrambling or full design
generation.

A more explicit formulation of this contraction target is in
`notes/gap2_open_channel_contraction.md`.

## Practical Ladder

There are three useful levels.

```text
Rung 1: theorem-backed noisy/disordered expander dynamics
    Add quenched disorder or Brownian couplings to get a provable
    second-moment contraction while keeping a sparse expander geometry.

Rung 2: deterministic Cayley expander, demonstrated numerically
    Use an explicit small Cayley/Ramanujan expander, evolve with K_N, and
    measure level statistics, OTOC decay, and emitted-history Page diagnostics.

Rung 3: deterministic Cayley expander, proven analytically
    Prove the sectorwise two-replica gap/contraction bound.
```

Rung 2 would test the actual antecedent of the paper: whether the proposed
deterministic `K_N` produces the decoupling that Section 5 currently assumes.
Rung 3 is the real theorem target.

## Current Assessment

The reduced target makes Gap 2 smaller and better posed:

```text
not full design,
not per-step Haar randomness,
not charge-blind decoupling,
but sectorwise cumulative second-moment contraction.
```

This is worth adding to the draft.  It should be presented as the precise
remaining problem for deterministic sparse Hamiltonians, not as a result we
already have.
