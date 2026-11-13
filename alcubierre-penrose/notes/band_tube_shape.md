# What the axial band becomes: a pinched tube with finite null exit faces

**Status correction: the uniformly pinched closure is retired.**
The finite-interior transformation below remains usable, but its closure
is not a faithful causal or conformal completion. A fixed spatial point
on an outer sending-horizon wing is mapped to the future rider tip as
t tends to infinity, although it can never receive a timelike signal
from any rider event. This contradicts openness of chronology at that
tip. See sections 6--10 of `joint_boundary_limits.md` for the proof and
the replacement signal-time criterion. Earlier claims below about the
topology of the whole closed tube are superseded by this correction.

This answers the proposed sausage-link picture in a definite conformal
display. It constructs the image of the **entire communication tube** of
the previously calculated bounded capped bubble, including its curved
horizon wings inside that tube. It is not just an extrusion of the cap.
The pointed ends are coordinate limits; smoothness at those endpoints is
not asserted. No manuscript edit is made here.

## 1. The actual region being drawn

Let gamma be the entire central rider in the original stationary patch.
The previous horizon calculation gives

\[
 \mathcal D=I^+(\gamma)\cap I^-(\gamma)
 =\{(t,x,y):-h(y)<x<h(y)\}.
\]

The spatial section is a bounded lens. For |y|<=a=0.6, h=1; outside the
aperture h decreases to zero at

\[
 y_*=C/\sqrt3\simeq1.52256.
\]

Equivalently -1<x<1 and |y|<R(x), where R is even, a<=R<=y_*, and
h(R(x))=|x|, with R(+/-1)=a by continuity. The original axial band is
the y=0 section. The complete horizons also extend beyond this tube;
those exterior portions and ordinary scri are not part of this drawing.

## 2. Longitudinal null coordinates regular at the cap faces

Use the actual global axial profile v0(x)=W(x^2-1), not the unbounded
quadratic collar. Its front and rear slopes have magnitude kappa=1.
On -1<x<1 define

\[
 P(x)=\exp\!\left[-\int_0^x\frac{ds}{1+v_0(s)}\right],\quad
 Q(x)=\exp\!\left[\int_0^x\frac{ds}{v_0(s)-1}\right],
 \qquad p=P(x)e^t,\quad q=Q(x)e^{-t}.
\]

Here p,q>0. Write F=PQ=exp(-J), with

\[
 J(x)=\int_0^x\frac{2\,ds}{1-v_0(s)^2},\qquad
 C(x)=\frac{1-v_0(x)^2}{F(x)}.
\]

Then g2=C dp dq. F decreases from infinity to zero as x goes from -1
to 1, so p and q independently cover the whole positive quadrant.
Since v0 is even, J is odd, F(-x)=1/F(x), and
C(-x)=C(x) F(x)^2.

The cap collar is exactly quadratic, allowing stable limits instead of
subtractions at x=+/-1. For x>=0.9,

\[
 J(x)=\log\frac{1+x}{1-x}+
 \frac{2}{\sqrt3}\arctan\frac{x}{\sqrt3}+\Delta,
 \qquad \Delta\simeq-0.971108323756.
\]

The front coefficient C0=lim_{x->1} C(x) is approximately
2.772600879803. The same constant governs the regular rear chart after
inverting p and q.

Compactify with a longitudinal weight w=2:

\[
 \alpha=w\frac{p-1}{p+1},\qquad
 \beta=\frac{1-q}{1+q},\quad
 T=\frac{\alpha+\beta}{2},\quad X=\frac{\beta-\alpha}{2}.
\]

Thus the axial band is the parallelogram -w<alpha<w, -1<beta<1. A
different longitudinal gauge changes its tilt and aspect ratio; retaining
the previous plotting gauge is not required. The future and past rider
limits are

\[
 P^+: (X,T)=((1-w)/2,(1+w)/2),\qquad P^-=-P^+.
\]

The front stationary generator ends at alpha=-w,beta=1. This is a
different corner of the axial band from P+. The rear counterpart has
alpha=w,beta=-1.

The old atan(w_null) plotting compactification made the transverse
normalization diverge at regular physical exits. The present beta is
Möbius in the regular Kruskal coordinate q; it remains regular there.

## 3. Conformal factor and transverse coordinate

One possible axial normalization is

\[
 \Omega_0^2=\frac{4w}{C(p+1)^2(q+1)^2},\qquad
 \Omega_0^2g_2=-dT^2+dX^2.
\]

For a simpler display, choose the equally valid smooth interior gauge

\[
 \Omega=K(1-\sigma\beta),\qquad
 \sigma=\alpha/w,\qquad K=\sqrt{w/C_0},\qquad Y=\Omega y.
\]

Omega is strictly positive throughout the band. It agrees with Omega0
on each of the four regular boundary faces and remains finite and
nonzero at every finite cap-crossing label. Its ratio to Omega0 is a
smooth positive rescaling there. Interior gauge differences alter the
outline, not the null geometry or physical regularity of a cap crossing.

Off the planar cap the full metric must still include v(x,y)-v0(x).
This is **not** an assertion that it is conformal to a flat 3D metric.
The actual full metric is pulled back under (t,x,y)->(T,X,Y) and scaled
by Omega squared. The coordinate transformation is a diffeomorphism in
the tube: the longitudinal map is invertible and Omega>0. The transverse
rescaling introduces mixed metric terms. No Euclidean 45-degree rule is
used for the off-axis cones or wing surfaces.

