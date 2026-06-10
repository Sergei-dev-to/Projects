# Expander Scrambler Bridge Attempt

## Goal

Try to close the hard step for a concrete shell mixer:

```text
expander H_mix
  -> OTOC/operator growth over scrambling blocks
  -> reference/core or reference/radiation decoupling
  -> Page/Hayden-Preskill information flow for the evaporation channel.
```

The point is to see which part is already in the literature and which part
remains a genuine dynamical assumption.

## Candidate Mixer

For an area sector with `N_A(E) ~ A(E)` active microscopic degrees of freedom,
take a bounded-degree expander graph `G_E` and a nonintegrable spin Hamiltonian

```text
K_E =
  P_E [
    sum_{(ij) in G_E}
      (J_x X_i X_j + J_y Y_i Y_j + J_z Z_i Z_j)
    + sum_i (h_x X_i + h_z Z_i)
  ] P_E.
```

`P_E` projects to the microcanonical shell.  The couplings are fixed after the
Hamiltonian is specified.  They are not redrawn during evaporation.

The emission Hamiltonian samples `A(E)` independent weak channels.  Therefore a
scrambling block should be judged by how it spreads code information over the
area-sized active set sampled by the outgoing channels.

## What We Actually Need

Let one coarse block consist of several emissions plus enough in-shell evolution
to last one scrambling time.  Let

```text
V_block : H_B(E) -> H_B(E') tensor H_R(block)
```

be the Stinespring map for that block, and let the full evaporation map be the
composition of such blocks.

For a code subspace purified by `Q`, the needed conditions are:

```text
before Page time:
  I(Q : R_so_far) small;

after Page time:
  I(Q : B_remaining) small.
```

Second-Renyi mutual information is the natural diagnostic because Page-purity,
decoupling, and OTOC-channel results all use second moments.

In trace-norm language, the targets are:

```text
||rho_QR - rho_Q tensor rho_R||_1 << 1      early,
||rho_QB - rho_Q tensor rho_B||_1 << 1      late.
```

Approximate 2-design behavior is a sufficient condition for these bounds.

## Known Bridge 1: Channel Scrambling to Decoupling

This part is standard.

Hosur-Qi-Roberts-Yoshida treat a unitary channel as a state and relate OTOC
decay to mutual information between input subsystems and output partitions.
Their key message for us is:

```text
generic decay of OTOCs
  -> input subsystems have nearly vanishing mutual information with most output
     partitions.
```

Yoshida-Kitaev use OTOC decay in the Hayden-Preskill setting and show that it
guarantees faithful recovery.  Their setting is idealized, but the logic is the
one we need: once the wrong output subsystem is decoupled from the input
reference, the complementary output can recover the code.

Thus the following implication is safe to use as a literature-backed bridge:

```text
OTOC/channel scrambling for the composed block channel
  -> reference decoupling
  -> Hayden-Preskill-style recovery.
```

The paper should use this bridge if we discuss a concrete `H_mix`.

References:

```text
P. Hosur, X.-L. Qi, D. A. Roberts, B. Yoshida,
"Chaos in quantum channels", JHEP 2016, arXiv:1511.04021.

B. Yoshida, A. Kitaev,
"Efficient decoding for the Hayden-Preskill protocol", arXiv:1710.03363.
```

## Known Bridge 2: Expander/Sparse Graphs to Fast Operator Growth

This part is partially standard.

Barbon-Magan propose local quantum systems on expander graphs as microscopic
models for horizon thermalization.  Their claim is directly aligned with our
candidate: expander connectivity gives a fast scrambler with sparse local
interactions on the graph.

Bentsen-Gu-Lucas analyze fast scrambling on sparse graphs.  They emphasize
operator growth and OTOCs, and argue that logarithmic scrambling can be
achieved in sparse-connectivity systems.  Their work supplies the right
operator-growth language for an expander graph.

What these papers give:

```text
bounded-degree nonlocal graph geometry can support O(log N) scrambling;
operator growth/OTOC spreading is the relevant diagnostic;
expander-like or sparse nonlocal connectivity is a standard route to fast
scrambling without complete all-to-all coupling.
```

References:

```text
J. L. F. Barbon, J. M. Magan,
"Fast Scramblers, Horizons and Expander Graphs", JHEP 2012, arXiv:1204.6435.

G. Bentsen, Y. Gu, A. Lucas,
"Fast scrambling on sparse graphs", PNAS 2019, arXiv:1805.08215.
```

