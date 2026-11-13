# A genuine conformal completion of the regular boundary pieces

This constructs one explicit global positive conformal factor for the
actual capped metric, a regular conformal null-infinity boundary, and a
smooth positive-factor continuation through the cap. It does not assume
that the rescaled metric is flat. It is a conformal completion of the
regular parts, not a compactification of all ideal rider, rim and spatial
ends into one closed coordinate domain. Those ends remain unadjoined.
The requested complete global diagram is therefore still outstanding.

No manuscript edits or new diagrams are made here. The purpose is to
establish the metric that a proper diagram must represent.

## 1. Physical metric and one global conformal gauge

Use the previously fixed smooth bounded capped profile

\[
 g=-dt^2+[dx-v(x,y)dt]^2+dy^2,\qquad
 v=W(x^2+\psi(y)-1),\quad -2\leq v\leq0.
\]

Here psi(y) denotes the code's signed-y version of the paper's function
of rho squared. The laboratory coordinate is X=x+2t. Let

\[
 R^2=(x+2t)^2+y^2,\qquad
 \omega_\infty=(1+R^2)^{-1/2}.
\]

For the cap choose the following convenient, nonunique gauge:

\[
 \omega_f=
 \frac{1}{\sqrt{1+(1-x)^2e^{2t}}\sqrt{1+e^{-2t}}},\qquad
 \omega_r(t,x)=\omega_f(-t,-x),\qquad
 \omega_c=\omega_f+\omega_r.
\]

Both terms are smooth and positive at every finite event. Let S be the
infinitely flat step already used for W and put

\[
 \chi=1-S((x^2+y^2-4)/5),\qquad
 \Omega=\chi\omega_c+(1-\chi)\omega_\infty.
\]

Thus chi=1 on comoving radius <=2 and chi=0 at radius >=3. The entire
communication tube lies in chi=1; its spatial section satisfies
|x|<1, |y|<1.523. The cutoff choice is a conformal gauge choice, not an
additional physical bubble profile.

The actual rescaled metric on the whole original spacetime is

\[
 \widehat g=\Omega^2 g.
\]

It is Lorentzian and nondegenerate at every finite event:
det(g_hat)=-Omega^6 in these physical coordinates. Its light cones are
exactly those of the warp metric. In particular a future null vector is
(1,v+cos(alpha),sin(alpha)), not the Minkowski background null vector.
This is the essential correction to using the standard double-cone
metric inside the bubble.

The global factor is invariant under t->-t,x->-x. The past construction
is consequently the time reverse of the future one.

## 2. Ordinary future scri: explicit full 2+1 metric

In the exactly flat exterior introduce laboratory polar coordinates
X=R cos(theta), y=R sin(theta), and future hyperboloidal coordinates

\[
 \tau=t-\sqrt{1+R^2},\qquad r=R/(1+R),\qquad
 z=1-r,\qquad d=r^2+z^2.
\]

The radial coordinate is compact, 0<=r<1. At each finite tau,theta
point of r=1, the comoving distance from the bubble tends to infinity.
The cutoff is therefore identically zero in a neighborhood of that
ordinary-scri point, not merely small. Consequently Omega=omega_infinity
there, and

\[
 \widehat g=\frac1d\left[
 -z^2d\tau^2-2\frac r{\sqrt d}\,d\tau\,dr
 +\frac{dr^2}{d}+r^2d\theta^2\right].
\]

This is the full three-dimensional rescaled metric, not a 1+1 quotient.
The construction is the standard hyperboloidal/scri-fixing method,
specialized to the actual exact exterior. See Zenginoglu,
*Hyperboloidal foliations and scri-fixing*, sections III--IV,
https://arxiv.org/html/0712.4333.

At r=1 it has the regular limit

\[
 \widehat g\big|_{r=1}=-2d\tau\,dr+dr^2+d\theta^2.
\]

The determinant is -r^2/d^3, giving -1 at scri. The normal dr is null
there, and dOmega is nonzero because Omega=z/sqrt(d). Also
g_hat^{-1}(d tau,d tau)=-1: the exterior hyperboloidal time is temporal,
including at the boundary. No universal 45-degree rule is assigned to
the plotted coordinates.

