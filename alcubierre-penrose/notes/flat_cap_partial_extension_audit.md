# Flat-cap partial extension audit

Working note, 2026-08-06.

## Verdict

A compact stationary scalar-shift bubble can admit a proper smooth Hausdorff
extension through the interior of an exact planar front or rear cap.  The
extension is the ordinary two-dimensional Kruskal completion, fibered over a
transverse open disk.  Compactness does not contaminate this interior gluing.

The cap rim fails for a different reason.  The product chart is not continuous
on a neighborhood containing the infinitely flat transition from the planar
cap to the curved wall.  More invariantly, a hypothetical regular endpoint of
the rim generator would make a transverse family of spacelike geodesics and
parallel frames converge, but a curvature component in those frames grows as
the square of the endpoint boost.  Thus the construction perforates the
finite-affine boundary through an open disk but cannot include its rim.  The
rim generator itself has no pp blow-up; the obstruction is the nonuniform
curvature arbitrarily close to it.

## 1. An explicit compact wall with exact planar caps

Put \(\rho^2=y^2+z^2\), choose \(0<a<b\), and let \(L>0\).  Define

\[
 h(u)=\begin{cases}0,&u\leq0,\\ e^{-1/u},&u>0,\end{cases}
 \qquad
 \eta(u)=\int_0^u h(s)\,ds,
\]

and

\[
 \psi(s)=L^2\frac{\eta(s-a^2)}{\eta(b^2-a^2)}.
\]

Then \(\psi=0\) on \(s\leq a^2\), \(\psi\) is smooth and strictly
increasing for \(s>a^2\), \(\psi(b^2)=L^2\), and \(\psi(s)>L^2\) for
\(s>b^2\).  The level set

\[
 \Sigma=\{\Phi=0\},
 \qquad
 \Phi(x,y,z)=x^2+\psi(\rho^2)-L^2,
\]

is a smooth compact connected surface.  It has the two exact planar caps

\[
 x=\pm L,\qquad \rho<a,
\]

