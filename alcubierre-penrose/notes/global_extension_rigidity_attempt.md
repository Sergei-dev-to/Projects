# Global extension rigidity: proof attempt and exact obstruction

> **Status, 2026-08-07.**  This is a historical working note.  Its verdict
> "neither proved nor refuted" concerns the stronger, subsequently withdrawn
> claim that no single extension can resolve all finite-affine stationary
> generators of a compact bubble.  It does **not** concern the scalar-shift
> extension alternative proved in `paper/main.tex`.  For nonpositive stationary
> scalar shifts with a compact regular wall, that theorem closes the old
> transverse-coordinate blocker by using an extension-bounded observer frame
> and a uniform transverse geodesic disk.  The unresolved discussion below is
> retained for more general vector shifts and attachment problems lacking that
> exact transverse-geodesic structure.
>
> **Addendum, 2026-08-06.**  The explicit scalar-shift flat-cap rim considered
> here has now been settled by a simpler transverse-geodesic argument; see
> `flat_cap_partial_extension_audit.md`.  A regular rim endpoint would give a
> uniform normal neighborhood for the unit spacelike geodesics transverse to
> the rim generator.  In a scalar (x)-shift these are exact coordinate
> (y)-lines, and parallel transport along them exposes a curvature component
> (q^2 e^{-(v+1)}(v_{yy}-v_y^2)), nonzero immediately on the curved side.
> This contradicts (C^2) curvature continuity.  Thus the open planar cap
> really does admit a Kruskal-product extension, but its rim does not admit a
> regular (C^2) geodesic resolution in that explicit construction.  The
> broader noncollapse problem below remains relevant to geometries without
> this exact transverse geodesic family and to merely topological attachments
> that do not resolve the affine tangent.

Working note, 2026-08-03. This attacks the strongest proposed sequel result:

> No single Hausdorff \(C^2\) extension of a compact superluminal stationary
> bubble resolves all finite-affine stationary generators of its Killing-norm
> zero set.

> **Correction after the exact theorem audit.** Sections 7--9 below correctly
> compute the endpoint boost one-jets, but they overread anchored-extension
> uniqueness: Sbierski supplies a diffeomorphism agreeing with the
> identification up to the boundary, and it is an isometry on the original
> one-sided region, not on the freely chosen far side of the extension. Thus
> it does **not** supply a two-sided local-isometry germ of the extended metric.
> The common-domain integration lemma for genuine germs is proved in Section
> 10, but its premise is unavailable here. The claimed smooth
> flow-rigidity/no-simultaneous-resolution theorem is therefore withdrawn; the
> genuine remaining issue is again a one-sided boundary-rigidity or holonomy
> lemma.

The discussion below is for the scalar-shift class
\[
g=-dt^2+[dx-v(x,y,z)dt]^2+dy^2+dz^2,
\]
with bounded smooth shift, compact regular component \(\Sigma=\{v=-1\}\), and
simple roots at the relevant generators. Extension to general vector shifts
(including Natário) is a separate step.

## 1. What compactness proves

Let \(p\) be a support point of the compact spatial surface \(\Sigma\) in the
\(x\)-direction. In a graph representation \(x=F(y,z)\), one has
\(F_A(p)=0\), equivalently \(v_A(p)=0\). Hence the stationary Killing orbit
through \(p\) is a null pregeodesic. If \(\kappa=-v_x(p)\ne0\), one affine
orientation reaches finite affine parameter.

The Hessian \(F_{AB}(p)\) is semidefinite. If it is nonzero, then
\(H_{AB}=v_{AB}=\kappa F_{AB}\ne0\), and the established parallel-propagated
formula
\[
R_{KAKB}=q^2H_{AB},\qquad
q=[\kappa(\lambda_*-\lambda)]^{-1}
\]
rules out a \(C^2\) endpoint for that generator.

Thus only a transversely degenerate support point can evade the established PP
test. Pointwise degeneracy is not a product condition: \(F=-y^4-z^4\) is the
basic counterexample to that inference.

## 2. The strongest adversary

The decisive geometry has exact open planar front and rear caps joined by
\(C^\infty\)-flat transitions to a compact wall. On the interior of a cap,
\(v=v(x)\) and the standard two-dimensional Kruskal extension lifts as a
transverse product. These generators are locally extendible.

At an edge point of the cap, smoothness forces every transverse derivative of
the cap graph to vanish. In particular the edge Killing orbit is still a
finite-affine stationary generator. But every transverse neighborhood of it
contains nonproduct points. Therefore a global theorem reduces to the edge
generator.

