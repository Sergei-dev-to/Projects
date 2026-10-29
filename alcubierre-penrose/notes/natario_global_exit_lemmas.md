# Natario global-exit lemmas

Adversarial verification note, 2026-08-03. This isolates everything needed
before the Natario-specific omega-limit and streamfunction arguments.

Consider the stationary unit-lapse flat-slice metric
\[
g=-dt^2+\delta_{ij}(dx^i-X^i(\boldsymbol x)dt)
                    (dx^j-X^j(\boldsymbol x)dt)
\tag{1.1}
\]
on \(M=\mathbb R^4\). Assume \(X\) is smooth and bounded and, for some
\(v_s>1\),
\[
|X+v_se_x|+|DX|\leq Ce^{-\sigma r}
\tag{1.2}
\]
outside a ball. The exactly constant exterior is included.

## Lemma 1: global hyperbolicity

The inverse metric satisfies
\[
g^{-1}(dt,dt)=-1,
\]
so \(t\) is temporal. Parametrize a future causal curve by \(t\). Its causal
inequality is exactly
\[
\left|\frac{d\boldsymbol x}{dt}-X(\boldsymbol x)\right|\leq1,
\tag{1.3}
\]
and hence
\[
\left|\frac{d\boldsymbol x}{dt}\right|
\leq \|X\|_\infty+1=:V.
\tag{1.4}
\]
If an inextendible causal curve had a finite endpoint \(t_*\) in its
\(t\)-range, (1.4) would make \(\boldsymbol x(t)\) Cauchy and therefore
convergent to a point of \(\mathbb R^3\). The curve could be continued from
\((t_*,\boldsymbol x_*)\), a contradiction. Thus \(t\) takes all real values
on every inextendible causal curve, every \(t=\mathrm{constant}\) slice is
Cauchy, and \(M\) is globally hyperbolic.

## Lemma 2: what the extension theorem actually supplies

Galloway--Ling--Sbierski, Theorem 2, states that a smooth globally hyperbolic
spacetime with a \(C^0\) extension contains a timelike geodesic with an
endpoint on the extension boundary. Suppose first that the extension has a
future boundary. Applied to a putative \(C^2\) extension, the future-boundary
version of their construction gives
\[
\gamma:[0,\tau_*)\to M,\qquad \tau_*<\infty,
\tag{2.1}
\]
with a future boundary endpoint \(q\). Its proper-time length is finite: the
curve's final segment lies in one of the coordinate neighborhoods in which
every causal curve has uniformly bounded Lorentzian length.

The endpoint-tangent issue needs a separate local argument; it must not simply
be assumed from (2.1). In the proof of the cited theorem, the geodesic is the
physical-spacetime portion of a causal maximizer in a small extension
neighborhood. Let \(q\) be its first boundary point. Choose a geodesically
convex normal neighborhood \(W\) of \(q\) in the \(C^2\) extension, contained
in that small neighborhood, and take a point \(p\) sufficiently far along
\(\gamma\) that its remaining segment lies in \(W\). The segment from \(p\)
to \(q\), with \(q\) appended, is still maximizing: any longer competitor in
\(W\) would also contradict maximality in the original neighborhood. In a
smooth convex normal neighborhood a positive-length causal maximizer is the
unique timelike geodesic from \(p\) to \(q\). Consequently the final part of
\(\gamma\) is the restriction of a \(C^1\) affinely parametrized extension
geodesic, and its unit tangent has a finite nonzero limit at \(q\).

Since the extension Ricci tensor is continuous,
\[
\operatorname{Ric}(\dot\gamma,\dot\gamma)=O(1)
\quad\hbox{as}\quad\tau\to\tau_*.
\tag{2.2}
\]
This is the quantity the final curvature calculation must contradict.

## Lemma 3: exact stationary geodesic system

Let
\[
P_i=\dot x_i-X_i\dot t,\qquad E=-p_t.
\]
The Lagrangian of (1.1) gives
\[
\dot t=E-X\cdot P,\qquad
\dot t^2=|P|^2+1,
\tag{3.1}
\]
\[
\dot{\boldsymbol x}=P+X\dot t,\qquad
\dot P_i=-\dot t\,(\partial_iX^j)P_j.
\tag{3.2}
\]
Future orientation gives \(\dot t>0\). With \(t\) as parameter, put
\[
\Pi=|P|,\qquad m=P/\Pi,\qquad
\beta=\frac{\Pi}{\sqrt{\Pi^2+1}}.
\]
Whenever \(P\ne0\),
\[
\boldsymbol x'=X+\beta m,
\tag{3.3}
\]
\[
P'=-(DX)^TP,
\tag{3.4}
\]
\[
m'=-(I-mm^T)(DX)^Tm,
\tag{3.5}
\]
\[
(\log\Pi)'=-m^T(DX)m,
\tag{3.6}
\]
and
\[
X\cdot m=\frac E\Pi-\sqrt{1+\Pi^{-2}}.
\tag{3.7}
\]
These identities are exact for a unit timelike geodesic. No high-frequency
approximation has entered yet.

## Lemma 4: finite Killing time is impossible

Suppose the exit had \(t\to t_*<\infty\). Equation (1.4) would give a finite
spatial limit and place the final coordinate segment in a compact set. On
that set \(DX\) is bounded, so the linear equation (3.4) and Gronwall's
inequality keep \(P\) bounded on the finite \(t\)-interval. Equation (3.4)
then also makes \(P(t)\) Cauchy as \(t\to t_*\). Equations (3.1)--(3.3) give a
finite limiting geodesic datum in \(TM\), and the smooth geodesic equation
continues it inside \(M\). This contradicts the boundary endpoint. Hence
\[
t\longrightarrow+\infty.
\tag{4.1}
\]

