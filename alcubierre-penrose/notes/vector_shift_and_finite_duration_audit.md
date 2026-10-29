# Vector shifts and finite-duration amplification

Working audit, 2026-08-03.

## 1. General stationary vector shift

Consider
\[
g=-dt^2+\delta_{ij}(dx^i-X^i(\boldsymbol x)dt)
                    (dx^j-X^j(\boldsymbol x)dt).
\]
Let
\[
E=-p_t,\qquad P_i=p_i.
\]
The orthonormal normal-frame decomposition and Hamilton equations are
\[
\dot t=E-X\cdot P,\qquad
\dot t^2=|P|^2+1,
\]
\[
\dot x^i=P_i+X^i\dot t,\qquad
\dot P_i=-\dot t\,(\partial_iX^j)P_j.
\tag{1.1}
\]
With \(t\) as parameter,
\[
\frac{dP}{dt}=-(\nabla X)^TP.
\tag{1.2}
\]

For a finite-proper-time exit with \(t\to+\infty\), one has
\[
|P|,\dot t\to\infty.
\]
Writing \(n=P/\dot t\),
\[
|n|\to1,\qquad 1+X\cdot n=\frac E{\dot t}\to0,
\tag{1.3}
\]
and
\[
\frac{d\boldsymbol x}{dt}=X+n.
\tag{1.4}
\]

For a scalar shift \(X=ve_x\), equations (1.2)--(1.4) reduce to the monotone
longitudinal system used in the Alcubierre proof. For a genuine vector shift
they do not.

Put \(P=\rho m\), \(|m|=1\). At high momentum,
\[
\frac{d\log\rho}{dt}
=-m^T(\nabla X)m,
\tag{1.5}
\]
\[
\frac{dm}{dt}
=-(I-mm^T)(\nabla X)^Tm,
\tag{1.6}
\]
\[
\frac{d\boldsymbol x}{dt}=X+m+o(1),
\qquad X\cdot m=-1+o(1).
\tag{1.7}
\]
The antisymmetric part of \(\nabla X\) rotates \(m\); its symmetric strain
controls growth of \(\rho\).

## 2. Why a universal Natário maximality theorem does not follow

Equations (1.5)--(1.7) permit invariant or recurrent high-frequency dynamics
inside \(|X|>1\). A bounded exit need not approach
\[
\Sigma=\{|X|=1\};
\]
it could approach a trapped set satisfying \(X\cdot m=-1\) on which the strain
makes \(\rho\) grow exponentially. The scalar proof excludes this with the
one-dimensional identity
\[
\frac{dx}{dt}=v-\frac1v+o(1),
\]
for which no vector analogue exists.

Thus a vector-shift global theorem needs one of:

1. a no-trapped-ray hypothesis for the system (1.5)--(1.7);
2. a Lyapunov function special to the chosen shift;
3. an explicit classification of its high-momentum invariant sets.

Compactness of \(\{|X|=1\}\) and the mean curvature of that surface do not
provide this information.

The stationary Killing orbit is null on \(\Sigma\). Its pregeodesic condition
is
\[
(I-X\otimes X)\nabla|X|^2=0
\qquad\text{on }|X|=1,
\tag{2.1}
\]
equivalently, the spatial normal to \(\Sigma\) is parallel to \(X\). A support
point in a fixed coordinate direction does not automatically satisfy (2.1).
Even when it does, the screen rotation from the antisymmetric part of
\(\nabla X\) can enter the endpoint linearization. Therefore the scalar
pure-boost and wall-mean-curvature formulas cannot be imported unchanged.

## 3. Natario global dynamics: streamfunction reduction

Natario's axisymmetric field has much more structure than a generic vector
shift. In cylindrical coordinates \((x,\varrho,\phi)\), put
\[
a(r)=2v_sf(r),\qquad b(r)=v_sr f'(r),\qquad
u=\frac{\varrho^2}{r^2}.
\]
Then
\[
X^x=-a-bu,\qquad
X^\varrho=b\frac{x\varrho}{r^2},\qquad X^\phi=0,
\]
and the poloidal streamfunction
\[
\Psi(x,\varrho)=-v_sf(r)\varrho^2
\tag{3.1}
\]
satisfies
\[
X^x=\frac1\varrho\partial_\varrho\Psi,\qquad
X^\varrho=-\frac1\varrho\partial_x\Psi,\qquad
X\cdot\nabla\Psi=0.
\tag{3.2}
\]

For a zero-angular-momentum high-frequency ray, let \(S=|X|>1\),
\(e=X/S\), and let \(n\) be the left Euclidean normal to \(e\) in the
meridional plane. The limiting constraint \(X\cdot m=-1\), \(|m|=1\), has
only two branches:
\[
m=-\frac eS\pm\sqrt{1-S^{-2}}\,n,
\]
so the spatial ray velocity is
\[
w=X+m=(S-S^{-1})e\pm\sqrt{1-S^{-2}}\,n.
\tag{3.3}
\]
Since \(\nabla\Psi=\varrho S n\), equations (3.1)--(3.3) give the exact
identity
\[
\frac{d\Psi}{dt}=\pm\varrho\sqrt{S^2-1}.
\tag{3.4}
\]
Thus a fixed branch has no periodic or recurrent orbit in the interior
\(\{\varrho>0,S>1\}\). This is the Natario analogue of the scalar monotonicity
identity and substantially narrows the global problem.

