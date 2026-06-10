# Emergent-Distance Candidate Systems

## Purpose

We want a system where "distance" is not simply inserted as particle position,
but can be inferred from the Hamiltonian/state structure.

The target is not quantum gravity.

The target is a non-gravitational many-body system where:

```text
1. a distance/topology can be extracted from correlations or mutual information;
2. a bound cluster/size notion can be defined from that emergent distance;
3. energy loss can plausibly make the cluster shrink and heat;
4. evaporation can be modeled without returning to pure bookkeeping.
```

## Selection Criteria

Good candidates should have:

```text
1. no explicit physical particle positions;
2. a Hamiltonian simple enough to diagonalize or simulate;
3. tunable interaction structure;
4. nontrivial correlation geometry in eigenstates or thermal states;
5. a plausible size observable from the emergent correlation graph;
6. a plausible radiation/loss channel.
```

The hard criterion:

```text
Can the microcanonical temperature increase as energy is lost?
```

That is the negative-heat-capacity test.

## Candidate 1: All-To-All Spin Model With Dynamical Coupling Pattern

Hamiltonian form:

```text
H = sum_i h_i + sum_{i<j} J_ij sigma_i^z sigma_j^z
```

with:

```text
J_ij
```

drawn from, or dynamically selected by, a low-rank / modular / random pattern.

Emergent distance:

```text
d_ij ~ -log I(i:j)
```

or:

```text
d_ij ~ -log |<O_i O_j>_c|.
```

Pros:

```text
simple;
finite Hilbert space;
no particle positions;
easy to compute pair mutual information for small N.
```

Cons:

```text
ordinary all-to-all spin systems do not naturally have negative heat capacity;
distance is likely just the imposed J_ij pattern in disguise;
no natural evaporation except removing spins.
```

Verdict:

```text
Too close to the spin-chain/register problem unless J_ij is dynamical.
```

## Candidate 2: Quantum Graphity / Dynamical Graph Model

Degrees of freedom:

```text
nodes + quantum link variables A_ij
```

Hamiltonian rewards:

```text
specific valence;
cycles;
local graph structure;
matter hopping on active links.
```

Emergent distance:

```text
graph geodesic distance in the active link graph.
```

Pros:

```text
distance/locality genuinely emerges from link states;
no background spatial position required;
clusters and horizons might be graph-theoretic.
```

Cons:

```text
technically heavy;
Hamiltonians are engineered;
negative heat capacity not natural by default;
evaporation mechanism unclear.
```

Verdict:

```text
Best for emergent locality, weak for evaporation/negative heat capacity.
```

## Candidate 3: Matrix Quantum Mechanics / Eigenvalue Geometry

Degrees of freedom:

```text
N x N Hermitian matrices X_a and conjugate momenta P_a.
```

Toy Hamiltonian:

```text
H = Tr(1/2 P_a^2 + g^2/4 [X_a, X_b]^2 + optional mass/trap terms)
```

In commuting sectors:

```text
X_a approximately diagonal
```

and eigenvalues behave like emergent positions:

```text
d_mn^2 = sum_a (x_a^m - x_a^n)^2.
```

A bound clump is a cluster of eigenvalues. Evaporation is an eigenvalue
separating from the clump.

Pros:

```text
geometry is emergent from matrices/eigenvalues;
evaporation has a known analogue: eigenvalue/D0-brane emission;
negative heat capacity appears in black-hole-like matrix-model contexts;
size can be measured from eigenvalue spread.
```

Cons:

```text
gravity/holography-adjacent;
simulation is technically heavier;
quantum Hilbert space truncation needed;
not obviously "non-gravitational control" anymore.
```

Verdict:

```text
Best candidate if we want emergent distance plus virial/shrinking behavior.
```

## Candidate 4: SYK / All-To-All Majorana Model

Hamiltonian:

```text
H = sum_{ijkl} J_ijkl chi_i chi_j chi_k chi_l.
```

Emergent geometry:

```text
not spatial distance in the ordinary sense;
low-energy dynamics has nearly-AdS2 / reparametrization structure.
```

Pros:

```text
maximally chaotic;
black-hole-adjacent;
no spatial geometry in microscopic Hamiltonian.
```

Cons:

```text
negative heat capacity is not Schwarzschild-like;
thermal behavior is more AdS/JT-like;
evaporation requires coupling to baths and is already heavily studied.
```

Verdict:

```text
Too black-hole-adjacent and not targeted to Schwarzschild evaporation.
```

## Candidate 5: Critical Spin Chain With Entanglement-Distance Diagnostic

Hamiltonian:

```text
XXZ or TFIM spin chain.
```

Emergent distance:

```text
d_ij ~ K / sqrt(I(i:j))
```

or similar mutual-information rule.

Pros:

```text
well studied;
easy numerics;
critical phases can produce metric-like mutual-information distance.
```

Cons:

```text
the chain geometry is already present;
negative heat capacity not natural;
evaporation again becomes site removal.
```

Verdict:

```text
Good diagnostic sandbox, not a new evaporator foundation.
```

## Candidate 6: Random Tensor Network / State Ensemble

Geometry:

```text
network graph inferred from entanglement.
```

Pros:

```text
excellent for Page/island-like information structure;
distance from network/entanglement is natural.
```

Cons:

```text
usually kinematic/state-based, not Hamiltonian evaporation;
thermodynamics and negative heat capacity must be added separately.
```

Verdict:

```text
Wrong direction for the thermodynamic engine.
```

## Ranking

For our actual goal:

```text
1. Matrix quantum mechanics / eigenvalue geometry
2. Quantum graphity / dynamical graph model
3. All-to-all spin model with dynamical couplings
4. Critical spin chain entanglement-distance diagnostic
5. SYK / Majorana all-to-all
6. Random tensor networks
```

## Recommendation

If we want a serious emergent-distance model without simply adding particle
positions, choose matrix quantum mechanics.

Minimal version:

```text
two or three small Hermitian matrices;
truncated oscillator basis;
commutator-squared interaction;
optional weak confining term for numerics;
size = eigenvalue spread or Tr X_a^2;
temperature = microcanonical density of states / kinetic energy;
evaporation = one eigenvalue separating from the clump.
```

But this is a bigger reset than modifying Track E.

The immediate low-cost diagnostic would be classical or semiclassical matrix
dynamics first:

```text
Does an initially bound matrix clump that loses energy show virial heating /
negative heat capacity in a measurable finite-size way?
```

If not, no need to quantize it.
