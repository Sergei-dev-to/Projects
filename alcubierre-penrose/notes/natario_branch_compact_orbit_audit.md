# Natario branch-switching and compact-orbit audit

Adversarial verification note, 2026-08-03. By
*natario_omega_limit_audit.md*, it is enough to study complete spatially
precompact orbits of
\[
\boldsymbol x'=X+m,\qquad
m'=-(I-mm^T)(DX)^Tm,\qquad
|m|=1,\quad X\cdot m=-1
\tag{0.1}
\]
in one fixed meridional plane.

Write
\[
a(r)=2v_sf(r),\qquad b(r)=\frac r2a'(r),\qquad
S=|X|.
\]
For the monotone profile class, \(a,b\geq0\). In meridional polar
coordinates,
\[
S^2=a^2+D\sin^2\theta,\qquad D=2ab+b^2\geq0.
\tag{0.2}
\]
The inner wall is the single compact level set \(S=1\), and
\[
\partial_rS^2>0
\tag{0.3}
\]
everywhere on it.

## Lemma 1: the two streamfunction branches

The smooth poloidal streamfunction is
\[
\Psi=-\frac{a(r)}2\varrho^2.
\tag{1.1}
\]
Direct differentiation of the Natario shift gives
\[
X\cdot\nabla\Psi=0,\qquad |\nabla\Psi|=\varrho S.
\tag{1.2}
\]
At a point with \(\varrho>0\) and \(S>1\), put
\[
e=\frac X S,\qquad n=\frac{\nabla\Psi}{\varrho S}.
\]
The unit-vector and zero-energy constraints in (0.1) have exactly two
solutions,
\[
m=-\frac eS\mathbin{\pm}\sqrt{1-S^{-2}}\,n.
\tag{1.3}
\]
Since the shift is tangent to the streamlines,
\[
\Psi'=\nabla\Psi\cdot(X+m)
      =\mathbin{\pm}\varrho\sqrt{S^2-1}.
\tag{1.4}
\]
Thus a zero of \(\Psi'\) on the constrained state space can occur only on the
axis \(\varrho=0\) or on the wall \(S=1\).

## Lemma 2: every nonstationary axial zero is a strict maximum

Use a signed transverse coordinate \(y\) in the fixed meridional plane. At an
axis point with \(S>1\), the shift is \(X=-a e_x\). The constraint gives
\[
m_x=\frac1a,\qquad
(y')^2=m_y^2=1-a^{-2}>0.
\tag{2.1}
\]
Because
\[
\Psi=-\frac12a\bigl(\sqrt{x^2+y^2}\bigr)y^2,
\]
all derivatives of \(a\) are multiplied by \(y\) at the crossing, and
\[
\Psi''=-a(y')^2<0.
\tag{2.2}
\]
The axial points with \(S=1\) are treated below; they are equilibria.

## Lemma 3: every nonaxial wall zero is a strict maximum

At \(S=1\), equality in Cauchy--Schwarz forces \(m=-X\), so
\(\boldsymbol x'=0\). Equation (0.1) gives
\[
m'=\frac12(I-XX^T)\nabla S^2.
\tag{3.1}
\]
Since \(\nabla\Psi\perp X\),
\[
\Psi''=\frac12\nabla\Psi\cdot\nabla S^2.
\tag{3.2}
\]
The orthonormal polar components are
\[
\nabla\Psi
=-r(a+b)\sin^2\theta\,e_r
 -ar\sin\theta\cos\theta\,e_\theta.
\tag{3.3}
\]
Combining (0.2)--(0.3) with (3.2) gives
\[
\Psi''
=-\frac{\sin^2\theta}{2}
 \left[
 r(a+b)\partial_rS^2+2aD\cos^2\theta
 \right]<0
\tag{3.4}
\]
at every nonaxial wall point. Indeed, \(\sin\theta\ne0\),
\(a+b>0\) on \(S=1\), and every other displayed factor is nonnegative,
while the first term in brackets is strictly positive.

## Lemma 4: the only equilibria are the two axial wall points

An equilibrium of (0.1) must have
\[
m=-X,\qquad S=1,\qquad
(I-XX^T)\nabla S^2=0.
\tag{4.1}
\]
At a nonaxial wall point, (3.2)--(3.4) show that the projected gradient in
(4.1) is nonzero. Thus no such point is an equilibrium.

On the axis, \(X\), \(\nabla S^2\), and the axis direction are parallel, so
(4.1) holds wherever \(S=1\). The single-wall hypothesis and
\(a(R_F)=1\) leave exactly
\[
Q_F=((R_F,0),e_x),\qquad Q_R=((-R_F,0),e_x)
\tag{4.2}
\]
as phase-space states \((\boldsymbol x,m)\). Both have
\[
\Psi(Q_F)=\Psi(Q_R)=0.
\tag{4.3}
\]

## Lemma 5: a nonconstant orbit has at most one critical time

Let \(h(s)=\Psi(\boldsymbol x(s))\) along a nonconstant complete orbit.
The orbit cannot reach an equilibrium at finite \(s\), because uniqueness
would then make it that equilibrium for all time. Lemmas 1--3 therefore show
that every zero of \(h'\) is a strict local maximum.

There cannot be two such zeros. If \(s_1<s_2\) were two strict maxima, the
minimum of \(h\) on \([s_1,s_2]\) would occur at an interior point. At that
point \(h'=0\), but it is not a strict local maximum. A constant minimum
interval gives the same contradiction at each of its points. Hence \(h'\)
has at most one zero.

If it has one zero \(s_0\), the sign of the continuous nonvanishing derivative
on each side, together with strict maximality, is
\[
h'>0\quad(s<s_0),\qquad h'<0\quad(s>s_0).
\tag{5.1}
\]
If it has no zero, \(h\) is strictly monotone on all of \(\mathbb R\).

## Lemma 6: both temporal limit sets consist of equilibria

Suppose the spatial orbit is precompact. Since \(m\in S^2\), the complete
phase orbit is precompact. Lemma 5 makes \(h\) monotone on each temporal tail,
so the finite limits
\[
\ell_-=\lim_{s\to-\infty}h(s),\qquad
\ell_+=\lim_{s\to+\infty}h(s)
\tag{6.1}
\]
exist.

The alpha- and omega-limit sets are nonempty, compact, and invariant. The
function \(h\) is respectively constant there with values \(\ell_-\) and
\(\ell_+\). Hence the complete orbit through any point of either limit set
has \(\Psi'=0\) for all its times. Such a point cannot be nonstationary:
Lemmas 2--3 would make its own \(\Psi\) have a strict local maximum rather
than remain constant. It must therefore be an equilibrium. By Lemma 4,
\[
\ell_-=\ell_+=0.
\tag{6.2}
\]

## Lemma 7: no nonconstant precompact complete orbit exists

The streamfunction has the global sign
\[
\Psi=-\frac a2\varrho^2\leq0.
\tag{7.1}
\]
If \(h'\) has no zero, \(h\) is strictly monotone but has the same value zero
at both temporal ends by (6.2), which is impossible.

If \(h'\) has one zero \(s_0\), then \(h\) is strictly increasing on
\((-\infty,s_0)\). Its limit at the negative end is zero, so strict increase
would give
\[
h(s)>0\qquad(s<s_0),
\]
contradicting (7.1). Equivalently, a homoclinic-looking graph that touches
\(\Psi=0\) at a central maximum would require a local minimum on either side
in order to return to the zero end value; Lemma 5 forbids that minimum.

Thus every spatially precompact complete orbit of (0.1) is one of the two
equilibria in (4.2).

## Step-4 conclusion

Every complete limiting orbit through the compact omega-limit set
\(\Omega\) is an equilibrium, so
\[
\Omega\subseteq\{Q_F,Q_R\}.
\tag{8.1}
\]
The set \(\Omega\) is connected by the preceding omega-limit audit. Therefore
it is exactly one of these two singleton states.

This step does not yet select front versus rear and does not use curvature.
The next stage must use the exact momentum-growth equation to select the front
state, then verify the Ricci blow-up and the final \(C^2\)-extension
contradiction.

## Adversarial audit

1. **A chain of axis and wall switches.** Every nonstationary critical point
   is a strict maximum; two maxima would force an intervening minimum.
2. **Infinitely many switches accumulating at an equilibrium.** There cannot
   be two finite critical times at all. Accumulation at a temporal end is
   absorbed into its invariant limit set, which Lemma 6 reduces to
   equilibria.
3. **A periodic or recurrent orbit with no switch.** Its streamfunction would
   be strictly monotone, incompatible with recurrence and with equal endpoint
   values.
4. **A homoclinic orbit through an axial maximum.** The negative temporal
   branch would have to increase strictly from limit \(0\), forcing
   \(\Psi>0\).
5. **A nonaxial stationary generator.** The strict wall identity (3.4)
   directly contradicts the projected-gradient equilibrium condition.
6. **A hidden use of numerics.** The proof uses only (0.2)--(0.3), the exact
   streamfunction identities, and the single-wall hypotheses.