Near a simple root, put
\[
U=e^{-\kappa t},\qquad x-F(y,z)=UV.
\]
The natural product regularization has
\[
g_{UA}=-\frac{F_A}{\kappa U}+O(U).
\]
For any sequence of nonproduct points \(y_n\to y_0\), choosing
\(U_n=|F_A(y_n)|^2\) makes this coefficient unbounded. This proves that the
natural product chart cannot extend continuously across a neighborhood of the
cap edge. It does **not**, by itself, prove invariant inextendibility: an
extension is allowed to use a different manifold and boundary chart.

## 3. What extension theory supplies

For a globally hyperbolic spacetime, a boundary endpoint in any locally
Lipschitz extension has a future-boundary chart in which the original spacetime
occupies the full region below a locally Lipschitz graph. Thus an extension of
the edge generator cannot use a merely cusp-shaped neighborhood containing only
paths with \(|F_A|\ll U\).

Moreover, locally Lipschitz extensions anchored by the same inextendible causal
curve are locally unique up to the boundary. The relevant reference is Jan
Sbierski, *Uniqueness and non-uniqueness results for spacetime extensions*,
arXiv:2208.07752, especially the future-boundary chart theorem and Theorem 5.23.

These results remove the easiest topological escape, but they do not identify
the original transverse coordinate \(y\) with a nondegenerate boundary-chart
coordinate. Consequently the divergence of \(F_A/U\) is not yet an invariant
contradiction.

## 4. Missing invariant lemma

The ceiling-one theorem follows from either of the following statements.

**Boundary-coordinate lemma.** In a \(C^2\) future-boundary chart anchored by
the edge generator, bounded-norm transverse directions in the original flat
spatial slices remain nondegenerate transverse directions at the boundary.
Then the full subgraph property forces paths with \(|F_A|/U\to\infty\) into
the chart, contradicting continuity of the metric.

**Holonomy lemma.** There are loops shrinking to the edge endpoint whose
Levi-Civita holonomy is unbounded. A locally Lipschitz extension has locally
bounded connection coefficients and cannot admit such local holonomy. The
candidate loops are rectangles in the affine-null/transverse plane with
\(U\)-width comparable to \(U_n\), transverse endpoint \(y_n\to y_0\), and
\(U_n\) chosen below the scale of the first nonzero transverse wall datum.
Sbierski's holonomy criterion (arXiv:2007.12049) is the appropriate invariant
framework.

For the exact local model \(v(x,y)=V(x-F(y))\), put \(p=F_y\), take the wall
\(x=F(y)\), and use the unit screen vector \(Y=\partial_y\) in the original
flat spatial coordinates. Direct computation gives on \(V=-1\)
\[
R(\partial_t,Y,\partial_t,Y)
 =v_{yy}-v_y^2
 =\kappa F_{yy}+(V''-\kappa^2)F_y^2.
\]
Thus the algebraically boosted screen curvature is
\[
R(q\partial_t,Y,q\partial_t,Y)
 =q^2\left[\kappa F_{yy}+(V''-\kappa^2)F_y^2\right].
\]
For every nonconstant \(C^\infty\)-flat transition, the bracket is nonzero on
sequences approaching the cap edge, and \(q\) can dominate its arbitrarily fast
decay. This supplies the curvature density needed for a holonomy blow-up.

What remains is not the blow-up scaling but the shrinking-loop topology. A
hypothetical extension could map its regular boundary coordinates to a
transversely narrowing cusp in the original \((U,y)\) variables. The standard
future-boundary chart is full in its own coordinates, but no cited theorem yet
forces original bounded-length transverse segments to remain nondegenerate in
that chart. Proving that fact (for example from nondegeneracy of the extended
metric or from an anchored-extension uniqueness argument) is necessary before
the displayed boosted curvature can be integrated into an invariant local
holonomy contradiction.

The exact holonomy estimate has not been derived. In particular, divergent
components in the natural \((U,V,y,z)\) chart cannot be substituted for that
estimate, because unbounded components in a singular frame are not invariant.

## 5. Historical verdict on the stronger withdrawn claim

At this stage of the investigation, the stronger no-simultaneous-resolution
theorem was neither proved nor refuted. It had been reduced to a precise local
problem at the edge of an infinitely flat planar cap. The then-existing PP
curvature theorem proved the result for every compact bubble having a support
generator with nonzero transverse Hessian; in particular it covered strictly
convex support points. Higher-order nonflat contact was not covered by that
pointwise Hessian test. The reassessment below replaced the proposed
boundary-coordinate route.