and closes at \(x=0,\rho=b\).  Regularity is immediate: where \(x\ne0\),
\(\Phi_x=2x\ne0\); where \(x=0\) on \(\Sigma\), one has \(\rho=b\) and
\(\psi'(b^2)>0\).

Choose a smooth nonincreasing function \(W\) with

\[
 W(0)=-1,\qquad W'(0)<0,
\]

which is zero sufficiently far inside and equals \(-v_s<-1\) sufficiently
far outside.  We may, and below do, take
\(W(\phi)=-1-c\phi\), \(c>0\), in a neighborhood of \(\phi=0\).  The shift

\[
 v(x,y,z)=W(\Phi(x,y,z))
\]

is smooth, bounded, and exactly constant outside a compact set.  Its
\(v=-1\) wall is \(\Sigma\).  On the open cylinder \(\rho<a\),

\[
 v=W(x^2-L^2),
\]

so the metric is exactly a product in the transverse directions, not merely
flat to finite order at the axial point.

## 2. Exact local extension at the front cap

Write \(x=L+s\) and

\[
 \bar v(s)=W(2Ls+s^2),
 \qquad
 \bar v(0)=-1,
 \qquad
 \bar v'(0)=-\kappa<0.
\]

There is a smooth function \(d\) such that

\[
 \bar v(s)=-1-\kappa s+s^2d(s).
\]

On \(\rho<a\), introduce

\[
 U=e^{-\kappa t},\qquad s=UV.
\]

The original spacetime occupies \(U>0\).  Direct substitution in

\[
 ds^2=-dt^2+[ds-\bar v(s)dt]^2+dy^2+dz^2
\]

gives

\[
\begin{aligned}
 ds^2={}&U^2dV^2+
 \left[-\frac{2}{\kappa}
 +\frac{2U^2V^2}{\kappa}d(UV)\right]dU\,dV\\
 &+\left[-\frac{2V^2}{\kappa^2}d(UV)
 +\frac{U^2V^4}{\kappa^2}d(UV)^2\right]dU^2
 +dy^2+dz^2.
\end{aligned}
\]

Every coefficient is smooth at \(U=0\), and the determinant of the
\((U,V)\) block is exactly \(-\kappa^{-2}\).  The metric therefore extends
smoothly and nondegenerately to \(U<0\).

The stationary field becomes

\[
 \partial_t=\kappa\left(V\partial_V-U\partial_U\right).
\]

Its norm is

\[
 \chi^2=\bar v(UV)^2-1=2\kappa UV+O((UV)^2).
\]

Thus the original half \(U>0\) contains one interior-type quadrant
(\(V<0\), \(\chi\) timelike) and one exterior-type quadrant
(\(V>0\), \(\chi\) spacelike); \(U<0\) supplies their two opposite Kruskal
partners.

The original cap generators are \(V=0,U>0\); they continue through
\(U=V=0\) to \(V=0,U<0\).  The surfaces \(U=0\) and \(V=0\) are the two
branches of a bifurcate Killing horizon, and \(U=V=0\) is a bifurcation
two-disk.  The rear cap has the time-reversed construction.

## 3. Hausdorff gluing and the extension obtained

Fix a transverse disk \(D=\{\rho<a_0\}\) with \(a_0<a\), and let

\[
 P=(-\epsilon,\epsilon)_U\times(-\delta,\delta)_V\times D.
\]

On \(P_+=P\cap\{U>0\}\), the map

\[
 (U,V,y,z)\longmapsto
 \left(-\kappa^{-1}\log U,\ L+UV,\ y,\ z\right)
\]

is an isometry onto an open subset of the original spacetime.  Glue \(P\) to
the entire original manifold along this open set.

The quotient is Hausdorff.  Equivalently, the graph of the gluing map is
closed in \(P\times M\).  If a sequence in that graph converges to a point
with \(U>0\), continuity gives another point of the graph.  If its \(P\)-limit
has \(U=0\), the corresponding sequence in \(M\) has \(t\to+\infty\) and
hence cannot converge there.  A limit with \(U<0\) is impossible.  Thus there
is no doubled-limit pair of the kind that produces a line with two origins.
The transverse boundary \(\rho=a_0\) is not part of \(P\).

The glued manifold is consequently a proper smooth Hausdorff Lorentzian
extension of the whole original spacetime, even though it resolves only an
open family of cap generators.  One may take \(D=\{\rho<a\}\) directly: the
rim is absent from this open disk, so the same closed-graph argument applies.

There is also a global description.  The entire cylinder \(\rho<a\) is the
product of the reduced eternal metric with \(D\).  If \(\widetilde M_2\) is
the usual Kruskal continuation of that reduced metric, glue
\(\widetilde M_2\times D\) to \(M\) along their common product submanifold.
This fibers the extra regions of the reduced conformal diagram over the open
cap disk.  At the marked finite-affine corner it contains all four local
Kruskal quadrants and a bifurcation disk.  It is a genuine four-dimensional
continuation, but only through a finite transverse aperture; it is not a new
complete asymptotic end of the whole bubble.

## 4. The first warning at the rim: the product chart fails

At \(\rho=a\), the wall begins its \(C^\infty\)-flat transition away from the
plane.  Write it locally as \(x=F(Y)+s\).  The same regularization gives

\[
 g_{UY}=-\frac{F_Y}{\kappa U}+O(U).
\]

Although every derivative of \(F\) vanishes at the rim point, every
transverse neighborhood contains points \(Y_n\) with \(F_Y(Y_n)\ne0\).
Along \(U_n=|F_Y(Y_n)|^2\), the displayed component is unbounded.  Therefore
the product/Kruskal chart cannot include the rim in a continuous metric
neighborhood.

This does not invalidate the interior extension: the rim is outside every
chart used in the gluing above.  By itself, however, this component blow-up
only rules out this chart.  The following argument rules out a regular
\(C^2\) resolution of the rim generator for the explicit wall constructed
above.

## 5. Invariant rim obstruction from a transverse geodesic family

Use the rim point \((x,y,z)=(L,a,0)\).  Its stationary orbit \(\gamma\) is a
finite-affine null geodesic.  Along it all transverse derivatives vanish, so
its own pp curvature is the same as on the product cap.  Let

\[
 e_0=\partial_t+v\partial_x,\qquad
 e_1=\partial_x,\qquad e_2=\partial_y .
\]

This is an orthonormal frame, and at the rim
\(\chi=\partial_t=e_0+e_1\).  An affine tangent is
\(K=q(e_0+e_1)\), where \(q\to\infty\) at the finite-affine end.
The vector \(e_2\) is parallel along \(\gamma\).

The frame-limit assertion is automatic if the generator has an endpoint in a
\(C^2\) extension.  In a relatively compact extension chart choose a temporal
coordinate \(T\) and put \(f=dT(K)>0\).  Compactness of the causal vectors
normalized by \(dT=1\) gives \(|f'|\leq Cf^2\), while convergence to the
endpoint gives \(\int f\,d\lambda<\infty\).  If \(f\) were unbounded, then
\(|(1/f)'|\leq C\) would force
\(f\geq[C(\lambda_* -\lambda)]^{-1}\), a contradiction.  Thus \(K\) is
bounded, and the geodesic and parallel-transport equations give finite limits
for \(K\) and \(e_2\); the limit of \(K\) is nonzero by uniqueness.

Assume that a \(C^2\) extension resolves this endpoint.  From every
point of \(\gamma\), shoot the unit spacelike geodesic with initial tangent
\(e_2\).  For a scalar \(x\)-shift,

\[
 \Gamma^\mu{}_{yy}=0,
\]

so these geodesics are exactly

\[
 \sigma_t(r)=(t,L,a+r,0).
\]

Continuous dependence of geodesics and parallel transport in a \(C^2\)
metric says that, for every sufficiently small fixed \(r\), the points
\(\sigma_t(r)\) and the frames obtained by transporting \(K,e_2\) along
\(\sigma_t\) must converge as the rim endpoint is approached.  Consequently
all Riemann contractions in those frames must remain bounded.

They do not.  Along a \(y\)-line,

\[
 \nabla_{e_2}e_0=\frac{v_y}{2}e_1,
 \qquad
 \nabla_{e_2}e_1=\frac{v_y}{2}e_0.
\]

Thus the parallel transport of \(K\) from the rim to \(a+r\) is

\[
 \widehat K(r)
 =q\exp\!\left[-\frac{v(L,a+r,0)+1}{2}\right](e_0+e_1),
\]

while \(e_2\) remains parallel.  Direct curvature evaluation gives

\[
 R(e_0+e_1,e_2,e_0+e_1,e_2)=v_{yy}-v_y^2.
\]

At \(x=L,z=0,y>a\), put
\(\phi(y)=\psi(y^2)\).  In the affine part of \(W\),

\[
 v=-1-c\phi,\qquad
 v_{yy}-v_y^2=-c\phi_{yy}-c^2\phi_y^2<0,
\]

because
\(\phi_{yy}=2\psi'(y^2)+4y^2\psi''(y^2)>0\).  Hence, for every sufficiently
small fixed \(r>0\),

\[
 R(\widehat K,e_2,\widehat K,e_2)
 =q^2 e^{-[v(L,a+r,0)+1]}(v_{yy}-v_y^2)
 \longrightarrow-\infty.
\]

The sign computation is convenient but not essential.  If
\(v_{yy}-v_y^2\) vanished on a one-sided interval beyond an exact cap rim,
then \((e^{-v})_{yy}=0\) there.  Flat matching gives (v_y=0) at the rim, so
\(e^{-v}\), and hence (v\), would be constant on that interval.  Therefore
any genuine transition away from the planar cap has points with
\(v_{yy}-v_y^2\ne0\) arbitrarily close to the rim.  One such fixed point
inside the assumed normal neighborhood is enough for the (q^2)
contradiction.

This contradicts curvature continuity in the assumed extension.  The logic
is worth distinguishing from the ordinary pp singularity: the contraction is
finite on the rim generator itself.  It is the uniform neighborhood demanded
by a regular endpoint that imports the curved side and exposes the divergent
transverse family.

## 6. Interpretation

The construction answers two different questions differently.

1. **Does a spatially compact eternal stationary bubble admit any proper
   continuation beyond the reduced finite-affine endpoint?** Yes.  Exact
   product structure on an open cap disk gives a genuine Hausdorff
   Kruskal-product extension.
2. **Does the entire compact bubble acquire the full larger reduced diagram as
   a regular four-dimensional continuation?** No.  The extension is a finite
   transverse aperture, and the infinitely flat cap rim is a genuine
   \(C^2\) obstruction for this construction even though the rim generator's
   own pp curvature remains finite.

The natural far side is not a new copy of ordinary null infinity.  Locally it
is the other Kruskal quadrants across a bifurcate Killing horizon, fibered over
the cap disk.  Beyond the horizon the original spacetime supplies no data, so
nonstationary additions flat at \(U=0\) make the far-side continuation
nonunique unless preservation of the stationary product symmetry is imposed.
The resulting spacetime is therefore extendible but not by a continuation
that erases the entire finite-affine boundary: the open cap becomes a
bifurcate-horizon aperture whose circular rim remains singular.
