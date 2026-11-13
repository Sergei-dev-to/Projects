# Capped bubble: outer wings, null-infinity contacts, and a global horizon atlas

This calculation fixes a particular globally bounded W in the family used
in the paper, while retaining exactly the local cap metric used there. It
constructs the complete stationary horizon sections and their exterior
conformal geometry. The resulting figure is a matched atlas covering the
original horizons and their regular boundary pieces; it is **not** a
claim to have completed all singular corners of a single Penrose domain.
The manuscript and its saved PDF are unchanged.

## 1. A fully specified member of the paper's capped family

Let L=1, a=0.6, b=1, d=0.2 and V_b=2. Set

\[
 H(z)=\begin{cases}\int_0^z e^{-1/w}\,dw,&z>0,\\0,&z\leq0,\end{cases}
 \qquad
 \psi(y)=\frac{H((y^2-a^2)/d)}{H((b^2-a^2)/d)},\qquad
 \Phi=x^2+\psi(y)-1.
\]

Here psi is written as a function of signed y, whereas the manuscript
writes the same function as a function of rho squared. The stationary
wall is Phi=0; its planar sections are x=+/-1, |y|<0.6.

Use the infinitely flat step

\[
 S(z)=\frac{e^{-1/z}}{e^{-1/z}+e^{-1/(1-z)}}\quad(0<z<1),
 \qquad S=0\ (z\leq0),\quad S=1\ (z\geq1).
\]

Choose

\[
 W(\phi)=\begin{cases}
 -(1+\phi/2)S((\phi+3/4)/(1/2)),&\phi<-1/4,\\
 -1-\phi/2,&|\phi|\leq1/4,\\
 -2+(1-\phi/2)[1-S((\phi-1/4)/(7/4))],&\phi>1/4.
 \end{cases}
\]

This is smooth and nonincreasing; W=0 for phi<=-3/4, W=-2 for phi>=2,
W(0)=-1 and W'(0)=-1/2. There is a genuine flat core, with v(0,0)=0, so
the central rider's proper time is t. In the affine collar the metric is
exactly the one already used in the paper:

\[
 v=W(\Phi)=-\tfrac12(1+x^2+\psi(y)).
\]

The nonflat region is compact in comoving space. In particular, when
|y|>=Y_E, where psi(Y_E)=3, all x are in the exact exterior v=-2. Here
Y_E approximately 1.312204812487.

The detailed numerical intercept below belongs to this specified W. The
Mach directions and the form of the scri contact have the general speed
dependence derived below.

## 2. Entire stationary sending and receiving horizons

As in the rounded calculation, the causal definitions are

\[
 H_s=\partial I^+(\gamma),\qquad H_r=\partial I^-(\gamma),
\]

for the entire central worldline gamma in the original stationary patch.
The sending section is even and solves

\[
 h(y)=1\quad(|y|\leq a),\qquad
 h'=-\sqrt{v(h,y)^2-1}\quad(y>a).
\]

The receiving section is x=-h(y), by time reversal and x reflection.
The same causal barrier as in `stationary_communication_horizons.md`
applies: on x=h(y), the maximum future d(x-h)/dt is
v+sqrt(1+h'^2)=0. Conversely, start just inside the subsonic region at
y=a+epsilon and approximate the horizon-tangent controls. The initial
deficit tends to zero, contracts where x>0 because v_x<=0, and remains
small on each subsequent compact interval. Every point x<h(y) is then
reachable by a timelike approximation followed by leftward travel.
Hence these are the actual communication boundaries, not merely two
solutions of a null-surface equation.

The wing remains outside Phi=0: at any later contact with Phi=0,
h'=0 and dPhi/dy=psi'(y)>0, excluding inward contact. The bound
|h'|<=sqrt(3) gives global existence. Once y>=Y_E, the ODE is exactly
h'=-sqrt(3), so the wing is exactly a straight line, not an approximate
tail:

\[
 h(y)=C-\sqrt3\,y,\qquad C\simeq2.637158425.
\]

The full meridional null surfaces are x=+/-h(y), with t arbitrary.
Restoring the suppressed angle gives spatial graphs over transverse R^2.
The horizons are noncompact even though the stationary-limit wall is
compact.

## 3. The flat rim: a stable numerical formulation and an error bound

Near y=a the wing is exponentially close to the stationary-limit wall.
Directly evaluating v+1 by subtracting floating-point numbers can erase
that difference. In the affine collar instead put k=-h'>0. Exactly,

\[
 \Phi=2(\sqrt{1+k^2}-1)=\frac{2k^2}{\sqrt{1+k^2}+1},\quad
 h=\sqrt{1-\psi+\Phi},\quad
 k'=\sqrt{1+k^2}\left(\frac{\psi'}{2k}-h\right).
