# Scalar-shift follow-up: generic maximality and the sharp exceptions

Working proof note, 2026-08-03.

## 1. Scope

Consider
\[
g=-dt^2+[dx-v(x,y,z)dt]^2+dy^2+dz^2
\]
on \(M=\mathbb R^4\). Assume:

1. \(v\) is smooth, bounded, and \(v\le0\);
2. \(v=-v_s\), with \(v_s>1\), outside a compact spatial set;
3. the full level set
   \[
   \Sigma=\{(x,y,z):v(x,y,z)=-1\}
   \]
   is compact and regular;
4. the stationary-geodesic locus
   \[
   \mathcal G=\{p\in\Sigma:v_y(p)=v_z(p)=0\}
   \]
   is finite;
5. at every \(p\in\mathcal G\), the transverse Hessian
   \(H_{AB}(p)=v_{AB}(p)\), \(A,B\in\{y,z\}\), is nonzero.

Condition 5 follows if the restriction of the height function \(x\) to
\(\Sigma\) is Morse. Indeed, near \(p\in\mathcal G\) the regular surface can be
written \(x=F(y,z)\), and if \(\kappa=-v_x(p)\ne0\), then
\[
F_{AB}(p)=\frac{H_{AB}(p)}{\kappa}.
\]

The exact-constant exterior is chosen because it makes the global escape
argument completely clean. A short-range tail can be added later under a
uniform integrable envelope on \(\nabla v\).

## 2. Candidate theorem

> **Generic compact scalar-shift maximality theorem.**
> Under assumptions 1--5, \((M,g)\) admits no proper Hausdorff \(C^2\)
> Lorentzian extension.

The proof is the nonradial version of the radial sech argument.

## 3. Global hyperbolicity

The inverse metric has \(g^{tt}=-1\), so \(t\) is temporal. Every
future-directed causal curve parametrized by \(t\) obeys
\[
\left|\frac{d\boldsymbol x}{dt}-v e_x\right|\le1,
\qquad
\left|\frac{d\boldsymbol x}{dt}\right|\le1+\|v\|_\infty.
\]
If its \(t\)-range had a finite endpoint, the spatial coordinates would
converge and the curve would extend. Hence every \(t=\mathrm{const.}\) slice is
Cauchy.

