# Four-row obstruction to the empty-tetrahedron mechanism

**Date:** 2026-07-23
**Status:** exact proof with a standalone finite verifier; specialist prior-art
review still required before any novelty claim.

## Theorem

For every integral boundary `(lambda, mu, nu)` with at most four rows, the hive
polytope is not an empty lattice tetrahedron of normalized volume
`Delta >= 2`. Equivalently:

> Every four-row hive polytope that is an empty lattice tetrahedron is
> unimodular.

This excludes the Reeve empty-tetrahedron mechanism through the
four-lattice-point channel. It is not a proof of four-row stretched-LR
positivity: hives with five or more lattice points are not covered.

## Proof

### 1. Fixed primitive normals in the correct lattice

After fixing the boundary, a side-four hive has the three free labels
`h_11, h_12, h_21`. Integral hives are exactly the points of `Z^3` in these
coordinates; there is no quotient lattice or hidden saturation factor.

The 18 rhombus inequalities have boundary-independent coefficient rows. With
multiplicity, they are

```text
+/- e1, +/- e2, +/- e3                 (each +ei occurs twice)
+/- (1,-1,0)
(1,0,-1), (0,1,-1), (-1,0,1), (0,-1,1)
(1,1,-1), (1,-1,1), (-1,1,1)
```

All rows are primitive. For a presentation `A x >= b`, a row points inward; an
outward facet normal is therefore a positive multiple of its negative. The sign
will not matter because only determinant magnitudes are used.

### 2. Exact minor census

The exact census of all `C(18,3) = 816` row triples is

| determinant magnitude | 0 | 1 | 2 | 4 |
|---:|---:|---:|---:|---:|
| number of triples | 299 | 468 | 48 | 1 |

The unique magnitude-four triple is

```text
(1,1,-1), (1,-1,1), (-1,1,1).
```

Thus every row-triple determinant has magnitude at most four, and only one
unordered row triple attains four. The standalone standard-library verifier is
`verify_four_row_obstruction.py`; its retained output is
`four_row_obstruction_certificate.json`.

The presence of magnitude-two and magnitude-four minors also shows why a blanket
Hoffman-Kruskal or total-unimodularity argument is unavailable.

### 3. Facet-normal lemma for empty tetrahedra

White's classification puts every empty lattice tetrahedron of normalized
volume `q`, up to an affine unimodular change of coordinates, in the form

```text
T(p,q) = conv{0, e1, e3, (p,q,1)},    gcd(p,q) = 1.
```

One choice of primitive facet normals is

```text
n1 = ( 0,-1, 0)
n2 = ( 0, 1,-q)
n3 = ( q,-p, 0)
n4 = (-q, p,-q).
```

Direct expansion gives

```text
det(n1,n2,n3) =  q^2
det(n1,n2,n4) = -q^2
det(n1,n3,n4) = -q^2
det(n2,n3,n4) =  q^2.
```

Under `x -> Ux+t`, with `U in GL_3(Z)`, primitive normal covectors transform by
`U^(-T)`. Their triple determinants therefore change only by a global sign. It
follows that every empty lattice tetrahedron of normalized volume `Delta` has
all four primitive facet-normal triples of determinant magnitude `Delta^2`.

### 4. Comparison with the hive rows

Every facet of a full-dimensional polytope given by finitely many halfspaces is
contained in at least one defining constraint hyperplane. If `p` is its
primitive normal and `r` is a parallel integral constraint row, then
`r = +/- k p` for an integer `k >= 1`. Hence

```text
|det(r_i,r_j,r_k)| >= |det(p_i,p_j,p_k)| = Delta^2.
```

If `Delta >= 3`, a facet-row triple would have determinant magnitude at least
nine, contradicting the census maximum of four.

If `Delta = 2`, choose one defining row for each of the four tetrahedron facets.
The four distinct three-subsets of those rows would all need determinant
magnitude four. The entire 18-row system has only one such triple. This is also
impossible. Therefore `Delta = 1`. QED.

## Corollary using known four-row integrality

Buch states that all vertices of an integral-boundary hive are integral for
`n <= 4`; Coquereaux-Zuber repeat the SU(4) fact. Consequently, every
three-dimensional four-row hive with exactly four lattice points is an empty
lattice tetrahedron, and the theorem forces it to be unimodular.

This is the precise relation to the finite pool in
`FOUR_ROW_SCREEN_RESULT.md`: the 150,316 count includes lower-dimensional
members, so it is not a count of 150,316 tetrahedra.

## Finite-screen coefficient conclusion

For a stretching polynomial of degree at most three,

```text
P(t) = 1 + a1 t + a2 t^2 + a3 t^3,
c1 = P(1),  c2 = P(2),
```

one has

```text
a1 = (4 c1 - c2 - 3)/2 + 2 a3.
```

The completed `c1=4` screen found `c2 <= 10`, so `a1 > 0`. The other
coefficients are also positive whenever present. One proof that does not assume
vertex integrality is to choose `D` so that `D H` is a lattice polytope. Then
`L_{D H}(s) = L_H(Ds) = P(Ds)`. In dimension three the coefficient of `s^2`
is half the positive normalized boundary volume, so `D^2 a2 > 0`; in lower
dimension the top nonzero coefficient is positive. Thus the recorded `c1=4`
pool has positive coefficients, although this says nothing about the
`c1 >= 5` channel.

## Scope and literature

- Open here: four-row hives with at least five lattice points.
- Untouched: lengths five through seven of the official target.
- The determinant obstruction is plausibly not stated in this form in the
  sources checked, but no novelty or publishability claim is made.

Primary references:

- A. S. Buch, *The saturation conjecture (after A. Knutson and T. Tao)*,
  arXiv:math/9810180, especially the `n <= 4` integrality statement after
  Example 2.
- R. Coquereaux and J.-B. Zuber, *From orbital measures to
  Littlewood-Richardson coefficients and hive polytopes*, arXiv:1706.02793.
- G. K. White, *Lattice tetrahedra*, Canadian Journal of Mathematics 16 (1964),
  389-396; see also Blanco-Santos, arXiv:1409.6701, Theorem 2.4, for the exact
  `T(p,q)` normal form used above.
