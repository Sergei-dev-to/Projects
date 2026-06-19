# Self-Review and External Review Packet

Date: 2026-06-17

Role: review packet

Status: current self-review after the observability-gap target adjustment.

External review update: the theorem stack survived a validity pass. The
reviewer's main correction is strategic, not fatal: the source-local
latency dichotomy is already the strongest result, while the positive
deterministic observability/export theorem remains open.

## Current Target

The project is now aimed at a constrained-access classification of private quantum information:

```text
public center
recorded-but-deep block
protected commutant
```

with recovery mechanisms:

```text
slow routing
fast routing / scrambling
dressed or nonlocal access
```

The main theorem stack is not trying to derive gravity or geometry. It is trying to classify when private information is hidden, de-protected, recoverable, delayed, or visible through nonlocal/dressed access.

## Self-Review Verdict

The current theorem stack is coherent and has a real spine:

```text
commutant structure
-> exact observability
-> approximate observability gap
-> fixed-diary de-protection
-> random-coding recovery baseline
-> source-local latency separation
```

The strongest current result is the mechanism classification:

```text
source-local finite-velocity access
=> no location-uniform fast recovery of arbitrary private deposits

location-uniform fast private recovery
=> fast routing/scrambling or nonlocal/dressed access
```

This obstruction is information-theoretic. It is not a decoding
complexity statement; before the LR light cone reaches the record
channel, the reduced record channel is close to constant in diamond norm.

The most important recent adjustment is that the deterministic problem now splits into two parts:

```text
observability:
    does alg{U^{-i} K U^i} see the diary algebra?

export/decoupling:
    does the emitted record system actually recover the diary?
```

This split is correct and prevents de-protection from being mistaken for recovery.

## What Looks Solid

### Commutant Theorem

The protected-complement theorem is standard finite-dimensional algebra/noiseless-subsystem theory. The exact protected private complement of passive records is the noncommuting part of the commutant of the record-generating algebra.

Risk level: low.

Reviewer ask: check that the record-generating algebra really includes all Heisenberg pullbacks of allowed passive record observables in the intended instrument model.

External-review action taken in `main.tex`: the record-generating algebra
is now explicitly relative to the specified access family. Enlarging the
instrument family enlarges `A_rec` and can shrink the protected
commutant.

### Source-Local Latency Bound

The reduced-record Lieb-Robinson argument gives a clean information-theoretic obstruction:

```text
remote diary cannot affect the record channel before the light cone reaches the access region.
```

The constant-channel lemma then excludes order-one recovery.

Risk level: moderate-low.

Reviewer ask: check the channel/reduced-state formulation carefully, especially side information exclusions and the relation between LR reduced-state closeness and diamond-norm closeness of the diary-to-record channel.

External-review action taken in `main.tex`: the LR proof note now
includes the controlled-`U_Y`/spectator-reference argument, making the
diamond-norm statement visibly ancilla-stable.

### Saturation and Anonymity Counterexamples

The saturated slow-router and collective-charge pointer examples correctly block tempting shortcuts:

```text
source-side saturation != fast recovery
anonymity + symmetry + unitarity != private mixing
```

Risk level: low.

Reviewer ask: check whether the examples are too artificial for the claims they are used to refute. They only need to be counterexamples to implication claims.

### Random Pauli Growth

The Pauli counting is correct:

```text
p_q = (D^2/2 - 1)/(D^2 - 1) < 1/2.
```

For fixed private operators, protected weight decays exponentially in independent record units. Whole-block commutant collapse is stronger and takes `O(log D)` independent generators.

Risk level: low.

Reviewer ask: verify the distinction between fixed-diary de-protection and whole-block collapse is consistently maintained.

### Random-Coding Recovery Baseline

The decoupling theorem is standard Hayden-Preskill/random-coding:

```text
E ||rho_{R_D C} - rho_{R_D} tensor rho_C||_1 <= O(d_D/d_R).
```

This closes the random baseline:

```text
independent randomization
=> fixed-diary de-protection
=> fixed-diary recovery
```

Risk level: moderate-low.

Reviewer ask: check constants/exponents in the high-probability statement, especially the `2 log(1/epsilon)` overhead and the use of Markov.

## What Is Conditional or Open

### Observability Gap for Deterministic Dynamics

The current approximate observability framework defines:

```text
Pi_i = projection onto one-step commutant A_i'
T_{1:n} = Pi_n ... Pi_1
```

and uses the gap condition:

```text
||T_{1:n}(O_D)||_2 <= C exp(-gamma n)||O_D||_2.
```

This implies:

```text
||E_n(O_D)||_2 <= C exp(-gamma n)||O_D||_2.
```

The hard open problem is proving a positive gap for correlated Heisenberg iterates:

```text
P_i = U^{-i} K U^i.
```

Risk level: high, because this is where physics enters.