A proper \(C^2\) extension therefore supplies a unit timelike geodesic
\[
\gamma:[0,\tau_*)\to M,\qquad \tau_*<\infty,
\]
which is the restriction of a regular extension geodesic crossing a future or
past boundary. Treat the future case; the past case follows by applying the
same argument to the transformed scalar shift
\(v'(x,y,z)=v(-x,y,z)\).

## 4. First integrals

Let
\[
E=-p_t,\qquad P=p_x,\qquad Q_A=p_A.
\]
Then
\[
\dot t=E-vP,\qquad
\dot t^2=P^2+Q_AQ_A+1,
\]
and
\[
\dot P=-v_xP\dot t,\qquad
\dot Q_A=-v_AP\dot t.
\]

Finite \(t\) cannot be an exit: the causal speed bound gives a finite spatial
limit and, with \(t\) as parameter,
\[
\frac{dP}{dt}=-v_xP,\qquad
\frac{dQ_A}{dt}=-v_AP,
\]
the momenta remain bounded on the resulting compact coordinate set. Thus a
future exit has \(t\to+\infty\).

The sign of \(P\) is fixed. If \(P\le0\), then \(v\le0\) gives
\(0<\dot t\le E\), contradicting infinite \(t\) in finite proper time. Hence
\(P>0\). Since
\[
\frac{d\log P}{dt}=-v_x
\]
has bounded right-hand side, the same disjoint-interval argument used in the
radial proof gives
\[
P\to+\infty,\qquad \dot t\to+\infty.
\]

Define
\[
n=\frac{(P,Q_y,Q_z)}{\dot t}.
\]
Then
\[
|n|\to1,\qquad 1+vn_x=\frac E{\dot t}\to0.
\tag{4.1}
\]

## 5. Spatial infinity is impossible

In the constant exterior \(v=-v_s\) and \(\nabla v=0\). Hence \(P,Q_A\), and
\(\dot t\) are constant on every exterior segment, and the spatial trajectory
there is a straight line with constant \(t\)-velocity. Once a straight
trajectory crosses a sufficiently large sphere outward, it cannot return.
Therefore any unbounded spatial trajectory is eventually entirely in the
constant exterior. This contradicts \(P\to\infty\).

Thus every extension-supplied exit has bounded spatial image.

## 6. Every bounded exit approaches the stationary-geodesic locus

Equation (4.1) implies \(|v|\ge1-o(1)\). Also
\[
\frac{dx}{dt}
=v+\frac{P}{E-vP}
=v-\frac1v+O(P^{-1}).
\tag{6.1}
\]
The positive part of the right-hand side is \(O(P^{-1})\), and
\[
\int^\infty\frac{dt}{P}
=\int^{\tau_*}\frac{\dot t}{P}\,d\tau<\infty.
\]
Since \(x\) is bounded, (6.1) gives finite total variation and an \(x\)-limit.
It also forces \(v(t)\to-1\); otherwise the bounded coordinate speed and
smoothness of \(v\) would produce infinitely many intervals of uniform width
with a fixed amount of negative \(x\)-variation.

Consequently
\[
n_x\to1,\qquad n_A\to0,\qquad
\frac{d\boldsymbol x}{dt}\to0.
\tag{6.2}
\]

Put \(c_A=Q_A/P=n_A/n_x\). The exact ratio equation is now
\[
\frac{dc_A}{dt}=-v_A+v_xc_A.
\tag{6.3}
\]
Equation (6.2) gives \(c_A\to0\). On the bounded tail, the right-hand side of
(6.3) has bounded derivative and is uniformly continuous. A convergent
function with uniformly continuous derivative has derivative tending to zero,
so (6.3) yields
\[
v_A(\boldsymbol x(t))\to0.
\]
Together with \(v\to-1\), compactness gives
\[
\operatorname{dist}(\boldsymbol x(t),\mathcal G)\to0.
\]

Because \(\mathcal G\) is finite, choose disjoint neighborhoods of its points.
The continuous trajectory is eventually contained in their union and cannot
move between components without leaving that union. Hence it converges to one
point \(p\in\mathcal G\).

Regularity of \(\Sigma\) and \(v_A(p)=0\) give \(v_x(p)\ne0\). Since
\(P\to\infty\) and
\[
\frac{d\log P}{dt}\to-v_x(p),
\]
the future endpoint necessarily has \(v_x(p)<0\). Put
\(\kappa=-v_x(p)>0\).

## 7. Full-Hessian curvature contradiction

The trace is not enough at a saddle. Use the full tidal operator.

Let
\[
e_0=\partial_t+v\partial_x,\qquad
e_1=\partial_x,\qquad e_A=\partial_A
\]
be the stationary orthonormal frame. The unit tangent is
\[
u=\dot t\,(e_0+n_ie_i).
\]
By (6.2), \(n\to e_1\). Choose unit spatial vectors \(s_A\) perpendicular to
\(n\) with \(s_A\to e_A\). They are unit spacelike vectors orthogonal to \(u\).
At a stationary point \(p\in\mathcal G\),
\[
e_0+e_1=\partial_t
\qquad\text{because }v(p)=-1,
\]
and the established scalar-shift curvature formula gives
\[
R(\partial_t,e_A,\partial_t,e_B)=H_{AB}(p).
\]
Therefore
\[
\frac{1}{\dot t^2}R(u,s_A,u,s_B)\longrightarrow H_{AB}(p).
\tag{7.1}
\]

If a \(C^2\) extension existed, \(u\) would have a finite unit timelike limit.
The unit spheres in its orthogonal rest spaces form a compact family in a
regular extension chart, so the components
\(R(u,s_A,u,s_B)\) would be uniformly bounded. Equation (7.1), together with
\(\dot t\to\infty\) and \(H_{AB}(p)\ne0\), is a contradiction.

This proves future inextendibility. Applying the argument to
\((t,x)\mapsto(-t,-x)\) proves the past case and completes the theorem.

## 8. Curvature and energy: tensor versus trace

At a stationary finite-affine generator,
\[
R_{KAKB}=q^2H_{AB},\qquad
8\pi T_{KK}=q^2\operatorname{tr}H.
\]

The same tensor has a third interpretation. Linearize the zero-energy
high-momentum ray system at the stationary orbit, using transverse position
\(\eta^A\) and direction angle \(\theta_A=m_A\). With
\(\kappa=-v_x(p)>0\),
\[
\frac d{dt}
\begin{pmatrix}\eta\\ \theta\end{pmatrix}
=
\begin{pmatrix}
0&I\\-H&-\kappa I
\end{pmatrix}
\begin{pmatrix}\eta\\ \theta\end{pmatrix}.
\tag{8.1}
\]
For an eigenvalue \(h\) of \(H\), the two transverse characteristic exponents
obey
\[
\lambda^2+\kappa\lambda+h=0,
\qquad
\lambda_+\lambda_-=h.
\tag{8.2}
\]
Thus \(H\) is not merely a curvature coefficient: it is the stiffness matrix
of the transverse horizon-ray dynamics. Its eigenvalues are the products of
the stable/unstable exponents, while its trace is the sum of those products and
is exactly the leading null source. At a curved support point, a negative
eigenvalue produces a saddle direction whose stable branch is the tuned ray
approaching the finite-affine generator.

Thus:

- \(C^2\) inextendibility is controlled by the full transverse Hessian;
- the divergent null source is controlled by its trace;
- the transverse stability of the horizon ray is controlled by the same full
  Hessian through (8.1);
- at a semidefinite support point, \(H\ne0\) implies
  \(\operatorname{tr}H\ne0\), so the two obstructions coincide;
- at a saddle, \(H\ne0\) can coexist with \(\operatorname{tr}H=0\), and the
  curvature obstruction is strictly stronger.

For a compact component \(\Sigma\), a front support point is automatically in
\(\mathcal G\). If the height function is Morse, its transverse Hessian is
negative definite there. With the front sign convention,
\[
\operatorname{tr}H<0,
\]
so the same mean-curvature coefficient gives the PP Ricci blow-up and the
unbounded negative \(T_{KK}\) along that support generator.

## 9. The three adversarial geometries

### 9.1 Quartic support

Let the wall be locally
\[
x=F(y,z)=-y^4-z^4.
\]
The origin is a strict support maximum, but
\[
F_{AB}(0)=H_{AB}(0)=0.
\]
Neither the PP Hessian test nor the Ricci-trace test detects the exact
stationary generator. This disproves the inference
\[
H_{AB}(p)=0\quad\Longrightarrow\quad\text{locally planar wall}.
\]
The natural endpoint chart is singular on paths approaching the generator
from nonproduct points, but converting that fact into invariant
inextendibility requires the stationary-flow rigidity lemma discussed below.

### 9.2 Tracefree saddle

Let
\[
F(y,z)=-y^2+z^2.
\]
Then \(H_{AB}\ne0\) but \(\operatorname{tr}H=0\). Equation (7.1) gives the
\(C^2\) obstruction, while the leading \(T_{KK}\) divergence cancels.
Nonconvex compact surfaces can have saddle critical points of the height
function, so this is a real obstruction to a universal one-scalar theorem.

### 9.3 Exact planar cap

Suppose on an open transverse disk \(D\) the metric is an exact product,
\[
g=g_{1+1}(t,x)+dy^2+dz^2,
\]
and the simple \(1+1\) horizon has its usual regular extension
\(\widetilde N\). For any smaller disk \(D_0\Subset D\), the product patch
\[
\widetilde N\times D_0
\]
can be glued to \(M\) along their common open product region. After shrinking
the overlap, this gives a proper Hausdorff local \(C^2\) extension through the
interior cap generators while adding no rim point.

Therefore a compact bubble with an exact open product cap need not be wholly
\(C^2\)-inextendible. What can still be true is that no single extension
resolves every generator, because the cap-edge generators are not interior
points of the product locus.

## 10. Superseded stationary-flow rigidity attempt

> **Correction.** The argument in this section overstates Sbierski's
> anchored-extension theorem. The extended identification is an isometry on
> the original one-sided subgraph and its boundary, but need not be an isometry
> on the freely chosen far side of the extension. Consequently it does not
> furnish the two-sided local-isometry germs assumed below, even for a smooth
> extension. The Baire argument in the global extension-rigidity note, Section
> 10, proves that genuine \(C^2\) germs would share a common domain; the
> unresolved premise is obtaining those germs from one-sided boundary data.
> The local flow-rigidity and no-simultaneous-resolution theorems stated below
> are withdrawn.

The boundary-one-jet part of the parameter-uniformity gap disappears once
"resolves a generator" is given its required geodesic meaning. A separate
common-domain issue for the resulting isometry germs is isolated below.

> **Definition (regular resolution).** A \(C^2\) extension regularly resolves
> an incomplete finite-affine null geodesic \(\gamma:[0,\lambda_*)\to M\) if
> \(\iota\circ\gamma\) continues through \(\lambda_*\) as a \(C^1\), affinely
> parametrized null geodesic with nonzero tangent.

This is stronger than merely assigning the image curve a topological endpoint,
but it is precisely what it means to extend the geodesic. In a \(C^2\) metric,
parallel transport along the continued curve is a regular linear ODE. Hence a
parallel null frame \((K,N,Y,Z)\) along \(\gamma\) has a finite nondegenerate
limit at the endpoint whenever \(\gamma\) is regularly resolved.

Let \(\phi_s\) be stationary time translation, and let \(p\) be the endpoint of
a regularly resolved stationary generator. The two embeddings
\[
\iota,\qquad \iota\circ\phi_s
\]
are anchored by the same curve, because \(\phi_s\gamma\) is an affine
reparametrization of the same stationary orbit. Sbierski's anchored-extension
uniqueness theorem therefore extends each fixed \(\phi_s\) to a local isometry
\(\Phi_s\) fixing \(p\). For \(C^2\) extensions the boundary identification has
the higher regularity supplied by Lemma 5.21 of arXiv:2208.07752.

At a scalar-shift stationary generator put \(\kappa=|v_x|>0\), with the affine
orientation chosen toward the endpoint. Along the orbit one may take
\[
K=q\,\partial_t,\qquad q(t+s)=e^{\kappa s}q(t).
\]
A direct connection calculation at \(v=-1,\ v_A=0\) shows that the coordinate
screen vectors \(\partial_y,\partial_z\) are parallel along the orbit. The
complementary parallel null vector scales inversely to \(K\). Passing to the
finite endpoint frame therefore gives
\[
L_s=(d\Phi_s)_p:\qquad
L_sK=e^{-\kappa s}K,\quad
L_sN=e^{\kappa s}N,\quad
L_sY=Y,\quad L_sZ=Z.
\tag{10.1}
\]
Thus the boundary one-jets are explicitly a smoothly parameterized pure boost.
There is, however, one last common-domain issue: anchored uniqueness supplies
an isometry *germ* for every fixed \(s\), not explicitly a common neighborhood
on which all small \(s\) act.

At smooth regularity this is handled by the standard finite-type fact that the
local-isometry pseudogroup of a pseudo-Riemannian metric is a Lie pseudogroup.
The one-parameter subgroup of germs represented by (10.1) then has common
local representatives. Isometries preserve affinely parametrized geodesics, so
on a common normal neighborhood
\[
\Phi_s=\exp_p\circ L_s\circ\exp_p^{-1}.
\tag{10.2}
\]
Equations (10.1)--(10.2) give smooth dependence on \(s\) and the local group law.
In exponential coordinates \((U,V,y,z)\), the action is
\[
(U,V,y,z)\longmapsto
(e^{-\kappa s}U,e^{\kappa s}V,y,z).
\]
Boost invariance and \(C^2\) regularity force
\[
g_{UU}=V^2a,\quad g_{VV}=U^2b,\quad g_{UV}=c,
\quad g_{UA}=Vd_A,\quad g_{VA}=Ue_A,
\]
where the coefficients are functions of \((UV,y,z)\), and nondegeneracy gives
\(c(0,0,0)\ne0\). For the extended Killing field
\(\widetilde\xi=\kappa(V\partial_V-U\partial_U)\),
\[
\widetilde g(\widetilde\xi,\widetilde\xi)
=\kappa^2UV\{UV(a+b)-2c\}.
\tag{10.3}
\]
After shrinking the neighborhood, the braced factor is nonzero. The local
zero set is exactly \(U=0\) or \(V=0\), and each branch is a Killing horizon.

> **Withdrawn local flow-rigidity claim.** If a
> smooth extension regularly resolves a simple scalar-shift stationary
> generator, then that generator's spatial point is an interior point,
> relative to \(\Sigma\), of the stationary-geodesic locus \(\mathcal G\).
> The same conclusion holds for a \(C^2\) extension provided the following
> low-regularity germ-integration statement holds: a \(C^2\) Lorentz metric's
> smooth one-parameter subgroup of local-isometry one-jets at a fixed point is
> represented by a common local \(C^1\) isometry action.

Indeed, the preimage of the normal neighborhood contains an ordinary open
neighborhood of every sufficiently late point of the orbit. Equation (10.3)
makes every nearby original point of \(\Sigma\) part of a Killing horizon and
therefore a stationary geodesic point.

This gives the sharp global statement that survives the exact-cap example.

> **Withdrawn no-simultaneous-resolution claim.** Let
> \(\Sigma\) be a connected compact regular component of \(\{v=-1\}\) in a
> scalar-shift spacetime. No single Hausdorff smooth extension regularly
> resolves every finite-affine stationary generator over \(\Sigma\). The
> \(C^2\) statement follows from the low-regularity germ-integration lemma just
> stated.

The proof is topological. The set
\[
\mathcal G=\{p\in\Sigma:v_y(p)=v_z(p)=0\}
\]
is closed and nonempty, since front and rear support points belong to it.
It is not all of \(\Sigma\): otherwise the normal of the connected closed
surface would everywhere be parallel to the fixed \(x\)-direction, which is
impossible. Hence \(\partial_\Sigma\mathcal G\ne\varnothing\). A point in that
boundary belongs to \(\mathcal G\) but is not an interior point, contradicting
the local flow-rigidity lemma if one extension resolves every generator.

The theorem deliberately concerns regular geodesic resolution. Whether an
arbitrary \(C^2\) extension can attach a mere endpoint at which the affine
tangent has no nonzero limit is a different, weaker boundary question and is
not needed for the maximal-extension interpretation. Exact open product caps
remain genuine local extensions: their interior generators are resolved, but
their rim supplies the non-interior members that cannot all be resolved in the
same extension.

## 11. Result ladder after the adversarial audit

1. **Radial family theorem:** complete for a unique simple root and a compact
   or uniformly short-range tail.
2. **Generic compact scalar-shift theorem:** complete under an exact-constant
   exterior and finite nonzero-Hessian stationary locus; the Morse hypothesis
   is a clean sufficient condition.
3. **Degenerate local rigidity:** still open at an infinitely flat nonproduct
   cap rim. The common-domain lemma for genuine \(C^2\) isometry germs is
   complete, but anchored uniqueness supplies only one-sided isometry data.
4. **All compact scalar-shift bubbles:** full inextendibility is false with
   exact open product caps. No-simultaneous resolution of the entire generator
   family remains plausible but is not proved, at smooth or \(C^2\)
   regularity.
5. **Natario:** global \(C^2\) maximality is complete for the monotone-wall
   profile class in the dedicated Natario maximality note. The strict
   streamfunction-maximum lemma eliminates branch-switching cycles, and
   \(J/|P|\to0\) eliminates the nonzero-angular-momentum limit.
