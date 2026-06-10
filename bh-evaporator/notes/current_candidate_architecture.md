# Current Candidate Architecture

## Goal

Build a non-gravitational quantum system that reproduces as much black-hole
evaporation phenomenology as possible:

```text
finite Hilbert space;
shrinking internal capacity;
S ~ M^2;
T ~ 1/M;
negative heat capacity;
accelerating evaporation;
small-quanta emission;
Page curve;
early/late radiation correlations;
fast scrambling.
```

The current best candidate is:

```text
edge-tension finite-gauge droplet
+ algebraic-expander interacting-spin scrambling
+ golden-rule boundary emission
+ coarse shell shrinkage.
```

## Module A: Thermodynamic Droplet

State sectors:

```text
dim H_L = q^(L^2).
```

Entropy:

```text
S_L = L^2 log q.
```

Mass from boundary tension:

```text
M_L = 4 sigma L.
```

Temperature:

```text
T_L = (dS/dM)^(-1) = 2 sigma / (L log q) ~ 1/M.
```

Heat capacity:

```text
C < 0.
```

Status:

```text
strong analytical core.
```

This is where the model gets the Schwarzschild-like thermodynamic package
without gravity.

## Module B: Small-Quanta Emission

Emission weights come from the microcanonical state-count ratio:

```text
p(omega) ~ rho(M - omega) / rho(M)
         ~ exp[S(M - omega) - S(M)].
```

With a 2D exterior bath:

```text
P ~ boundary * T^3 ~ L * (1/L)^3 ~ 1/L^2 ~ 1/M^2.
```

The many-cycle tracker gives:

```text
tau ~ M0^3.
```

Status:

```text
small-quanta golden-rule diagnostics work;
literal whole-shell jumps are suppressed;
many-cycle trajectory works.
```

## Module C: Shell Shrinkage

The finite-gauge sector has exact capacity factorization:

```text
H_L ~= H_(L-1) tensor H_shell(L),
dim H_shell(L) = q^(2L - 1).
```

The evaporator uses many small microscopic emissions before applying one coarse
capacity update:

```text
L -> L - 1.
```

Status:

```text
kinematics are clean;
dynamical triggering remains an imposed threshold/coarse update;
the threshold update has a reversible finite-register implementation.
```

This is one of the remaining naturalness issues.

## Module D: Page Curve and Early/Late Correlations

Given the sector dimensions:

```text
dim H_BH(L)  = q^(L^2),
dim H_rad(L) = q^(L0^2 - L^2),
```

Page's theorem predicts:

```text
S_rad(L) ~= min(L^2, L0^2 - L^2) log q.
```

Turnover:

```text
L ~= L0 / sqrt(2).
```

Random-isometry and stabilizer diagnostics confirm:

```text
Page-like radiation entropy;
old/new radiation mutual information turns on near Page crossing.
```

Status:

```text
conditional theorem plus explicit circuit realization.
```

## Module E: Fast Scrambling

The strongest current branch uses:

```text
qubits on a deterministic Margulis/Gabber-Galil-style algebraic graph;
interacting spin dynamics on graph edges.
```

Hamiltonian form:

```text
H = sum_i (h_x,i X_i + h_z,i Z_i)
  + sum_(ij in E) (J_x,ij X_i X_j + J_y,ij Y_i Y_j + J_z,ij Z_i Z_j).
```

Evidence:

```text
1. Clifford/Floquet expander circuits produce Page behavior.
2. Global fixed-Floquet algebraic graph removes graph-by-hand tuning.
3. Free Majorana Hamiltonian fails, showing interactions matter.
4. Interacting spin dynamics nearly saturates Page at L0 = 4.
5. Entanglement growth: Margulis faster than grid, close to complete.
6. OTOC/operator spreading: Margulis faster than grid, complete fastest.
```

Status:

```text
promising F14 module, still small-size and Trotterized.
```

## Current F-Status

The edge-tension gauge droplet is now roughly:

```text
F1  finite explicit quantum system                 Y
F2  unitary or purifiable evaporation              P
F3  shrinking internal state space                 P
F4  S ~ M^2                                        Y
F5  T ~ 1/M / negative heat capacity               Y
F6  accelerating evaporation                       Y
F7  emission rates from dynamics/matrix elements   P
F8  Page-like radiation entropy                    P+
F9  early/late radiation correlations              P+
F10 separates generic from gravitational           Y
F11 outgoing phase-space diagnostic                P
F12 mass-law controls                              P
F13 local-vs-scrambled removal controls            P
F14 fast scrambling                                P+
F15 autonomy / one update rule or Hamiltonian       P+
```

The `P+` labels are not official matrix entries; they mean:

```text
substantial evidence, but not yet a clean final derivation.
```

The `P+` label for F15 means:

```text
one explicit repeated-interaction architecture now exists, and the combined
bath/emission/shrinkage register rule has a state-vector isometric lift. This
is still not one autonomous time-independent Hamiltonian.
```

## Remaining Non-Naturalness