Reviewer ask: judge whether the projection-product definition is the right approximate observability object, and whether the sufficient condition is too strong, too weak, or missing a better known control/observability analogue.

### Conditional Contraction Benchmark

The benchmark proposition says that if, after conditioning on the past,

```text
E[||Pi_i O||_2^2 | past] <= (1 - eta)||O||_2^2
```

for every current operator descended from the diary algebra, then:

```text
E||T_{1:n}O||_2^2 <= exp(-eta n)||O||_2^2.
```

Risk level: low as a lemma, high as a physical assumption.

Reviewer ask: determine whether ETH, local random circuits, or operator-spreading results imply this condition, perhaps only over scrambling-time windows rather than single steps.

### Export/Decoupling for Physical Records

Observability is not recovery. The physical model still needs an export condition:

```text
remaining block C decouples from diary reference
```

so records plus side information recover the diary.

Risk level: high.

Reviewer ask: identify the weakest channel-theoretic condition that links observability of record pullbacks to actual decoupling into emitted records.

## Possible Weak Points

### Projection Product Is Sufficient, Not Necessary

The product

```text
T_{1:n} = Pi_n ... Pi_1
```

is not generally the same as the orthogonal projection onto the accumulated commutant. The proof uses it as a sufficient criterion:

```text
||E_n(O)|| <= ||T_{1:n}(O)||.
```

This is valid, but the converse is not claimed. A failed product-gap test may not prove absence of de-protection.

Reviewer ask: check if a better canonical approximate intersection measure exists.

External-review action taken in `main.tex`: the product map is now
described as a sufficient certificate. The physical target is conditional
or windowed contraction for the actual Heisenberg record sequence. The
text now flags the deterministic product as an alternating-projections /
Friedrichs-angle problem.

### Generic Exact Observability May Be Too Weak

The generic full-algebra proposition is an exact nongenericity statement. It does not give rate, conditioning, or physical realism.

Reviewer ask: confirm it is framed as a structural sanity check, not a scrambling theorem.

### One-Step Versus Windowed Gap

Physical scrambling likely gives contraction over windows, not every step:

```text
T_{i:i+\tau_scr}
```

rather than each `Pi_i`.

Reviewer ask: recommend whether the draft should introduce a windowed observability gap now.

### Approximate Public Stability Is Imported

The public-center side is exact in the theorem but approximate public objectivity is imported from Quantum Darwinism/SBS/no-broadcasting literature.

Reviewer ask: determine whether the draft needs an explicit approximate-public lemma or whether citations suffice.

## Outside Review Ask

Ask an outside reviewer to focus on validity and potential, not polish.

Suggested prompt:

```text
Please review the attached theorem draft and notes as a proposed
constrained-access classification of private quantum information.

Main questions:

1. Is the commutant/noiseless-subsystem characterization of protected
   private information being used correctly?

2. Is the source-local finite-velocity latency theorem stated with the
   right channel norms and side-information exclusions?

3. Is the observability-gap definition using products of one-step
   commutant projections a sensible sufficient notion of approximate
   observability?

4. Does the benchmark proposition correctly separate iid Pauli growth,
   common-commutant obstructions, and conditional correlated contraction?

5. What known results in quantum control, operator spreading, ETH,
   random circuits, or decoupling most directly address the missing
   deterministic gap?

6. Is the separation between de-protection and recovery maintained
   clearly enough?

7. Does the horizon-interface mechanism classification overclaim, or is
   it appropriately conditional?
```

## Files To Send

Minimum packet:

```text
paper_access_latency_classification/main.tex
paper_access_latency_classification/refs.bib
paper_access_latency_classification/notes/private_information_fate_classification.md
paper_access_latency_classification/notes/access_latency_stress_test.md
paper_access_latency_classification/notes/README.md
```

Optional context:

```text
paper_access_latency_classification/notes/long_term_goal_constrained_access.md
paper_access_latency_classification/notes/access_profile_verification_target.md
paper_access_latency_classification/notes/wigner_friend_horizon_access_pass.md
```

Do not send the whole notes folder for a first review. It will obscure the theorem stack.

## Current Next Technical Step

The next proof-facing task should use one of the known toolchains for
correlated dynamics rather than another iid toy model:

```text
free probability / asymptotic freeness
unitary designs / frame potentials
operator spreading / OTOCs
quantum-control observability
```

Concrete options:

1. Windowed observability-gap theorem:

   ```text
   contraction over scrambling-time blocks
   => exponential de-protection per block.
   ```

2. ETH/random-circuit attempt:

   ```text
   show Heisenberg iterates of K satisfy a conditional contraction
   after sufficient time separation.
   ```

3. Counterexample map:

   ```text
   integrable / MBL / symmetry / fragmentation / collective K
   => gamma = 0 or parametrically small.
   ```

The windowed theorem is probably the most natural next internal step before asking a reviewer to evaluate the ETH plausibility.
