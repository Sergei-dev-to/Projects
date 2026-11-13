# Resolving the apparent junction at background spatial infinity

This calculation replaces the identification at the old background pole
by explicit approach coordinates. It separates ordinary null infinity,
finite cap crossings, and stationary infinite-time approaches, and finds
how the forward axial scri and cap parameters diverge towards the critical
flow label. It does not construct a smooth conformal rider vertex or a
finished global diagram. The distinction between an approach-space
resolution and a regular conformal completion is essential below.

## 1. Resolve the background spatial approach directions

For the V=2 example let X_lab=x+2t, R=sqrt(X_lab^2+y^2), and define

\[
 r=R^{-1},\quad s=t/R,\quad
 (X_{\rm lab},y)=R(\cos\theta,\sin\theta).
\]

The exact inverse is

\[
 t=s/r,\quad x=(\cos\theta-2s)/r,\quad y=\sin\theta/r.
\]

These variables retain approach directions that the background
Minkowski spatial-infinity point collapses. They are coordinates for a
directional blow-up, not automatically a regular conformal metric chart.
In particular the rider's spacelike *background* direction does not make
its worldline spacelike in the physical bubble metric.

At ordinary future scri, finite retarded time u=t-R means

\[
 s=1+ur\longrightarrow1.
\]

For every bounded comoving x,y with t -> positive infinity,

\[
 s\longrightarrow\tfrac12,\qquad\theta\longrightarrow0.
\]

This includes both the rider and finite front-cap approaches, but it is
a different directional limit from ordinary scri at every finite cut.
The corresponding past bubble direction is s=-1/2, theta=pi; ordinary
past scri has s=-1.

In the exact flat exterior the physical directional metric is

\[
 g=\frac{1-s^2}{r^4}dr^2+\frac{2s}{r^3}dr\,ds
   -\frac{ds^2}{r^2}+\frac{d\theta^2}{r^2}.
\]

Substituting s=1+ur and choosing Omega=r gives the full regular metric

\[
 \widehat g=2du\,dr-r^2du^2+d\theta^2,
 \qquad\det\widehat g=-1.
\]

Its r=0 normal is null. The previous exterior gauge differs by the
smooth positive factor (1+r^2)^(-1/2), so has the same boundary limit.
Thus the ordinary-scri part is checked, including the angular dimension.

## 2. Resolve the bubble direction

The finer variables near s=1/2,theta=0 are precisely

\[
 x=\frac{\cos\theta-2s}{r},\qquad y=\frac{\sin\theta}{r}.
\]

They distinguish, for example, the central rider x=y=0 from an approach
to the front cap x -> 1, |y|<a. They retain a continuum of stationary
approaches, not a single predetermined endpoint.

To distinguish finite crossing locations on the cap, resolve one more
scale:

\[
 q=e^{-t}=e^{-s/r},\qquad
 \lambda=(x-1)e^t,\qquad x=1+q\lambda.
\]

The limit q=0 with finite lambda and |y|<a=0.6 is the regular cap face.
The rider x=0 instead has lambda=-1/q -> -infinity. Thus finite cap
locations and the rider end are explicitly distinguished.

In the actual affine cap collar v=-(1+x^2)/2, direct substitution gives
the exact physical metric

\[
 \boxed{g=q^2d\lambda^2
 -2(1+\tfrac12q^2\lambda^2)d\lambda\,dq
 +(\lambda^2+\tfrac14q^2\lambda^4)dq^2+dy^2.}
\]

Its determinant is identically -1. At q=0,

\[
 g=-2d\lambda\,dq+\lambda^2dq^2+dy^2.
\]

This is a regular null face with an open transverse interval. The prior
conformal factor becomes

\[
 \Omega=
 \frac1{\sqrt{(1+\lambda^2)(1+q^2)}}+
 \frac q{\sqrt{[1+(2+q\lambda)^2q^2](1+q^2)}},
\]

and has positive limit (1+lambda^2)^(-1/2). There is no zero-Omega
infinity at a finite crossing. Signed q continues the metric and factor.
The covector d(-lambda-q) is timelike throughout this polynomial collar:

\[
 g^{-1}(d(-\lambda-q),d(-\lambda-q))
 =-2-\lambda^2-q^2(1+\lambda^2+\lambda^4/4)<0.
\]

As an explicit timelike approach from inside, choose lambda=-0.4+q and
y=0.3, with q decreasing from 0.05 to zero. Its proper time is finite,
approximately 0.0681620369 in the chosen units. This trajectory is used
as a timelike check, not asserted to be geodesic.

