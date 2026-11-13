# Focusing the global construction on the stationary horizons

The whole conformal completion is not required to determine the rider's
communication horizons. For the rounded example this reduces to a scalar
ODE, with a causal argument selecting its branch. This note concerns the
original stationary spacetime, not the Cauchy horizons of a chosen larger
continuation. No manuscript edits are made here.

## 1. Definitions that select the relevant null surfaces

Use the signed meridional metric

\[
 g_3=-dt^2+[dx-v(x,y)dt]^2+dy^2,\qquad
 v=2\operatorname{sech}\sqrt{x^2+y^2}-2.
\]

Let gamma be the entire central rider (t,0,0), -infinity<t<infinity. Define

\[
 H_{send}=\partial I^+(\gamma),\qquad
 H_{receive}=\partial I^-(\gamma),
\]

where the chronological sets and boundaries are taken **within this
original stationary patch**. These definitions refer to sending or
receiving at any finite time on the eternal rider's clock; they do not
mean a light cone from one launch event. They avoid ambiguous front/rear,
black/white, event/Cauchy horizon terminology.

The qualitative forward and rearward communication exclusions and their
Mach-cone character are established prior literature, e.g. Clark,
Hiscock and Larson (1999), *Null geodesics in the Alcubierre warp drive
spacetime: the view from the bridge*,
https://arxiv.org/abs/gr-qc/9907019. The explicit scalar construction and
checks below are our calculation for the draft's sech example. They are
not a claim of priority for communication horizons.

## 2. Stationary null graph and the sending branch

Write the sending horizon as x=h(y), h even. The normal d(x-h(y)) has norm

\[
 g_3^{-1}(d(x-h),d(x-h))=1+h'^2-v(h,y)^2.
\]

Thus its upper branch must solve

\[
 h'=-\sqrt{v(h,y)^2-1},\qquad h(0)=R_F=\operatorname{acosh}2.
\]

Let kappa=-v_x(R_F,0)=sqrt(3)/2. Expanding h=RF+A y^2+O(y^4) gives

\[
 4A^2=2\kappa(A+1/(2R_F)),\qquad
 A=\frac{\kappa-\sqrt{\kappa^2+4\kappa/R_F}}4<0.
\]

The positive root belongs to a different stationary null surface. The
null equation alone does not identify a communication horizon.

For clarity about the singular initial point: writing h=RF+y^2 a and
z=log y gives

\[
 a_z=f(a,e^{2z}),\quad f(A,0)=0,\quad
 f_a(A,0)=-2-\kappa/\beta<0,\quad \beta=-2A>0.
\]

Near z=-infinity the bounded solution a-A=O(e^{2z}) is obtained by the
variation-of-constants integral with the decaying kernel
exp[f_a(A,0)(z-s)]. A contraction on that weighted class gives the local
smooth branch and its uniqueness with this limiting quadratic term.
This regularization is also what the numerical calculation uses.