That assessment is retained only to document the abandoned route.  The current
scalar-shift result and its hypotheses are stated and proved in
`paper/main.tex`; this note is not a status report for that theorem.

## 6. Blocked audit after the extension-theory check

The obstruction has survived three independent formulations.

1. **Natural endpoint coordinates.** They give \(g_{UA}\sim-F_A/(\kappa U)\),
   but an arbitrary extension need not use these coordinates.
2. **Future-boundary charts.** The boundary of a globally hyperbolic spacetime
   is locally a full Lipschitz graph in the extension chart, but the theorem
   gives no noncollapse estimate relating its spatial coordinates to the
   original transverse coordinate \(y\).
3. **Local holonomy.** Sbierski's bounded-holonomy lemma applies to curves with
   uniformly bounded coordinate velocity and parameter interval *in the
   extension chart*. The boosted curvature above suggests unbounded holonomy,
   but establishing that the required loops remain local with uniformly bounded
   extension-chart velocity is precisely the missing noncollapse estimate.

Accordingly, no cited theorem turns the computed \(F_A/U\) or \(q^2\)-curvature
growth into an invariant contradiction for an infinitely flat cap edge. A proof
now requires a new boundary noncollapse/holonomy lemma, while a disproof requires
an explicit nondegenerate \(C^2\) cusp extension. Neither follows from the
current calculations. This is a genuine mathematical impasse rather than an
unfinished algebraic step.

## 7. Superseded attempt: stationary flow

The audit above overlooked the strongest use of anchored-extension uniqueness.
It should be applied to the stationary isometry flow, not merely to two choices
of endpoint coordinates.

Here "resolve" means geodesic resolution: \(\iota\circ\gamma\) continues
through its finite affine endpoint as a \(C^1\) affinely parametrized null
geodesic with nonzero tangent. This is stronger than attaching a mere
topological endpoint and is the notion relevant to extending a geodesic. In a
\(C^2\) metric it also implies that every parallel frame along \(\gamma\) has a
finite nondegenerate endpoint limit, by the ordinary parallel-transport ODE.

Let \(\phi_s\) be the flow of \(\xi=\partial_t\), and suppose
\(\iota:M\hookrightarrow\widetilde M\) regularly resolves the finite-affine
stationary generator \(\gamma\) at \(p\). For fixed \(s\), the maps
\[
\iota,
\qquad
\iota\circ\phi_s
\]
are two extensions of the same globally hyperbolic spacetime. They are anchored
by \(\gamma\): time translation only rescales \(\lambda_*-\lambda\), so both
images of \(\gamma\) converge to the same point \(p\). Anchored-extension
uniqueness therefore extends \(\phi_s\) to a local isometry \(\Phi_s\) fixing
\(p\).

Along \(\gamma\),
\[
\xi=\kappa(\lambda_*-\lambda)K,
\qquad
\nabla_K\xi=-\kappa K.
\]
The scalar-shift connection also makes the coordinate screen vectors
\(\partial_y,\partial_z\) parallel on this orbit. In the limiting parallel
null frame \((K,N,Y,Z)\), the boundary one-jet is therefore
\[
L_s=(d\Phi_s)_p:\qquad
K\mapsto e^{-\kappa s}K,\quad
N\mapsto e^{\kappa s}N,\quad
Y\mapsto Y,\quad Z\mapsto Z.
\]
Thus the one-jets form a smooth pure-boost group. At smooth regularity, the
finite-type local-isometry pseudogroup theorem integrates this subgroup of
germs on a common neighborhood. Preservation of affinely parametrized
geodesics then gives
\[
\Phi_s=\exp_p\circ L_s\circ\exp_p^{-1}.
\]
This formula supplies both the local group law and smooth dependence on \(s\),
so the local action has a Killing generator \(\widetilde\xi\) extending \(\xi\)
and fixing \(p\). The absence of a screen rotation is essential: a boost
combined with a rotation can have a non-horizon null set.

Choose local coordinates \((u,w,y,z)\) adapted to the fixed two-surface and the
boost action. The extended flow acts as
\[
(u,w,y,z)\longmapsto
(e^{\kappa s}u,e^{-\kappa s}w,y,z).
\]
Invariance and regularity force
\[
g_{uu}=w^2a(uw,y,z),\qquad
g_{ww}=u^2b(uw,y,z),\qquad
g_{uw}=c(uw,y,z),
\]
with \(c(0,y,z)\ne0\). Therefore
\[
\widetilde g(\widetilde\xi,\widetilde\xi)
=\kappa^2uw\{uw[a+b]-2c\}.
\]
After restricting the neighborhood, the braced factor never vanishes. The
Killing-norm-zero set is exactly
\[
\{u=0\}\cup\{w=0\},
\]
the two branches of a bifurcate Killing horizon. In particular every original
point of \(\{\xi^2=0\}\) lying in this neighborhood belongs to an open Killing
horizon and is a stationary geodesic point.

