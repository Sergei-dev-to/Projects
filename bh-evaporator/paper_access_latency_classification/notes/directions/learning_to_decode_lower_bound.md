# Direction Plan: Learning-to-Decode Lower Bound

Date: 2026-07-02

Role: research direction plan (theory track)

Status: planning; not started.

## One-Line Goal

Prove a query/sample lower bound for Hayden-Preskill decoding when the
decoder has no inverse-dynamics oracle and must learn the scrambler by
observation.  This turns coupling 2 of the qi access note ("waiting
lowers complexity" via time-parametrized knowledge of `U`) from a
taxonomy entry into a theorem.

## Why This Is the Right Target

The latency dichotomy (`../paths_forward_2026_06_18.md`) is
information-theoretic and robust, but the program currently has no
complexity-side result of its own; the decoder-complexity axis of the
access profile is entirely borrowed (Harlow-Hayden, Aaronson, Python's
Lunch).  Yoshida-Kitaev shows latency and complexity decouple when
`U^dagger` is free.  The open, provable-looking question is the price
of *not* having `U^dagger`:

```text
how many queries to the forward dynamics, or samples of the record
channel, does a decoder need before it can decode as if it knew U?
```

No note in this program touches it, and it is not settled in the
literature as far as currently known (blocking check below).

## Target Statement

Setting: diary `D` (k qubits), scrambler `U` drawn from a stated
ensemble, emitted records `R_m`, side information `E` as in the HP
setup.  The decoder receives `E R_m` but no classical description of
`U`; its access to the dynamics is `q` forward queries (no inverse).

```text
target:
    F_rec^e >= 1/d_D^2 + eta
    =>
    q >= f(n, t, eta)

with f growing in the scrambling depth t for the stated ensemble.
```

The bound must be ensemble-sensitive, because two known upper bounds
bracket it:

```text
Clifford scramblers:
    U learnable from O(n^2) samples; decoding cheap after learning.

shallow circuits:
    efficiently learnable (recent learning-shallow-circuits results);
    decoding cheap at small t.
```

So the content of the theorem is the *depth dependence*: learnability
degrades as `t` grows, and the degradation curve is exactly the
latency-complexity coupling.  The shallow-learnable / deep-hard
transition is the result, not an obstacle to it.

## Routes

```text
Route A (conditional, cleanest):
    if the scrambler ensemble at depth t is pseudorandom (PRU), a
    poly-query decoder without a description of U would break the PRU;
    hardness inherits the PRU assumption.  Latency enters through the
    depth at which the ensemble becomes pseudorandom.

Route B (unconditional, restricted):
    Haar or design ensembles with forward-query access; adapt unitary
    discrimination / process-learning lower bounds to the decoding
    task.  Harder; may only give polynomial bounds.

Route C (adjacent theorem, mostly assembled):
    coupling 3 of the qi note: a decoder that must implement U(t)^dagger
    pays circuit size growing with t.  Linear growth of exact circuit
    complexity in random circuits is proven (Haferkamp et al. 2022).
    Check whether the decoding corollary is already stated somewhere;
    if not, it is a low-risk short result.
```

Recommended order: prior-art pass, then Route C (cheap, calibrates the
writing), then Route A as the main result, Route B only if A collapses
into folklore.

## Blocking Prior-Art Checks

Do these before proving anything:

```text
1. Bouland-Fefferman-Vazirani (computational pseudorandomness vs
   AdS/CFT) and successors: is a latency-parametrized decoding bound
   already stated there?  This is the closest known line.

2. Pseudorandom unitaries: Ji-Liu-Song definition; Ma-Huang style
   constructions (2024); any black-hole-decoding application papers.

3. Kim-Tang-Preskill ghost logical operators (decoder-independent
   hardness inside the horizon context).

4. Process-learning bounds: Huang et al. learning quantum processes;
   unitary tomography lower bounds; learning-shallow-circuits
   upper bounds (these calibrate the small-t end).

5. Yoshida-Kitaev follow-ups on decoding with imperfect knowledge of U
   (there is a known noise-robustness line; check whether "unknown U"
   was treated).
```

If check 1 or 5 already contains the theorem, the direction dies as a
standalone paper and becomes two paragraphs plus citations in the
main.tex complexity section.  That outcome still pays: the access
profile gets its fifth axis properly anchored.

## Milestones

```text
M1  access-model definitions: decoder resources (queries, samples,
    description bits), what "forward-only" means, ensemble families.
    Deliverable: 2-3 page formal setup note.

M2  prior-art pass (blocking checks above).
    Deliverable: collision matrix in the style of
    ds_literature_collision_matrix.

M3  Route C write-up: inversion-cost coupling from complexity growth.
    Deliverable: short proposition + proof sketch.

M4  Route A: PRU reduction with the depth-parametrized statement.
    Deliverable: main theorem draft or documented failure mode.

M5  decision point: standalone paper vs main.tex section.
```

## Kill Criteria

```text
- BFV line or YK follow-ups already state the depth-parametrized bound
  => fold into main.tex, cite, stop.
- Route A yields only "PRU implies hard decoding" with no latency
  dependence => that is folklore; stop unless Route B shows life.
- Formal setup (M1) reveals the coupling is definitionally circular
  (latency defined through the same resource being bounded) => rethink
  before proving.
```

## Deliverable and Venue

If the main theorem lands: standalone paper, Quantum / PRX Quantum /
QIP-track.  If only Route C lands: proposition inside the horizon
paper's new decoder-complexity section.  Either outcome upgrades the
access profile's complexity axis from borrowed to owned.

## Dependencies

- Fix the sample-complexity exponent in `../qi_access_inequality_note.md`
  first (the adaptive-strategy bound is 1/epsilon, not 1/epsilon^2);
  M1's access-model definitions should be consistent with the corrected
  statement.
- No numerics required anywhere in this plan.
