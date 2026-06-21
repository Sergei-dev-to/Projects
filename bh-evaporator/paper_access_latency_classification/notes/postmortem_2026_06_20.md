# Constrained-Access Postmortem

Date: 2026-06-20

Role: decision note / stop rule

Status: current

## Verdict

The constrained-access program produced a useful organizing language, but
not an uncovered result at the level we were looking for.

The central mechanisms have prior homes:

- static public/private access structure: quantum secret sharing, data
  hiding, private quantum channels, locking, decoherence-free/noiseless
  subsystems;
- recovery versus scrambling as a sharper diagnostic than OTOCs or level
  statistics: Hayden-Preskill recovery in Hamiltonian and circuit
  systems;
- symmetry and conservation-law obstructions to coherent recovery:
  Hayden-Preskill with symmetry and symmetry-versus-coherence recovery
  bounds;
- locality, latency, and light-cone constraints: Lieb-Robinson bounds
  and local Hamiltonian recovery studies;
- logarithmic recovery/scrambling on sparse or expander-like geometries:
  fast-scrambler and expander-graph literature;
- export once the right subsystem is available: standard decoupling and
  Hayden-Preskill recovery.

Our remaining contribution is synthesis: the access/export two-bottleneck
organization, the routed-versus-dressed recovery distinction, and the
application of these ideas to horizon/cut language. That is useful, but
it is not enough to keep mining this direction as a primary source of new
results.

## What Looked Novel

The promising candidate was:

```text
scrambling / de-protection / public record formation
does not imply
coherent private recovery from a specified access channel.
```

Together with the latency version:

```text
an abstractly authorized recovery set may exist,
but local physical dynamics constrains how quickly that set can be
generated from source-local records.
```

These are good organizing statements. The issue is that the ingredients
are already well developed in the adjacent literature.

## Literature Absorption

Representative anchors:

- Nakata--Tezuka, "Hayden-Preskill Recovery in Hamiltonian Systems":
  recovery is possible in some but not all chaotic Hamiltonian models,
  separating HP recovery from energy-spectrum chaos and OTOC diagnostics.
- Rampp--Claeys, "Hayden-Preskill recovery in chaotic and integrable
  unitary circuit dynamics": HP recovery as a dynamical probe of local
  many-body circuits.
- Nakata--Wakakuwa--Koashi, "Black holes as clouded mirrors": symmetry
  delays leakage and leaves information remnants in Hayden-Preskill.
- Tajima--Saito, "Universal limitation of quantum information recovery:
  symmetry versus coherence": conservation laws impose recovery limits
  for coherent information.
- Barbon--Magan and Bentsen--Gu--Lucas: expander/sparse-graph routes to
  logarithmic fast scrambling and horizon analogies.
- Brown--Fawzi and standard one-shot decoupling: once the relevant
  subsystem is available, recovery follows from known decoupling
  machinery.

## What Remains Useful

Keep these as language and scaffolding:

```text
publicization != de-protection != coherent export
```

```text
recovery has two bottlenecks:
    access geometry / routing;
    coherent export / decoupling.
```

```text
fast private recovery requires either:
    fast internal routing/scrambling plus export;
or
    nonlocal/dressed access that bypasses source-local routing.
```

```text
horizons and measurement cuts can be compared through access profiles,
but this comparison is interpretive unless tied to a concrete new
calculation.
```

These ideas may still help frame other drafts, especially when avoiding
overclaims about what follows from Page/decoupling alone.

Use them defensively, not generatively. The right use is auditing a claim
(does this actually follow from decoupling, or only from de-protection?).
The wrong use is making access/export the organizing lens of the next
project, which is how this vocabulary would leak into boundary-saturation
or super-Hagedorn and restart the synthesis habit one directory over. The
toolkit checks claims; it does not frame programs.

## Stop Rule

Do not write more broad constrained-access synthesis notes unless the
work is attached to one of:

- a concrete calculation;
- a proof that is not already a direct restatement of QI/crypto/HP/LR
  results;
- a specific draft section that needs positioning.

In particular, do not run the proposed U(1) recovery-versus-scrambling
phase diagram as a discovery search. Symmetry obstruction and recovery
versus chaos are already covered well enough that the likely outcome is
reproduction.

This note is terminal. The first test of the stop rule is whether it is
the last word. A "postmortem addendum" or "follow-up" is itself a
violation; the next file in this folder should be a literature check on a
different problem, not a reflection on this one.

## Start Rule For The Next Program

The real lesson is not "constrained access is mined." It is that we
invested heavily before checking whether the territory was occupied. The
half-day literature pass that closed this program could have run at the
start.

So the carry-forward is a start rule, not just a stop rule:

```text
before drafting or proving in a new direction,
spend one day on a literature pass.
if the core mechanism already has a home, narrow or redirect
before investing, not after.
```

The asset this program actually produced is not the synthesis language.
It is fluency in the recovery / scrambling / crypto / Lieb-Robinson
corner of the literature, acquired by reconstructing it. That fluency is
what makes the next literature pass take a day instead of a month. Bank
that, not the notes.

## Where To Go Next

The stronger result candidates now lie elsewhere:

1. Boundary saturation / de Sitter reservoir contrast.
2. Super-Hagedorn state count and forced corpuscular kinematics.
3. Operational Hamiltonian model cleanup and precise necessity claims.
4. Variance / half-wormhole calculation.
5. Other repo directions with less saturated overlap.

Gate each candidate on the start rule: a one-day literature pass before
any drafting. These are all still inside the bh-evaporator program, so
treat the first lit-check as a signal about the program, not only the
sub-direction. If candidate 1 comes back as occupied as constrained
access did, the honest read is that the diminishing returns are at the
program level, and the move is out of bh-evaporator entirely (wormholes,
anyons, Alcubierre) where a literature pass may come back empty.

The constrained-access work should remain a citation-backed conceptual
toolkit, not the main result engine.
