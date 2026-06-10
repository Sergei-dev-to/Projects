# Result 2B Hamiltonian Realization Probe

## Question

After closing Result 2A with theorem-backed shell mixers, can we push toward a
more microscopic `H_mix` that looks like ordinary Hamiltonian dynamics rather
than an abstract approximate design or tensor-product expander?

The desired implication is:

```text
specific shell Hamiltonian K_E
  -> decoupling of the evaporation code subspace.
```

The direct decoupling condition is:

```text
early:
  I(Q : R_so_far) small;

late:
  I(Q : B_remaining) small.
```

The standard sufficient condition is approximate 2-design behavior on the
active shell, and the Hamiltonian diagnostic route is OTOC/channel scrambling.

## What the Literature Lets Us Use

### Expander and sparse-graph scrambling

Barbon-Magan and Bentsen-Gu-Lucas support the idea that sparse nonlocal
connectivity, especially expander-like connectivity, can produce logarithmic
scrambling and rapid operator growth.

This supports:

```text
expander graph shell Hamiltonian
  -> plausible fast operator growth / OTOC spreading.
```

It does not give the exact evaporation-channel decoupling theorem.

### Channel scrambling

Hosur-Qi-Roberts-Yoshida relate OTOC decay to mutual information of the unitary
channel state.  Yoshida-Kitaev connect OTOC decay to Hayden-Preskill recovery.

This supports:

```text
OTOC/channel scrambling
  -> mutual-information decoupling
  -> Hayden-Preskill-style recovery.
```

So the bridge from OTOC decay to information flow is known.

### Hamiltonian-to-design caution

Recent Hamiltonian-design literature gives a warning.  Cui-Schuster-Mao-Huang-
Brandao show a no-go result: ensembles of constant-local Hamiltonians evolved
for arbitrary times can be efficiently distinguished from Haar-random unitaries
and fail to form a 2-design or pseudorandom unitary in that strong global
sense.  They also show that increasing the locality to polylogarithmic can
overcome the obstruction.

This matters because it says a simple constant-local Hamiltonian proof of full
unitary-design behavior is the wrong target.

### Nearly time-independent design Hamiltonians

Nakata et al. construct unitary designs using nearly time-independent or
periodically changing Hamiltonian dynamics.  This is closer to a Hamiltonian
realization of design behavior, but it uses designed interactions and temporal
structure rather than a simple autonomous spin Hamiltonian.

This supports a possible intermediate route:

```text
designed Hamiltonian dynamics
  -> approximate design
  -> decoupling.
```

It is less microscopic than a fixed expander spin Hamiltonian and more
Hamiltonian-like than an abstract design block.

## Candidate Routes for 2B

### Route B1: expander spin Hamiltonian

Use

```text
K_E =
  P_E [
    sum_{(ij) in G_E}
      (J_x X_i X_j + J_y Y_i Y_j + J_z Z_i Z_j)
    + sum_i (h_x X_i + h_z Z_i)
  ] P_E.
```

with a deterministic bounded-degree expander graph `G_E`.

What is known:

```text
fast operator-growth route is strongly motivated.
```

What is missing:

```text
the OTOC/channel-decoupling bound for the evaporation partitions.
```

Assessment:

```text
best microscopic candidate, but not closable from existing theorems found so
far.
```

### Route B2: polylog-local Hamiltonian design

Use a shell Hamiltonian whose locality grows mildly, following the direction of
the Hamiltonian-design literature.

What is known:

```text
polylog-local Hamiltonians can evade the constant-local no-go and produce
design-like behavior in known constructions.
```

What it costs:

```text
less like a simple spin Hamiltonian;
more engineered than the expander spin model.
```

Assessment:

```text
best theorem-backed Hamiltonian route beyond 2A.
```

### Route B3: nearly time-independent design Hamiltonian

Use the design-Hamiltonian construction of Nakata et al. or related work.

What is known:

```text
Hamiltonian dynamics can realize unitary designs after a threshold time, using
designed spin-glass-like interactions and periodic changes.
```

What it costs:

```text
time dependence or designed temporal structure;
less autonomous than the desired final model.
```

Assessment:

```text
useful if the target is Hamiltonian-realizable design behavior rather than a
simple autonomous microscopic Hamiltonian.
```

## Best Current Strategy

Do not try to make the expander spin Hamiltonian carry Result 2A.

Use Result 2A:

```text
approximate-design / tensor-product-expander shell mixing
  -> decoupling by known theorems.
```

Then treat Result 2B as one of two possible refinements:

```text
B1:
  prove or cite OTOC/channel-decoupling for a deterministic expander spin
  Hamiltonian;

B2:
  replace the abstract shell mixer by a known Hamiltonian design construction,
  accepting polylog-locality or mild temporal structure.
```

## What Would Close 2B

The clean closure would be a theorem of the form:

```text
For a nonintegrable Hamiltonian on a deterministic expander graph, evolution
for O(log N) scrambling time makes the channel state have small mutual
information between any small input code and most output partitions.
```

That theorem was not found in the checked literature.

The more achievable closure is:

```text
Use a known Hamiltonian design construction, then apply approximate-design
decoupling.
```

This is closer to Result 2A, but now the mixer is explicitly Hamiltonian
generated.

## References To Track

```text
Barbon, Magan,
"Fast Scramblers, Horizons and Expander Graphs", arXiv:1204.6435.

Bentsen, Gu, Lucas,
"Fast scrambling on sparse graphs", arXiv:1805.08215.

Hosur, Qi, Roberts, Yoshida,
"Chaos in quantum channels", arXiv:1511.04021.

Yoshida, Kitaev,
"Efficient decoding for the Hayden-Preskill protocol", arXiv:1710.03363.

Nakata et al.,
"Efficient unitary designs with nearly time-independent Hamiltonian dynamics",
arXiv:1609.07021.

Cui, Schuster, Mao, Huang, Brandao,
"Random unitaries from Hamiltonian dynamics", arXiv:2510.08434.
```
