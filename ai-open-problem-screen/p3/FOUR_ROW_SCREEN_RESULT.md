# Four-row screen — complete over the corrected official domain

**Date:** 2026-07-23 · **Code:** `four_row_screen.py` · **Artifact:**
`four_row_screen_len4_size30.json` · runtime 477 s. The artifact's embedded
`0b7cc315...` value hashes its canonical semantic payload with the `sha256` field
removed; the actual file digest is recorded in the adjacent `.sha256` sidecar.

## Scope (corrected domain)

All three partitions of length ≤ 4, and `|ν| = |λ| + |μ| ≤ 30` — the **corrected**
official bound (each partition weight ≤ 30), not the earlier erroneous independent
`|λ|,|μ| ≤ 30`. Hive dimension for n = 4 is `(n−1)(n−2)/2 = 3`, so `deg P ≤ 3`.

## The exact test

Four-row (`n <= 4`) integral-boundary hives have integral vertices (Buch,
following Example 2; also Coquereaux-Zuber for SU(4)). Therefore a
3-dimensional four-row hive with exactly 4 lattice points is an **empty lattice
tetrahedron**; by White's classification its Ehrhart polynomial is

    P(t) = (Δ/6)t³ + t² + (2 − Δ/6)t + 1,     Δ = normalized volume,

so `P(1) = 4` identically and `P(2) = Δ + 9`. The linear coefficient is negative
exactly when `Δ > 12`, i.e. **`P(2) > 21`**.

Dimension needs no separate computation: a lattice polytope of dimension ≤ 2 with
4 lattice points has `P(2) ≤ 10` (dim 1 → 7; dim 2 by Pick with `I+B=4` → 9 or 10).
So any hit with `P(2) > 21` is necessarily a 3-dimensional empty tetrahedron with
`Δ > 12` — a genuine negative coefficient. Both counts use **capped** LR counting
(abort once the threshold is exceeded), avoiding construction of larger tableau
counts; this is an execution cap, not an `O(cap)` worst-case time bound.

## Result

| Quantity | Value |
|---|---:|
| support-compatible triples | 9,332,014 |
| nonzero triples | 4,229,644 |
| mechanism pool (`c(1) = 4`) | 150,316 |
| **hits (`c(2) > 21`)** | **0** |
| **maximum `c(2)` over the entire pool** | **10** |

`c(1)` histogram (capped at 5): `1→2,622,691  2→927,080  3→365,496  4→150,316
≥5→164,061`.

For every **three-dimensional** member of the pool, `c(2) = Δ + 9`; hence the
observed maximum `c(2) = 10` forces `Δ = 1`. Every such member is unimodular,
whereas the counterexample threshold is `Δ > 12`. The pool total 150,316 also
contains lower-dimensional polytopes and must not be reported as “150,316
unimodular tetrahedra.”

## Independent verification

Six pool members were recomputed with the *uncapped*, independently validated
evaluator, taking `c(0..4)` exactly and interpolating the full Ehrhart polynomial.
They fall into exactly two rigid families, all coefficients positive:

- dimension 2: `P = 1 + 2t + t² = (1+t)²`, `c(2) = 9`;
- dimension 3, unimodular: `P = 1 + (11/6)t + t² + (1/6)t³`, `c(2) = 10`, `Δ = 1`
  — matching the predicted empty-tetrahedron form.

The capped counter was spot-checked against the uncapped evaluator on 6,380 cases
with 0 mismatches. The original ordered validation sample and machine manifest
were not retained, so this is supporting internal evidence rather than a
publication-grade independent certificate.

## Proved structural endpoint

`FOUR_ROW_OBSTRUCTION.md` proves:

> Every four-row hive polytope that is an empty lattice tetrahedron is
> unimodular.

The exact finite normal census is reproduced by
`verify_four_row_obstruction.py`. This is a genuine but narrow outcome-C result;
no novelty claim is made pending specialist prior-art review.

## Scope limits — what this does NOT establish

- **Only the empty-tetrahedron (Reeve) mechanism.** Dimension-3 hives with more
  than 4 lattice points (`c(1) ≥ 5`: 164,061 triples) are **not** screened.
- **Only four rows.** Lengths 5–7 of the official target are untouched.
- The result closes the four-point Reeve mechanism, **not** four-row positivity.

### Cheap route to a complete four-row screen

For `dim ≤ 3` write `P(t) = a₃t³ + a₂t² + a₁t + 1`. For a 3-dimensional lattice
polytope `a₃` (volume) and `a₂` (half the normalized surface area) are always
positive, so `a₁` is the only coefficient that can be negative. From
`c₁ = P(1)`, `c₂ = P(2)`:

    6a₃ + 2a₂ = c₂ − 2c₁ + 1,        a₁ = c₁ − 1 − a₂ − a₃,

and maximizing `a₂ + a₃` subject to `a₂, a₃ ≥ 0` gives the **necessary condition**

    a₁ < 0   ⟹   c₂ > 4c₁ − 3.

So a complete four-row screen needs only `c(1)` and `c(2)` per triple, with the
exact `c(3)` evaluation reserved for the (presumably tiny) set passing
`c₂ > 4c₁ − 3`. For `c₁ = 4` this reduces to `c₂ > 13`, weaker than — and
consistent with — the exact empty-tetrahedron test `c₂ > 21`.
