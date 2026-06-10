# Step 3: Natural Core Investigation

## Goal

Step 2 uses an engineered shell Hamiltonian:

```text
H_core = direct_sum_m E_m I_{D_m}
D_m = exp[S(E_m)]
```

This is enough for a minimal control model, but not a natural evaporator.

Step 3 asks:

```text
Can a standard finite many-body Hamiltonian provide the convex microcanonical
entropy window automatically?
```

If yes, the project becomes much stronger. If no, the paper should remain a
minimal engineered Hamiltonian control model.

## What Step 3 must supply

A candidate natural core must provide:

```text
1. A finite Hamiltonian H_core.
2. A computable density of states Omega(E).
3. A microcanonical entropy S(E) = log Omega(E) with a convex window.
4. Negative microcanonical heat capacity over that window.
5. Coupling operators X that can connect the working window to outgoing modes.
```

It does not initially need to reproduce the full Page curve. The first test is
thermodynamic:

```text
Does H_core naturally produce the convex intruder?
```

Only after that should we attach the radiation collision channel.

## Candidate families

### 1. Finite droplet / cluster evaporation model

Physical idea:

```text
finite clusters can have negative heat capacity during evaporation or
phase-coexistence-like regimes.
```

Pros:

```text
directly aligned with convex-intruder microcanonical thermodynamics
closest conceptual analogue to an evaporating finite object
well-known classical and finite-system literature
```

Cons:

```text
may be easier classically than quantum mechanically
quantum Hilbert space may be awkward
coupling to radiation bins may be less clean
```

Possible first model:

```text
small lattice gas / finite cluster with attractive interactions
compute DOS by exact enumeration
look for convex S(E)
```

Assessment:

```text
best physical match, but may require building a new finite-system codebase.
```

### 2. Attractive Bose-Hubbard cluster

Hamiltonian:

```text
H =
-J sum_<ij> (b_i^\dagger b_j + h.c.)
+ U/2 sum_i n_i(n_i-1)
+ V_long-range or trap terms
```

with:

```text
U < 0
fixed particle number
small number of sites
```

Physical idea:

```text
attractive bosons can cluster; finite systems can show phase coexistence,
self-binding, and anomalous microcanonical response.
```

Pros:

```text
standard quantum Hamiltonian
exact diagonalization feasible for small sites/particles
natural bosonic "droplet" interpretation
emission operator can remove/relocate particles or energy quanta
```

Cons:

```text
negative heat capacity is not guaranteed
Hilbert space grows quickly
may need long-range attraction or trap engineering
```

First test:

```text
enumerate/diagonalize small Bose-Hubbard clusters
bin eigenvalues
compute S(E), beta(E), C_mu(E)
scan U/J, site count, particle count
```

Assessment:

```text
probably the best first quantum Step 3 attempt.
```

### 3. Long-range interacting spin model

Candidate:

```text
fully connected or power-law Ising/XXZ model
H = -J/N sum_{ij} sigma_i^z sigma_j^z + transverse/XY terms + fields
```

Physical idea:

```text
long-range systems are known to have ensemble inequivalence and negative
microcanonical heat capacity.
```

Pros:

```text
finite Hilbert spaces are easy
we already have spin ED infrastructure
long-range interactions are natural for negative heat capacity
coupling operators are straightforward
```

Cons:

```text
may look close to the old fully connected XXZ setup
convex window may be small or binning-sensitive
less obviously "evaporating object" than a droplet
```

First test:

```text
modify existing XXZ ED to scan long-range Ising/XXZ parameters
compute binned DOS and convexity
identify robust convex windows
```

Assessment:

```text
lowest implementation cost; good first diagnostic.
```

### 4. Finite-system phase coexistence / Potts-type model

Candidate:

```text
finite q-state Potts model or lattice model with first-order transition
```

Physical idea:

```text
finite first-order transitions can produce convex intruders in microcanonical
entropy.
```

Pros:

```text
textbook connection to convex intruders
exact enumeration possible for small classical systems
```

Cons:

```text
classical rather than quantum unless quantized
less direct unitary dynamics
would need a separate quantum embedding for Step 2
```

