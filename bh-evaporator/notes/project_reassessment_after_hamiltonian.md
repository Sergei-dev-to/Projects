# Project Reassessment After the Naive Hamiltonian Test

## Current state

The project has narrowed to a specific possible contribution:

```text
a geometry-free quantum evaporator whose negative microcanonical heat capacity
dynamically controls emission, while radiation entropy is computed from emitted
quantum degrees of freedom.
```

This remains a real gap in the adjacent literature, but only if the model is
an actual dynamical evaporator rather than a Page-curve construction with a
black-hole label.

## What we now know

### 1. Generic Page-like turnover is not the novelty

This is already covered by:

```text
Page random-state arguments
random circuits / tensor networks
open quantum systems
Glatthard-style thermodynamic Page curves
```

The paper cannot be sold as:

```text
Page curves can happen without gravity.
```

That would be a weak and crowded claim.

### 2. The useful niche is still plausible

The adjacent literature does not obviously contain:

```text
a non-gravitational evaporator in which negative microcanonical heat capacity
drives an accelerating emission schedule and the emitted radiation entropy is
computed from the unitary dynamics.
```

That is the only claim worth pursuing.

### 3. The shell-channel kill test was encouraging but not enough

The shell-channel model showed the desired separation:

```text
Page-like turnover:
  appears in both convex and linear entropy profiles
  therefore comes from Hilbert-space competition

Acceleration:
  appears only in the convex profile
  therefore is tied to negative C_mu / convex S(E)
```

This was a useful sanity check, but it relied on random Stinespring maps that
were effectively re-randomized. It is not yet a fixed microscopic model.

### 4. The naive Hamiltonian test failed for a physically meaningful reason

The binary collision Hamiltonian:

```text
H_int = sum_m g X_m tensor |1><0| + h.c.
```

does not reproduce the shell-channel behavior.

Main reason:

```text
X_m: C^{D_m} -> C^{D_{m+1}}
rank X_m <= D_{m+1} < D_m
```

As the system evaporates, shell dimensions shrink, so a fixed one-channel
transition has large dark subspaces. The bright component emits; much of the
state remains trapped.

This is not a nuisance detail. It is a real design constraint.

## Interpretation

The central physics lesson so far is:

```text
negative heat capacity is not enough.
```

A Hamiltonian evaporator also needs:

```text
enough outgoing channel capacity
and/or
strong enough internal scrambling
```

to make the effective emission map high-rank.

This is actually a useful refinement of the paper idea. A black hole does not
emit through one rank-limited channel. It radiates into many angular,
frequency, species, and time-bin modes. A finite control model has to represent
that channel capacity somehow.

## Honest verdict

The project is not ready to become a paper.

The current evidence supports:

```text
there is a coherent mechanism worth testing
```

but not yet:

```text
we have constructed a Hamiltonian quantum evaporator.
```

If we stopped here, the result would be too weak:

```text
shell-channel model works
naive Hamiltonian model fails
therefore more engineering is needed
```

That is a good internal research note, not a publishable endpoint.

## What would make it worth continuing

A next model would need to show all of:

```text
fixed Hamiltonian collision dynamics
high-rank effective emission channel
convex/control separation
computed Page-like radiation entropy
stable behavior over seeds
```

The most plausible next designs are:

```text
1. Fixed high-rank channel model:
   pre-generate a fixed Stinespring map with enough emitted labels, then check
   whether the shell-channel result survives without re-randomization.

2. Scramble-then-emit Hamiltonian:
   alternate fixed intra-shell scrambling unitaries with fixed emission
   Hamiltonian collisions.

3. Multi-mode collision Hamiltonian:
   give each time bin enough emitted labels that
   D_{m+1} * M >= D_m
   over the working window.

4. Weak-coupling master equation first:
   derive rates from fixed operators and density of states, then purify the
   resulting quantum-jump unraveling.
```

The third option is closest to a Hamiltonian evaporator, but it becomes
numerically expensive quickly because the radiation Hilbert space grows as:

```text
(1 + M)^t
```

## Recommendation

Do not keep pushing blindly.

The next step should be a smaller conceptual/technical probe:

```text
Can a fixed high-rank emission map reproduce the convex/control separation?
```

This sits between the successful re-randomized shell-channel model and the
failed low-rank Hamiltonian model.

Decision rule:

```text
If fixed high-rank maps work:
  proceed to a high-rank/multi-mode Hamiltonian construction.

If fixed high-rank maps fail:
  archive the project for now.
```

This is the cleanest way to avoid spending time on a Hamiltonian design whose
failure mode is already visible.

## Bottom line

The idea is still interesting, but the bar has moved.

The question is no longer:

```text
Can negative heat capacity be paired with a Page-like curve?
```

The shell-channel test says yes, in an engineered channel model.

The real question is now:

```text
Can a fixed finite quantum dynamics implement a high-rank evaporative channel
without smuggling in the Page curve?
```

That is the next decisive question.

## Update after fixed high-rank channel probe

See:

```text
notes/fixed_high_rank_channel_results.md
```

The fixed high-rank channel probe passes the intermediate test.

Important result:

```text
With fixed Stinespring maps and a fixed number of emitted labels, convex
entropy profiles show rising emitted power while the linear control does not.
```

Representative fixed-channel comparison:

```text
convex curvature 3, channels = 3:
  acceleration ratio: 1.112
  Page-like S2 turnover: yes

linear control, channels = 3:
  acceleration ratio: 0.991
  Page-like S2 turnover: yes
```

Interpretation:

```text
The dark-subspace obstruction in the naive Hamiltonian is not fatal. It is a
channel-capacity problem.
```

Updated next target:

```text
build a multi-mode collision Hamiltonian whose short-time Stinespring map
approximates the successful fixed high-rank channel.
```

## Update after multi-mode Hamiltonian result

That target has now been met in a minimal reduced-density simulation.

See:

```text
notes/hamiltonian_density_channel_results.md
notes/current_status_review.md
```

The current result is:

```text
fixed multi-mode collision Hamiltonian
weak coupling
many emitted labels
convex/control acceleration separation
computed radiation Renyi-2 entropy
```

The project is therefore no longer blocked at the Hamiltonian-evidence stage.
The next issue is robustness:

```text
does the effect occupy a real parameter regime, or only a tuned example?
```
