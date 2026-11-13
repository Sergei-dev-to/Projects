# Restart: verified 2+1 boundary neighborhoods

The background laboratory double cone is retired as a global conformal
construction. We do not inherit its boundary shape, colored tube shape,
waist identifications, or assignment of endpoints. Its finite-interior
inverse remains a mathematically valid coordinate calculation, but it
does not specify the boundary of the intended completion.

This restart retains the physical capped metric and the conformal factor
checked in `proper_conformal_completion.md`. It independently checks the
cap pullback and draws only the boundary neighborhoods justified by those
calculations. It does not change the manuscript or its figures.

Run:

    python exploration/verified_2p1_start.py

New outputs are isolated from the earlier double-cone images:

- `output/verified_2p1_start/verified_boundary_neighborhoods.png`
- `output/verified_2p1_start/checks.json`

## 1. Fixed physical geometry

Use the signed meridional double

\[
 g=-dt^2+[dx-v(x,y)dt]^2+dy^2.
\]

The actual axial-symmetry quotient folds y to |y|; we display its signed
double to show both transverse directions. No transverse symmetry beyond
the actual planar cap is used to simplify the metric.

The globally bounded profile is the one in `capped_horizon_atlas.py`.
In the exact cap collar |y|<a=0.6 and |x^2-1|<0.25,

\[
 v=-(1+x^2)/2.
\]

The old conformal factor is retained, not replaced by another guessed
compactification:

\[
 \Omega=\chi\omega_c+(1-\chi)(1+R^2)^{-1/2},\quad
 R^2=(x+2t)^2+y^2,\quad
 \chi=1-S((x^2+y^2-4)/5).
\]

The exact cap expression for omega_c and its signed continuation are in
the earlier notes and `proper_conformal_completion.py`. The new script
checks matching on the original side. The exterior factor is exactly
(1+R^2)^(-1/2) near every finite ordinary-scri cut.

## 2. Cap crossing: derive the coordinates from the metric

Let

\[
 h(x)=\frac2{\sqrt3}\arctan\frac{x}{\sqrt3},\quad
 s_0^2=2e^{h(1)},\quad
 P(x)=s_0\frac{1-x}{1+x},\quad Q(x)=s_0e^{-h(x)},
\]

\[
 p=P(x)e^t,\quad q=Q(x)e^{-t},\quad
 C(x)=\frac{(1+x)^2(x^2+3)e^{h(x)}}{4s_0^2}.
\]

The new script symbolically pulls C dp dq+dy^2 back into (t,x,y), and
obtains the exact physical metric with zero residual. As F=PQ has
F'(1)=-1, x is a smooth function of pq near zero, and C(0)=2.
Consequently

\[
 \widehat g=\Omega^2[C(pq)dp\,dq+dy^2]
\]

is a regular metric through q=0 for finite p and |y|<a. Here and below
C(0) means its value as a function of pq.

Now define, without any compactifying arctangent,

\[
 X=(p+q)/2,\qquad T=(p-q)/2.
\]

Then

\[
 \boxed{\widehat g=\Omega^2
       [C(pq)(dX^2-dT^2)+dy^2]},\qquad
 \widehat g^{-1}(dT,dT)=-1/(\Omega^2C)<0.
\]

T is a genuine temporal coordinate on this patch. The original side
has q>0, or T<X; the continued side has q<0, or T>X. The cap crossing
surface q=0 is the null plane T=X, with a finite open transverse
aperture. Omega stays positive there. It is not null infinity.

At each point its future null directions can be parameterized in
(X,y,T) by

\[
 (dX,dy,dT)=(\cos\alpha,\sqrt C\sin\alpha,1).
\]

Their nullness is exact. This represents the full local 2+1 metric,
including its transverse coefficient, not a flat 1+1 diagram extruded
while forgetting the transverse geometry. No conformal flatness is
asserted.

The displayed p range is 0.08 to 0.85 and q range -0.08 to 0.12. The
entire range has -0.177 < x^2-1 < 0.152, inside the actual profile's
affine collar. The freely falling trajectory is integrated with physical
unit timelike normalization. It crosses q=0 at proper time
0.0561839995148 from the specified initial event; its plotted T is
strictly increasing. Neither this elapsed time nor the finite coordinate
cuts are global invariants or spacetime boundaries.

## 3. Ordinary future null infinity: a different verified chart

In the exact exterior let X_lab=x+2t and use polar coordinates R,theta.
Set

\[
 \tau=t-\sqrt{1+R^2},\quad r=R/(1+R),\quad z=1-r,\quad d=r^2+z^2.
\]

The previously checked full metric is

\[
 \widehat g=\frac1d\left[-z^2d\tau^2
 -2\frac r{\sqrt d}d\tau\,dr+\frac{dr^2}{d}+r^2d\theta^2\right].
\]

At r=1 the full ambient metric has the regular boundary value

\[
 \widehat g=-2d\tau\,dr+dr^2+d\theta^2,
 \quad\det\widehat g=-1,\quad
 \widehat g^{-1}(d\tau,d\tau)=-1.
\]

This is the ambient tensor evaluated at the boundary, not its induced
metric; the induced metric is dtheta^2 with null generator partial_tau.
The normal dr is null. Here Omega=0 and dOmega is nonzero, as required
at ordinary null infinity. In the figure it is a cylinder because theta
is periodic and tau has not been compactified. Its drawn upper and
lower cuts are just finite chart cuts, not endpoints of scri.

The drawn exterior neighborhood r>=0.94, -1<=tau<=1 is verified to lie
in the actual exactly flat region at every sampled angle. At r=1 the
future null directions in (tau,r,theta) are

\[
 (1,1+\cos\alpha,\sin\alpha).
\]

Those are the directions used in the exterior panel. The time-reversed
construction gives past scri and the rear crossing.

## 4. Status and next mathematical target

The two surfaces are distinct null surfaces of different kinds: a cap
exit with positive conformal factor, and ordinary scri with zero factor.
Both have regular ambient metrics in their stated neighborhoods.
The new figure makes no global connection between them and places no
rider endpoint, rim endpoint, or spatial endpoint. Those ends are outside
the displayed neighborhoods and remain unresolved.

The next target is the domain and transition maps of the intervening
region, derived from this same physical metric. A global diagram must
follow that calculation. A proposed drawing must not supply the missing
boundary identification by appearance.