## 3. Where the cap and forward scri go in the global flow label

Use the exact global flow from `global_spacelike_flow.md`:

\[
 F_t=v_0(F)+1+\eta\operatorname{sech}^2t,\quad F(0,A)=A,
 \qquad\eta=0.05.
\]

Its separating label is A_* approximately -1.02841138321357.
The future asymptotic regimes are:

- A<A_*: F eventually escapes into the left flat exterior;
- A>A_*: F tends to the front cap x=1;
- A=A_*: F tends to the rear stationary null generator x=-1.

The rider x=0 is not this last flow trajectory. Its varying label A(t)
tends to A_* from above. Losing that rate would conflate distinct
approaches; the scaled coordinate zeta=(A-A_*)/q retains it. For the
central rider zeta tends to a finite positive value (about 0.577 in this
normalization). More generally, finite fixed x between the axial horizons
gives a nontrivial stationary-approach family in this zoom.

On the escaping side, after reaching the exact exterior,

\[
 F=-t+\eta\tanh t+\mathcal B(A),\qquad
 u\longrightarrow-\eta-\mathcal B(A)
\]

at the forward angular generator with bounded y. On the cap side,
lambda tends to L0(A). The saddle near x=-1 has growth exponent 1;
the delay in leaving it scales as -log|A-A_*|. Matching to the front
decay exponent 1 and the exterior speed -1 gives leading behavior

\[
 L_0(A)\sim-\frac{K}{A-A_*}\quad(A\downarrow A_*),\qquad
 u(A)=\log(A_*-A)+c+o(1)\quad(A\uparrow A_*),
\]

with K>0. This leading-order saddle analysis is supported numerically;
a uniform remainder theorem for joint angular limits has not been proved.
In the tested normalization, the products -(A-A_*)L0 approach roughly
0.340, while u-log(A_*-A) approaches roughly 2.540. These are numerical
asymptotic estimates, not exact constants or certified error bounds.

Therefore a finite cap crossing is not glued to a finite retarded-time
cut of scri. Towards the critical label, the cap coordinate goes to
-infinity and the forward scri retarded time also goes to -infinity.
This determines the axial incidence of the limiting sectors, rather
than assuming that finite pieces meet in the old picture.

Independent backward-flow checks at t=20 give approximately:

| approach | A |
|---|---:|
| ordinary forward scri, u=0.7 | -1.199853394 |
| central rider | -1.028411382 |
| cap crossing, lambda -> -0.4 | 0.1410925 |

The angular statement has limits: finite nonforward scri directions do
not all have finite A. In the exterior the full regular transverse
resolution uses Q=1/(t+X_lab), Y=y/(t+X_lab), and
U=t-X_lab-y^2/(t+X_lab), with Q^2g=dU dQ+dY^2. That chart, or the radial
scri chart in section 1, must be retained. The flow-label asymptotics
alone are not a proof that the full two-dimensional scri has been glued
smoothly to a rider vertex.

## 4. The rider-side face is not regular in this resolution

Keep finite comoving x,y while q=e^-t -> 0. Then

\[
 q^2g=(v^2-1)dq^2+2vq\,dx\,dq+q^2(dx^2+dy^2).
\]

At q=0 this ambient tensor has rank one wherever v^2 != 1, not Lorentzian
rank three. The chosen Omega has Omega/q -> 2/(1-x^2) in the planar
interior |x|<1, so gives the same rank failure. Thus retaining these
approach directions yields a degenerate stationary-end face, not a
regular conformal boundary.

This rank calculation is specific to the resolved coordinates and gauge.
It does not prove that the central flat rider orbit cannot be assigned
a regular endpoint under every possible completion. The earlier Cotton
and Weyl audit supplies stronger obstructions for nonflat stationary
orbits when they are assigned zero-Omega endpoints of the stated
regularity. Neither argument licenses a claim of a physical singularity
along the central rider at finite proper time.

## Result and scope

We now have exact transition formulas separating the approach sectors,
regular metrics at ordinary scri and at finite cap crossings, and an
explicit diagnosis of the stationary-end degeneration. The old point
identification is replaced by a stratified approach-space resolution.
It is not a proof that a smooth global conformal manifold including all
these ends exists, nor that a single rider vertex is the correct boundary
assignment. The complete angular junction and any blow-down of the
stationary-end face remain open.

Run `python exploration/junction_blowup.py`. Symbolic checks verify both
regular metric limits, determinants and time orientation. Seventy-digit
inverse checks and flow/scattering calculations are recorded in
`output/junction_blowup/checks.json`. No manuscript figure is changed.