For ordinary past scri use tau_minus=t+sqrt(1+R^2). The cross term
changes sign and the boundary metric is +2d tau_minus dr+dr^2+dtheta^2.
All finite advanced/retarded-time cuts and all angles are included.

These hyperboloidal time functions are exterior charts. They are not
asserted to be global temporal functions through the eternally moving
bubble. The global rescaling on finite events remains the Omega given
in section 1; physical t itself stays temporal throughout that interior.

## 3. Finite cap crossings: positive factor and regular metric

Use the existing front collar

\[
 p=P(x)e^t,\quad q=Q(x)e^{-t},\quad
 g=C(pq)\,dp\,dq+dy^2,
\]

where P(x)=s0(1-x)/(1+x), Q(x)=s0 exp[-h(x)], and C(0)=2 for the
normalization in the supplement. These formulas are used only where
the actual W is exactly affine and |y|<0.6.

For a finite crossing label p and sufficiently small |q|, chi=1. Put

\[
 k=q/Q(x),\qquad s=p(1+x)/s_0.
\]

Then the restriction of the SAME global conformal factor has the smooth
extension

\[
 \Omega=\frac1{\sqrt{(1+s^2)(1+k^2)}}
 +\frac{k}{\sqrt{[1+(1+x)^2k^2](1+k^2)}}.
\]

The signed k in the second term is important: this expression continues
smoothly through q=0. On the original side it agrees exactly with the
finite-t formula. Near any finite p the extension remains positive.
At the crossing,

\[
 \Omega(p,0,y)=\frac1{\sqrt{1+(2p/s_0)^2}}>0.
\]

Therefore

\[
 \widehat g=\Omega^2[C(pq)\,dp\,dq+dy^2]
\]

is smooth and Lorentzian across q=0, with determinant
-Omega^6 C(pq)^2/4. This is an ordinary interior crossing surface in
the extended physical spacetime, not conformal infinity. The rear cap
has the reflected construction. The aperture rim is excluded.

For each compact set of finite p,y cap labels, a sufficiently small
collar can be chosen so both the physical metric and this conformal
factor extend. Their union gives the open cap continuation already
proved Hausdorff in the manuscript. Cap neighborhoods have bounded
comoving spatial position, while finite-cut scri neighborhoods have
unbounded comoving position; they remain separated.

## 4. What has genuinely been completed

There is one rescaled metric on the full original spacetime, rather
than unrelated conformal choices in separate drawings. It extends
smoothly to all open ordinary future and past scri and through the
finite cap crossings. The zero-factor boundary consists of the stated
scri components; the cap crossings have positive factor and can be
included in the interior of the physical continuation.

The coordinate charts overlap and represent this one metric. Their
existence is not itself a single 3D coordinate embedding or a closed
global Penrose diagram. At scri the extension uses a curved rescaled
metric, with its actual angular and mixed terms retained.

On the central rider Omega=sech(t), so its infinite-time end still
requires an ideal-end attachment. The invariant corner audit prevents
claiming smooth pinched endpoints containing all fixed cap orbits.
This construction leaves those singular rider ends, the aperture rim
and the spatial corner unadjoined. It does not settle their topology
or construct a maximal physical continuation.

Thus the result is a proper regular-boundary **conformal completion**,
not yet the full all-ends compactification requested in the wider task.
No new global diagram is inferred merely from these formulas.

## Checks

Run `exploration/proper_conformal_completion.py`. Symbolic checks verify
the exterior determinant, the inverse time metric component, the null
scri normal and boundary metric. An independent 70-digit pullback in
the exact exterior agrees to below 5e-59. The cap factor agrees with
the global finite-event expression to below 9e-15; the metric is
nondegenerate on both sides of the crossing. Positivity is also checked
on interior samples and follows analytically from the formula.

Raw output: `output/global_2p1/proper_conformal_completion_check.json`.
The paper and saved PDF are unchanged.