This proves the missing local statement without controlling the old transverse
coordinate:

> **Local flow-rigidity lemma.** For a globally hyperbolic stationary spacetime
> with pure-boost linearization at a nondegenerate finite-affine stationary
> generator, a regular geodesic resolution in a smooth extension forces the
> Killing-norm-zero set to be a Killing horizon on an original-spacetime
> neighborhood of every sufficiently late point of that generator. At exactly
> \(C^2\), the same statement is conditional on common-domain integration of
> the smooth pure-boost subgroup of local-isometry germs.

The reason a transversely narrowing cusp cannot evade the conclusion is simple
in this formulation. A local extension neighborhood contains an ordinary open
neighborhood of a late point of \(\gamma\) inside \(M\). If nongeodesic points
of \(\Sigma\) occur arbitrarily close to the generator's spatial position, some
of them lie in that open set, contradicting the boost normal form.

## 8. Superseded claimed global consequence

Let \(\mathcal G\subset\Sigma\) be the stationary geodesic locus. It is closed.
The local flow-rigidity lemma says that every member of \(\mathcal G\) regularly
resolved by one \(C^2\) extension must be an interior point of \(\mathcal G\).

For a connected compact scalar-shift bubble:

1. \(\mathcal G\ne\varnothing\), because front and rear support points satisfy
   \(v_A=0\).
2. \(\mathcal G\ne\Sigma\), because a compact closed surface cannot have its
   normal everywhere parallel to the fixed longitudinal direction.
3. Hence \(\partial_\Sigma\mathcal G\ne\varnothing\).
4. Every point of \(\partial_\Sigma\mathcal G\) still belongs to \(\mathcal G\)
   because \(\mathcal G\) is closed, but it is not an interior point.
5. A single smooth extension regularly resolving all finite-affine stationary
   generators would resolve such a boundary point, contradicting local flow
   rigidity.

Thus, subject to the simple-root condition \(\kappa\ne0\), the ceiling-one
statement follows for the scalar-shift class. Exact planar caps do not evade it:
their edge lies in \(\partial_\Sigma\mathcal G\).

The more conceptual formulation does not use compactness once existence and
properness of the geodesic locus are known:

> **Clopen-geodesic-locus theorem.** Let \(\Sigma\) be a connected
> regular component of \(\{\xi^2=0\}\), and let \(\mathcal G\subset\Sigma\) be
> its stationary geodesic locus. Assume the endpoint linearization is a pure
> boost at every point of \(\mathcal G\). If one Hausdorff smooth extension
> regularly resolves every corresponding finite-affine generator, then
> \(\mathcal G\) is both open and closed. Hence \(\mathcal G=\varnothing\) or
> \(\mathcal G=\Sigma\); in the latter case \(\Sigma\) is locally a Killing
> horizon everywhere.

The scalar-shift compactness facts are then only a device for proving
\(\varnothing\ne\mathcal G\ne\Sigma\). This formulation also explains all
controls: PG-Schwarzschild and Ori lie on the \(\mathcal G=\Sigma\) branch,
whereas Alcubierre and the computed Natário example have a proper geodesic
locus.

The pure-boost hypothesis cannot simply be dropped. In flat spacetime a Killing
field combining a Lorentz boost with a nonzero rotation in the screen has a
regular fixed point while its norm-zero set is not just the two boost horizons.
It is therefore a model showing that a boost-plus-rotation endpoint can evade
the clopen conclusion. For general vector-shift warp metrics, the screen
rotation must be computed; compactness alone is not enough, and compact genuine
Killing horizons provide regular control examples.

## 9. Superseded scope audit

The previous boundary-coordinate/holonomy impasse is withdrawn for smooth
regular geodesic resolution. The endpoint parallel frame fixes the boundary
one-jets, and the local-isometry pseudogroup theorem supplies a common local
action.

At exactly \(C^2\), the residual issue is narrower but real: Sbierski's theorem
gives an isometry germ for every fixed \(s\), while the boost normal form needs
those germs represented on a common neighborhood for all small \(s\). The
needed low-regularity lemma is: a \(C^2\) Lorentz metric's smooth one-parameter
subgroup of fixed-point local-isometry one-jets integrates to a common local
\(C^1\) action. A precise citation or proof of this statement is still required.

