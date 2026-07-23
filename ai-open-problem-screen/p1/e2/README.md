# E2: explicit hives + Normaliz

This directory is the independent geometric evaluator for Phase 1. It does not
import or reuse either dry-run LR counter or its interpolation code. It constructs
the hive inequalities, eliminates only the fixed boundary variables, and gives the
remaining integral-coordinate polytope directly to Normaliz.

## Frozen coordinate convention

For side length `n`, vertices are `q[i,j]` with `i,j >= 0` and `i+j <= n`.
Partitions are padded with zeros to length `n`, and the three boundaries are

```text
q[k,0]   = lambda_1 + ... + lambda_k
q[0,k]   = nu_1     + ... + nu_k
q[n-k,k] = |lambda| + mu_1 + ... + mu_k.
```

Thus the corners are `0`, `|lambda|`, and `|nu|=|lambda|+|mu|`.
The free coordinates are exactly `q[i,j]` with `i,j >= 1` and `i+j <= n-1`,
ordered lexicographically by `(i,j)`. They carry the ordinary lattice `Z^d`.

Every rhombus is generated geometrically. For a base vertex `p` and a consecutive
direction pair `(a,b)`, the inequality is

```text
q[p+a] + q[p+b] - q[p] - q[p+a+b] >= 0,
```

the sum at the obtuse vertices at least the sum at the acute vertices. The three
families are:

```text
east_north:       a=( 1,0), b=( 0,1)
north_northwest:  a=( 0,1), b=(-1,1)
northwest_west:   a=(-1,1), b=(-1,0)
```

There are exactly `n(n-1)/2` inequalities in each family. The equivalent common
indexing `h[i,j]=q[j-i,i]`, `0<=i<=j<=n`, has boundaries along `h[0,j]`,
`h[j,j]`, and `h[i,n]`.

The convention follows the standard rule that the sum on the obtuse vertices is
at least the sum on the acute vertices; see Knutson--Tao's original honeycomb/hive
paper and the explicit boundary formulation in Rassart. The primary executable
anchor is Anders Buch, *The Saturation Conjecture (after A. Knutson and T. Tao)*,
Example 1 ([arXiv:math/9810180](https://arxiv.org/abs/math/9810180)). For
`n=3`, `lambda=mu=(2,1)`, `nu=(3,2,1)`, the sole free label `x=q[1,1]`
must satisfy `4 <= x <= 5`. The implementation produces only the two distinct
rows `x-4 >= 0` and `5-x >= 0` (with the expected geometric duplicates), hence
two integer hives and Ehrhart polynomial `N+1`.

## Fixture gate

`fixtures.json` fixes six cases:

- LR coefficient `0`, `1`, and `>1`;
- empty, zero-dimensional, positive-dimensional, and dimension-collapsed hives;
- all three rhombus orientations and all three boundary edges;
- the hand-audited Buch interval;
- an asymmetric degree-2 case; and
- the campaign's degree-6 anchor.

Run from the repository root inside the existing WSL environment:

```bash
.venv-wsl/bin/python -m unittest -v p1.e2.test_hive_e2
.venv-wsl/bin/python -m p1.e2.run_fixtures
```

The runner is fail-closed. For each fixture it preserves:

- the complete geometric rhombus list and boundary in `reports/inputs/*.hive.json`;
- the exact rows sent to PyNormaliz;
- a replayable Normaliz CLI input and raw `.out` file;
- raw Ehrhart/quasipolynomial, vertices, lattice points, and support hyperplanes;
- independent positive-stretch `lrcalc` counts; and
- every exact comparison in a per-fixture report.

It also exports `reports/fixture_agreement.json` in the controller's
`lr-p1-fixture-agreement/v1` schema. The two evaluator records point to separately
manifestable `lrcalc_interp_evaluator.json` and
`normaliz_ehrhart_evaluator.json` artifacts. `controller_adapter_artifacts.json`
contains the corresponding roles and file hashes. The `lrcalc-interp` polynomial
is genuinely recomputed from positive-stretch counts by exact Lagrange
interpolation at the universal hive-dimension degree bound, with a reserved
positive-stretch check; it is not copied from the expected fixture.

The empty fixture compares positive stretches only. `c^0_{0,0}=1` is not the
Ehrhart polynomial of an empty hive polytope; saturation makes all positive
stretches zero, whose polynomial extension is the zero polynomial.

Passing these fixtures validates this explicitly documented convention on the
fixed suite. It is necessary for P1, but this directory alone does not declare the
campaign-wide P1 gate.
