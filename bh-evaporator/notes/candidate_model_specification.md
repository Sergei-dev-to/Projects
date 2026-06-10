# Candidate Model Specification

## Name

Working name:

```text
Edge-Tension Expander Evaporator
```

## Purpose

Construct a finite, non-gravitational quantum evaporator that reproduces the
black-hole evaporation phenomenology package:

```text
S ~ M^2;
T ~ 1/M;
C < 0;
P ~ 1/M^2;
finite evaporation time ~ M0^3;
shrinking internal state space;
Page-like radiation entropy;
early/late radiation correlations;
fast scrambling.
```

The model is not intended to be a real black hole. It is intended to separate:

```text
generic quantum/statistical evaporation phenomenology
```

from:

```text
genuinely gravitational mechanisms.
```

## Parameters

```text
L:
  droplet size.

q:
  finite gauge/state-counting base.

sigma:
  boundary tension.

d:
  exterior bath dimension.

G_L:
  deterministic algebraic expander-style graph on active internal degrees of
  freedom.

H_scr(L):
  interacting spin Hamiltonian on G_L.

N_h(L):
  bath degeneracy for emitted bin h.
```

Default phenomenology choice:

```text
d = 2.
```

This gives:

```text
P ~ M^-2,
tau ~ M0^3.
```

## Internal Droplet Sectors

The active internal sector at size `L` is:

```text
B_L
```

with:

```text
dim B_L = q^(L^2).
```

Entropy:

```text
S_L = log dim B_L = L^2 log q.
```

The exact shell factorization is:

```text
B_L ~= B_(L-1) tensor Shell_L,
dim Shell_L = q^(2L - 1).
```

## Mass and Temperature

Mass is boundary tension:

```text
M_L = 4 sigma L.
```

Temperature is microcanonical:

```text
T_L = (dS/dM)^(-1)
    = 2 sigma / (L log q).
```

Therefore:

```text
T_L ~ 1/L ~ 1/M.
```

Heat capacity is negative:

```text
C = dM/dT < 0.
```

## Scrambling Dynamics

The internal scrambling Hamiltonian is:

```text
H_scr(L)
  = sum_i (h_x,i X_i + h_z,i Z_i)
  + sum_(ij in G_L) (J_x,ij X_i X_j
                    + J_y,ij Y_i Y_j
                    + J_z,ij Z_i Z_j).
```

The graph `G_L` is the active restriction of a deterministic
Margulis/Gabber-Galil-style algebraic graph.

This module is responsible for:

```text
fast internal scrambling;
typicality needed for Page-like shell emission;
rapid operator spreading relative to a local grid.
```

## Bath and Emission

For emitted hard bin `h` with energy `omega_h`, the target density is:

```text
w_h(L) ~ omega_h^(d-1) exp[S(M_L - omega_h) - S(M_L)].
```

The finite bath has degeneracies:

```text
N_h(L) / sum_k N_k(L) ~= w_h(L) / sum_k w_k(L).
```

The finite emission Hamiltonian is:

```text
H_emit(L) = g sum_(h,a) ( |h,a><in| + |in><h,a| ),
```

where:

```text
a = 1,...,N_h(L).
```

Thus:

```text
P(h | emit) = N_h / sum_k N_k.
```

The golden-rule weights come from:

```text
equal microscopic coupling
times
finite bath density of states.
```

## Bookkeeping and Shrinkage

Registers:

```text
A:
  emitted-energy accumulator for the current shell.

R:
  hard radiation record.

Q:
  soft/shrink record.
```

Each emission updates:

```text
A -> A + omega_h.
```

The shell gap is:

```text
Delta M = M_L - M_(L-1) = 4 sigma.
```

If:

```text
A < Delta M,
```

then `L` is unchanged.

If:

```text
A >= Delta M,
```

then apply:

```text
L -> L - 1,
A -> A - Delta M,
Shell_L -> Q.
```

The bookkeeping map is reversible when:

```text
emitted bin;
shrink record;
shell label
```

are retained.

## One-Cycle Update

The repeated-interaction update is:

```text
U_cycle(L) = U_bookkeep U_emit(L) U_edge(L) U_scramble(L).
```

Interpretation:

```text
U_scramble:
  mixes internal droplet information.

U_edge:
  makes boundary/edge degrees typical at T_L.

U_emit:
  emits a microscopic hard bin into finite bath/radiation states.

U_bookkeep:
  updates emitted-energy accumulator and applies reversible shell shrinkage if
  threshold is crossed.
```

This is the current autonomous object:

```text
a single repeated-interaction / Floquet architecture.
```

