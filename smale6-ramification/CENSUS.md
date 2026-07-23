# Ramification candidate search on (1,1,μ,μ,ν), seeded at Chen--Hsiao

**Snapshot:** 2026-07-22
**Status:** double-precision discovery stage (Gate 4 of the stop/go protocol in
`SMALE6_PROGRAM_RETROSPECTIVE.md`).  Nothing below is interval-certified; the
claims are numerical classifications with stated separations, not proofs.

**Post-run audit:** this file now distinguishes a numerically followed route
in the augmented singular system from an exhaustive census of a physical
discriminant component.  The latter has **not** been achieved.  The detector
sees sampled sign changes of \(Q\), so it can miss tangential or
even-multiplicity zeros and pairs of zeros between steps.  At a corank-two
point the normalized kernel vector adds an \(S^1\) fiber to the augmented
system, and one pseudo-arclength path need not visit every physical branch.

## What was run

`census.js` implements the first-priority track from the retrospective: instead
of hand-picking singular configurations, it traces the singular set of the mass
projection on the two-equal-pairs family

\[
\{(z,\mu,\nu): F(z;\mu,\nu)=0,\ \operatorname{corank} D_zF\ge1\},
\]

by pseudo-arclength continuation of the augmented system
\([F;\,(D_zF)v;\,v\cdot v-1]=0\) in the 20 unknowns \((z,v,\mu,\nu)\),
starting from the certified Chen--Hsiao fold of `CERTIFIED_FOLD.md`.  The
masses are genuine Taylor variables in the series evaluator, so every Jacobian
block and second derivative is exact modulo rounding; no finite differences
occur anywhere.  Along the curve it evaluates

- the fixed-mass Lyapunov--Schmidt quadratic obstruction
  \(Q=\tfrac12 w^TD_z^2F[v,v]\) (left kernel vector \(w\) continued by sign),
- the mass-transversality projections \(w^TF_\mu\), \(w^TF_\nu\),
- the second singular value \(\sigma_2\) of \(D_zF\) (corank-two watch),
- positivity, collision, and gauge monitors.

Sampled sign crossings of \(Q\) are refined by bisection with Newton
reprojection and then re-examined by the independent fixed-mass
`jet_sieve.js` at frozen masses.  Near-corank-two hits are escalated to a
kernel-circle sweep (`census_corank2.js`).  This is a candidate generator, not
an interval enclosure or complete zero finder.  A post-run code audit also
found and fixed an off-by-one pairing error in the refinement endpoints; the
reported simple-zero coordinates were reproducible, but the original code
supplied a wider, not necessarily bracketing chord.

**Seed controls.**  At the seed the pipeline reproduces the certified data:
\(\sigma_1\approx7\times10^{-14}\), \(\sigma_2=0.20844188\) (matches the
0.2084418804 separation in `RESULT.md`), \(Q=-0.17725540366\) (matches the
recorded order-two obstruction norm 0.177255403655 up to the sign convention of
\(w\)), and \(w^TF_\nu\ne0\).  The Chen--Hsiao point is thus correctly
classified as an ordinary fold by the very pipeline that must discard folds.

## Extent of the followed routes

Gauge: inertia fixed at the Chen--Hsiao value \(I=5.442203764127745\)
throughout; scale-invariance makes this a valid slice.

- **Forward route** (4000 steps, arclength ≈ 160): \(\mu\) climbs
  monotonically from 7.215 to 22.41.  The sampled \(\nu\) reaches a minimum
  0.4454517 near \(\mu=20.34\) and then rises slightly to 0.4456729; no
  asymptotic limit is established.  \(\sigma_2\) decays from 0.208 to 0.021.
  The normal-equations eigensolver also loses small-mode accuracy at this end
  (reported \(\sigma_1\) reaches about \(2\times10^{-9}\)).  Terminated at the
  step budget.  **Open end.**
- **Backward route** (1404 accepted steps): descends through \(\mu=1\) at
  \(\nu\approx2.3797\) (the square-plus-center point below), continues to a
  quadratic-zero point at \((\mu,\nu)\approx(0.1386,0.0718)\), then runs into
  region, where corrections become ill-conditioned near
  \((\mu,\nu)\approx(3.9\times10^{-5},2.3\times10^{-5})\) and
  \(\sigma_2\approx3.9\times10^{-6}\).  It then returns along the sampled arc
  and reaches the seed.  This is compatible with a vanishing-mass limit, but
  the chart does not resolve the boundary.  The return reproduces the
  small-mass event to about 12 digits, but it is not an independent run: the
  normalized-null-vector sheets can connect or switch at singular strata.