## The Missing Implication

The literature does not appear to give, off the shelf, this theorem:

```text
For the fixed nonintegrable spin Hamiltonian K_E on a deterministic expander,
the block channel V_block has small I_2(input code : wrong output partition)
for the evaporation partitions needed here.
```

Graph expansion alone gives a strong reason to expect rapid spreading.  It does
not automatically prove:

```text
1. absence of relevant hidden conserved quantities inside P_E;
2. sufficiently uniform operator weight over all area channels;
3. small channel mutual information for the particular B/R partitions;
4. decoupling for a code subspace of the intended size.
```

This is the real remaining hard point.

## Useful Tweak: Replace Design by OTOC-Decoupling Condition

The strongest useful reformulation is:

```text
Assume the block channel generated by K_E satisfies the OTOC/channel-scrambling
condition needed for small second-Renyi mutual information between the input
code and the wrong output subsystem.
```

In symbols, for each block or for the composed post-Page channel, require

```text
I_2(Q : X_wrong) <= epsilon,
```

where `X_wrong = R_so_far` before Page time and `X_wrong = B_remaining` after
Page time.

Then Pinsker-type bounds give trace-distance decoupling, and the decoupling
theorem gives recovery from the complementary subsystem.

This replaces the stronger sufficient condition

```text
K_E generates an approximate unitary 2-design on the whole active shell.
```

It is also closer to the expander/OTOC literature.

## Coarse-Block Time Scale

For Schwarzschild scaling,

```text
t_emit ~ M,
t_scr  ~ M log M,
t_evap ~ M^3.
```

So

```text
t_scr / t_emit ~ log M,
t_evap / t_scr ~ M^2 / log M.
```

The model should therefore use scrambling blocks, not per-quantum scrambling.
Each block contains `O(log M)` emitted quanta.  The Page-curve and island-min
statements are coarse trajectory statements and naturally live at this block
level.

This removes an unnecessarily strong demand from the Hamiltonian.

## What We Can Claim If This Condition Holds

If the expander mixer satisfies the OTOC/channel-decoupling condition on the
active support, then the rest of Result 2 follows:

```text
S(E) ~ E^2
  -> T ~ 1/E and negative heat capacity.

A(E)-many weak channels
  -> Hawking number flux, power, and lifetime scaling.

DOS ratio
  -> local thermality and finite-energy correction.

OTOC/channel decoupling of the block map
  -> Page curve, post-Page early/late correlations, and Hayden-Preskill-style
     recovery for the chosen code subspace.
```

This would make the expander model a strong deterministic version of the ideal
Hamiltonian evaporator.

## What Is Still Missing

We do not yet have a proof that the fixed expander spin Hamiltonian above
satisfies the needed OTOC/channel-decoupling condition.

The current evidence is:

```text
expander horizon models motivate the graph;
sparse-graph scrambling literature motivates logarithmic operator growth;
channel-scrambling literature turns OTOC decay into mutual-information
decoupling.
```

The unproved bridge is:

```text
this particular K_E
  -> the needed OTOC/channel mutual-information bound for the evaporation
     partitions.
```

That is a narrower and more standard hard problem than proving a full design
theorem.

## Possible Next Moves

### Analytical route

State a conditional lemma:

```text
If the expander block channel has
I_2(Q:X_wrong) <= epsilon
for the relevant code and partition, then the evaporation channel has the
Page/Hayden-Preskill information-flow behavior.
```

This lemma is largely a direct application of decoupling and channel-scrambling
results.  It is worth writing because it isolates the exact condition the
Hamiltonian must meet.

### Literature route

Look for a theorem specifically connecting nonintegrable Hamiltonian dynamics
on deterministic expanders to OTOC decay or channel mutual information.  The
papers checked so far motivate this strongly but do not appear to give the
exact statement.

### Numerical route

Use small deterministic expander Hamiltonians to measure:

```text
I_2(input code : output partition),
OTOC decay averaged over area channels,
reference/core decoupling after Page-like partitions.
```

This would test the missing implication directly without confusing it with the
thermodynamic/rate part of the model.

## Current Status

Established:

```text
The design requirement can be weakened to a standard OTOC/channel-decoupling
condition.
```

Established:

```text
Expander H_mix is the best candidate for making that condition natural.
```

Still open:

```text
Prove or demonstrate that the fixed expander Hamiltonian actually satisfies the
condition for the evaporation block channel.
```

This is where the project stands on the hard deterministic-scrambler issue.
