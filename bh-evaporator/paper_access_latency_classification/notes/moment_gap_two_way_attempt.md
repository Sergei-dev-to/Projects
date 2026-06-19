# Moment-Gap Two-Way Attempt

Date: 2026-06-18

Role: result stack

Status: proof route plus counterexample route

## Question

After the moment-gap export criterion, the deterministic expander problem
has two natural attacks:

```text
positive:
    prove a useful second-moment/export gap for a concrete expander
    dynamics

negative:
    construct fast operator growth or fast publicization without
    second-moment export
```

Both routes are informative. The positive route would realize the
horizon-fast branch with sparse dynamics. The negative route would show
that the visibility/recovery distinction is not cosmetic.

## Positive Route: Expander Moment Hamiltonian

Model:

```text
G_S:
    bounded-degree expander on S qudits

layers:
    edge-color G_S into O(1) matchings;
    in one circuit layer, apply independent Haar two-qudit gates on one
    or all matching classes

record:
    after mixing, emit a coherent record subsystem R of size satisfying
    the HP/export capacity budget
```

The target is:

```text
|| M_2^n - P_Haar ||_{dec(D,R)}
    <= C_dec(D,R) exp(-gamma_2 n)
```

with

```text
gamma_2 = Omega(1)
```

per parallel layer, or at least

```text
gamma_2 >= 1/polylog(S).
```

Then the main theorem gives

```text
t_rec <= O(log S)
       + O(gamma_2^{-1} log(C_dec/epsilon))
       + O(k/c_R).
```

The norm is the one controlling the HP decoupling functional for the
fixed diary and emitted-record partition. It is not a global-design
norm. If `C_dec = exp(O(k + log(1/delta)))`, constant `gamma_2` gives
the desired horizon-fast scaling. If one routes through a global
2-design norm with `C_dec = exp(O(S))`, the bound becomes linear in `S`
and the expander advantage is lost.

## Proof Skeleton

For `t=2`, the local Haar twirl on an edge is a projector `P_e` onto the
two-copy invariant subspace of that edge. Define the frustration-free
moment Hamiltonian

```text
H_2 = sum_e (I - P_e).
```

The global ground space is the Haar second-moment invariant space, but
global design convergence is stronger than the recovery task. The
desired small-subsystem export gap should follow from a spectral gap for
`H_2`, a controlled initial-deviation bound for the diary/record
functional, and a detectability-lemma/product-of-projectors step for the
parallel layer schedule:

```text
gap(H_2) >= gamma_H
    => layer moment contraction gamma_2 = f(gamma_H, degree)
    => small-subsystem second-moment export criterion
    => recovery.
```

The plausible expander-specific lemma is:

```text
Lemma target:
    On a bounded-degree expander, the normalized two-copy moment
    Hamiltonian for Haar two-site gates has gap Omega(1).
```

Why it is plausible:

```text
t=2 has only the identity/swap permutation labels in the Schur-Weyl
sector;

edge projectors energetically penalize disagreement of those labels
across an edge;

an expander makes every nontrivial label domain have many boundary
edges;

non-permutation components have local twirl gap.
```

So `H_2` should compare to a ferromagnetic two-state synchronization
Hamiltonian plus local leakage penalties. Expansion should give a
constant normalized gap.

## What Existing Literature Gives

Known random-circuit design results support the route but do not close
the sharp expander result automatically.

```text
Brown-Fawzi:
    decoupling from random circuits with O(n log^2 n) gates and
    polylogarithmic depth when broad parallel interactions are available.

Harrow-Mehraban:
    short random-circuit designs for nearest-neighbor and long-range
    architectures.

Mittal-Hunter-Jones:
    approximate designs on arbitrary connected architectures, with
    bounds derived from local-Hamiltonian spectral gaps.
```

The arbitrary-architecture results are especially relevant because they
frame the problem in exactly the right language: spectral gaps of moment
Hamiltonians. The available general bounds, however, are not the desired
logarithmic-depth expander export theorem. The missing result is the
expander-specific `t=2` moment gap in the small-subsystem decoupling
norm, or a direct decoupling bound for the emitted-record partition. A
route through full global design convergence is too strong for the
desired latency.

## Immediate Proof Task

Prove or disprove:

```text
For Haar two-qudit random gates applied in parallel matching layers on a
bounded-degree expander, the two-copy moment dynamics contracts the HP
diary/record decoupling functional with gamma_2 = Omega(1), or at least
gamma_2 >= 1/polylog(S), with prefactor controlled by k and the record
budget rather than S.
```

Concrete route:

```text
1. Write the edge twirl projector P_e explicitly for t=2.
2. Decompose the two-copy operator space into permutation-label and
   leakage sectors.
3. Show leakage sectors are locally penalized.
4. Compare the permutation-label sector to the graph Laplacian or
   ferromagnetic Potts/Ising synchronization Hamiltonian.
5. Use the expander spectral gap to bound the normalized H_2 gap.
6. Convert H_2 gap to parallel-layer contraction by the detectability
   lemma.
7. Bound the initial deviation for the HP decoupling functional by
   exp(O(k + record overhead)), not exp(O(S)).
```

If this works, the deterministic/random-local expander circuit gives the
fast-routed branch without a black-box mixer.

## Negative Route: Fast OTOC Without Export

A clean counterexample family should have:

```text
fast operator support growth;
fast public record formation;
no coherent private recovery.
```

Candidate:

```text
expander controlled-phase or CNOT circuit
+ record coupling to a commuting Z algebra.
```

On an expander, a depth `O(log S)` Clifford or diagonal circuit can make
the Heisenberg evolution of a local `X` operator acquire support on
`O(S)` sites:

```text
X_D -> X_D product_{j in ball(D,t)} Z_j.
```

Thus support growth and many OTOC diagnostics become fast. But if the
accessible records only couple to the commuting `Z` algebra, the channel
exports public/classical information, not the diary qubit. For a diary
maximally entangled with a reference, the record channel is dephasing or
entanglement-breaking on the diary:

```text
quantum recovery fidelity stays bounded away from 1;
rho_{R_D C} does not decouple in the HP sense;
the generated accessible algebra remains abelian or block-diagonal.
```

This gives a sharp warning:

```text
fast operator growth / fast OTOCs / fast publicization
    do not imply coherent export.
```

It also separates de-protection from recovery. With records restricted
to the commuting `Z` algebra, the record-generating algebra can remove
the protected component of an off-diagonal diary operator such as `X_D`:

```text
E_n(X_D) = 0
```

in the observability/commutant diagnostic. The diary is no longer
protected in that diagnostic, but it has not been coherently exported;
it has been dephased relative to the allowed records. Thus the
de-protection rate `lambda` is a necessary precursor for recovery, not a
sufficient recovery invariant. The recovery-relevant invariant is the
second-moment/export gap `gamma_2`.

In the moment-gap language, the failure is that the second-moment
channel has an invariant subspace far larger than the Haar/design
invariant space:

```text
gamma_2 = 0
```

for the decoupling-relevant sector, even though selected operators have
large Heisenberg support quickly.

## Stronger Negative Target

The diagonal/abelian model is a sanity counterexample. A stronger
counterexample would be:

```text
nonabelian fast operator growth
+ no HP export for the emitted-record partition.
```

Possible mechanisms:

```text
symmetry conservation:
    fast scrambling inside charge sectors but no export of charge-sector
    coherences;

fragmentation:
    large operator support inside disconnected dynamical sectors;

Clifford stabilizer restriction:
    fast Pauli growth but recovery only for stabilizer-compatible code
    data unless the ensemble/randomization is rich enough;

collective bottleneck:
    many source degrees feed a low-rank record channel, so instantaneous
    observables saturate while coherent diary export fails.
```

The useful counterexample should not merely be integrable or trivial. It
should pass a standard scrambling diagnostic and fail the
second-moment/export criterion.

## Current Verdict

The positive route has a plausible sharp subproblem:

```text
prove the t=2 expander moment-Hamiltonian gap.
```

The negative route already has a simple counterexample:

```text
fast support growth with abelian/public export can de-protect a private
operator in the commutant/observability sense while still failing to
recover private quantum information.
```

That counterexample is not a defeat of the program. It validates the
moment-gap/export criterion as the right invariant: OTOC growth is too
weak, and de-protection is still too weak. Second-moment export is the
missing quantum recovery condition.