This does not prove the same statement for an extension that merely attaches a
topological endpoint while the affine tangent has no nonzero limit. Such an
attachment does not extend the null geodesic and is outside the stated meaning
of "resolves." The argument proves the advertised ceiling only for classes in which
\(\varnothing\ne\mathcal G\ne\Sigma\) and the endpoint linearization is a pure
boost. It does not prove that *compactness by itself* excludes extension:
compact Killing horizons are counterexamples to that broader wording. General
vector-shift Natário geometries require both the geodesic-locus and screen-
rotation checks.

## 10. Exact correction: the integration lemma is true, but inapplicable

There are two logically different statements which the preceding attempt
conflated.

### 10.1 Genuine isometry germs do integrate

Let \(\widetilde g\) be a \(C^2\) pseudo-Riemannian metric near \(p\). Suppose
that, for every \(s\) in an interval about zero, there is a **genuine
local-isometry germ** \(F_s\) of \(\widetilde g\) fixing \(p\), and that
\[
(dF_s)_p=L_s
\]
is a smooth one-parameter subgroup. Then the germs have representatives on
one common neighborhood for all sufficiently small \(s\).

The proof is elementary. A \(C^2\) metric has a \(C^1\) exponential map which
is a local \(C^1\) diffeomorphism. An isometry is determined by its value and
derivative at one point, because it maps affinely parametrized geodesics to
geodesics. Hence every germ is represented, wherever it is an isometry, by
\[
\mathcal F_s=\exp_p\circ L_s\circ\exp_p^{-1}.
\tag{10.1}
\]
After fixing a parameter interval, all \(\mathcal F_s\) are defined on a
common small normal ball. Let \(A_n\) be the set of parameters for which
\(\mathcal F_s^*\widetilde g=\widetilde g\) on the ball of radius \(1/n\).
Continuous dependence of the \(C^1\) exponential map on \(s\) makes \(A_n\)
closed, and the germ hypothesis gives
\[
\bigcup_n A_n=[-\epsilon,\epsilon].
\]
Baire category gives an \(A_n\) containing an interval \(I\). If \(s,t\in I\),
then on a uniformly smaller ball
\[
\mathcal F_{s-t}=\mathcal F_t^{-1}\circ\mathcal F_s
\]
is an isometry. Since \(I-I\) contains an interval about zero, all small
parameters act isometrically on one common ball. This proves the exact
low-regularity lemma that Sections 7--9 had left conditional.

For a pure boost \(L_s\), exponential coordinates make this common action
linear. Continuity of \(\exp_p^*\widetilde g\) already suffices to classify
the local Killing-norm zero set. The axes \(U=0\) and \(V=0\) have zero norm
by boost invariance and continuity at the fixed surface. For \(UV\ne0\),
move along the boost orbit to \(|U|=|V|=\sqrt{|UV|}\). There
\[
\widetilde g(\widetilde\xi,\widetilde\xi)
=-2\kappa^2 UV\,g_{UV}(0,0,y,z)+o(UV),
\]
whose leading coefficient is nonzero by nondegeneracy. Thus the zero set is
exactly the two boost horizons. No \(C^\infty\) finite-type theorem is needed.

### 10.2 Anchored uniqueness does not furnish those germs

For the two embeddings \(\iota\) and \(\iota\circ\phi_s\), Sbierski's theorem
extends the identification to a diffeomorphism on a full coordinate
neighborhood. Its isometry statement, however, is only on the original
subgraph and its boundary. The metric on the other side is unconstrained.
This limitation is necessary: start with a Rindler wedge in Minkowski space
and add to the metric beyond one horizon a non-boost-invariant tensor
multiplied by a smooth function flat at the horizon. The result is a smooth
extension which agrees exactly with Minkowski space on the wedge, but the
wedge boost has no two-sided local-isometry extension.

Therefore the Baire lemma cannot be invoked from anchored uniqueness alone,
at \(C^2\) **or at smooth regularity**. What remains true from the stationary
calculation is only:

1. every fixed time translation has a boundary diffeomorphism extension;
2. its endpoint one-jet is the pure boost displayed in Section 7;
3. these maps are isometries on the original one-sided region.

Turning those one-sided facts into transverse noncollapse at an infinitely
flat cap rim is precisely the boundary-coordinate/holonomy problem isolated
in Sections 4--6. No-simultaneous resolution remains plausible, but is not a
proved theorem.
