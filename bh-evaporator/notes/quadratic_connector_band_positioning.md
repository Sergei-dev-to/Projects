# Quadratic Connector Band Positioning

## Why This Note Exists

The connector heating gate narrowed the live branch to spectra with a
quadratic low-energy dispersion:

```text
omega(k) ~ k^2.
```

The linear ring has better simple power scaling, but fails the heating
robustness gate. The quadratic ring heats.

The immediate question is whether a quadratic critical connector band is a
recognizable physical structure or just a numerical convenience.

## Standard Language

The standard terms to use are:

```text
quadratic dispersion;
z = 2 dynamical exponent;
type-B Nambu-Goldstone mode;
ferromagnetic magnon;
nonrelativistic Goldstone mode;
Lifshitz criticality.
```

The point is not that our connector modes are literally magnons. The point is
that gapless quadratic collective modes are standard in nonrelativistic many-
body physics.

## Literature Anchor

Watanabe's review on Nambu-Goldstone counting emphasizes that in systems
without Lorentz invariance, Nambu-Goldstone dispersions need not be linear:

```text
Watanabe, "Counting Rules of Nambu-Goldstone Modes",
Annual Review of Condensed Matter Physics 11, 169-187 (2020).
DOI: https://doi.org/10.1146/annurev-conmatphys-031119-050644
```

The review page states that when Lorentz invariance is absent, the dispersion
of Nambu-Goldstone modes is "not necessarily linear."

Hayata and Hidaka state the sharper type-A/type-B distinction:

```text
type-A modes: linear dispersion;
type-B modes: quadratic dispersion.
```

Reference:

```text
Hayata and Hidaka, "Dispersion relations of Nambu-Goldstone modes at finite
temperature and density", Phys. Rev. D 91, 056006 (2015).
arXiv: https://arxiv.org/abs/1406.6271
DOI: https://doi.org/10.1103/PhysRevD.91.056006
```

There is also a one-dimensional `z=2` Lifshitz-critical literature, but it
comes with a warning: interactions can destabilize a quadratic fixed point or
drive it toward a linear low-energy theory. That matters for us because the
quadratic connector band may need symmetry protection or a ferromagnetic/type-B
mechanism.

Reference:

```text
Wang, "Quantum z=2 Lifshitz criticality in one-dimensional interacting
fermions", Phys. Rev. B 108, L081112 (2023).
arXiv: https://arxiv.org/abs/2302.13243
DOI: https://doi.org/10.1103/PhysRevB.108.L081112
```

## Consequence For The Model

The viable connector sector should not be described as a generic critical
chain. A generic critical chain suggests linear dispersion.

The more accurate target is:

```text
an O(N^2)-mode relational sector with a protected quadratic collective band.
```

The most physically legible analogy is:

```text
a ferromagnetic or type-B Goldstone-like connector sector living on relational
links.
```

## Remaining Non-Naturalness

This does not solve the model problem. It only makes the required spectrum less
mysterious.

Still missing:

```text
1. why the relational connector modes organize into one effective band;
2. why that band has O(N^2) length;
3. what symmetry or ordered phase protects the quadratic dispersion;
4. how a site leaving the core deactivates the right connector modes;
5. whether the same Hamiltonian gives the power scaling and Page-like
   information diagnostics.
```

## Updated Search Target

The next candidate model should be built around:

```text
N active constituents;
L(N) ~ N^2 relational connector degrees;
a ferromagnetic/type-B Goldstone-like Hamiltonian on those connectors;
local emission operators coupled to the connector band;
an autonomous mechanism that changes L(N) as the active core shrinks.
```

This is the strongest current no-settling direction.
