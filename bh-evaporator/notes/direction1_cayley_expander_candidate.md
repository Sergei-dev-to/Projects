# Direction 1: Cayley-Expander Fixed Mixer

## Goal

Close Gap 2 as far as possible with an explicit deterministic Hamiltonian:

```text
fixed graph,
fixed homogeneous couplings,
symmetry-related boundary emission operators,
fast channel scrambling.
```

The aim is not to prove a full unitary design.  The aim is to supply the
decoupling input needed by the evaporation channel.

## Deterministic Graph Choice

Use an explicit Cayley expander family

```tex
G_N = {\rm Cay}(\mathcal G_N,S_N),
```

where `\mathcal G_N` is a finite group and `S_N` is a symmetric generating set
of bounded size.  The vertices are group elements `g in \mathcal G_N`, and
edges connect

```tex
g \longleftrightarrow gs,\qquad s\in S_N.
```

Cayley graphs are vertex-transitive because the group acts on itself by left
multiplication.  Explicit Ramanujan/Cayley expander families exist; the
Lubotzky-Phillips-Sarnak graphs are the standard example.

This is better than a generic deterministic expander for our purpose because
vertex transitivity gives exact equivalence of boundary labels.

## Hamiltonian

Put one qubit or qudit on each vertex.  A homogeneous anisotropic spin
Hamiltonian is

```tex
K_N =
\sum_{g\in\mathcal G_N}
\sum_{s\in S_N^+}
\left(
J^x_s X_gX_{gs}
+J^y_s Y_gY_{gs}
+J^z_s Z_gZ_{gs}
\right)
+\sum_{g\in\mathcal G_N}
\left(h_xX_g+h_zZ_g\right).
```

Here `S_N^+` chooses one orientation from each inverse pair to avoid double
counting.  The generator-dependent couplings `J_s^a` can break accidental
edge-color symmetries while preserving vertex transitivity.  The two nonparallel
fields `h_x,h_z` remove simple spin-component conservation.

The full shell mixer is

```tex
H_{\rm mix}
=
\bigoplus_E P_E K_{N(E)}P_E.
```

No coupling is resampled during evaporation.

## Boundary Emission Operators

Use one local emission operator per vertex:

```tex
O_{g,\lambda} = O_\lambda(g).
```

The radiation coupling is

```tex
H_I =
g_{\rm em}
\sum_{g\in\mathcal G_N}
\sum_\lambda
\int d\omega\,\omega^{p/2}
\left[
O_{g,\lambda}(\omega)b^\dagger_{g,\lambda}(\omega)
+{\rm h.c.}
\right].
```

The left-regular action `L_a:g -> ag` is represented by a unitary `U_a` on the
spin Hilbert space.  By construction,

```tex
[U_a,K_N]=0,
\qquad
O_{ag,\lambda}=U_aO_{g,\lambda}U_a^\dagger.
```

Therefore `[U_a,\Pi_E]=0`, and the shell-averaged emission weights are equal:

```tex
{\cal A}_{g,\lambda}(E,\omega)
=
{\cal A}_{g',\lambda}(E,\omega)
```

for all vertices `g,g'`.  The area factor is then exactly

```tex
\sum_g {\cal A}_{g,\lambda}
=
N(E){\cal A}_{0,\lambda}.
```

This closes the boundary-channel uniformity side of Gap 2, up to the ordinary
ETH requirement that the common local spectral function is smooth and thermal.

## What This Buys Us

The bridge lemma now becomes much sharper:

```text
Cayley symmetry
    -> exact equality of boundary-channel weights,
ETH for the common local operator
    -> smooth DOS-ratio emission spectrum,
OTOC/channel scrambling for K_N
    -> Page decoupling for typical emitted histories.
```

Thus the only hard dynamical input left is channel scrambling of `K_N`.

## Symmetry Sectors

The same symmetry that gives uniform emission also creates conserved group
quantum numbers.  This is not fatal, but it must be handled.

There are two clean options:

1. Work in a fixed irreducible representation sector of the Cayley symmetry and
   state the decoupling result for code subspaces inside chaotic energy windows
   of that sector.
2. Include the symmetry charge as a classical/superselection label and exclude
   it from the information claimed to be hidden in the Page calculation.

The model should not claim to scramble information stored purely in exact
symmetry charges.

## Remaining Scrambling Question

We need a statement of the form

```tex
K_N
\quad\Rightarrow\quad
\epsilon_{\rm scr}(N,m,t)\to0
```

for `t = O(log N)`, where `epsilon_scr` is the channel-scrambling or OTOC
quantity used in the decoupling theorem.

Existing sparse/expander fast-scrambling work supports this route but does not
appear to provide the exact theorem for the homogeneous Cayley-expander
Hamiltonian above.

The next search target is therefore specific:

```text
OTOC/operator spreading for homogeneous quantum spin Hamiltonians on Cayley or
Ramanujan expanders.
```

If no theorem exists, the fallback is to cite the sparse-graph fast-scrambling
literature as motivation and leave the Cayley-expander channel-scrambling
statement as a precise open input.

## Status

This direction is stronger than the previous deterministic-expander proposal:

```text
boundary uniformity        essentially closed by Cayley symmetry,
local thermality           ETH input for one common operator,
Page information hiding    reduced to channel scrambling of K_N.
```

It does not close Gap 2 completely unless the OTOC/channel-scrambling bound can
be imported or proven for this Hamiltonian family.

## Sources

- Lubotzky, Phillips, Sarnak, "Ramanujan graphs," Combinatorica 1988.
- Harrow, "Quantum expanders from any classical Cayley graph expander,"
  Quantum Information and Computation 2008.
- Barbon, Magan, "Fast Scramblers, Horizons and Expander Graphs,"
  arXiv:1204.6435.
- Bentsen, Gu, Lucas, "Fast scrambling on sparse graphs," arXiv:1805.08215.
- Hosur, Qi, Roberts, Yoshida, "Chaos in quantum channels,"
  arXiv:1511.04021.
