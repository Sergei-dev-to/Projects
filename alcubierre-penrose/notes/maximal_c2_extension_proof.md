# Maximal C2 extension of the eternal Alcubierre spacetime

Working proof note, 2026-08-03.

## Theorem

Let
\[
g=-dt^2+[dx-v(r)dt]^2+dy^2+dz^2,
\qquad r=(x^2+y^2+z^2)^{1/2},
\]
where \(v(r)=v_s[f(r)-1]\), \(v_s>1\), and the profile used in the paper is
smooth, strictly decreasing for \(r>0\), has a simple root \(v(R_F)=-1\), and
approaches the constant \(-v_s\) with its derivatives sufficiently rapidly.
Then the eternal four-dimensional Alcubierre spacetime
\((\mathbb R^4,g)\) has no proper Hausdorff \(C^2\) Lorentzian extension.
Consequently the computed three-region conformal diamond is the maximal
Hausdorff \(C^2\) extension of the eternal spacetime. The larger continuation
of the axial \(1+1\) quotient is not a continuation of the four-dimensional
metric.

The proof has four steps.

## 1. Global hyperbolicity

The inverse metric has \(g^{tt}=-1\), so \(t\) is a smooth temporal function.
For every future causal curve, parametrized by \(t\),
\[
\left|\frac{d\boldsymbol x}{dt}-v(r)e_x\right|\le1,
\]
and hence
\[
\left|\frac{d\boldsymbol x}{dt}\right|\le1+v_s.
\]
If an inextendible causal curve had a finite upper or lower endpoint for its
\(t\)-range, its spatial coordinates would be Cauchy and converge to a finite
point of \(\mathbb R^3\); the curve would then extend in the smooth spacetime,
a contradiction. Thus \(t\) ranges from \(-\infty\) to \(+\infty\) on every
inextendible causal curve and every slice \(t=\mathrm{constant}\) is Cauchy.
The spacetime is globally hyperbolic.

## 2. What any extension would supply

Assume that a proper Hausdorff \(C^2\) extension
\(\iota:M\hookrightarrow\widetilde M\) exists. The standard future/past
boundary theorem for extensions of globally hyperbolic spacetimes supplies,
after reversing time if necessary, a future-directed unit timelike geodesic
\[
\gamma:[0,\tau_*)\longrightarrow M,
\qquad \tau_*<\infty,
\]
such that \(\iota\circ\gamma\) has a regular endpoint in \(\widetilde M\).
Because the extension is \(C^2\), the unit tangent \(u=\dot\gamma\) and a
parallel frame have finite limits there, and the continuous Ricci tensor must
satisfy
\[
R_{ab}u^au^b=O(1).
\tag{2.1}
\]

It remains to show that no such exit geodesic exists.

## 3. Exhaustion of finite-proper-time exits

Let
\[
E=-p_t,
\qquad P=p_x,
\qquad Q_A=p_A \quad(A=y,z).
\]
Stationarity and unit normalization give
\[
\dot t=E-vP,
\qquad
\dot t^2=P^2+Q_AQ_A+1,
\tag{3.1}
\]
while the Hamilton equations give
\[
\dot P=-v_xP\dot t,
\qquad
\dot Q_A=-v_AP\dot t.
\tag{3.2}
\]

### 3.1 Finite Killing time is not an exit

If \(t\) remains bounded as \(\tau\to\tau_*\), the causal speed estimate in
Step 1 makes the spatial coordinates converge. Using \(t\) as parameter,
Eq. (3.2) becomes
\[
\frac{dP}{dt}=-v_xP,
\qquad
\frac{dQ_A}{dt}=-v_AP.
\]
On the resulting compact coordinate set these linear equations keep
\((P,Q_A)\) bounded. The geodesic data therefore converge in \(TM\), and the
smooth geodesic equation extends \(\gamma\) past \(\tau_*\), a contradiction.
Hence an exit requires \(t\to+\infty\) (or, after time reversal,
\(t\to-\infty\)).

### 3.2 Spatial infinity is not an exit

Because \(v\le0\), Eq. (3.1) shows that a future exit with unbounded
\(\dot t\) must have \(P>0\). The sign of \(P\) is fixed by (3.2). Moreover,
if \(P\) returned below a fixed bound infinitely often, the bounded logarithmic
derivative
\[
\frac{d\log P}{dt}=-v_x
\]
would give infinitely many \(t\)-intervals of uniform positive width on which
\(\dot t=E-vP\) is bounded. Each contributes a fixed positive amount to
\(d\tau=dt/\dot t\), contradicting \(\tau_*<\infty\). Hence
\[
P\longrightarrow+\infty,
\qquad
\dot t=E-vP\longrightarrow+\infty.
\tag{3.3}
\]

Define
\[
n=(P,Q_y,Q_z)/\dot t.
\]
Then \(|n|\to1\) and, after renumbering subsequent equations,
\[
1+vn_x=E/\dot t\to0.
\tag{3.4}
\]
In the asymptotic region \(|v|>1\), the longitudinal coordinate velocity has
\[
\frac{dx}{dt}=v+n_x\longrightarrow v-\frac1v\ne0,
\]
and is uniformly negative once \(r\) is large. Thus escape through
\(x\to+\infty\) is impossible, while escape through \(x\to-\infty\) makes
\(v_x=v_r x/r>0\) and therefore makes \(P\) decrease rather than diverge.

