# Paths Forward After the Latency Classification

Date: 2026-06-18

Role: result stack

Status: current orientation note

## Fixed Point

The current robust result is the latency dichotomy:

```text
finite-velocity source-local access
=> remote private information is absent from records before routing time
=> location-uniform fast private recovery requires
   fast routing/scrambling or nonlocal/dressed access.
```

The result is information-theoretic. It is not a decoding-complexity
barrier.

The next work should not merely add examples. It should explain one of
the two escape mechanisms, or prove that broad systems fail to realize
them.

## 1. Deterministic De-Protection Plus Export

Question:

```text
Given a record coupling K and dynamics U,
when does alg{U^{-i} K U^i} rapidly destroy the private commutant,
and when does the diary actually export into the emitted/accessed
subsystem so recovery follows?
```

Target de-protection result:

```text
||E_n(O_D)||_2 <= C exp(-gamma n) ||O_D||_2
```

for a fixed diary algebra in a concrete chaotic or scrambling family,
possibly after coarse-graining into scrambling-time windows.

Target export result:

```text
rho_{R_D C} approx rho_{R_D} tensor rho_C
```

or an equivalent recovery-fidelity statement for the emitted/accessed
record subsystem. Observability alone is not recovery. In deterministic
models, de-protection and export are separate gates.

What it would mean:

```text
private information becomes accessible because dynamics rotates the
record coupling through enough of operator space and transfers the diary
into the allowed record subsystem.
```

This would turn the classification into a worked mechanism.

Promising tools:

```text
operator spreading / OTOCs
unitary designs / frame potentials
free probability / asymptotic freeness
quantum-control observability
```

Risk:

The theorem may be model-specific. That is acceptable if the model is a
recognizable chaotic family rather than an iid random baseline.

Verdict:

This is the highest-confidence proof target.

## 2. Local Tightness Benchmark

Question:

```text
Can the latency lower bound be saturated in a solvable local chaotic
model?
```

Candidate:

```text
1D dual-unitary circuit with an explicitly defined emitted/accessed
record subsystem.
```

Target result:

```text
no recovery before the light cone reaches the access region;
de-protection plus export shortly after the light cone arrives.
```

What it would mean:

The latency theorem would become tight for local chaos. Dual-unitary
dynamics is not horizon-fast on a large spatial lattice, because its
routing is still ballistic. Its value is sharper: it can provide the
matching upper bound for the local finite-velocity case.

Verdict:

This is the best controlled benchmark before attempting the
logarithmic-diameter case.

## 3. Horizon-Fast Routing Candidate

Current module:

```text
level2_expander_fast_routing.md
level2_expander_mixer_theorem.md
```

Question:

```text
Can branch 1 be realized with finite-range local gates on a graph whose
diameter is O(log S)?
```

Candidate:

```text
bounded-degree expander graph with local chaotic gates
```

Target result:

```text
t_rec = O(log S) + O(gamma_2^{-1} log(C_dec/epsilon)) + O(k/c_R)
```

for worst-case deposits, where `gamma_2` is a second-moment/export gap
for the actual expander dynamics and record partition, and `C_dec` is
the initial deviation for the HP diary/record decoupling functional.
The useful target has `C_dec` controlled by the diary and record budget,
not by the full source size. All-to-all or SYK-like models are the
diameter-one limiting cases, but the expander is the cleanest
finite-degree realization.

What it would mean:

The fast-routing branch is nonempty in a controlled deterministic
setting. The mechanism is small graph diameter plus local chaotic
mixing, rather than annealed iid randomness.

Verdict:

This is the strongest current candidate for a genuine horizon-like fast
routing theorem. The main draft now contains the reduction: a
second-moment gap in the decoupling norm implies the desired recovery
bound. The open problem is to prove that gap, or find a fast-scrambling
expander whose OTOCs grow while export still fails.

## 4. Failure Classification

Question:

```text
Which systems keep private information protected or deep despite records?
```

Likely failure classes:

```text
integrable systems
MBL systems
fragmented systems
symmetry-protected sectors
collective observables
closed or low-dimensional observable algebras
localized single-particle dynamics
restricted decoder/access classes
```

Target result:

```text
gamma = 0
```

or parametrically small `gamma`.

What it would mean:

Fast private recovery is a special dynamical property. It is not implied
by decoherence, saturation, anonymity, symmetry, or unitary record
formation.

Primary invariant:

```text
growth and irreducibility of the generated *-algebra on the diary block
```

Operator-Krylov growth is a useful diagnostic, not the invariant itself.
The relevant question is whether the generated algebra becomes
irreducible and reconstructive, not merely whether the linear Krylov span
is large.

Verdict:

Develop this alongside the positive scrambling case. The contrast is
part of the result.

## 5. Nonlocal / Dressed Access

Question:

```text
Can private information be recoverable without internal routing because
the allowed algebra was nonlocal from the start?
```

Diagnostic:

