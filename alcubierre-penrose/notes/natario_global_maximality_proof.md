# Global C2 maximality for the Natario zero-expansion bubble

Audited proof, 2026-08-03.

## 1. Result

Consider
\[
g=-dt^2+\delta_{ij}(dx^i-X^i dt)(dx^j-X^j dt)
\]
with Natario's smooth stationary axisymmetric shift.  In cylindrical
coordinates \((x,\varrho,\phi)\), put
\[
a(r)=2v_s f(r),\qquad b(r)=v_s r f'(r)=\frac r2a'(r),
\qquad r^2=x^2+\varrho^2.
\]
Then
\[
X^x=-a-b\frac{\varrho^2}{r^2},\qquad
X^\varrho=b\frac{x\varrho}{r^2},\qquad X^\phi=0.
\tag{1.1}
\]

Assume:

1. \(X\) is smooth and bounded on \(\mathbb R^3\), with \(f\geq0\) and
   \(f'\geq0\), and
   \[
   X\longrightarrow-v_s e_x,\qquad
   |X+v_s e_x|+|DX|\leq Ce^{-\sigma r}
   \tag{1.2}
   \]
   for some \(v_s>1\); an exactly constant exterior is included;
2. \(S=|X|\) has a single smooth inner level surface \(S=1\), separating
   a bounded \(S<1\) region from the exterior \(S>1\) region;
3. on that surface,
   \[
   \partial_r S^2>0;
   \tag{1.3}
   \]
4. the front axial root \(a(R_F)=1\) is simple, with
   \(\kappa=a'(R_F)>0\).

> **Theorem.** Under assumptions 1--4, the eternal Natario spacetime has no
> proper Hausdorff \(C^2\) Lorentzian extension.  Its given manifold is its
> maximal \(C^2\) spacetime.

Condition (1.3) is elementary for the usual monotone wall.  Indeed
\[
S^2=a^2+D\sin^2\theta,\qquad D=2ab+b^2,
\tag{1.4}
\]
and
\[
\partial_rS^2
=2aa'+2\{a'b+(a+b)b'\}\sin^2\theta.
\tag{1.5}
\]
Thus \(a'>0\) and \(b'\geq0\) through the inner wall suffice.  The logistic
wall used in the numerical audit, \(v_s=2\) and
\(f=\tfrac14[1+\tanh\sigma(r-r_0)]\), has \(a(r_0)=1\), \(a''\geq0\), and
\(b'>0\) for \(r\leq r_0\); every inner-wall root lies there because
\(S^2\geq a^2\).  The raw radial logistic is not smooth at \(r=0\), but any
smooth completion that agrees with it through the wall and flattens it inside
has exactly the same conclusion.  Natario's standard smooth compact-transition
profiles fall directly under the theorem whenever (1.3) holds.

## 2. Timelike exit dynamics

Let \(E=-p_t\), let \(P\) be the Euclidean spatial momentum, and let
\(J=p_\phi\) be the conserved axial angular momentum.  A unit timelike
geodesic obeys
\[
\dot t=E-X\cdot P,\qquad \dot t^2=|P|^2+1,
\tag{2.1}
\]
\[
\dot x=P+X\dot t,\qquad
\dot P=-\dot t\,(DX)^TP.
\tag{2.2}
\]
With (t) as parameter, write
\[
\Pi=|P|,\qquad m=P/\Pi,\qquad
\beta=\frac{\Pi}{\sqrt{\Pi^2+1}}.
\]
Then the exact projectivized system is
\[
x'=X+\beta m,
\tag{2.3}
\]
\[
m'=-(I-mm^T)(DX)^Tm,
\tag{2.4}
\]
\[
(\log\Pi)'=-m^T(DX)m,
\tag{2.5}
\]
and (2.1) gives
\[
X\cdot m=\frac E\Pi-\sqrt{1+\Pi^{-2}}.
\tag{2.6}
\]

As in the scalar-shift proof, \(t\) is a Cauchy temporal function: causal
curves satisfy \(|x'-X|\leq1\).  A proper extension therefore supplies a unit
timelike geodesic of finite proper length crossing an extension boundary.  A
finite \(t\)-endpoint is impossible because (2.2), with \(t\) as parameter,
has bounded coefficients on the resulting compact coordinate set.  In the
future case, therefore, \(t\to+\infty\).

The extension-theorem reduction, including the nonautomatic endpoint-tangent
step, is proved separately in `natario_global_exit_lemmas.md`.  There the
maximizer in the Galloway--Ling--Sbierski construction is restricted to a
convex normal neighborhood of its first boundary point.  This proves that the
physical geodesic is the restriction of a smooth extension geodesic and that
its extension tangent is finite.

Moreover
\[
\Pi\longrightarrow\infty.
\tag{2.7}
\]
Indeed, finite remaining proper time says
\(\int^\infty dt/\sqrt{\Pi^2+1}<\infty\), while (2.5) makes
\(\log\Pi\) uniformly Lipschitz.  Any infinitely recurring bounded value of
\(\Pi\) would consequently contribute a fixed positive amount to that
integral on disjoint time intervals.

## 3. Spatial infinity is not an exit

The short-range tail (1.2) is enough; exact compact support is the easy special
case.  From (2.6), for sufficiently large \(t\) and \(r\),
\[
m_x=\frac1{v_s}+o(1),
\]
and hence
\[
x'=X^x+\beta m_x
\leq-v_s+\frac1{v_s}+o(1)\leq-c<0.
\tag{3.1}
\]
Choose a sphere \(r=R\) on which (3.1) holds.  A component \([t_1,t_2]\) of
an excursion through \(r\geq R\) which returns to the sphere has
\[
c(t_2-t_1)\leq x(t_1)-x(t_2)\leq2R.
\]
Since \(|x'|\leq\|X\|_\infty+1\), every returning excursion has a uniformly
bounded maximum radius.  An unbounded trajectory must therefore eventually
remain outside the sphere.  Equation (3.1) then makes \(x\to-\infty\)
linearly, so (1.2) gives
\[
\int^\infty |DX(x(t))|\,dt<\infty.
\]
Equation (2.5) would make \(\Pi\) converge to a finite value, contradicting
(2.7).  Every finite-proper-time exit is thus spatially bounded.

## 4. The limiting zero-energy flow

The bounded state \((x(t),m(t))\) has a nonempty compact connected omega-limit
set \(\Omega\).  Equations (2.3), (2.6), and (2.7) show that every time-shifted
limit is a complete orbit of
\[
x'=X+m,\qquad
m'=-(I-mm^T)(DX)^Tm,
\tag{4.1}
\]
on
\[
|m|=1,\qquad X\cdot m=-1.
\tag{4.2}
\]
This assertion needs no abstract compactification theorem.  If
\(t_n\to\infty\), the logarithmic Lipschitz bound in (2.5) makes
\(\Pi(t_n+s)\to\infty\) uniformly on every bounded \(s\)-interval.  Arzela--
Ascoli then gives a subsequential complete solution of (4.1)--(4.2), and both
its positive and negative segments remain in \(\Omega\).

The compactness, connectedness, two-sided diagonal limit, invariance of the
zero-energy constraint, and the axis-crossing issue are proved in full in
*natario_omega_limit_audit.md*.

The conserved angular momentum removes the apparent nonmeridional loophole:
\[
y m_z-zm_y=\frac J\Pi\longrightarrow0.
\tag{4.3}
\]
Hence every limiting orbit has zero axial angular momentum and lies in a
meridional plane.  At the axis the plane can be chosen to contain its
transverse direction.  Reflection equivariance and uniqueness then keep the
complete orbit in that same plane through every axis crossing. No estimate on
\(\varrho\Pi\) is required.

## 5. The branch-switching lemma

The poloidal streamfunction is
\[
\Psi=-v_sf(r)\varrho^2=-\frac{a(r)}2\varrho^2,
\qquad X\cdot\nabla\Psi=0.
\tag{5.1}
\]
For a zero-angular-momentum limiting ray in \(S>1\), let \(e=X/S\) and let
\(n=\nabla\Psi/(\varrho S)\).  The two solutions of (4.2) are
\[
m=-\frac eS\pm\sqrt{1-S^{-2}}\,n,
\]
and therefore
\[
\Psi'=\pm\varrho\sqrt{S^2-1}.
\tag{5.2}
\]
The sign is constant except at the axis or at \(S=1\).  The key fact is that
**every nonstationary sign-switch point is a strict local maximum of
\(\Psi\)**.

On the axis with \(S>1\), use a signed meridional coordinate \(y\).  The
constraint gives
\(y'^2=1-S^{-2}>0\), while
\(\Psi=-a y^2/2+O(y^4)\).  Thus
\[
\Psi''=-a y'^2<0.
\tag{5.3}
\]

At a nonaxial point of \(S=1\), (4.2) forces \(m=-X\), so \(x'=0\), and
\[
m'=\frac12(I-XX^T)\nabla S^2.
\]
Since \(\nabla\Psi\perp X\),
\[
\Psi''=\frac12\nabla\Psi\cdot\nabla S^2.
\tag{5.4}
\]
In polar coordinates in the meridional plane,
\[
\nabla\Psi
=-r(a+b)\sin^2\theta\,e_r
 -ar\sin\theta\cos\theta\,e_\theta,
\]
so (1.3)--(1.4) give
\[
\Psi''
=-\frac{\sin^2\theta}{2}
 \left[r(a+b)\partial_rS^2+2aD\cos^2\theta\right]<0.
\tag{5.5}
\]

Consequently a ray can switch from the increasing to the decreasing branch,
but never from decreasing back to increasing.  It can switch at most once.
This disposes of the proposed axis/wall branch-switching chains.

There is a useful global formulation.

> **Branch-switching lemma.** Every complete zero-angular-momentum orbit of
> (4.1)--(4.2) whose spatial projection is precompact is an equilibrium.

The complete proof is in *natario_branch_compact_orbit_audit.md*. In brief,
two strict maxima would force an intervening minimum, so a nonconstant orbit
has at most one critical time. Its alpha- and omega-limit sets are invariant
constant-\(\Psi\) sets and therefore consist only of equilibria. The strict
wall identity excludes every nonaxial equilibrium; the single wall leaves the
front and rear axial points, both with \(\Psi=0\). If there is no critical
time, strict monotonicity is incompatible with equal end values. If there is
one maximum, the increasing negative-time branch would rise from limiting
value zero and force \(\Psi>0\), contradicting
\(\Psi=-a\varrho^2/2\leq0\).

Every point of \(\Omega\) lies on a complete limiting orbit contained in the
compact set \(\Omega\).  The lemma therefore gives
\[
\Omega\subseteq\{\text{front axial equilibrium},
                  \text{rear axial equilibrium}\}.
\]
The omega-limit set of a precompact continuous curve is connected, so it is
one of these points.  At the rear point, however,
\((\log\Pi)'\to-\kappa\), contradicting (2.7).  Hence
\[
x(t)\longrightarrow(R_F,0,0),\qquad
m(t)\longrightarrow e_x,qquad
(\log\Pi)'\longrightarrow\kappa.
\tag{5.6}
\]

## 6. Curvature contradiction

The closed local-jet calculation gives at the front axis
\[
R_{tyty}=R_{tztz}
=-\frac{2\kappa}{R_F}-\frac{3\kappa^2}{4}<0,
\]
and hence
\[
R_{tt}=2R_{tyty}
=-\frac{\kappa(3R_F\kappa+8)}{2R_F}<0.
\tag{6.1}
\]
Equations (2.1)--(2.3) and (5.6) imply
\[
\frac{\dot\gamma}{\Pi}\longrightarrow\partial_t.
\]
Therefore
\[
\frac{\operatorname{Ric}(\dot\gamma,\dot\gamma)}{\Pi^2}
\longrightarrow R_{tt}(R_F,0,0)<0.
\tag{6.2}
\]
The left side diverges in magnitude because \(\Pi\to\infty\).  In a \(C^2\)
extension, the crossing geodesic has a finite tangent at its endpoint and the
Ricci tensor is continuous, so the same contraction must remain finite.  This
is the contradiction.

The isometry
\((t,x,y,z)\mapsto(-t,-x,y,z)\) converts the past case into the future case.
No future or past extension boundary remains, proving the theorem.

The front/rear selection, exact Natario Ricci jet, tangent asymptotics,
extension-regularity contradiction, and time-reversal isometry are audited
independently in *natario_endpoint_curvature_audit.md*.

## 7. Audit status

- The proof is analytic; the ray scans are no longer load-bearing.
- `natario_explicit_smooth_profile.md` constructs a globally smooth compact
  transition satisfying every profile hypothesis and proves
  \(\partial_rS^2>0\) analytically on its complete wall.
- `natario_global_exit_lemmas.md` gives the adversarially audited extension,
  finite-Killing-time, uniform momentum-divergence, and spatial-infinity
  arguments.  In particular, the infinity proof controls repeated excursions
  and does not assume eventual radial monotonicity.
- `sim/vector_shift_geodesic_symbolic.py` independently checks the energy,
  momentum, normalization, and spatial Euler--Lagrange signs in (2.1)--(2.2).
- `sim/natario_branch_switch_symbolic.py` verifies the exact wall identity
  (5.5) and reduces its difference from the displayed target to zero.
- `sim/natario_ray_scan_3d.py` independently samples the complete azimuthal
  direction circle and found no bounded counterexample in the standard wall
  model, consistent with the theorem.
- *natario_omega_limit_audit.md* proves the complete two-sided limiting-flow
  construction and closes the possible change-of-plane loophole at the axis.
- *sim/natario_omega_limit_symbolic.py* checks exact angular-momentum
  conservation and tangency of the limiting flow to the unit zero-energy
  constraint.
- *natario_branch_compact_orbit_audit.md* supplies the full alpha/omega-limit
  argument excluding recurrent, periodic, and homoclinic-looking compact
  limiting orbits.
- *natario_endpoint_curvature_audit.md* checks front selection, the exact
  vector-shift Ricci coefficient, the invariant blow-up, and the past
  isometry.
- The essential new observation is (5.5): both types of branch switch are
  strict maxima of the same streamfunction.  Conserved angular momentum then
  vanishes automatically in every high-momentum omega-limit.
- The hypotheses are profile conditions, not merely compactness or mean
  curvature.  A profile with a nonmonotone \(S=1\) wall could violate (1.3)
  and would require a separate dynamical analysis.