A finite-register version of this cycle has been checked explicitly:

```text
bath microstate input
+ hard-bin emission
+ emitted-energy accumulation
+ conditional shell shrinkage
```

The full register map is injective when the bath microstate and shrink record
are retained, and the compact map has a state-vector isometric lift.

The visible hard-radiation density matrix can also be computed after tracing
hidden bath/shrink records. In the current three-emission diagnostic it is
close to the expected coarse bath distribution, with trace distance
approximately 1.1e-3.

A tiny reference-flow diagnostic entangles a reference with an emitted shell
label. The global rule sends that reference information into the soft/shrink
record when shrinkage occurs, while the visible hard record remains
uninformative about it.

The entropy accounting is therefore split:

```text
hard bins:
  coarse local thermal observer entropy.

soft/shrink records:
  fine-grained radiation degrees entering the Page diagnostic.
```

A small integrated state-vector diagnostic now realizes this split in one pure
state with scrambling core qubits, soft shell records, visible hard bins, and
hidden bath purifiers. In that diagnostic, no-scrambling fails the soft Page
test while the hard bins remain locally thermal.

A thresholded sparse state-vector diagnostic now adds microscopic emissions
and an accumulator-triggered shell-transfer rule. This shows that shrinkage can
be triggered by emitted hard quanta inside the branch structure, rather than
scheduled one shell per cycle. That diagnostic uses record entropies rather
than full reduced-density entropies.

A full reduced-density threshold scaling diagnostic now runs the same idea for
4, 5, and 6 microscopic emissions with scrambling controls. It reaches 32768
branch terms and confirms that hard entropy stays thermal while scrambled soft
entropy remains above the no-scrambling control.

The final Floquet candidate scan adds nonuniform hard weights and selects a
readable small trajectory: threshold=5, six microscopic emissions, and
P(energy 2)=0.35. This gives exact hard entropy relative to the target
distribution and a large scrambled-vs-none soft entropy gap.

It is not yet:

```text
a single time-independent Hamiltonian H_total.
```

## Observables

Thermodynamic:

```text
S_L;
M_L;
T_L;
C_L;
P_L;
evaporation lifetime.
```

Information-theoretic:

```text
S_rad;
Page crossing;
I(old radiation : new radiation);
hard-local vs hard+soft information.
```

Scrambling:

```text
entanglement growth;
OTOC/operator spreading;
grid vs Margulis vs complete controls.
```

Controls:

```text
2D vs 3D bath;
grid vs expander graph;
free Majorana vs interacting spin dynamics;
direct bin coupling vs finite bath density.
```

## Evidence Status

Analytical:

```text
S_L = L^2 log q;
M_L = 4 sigma L;
T_L ~ 1/M;
C < 0;
P ~ M^-2 for d = 2;
tau ~ M0^3;
Page crossing L ~= L0 / sqrt(2) under typicality.
```

Numerical / computational:

```text
golden-rule small-quanta trajectory;
many-cycle evaporation tracker;
finite bath-density emission;
reversible shrinkage automaton;
global register Floquet rule;
global state-vector lift;
global hard-density diagnostic;
global reference-flow diagnostic;
hard/soft Page accounting;
integrated state-vector evaporator;
threshold integrated state-vector evaporator;
threshold density scaling;
final Floquet candidate scan;
stabilizer Page diagnostics;
interacting spin Page diagnostics;
entanglement-growth graph comparison;
OTOC graph comparison;
stitched Floquet coarse simulator.
```

Assumptions / caveats:

```text
large-L typicality from small-size/circuit evidence;
finite bath density assigned rather than derived from an explicit bath
Hamiltonian;
shell shrinkage threshold is a designed repeated-interaction rule;
final Floquet-control claim not yet written as a single theorem/result with
the F-list statuses fixed;
not one time-independent Hamiltonian.
```

## Current Claim

Defensible current claim:

```text
There exists a coherent finite, non-gravitational repeated-interaction
evaporator architecture that reproduces the black-hole evaporation
phenomenology package at the thermodynamic/capacity level, with supporting
small-size quantum diagnostics for Page behavior and fast scrambling.
```

Not yet defensible:

```text
There exists one natural autonomous Hamiltonian whose dynamics derives all of
these features without modular design.
```

## Main Remaining Gaps

```text
1. Write the final Floquet-control result statement and fix the F-list statuses
   under that standard.
2. Larger-scale scrambling/Page diagnostics.
3. Microscopic derivation of bath density.
4. Less explicit threshold/shrinkage trigger.
5. Literature comparison against known non-gravitational evaporators.
```