The main remaining imposed ingredients are:

```text
1. shell erosion is still an external coarse update;
2. bath coupling is not one autonomous Hamiltonian;
3. interacting spin scrambling is tested at small size;
4. random couplings are still present in the strongest Hamiltonian test;
5. no asymptotic fast-scrambling scaling theorem has been shown.
6. the full model is not yet one autonomous time-independent Hamiltonian.
```

Recent F15 improvement:

```text
the threshold/shell-shrinkage step has been represented as an explicit
reversible finite-register automaton. The update is injective when emitted
radiation bins and shrink records are retained, so the coarse shrink rule is
not intrinsically nonunitary.

The emission step has also been represented as a finite Hamiltonian block whose
matrix elements reproduce the golden-rule hard-bin distribution and compose
with the reversible shrinkage automaton.

A finite bath-density variant improves this further: the microscopic coupling
is equal for all bath microstates, and the bin weights arise from integer bath
degeneracies approximating the golden-rule density of states.

A global finite-register Floquet rule now combines bath microstate input,
hard-bin emission, emitted-energy accumulation, and conditional shell
shrinkage in one repeated rule. The map is injective over 1048576 enumerated
inputs when bath microstate and shrink records are retained. The same rule has
an explicit state-vector lift with zero norm error and inverse fidelity
0.9999999999999989.

The visible hard record in that lifted global rule has an explicit reduced
density matrix after tracing hidden bath/shrink records. It is close to the
coarse 2D-bath target, with trace distance 1.137e-03 and entropy within about
5e-06 of ln(8). This checks hard-local thermality inside the global rule, but
not Page/old-new information flow.

A tiny reference-flow diagnostic now entangles a reference with the emitted
shell label and runs the same global rule. It finds I(ref:hard)=0 while
I(ref:soft)=3.639023 and I(ref:core)=0.519860. That confirms the intended
hard-local/soft-purifying split inside the global rule.

A hard/soft entropy accounting diagnostic now puts this beside the Page curve.
For L0=8 stabilizer shell runs, the soft fine-grained radiation entropy follows
the Page capacity and returns to zero, while the coarse hard-bin observer
entropy stays monotone. This makes explicit that hard thermal entropy is not
the Page entropy.

A small L0=3 integrated state-vector diagnostic now places core scrambling,
soft shell records, visible hard bins, and hidden bath purifiers in one pure
state. Scrambled margulis/grid runs show near-Page soft entropy and old/new MI;
no-scrambling fails the soft Page diagnostic while hard bins remain locally
thermal. This is the current strongest F8/F9/F15 merger.

A larger thresholded sparse state-vector diagnostic now adds microscopic
emissions and an emitted-energy accumulator. Shell transfer is triggered when
the accumulator crosses threshold, not imposed one shell per cycle. After eight
micro-emissions, the final branch state has mean transferred shell count
2.63671875 and complete evaporation probability 0.63671875. This is a
record-entropy diagnostic, but it directly addresses the external-shrink-
schedule weakness.

The full reduced-density version has now been pushed through a small scaling
test: L0=3, emission counts 4,5,6, margulis/grid/none controls, two seeds, and
up to 32768 branch terms. Hard entropy tracks n ln 2 to numerical precision,
while scrambled soft entropy remains well above no-scrambling at each emission
count. This is now the strongest integrated quantum diagnostic.

The current final-candidate scan adds nonuniform hard weights. The cleanest
case uses threshold=5, six microscopic emissions, and P(energy 2)=0.35. It has
exact hard entropy relative to the target distribution, mean transferred shell
count 1.117, and S_soft=2.636/2.647 for margulis/grid versus 0.362 for no
scrambling.
```

The graph itself is less of a problem now:

```text
we have a deterministic algebraic graph, not a sampled random graph.
```

The dynamics is also less of a problem than before:

```text
interacting spin Hamiltonian-like dynamics works at small size;
free Hamiltonian dynamics fails, for a clear reason.
```

## What Would Count as a Strong Result

A strong version of the result would be:

```text
Here is a finite, non-gravitational quantum system with area-like entropy,
boundary-tension energy, negative heat capacity, accelerated evaporation,
Page-like radiation entropy, early/late correlations, and fast-scrambling
interior dynamics.
```

The current architecture is close to that, but still modular:

```text
thermodynamics;
emission;
shrinkage;
scrambling;
Page behavior
```

are tested in linked components, not derived from one autonomous Hamiltonian.

## Next Decisions

Reasonable next steps:

```text
1. Strengthen F14:
   more OTOC samples, deterministic couplings, or small exact Hamiltonian
   checks.

2. Strengthen autonomy:
   combine the state-vector global rule with scrambling and explicit hard/soft
   density-matrix diagnostics.

3. Strengthen synthesis:
   write a clean model specification and state exactly which claims are
   theorem, numerical evidence, or assumption.
```

The highest-value next move is now synthesis: write the final Floquet-control
claim and decide which entries are `Y`, `Y-`, or still `P` under that standard.
