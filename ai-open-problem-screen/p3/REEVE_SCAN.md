# Frozen empty-Reeve direct scan

Status: **internal, bounded, non-certifying direct search**. This replaces the
proposed control bake-off before any prospective artifact or polynomial result
was created. It does not revive the superseded P3 held-out gate.

## Why this is a direct scan, not a bake-off

For a 3-dimensional integral tetrahedron with exactly its four vertices as
lattice points and normalized volume `Delta`,

```text
L(t) = 1 + (12-Delta)/6 t + t^2 + Delta/6 t^3.
```

Consequently, the geometric data needed for the proposed “Reeve ranker” already
determine the polynomial and its sign. Comparing rankings after computing those
data would not measure predictive efficiency. The honest experiment is to scan
a frozen finite panel for the exact structural signature and dual-verify every
hit.

## Frozen design

- Universe: exact `N=1` support of B1 minus B0-7, restricted to `len(nu)>=4`.
  Expected size: 1,020,764.
- Mechanism slice: `c(1)==4`, necessary for an empty lattice tetrahedron. This
  is paid common `N=1` preprocessing, not a label-free claim.
- Panel: 512 triples allocated proportionally across
  `(len(nu), max(|lambda|,|mu|))` strata and selected by a fixed,
  domain-separated SHA-256 key.
- Geometry: explicit hive inequalities followed only by exact Normaliz
  `AffineDim` and `VerticesOfPolyhedron` calls. The normalized tetrahedron
  volume is the gcd of all `3x3` edge-matrix minors in the saturated affine
  lattice.
- Hit: affine dimension 3, exactly four integral vertices, and `Delta>12`.
- Verification: every hit must agree under bounded and conservative E1 exact LR
  interpolation and E2 raw-period-one Normaliz Ehrhart evaluation.

The full eligible-universe stream and the complete `c(1)==4` mechanism pool are
hash-pinned before sampling. Geometry and verification are resumable immutable
per-triple records. Query counts—not an efficiency comparison—enforce the
budget.

## Outcomes

- A dual-evaluator hit becomes a candidate-verification event. It is not an
  automatic publication or scaling authorization.
- Zero hits yields `BUDGET_STOP_NO_HIT_IN_FROZEN_PANEL`. This is a resource
  decision about this 512-case panel, not evidence that the Reeve mechanism is
  absent from the million-case universe and not evidence for positivity.
- Any formula, period, lattice-count, or evaluator disagreement fails closed.

## Completed run

`run/p3/empty-reeve-scan-v2` completed with deep verification
(`complete=true`). The exact eligible universe contains 1,020,764 triples and
the complete `c(1)==4` mechanism slice contains 48,019. In the frozen 512-case
panel, 86 polytopes have affine dimension 2 and 426 are empty integral
3-tetrahedra. Every one of those 426 tetrahedra has `Delta=1`; there are zero
`Delta>12` signatures.

Decision: `BUDGET_STOP_NO_HIT_IN_FROZEN_PANEL`. Plan/panel/geometry/adjudication/
manifest hashes begin `c41e72ad` / `23463f3f` / `2a8f5136` / `c8cfd575` /
`edd4bb43` respectively.
