# Level 2 Expander Mixer Theorem

Date: 2026-06-18

Role: result stack

Status: theorem module plus theorem-backed instantiations

## Purpose

Turn the Level 2 expander idea into an end-to-end theorem:

```text
log-diameter access geometry
+ explicit decoupling-capable mixer/export primitive
=> location-uniform fast private recovery.
```

The theorem separates three notions that should not be merged:

```text
access geometry:
    graph/light-cone route from diary to export-active region

mixing/export primitive:
    a theorem-backed channel that decouples the diary reference from the
    remaining source

physical Hamiltonian realization:
    a fixed deterministic local Hamiltonian or Floquet system that
    supplies the same primitive
```

The first two are enough for an existence theorem. The third is the
physical strengthening.

## Setup

Let `G_S = (V_S,E_S)` be a bounded-degree graph family with `|V_S| = S`
and access/emission set `X_S`.

Assume:

```text
access radius:
    R_X(S) = max_y dist_G(y, X_S) = O(log S)

finite-speed graph-local propagation:
    a diary at Y cannot affect records before dist_G(Y,X_S)/v

collection:
    every k-qudit diary reaches an export-active block by
    t_arr(Y -> X_S) <= C_arr log S + O(k)

export capacity:
    the record channel emits c_R qudits per step or otherwise emits a
    record subsystem R of the required dimension during the export window
```

Let `D` be the diary, `R_D` its reference, `E` admissible side
information independent of `D` at deposit time, `R` the emitted/accessed
record subsystem, and `C` the remaining source after export.

There are two versions:

```text
whole-source mixer:
    the export-active block is the whole covered source during the mixer
    window. Collection is then free: the diary is in the mixed block
    wherever it was deposited, and the design/TPE/random-circuit
    primitive supplies export/decoupling directly.

localized export:
    only a bounded region near X_S can emit. Then collection into that
    region is a separate routing hypothesis. A light cone reaching X_S
    gives possible influence/visibility, not automatic collection or
    recovery.
```

## Theorem: Fast Recovery From Log-Diameter Access Plus Decoupling Export

If the export window implements a channel satisfying

```text
||rho_{R_D C} - rho_{R_D} tensor rho_C||_1 <= epsilon,
```

then records plus admissible side information recover the diary with
entanglement-fidelity loss `O(epsilon)`.

If the export channel is produced by a unitary two-design,
approximate two-design, quantum tensor-product expander, or random
circuit ensemble satisfying a decoupling theorem, then the condition
holds with the corresponding theorem's error.

Consequently:

```text
t_rec <= C_arr log S + Delta_mix/export
```

where `Delta_mix/export` includes both the implementation time of the
chosen mixer and the time needed to emit a record with

```text
log d_R >= k + 2 log(1/epsilon) + log(1/delta) + O(1).
```

The matching lower-bound side is the export capacity theoremlet in the
main draft. If the record channel emits at most `c_R` coherent qubits
per step, then any high-fidelity recovery of a k-qubit diary needs

```text
Delta_export >= (k - O(error terms)) / c_R.
```

The expander shortens access distance. It does not compress the quantum
message below the diary-size floor.

In the ideal theorem-backed primitive case with constant or logarithmic
mixing/export overhead:

```text
t_rec = O(log S + k + log(1/epsilon) + log(1/delta)).
```

Before the graph light cone reaches `X_S`, the reduced-record LR theorem
gives a constant diary-to-record channel up to the LR tail, so no record
decoder can recover the diary in that interval.

## Proof

The no-recovery side is the reduced-record LR theorem. Before the
diary's graph light cone reaches the access set, the diary-to-record
channel is diamond-close to a constant channel. Post-processing by any
decoder cannot create diary entanglement.

For recovery, collection places the diary-bearing subsystem in the
export-active block by time `C_arr log S + O(k)`. The export primitive
then satisfies the decoupling condition. By information-disturbance /
decoupling recovery, a decoder exists from `R E` to the diary. The
Hayden-Preskill record-size budget gives the displayed emitted-record
dimension. Adding collection time, mixer implementation time, and record
emission time gives the recovery bound.

## Instantiation 1: Quantum Tensor-Product Expander / Approximate Design Primitive

Use a theorem-backed mixer primitive whose second moment is close to
Haar:

```text
quantum 2-tensor-product expander
or
approximate unitary 2-design.
```

Harrow and Low construct efficient constant-degree, constant-gap quantum
`k`-tensor-product expanders and obtain approximate unitary
`k`-designs for `k = O(n/log n)`. Szehr-Dupuis-Tomamichel-Renner prove
decoupling for approximate unitary two-designs.

The chain is:

```text
TPE / approximate 2-design primitive
    -> second-moment decoupling
    -> rho_{R_D C} approx rho_{R_D} tensor rho_C
    -> recovery from R E.
```

This gives the cleanest theorem-backed existence proof for the export
half.

What it proves:

```text
fast-routing branch is nonempty once a theorem-backed design/TPE mixer
is allowed in the export-active block.
```

