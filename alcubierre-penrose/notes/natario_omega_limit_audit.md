# Natario omega-limit and angular-momentum audit

Adversarial verification note, 2026-08-03. This begins with the output of
*natario_global_exit_lemmas.md*: a future finite-proper-time exit satisfies

\[
t\longrightarrow\infty,\qquad
\Pi=|P|\longrightarrow\infty,
\qquad \boldsymbol x(t)\ \hbox{bounded}.
\tag{0.1}
\]

The exact projectivized equations are
\[
\boldsymbol x'=X+\beta m,
\qquad
m'=-(I-mm^T)(DX)^Tm,
\qquad
\beta={\Pi\over\sqrt{\Pi^2+1}},
\tag{0.2}
\]
with
\[
|m|=1,\qquad
X\cdot m={E\over\Pi}-\sqrt{1+\Pi^{-2}},
\qquad
|(\log\Pi)'|\leq B.
\tag{0.3}
\]

## Lemma 1: the omega-limit set is nonempty, compact, and connected

Put \(z(t)=(\boldsymbol x(t),m(t))\). By (0.1), the positive orbit has
compact closure in \(\mathbb R^3\times S^2\). For \(T\geq0\), let
\[
K_T=\overline{\{z(t):t\geq T\}}.
\]
Each \(K_T\) is nonempty and compact. It is connected because it is the
closure of the continuous image of the connected interval \([T,\infty)\).
The sets are nested, so
\[
\Omega=\bigcap_{T\geq0}K_T
\tag{1.1}
\]
is nonempty, compact, and connected.

## Lemma 2: every shifted limit is a complete limiting orbit

Let \(t_n\to\infty\). For every fixed \(A<\infty\), the logarithmic bound in
(0.3) gives
\[
\Pi(t_n+s)\geq \Pi(t_n)e^{-BA}\longrightarrow\infty
\quad\hbox{uniformly for }|s|\leq A.
\tag{2.1}
\]
Consequently \(\beta(t_n+s)\to1\) and \(E/\Pi(t_n+s)\to0\), also uniformly
on that interval.

The right sides of (0.2) are uniformly bounded on the compact orbit closure.
Thus the shifted curves
\[
z_n(s)=z(t_n+s),\qquad s\in[-t_n,\infty),
\]
are equi-Lipschitz on every bounded \(s\)-interval. Arzela--Ascoli, followed
by a diagonal subsequence, gives locally uniform convergence on all of
\(\mathbb R\) to a complete curve
\(z_\infty(s)=(\boldsymbol x_\infty,m_\infty)\).
Passing to the integral form of (0.2) proves that it solves
\[
\boldsymbol x_\infty'=X+m_\infty,
\qquad
m_\infty'=-(I-m_\infty m_\infty^T)(DX)^Tm_\infty,
\tag{2.2}
\]
and (0.3) gives
\[
|m_\infty|=1,\qquad X\cdot m_\infty=-1.
\tag{2.3}
\]
For every fixed \(s\), \(t_n+s\to\infty\), so
\(z_\infty(s)\in\Omega\). Hence the complete orbit lies in \(\Omega\), in
both time directions.

Conversely, for every \(z_*\in\Omega\) there is a sequence \(t_n\to\infty\)
with \(z(t_n)\to z_*\). The preceding construction therefore produces a
complete solution of (2.2)--(2.3), contained in \(\Omega\), through every
point of \(\Omega\).

The limiting constraint is dynamically consistent rather than an artifact of
subsequence convergence. If \(H=X\cdot m\), direct differentiation under
(2.2) gives
\[
H'=(1+H)m^T(DX)m,
\tag{2.4}
\]
while \(d|m|^2/ds=0\) on \(|m|=1\). Thus \(H=-1\) and the unit sphere are
invariant under the limiting flow.

## Lemma 3: angular momentum vanishes on every limiting orbit

For the stationary axisymmetric no-swirl Natario shift, the rotational
Killing field is
\[
K=-z\,\partial_y+y\,\partial_z.
\]
Because \(p_i=P_i\), its geodesic first integral is
\[
J=p(K)=yP_z-zP_y.
\tag{3.1}
\]
Consequently the exact orbit obeys
\[
y m_z-zm_y={J\over\Pi}\longrightarrow0.
\tag{3.2}
\]
The convergence is uniform on every shifted compact time interval by (2.1).
Every complete limiting orbit therefore satisfies
\[
y m_z-zm_y=0
\tag{3.3}
\]
at every time, not merely at its initial point.

This conclusion does not require \(J=0\) on the original timelike geodesic.
It also does not require an estimate on \(\varrho\Pi\), so no cylindrical
"boundary-layer" assertion is load-bearing.

## Lemma 4: one fixed meridional plane

Away from the symmetry axis, (3.3) says that the transverse position
\(q=(y,z)\) and transverse direction \(m_\perp=(m_y,m_z)\) are parallel.
They therefore lie in the meridional plane determined by \(q\).

The possible loophole is an axis crossing, where \(q=0\) and (3.3) imposes no
instantaneous restriction on \(m_\perp\). Fix such a state. If
\(m_\perp\ne0\), choose the meridional plane containing \(m_\perp\); if
\(m_\perp=0\), choose any meridional plane. Reflection across this plane fixes
both \(\boldsymbol x\) and \(m\) at that state. The Natario shift is
axisymmetric and has no azimuthal component, so the phase vector field in
(2.2) is equivariant under the same reflection. Uniqueness for the smooth
ODE implies that the entire maximal orbit, forward and backward, stays in the
reflection-fixed set. It therefore stays in that one meridional plane through
and after every axis crossing.

The same reflection argument applied at any off-axis state satisfying (3.3)
shows that its complete orbit remains in the meridional plane selected there.
Thus every complete orbit supplied by Lemma 2 is genuinely a planar
zero-angular-momentum orbit, globally in its limiting time.

## Step-3 conclusion

Every point of the compact connected omega-limit set \(\Omega\) lies on a
complete, spatially precompact orbit of
\[
\boldsymbol x'=X+m,\qquad
m'=-(I-mm^T)(DX)^Tm,\qquad
|m|=1,\quad X\cdot m=-1,
\tag{4.1}
\]
and each such orbit lies in one fixed meridional plane. The original exit may
have arbitrary finite conserved angular momentum \(J\); it disappears after
projectivization because \(\Pi\to\infty\).

The next proof stage may therefore apply the two-branch streamfunction
argument to every complete orbit in \(\Omega\). It still must prove, rather
than assume, that no nonconstant spatially precompact meridional orbit exists.

## Adversarial audit

1. **Only forward limits.** Shifting by \(t_n\to\infty\) gives domains
   \([-t_n,\infty)\); the diagonal construction therefore produces complete
   two-sided limiting orbits.
2. **Nonuniform high momentum.** The global logarithmic Lipschitz estimate
   upgrades \(\Pi(t_n)\to\infty\) to uniform divergence on every shifted
   compact interval.
3. **A limit that leaves the omega set backward in time.** For fixed positive
   or negative \(s\), \(t_n+s\to\infty\), so every point of the complete limit
   remains in \(\Omega\).
4. **Residual azimuthal motion.** Equation (3.2) converges uniformly on the
   shifted windows. At nonzero radius it forces \(m_\phi=0\).
5. **Changing planes at the axis.** Reflection equivariance and uniqueness,
   formulated in smooth Cartesian variables, fix a single plane through an
   axis crossing. Cylindrical-coordinate degeneracy is never used.
6. **An unjustified boundary-layer estimate.** No claim about
   \(\varrho\Pi\) is needed and none is made.
