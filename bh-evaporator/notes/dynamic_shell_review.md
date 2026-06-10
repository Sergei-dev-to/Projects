# Review of Dynamic Shell Kill Test

## What we set out to test

The minimum question was:

```text
Can the same shell model generate both a black-hole-like evaporation schedule
and a Page-like radiation entropy curve?
```

More concretely, we wanted:

```text
convex S(E) -> negative microcanonical heat capacity
convex S(E) -> rising emission probability as E decreases
unitary time-bin evolution -> computed S2_rad(t)
linear-S(E) control -> no comparable acceleration
```

## What was actually implemented

The script:

```text
sim/dynamic_shell_evaporator.py
```

implements a shell-channel model:

```text
E_0 > E_1 > ... > E_L
D_m = exp[S(E_m)]
emission weight m -> m+1 proportional to exp[S(E_{m+1}) - S(E_m)]
fresh binary radiation bin at each step
pure-state update by random isometry/Stinespring blocks
S2_rad computed from the complementary reduced core state
```

This removes the old synthetic Page-curve problem in one important sense:

```text
the radiation entropy is calculated from the evolving pure state.
```

But it does not yet give a time-independent microscopic Hamiltonian.

## Main positive result

The convex and linear controls separate the two mechanisms.

Convex run:

```text
emission probabilities: 0.401 -> 0.596
mid/early emitted-power ratio: 1.127
peak S2_rad: 2.900 at step 7
```

Linear control:

```text
emission probabilities: flat at 0.498
mid/early emitted-power ratio: 0.984
peak S2_rad: 3.312 at step 7
```

Interpretation:

```text
The Page-like turnover is generic Hilbert-space competition.
The acceleration diagnostic is tied to convex S(E), hence to negative C_mu.
```

This is exactly the distinction we needed to see.

## Main weakness

The current channel blocks are redrawn during the evolution.

That means the current implementation is best interpreted as:

```text
a fresh random chaotic collision model
```

not:

```text
one fixed microscopic unitary repeatedly applied
```

This is acceptable for a kill test, but not strong enough for a final claim
that one explicit microscopic model generated the whole evaporation history.

The next implementation should pre-generate the shell maps or Hamiltonian
couplings and then reuse them throughout each run.

## Other weaknesses

The model is engineered:

```text
S(E) is chosen by hand
only nearest-shell emissions are allowed
radiation bins are binary
the emission passband is implicit
there is no collision Hamiltonian yet
```

The acceleration signal is present but modest:

```text
1.13 in the default run
1.18 in the faster/longer run
```

That is enough for a first check, but any paper figure should use a tuned
parameter regime and show confidence bands over more seeds.

The Page peak occurs later than the simple dimension-crossing estimate:

```text
dimension crossing step: 4
S2 peak step: 7
```

This is not necessarily a bug, because the state has shell superpositions and
the effective core dimension is not just `exp[S(E_mean)]`. But it means the
Page-time diagnostic needs refinement before manuscript use.

## Process review

The process was sound for a kill test:

```text
1. identify the literature gap
2. define the minimum criterion
3. build the smallest model that ties D(E), beta(E), emission, E(t), and S_rad
4. compare against a linear-S(E) control
```

The main process mistake would be to stop here and write the result as if it
were already Level 2. It is not. It is Level 1.5:

```text
better than a synthetic Page curve
weaker than a fixed Hamiltonian collision model
```

## Recommendation

Continue, but the next task is specific:

```text
make the random shell maps fixed per seed, then rerun the convex/control
comparison.
```

If the separation survives fixed maps, proceed to:

```text
multi-frequency radiation bins
then collision Hamiltonian version
```

If the separation disappears or becomes purely parameter-tuned, stop and
archive the result as a useful diagnostic exercise.