## Lemma 5: momentum diverges uniformly

First dispose of \(P=0\). Since (3.4) is homogeneous and linear, if \(P\)
vanishes once it vanishes identically. Then \(\dot t=1\), so (4.1) would
require infinite proper time. Thus \(P\ne0\) on a finite-proper-time exit.

Let
\[
B=\sup_{\mathbb R^3}|DX|<\infty.
\]
Equation (3.6) gives
\[
|(\log\Pi)'|\leq B.
\tag{5.1}
\]
Finite remaining proper time is
\[
\int^{\infty}\frac{dt}{\sqrt{\Pi(t)^2+1}}<\infty.
\tag{5.2}
\]
If \(\Pi\not\to\infty\), there are \(M<\infty\) and arbitrarily large times
\(t_n\) with \(\Pi(t_n)\leq M\). Choose a subsequence whose unit intervals are
disjoint. By (5.1),
\[
\Pi(t)\leq Me^B\qquad (|t-t_n|\leq1),
\]
so each interval contributes at least
\[
\frac{2}{\sqrt{M^2e^{2B}+1}}
\]
to (5.2), a contradiction. Therefore
\[
\Pi(t)\longrightarrow\infty
\tag{5.3}
\]
without passing to a subsequence. Equations (3.3) and (3.7) consequently give
\[
\beta\to1,\qquad X\cdot m\to-1.
\tag{5.4}
\]

## Lemma 6: spatial infinity is impossible

Choose
\[
c< v_s-\frac1{v_s}.
\]
By (1.2), (5.3), and (3.7), there are \(T,R\) such that whenever
\(t\geq T\) and \(r\geq R\),
\[
\left|m_x-\frac1{v_s}\right|
\]
is sufficiently small and
\[
x'=X^x+\beta m_x\leq-c<0.
\tag{6.1}
\]
This estimate is uniform in the transverse direction of \(m\).

Consider a connected component \([t_1,t_2]\) of
\[
\{t\geq T:r(t)\geq R\}
\]
which enters and later returns through \(r=R\). At both endpoints
\(-R\leq x\leq R\), while (6.1) gives
\[
c(t_2-t_1)\leq x(t_1)-x(t_2)\leq2R.
\tag{6.2}
\]
Thus every returning exterior excursion has duration at most \(2R/c\).
Equation (1.4) then bounds its radius by
\[
r(t)\leq R+\frac{2RV}{c}.
\tag{6.3}
\]
This argument deliberately does not assume that \(r\) is monotone.

If the spatial trajectory were unbounded, (6.3) implies that one exterior
component must be nonreturning: \(r(t)\geq R\) for all sufficiently large
\(t\). Equation (6.1) then yields
\[
x(t)\leq x(T_0)-c(t-T_0),\qquad
r(t)\geq c t-O(1).
\tag{6.4}
\]
For an exactly constant exterior, (3.4) makes \(P\) constant after \(T_0\),
contradicting (5.3). Under the exponential alternative (1.2),
\[
\int_{T_0}^{\infty}|DX(\boldsymbol x(t))|\,dt<\infty.
\]
Equation (3.6) makes \(\log\Pi\) converge to a finite value, again
contradicting (5.3). Therefore
\[
\{\boldsymbol x(t):t\geq0\}\quad\hbox{is bounded}.
\tag{6.5}
\]

## Step-2 conclusion

Every future boundary of a proper \(C^2\) extension would supply a unit
timelike geodesic satisfying all of
\[
\tau_*<\infty,\qquad
t\to+\infty,\qquad
\Pi\to\infty,\qquad
\boldsymbol x(t)\ \hbox{bounded},
\tag{7.1}
\]
while its extension tangent and Ricci contraction remain finite. The next
stage may therefore work entirely on the compact spatial phase space and take
time-shifted high-momentum limits.

## Adversarial audit

The rewritten proof closes the following possible loopholes.

1. **A merely topological geodesic endpoint.** The extension geodesic is tied
   to the normal-neighborhood maximizer in the proof of the boundary theorem;
   (2.2) is not inferred from endpoint convergence alone.
2. **Zero spatial momentum.** Homogeneity of (3.4) makes that solution
   identically comoving and therefore infinite in proper time.
3. **Narrow momentum dips.** The global logarithmic Lipschitz bound (5.1)
   turns every dip into a time interval of uniform width.
4. **Repeated large-radius returns.** The longitudinal estimate bounds the
   duration and radius of every returning excursion; no radial monotonicity is
   assumed.
5. **Slow escape through an exponential tail.** A nonreturning excursion has
   linear negative \(x\)-drift, making \(DX\) integrable and momentum bounded.

No Natario-specific streamfunction, zero-angular-momentum assumption, or
curvature sign is used in these lemmas. A past boundary is the time-dual
case; for the Natario profile it is carried to the future case by the
reflection used in the final maximality proof.

## Reference

G. J. Galloway, E. Ling, and J. Sbierski,
[*Timelike completeness as an obstruction to \(C^0\)-extensions*](https://arxiv.org/abs/1704.00353),
Commun. Math. Phys. **359** (2018), 937--949. Theorem 2 is the endpoint
statement; the maximizer is constructed in the proof of Theorem 3.3.