The tube's coordinate image is explicitly

\[
 |Y|<\Omega(\alpha,\beta)R(x(\alpha,\beta)),\qquad
 -w<\alpha<w,\quad-1<\beta<1.
\]

Its curved boundary is obtained from the previously checked horizons,
not inferred from a convenient envelope shape. The front horizon has
x=h(y), the rear x=-h(y). Their portions bounding the tube meet at
x=0, y=+/-y_*; those intersection curves appear as creases on the
coordinate envelope. A smooth sausage is therefore only a rough analogy.

## 4. Yes: the complete diagram-time sections pinch

At the future rider end write sigma=1-d, beta=1-e, with d,e>=0. Then

\[
 \epsilon=T_+-T=\tfrac12(wd+e),\qquad
 \Omega=K(d+e-de)\leq2K\epsilon
 \quad(w\geq1).
\]

Since R(x)<=y_*, every fixed-T section has transverse diameter at most
4K y_* epsilon. Its longitudinal diameter is exactly 2epsilon once
sufficiently close to T+. The whole section consequently shrinks to the
point P+, linearly in the remaining diagram time. Reflection gives the
same result at P-. This proves a uniform pinch of the entire tube image,
including the curved wing portions, not only of the axial line.

For a particularly simple exact check, on the central spatial line x=0,
P=Q=1 and sigma=beta=tanh(t/2). Hence

\[
 \Omega(t,0)=K\operatorname{sech}^2(t/2),\qquad
 |Y|_{max,x=0}=K y_*\operatorname{sech}^2(t/2).
\]

This is a conformal display scale; no physical contraction is inferred.
The slices just proved to shrink uniformly are fixed **diagram time T**
slices. Fixed comoving t slices have a different limiting behavior near
the crossing faces, which is essential in the next section.

## 5. The finite-time exit does not collapse into the pointed end

At a regular future cap crossing, q=0, p is finite and |y|<a. Thus
beta=1 and

\[
 \Omega=K(1-\sigma)>0,\qquad
 T+X=1,\qquad |Y|<aK(1-\sigma).
\]

This is an open triangular **null face** in the 3D coordinate picture.
It has a nonzero-width edge at the endpoints of the front stationary
cap generators (p=0), and tapers toward P+ only as p->infinity. Its two
rim edges are excluded from the regular physical attachment.

The past cap-crossing face has beta=-1 and is the reflected triangle.
The planar front and rear horizon portions are two further triangular
faces. For example alpha=-w gives Omega=K(1+beta): it runs from P- to
the finite-width front generator endpoints. Those are the 3D versions
of the different sides of the familiar axial band.

The full pictured object therefore has pointed rider-time ends **and**
nonzero-width null exit faces. A freely falling traveler may leave
through the latter at finite proper time. The rider's own worldline
instead runs to P+ after infinite proper time. Both features can be
displayed together; a uniform collapse of all t->infinity approaches
would lose this distinction.

This does not identify the exit face with ordinary scri. The external
ordinary-scri chart is separate, as checked in the previous atlas.

## 6. Diagram time really increases in the full transverse metric

Extending an arbitrary axial diagram time off-axis need not work. Here
there is a check using the full metric, not just the planar product.
Write fu=2w p/(p+1)^2, fw=2q/(q+1)^2. Then

\[
 T_t=\tfrac12(f_u+f_w),\qquad
 T_x=-\tfrac12\left(\frac{f_u}{v_0+1}+
                          \frac{f_w}{v_0-1}\right),\qquad T_y=0.
\]

For all t at fixed x, fu/fw is at least w exp(-J(|x|)). The actual
transverse shift satisfies -2<=v(x,y)<=v0(x)<=0 in the longitudinal
interior. Positivity of T on both future radial null directions, and
therefore on all future causal directions, follows if

\[
 w>\max_{0\leq x<1} e^{J(x)}
 \frac{(2+v_0)(1+v_0)}{(4+v_0)(1-v_0)}.
\]

For this specified profile a monotone right-Riemann enclosure bounds the
right-hand side below 1.579 on [0,0.9]. In the remaining exact affine
collar an elementary bound gives less than 0.266. Thus w=2 satisfies
the condition with a substantial margin. The chosen T is future temporal
on the entire tube, including its nonplanar portions. This was checked
before plotting; the old axial plotting gauge is not silently reused.

## Checks and scope

`exploration/band_tube_shape.py` verifies primitive inversion, the global
time bound, sampled full-metric time orientation, exact central scaling,
finite-width exit limits and shrinking full cross-sections. The numerical
coordinate inversion residual is below 1.1e-7 for the sampled points;
the pinch and time-orientation arguments above are analytic, rather than
inferences from those samples. Near T+=1.5 the measured transverse
diameter divided by (T+-T) tends to about 3.45 in this gauge.

Outputs are `output/global_2p1/band_tube_shape.png` and
`output/global_2p1/band_tube_shape_check.json`. The figure is the full
communication tube for this chosen capped profile. It is not the whole
original spacetime or a maximal continuation. Smooth corner completion
at P+/- and attachment of the exterior remain separate questions.
Folding Y and -Y gives the angular quotient; restoring the suppressed
angle produces the four-dimensional counterpart.