Assessment:

```text
useful for intuition and benchmarks, less ideal as the final core.
```

## Recommended Step 3 path

Do not start with the hardest physical droplet.

Proceed in two probes:

```text
Probe A:
  long-range spin ED using existing code style.
  Goal: find a robust convex S(E) window.

Probe B:
  small attractive Bose-Hubbard ED.
  Goal: see whether a bosonic cluster gives a cleaner droplet-like convex
  window.
```

If neither produces a robust convex window, stop Step 3 and keep it as future
work.

If one does, attach the existing multi-mode radiation-bin Hamiltonian to that
core.

## Minimum diagnostic script

Create:

```text
sim/scan_natural_core_dos.py
```

For each candidate Hamiltonian:

```text
diagonalize H
bin eigenvalues
compute S(E)=log(histogram)
smooth S(E)
compute beta=dS/dE
compute S''(E)
flag windows with S''(E)>0 and beta>0
```

Output:

```text
candidate name
parameters
convex-window width
max S''(E)
temperature trend
plots of S(E), beta(E), C_mu(E)
```

## Decision rule

Continue Step 3 only if a candidate gives:

```text
convex window over several bins
stable under bin-width changes
not just a one-bin histogram artifact
large enough Hilbert-space support to couple to radiation
```

Otherwise:

```text
do not force Step 3 into the paper.
```

The Step 2 paper can honestly say:

```text
we engineer the density of states; finding a natural finite many-body core is
left as future work.
```

## Current probe status

The first probes have now been run.

Long-range spin scan:

```text
sim/scan_natural_core_dos.py
```

Result:

```text
no robust convex window under the current scan
```

Attractive Bose-Hubbard scan:

```text
sim/scan_bose_hubbard_dos.py
```

Result:

```text
promising finite convex window in an attractive Bose-Hubbard ring
```

Best current candidate:

```text
L=6, N=8, ring, J=0.5, U=-1, V=-0.2
```

This candidate passed 6 of 8 bin choices in two disorder seeds in the focused
scan. The result is not enough to claim a natural evaporator, but it is enough
to justify the next test: attach the reduced-density collision channel and see
whether the emission rate accelerates.

That next test has now been started in a cheaper weak-coupling form:

```text
sim/bose_hubbard_emission_markov.py
```

Result:

```text
the candidate emits, but local density/hopping couplings mostly decelerate
instead of accelerate.
```

A narrow hopping-only parameter pocket gives modest acceleration, but the
effect is not robust enough to treat as a successful natural evaporator.

This updates the Step 3 criterion. A natural core must supply:

```text
1. convex microcanonical entropy;
2. energy-lowering matrix elements that actually sample the growing final-state
   phase space.
```

The first requirement alone is not enough.

The next correction was to let the Bose-Hubbard object shrink. Instead of a
fixed-N sector, use:

```text
H_core = direct sum_N H_N
```

with particle-loss emission operators:

```text
b_i : H_N -> H_{N-1}
```

This variable-N probe is qualitatively better. It produces accelerating
emission in robust scan regions. The best grouped case across two seeds has:

```text
mu = 6
max emitted gap = 4
initial N=8 internal-energy window = [-18.5, -17]
mid / early emitted power = 1.36
```

So the updated Step 3 lesson is:

```text
fixed-sector relaxation fails;
shrinking-sector particle loss can work.
```

Detailed results:

```text
notes/step3_natural_core_probe_results.md
notes/variable_n_bose_hubbard_results.md
step3_natural_core_probe.pdf
step3_bose_hubbard_emission_probe.pdf
step3_variable_n_bose_hubbard.pdf
```

## Candidate assessment update

See:

```text
notes/step3_candidate_assessment.md
```

Current ranking:

```text
1. Attractive Bose-Hubbard / dimer aggregate:
   current leading Step 3 route, specifically in variable-N particle-loss form.

2. Potts / first-order lattice model:
   best benchmark for validating the entropy detector.

3. Long-range spin model:
   cheap probe, but weak under the first scan.

4. Finite droplet / atomic cluster:
   strongest physical analogy, hardest implementation.
```