What it does not prove:

```text
the design/TPE primitive is generated by a simple fixed local Hamiltonian
on the expander graph.
```

References:

```text
Harrow-Low:
    Efficient Quantum Tensor Product Expanders and k-designs
    arXiv:0811.2597

Szehr-Dupuis-Tomamichel-Renner:
    Decoupling with unitary approximate two-designs
    arXiv:1109.4348
```

## Instantiation 2: Random-Circuit Decoupling Primitive

Use a random-circuit ensemble with a direct decoupling theorem.

Brown and Fawzi prove that random quantum circuits with

```text
O(n log^2 n)
```

two-qubit gates satisfy an essentially optimal decoupling theorem, and
that such circuits can be implemented in depth

```text
O(log^3 n)
```

when the architecture allows the needed parallel interactions.

The chain is:

```text
random-circuit decoupling theorem
    -> export condition
    -> recovery.
```

This is theorem-backed and physically closer to circuits than a black-box
TPE primitive. Its recovery latency is:

```text
t_rec <= O(log S) + O(log^3 n_active) + HP record budget,
```

where `n_active` is the size of the active block being mixed.

This is a polylogarithmic fast-recovery existence result. It is not by
itself the sharp `O(log S)` horizon-fast theorem unless the active
export block and circuit architecture give `Delta_mix/export = O(log S)`
or better.

Reference:

```text
Brown-Fawzi:
    Decoupling with random quantum circuits
    arXiv:1307.0632
```

## Instantiation 3: Sparse-Graph Fast-Scrambling Motivation

Bentsen, Gu, and Lucas analyze fast scrambling on sparse graphs and
support the idea that sparse/log-diameter connectivity can produce
logarithmic operator spreading.

This is the right physical motivation for a deterministic expander
Hamiltonian or Floquet circuit:

```text
bounded-degree expander graph
    -> O(log S) operator growth / scrambling diagnostics.
```

But this is not yet the export theorem:

```text
large OTOCs or fast operator growth
    !=
rho_{R_D C} decoupled from C.
```

The remaining deterministic problem is to prove that the particular
expander Hamiltonian or Floquet system supplies the decoupling/export
condition for the diary recovery channel.

The main draft now formulates this as a moment-gap criterion. For a
mixing step ensemble or Floquet block with second-moment channel

```text
M_2(X) = E[ U^{tensor 2} X U^{dagger tensor 2} ],
```

the needed hypothesis is

```text
|| M_2^n - P_Haar ||_{dec(D,R)}
    <= C_dec(D,R) exp(-gamma_2 n),
```

where the seminorm controls the second-moment decoupling functional for
the fixed diary and emitted-record partition. Under that hypothesis,

```text
t_rec <= O(log S)
       + O(gamma_2^{-1} log(C_dec/epsilon))
       + O(k/c_R).
```

This is the precise bridge between operator-growth motivation and
recovery. Large OTOCs can suggest that `gamma_2` may be favorable, but
the recovery theorem needs the second-moment/export gap for the actual
record partition. A global-design norm is stronger than needed and can
carry an extensive initial deviation; the horizon-fast target is
small-subsystem decoupling, with prefactor controlled by the diary and
record budget.

References:

```text
Bentsen-Gu-Lucas:
    Fast scrambling on sparse graphs
    arXiv:1805.08215

Barbon-Magan:
    Fast Scramblers, Horizons and Expander Graphs
    arXiv:1204.6435
```

## What Is Actually Achieved

The theorem-backed result is:

```text
log-diameter access geometry
+ design/TPE or random-circuit decoupling primitive
=> location-uniform private recovery in logarithmic or polylogarithmic
   time, depending on the primitive's implementation depth.
```

This is stronger than the original classification because it shows the
fast-routing branch is nonempty under explicit information-theoretic
mixing assumptions.

The non-tautological part is the access geometry:

```text
lattice:
    finite-speed access gives S^{1/d}

expander/log-diameter graph:
    finite-speed access gives log S.
```

The random/design primitive supplies export. The expander supplies the
location-uniform access speed.

## What Remains Open

The strongest physical version remains:

```text
fixed deterministic bounded-degree expander Hamiltonian
    -> collection in O(log S)
    -> second-moment/export gap for the emitted record channel
    -> HP recovery.
```

Known sparse-graph scrambling results motivate the first two arrows but
do not automatically prove the decoupling/export condition.

## Next Action

Move the theorem into `main.tex` only after choosing which instantiation
the main draft wants:

```text
TPE/design primitive:
    clean theorem-backed existence, less microscopic

Brown-Fawzi random circuit:
    circuit-level decoupling, polylog depth

deterministic expander Hamiltonian:
    physical target, still open
```

For a result-first push, the recommended sequence is:

```text
1. state the abstract expander mixer theorem;
2. instantiate with TPE/design decoupling;
3. add Brown-Fawzi as a circuit-level polylog variant;
4. use the moment-gap export criterion to reduce deterministic expander
   recovery to a concrete second-moment gap problem.
```
