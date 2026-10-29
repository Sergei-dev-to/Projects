# Natario endpoint selection and curvature audit

Final verification note, 2026-08-03. The preceding audits reduce every
hypothetical future boundary of a proper \(C^2\) extension to a unit timelike
geodesic satisfying
\[
\tau_*<\infty,\qquad
t\to\infty,\qquad
\Pi=|P|\to\infty,
\tag{0.1}
\]
whose projectivized state \(z(t)=(\boldsymbol x(t),m(t))\) has omega-limit set
equal to one of the two axial equilibria
\[
Q_F=((R_F,0,0),e_x),\qquad
Q_R=((-R_F,0,0),e_x).
\tag{0.2}
\]

Put
\[
\kappa=a'(R_F)=2v_sf'(R_F)>0.
\tag{0.3}
\]

## Lemma 1: a future exit selects the front equilibrium

If a precompact continuous trajectory has a singleton omega-limit set, it
converges to that point. Otherwise a sequence staying a fixed distance away
would have a convergent subsequence and produce a second omega-limit point.
Thus \(z(t)\to Q_F\) or \(z(t)\to Q_R\).

The exact momentum equation is
\[
(\log\Pi)'=-m^T(DX)m.
\tag{1.1}
\]
On the axis \(X^x=-a(r)\). At the two roots,
\[
\partial_xX^x(Q_F)=-\kappa,\qquad
\partial_xX^x(Q_R)=+\kappa.
\tag{1.2}
\]
Since \(m=e_x\) at both equilibria, convergence to the rear would give
\[
(\log\Pi)'\longrightarrow-\kappa.
\]
For all sufficiently large \(t\), this derivative would be less than
\(-\kappa/2\), forcing \(\Pi\to0\) exponentially. That contradicts (0.1).
Therefore
\[
z(t)\longrightarrow Q_F,\qquad
(\log\Pi)'\longrightarrow\kappa.
\tag{1.3}
\]

## Lemma 2: the rescaled unit tangent approaches the stationary null vector

Let \(u=\dot\gamma\) be the unit future tangent. The exact equations give
\[
\dot t=\sqrt{\Pi^2+1},\qquad
\dot{\boldsymbol x}=\Pi m+X\dot t.
\]
Consequently
\[
\frac u\Pi
=\frac{\sqrt{\Pi^2+1}}{\Pi}\,\partial_t
 +\left(m+\frac{\sqrt{\Pi^2+1}}{\Pi}X\right)^i\partial_i
\longrightarrow\partial_t
\tag{2.1}
\]
by (1.3), because \(m\to e_x\) and \(X(Q_F)=-e_x\). Hence, for every smooth
covariant two-tensor \(T\),
\[
\frac{T(u,u)}{\Pi^2}\longrightarrow T_{tt}(Q_F).
\tag{2.2}
\]

## Lemma 3: the Natario front Ricci coefficient is strictly negative

Center Cartesian coordinates at the front point. The local Natario shift jet
has
\[
\partial_xX^x=-\kappa,\qquad
\partial_yX^y=\partial_zX^z=\frac\kappa2,
\tag{3.1}
\]
and
\[
\partial_{yy}X^x=\partial_{zz}X^x=-\frac{2\kappa}{R_F}.
\tag{3.2}
\]
For the general axisymmetric jet
\[
X^x=-1+A x+\frac12(B_x\,x^2+B_y\,y^2+B_z\,z^2)+O(3),
\]
\[
X^y=C y+D\,xy+O(3),\qquad
X^z=C z+D\,xz+O(3),
\tag{3.3}
\]
the exact coordinate calculation for
\[
g=-dt^2+\delta_{ij}(dx^i-X^idt)(dx^j-X^jdt)
\]
gives, with
\((\nabla_c\nabla_d-\nabla_d\nabla_c)V^a=R^a{}_{bcd}V^b\),
\[
R_{tyty}=AC+B_y-C^2,\qquad
R_{tztz}=AC+B_z-C^2.
\tag{3.4}
\]
Substitution of
\[
A=-\kappa,\qquad C=\frac\kappa2,\qquad
B_y=B_z=-\frac{2\kappa}{R_F}
\]
therefore yields
\[
R_{tyty}=R_{tztz}
=-\frac{2\kappa}{R_F}-\frac{3\kappa^2}{4}.
\tag{3.5}
\]
At \(X=-e_x\), the inverse metric has \(g^{xx}=0\); equivalently, a direct
Ricci contraction of the same jet gives
\[
\operatorname{Ric}_{tt}
=R_{tyty}+R_{tztz}
=-\frac{4\kappa}{R_F}-\frac{3\kappa^2}{2}
=-\frac{\kappa(3R_F\kappa+8)}{2R_F}<0.
\tag{3.6}
\]