\]

The stiff forward equation for k is integrated with an implicit solver,
then matched to the h equation after y=0.67. Independent starts at 0.610
and 0.615, with different matching points, give the same resolved wing
to numerical tolerance.

The branch can be defined without a numerical guess at the flat rim:
start at y=a+epsilon with heights between the wall w and L, integrate
forward, and let epsilon decrease to zero. The initial height interval
has width L-w tending to zero. Where h>0, the derivative of the h-ODE
right-hand side with respect to h is nonpositive, so this interval
contracts rather than amplifies. Subsequent compact intervals have
bounded amplification. This selects a unique outgoing limiting branch.
The wall-start construction has k=0 initially and stays below the bound
K used next.

The tiny unresolvable part next to the rim is bounded analytically. Let
w=sqrt(1-psi), K=psi'/(2w). Since psi''>0 and w decreases, K increases.
The outgoing solution satisfies k<=K: at a hypothetical crossing k=K,
the equation gives k'<=0, while K'>0. Consequently

\[
 0\leq h-w=\frac{\Phi}{h+w}\leq\frac{K^2}{2w}.
\]

At y=0.610 the upper bound is 9.522e-15 and is still smaller closer to
the rim. The plotted wall track below that numeric start is an
approximation with this explicit bound, not an independently resolved
numerical null wing. Errors in the initial height contract while h>0;
the subsequent finite interval has bounded error amplification. No
machine-scale distinction is used as evidence for regularity at the rim.

For every nonstationary wing generator, dy/dt=k/(-v)>0. It approaches the
rim only as t->-infinity, with infinite past affine length, and travels to
ordinary future scri with infinite future affine length. On the planar
cap, including the rim itself as a finite-t generator, y is constant.
Its future affine length is finite. The open cap generators have regular
future endpoints; the rim's extension obstruction remains the one proved
in the manuscript.

## 4. How the wings meet ordinary null infinity

For either upper exterior sending wing, x=C-c y with c=sqrt(V_b^2-1).
Laboratory coordinates X=x+V_b t, Y=y give the exact Minkowski null plane

\[
 t-\frac{X+cY}{V_b}=u_M,
 \qquad u_M=-C/V_b.
\]

Let theta_M=acos(1/V_b), with sin(theta_M)=c/V_b. Every fixed physical
null generator in the upper wing tends to

\[
 \theta=\theta_M,\qquad u=t-R=u_M
\]

on ordinary future scri. The lower wing is reflected. For this profile,
theta_M=pi/3, u_M approximately -1.318579212. Receiving wings have the
time-reversed data on ordinary past scri:

\[
 \cos\theta=-1/V_b,\qquad w=t+R=C/V_b.
\]

The full surface closure is larger than the endpoints of fixed generators.
With s=1/R, delta=theta-theta_M, its exact equation near future scri is

\[
 F=s(u-u_M)+1-\cos\delta=0.
\]

At every finite u<u_M it approaches scri tangentially, with
delta^2 approximately 2s(u_M-u). Thus its closure on future scri is the
half-generator theta=theta_M, u<=u_M, plus its lower reflection. Holding
one physical generator fixed gives the endpoint u=u_M; varying the
generator label while taking the limit supplies the earlier scri points.

This also checks the null character in the regular boundary chart. For
the conformal metric

\[
 \widehat g=-s^2du^2+2du\,ds+d\delta^2,
\]

the norm of dF is F(F+2 cos(delta)), hence zero on F=0. At s=delta=0,
u<u_M, the horizon normal is parallel to the scri normal ds. At u=u_M
the defining function has zero gradient: this is the conformal focusing
point of the fixed generators. The past contact is similarly
s(w-w_M)-(1-cos(delta))=0 and w>=w_M.

Restoring the suppressed angle turns the two meridional half-generators
into a null cylinder on scri, ending on a circle of generator endpoints.
The wing does not meet future scri as a generic transverse surface cut.

## 5. The global atlas used for the drawing

The charts have actual overlaps; the figure is not a proposal to glue its
drawn frame edges to each other.