The norm also has the simple form
\[
S^2=a^2+(2ab+b^2)\sin^2\theta.
\tag{3.5}
\]
If \(\partial_rS^2>0\) on the inner \(S=1\) surface, the stationary-geodesic
locus there consists only of the two axial points. Indeed, with
\(D=2ab+b^2\), the condition that \(\nabla S^2\) be parallel to \(X\) has,
off axis, the strictly negative cross product
\[
X_r\frac1r\partial_\theta S^2-X_\theta\partial_rS^2
=-\sin\theta\left[
  \frac{2aD}{r}\cos^2\theta+(a+b)\partial_rS^2
 \right].
\tag{3.6}
\]
For the standard \(v_s=2,\sigma=3,r_0=1\) tanh profile, a 101-angle bisection
audit finds
\[
\min_{S=1}\partial_rS^2=6
\]
at the axis, so this sufficient condition holds.

Script `sim/natario_ray_scan.py` also integrated the full projectivized
meridional system. In a scan of 1028 constrained initial rays through
\(t=100\), no bounded orbit was found. A separately shot stable branch
approaches the front axial generator and has mean momentum growth \(\kappa=3\),
as predicted. This is evidence, not the missing global proof.

There is a sharper local dynamical identity. Write \(\eta=\varrho\) and let
\(\psi\) be the small angle of \(m\) away from the forward axial direction. The
Natario front jet gives
\[
\frac d{dt}
\begin{pmatrix}\eta\\ \psi\end{pmatrix}
=
\begin{pmatrix}
\kappa/2 & 1\\[2pt]
2\kappa/R_F & -3\kappa/2
\end{pmatrix}
\begin{pmatrix}\eta\\ \psi\end{pmatrix}.
\tag{3.7}
\]
Its trace is \(-\kappa\), while its determinant is
\[
\det M
=-\frac{2\kappa}{R_F}-\frac{3\kappa^2}{4}
=R_{tyty}.
\tag{3.8}
\]
Thus the same coefficient that drives the parallel-propagated tidal divergence
is the transverse stability determinant of the limiting ray. Since it is
negative, the front orbit is a saddle with a one-dimensional transverse stable
manifold. For \(\kappa=3,R_F=1\),
\[
\lambda_\pm=\frac{-3\pm\sqrt{60}}2,
\]
and the stable direction has
\(\psi/\eta=\lambda_--\kappa/2=-6.872983\ldots\), exactly the direction found
by the numerical shooting check. This is stronger than a catalogue
coincidence: wall curvature, null-ray stability, and tidal amplification are
three readings of the same local coefficient in the Natario front jet.

The apparent dynamical loophole is now closed. At an axis crossing with
\(S>1\), a signed meridional coordinate gives
\[
\Psi''=-a\,y'^2<0.
\]
At a nonaxial turning point of \(S=1\),
\[
\Psi''=\frac12\nabla\Psi\cdot\nabla S^2
=-\frac{\sin^2\theta}{2}
 \left[r(a+b)\partial_rS^2+2a(2ab+b^2)\cos^2\theta\right]<0
\tag{3.9}
\]
whenever \(\partial_rS^2>0\) on the inner wall. Thus every possible sign
switch in (3.4) is a strict local maximum of the same streamfunction. A
meridional ray can switch at most once, so no axis/wall switching chain is
possible.

Nonzero conserved angular momentum also disappears in the only limit relevant
to a finite-proper-time exit. If \(\Pi=|P|\) and \(J=p_\phi\), then
\[
y m_z-zm_y=\frac J\Pi\longrightarrow0
\]
because \(\Pi\to\infty\). Every time-shifted omega-limit orbit is therefore a
complete zero-angular-momentum orbit of the limiting system. The
streamfunction maximum lemma makes the only spatially precompact complete
orbits the front and rear axial equilibria. Momentum decays at the rear and
grows at the front, so a future exit must approach the front. The nonzero
coefficient (3.8)/(4.1) then gives the \(C^2\) curvature contradiction.
The full proof, including exclusion of spatial infinity for an exponential
tail, is in the dedicated Natario global-maximality note.

## 4. Natario local coefficient: closed form

For Natário's axisymmetric zero-expansion field, the front axis is an invariant
geodesic locus and the linearization is pure boost by axisymmetry. Let
\[
\kappa=2v_s f'(R_F)>0
\]
at the simple front root \(2v_sf(R_F)=1\). The local-jet calculation in
sim/natario_local_jet.py gives
\[
R_{tyty}=R_{tztz}
=-\frac{\kappa(3R_F\kappa+8)}{4R_F}
=-\frac{2\kappa}{R_F}-\frac{3\kappa^2}{4},
\tag{4.1}
\]
\[
R_{txtx}=-\kappa^2-2v_sf''(R_F).
\tag{4.2}
\]
Equation (4.1) is strictly negative for every simple front root. Hence
\[
R_{KYKY}=q^2R_{tyty}
\]
and
\[
R_{tt}=2R_{tyty}
=-\frac{\kappa(3R_F\kappa+8)}{2R_F}<0.
\tag{4.3}
\]
The local PP curvature and negative null-source divergences therefore hold for
the entire simple-root Natário profile class.