The extra \(-3\kappa^2/2\) compared with the scalar-shift Ricci coefficient is
the genuine vector-shift strain contribution. The exact symbolic calculation
in *sim/natario_local_jet.py* verifies (3.4)--(3.6). The independent
finite-difference calculation in *sim/natario_curvature_fd.py* gives, for
\(\kappa=3\) and \(R_F=1\),
\[
R_{tyty}\simeq-12.75029,\qquad
\operatorname{Ric}_{tt}\simeq-25.50058,
\]
against the exact values \(-12.75\) and \(-25.5\).

## Lemma 4: curvature contradicts a \(C^2\) endpoint

Equations (2.2) and (3.6) give
\[
\frac{\operatorname{Ric}(u,u)}{\Pi^2}
\longrightarrow
-\frac{\kappa(3R_F\kappa+8)}{2R_F}<0.
\tag{4.1}
\]
Since \(\Pi\to\infty\),
\[
\operatorname{Ric}(u,u)\longrightarrow-\infty.
\tag{4.2}
\]

The extension-boundary audit supplied more than a topological endpoint. The
final segment of \(\gamma\), with its boundary point appended, is a smooth
timelike geodesic in a convex normal neighborhood of the putative \(C^2\)
extension. Its unit tangent therefore has a finite limit there. A \(C^2\)
metric has continuous Ricci tensor, so \(\operatorname{Ric}(u,u)\) must remain
finite. This contradicts (4.2). No future extension boundary exists.

## Lemma 5: the past case is isometric to the future case

The Natario shift obeys
\[
X^x(-x,y,z)=X^x(x,y,z),\qquad
X^{y,z}(-x,y,z)=-X^{y,z}(x,y,z).
\]
Therefore
\[
\mathcal I:(t,x,y,z)\longmapsto(-t,-x,y,z)
\tag{5.1}
\]
is an isometry of the full spacetime. It exchanges past with future and rear
with front. A past extension boundary would consequently produce a future
extension boundary after precomposing the embedding with \(\mathcal I\),
which Lemma 4 excludes.

## Final theorem

For every smooth stationary Natario zero-expansion profile satisfying:

1. \(v_s>1\), \(f\geq0\), \(f'\geq0\), and a bounded smooth shift approaching
   its constant exterior value exponentially; an exactly constant exterior is
   included;
2. one smooth compact inner wall \(S=|X|=1\), separating the bounded
   \(S<1\) region from \(S>1\);
3. \(\partial_rS^2>0\) on that entire wall;
4. a simple axial root \(a(R_F)=1\), \(a'(R_F)=\kappa>0\);

the spacetime on \(\mathbb R^4\) admits no proper Hausdorff \(C^2\)
Lorentzian extension. It is maximal as a \(C^2\) spacetime.

The explicit compact-transition profile in
*natario_explicit_smooth_profile.md* proves that this hypothesis class is
nonempty without any smoothing caveat.

## Adversarial audit

1. **A singleton omega set without convergence.** Precompactness turns every
   nonconvergent subsequence into another omega-limit point.
2. **Rear momentum that still diverges because of earlier growth.** An
   eventually negative logarithmic derivative forces exponential decay
   regardless of earlier history.
3. **Using \(\dot t\) and \(\Pi\) interchangeably.** Their exact ratio is
   \(\sqrt{1+\Pi^{-2}}\to1\), which is retained in (2.1).
4. **Ignoring spatial tangent components.** They cancel in the limit because
   \(m+X\to e_x-e_x=0\).
5. **Importing the scalar-shift curvature formula.** The Natario vector jet is
   recomputed directly and includes the additional strain term.
6. **Inferring Ricci from only one Riemann component.** Both transverse
   components and the direct Ricci contraction are checked symbolically.
7. **Only a divergent coordinate component.** The coordinate Ricci tensor is
   finite; it is the contraction with the diverging unit tangent that blows
   up, an invariant scalar along the geodesic.
8. **A boundary endpoint with uncontrolled tangent.** The convex-normal
   maximizer argument from the global-exit audit supplies the finite extension
   tangent needed here.
9. **Only future inextendibility.** The explicit isometry (5.1) closes the
   past case.