The remaining possibility is transverse escape with bounded \(x\). Put
\(\rho=(y^2+z^2)^{1/2}\). The axial angular momentum
\[
L=yQ_z-zQ_y
\]
is conserved. If \(Q_\rho=(yQ_y+zQ_z)/\rho\) and
\(a(r)=-v_r(r)>0\), the transverse equations give
\[
\frac{dQ_\rho}{d\tau}
=\frac{a(r)\rho}{r}P\dot t+\frac{L^2}{\rho^3}\ge0.
\]
Thus an unbounded transverse trajectory eventually has \(Q_\rho>0\) and
\(\rho\to\infty\). Its tangential momentum is \(L/\rho\), so (3.4) and the
normalization imply
\[
\frac{Q_\rho}{\dot t}\longrightarrow\sqrt{1-v_s^{-2}}>0.
\]
Consequently \(d\rho/dt\) is eventually bounded below and
\(r(t)\ge ct-O(1)\). Since the sech tail has
\(a(r)\le Ce^{-r/a}\) and \(x\) is bounded,
\[
\left|\frac{d\log P}{dt}\right|
=\frac{a(r)|x|}{r}\le C'e^{-ct/a}.
\]
The logarithm of \(P\) therefore has a finite limit, contradicting (3.3).
No finite-proper-time exit reaches spatial infinity.

### 3.3 The only finite spatial limits are the axial v=-1 points

The spatial image is therefore bounded. By (3.3)--(3.4), the tail lies in the
superluminal region \(|v|\ge1-o(1)\). On this tail
\[
\frac{dx}{dt}=v+\frac{P}{E-vP}
  =v-\frac1v+O(P^{-1}).
\]
The leading term is strictly negative away from \(v=-1\). Its possible
positive part is \(O(P^{-1})\), which is integrable because
\[
\int^\infty\frac{dt}{P(t)}
 \asymp\int^{\tau_*}d\tau<\infty
\]
on \(|v|\ge1-o(1)\). Thus \(x(t)\) has a limit, and
every spatial accumulation point lies on \(v=-1\). Indeed, if \(|v(p)|<1\),
Eq. (3.4) is impossible because \(|n_x|\le1\). If \(|v(p)|>1\), the limiting
longitudinal velocity is bounded away from zero and \(p\) cannot be an
accumulation point. Therefore every accumulation point has \(v(p)=-1\), and
(3.4) gives
\[
n_x\to1,
\qquad n_A\to0,
\qquad
\frac{d\boldsymbol x}{dt}=ve_x+n\to0.
\tag{3.5}
\]

Put \(c_A=Q_A/P\) and \(a(r)=-v_r(r)>0\). The equations give the exact
transverse system
\[
\frac{dc_A}{dt}=\frac{a(r)}r\,[y_A-xc_A],
\qquad
\frac{dy_A}{dt}=\frac{c_AP}{E-vP}.
\tag{3.6}
\]
Equation (3.5) says \(c_A\to0\). The right sides of (3.6) are uniformly
continuous on the bounded tail. Hence \(dc_A/dt\to0\), which forces
\(y_A\to0\). Since \(r\to R_F\), one has \(|x|\to R_F\). The rear choice
\(x\to-R_F\) would give
\(d(\log P)/dt=a(r)x/r\to-\kappa\), contradicting \(P\to\infty\). Therefore
the spatial coordinates converge to the front axial point
\[
p_F=(R_F,0,0),
\qquad v=-1,\quad v_x=-\kappa,\quad v_A=0.
\tag{3.7}
\]

Equivalently, the stronger logarithmic contradiction already established in
`paper/main.tex` applies if one assumes convergence to a nonaxial point:
\(|P|\asymp(\tau_* -\tau)^{-1}\) and
\(y^A=c_A\log(\tau_*-\tau)+O(1)\).

The time-reversed past exit can only approach the rear axial point.

## 4. Ricci blow-up at every remaining exit

At the front point the transverse Hessian is
\[
v_{yy}=v_{zz}=-\frac{\kappa}{R_F}.
\]
The curvature calculation in `paper/main.tex` gives
\[
R_{tt}=R_{ab}(\partial_t)^a(\partial_t)^b
=v_{yy}+v_{zz}
=-\frac{2\kappa}{R_F}\ne0
\qquad\text{at }p_F.
\tag{4.1}
\]
Here \(R_{tt}=G_{tt}\) because \(\partial_t\) is null at \(v=-1\).

By (3.5), the unit tangent of every putative future exit satisfies
\[
u=\dot t\,[\partial_t+o(1)],
\qquad \dot t\to\infty.
\]
Continuity of the stationary-coordinate Ricci tensor at \(p_F\) and (4.1)
therefore give
\[
R_{ab}u^au^b
=\dot t^{\,2}
  R\bigl(\partial_t+o(1),\partial_t+o(1)\bigr)
\sim-\frac{2\kappa}{R_F}\dot t^{\,2},
\tag{4.2}
\]
which is unbounded. This contradicts the necessary boundedness (2.1) in a
\(C^2\) extension. The rear endpoint gives the time-reversed contradiction.

No future or past boundary point of a proper \(C^2\) extension can therefore
exist. The assumed extension does not exist, and \((M,g)\) is Hausdorff
\(C^2\)-inextendible.

## Proof audit

The argument upgrades the paper's local corner obstruction to global
maximality by adding two ingredients:

1. global hyperbolicity, which turns any proper extension into a finite-time
   timelike exit geodesic;
2. exhaustion of those exits using the stationary first integrals.

The short-range argument in Section 3.2 is stated for the exponential sech
tail and now uses conserved axial angular momentum to make the comparison
estimate \(r(t)\ge ct-O(1)\) explicit. For a compactly supported shape function
the same step simplifies further because the exterior is exactly
constant-shift Minkowski.
