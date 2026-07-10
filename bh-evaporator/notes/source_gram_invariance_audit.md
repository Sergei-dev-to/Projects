# Source-Gram Invariance Audit

Date: 2026-07-09

Status: exact representation counterexample plus a corrected invariant target.
This audit is prior to any further tomography claim.

## Result in One Line

The participation ratio of

```text
W_mu,nu = <O_mu,O_nu>_shell
```

is invariant under unitary rebasing of a fixed source list, but it is not
invariant under general refactorizations of

```text
H_int = sum_mu O_mu tensor B_mu
```

that leave the physical interaction unchanged.  Therefore the raw `W` used in
the current paper is a model-side quantity unless the source/exterior metrics
or a canonical microscopic decomposition are supplied.  A representation-
invariant replacement is the Choi spectrum of the frequency-resolved jump
superoperator after the exterior coupling has been contracted in a fixed
orthonormal one-particle basis.

## 1. Exact Refactorization Counterexample

At a fixed frequency, write the interaction as

```text
H_int = sum_mu O_mu tensor B_mu.
```

Let `A` be any invertible matrix and define

```text
O'_a = sum_mu A_a,mu O_mu,
B'_a = sum_mu (A^-1)_mu,a B_mu.
```

Then exactly

```text
sum_a O'_a tensor B'_a = sum_mu O_mu tensor B_mu.          (1.1)
```

The shell Gram matrix transforms by congruence,

```text
W' = A W A^dagger.                                        (1.2)
```

For unitary `A`, the spectrum is unchanged.  For a general invertible
refactorization it is not.

Take two shell-orthogonal source operators with

```text
W = diag(1,1),
A = diag(a,a^-1).
```

The physical Hamiltonian is unchanged after the compensating transformation
of the `B` operators, while

```text
N_eff(W')
  = (a^2+a^-2)^2/(a^4+a^-4).                              (1.3)
```

This equals two at `a=1` and tends to one as `a -> infinity`.  Hence the
participation ratio of the source-only Gram matrix is not an invariant of the
physical interaction under its full representation freedom.

**Consequence.**  Overall-rescaling and unitary-basis invariance are
insufficient.  A claim that `N_eff(W)` is intrinsic must additionally specify
the physical metric that forbids or compensates nonunitary refactorizations.

## 2. Shared Exterior Modes Make the Issue Physical

If several microscopic source terms feed the same exterior operator `B`, then

```text
sum_mu O_mu tensor B = (sum_mu O_mu) tensor B.              (2.1)
```

An exterior experiment sees the combined jump operator.  It cannot determine
how that operator was split into microscopic summands without extra source-
side structure such as locality, a preferred cell decomposition, or an
independently supplied operator metric.

This is not the HIGH/LOW cancellation problem.  It occurs before any response
ratio is formed: the target source spectrum itself has not yet been made
representation invariant.

## 3. Corrected Invariant: the Jump-Superoperator Choi Spectrum

Choose a fixed orthonormal exterior one-particle wave-packet basis `{|1_k>}`
for the resolved detector band and include all physical coupling constants in
the matrix elements.  Contract the interaction with the exterior vacuum:

```text
L_k(E,omega)
  = Pi_(E-omega) <1_k|H_int|0> Pi_E.                       (3.1)
```

The frequency-resolved emission jump map is

```text
J_omega(rho) = sum_k L_k rho L_k^dagger.                   (3.2)
```

Its Choi operator is

```text
C_J = sum_k |L_k>><<L_k|.                                  (3.3)
```

Define

```text
N_Choi = (Tr C_J)^2/Tr(C_J^2).                             (3.4)
```

The nonzero spectrum of `C_J` is independent of the Kraus representation.
Adding redundant Kraus operators or changing them by an isometry adds only
zero eigenvalues or unitarily rebases the support.  Equation (3.4) is therefore
an invariant of the physical jump map once the detector band and shell metric
are fixed.

The source-only Gram matrix in the current paper agrees with this invariant
only when the listed `O_mu` are already canonical, coupling-weighted Kraus
operators for orthonormal exterior channels.  With nonorthogonal/shared
`B_mu`, their covariance must first be absorbed into the `L_k`.

## 4. The Shared-Mode Bottleneck Reappears

For one exterior wave packet, equation (3.1) gives one combined jump operator
and the one-use map (3.2) has Choi rank one, even if that jump operator is a sum
of many microscopic local terms.  The microscopic summands may still be
physically meaningful in a model with a supplied local tensor structure, but
their participation is not reconstructible from the exterior jump map alone.

This separates two targets that the current program sometimes conflates:

```text
microscopic source participation:
  number/weight of preferred local source terms;
  model-side unless a canonical source structure is supplied;

operational jump-map participation:
  invariant Choi spectrum of the resolved emission instrument;
  exterior-defined, but bottlenecked by the observable channel family.
```

## 5. Temporal Accessibility Is the Natural Operational Replacement

A single shared jump operator can access a large internal algebra through its
Heisenberg orbit under the system dynamics.  The relevant operational object
is then not an arbitrary decomposition `L=sum_mu O_mu`, but a temporal or
frequency-resolved coupling map built from

```text
L(t), [H,L], [H,[H,L]], ...
```

projected into the code/microcanonical sector.  Its span is a controllability
or Krylov-type source space.  The Q2 latency theorem already probes the
diary-visible part of precisely this orbit.

This suggests a corrected demarcation split:

```text
instantaneous microscopic boundary saturation:
  a gravitational/model-side structural input;

operational accessibility:
  growth of the diary-visible coupling orbit and its emitted record channel.
```

Static response can constrain a canonical jump map and exclude some enhanced
outliers.  It cannot recover an unobservable decomposition of a shared jump
operator into microscopic source labels.

## 6. What Tomography Can and Cannot Do

Exterior process tomography can at most reconstruct the radiation instrument
available under its preparation and measurement controls.  It does not reveal
a unique internal Kraus/source decomposition.  Full tomography of (3.2) would
also require control or readout of the system input/output, which is not
available for a black hole.

Therefore every future use of “response-kernel tomography” must state which
object is identifiable:

```text
exterior covariance/response kernel;
resolved radiation instrument;
system jump superoperator;
microscopic local source decomposition.
```

Only the first two are naturally exterior observables.  The fourth is not.

## 7. Consequence for Input 2

The active plan defines input 2 as `N_access ~ S`.  This audit shows that two
versions must be kept separate:

```text
structural input 2a:
  entropy-many preferred microscopic boundary source directions;

operational input 2b:
  entropy-wide diary-visible orbit of the physical emission instrument.
```

The source-Gram paper currently targets 2a but its proposed exterior response
certificate naturally accesses only a restricted version of 2b.  Closing the
ordinary Gram tail cannot repair that mismatch unless a canonical source
metric is independently justified.

## Immediate Repairs Owed

1. Replace “basis-independent” by “invariant after fixing the physical source
   and exterior metrics,” or use the jump-map Choi definition.
2. State whether the flagship is a model-side structural theorem or an
   exterior-identifiable theorem.
3. Do not treat microscopic labels feeding a shared exterior mode as
   separately observable merely because their shell Gram matrix is diagonal.
4. Reconnect the operational claim to the temporal coupling orbit and Q2.

## Discipline

- Unitary invariance of a chosen list is not representation invariance of the
  interaction.
- Always include coupling constants and exterior-mode covariance before
  computing an operational participation spectrum.
- Distinguish a preferred local decomposition from a minimal Kraus
  representation.
- Do not claim that exterior data reconstructs an internal Kraus
  decomposition.