**Stationary chart.** Use (tau,x,y), tau=(2/pi) atan(t), for |y|<3,
all finite x and t. This covers the core, caps and inner wings. Since
g^-1(dt,dt)=-1, tau is globally future temporal in this chart. The metric
is the exact original metric pulled back with
dt=(pi/2) sec^2(pi tau/2) d tau. The figure's finite plotting cuts are
not physical boundaries. Open markers on the central line denote
unattached infinite rider time, not the exterior timelike-infinity points.

**Exterior conformal chart.** Where Phi>2, use exact laboratory Minkowski
coordinates and

\[
 T=\arctan(t-R)+\arctan(t+R),\quad
 \chi=\arctan(t+R)-\arctan(t-R),\quad
 (Z_1,Z_2)=(\chi\cos\theta,\chi\sin\theta).
\]

Then

\[
 (\cos T+\cos\chi)^2g_3
 =-dT^2+d\chi^2+\sin^2\chi\,d\theta^2,
 \qquad |T|+\chi<\pi.
\]

The stationary and exterior charts cover the whole original meridional
spacetime: every |y|>=3 point is exterior. They overlap openly. The
exterior wings are plotted for |y|>=2.5, so the horizon drawings also
have an explicit overlap with the inner chart. All finite-parameter cuts
of ordinary scri lie in this regular exterior completion. The bold scri
curves and their endpoint dots are fixed by section 4, before plotting.

The double-cone display retains spatial directions around its base for
visualization. Its base is **not** a newly established boundary circle
of the physical spacetime. In particular, the ordinary Minkowski i0
identification is not applied to collapse the bubble's different ends.
That corner is omitted from this atlas. The ordinary exterior i+/-
vertices are distinct from the rider's limiting ends.

**Regular front cap chart.** In |y|<a and near x=1, the existing normalized
coordinates are

\[
 p=P(x)e^t,\quad q=Q(x)e^{-t},\quad
 g_3=C(pq)\,dp\,dq+dy^2,
\]

with C(0)>0. Use X_c=(p+q)/2, T_c=(p-q)/2 to draw it. The metric is
C(dX_c^2-dT_c^2)+dy^2, not a Minkowski metric with a spectator
coordinate unless C is appropriately accounted for. T_c is temporal.
The original sending horizon is p=0,q>0; its continuation has p=0,q<0.
The regular crossing surface is q=0 with finite p and |y|<a. The
intersection p=q=0 is the cap's disk of original-generator endpoints;
it is not the entire crossing surface. The black curve is the existing
unit timelike geodesic, checked to remain inside this particular W's
affine collar throughout the displayed crossing. The rear chart is its
time reverse.

The cap chart overlaps the stationary chart via the displayed p,q
formulas. On compact sets of finite cap labels, q->0 gives t->infinity,
x->1 and bounded y, so lab retarded time u tends to -infinity. These
finite physical crossing points are therefore not finite-u points of
ordinary null infinity. The local physical metric is regular and its
conformal factor may remain positive; ordinary scri uses a vanishing
factor. These open attachments are Hausdorff-separated. A smooth positive
interior conformal factor can be patched from the cap's factor 1 and the
exterior defining function. This is a global **open partial conformal
completion**, including the entire original patch and the stated regular
boundary pieces. It is not compact, and no maximality is claimed.

The signed meridional double makes both wings visible. Folding y and -y
together gives the actual angular quotient of the axisymmetric 4D
spacetime; its axis is a quotient edge, not a physical boundary.

## 6. Remaining limits of the diagram

The atlas does not determine all singular corner identifications at
infinite rider time, spatial infinity, or the excluded cap rim. It does
not replace the reduced diagram by a completed single 2+1 Penrose
domain, and it does not prove maximality of a capped continuation.
Its global content is the complete original horizon geometry, a cover
of the full original spacetime, the checked ordinary-scri contacts, and
the separate regular cap crossing charts. Those are what is drawn.

## Reproduction and checks

Run `exploration/capped_horizon_atlas.py`. The audit precedes drawing and
checks the global W, the cap parameters, independent near-rim starts,
the analytic unresolved-rim bound, matching to the exact straight
exterior, the null-surface equation, and full Hamilton geodesics with
conserved E=0. The independent geodesics remain within about 4e-13 of
the horizon; energy errors are below 8e-12. It also checks finite-u
scri contact limits and the unit timelike crossing against the actual
global W, not only against the local collar.

Outputs:

- `output/global_2p1/capped_horizon_check.json`
- `output/global_2p1/capped_global_horizon_atlas.png`