## Classified points

### 1. Quadratic-zero point adjacent to Chen--Hsiao — rejected at order 3

\[
(\mu,\nu)=(7.215936934146546,\ 0.518255839161033),\qquad
\lambda=16.953678364645.
\]

\(Q\) crosses zero here (arclength 0.045 from the seed).  Independent
fixed-mass jet check: corank one (\(\sigma_2=0.2085\)), order-2 obstruction
\(1.7\times10^{-12}\), order-3 obstruction \(36.81\).  The fixed-mass kernel
direction therefore fails its next compatibility condition and is **not a
continuum source** (numerically).  Calling the mass projection an ordinary
cusp would additionally require the standard unfolding and transversality
checks; those were not run.  No conclusion is drawn merely from its proximity
to the Chen--Hsiao point.

### 2. Square plus central body at μ=1 — corank two, quadratic forced to vanish, rejected at order 3

At \(\mu=1\) the outer masses become equal and the singular configuration is
the exact square with a central body:

\[
q_{1..4}=(\pm a,0),(0,\pm a),\quad q_5=(0,0),\qquad
a=1.1664265690698,
\]
\[
\nu_*=\frac{13+11\sqrt2}{12}=2.379695765508671\ldots,\qquad
\lambda=(1/4+1/\sqrt2+\nu_*)/a^3=2.1026079285667.
\]

The square-plus-center is an exact central configuration for **every**
\(\nu\); the gauge-fixed Jacobian degenerates at \(\nu_*\), where the census
curve crosses \(\mu=1\).  The determinant touches zero without a sign change:
the kernel is a genuine two-dimensional symmetry doublet
(\(\sigma_1,\sigma_2\approx10^{-15}\), \(\sigma_3=0.7354\)).

`census_corank2.js` samples the fixed-mass quadratic and cubic obstruction in
360 directions of the projective kernel circle:

- **order-2 samples:** maximum \(6.23\times10^{-16}\), consistent with exact
  structural vanishing;
- **order-3 samples:** minimum \(0.120764\) and maximum \(0.990230\).
  Reconstructing the homogeneous binary cubic from four directions predicts
  all sampled obstruction vectors within \(1.7\times10^{-15}\).  A
  million-angle evaluation of that fitted cubic gives minimum \(0.120726\)
  near \(\theta=2.065858\), maximum \(0.990240\), and a two-component
  Sylvester resultant of magnitude \(0.427199\).  These reproducible fields
  are stored in `cubicFitAudit` in `census_corank2_out.json`.  This is strong
  discovery evidence for no projective zero, but it is not interval proof.

The vanishing quadratic is structurally forced, not accidental.  Sketch: the
kernel doublet spans the two-dimensional irreducible representation \(E\) of
the \(D_4\) symmetry of the square; \(\mathrm{Sym}^2(E)\) decomposes into
one-dimensional representations only, while the cokernel again carries
\(E\), so no nonzero equivariant quadratic map exists.  \(\mathrm{Sym}^3(E)\)
does contain \(E\), so the cubic may be nonzero.  In symmetry-adapted complex
coordinates every such real cubic has the form
\(G(z)=\alpha z|z|^2+\beta\bar z^3\).  It has no projective zero exactly when
\((\alpha+\beta)(\alpha-\beta)\ne0\), reducing a rigorous check to the axis
and diagonal symmetry directions.  This is precisely
the retrospective's target class — "an exact symmetry … that could force the
quadratic to vanish" — and the census answer is that the mechanism dies at
cubic order.  Consistency check: the Palmore centered-triangle control also
has a doublet kernel but a \(D_3\) symmetry, for which \(\mathrm{Sym}^2(E)\)
**does** contain \(E\); its order-2 obstruction is correspondingly nonzero
(0.49–1.58 in the jet-sieve sweep).

This representation-theoretic observation is only a low-order filter.  In a
self-adjoint fixed-mass Lyapunov--Schmidt reduction, the cokernel is identified
with the kernel \(K\), and every finite isotropy group allows the equivariant
gradient cubic

\[
u\longmapsto \lVert u\rVert^2u.
\]

Thus finite isotropy alone cannot force the reduced germ to vanish at every
order.  Conversely, the fact that a cubic is symmetry-allowed does not prove
that its coefficient is nonzero or that its projective zero set is empty.
The first allowed jet must be computed, as it was here; if it vanishes, an
additional identity, factorization, syzygy, or coefficient relation is still
possible.

