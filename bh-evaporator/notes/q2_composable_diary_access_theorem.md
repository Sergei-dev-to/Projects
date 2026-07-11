# Q2 Composable Long-Time Diary-Access Theorem

Date: 2026-07-10

Status: exact theorem for arbitrary finite sequential processes with shared
memory and changing memory dimension; energy-constrained extension stated on
hybrid-reachable sectors. This removes the exponential/bounded-budget weakness
of `q2_operator_overlap_bridge_theorem.md`.

## Result in One Line

Let an actual evaporation comb be compared step by step with any comb whose
entire emitted record is diary blind. If the `j`th actual and blind steps differ
by at most `eta_j` on every state reachable by the hybrid comparisons, then

```text
distance(actual record, blind record) <= sum_j eta_j.       (1.1)
```

There is no exponential in the total blind evolution and no assumption that
the record ancillas are memoryless. Consequently reliable recovery by time
`K` requires order-one cumulative diary-visible process defect.

## 1. Sequential Process

Let `D` be a diary initially encoded with a hidden memory `M_0`; allow an
arbitrary reference `A`. At step `j`, an actual CPTP map

```text
Phi_j : M_(j-1) -> M_j tensor R_j                         (1.2)
```

emits a new accessible record piece `R_j`. The dimensions and Hamiltonians of
`M_j` may change with `j`. Previously emitted records are spectators, while
`M_j` can retain arbitrary non-Markovian memory.

Choose comparison maps

```text
Psi_j : M_(j-1) -> M_j tensor R_j                         (1.3)
```

with the same interfaces. Their composed record channel `C_K` must be diary
blind on the code:

```text
C_K(rho_D) = omega_R(K)  for every diary state rho_D.     (1.4)
```

This channel-level condition is the invariant definition. A sufficient
algebraic realization is that the complete comparison Heisenberg algebra of
all emitted-record observables reduces to scalars on `D`. Checking only the
individual generators, without closure under the internal dynamics and
multi-time products, is not sufficient.

## 2. Reachable-Hybrid Step Defect

For each binary string `s_1...s_(j-1)`, compose actual or blind maps according
to the string and let `S_(j-1)` contain every resulting joint state of

```text
A tensor M_(j-1) tensor R_(<j)                            (2.1)
```

from an allowed code/reference input. Define

```text
eta_j = sup_(sigma in S_(j-1))
        || [(Phi_j-Psi_j) tensor id_(A R_<j)](sigma) ||_1. (2.2)
```

This is a state-restricted completely bounded defect. It is no larger than the
ordinary diamond distance. For bosonic systems it is no larger than an
energy-constrained diamond distance whenever all hybrid-reachable states obey
the chosen energy bound `E_(j-1)`.

The reachable-set definition is important: it permits a persistent pump,
partner accumulation, changing shell dimension, and correlations between the
memory and all earlier records.

## 3. Theorem: Linear Composable Bound

Let `N_K` and `C_K` be the actual and blind emitted-record channels through
step `K`, after tracing the final hidden memory. Then

```text
|| N_K - C_K ||_(code,diamond) <= sum_(j=1)^K eta_j.       (3.1)
```

Here the left side is the diamond norm restricted to the allowed code inputs;
equivalently it is the supremum trace distance including a reference.

### Proof

Insert the comparison maps one step at a time. Adjacent hybrid processes differ
only at step `j`. By definition their states immediately after that step differ
by at most `eta_j`. Every later actual or blind map is CPTP, so trace-norm
contractivity prevents amplification. Partial trace to the emitted record is
also contractive. The triangle inequality over the `K` hybrids gives (3.1).

No norm of the blind Hamiltonian enters. Large diary-blind evolution is free;
only distance from the blind comparison process accumulates.

## 4. Hamiltonian and Isometry Corollaries

For bounded self-adjoint collision generators

```text
U_j = exp(-i g_j H_j),
U_j^0 = exp(-i g_j H_j^0),                                (4.1)
```

Duhamel's identity has unitary left and right factors and therefore gives

```text
||U_j-U_j^0|| <= |g_j| ||H_j-H_j^0||.                    (4.2)
```

There is no exponential factor. The corresponding channel defect obeys

```text
eta_j <= 2 |g_j| eps_j,
eps_j = ||H_j-H_j^0||,                                   (4.3)
```

or the same bound with operator norms restricted to a common invariant energy
sector. Hence

```text
||N_K-C_K||_(code,diamond)
  <= 2 sum_j |g_j| eps_j.                                 (4.4)
```

For collision isometries `V_j,V_j^0`, directly

```text
eta_j <= 2 ||V_j-V_j^0||                                 (4.5)
```

on the reachable input sector.

## 5. Recovery Converse

Take two orthogonal diary states `rho_D,sigma_D`, with full trace distance two.
If a decoder `Dec_K` acting on the emitted record recovers each with trace-norm
error at most `alpha`, contractivity and (3.1) imply

```text
2-2 alpha
 <= ||N_K(rho_D)-N_K(sigma_D)||_1
 <= 2 sum_j eta_j.                                       (5.1)
```

Thus

```text
sum_j eta_j >= 1-alpha.                                  (5.2)
```

Reliable classical distinguishability, and therefore reliable quantum diary
recovery, requires order-one cumulative process defect from every diary-blind
comparison comb. This is a necessary condition, not a sufficiency theorem.

## 6. Finite Pump and Energy Constraint

The finite pump begins in levels `0,...,N` and can emit at most `N` pair-energy
units. Every hybrid built from an actual finite-pump collision and a blind
finite-pump comparison therefore stays in the finite total-energy sector

```text
E_pump + E_emitted <= N.                                 (6.1)
```

Equations (3.1)--(4.5) apply exactly for arbitrarily many collisions; no
infinite-dimensional norm is required. For an unbounded pump family, impose a
uniform mean-energy constraint and use `eta_j` from (2.2), or an
energy-constrained diamond norm that dominates it. The theorem only requires
that all hybrid processes remain inside the declared admissible sets.

For the exact diary-blind pump,

```text
Phi_j = Psi_j = V_q tensor I_D,
eta_j = 0                                                 (6.2)
```

for every `j`, although the blind pump undergoes `O(S)` interactions and its
global energy-history participation grows. This is precisely the long-time
regime the old exponential estimate could not express usefully.

## 7. What Is and Is Not Closed

Closed:

```text
small cumulative channel/process distance from a diary-blind evaporation comb
  => no accurate diary recovery from the emitted record;

large blind dynamics, shared pump memory, partner accumulation, and changing
shell dimensions do not weaken the bound.
```

Still open:

```text
how a microscopic black-hole model supplies order-one cumulative diary access;
whether that access mixes all diary directions rather than a conserved tag;
whether the resulting channel satisfies a decoupling/recovery condition;
how the exterior radiation algebra is selected in gravity.
```

## 8. Drafting Rule

The robust statement is now:

```text
Fast recovery requires order-one cumulative distance of the physical
evaporation process from every diary-blind comparison comb on the reachable
energy sectors.
```

Do not replace "process distance" by one-time source rank, a raw generator
list, or total emitted-record rank.