```text
freeze source-local routing;
if private recovery survives, the recovery uses dressed/nonlocal access
or trivial diary side information.
```

What it would mean:

The apparent private interior was private only relative to a factorized
source-local access model. This is the branch closest to Gauss-law
dressing, holography of information, and boundary reconstruction.

Risk:

The literature is dense. A useful result here needs a clean access
diagnostic or finite-dimensional model, rather than another verbal
comparison to gravitational dressing.

Verdict:

Highest conceptual payoff, but best treated as conceptual hygiene until
a factorization and access algebra are fixed. The frozen-routing test
classifies routed versus dressed recovery; it is not by itself the next
positive theorem.

## 6. Export Capacity / Code-Size Bounds

Question:

```text
Even after access is fast, how much record capacity is required to
recover private information?
```

Target result:

```text
t_export >= (k + recovery overhead) / c_R
```

or, for a larger code subspace,

```text
emitted record dimension must exceed the decoupling / HP threshold.
```

What it would mean:

This is the capacity-side partner of access geometry. It prevents
log-diameter access from being mistaken for recovery when the export
channel is too narrow. It also connects back to boundary saturation and
record-capacity issues: horizon-like recovery requires both fast access
and enough coherent export bandwidth.

Risk:

The basic bound may be standard dimension counting / decoupling
bookkeeping. The value is in making it an explicit necessary condition
paired with the access-geometry bound.

Verdict:

Now present as a standalone theoremlet in the main draft. It is not the
largest conceptual branch, but it closes a real loophole: logarithmic
access geometry does not erase the need to export a diary-sized coherent
record, up to continuity terms.

## 7. Measurement Cut / Quantum-Classical Transition

Question:

```text
Does quantum-to-classical emergence generically produce
public center + deep recorded block + protected/private complement?
```

Target signature:

```text
m_public << m_private
```

where `m_public` is the record scale for objective classical data and
`m_private` is the record/resource scale for private coherence recovery.

What it would mean:

Classical reality is the public layer of a constrained-access channel.
The private complement is not simply destroyed; it has a fate:
protected, deep, routed, or recoverable under enlarged access.

Risk:

This becomes only a restatement of decoherence and Quantum Darwinism
unless the private-recovery side supplies a new quantitative statement.

Verdict:

This is the broader interpretive direction, but it should be powered by
the same observability and recovery machinery as the horizon direction.

## 8. Experimental / Numerical Access Profile

Question:

```text
Can publicization and private recoverability be measured separately?
```

Candidate quantities:

```text
m_public:
    records needed to infer public pointer data

m_private:
    records/resources needed to recover private coherence

lambda:
    de-protection / observability rate

F_rec:
    recovery fidelity

frozen-dynamics response:
    whether recovery survives when source-local routing is disabled
```

What it would mean:

The program would become testable inside ordinary quantum mechanics,
without requiring deviations from QM.

Risk:

A useful protocol must avoid being ordinary tomography, quantum erasure,
or decoherence diagnostics under new names.

Verdict:

Keep this visible, but do not lead with it until the theoretical access
profile is sharper.

## Ranking

For results, not paper packaging:

```text
1. expander / logarithmic-diameter fast-routing theorem
2. deterministic de-protection plus export theorem
3. local tightness benchmark
4. failure map for non-scrambling or reducible-access systems
5. frozen-dynamics / dressed-access diagnostic
6. public/private scale separation for measurement cuts
7. experimental or numerical access-profile protocol
```

Closed supporting item:

```text
export capacity / code-size bound:
    now in the main theorem stack as the record-size floor.
```

## Recommended Next Move

Push the expander theorem-backed mixer first, while keeping the Level 1
local benchmark as the sanity check.

Current priority:

```text
bounded-degree/log-diameter access geometry
+ second-moment/export gap for the actual mixer
+ HP/decoupling export and capacity floor
=> logarithmic or polylogarithmic location-uniform recovery,
   depending on the chosen mixer implementation depth.
```

This is the first existence proof for the fast-routing branch in the
horizon-like logarithmic sense.

The local benchmark remains useful:

```text
dual-unitary local circuit:
    prove tight lower/upper latency behavior,
    including de-protection and export after light-cone arrival

nearby failure/control models:
    identify which generated-algebra or decoder restrictions keep
    private information protected or deep
```

but it is the slow-side tightness problem, not the horizon-fast
existence theorem.

The horizon-fast candidate is:

```text
bounded-degree expander with local chaotic gates:
    reuse the finite-velocity theorem with diameter O(log S),
    then prove a second-moment/export gap for the emitted-record
    partition
```

Either outcome is useful:

```text
positive local benchmark:
    the latency bound is tight for solvable local chaos

positive expander result:
    branch 1 is nonempty in a deterministic horizon-like setting

negative/control result:
    sharper conditions on what generated-algebra irreducibility and
    export require
```

This is the most direct route from the current classification to a new
result.