The branch exists for all y>0. It starts strictly outside the circle
r=RF. At a hypothetical first later contact with that circle, h'=0 and
dr/dy=y/RF>0, excluding inward contact. Also |h'|<=sqrt(V_b^2-1), so
finite-y blowup is impossible. In fact r increases and h is strictly
concave for y>0: if r' first vanished, differentiating r r'=h h'+y would
give (h h'+y)'=v^2>0 there, excluding a crossing to negative r'.

## 3. Why this graph really is the communication boundary

A future causal spatial trajectory parametrized by t satisfies

\[
 x'=v+u_x,\qquad y'=u_y,\qquad u_x^2+u_y^2\leq1.
\]

At F=x-h(y)=0,

\[
 F'=v+u_x-h'u_y\leq v+\sqrt{1+h'^2}=0.
\]

The graph is therefore a one-way barrier: no future timelike curve
starting at the rider can cross from x<h(y) to x>=h(y). Smoothness gives
the usual local comparison argument also at a tangency.

Conversely, every point strictly below the graph is reachable. The
connected subsonic disk v>-1 is reachable from the center by sufficiently
slow timelike spatial paths. Start in that disk at

\[
 y=\epsilon,\qquad
 x=\sqrt{R_F^2-\epsilon^2}-\epsilon^2.
\]

Outside it, follow the horizon-tangent unit controls

\[
 u_x=-1/v_H(y),\quad u_y=h'/v_H(y),\quad v_H=v(h(y),y)<-1.
\]

They have unit norm. The resulting spatial path, parametrized by y, obeys

\[
 \frac{dx}{dy}=\frac{v(x,y)v_H(y)-1}{h'(y)}.
\]

It remains below h. Its initial deficit from h is O(epsilon^2), and while
x,h>0 the deficit contracts, because v_x<=0 and v_H/h'>0. On every
subsequent fixed finite y interval the coefficients are bounded, so the
deficit still tends to zero as epsilon->0. This constructs reachable
paths arbitrarily close to any chosen finite point of the graph.

For each finite epsilon the flight time is finite. Slightly reduce the
unit control magnitude to obtain timelike paths with endpoints still
arbitrarily close to the graph. From a reachable point just above any
specified target x<h(y), a horizontal timelike path moving to smaller x
reaches that target. The y=0 case follows directly from subsonic access
and leftward timelike travel. Hence

\[
 I^+(\gamma)=\mathbb R_t\times\{x<h(y)\}.
\]

Time reversal combined with x reflection is an isometry of this symmetric
example. Therefore

\[
 I^-(\gamma)=\mathbb R_t\times\{x>-h(y)\},\qquad
 H_{receive}:x=-h(y).
\]

The numerical reachable-side calculation checks this construction at
y=2: starting at epsilon=.04,.02,.01 gives deficits approximately
4.41e-6, 3.21e-7, 2.33e-8. The causal identification rests on the argument,
not on those numerical samples alone.

## 4. Null generators and topology

On H_send the induced metric is

\[
 g_H=(h'\,dt-v_H\,dy)^2,
\]

so its future generators obey

\[
 \frac{dy}{dt}=\frac{h'}{v_H},\qquad
 \frac{dx}{dt}=\frac{v_H^2-1}{v_H}.
\]

Above the axis they move outward toward increasing y and backward in
comoving x. Below the axis the picture is reflected. The exact axial
generator remains x=RF,y=0. On H_receive the future directions are toward
the rear axial generator.

These are E=0 null geodesics. Writing their affine momentum as
P=p_x>0, Q=-P h' gives

\[
 \frac{d\log P}{dt}=-v_x,\qquad
 \frac{dt}{d\lambda}=-v_H P.
\]

Near y=0 on a sending wing, y is proportional to exp(beta t) as
t->-infinity and P is proportional to exp(kappa t). Its past affine
length is infinite. In the future its momentum tends to a finite positive
constant in the exterior, so its future affine length is also infinite.
The exact sending axial generator instead has finite future affine
length, as established in the paper. Time reversal gives the corresponding
rear statement. These statements concern generators of the horizons;
they do not classify all off-horizon rays approaching the tip.

On the signed meridional double each horizon has topology R_t x R_y.
On the actual angular quotient it is R_t x [0,infinity), with the axis a
quotient edge. Restoring the suppressed angle gives a spatial graph over
the entire transverse R^2: each full 4D horizon is topologically
R_t x R^2. It is noncompact, unlike the stationary-limit worldtube
S^2 x R. The latter is timelike away from its tips, since its radial
normal has norm y^2/RF^2 in the meridional section.

The two horizon sections cross at x=0, |y| approximately 2.23726332936.
Between them, where h(y)>0, the rider can both send and receive. Their
intersection in spacetime is spacelike, not a stationary timelike orbit.

## 5. The asymptotes identify specific points of ordinary scri

Let c=sqrt(V_b^2-1). The short-range tail gives

\[
 h(y)=-c y+C+o(1),\qquad y\to+\infty.
\]

For V_b=2 the calculation gives C approximately 4.249396222753. These
are spatial Mach asymptotes with half-angle asin(1/V_b) measured about
the backward comoving x direction. This is different from the angle of
their null generators in laboratory coordinates.

In laboratory coordinates X=x+V_b t,Y=y, the upper sending generator
asymptotically has velocity

\[
 (dX/dt,dY/dt)\to(1/V_b,c/V_b).
\]

All upper-wing generators therefore end at the same future-scri point
of the meridional double:

\[
 \cos\theta=1/V_b,\qquad u=t-R=-C/V_b.
\]

The lower wing gives its reflection. To see why the retarded time is
independent of the generator's time translation, use

\[
 t-\frac{X+cY}{V_b}=-\frac{x+cy}{V_b}\to-C/V_b.
\]

For V_b=2, theta=+/-pi/3 and u approximately -2.124698111376. After
restoring the suppressed transverse angle these two meridional points
are the section of a circle on ordinary future scri. The receiving wings
originate at the reflected past-scri circle, cos(theta)=-1/V_b and
w=t+R=C/V_b.

There is an important distinction between individual generator endpoints
and the closure of the entire horizon surface. Near the upper Mach
direction, with delta=theta-theta_M, the horizon equation gives

\[
 u=u_M+R(\cos\delta-1)+o(1),\qquad u_M=-C/V_b.
\]

Thus its closure on ordinary future scri is the half-generator
theta=theta_M, u<=u_M, together with its lower-wing reflection. Holding
one physical null generator fixed gives u=u_M. Allowing its label to vary
with R, with R delta^2 tending a nonzero finite constant, reaches earlier
points on the same scri generator. Near a point u<u_M the approach has
the checked local form delta^2 approximately 2s(u_M-u), s=1/R: the null
surface touches scri tangentially. In four dimensions this becomes the
scri cylinder theta=theta_M, u<=u_M, ending on the circle of fixed-generator
endpoints. The receiving horizon has the past counterpart
cos(theta)=-1/V_b, w>=C/V_b.

This identifies actual ordinary-scri attachment data for the horizon
wings, including the distinction between generator endpoints and surface
closure. It does not resolve every accumulation at the singular axial
end or the entire finite-parameter boundary beyond the axial ray.

## 6. What changes for a planar cap?

For the paper's capped profile v=W(x^2+psi(rho^2)-L^2), the sending
horizon is exactly x=L on 0<=rho<a, and the receiving horizon is x=-L.
This follows directly from the barrier at x=L and accessibility of its
interior side, since psi=0 on the aperture. These are actual open
Killing-horizon patches with a disk of stationary null generators.

Thus the rounded horizon's single axial finite-affine generator is
replaced on the cap by an open disk of such generators. Their future
endpoints continue through the regular extension; the rim remains the
separate obstruction proved in the paper. These horizon generators meet
the regular crossing surface only at its p=0 section; the whole crossing
surface also contains finite p nonzero.

The curved wings beyond the rim can be sought with the same null graph
equation. Their calculation must use the globally bounded W, not the
unbounded affine collar used only for local figures. No numerical global
capped wing is claimed here, since the manuscript specifies a class of
global W functions rather than one fixed numerical W.

## Checks and drawing

`exploration/stationary_horizons.py` solves the regularized horizon ODE,
compares independent near-axis starts, checks the null normal and induced
metric, verifies the one-way barrier, integrates the full null Hamilton
equations independently, checks E=0, and verifies the asymptotic scri
data. Only after these checks pass does it produce
`output/global_2p1/stationary_horizons.png`. That figure is a spatial
cross-section of the global stationary null surfaces, not a Penrose
diagram. The raw check report is
`output/global_2p1/stationary_horizons_check.txt`.