This calculation independently rediscovers a classical result.  Meyer and
Schmidt (1988) give the exact value above, prove nullity two, carry out the
Lyapunov--Schmidt reduction with exact radical coefficients, show that its
first reduced terms are cubic, and classify all nearby branches: four kites
for \(\nu>\nu_*\), four isosceles trapezoids for \(\nu<\nu_*\), and no nearby
nonsymmetric branches.  In particular, the square is locally isolated at the
fixed critical mass.  The present square computation is therefore a valuable
negative control for the pipeline, **not a new mathematical result**.

Primary source: K. R. Meyer and D. S. Schmidt,
[“Bifurcations of relative equilibria in the 4- and 5-body problem”](https://doi.org/10.1017/S0143385700009433),
*Ergodic Theory and Dynamical Systems* 8 (1988), 215--225.  A modern
representation-theoretic treatment is T. Zhou and Z. Xia,
[“On the Degeneracy of the Central Configuration Formed by a Regular n-Gon with a Central Mass”](https://arxiv.org/abs/2604.04610)
(2026).

The two "Q-zero" flags the continuation raised near this point (with
\(|Q|\sim5\times10^{-4}\) and \(\sigma_2\sim5\times10^{-7}\)) are artifacts
of the left kernel vector rotating through the near-degenerate doublet; the
kernel-circle sweep supersedes them.

### 3. Small-mass quadratic-zero point — rejected at order 3

\[
(\mu,\nu)=(0.13858214243364,\ 0.07182100451968),\qquad
\lambda=0.121208232280.
\]

Corank one (\(\sigma_2=0.0202\)), order-2 obstruction \(\sim5\times10^{-13}\),
order-3 obstruction \(0.11116\).  The sampled fixed-mass direction is **not a
continuum source**.  As above, “ordinary cusp” is not asserted without the
missing unfolding checks.  The returning numerical route revisits the point
with coordinates agreeing to about 12 digits.

## Decision-register updates

| Point | Decision | Evidence | Revisit condition |
|---|---|---|---|
| Quadratic-zero point at (7.21594, 0.51826) | Rejected as a fixed-mass tangent (numerical), order-3 obstruction 36.8 | `census_summary.json` candidate 1 + fixed-mass jet | Check unfolding rank only if a cusp classification is needed |
| Square+center, μ=1, ν=(13+11√2)/12 | Classical negative control; exact local isolation and cubic normal form already published | `census_corank2_out.json`; Meyer--Schmidt (1988) | Revisit only to validate or improve the pipeline, not for a novelty claim |
| Quadratic-zero point at (0.13858, 0.07182) | Rejected as a fixed-mass tangent (numerical), order-3 obstruction 0.111 | `census_summary.json` candidates 2/3 | Same as first point |
| Large-μ forward end | Open at μ=22.4; no asymptotic limit established | Step budget reached and small-mode accuracy is degrading | Continue with a robust SVD and an adapted/rescaled chart |
| Near (μ,ν)=(0,0) | Unresolved boundary/branch-switch region | Corrections become ill-conditioned and σ₂ becomes small | Use a restricted-problem blow-up chart before classifying it |
| Other routes and discriminant components | Untouched | One augmented path cannot enumerate branches through corank two, and sign-change detection is incomplete | Branch-switch locally, then use a global singular solve or interval subdivision |

## What this run does and does not clear

- **Supported at discovery level:** one numerically followed route in the
  augmented singular system contains three detected exceptional events.  The
  two corank-one fixed-mass directions are obstructed at cubic order, and the
  square event reproduces a classical exact negative control.  No
  counterexample germ was observed on the sampled route.
- **Not cleared:** tangential/even-multiplicity zeros of \(Q\); sub-step event
  pairs; other branches through the corank-two square or the small-mass
  boundary; other discriminant components; the large-\(\mu\) end; other
  configurations in any fixed-mass fiber; and everything at the level of a
  global exact proof.

## Reproduction

```powershell
node .\census.js            # full two-direction continuation (CENSUS_MAX_STEPS, default 4000)
node .\census_corank2.js    # kernel-circle sweep at the square point
```

Outputs: `census_summary.json` (candidates + branch summaries),
`census_trace.json` (full monitor trace), `census_corank2_out.json`
(360-direction sweep).  The seed control values printed on stderr must match
`RESULT.md` as quoted above.