This local calculation alone does not prove global \(C^2\)-inextendibility;
that additionally requires exhausting all finite-proper-time exits of
(1.5)--(1.7). The subsequent streamfunction and omega-limit audits now perform
that exhaustion for the monotone single-wall profile class; see
*natario_global_maximality_proof.md* and its dedicated audit notes.

## 5. Finite-duration stationary segment

Suppose a geometry is exactly stationary near a nondegenerate generator for a
Killing-time interval of duration \(T\). If \(K=q\partial_t\) is affinely
normalized at entry, then
\[
\frac{dq}{dt}=\kappa q,\qquad
\frac{q_{\rm out}}{q_{\rm in}}=e^{\kappa T}.
\tag{5.1}
\]
Consequently
\[
R_{KAKB}^{\rm out}
=e^{2\kappa T}R_{KAKB}^{\rm in}
\tag{5.2}
\]
when the stationary screen coefficient is constant, and likewise
\[
T_{KK}^{\rm out}
=e^{2\kappa T}T_{KK}^{\rm in}.
\tag{5.3}
\]

The affine normalization must be fixed physically, for example by prescribing
the ray frequency measured by an entry observer. Equations (5.2)--(5.3) then
describe an exponential blueshift in the transported frame. They do **not**
say that the stationary coordinate components of the metric or source grow
with the lifetime of the bubble.

There is also a clean conditional stability theorem for a smoothly created and
destroyed bubble. The spatial momentum equation remains exact even for a
time-dependent shift:
\[
\frac{dP}{dt}=-(\nabla X)^TP,
\qquad
\frac{d\log|P|}{dt}=-m^T(\nabla X)m.
\tag{5.4}
\]
Let \(A_0=\nabla X_0(p)\) and let \(m_0\) be the stationary generator direction,
so \(-m_0^TA_0m_0=\kappa>0\). If throughout a stationary core interval of
length \(T\)
\[
|m-m_0|\le\delta,
\qquad
\|\nabla X-A_0\|\le\varepsilon,
\]
then
\[
\frac{|P|_{\rm out}}{|P|_{\rm in}}
\ge
\exp\{[\kappa-\varepsilon-2\|A_0\|\delta]T-B\}.
\tag{5.5}
\]
Here
\[
B=\int_{\text{switching layers}}
\max\{0,m^T(\nabla X)m\}\,dt
\]
is the finite logarithmic loss in the creation and destruction phases. Equation
(5.5) follows directly by integrating (5.4). If the relevant screen-curvature
coefficient stays bounded away from zero along the shadowing ray, the measured
tidal contraction inherits the square of this lower bound.

Thus amplification is proved for every ray satisfying quantitative shadowing.
The genuinely dynamical finite-duration problem is now to prove the existence
of such a ray, with \(\delta,\varepsilon,B\) independent of \(T\), for a stated
creation/destruction protocol. That is a stable-manifold or normally-hyperbolic
shadowing theorem, not another curvature calculation.

## 6. Current ceiling

- **Complete:** radial scalar-shift maximality for a profile class.
- **Complete:** generic compact nonradial scalar-shift maximality under a
  compact nonzero-Hessian stationary locus and constant exterior; discreteness
  is not required.
- **Complete:** closed Natário local PP/source coefficient for all simple-root
  profiles.
- **Open even smoothly:** degenerate scalar-shift local rigidity and no
  simultaneous regular geodesic resolution. The common-domain lemma for
  genuine \(C^2\) isometry germs is proved, but anchored uniqueness supplies
  only one-sided isometry data.
- **Complete for a profile class:** global Natario \(C^2\) maximality. Under a
  single monotone inner \(S=1\) wall with \(\partial_rS^2>0\), and an exact or
  exponentially short-range exterior tail, branch switching cannot recur,
  angular momentum vanishes in the omega-limit, and every exit reaches the
  singular front axial generator.
- **Complete:** finite-duration maximality for every smooth bounded
  time-dependent shift with
  \(\int_{\mathbb R}\|D_{\boldsymbol x}X(t,\cdot)\|_\infty dt<\infty\).
  The spatial momentum equation and Gronwall's inequality give timelike
  completeness; global hyperbolicity then gives \(C^0\)-inextendibility by the
  Galloway--Ling--Sbierski theorem.  This includes uniformly controlled shifts
  switched on and off in finite time.
- **Complete conditionally, open dynamically only as an amplification
  problem:** the finite-duration bound (5.5) is rigorous for a quantitatively
  shadowing ray; existence of such a ray uniformly in the bubble lifetime is
  the remaining protocol-dependent stable-manifold problem.  It is not needed
  for the preceding maximality result.
