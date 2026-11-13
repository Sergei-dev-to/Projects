# Joint angular limits and a corrected boundary coordinate

This completes the proposed boundary-identification calculation for the
regular cap and ordinary-scri pieces. It proves a uniform exclusion of
finite ordinary-scri points at the critical flow label and constructs a
corrected flow label giving a smooth full-angular scri chart. It does not
determine the topology of every exceptional infinite-time/spatial end or
produce a single global compact drawing.

## 1. A uniform theorem: the critical label cannot reach finite scri

Retain the global flow

\[
 F_t=v_0(F)+1+\epsilon(t),\quad F(0,A)=A,\quad
 \epsilon(t)=\eta\operatorname{sech}^2t,\quad\eta=0.05.
\]

Let A_* be the separating label whose trajectory tends to x=-1 as
t -> infinity. Define H(t,A)=t+F(t,A). Since v0>=-2,

\[
 H_t=v_0(F)+2+\epsilon(t)>0.
\]

Also H(t,A_*) -> infinity. Consequently, for **every** sequence
A_n -> A_*, t_n -> infinity,

\[
 H(t_n,A_n)\longrightarrow+\infty.
\]

Proof: given M choose a fixed t0 with H(t0,A_*)>M+1. Continuity in A
makes H(t0,A)>M for A sufficiently close to A_*. Monotonicity in t then
gives H(t,A)>M for all t>=t0 in that same neighborhood. No rate relation
between A-A_* and t is required.

At an arbitrary transverse position y, put X_lab=F+2t and
R=sqrt(X_lab^2+y^2). The radial retarded time obeys the exact inequality

\[
 \boxed{u=t-R\le t-X_{\rm lab}=-H(t,A).}
\]

Hence u -> -infinity for all the above sequences, **uniformly over arbitrary
y_n**, bounded or unbounded. The critical-label sector has no limit at
any finite-retarded-time point of ordinary future scri. This is stronger
than checking y fixed, y~sqrt(t), and y~t separately.

This statement concerns sequences of events. Many sequences with growing
y and fixed comoving x are not future causal observer trajectories.
It must not be interpreted as assigning all such sequences to the rider.

## 2. Why the uncorrected flow label fails at ordinary scri

For A<A_*, once its trajectory reaches the left exact-flat exterior,

\[
 F(t,A)=-t+\eta\tanh t+\mathcal B(A).
\]

The scattering function B is smooth and strictly increasing there:
B'=F_A>0 after exit. It maps (-infinity,A_*) onto R; for sufficiently
negative A it is exactly A, and it diverges as A approaches A_* from below.

At a large-radius event t=R+u, X_lab=R cos(theta), y=R sin(theta), define

\[
 \Delta=R(1-\cos\theta)=R-X_{\rm lab}\ge0.
\]

The **exact** relation in this exterior is

\[
 \boxed{u=-\mathcal B(A)-\eta\tanh t-\Delta.}
\]

Thus the same endpoint (u,theta=0) can be approached with different
limits of A:

- theta=0 gives Delta=0;
- theta~c/sqrt(R) gives Delta -> c^2/2 and y~c sqrt(R);
- theta=R^(-1/4) still tends to zero but Delta~sqrt(R)/2 -> infinity.

The last family has A -> -infinity even though its ordinary-scri endpoint
has the same finite u and angle as the first family. Therefore raw A
cannot be used as a continuous coordinate on that boundary. This is an
actual path-dependence error, not just a different visual convention.

## 3. The correction, its inverse, and its metric

Define, in the future exact-flat exterior,

\[
 \boxed{\bar A=\mathcal B^{-1}\bigl(\mathcal B(A)+\Delta\bigr).}
\]

Then B(Abar)=-u-eta tanh(t), and at scri

\[
 \bar A=\mathcal B^{-1}(-u-\eta).
\]

This limit depends on the endpoint, not the transverse approach rate.
The coordinates (Abar,r=1/R,theta) cover the whole angular cylinder of
ordinary future scri, with the ordinary periodic angle charts understood.

An explicit inverse near any compact set of finite u is:

1. Set R=1/r.
2. Solve u+eta tanh(R+u)=-B(Abar). Its derivative in u is
   1+eta sech^2(R+u)>0, so the solution is unique.
3. Set t=R+u, x=R cos(theta)-2t, y=R sin(theta).
4. If the original flow label is needed, recover
   A=B^(-1)(B(Abar)-R(1-cos(theta))).

This is an invertible three-dimensional transition, not just an axial
parameter relabeling.

The existing conformal factor is retained. In this exterior
Omega=1/sqrt(1+R^2), and the exact radial metric is

\[
 \widehat g=\frac{-r^2du^2+2du\,dr+d\theta^2}{1+r^2}.
\]

Let e=eta sech^2(R+u) and b=B'(Abar)>0. Differentiating the inverse gives

\[
 du=\alpha\,d\bar A+\beta\,dr,\qquad
 \alpha=-\frac b{1+e},\quad
 \beta=\frac{e}{r^2(1+e)}.
\]

At r=0, e and beta vanish to all orders on compact u intervals.
The one-sided tanh expression can be continued smoothly with value 1
across r=0; one must not substitute negative r into the original
physical-time expression, which would instead select the past branch.
The conformal metric has the regular boundary value

\[
 \boxed{\widehat g\big|_{r=0}
 =-2\mathcal B'(\bar A)\,d\bar A\,dr+d\theta^2,\qquad
 \det\widehat g=-\mathcal B'(\bar A)^2<0.}
\]

The full determinant before the limit is
-alpha^2/(1+r^2)^3. The r=0 normal is null. These formulas verify the
ambient metric, not only its induced angular metric.

## 4. Uniform transition domains

For a compact retarded-time interval |u|<=M and all angles,

\[
 x=R\cos\theta-2(R+u)\le -R+2M.
\]

Therefore R>2M+3 puts the entire angular collar in x<-3. Here the actual
profile is exactly flat, the comoving cutoff is exactly zero, and the
scattering formula applies. This is a uniform domain, including angular
sequences with y~sqrt(R), y~R, and intermediate rates.

For any compact cap set |lambda|<=L, |y|<=a-delta with delta>0,
x=1+q lambda stays in the actual affine profile collar and in cutoff=1
for all sufficiently small |q|. The polynomial cap metric from
`junction_blowup.md` and its positive conformal factor are uniformly
regular there. Its original flow labels lie in a compact subset of
A>A_*: the cap-to-flow transition is smooth at finite lambda, and no
finite lambda is the separating trajectory.

Thus finite cap neighborhoods and finite ordinary-scri neighborhoods
can be chosen disjoint (bounded versus uniformly large comoving
position), and they have explicit common-interior transition formulas.
There is no need to identify a finite cap point with a finite scri point.
All metric matching on the original interior uses the same Omega^2 g.

The cap rims |y|=a are excluded; the uniform argument does not adjoin them.
The exceptional limits u->-infinity, |lambda|->infinity, and the critical
flow label are also outside these compact regular-boundary domains.

## 5. Regular-boundary classification (before the causal analysis below)

| Sector | Coordinates that identify finite points | Status |
|---|---|---|
| Ordinary future scri | finite u and theta, equivalently Abar and theta | full angular, regular null boundary |
| Front cap crossings | finite lambda, |y|<a | regular physical continuation; Omega>0 |
| Critical flow-label approaches | A->A_*, t->infinity, arbitrary y | uniformly u->-infinity; no finite scri point |
| Stationary timelike interior approaches | bounded subsonic x,y, t->infinity | exceptional end; resolved metric degenerates in the current zoom |
| Cap rim | |y|->a at a crossing | excluded by the earlier extension obstruction |

Time reversal gives the corresponding past statements. The full circle
at ordinary scri is retained: the projective variables Q,Y,U used in
earlier notes are only one angular chart, with boundary relation
theta=2 atan(Y), u=U/(1+Y^2). Their missing direction is included by the
radial chart above.

This settles the finite-point angular identifications and regular
transition domains. Sections 6--10 below now identify the rider ends in
the causal boundary, but do not supply a smooth conformal vertex or a
classification of every other exceptional end.

## 6. The rider has one future causal endpoint and one past endpoint

All statements here concern the original stationary patch. Write

\[
 P=I^-(\gamma)=\{(t,x,y):x>-h(y)\},\qquad
 F=I^+(\gamma)=\{(t,x,y):x<h(y)\},
\]

where gamma(t)=(t,0,0), and put
D={ (x,y): -h(y)<x<h(y) }. The previous horizon calculation identifies
these sets; no new horizon equation is assumed here.

Use the intrinsic causal boundary: a future-inextendible timelike curve
defines a terminal indecomposable past set (TIP), its chronological past.
Curves with the same TIP define the same future endpoint. This definition
does not presume a conformally flat embedding or a regular boundary metric.
For the definitions, chronological topology and its relation to conformal
boundaries, see Flores, Herrera and Sanchez,
[On the final definition of the causal boundary and its relation with the
conformal boundary](https://arxiv.org/abs/1001.3270), especially Lemma 3.11
and Remark 3.13(B). Conformal and causal boundaries are not automatically
equivalent without additional hypotheses.

**Proposition.** Every future-inextendible timelike curve whose late
spatial projection stays in a compact subset K of D has chronological
past P. The time-reversed assertion gives future set F.

Proof. The coordinate t is temporal. Future causal curves have spatial
coordinate speed at most 3 because |v|<=2. If t had a finite upper limit,
their spatial coordinates would have finite limits, giving an ordinary
endpoint and allowing extension. Thus t tends to infinity.

Every tail point lies in P, so the past of the entire curve is contained
in P. Conversely, for every z in K there is a finite timelike trip from
the center to z, because K is contained in F. Openness of chronology
gives the same finite travel-time bound on a neighborhood of z. A finite
cover of K, stationarity and waiting on the central worldline give a
uniform bound B on these trips. If p is in P, choose s with p << gamma(s).
All sufficiently late points (t,z) of the curve satisfy t>s+B, and hence
p << gamma(s) << (t,z). This proves equality of the past sets.

In particular, all stationary timelike observers in the connected
subsonic region U={v>-1} define the same endpoint. For this explicit
profile U is star-shaped. On the radial path to any z in U, let
m=1-max_path |v|>0 and take spatial speed m/2 in either direction. Then
|spatial_velocity-v e_x|<=1-m/2<1, so the path is timelike and has finite
duration 2|z|/m. This directly verifies mutual communication with the
center without relying on the numerically computed horizon.

P is terminal: it contains central events at arbitrarily large t and
therefore cannot be the past of a finite event. Its common future in M
is empty for the same reason. Thus the corresponding full c-boundary
pair is unambiguously

\[
 \boxed{P_r^+=(P,\varnothing)},\qquad
 \boxed{P_r^-=(\varnothing,F)}.
\]

These are two individual causal points, not transverse curves or faces.
The result does not classify curves approaching the boundary of D, nor
sequences escaping every compact spatial set.

## 7. An exact convergence criterion using signal times

For a spatial location z define the infimum travel time

\[
 \tau_s(z)=\inf\{T>0:\gamma(0)\ll(T,z)\},
\]

and set tau_s=infinity if z cannot receive a signal. Stationarity and
waiting at the center imply

\[
 \gamma(s)\ll(t,z)\quad\Longleftrightarrow\quad
 s<t-\tau_s(z).
\]

The strict inequality follows also from openness of chronology at the
infimum. Thus E(t,z)=t-tau_s(z) is the supremum of possible rider emission
times for timelike signals arriving at (t,z).

**Criterion.** For a sequence p_n=(t_n,z_n) lying in the closure of P
(closure taken inside the physical spacetime), convergence to
P_r^+ in the chronological c-boundary topology is equivalent to

\[
 \boxed{E(t_n,z_n)\longrightarrow+\infty.}
\]

Necessity follows from openness of I^+(gamma(s)) for every finite s.
For sufficiency, put P_n=I^-(p_n). The assumption p_n in closure(P) gives
P_n subset P: if r<<p_n, the open set I^+(r) meets P near p_n, so r
belongs to the past set P. Every p in P precedes some gamma(s), and the criterion
places gamma(s) in P_n eventually. Consequently LI(P_n)=LS(P_n)=P.
Also t_n>=E(t_n,z_n) tends to infinity, so LI(I^+(p_n)) and LS(I^+(p_n))
are empty. These are exactly the defining chronological-limit conditions;
P is the unique maximal indecomposable past set in LS(P_n).

This is more informative than bounded coordinates plus t->infinity.
Travel time can diverge when approaching the sending boundary. Compact
subsets of D have uniformly bounded tau_s and do approach P_r^+; the
whole closure of D cannot be collapsed uniformly. Reverse time for P_r^-.

## 8. Which end of the regular cap attaches to the rider point?

For 0<x<1 on the axis, the exact infimum travel time is

\[
 S(x)=\int_0^x\frac{d\xi}{1+v_0(\xi)}.
\]

The axial outgoing null ray attains the infimum as a causal curve and
can be approximated by timelike trips. No transverse detour is faster:
v(x,y)<=v_0(x), hence dx/dt<=1+v_0(x) for any causal curve. Applying this
bound between a last crossing of x=0 and a first arrival at x gives the
same lower bound, even for paths that first detour to x<0.

In the exact quadratic collar, choose x_j=0.9 and define

\[
 c_s=S(x_j)-\log\frac{1+x_j}{1-x_j}+\log 2.
\]

Then, exactly for x_j<=x<1,

\[
 S(x)=-\log(1-x)+c_s+\log\frac{1+x}{2}.
\]

Use q=e^{-t}, lambda=(x-1)e^t. On the inner side lambda<0,

\[
 \boxed{E(t,x,0)=\log(-\lambda)-c_s-\log\frac{1+x}{2}.}
\]

At finite negative lambda, q->0 therefore gives a finite latest emission
time log(-lambda)-c_s, not the rider endpoint. In a joint limit x->1,
q->0, lambda->-infinity the emission time diverges, and the endpoint is
P_r^+. This also holds uniformly across the open planar aperture:
first moving at x=0 to y in |y|<a takes less than 2a coordinate time,
and the subsequent axial profile is independent of y. Consequently

\[
 S(x)\le\tau_s(x,y)\le S(x)+2a\qquad(|y|<a).
\]

Each finite regular front-cap point defines a TIP by timelike curves in
q>0 approaching it. For lambda<0 those curves have tails in P, so their
TIPs are subsets of P. Their latest central emission times obey the same
finite bounds above. As lambda->-infinity these TIPs exhaust P in the
set-limit sense, uniformly in y on compact subsets of the aperture.
Their future partners are empty because the approaching physical curves
have t->infinity. Hence the corresponding cap boundary points converge
to P_r^+ in the chronological topology as well.

This fixes one previously ambiguous attachment: the entire negative
infinite lambda end of the open front-cap face has one causal rider
endpoint. It does not identify the finite cap, the lambda>=0 end, or
the aperture rims with that endpoint. Time reversal fixes the analogous
past attachment. All statements about the front cap refer to its original
patch side; a chosen larger physical extension has its own causal boundary.

## 9. A causal obstruction to the old uniformly pinched tube

In any completion retaining the original chronology and making I^+(p)
open for physical p, no sequence on H_s=boundary I^+(gamma) can converge
to P_r^+. Indeed, gamma(s) precedes P_r^+ for every s. Openness would then
give gamma(s)<<p_n eventually, although no point of H_s can be reached
from gamma by a timelike curve. This is a contradiction. Similarly,
H_r cannot accumulate at P_r^-.

The converse horizon incidences can actually be proved. At any fixed
y_0 with h(y_0)>0, the receiving-horizon points (t,-h(y_0),y_0) lie in
closure(P) and in F. Their sending time tau_s is a fixed finite number.
Section 7 therefore gives

\[
 (t,-h(y_0),y_0)\longrightarrow P_r^+\quad(t\to+\infty).
\]

By time reversal, (t,h(y_0),y_0) on the sending horizon converges to P_r^-
as t->-infinity. These are sequences of events, not stationary timelike
observers; off the planar cap those fixed-position lines are spacelike.

At h(y_0)<=0 neither sending nor receiving horizon can approach either
rider endpoint by a fixed-position sequence. For the receiving horizon
there is no rider signal when x=-h>=h, excluding P_r^+; being on H_r
excludes P_r^- for every y. The sending statement is reversed. Thus
the intersection lines x=0, y=+/-C/sqrt(3) are not part of either rider
tip. This supplies a genuine incidence restriction on a global picture,
not just a smoothness warning.

An arbitrary
topological closure or conformal embedding with ill-behaved induced
boundary chronology need not obey this test. The test applies to the
standard c-boundary and to a proposed conformal diagram that claims the
same endpoint chronology with open chronological futures/pasts.

There is a concrete counterexample to the old tube closure. Take y_0=0.9
and x_0=h(y_0), which lies strictly between -1 and 1, on an outer sending
wing. Its events (t,x_0,y_0) cannot receive any rider signal. Nevertheless
the old map has

\[
 p=P_0(x_0)e^t\to\infty,\quad
 q_0=Q_0(x_0)e^{-t}\to0,\quad
 \alpha\to2,\quad\beta\to1,\quad\Omega y_0\to0.
\]

It therefore sends them to its displayed rider vertex (X,T)=(-1/2,3/2).
The failure is in the boundary topology, even though its finite-interior
coordinates and temporal-gradient check are valid. The earlier whole
closed-tube pinch is retired as a causal/conformal completion.

## 10. Causal points do not supply regular conformal vertices

The stationary timelike orbit x=0.95,y=0.3 belongs to the rider TIP proved
above. On this orbit, the already checked physical Cotton norm is

\[
 C_{abc}C^{abc}=9x^2(1-v_0^2)=0.77264012109375>0.
\]

Under g_hat=Omega^2 g this norm is multiplied by Omega^{-6}.
Thus a completion assigning the orbit an endpoint with Omega->0 cannot
have a nondegenerate C3 unphysical metric there. In the actual 4D product
cap the Weyl norm is (1+3x^2)^2/3>0 and scales as Omega^{-4}, giving the
corresponding C2 obstruction. See `corner_resolution_audit.md` for tensor
calculations and the conformal-invariance reference. These obstructions
do not assert a physical curvature singularity at finite rider time.

The causal identification and the smoothness question must therefore be
kept separate. A causal diagram can mark P_r^+ and P_r^- as singular ideal
points. Resolving approach directions into a curve or face in some other
compactification does not make them distinct rider TIPs, and by itself
does not repair the curvature obstruction.

What is still needed for a complete global drawing is the topology of
the remaining exceptional sequences: cap rims, other infinite-cap ends,
and spatial/horizon approaches outside the compactly trapped rider
sector. The c-boundary describes timelike-curve endpoints; it does not
automatically adjoin a spacelike infinity point. No complete global
conformal diagram, nor a theorem excluding every singular-boundary
diagram, is claimed here.

## 11. Finite-label rim ends form distinct singular families

Use q=e^{-t}, lambda=(x-1)e^t, retaining the transverse function psi(y)
instead of setting it to zero. In the affine profile collar the exact
metric is

\[
\begin{split}
g={}&q^2d\lambda^2-(2+q^2\lambda^2+\psi)d\lambda\,dq+dy^2\\
 &+\left[\lambda^2(1+\psi/2)+q^2\lambda^4/4
       +\frac{\psi+\psi^2/4}{q^2}\right]dq^2.
\end{split}
\]

Its determinant is -1 for q>0. At y=+/-a every derivative of psi
vanishes, so curves at the rim have exactly the product-cap equations.
For every finite lambda_0, take y=+/-a and
lambda(q)=lambda_0+Aq, with 2A>lambda_0^2. Its limiting squared tangent
norm is lambda_0^2-2A<0. Decreasing q is future directed, t tends to
infinity, and the remaining proper time is finite. These explicit
timelike curves define future TIPs at every finite rim label.

Different labels are not merely different approaches to the rider point.
To see this, normalize the signed outgoing coordinate

\[
 p=e^t f(x),\qquad f'= -f/(1+v_0),\qquad f(1)=0,
 \quad f'(1)=-1.
\]

In the quadratic collar f=2(1-x)/(1+x), and the cap limit is p=-lambda.
The function extends with f'<0 throughout x>-1. Future curves reaching
the front cannot have crossed x=-1 from the left. For any causal control
x'=v+u_x, y'=u_y, |u|<=1,

\[
 \frac{dp}{dt}=e^t(-f')\big[v_0-v+1-u_x\big]\ge0.
\]

At fixed rim y, an event with outgoing coordinate between two distinct
endpoint p-values can reach the larger endpoint value and cannot reach
the smaller one. Thus the TIPs are distinct. For two different limiting
transverse positions, in a collar where -f'>=m>0 the stronger bound is

\[
 p'(t)\ge\frac m2e^t y'(t)^2.
\]

A late event with bounded remaining p-budget can change y by at most
O(sqrt(q)). It cannot reach two endpoints separated by a fixed transverse
distance. Excursions out of the collar cannot evade this estimate: at
late t a fixed inner displacement would already require p of order e^t,
incompatible with a finite target p. This separates the two signed rim
families as well as the transverse labels of the open cap.

The finite rim labels therefore supply two one-parameter families
(lambda,+a) and (lambda,-a) in the signed 2+1 double. The angular quotient
retains one rim family; restoring the angle gives a circle times the
lambda label. This is a classification of these explicitly constructed
finite-label ends, not an assertion that all exceptional approaches
have been enumerated.

The physical C2 extension obstruction applies to every finite rim label,
not only to the stationary generator lambda=0. The outgoing axial null
geodesic with constant p and y=a has lambda->lambda_0, affine tangent
K=Q(e_0+e_1) with Q asymptotic to a positive constant times e^t, and
finite remaining affine length. The transverse vector e_y is parallel
along it. If it had an endpoint in a C2 extension, transverse geodesic
flow would supply a fixed-width disk with bounded transported curvature,
just as in the manuscript's rim proposition. At a fixed small transverse
offset r>0 its contraction is

\[
 Q^2 e^{\psi(a+r)/2}
 \left[-\frac12\psi''(a+r)-\frac14\psi'(a+r)^2\right].
\]

It diverges, since psi''>0 there. Hence these rim ends have no C2 physical
extension endpoint. Allowing singular rider points alone does not make
the rest of the boundary regular.

The displayed metric also explains why the naive rim chart fails:
approaches with psi=zeta q^2 have g_qq->lambda^2+zeta, whereas approaches
inside the aperture have g_qq->lambda^2. This is a chart-level path test,
not by itself a coordinate-invariant C0 inextendibility theorem.

There is useful control on causal approaches. If x->1 and p has a finite
limit, integration of the bound above gives a transverse limit y_infty
with

\[
 |y(t)-y_\infty|^2\le\frac{2q}{m}[p_\infty-p(t)]=o(q).
\]

Also |y_infty|<=a: otherwise v0-v has a positive lower bound and p' would
grow like e^t. At a rim limit the infinitely flat psi is then smaller
than every power of q along that causal curve. The dangerous generic
coordinate approaches psi~q^2 are therefore not finite-p causal curves.
This does not remove the neighborhood obstruction just proved.

## 12. Escape from outside the closed receiving region

This lemma controls the ordinary-infinity sectors and rules out hidden
trapping in the argument below. Set G=x+h(y), so P={G>0}.

For the specified profile h is positive throughout |y|<=Y_E. This does
not rely on subtracting near-rim numerical values. First |h'|<=sqrt(3)
implies |h|<=1 on [a,Y_E]. Then Phi=h^2+psi-1<=psi, and

\[
 h(Y_E)\ge1-\int_a^{Y_E}\sqrt{W(\psi(y))^2-1}\,dy>0.2673.
\]

The last bound is checked by an upper right Riemann sum of the monotone
integrand; its positive margin is much larger than floating-point error.
One can equally use h>0 on this interval as an explicit hypothesis of
the following lemma for other profiles.

If G<0 and |y|<=Y_E, then x<-h(y)<0. Monotonicity in |x| gives

\[
 \dot G\le v(x,y)+\sqrt{1+h'^2}
          =v(x,y)-v(-h(y),y)\le0.
\]

For |y|>=Y_E the same bound holds exactly because v=-2 and |h'|=sqrt(3).
Thus a causal curve starting with G=-delta<0 keeps G<=-delta.
In the nonflat strip its profile argument satisfies

\[
 x^2+\psi-1\ge(h+\delta)^2+\psi-1\ge\delta^2.
\]

Consequently everywhere along the curve

\[
 \dot x\le1+W(\delta^2)=-\epsilon_\delta<0.
\]

It reaches x<-3 in uniformly bounded coordinate time, at most
(x_initial+3)_+/epsilon_delta (with a slightly later time for strict
x<-3). That exact-flat left region is future invariant. At any fixed
such escape time the reachable set is compact, by bounded coordinate
speed and global hyperbolicity. These facts hold uniformly over all
causal choices from the fixed initial event.

## 13. A two-limit theorem at the Mach half-generators of scri

Let theta_M=pi/3 and u_M=-C/2. Choose u_0<u_M and let Q be the ordinary
future-scri endpoint (u_0,theta_M). Take

\[
 Q_n=(u_0,\theta_n),\qquad\theta_n<\theta_M,\quad
 \theta_n\longrightarrow\theta_M,
\]

with theta_n near theta_M so 2 cos(theta_n)-1>0. Denote their TIPs by
B_n, and the TIP of Q by B. Every ordinary-scri point here can be
represented by an asymptotically null timelike curve in the exact-flat
left exterior, so these are actual indecomposable terminal past sets.

**Claim:** in the standard chronological c-boundary topology the same
sequence Q_n converges both to Q=(B,empty) and to P_r^+=(P,empty).
In particular this boundary is non-Hausdorff.

First P is contained in every B_n. An event in P reaches the rider at
some finite time. The rider can then wait until T and take the same
fixed timelike trip to x=-3,y=0, with duration D. At its flat exit the
retarded plane value in direction theta_n is

\[
 b_n=(1-2\cos\theta_n)(T+D)+3\cos\theta_n.
\]

It tends to -infinity as T grows. Taking b_n<u_0 permits a timelike
continuation through the future-invariant flat exterior to Q_n. This
works however late the initial rider event was.

Second, B is contained in LI(B_n). Any event in B reaches a finite point
on a timelike curve ending at Q. In the flat final portion the strict
retarded-time inequality persists under small changes of theta, giving
membership in B_n for all sufficiently large n.

Third, P and B are incomparable. No rider event belongs to B: at the
Mach angle, late physical points approaching Q satisfy

\[
 x-h(y)=-2u_0-C=2(u_M-u_0)>0,
\]

so they are outside the rider's sending region. Conversely, choose an
exact-flat event x=-3,y=10,t=0. Its Mach retarded value is
1.5-5 sqrt(3), below the chosen u_0=u_M-1, and G<0. It belongs to B but
not P. For any other finite u_0<u_M, increase y to obtain such a witness.

Finally, there is no larger IP in LS(B_n) containing either P or B.
Here is the step that excludes merely inferring non-Hausdorffness from
discontinuous pasts. Suppose an IP J contained in LS(B_n) is not contained
in P. Since J is open it contains some event z outside closure(P).
Given any r in J, indecomposability supplies w in J with z,r<<w.
The escape lemma places w outside closure(P) as well. Along a subsequence
for which w is in B_n, take connecting curves from w to Q_n. At a fixed
uniform escape time, their intermediate points have a convergent
subsequence in a compact reachable set. Their limiting point is causally
reachable from w, and its flat retarded value at theta_M is <=u_0.
It therefore has a causal continuation to Q. The push-up property with
r<<w gives r in B. Thus J is contained in B.

Every IP in LS(B_n) is consequently contained in P or in B. Both are
contained in LI(B_n), and neither contains the other. They are exactly
the two maximal IPs in LS(B_n). This proves the claim by the defining
chronological limit operator (Flores--Herrera--Sanchez, equation (3.6)).
All future partners are empty because the defining curves have t->infinity.

Reflection gives the lower Mach half-generator and time reversal the
corresponding past statement. The theorem needs only one chosen u_0<u_M
to establish the obstruction; it does not rely on the focal point u=u_M.

## 14. Which large-label ends have causal limits?

There are also definite conclusions about the ends sometimes lumped
together as spatial infinity.

* At fixed finite cap y, lambda->-infinity approaches P_r^+, as proved
  above. The same signal-time bounds apply to the canonical rim families.
* As lambda->+infinity, the cap's outgoing label p=-lambda tends to
  -infinity. Monotonicity of p excludes every fixed physical event from
  the corresponding TIPs eventually. Points with x<=-1 cannot reach
  this front cap at all. Thus LI=LS=empty: there is no future c-boundary
  limit. Adding a spatial ideal point or face is extra completion data.
* At fixed ordinary-scri direction with 2 cos(theta)>1, taking u->-infinity
  has the rider endpoint as its chronological limit. P lies in every
  TIP by the waiting argument. The escape lemma excludes any event
  outside closure(P) from the limsup, so P is its unique maximal IP.
* At fixed direction with 2 cos(theta)<=1, u->-infinity has no future
  c-boundary limit. For a fixed initial event, every final exit from the
  compact nonflat region has retarded value
  (1-2 cos(theta))t_exit-n dot z_exit, bounded below since t_exit is bounded
  below and z_exit lies in a fixed compact set. Curves that never enter
  that region obey the ordinary flat bound from their initial event.
  Every fixed event therefore drops out of the past sets.
* At fixed angle, u->+infinity has TIP=M, the ordinary exterior i^+.
  Any fixed event can escape left in finite time and then reach all
  sufficiently late retarded-time endpoints in that direction.

These statements concern causal limits, not the Euclidean shape of a
compactified drawing. The directional change at the Mach angle and the
two-limit result explain why assigning a single ordinary spatial corner
has repeatedly failed. Merely adjoining a point for the empty-set limit
does not eliminate the two distinct nonempty TIP limits of section 13.

## 15. Consequence for the requested global diagram

The verified boundary data now include singular rider points, distinct
finite-label rim families, the cap's two different large-label ends,
ordinary scri's directional large-label limits, and a non-Hausdorff
incidence at the horizon contact. This is enough to disprove the proposed
assembly as an ordinary Hausdorff solid faithfully representing the
standard chronological c-boundary, even if the rider tips are allowed to
be singular. A sequence in a Hausdorff space cannot have the two distinct
limits proved in section 13. Identifying them would also discard their
different chronological pasts.

This is NOT a proof that every Hausdorff conformal completion with a
different boundary topology is impossible. At singular ends, equivalence
between conformal and causal boundaries is an additional requirement,
not an automatic theorem. Nor have we proved an exhaustive classification
of all possible future TIPs or all mixed cap-rim/spatial sequences. The
result changes the completion problem: a faithful standard c-boundary
needs a non-Hausdorff incidence description; a Hausdorff conformal drawing
would need an explicitly different topology and a fresh compatibility
analysis. We should not label either a finished global conformal diagram.

## 16. A global coordinate closure without imposing the c-boundary topology

The construction below returns to the conformal metric. It gives one
bounded coordinate domain for the ENTIRE original signed meridional
spacetime, with an explicit inverse characterization. It is not an atlas
whose boundary pieces have yet to be assembled. Ordinary null infinity
and the open cap crossings are regular in these same global coordinates;
the residual boundary is allowed to be singular and to retain approach
directions. This is a global conformal-metric representation with a
singular boundary, not an everywhere-regular Penrose completion.

In particular it does not impose the chronological c-boundary topology.
Stationary observers with the same TIP can have different locations on
the resolved singular face. The central rider itself has one definite
point there. These extra labels describe approaches, not new physical
events. Some residual faces resolve ordinary timelike/spacelike infinity
and are artifacts of this nonminimal compactification.

Put w=(t,X,y), X=x+2t, R=sqrt(X^2+y^2), and define

\[
 H(r)=\sqrt{1+r^2}-\log(1+\sqrt{1+r^2}),\qquad
 h(z)=H'(z)=\frac{z}{1+\sqrt{1+z^2}},
\]

where H is even when its argument is signed. Let Q(t)=log(1+e^{-t}),
k=1/a=5/3, and choose the presentation constants

\[
 A=1,\quad B=0.15,\quad\beta=1.45,\quad c=d=0.04.
\]

Define three convex potentials:

\[
\begin{split}
 \Phi_E(w)&=A H(\sqrt{t^2+R^2})+B[H(t+R)+H(t-R)],\\
 \Phi_+(w)&=\beta X+cH(\sqrt{x^2+k^2y^2})
                 +d\sqrt{(x-1)^2+Q(t)^2}-2,\\
 \Phi_-(w)&=\Phi_+(-w).
\end{split}
\]

The apparent R=0 singularity in Phi_E is removable: the sum is an even
smooth function of R, and its spatial Hessian there is 2B h'(t) times
the identity, in addition to the positive radial-H term.

Use a smooth convex maximum M. Explicitly, with width b_0=0.15,

\[
 M(a,b)=b+m(a-b),\qquad
 m'(z)=S((z+b_0)/(2b_0)),\quad m(-b_0)=0,
\]

where S is the earlier infinitely flat step; extend m=0 for z<=-b_0
and m=z for z>=b_0. Symmetry of S makes M symmetric. Finally set

\[
 \boxed{\Phi=M(\Phi_E,M(\Phi_+,\Phi_-)),\qquad Z=\nabla_w\Phi.}
\]

This is one formula, evaluated at every physical event. The max is exact
outside a finite transition interval, not a log-sum approximation with
uncontrolled tails at a cap.

## 17. Global injectivity and the exact closed drawing domain

The radial-H Hessian is positive definite. Phi_E is therefore strictly
convex. For Phi_+, the spatial H term controls the x,y directions, while
the norm term controls t and x. Indeed for s=x-1 and q=Q(t), the Hessian
of sqrt(s^2+q^2) in (s,t) has determinant

\[
 \frac{q^3 Q''(t)}{(s^2+q^2)^2}>0
\]

and a positive ss entry. Phi_- has the same property. The Hessian of a
smooth convex maximum is a convex combination of the branch Hessians
plus a nonnegative gradient-difference outer product. Thus

\[
 J=\nabla^2\Phi>0
\]

at every finite event. Strict convexity makes Z injective; the inverse
function theorem makes it a local diffeomorphism.

There is also an exact description of its image. Let n=(n_t,n_X,n_y),
r_n=sqrt(n_X^2+n_y^2), and
L n=(n_X-2n_t,k n_y). Define the homogeneous support functions

\[
\begin{split}
 h_E(n)&=A|n|+2B\max(|n_t|,r_n),\\
 h_+(n)&=\beta n_X+c|Ln|
     +d\sqrt{(n_X-2n_t)^2+\min(n_t,0)^2},\\
 h_-(n)&=-\beta n_X+c|Ln|
     +d\sqrt{(n_X-2n_t)^2+\max(n_t,0)^2},\\
 h_K(n)&=\max(h_E(n),h_+(n),h_-(n)).
\end{split}
\]

These are support functions of compact convex bodies; K is the convex
hull of the three bodies. Uniformly in direction,
Phi(w)=h_K(w)+O(log(2+|w|)). For every Z in int(K), the function
Phi(w)-Z dot w is therefore coercive and strictly convex, so it has a
unique minimizer. Its stationarity condition is grad(Phi)=Z.
Conversely strict convexity along every ray gives grad(Phi(w)) dot n
<h_K(n). Consequently

\[
 \boxed{Z:\mathbb R^3\longrightarrow\operatorname{int}K
        \text{ is a global diffeomorphism}.}
\]

The inverse is concretely the unique minimizer just specified; Newton
iteration using the positive Hessian implements it. The compact closure
K is a single Hausdorff three-dimensional convex body. Every escaping
sequence has subsequential limits on its actual boundary; no additional
gluing instructions are needed to assemble the drawing.

## 18. The conformal metric on that whole domain

Keep the global positive factor Omega from section 1 of
`proper_conformal_completion.md`: the smooth comoving cutoff blends the
cap factor with (1+R^2)^(-1/2). In laboratory coordinates the physical
metric is

\[
 g_w=-dt^2+[dX-(v+2)dt]^2+dy^2.
\]

On int(K), define

\[
 \boxed{\widehat g_Z=\Omega^2 J^{-T}g_wJ^{-1}.}
\]

This is the actual rescaled Alcubierre metric, with
det(g_hat_Z)=-Omega^6/(det J)^2<0. All interior light cones are preserved.
Neither Z_t nor the height of the Euclidean rendering is asserted to be
a temporal function. The drawing is not an embedding into a flat
Lorentzian three-space and does not assign a universal 45-degree rule.

The construction is coupled to the two regular boundary scales. At
ordinary scri Phi_E is eventually selected EXACTLY; at bounded comoving
future ends Phi_+ is eventually selected exactly. The uniform recession
gaps proving these assertions are

\[
 A\sqrt2+2B-[\beta+3c+\sqrt{10}d]=0.017722455966\ldots>0,
\]

\[
 2\beta-[A\sqrt5+4B]=0.063932022500\ldots>0.
\]

Here k^2<=3 bounds |Ln|<=3 on laboratory future/past null directions.
The logarithmic subleading terms cannot defeat a positive linear gap.
For each compact set of finite boundary labels the selection is uniform.
At finite radii one must still use the full global formula; replacing it
prematurely by an asymptotic branch is not valid.

## 19. Ordinary scri is regular in the GLOBAL Z coordinates

For future scri use r=1/R, u=t-R, and direction n=(cos(theta),sin(theta)).
The exact limiting global coordinates are

\[
 Z_t=\frac A{\sqrt2}+B[1+h(u)],\qquad
 (Z_X,Z_y)=\left[\frac A{\sqrt2}+B(1-h(u))\right]n.
\]

Thus the entire finite-u future scri is a conical frustum of the SAME
convex body, with equation

\[
 Z_t+\sqrt{Z_X^2+Z_y^2}=A\sqrt2+2B.
\]

The past face is its central reflection. All angles are included.
Writing R_Z=A/sqrt(2)+B(1-h(u)), the boundary Jacobian in (r,u,theta)
has columns

\[
\begin{split}
 Z_r&=\left(\frac{Au}{2\sqrt2}-\frac{A+B}2,
       [-\frac{Au}{2\sqrt2}-\frac{A+B}2]n\right),\\
 Z_u&=B h'(u)(1,-n),\qquad Z_\theta=(0,R_Z n_\perp),
\end{split}
\]

and determinant (A+B)B h'(u)R_Z>0. It is a genuine boundary coordinate
change, not a map that loses its normal derivative. The already checked
metric

\[
 \widehat g=\frac{2du\,dr-r^2du^2+d\theta^2}{1+r^2}
\]

therefore remains smooth, Lorentzian and nondegenerate in Z at every
finite-u, finite-angle boundary point. Omega has a simple zero there,
and the normal of the displayed frustum is null in this metric.

The sending wings attach at theta=+/-pi/3, u<=u_M=-C_h/2, exactly as
derived earlier (C_h denotes the horizon intercept). Their equation
r(u-u_M)+1-cos(theta-theta_M)=0 supplies explicit approaching sequences.
Substitution into the ONE global coordinate map gives the stated scri
points. The fixed-generator endpoints are the cut u=u_M. Receiving wings
have the time-reversed attachment. These relations are drawn, rather
than guessed from proximity of surfaces.

## 20. Cap, rim, and rider attachments on the global planar faces

The exposed future bubble face has normal (1,2,0) and equation

\[
 \boxed{Z_t+2Z_X=2\beta.}
\]

Its shape is an elliptical disk plus a line segment: in vector notation
beta e_X+c L^T(B^2)+d[-1,1](-2,1,0). It is part of the boundary of K,
not a separately positioned inset. The past face is its reflection.

Use the physical cap variables q=e^{-t}, lambda=(x-1)/q. Put

\[
 a_q=\frac{\log(1+q)}q,\quad a_0=1,\quad
 s=\sqrt{1+(1+q\lambda)^2+k^2y^2},\quad
 b_q=\sqrt{\lambda^2+a_q^2}.
\]

The exact selected branch of the global coordinate formula is

\[
\begin{split}
 Z_X&=\beta+\frac{c(1+q\lambda)}{1+s}+\frac{d\lambda}{b_q},\\
 Z_y&=\frac{ck^2y}{1+s},\\
 Z_t&=-\frac{2c(1+q\lambda)}{1+s}
       +d\left[-\frac{2\lambda}{b_q}
       -\frac{q a_q}{(1+q)b_q}\right].
\end{split}
\]

It is smooth for signed q near zero. At q=0, write s_0=sqrt(2+k^2y^2)
and f_yy=k^2/(1+s_0)-k^4y^2/[s_0(1+s_0)^2]>0. Its Jacobian satisfies

\[
 \det\frac{\partial Z}{\partial(q,\lambda,y)}
   =-\frac{c d^2 f_{yy}}{(1+\lambda^2)^2}\ne0.
\]

The physical cap metric tends to
lambda^2 dq^2-2 d lambda dq+dy^2, and Omega tends to
(1+lambda^2)^(-1/2)>0 for |y|<a. Hence the rescaled metric is regular,
Lorentzian and nondegenerate at every open cap point IN THE GLOBAL Z
COORDINATES. The face normal is null. Signed negative q gives its regular
local physical continuation outside K; such a continuation is not a
crossing of ordinary null infinity.

The rim curves y=+/-a have explicit locations from the same formula.
They are singular boundaries of the regular cap strip. Mixed wall/rim
approaches are also checked: the wall equation gives
psi(y)=1-(1+q lambda)^2. For fixed negative lambda, q->0 puts y->a from
outside and lands at that particular finite rim label. Thus these limits
fill the appropriate rim segment instead of collapsing to the rider.

For fixed x!=1,y and t->infinity the boundary coordinate is

\[
\begin{split}
 Z_X&=\beta+\frac{cx}{1+\sqrt{1+x^2+k^2y^2}}
                       +d\operatorname{sgn}(x-1),\\
 Z_y&=\frac{ck^2y}{1+\sqrt{1+x^2+k^2y^2}},\qquad
 Z_t=-2(Z_X-\beta).
\end{split}
\]

In particular the central rider ends at (Z_t,Z_X,Z_y)=(0.08,1.41,0).
The fixed outer sending-wing point y=0.9, x=h(0.9) ends at approximately
(0.0557758,1.4221121,0.0330942), not at the rider. This explicitly removes
the old incorrect identification.

The limits lambda->+/-infinity of the cap strip join the two stationary
face curves x->1 from the corresponding side. They are not collapsed
onto the rider in this resolved conformal closure. That is an intentional
difference from the chronological c-boundary, not a contradiction.

There is also a separating-functional gap between the entire closed
ordinary-scri frusta and the future bubble face:

\[
 2\beta-[3A/\sqrt2+4B]=0.17867965644\ldots>0.
\]

Consequently no finite cap crossing or rider face point is accidentally
identified with ordinary null infinity. The residual spatial boundary
of the single body joins these faces and retains the intervening approach
directions. There is no unassigned geometric junction in this coordinate
closure, although the rescaled metric is singular on residual pieces.

## 21. What the completed drawing does and does not establish

This now supplies one global bounded domain, one globally injective map
and inverse prescription, one conformal metric, and checked attachments
of all advertised regular boundary pieces. The image is therefore drawn
as a single three-dimensional object, with a magnification of one of its
actual planar faces. The standalone HTML viewer rotates this same object.

The singular set is the residual boundary after removing ordinary finite-
cut scri and the two open physical cap strips. We make no claim of a
continuous nondegenerate unphysical metric throughout that residual set.
It includes the cap rims, resolved stationary ends, and extra resolution
of ordinary timelike/spatial directions. Its labels are coordinate
approach data. We have not claimed these faces to be canonical, intrinsic
physical singularities, or extra regions of the physical extension.

Thus, if "conformal compactification" is required to mean a smooth
nondegenerate ambient metric at EVERY boundary point, this construction
does not satisfy that stronger definition. It does meet the present
singular-boundary drawing specification while preserving the actual
metric and verifying regularity at scri and the cap crossings. It is not
a maximal physical extension, nor a homeomorphic realization of the
standard c-boundary. No manuscript figure has been replaced automatically.

## 22. A useful physical 2+1 view, paired with a regular cap detail

The convex coordinate closure above is not a satisfactory causal
illustration: its displayed height is not temporal and its Euclidean
shape does not show the light cones. The current visualization instead
uses the actual finite-time geometry, with a separate, explicitly matched
regular cap neighborhood. It is intended to supplement the axial 1+1
Penrose diagram, not replace it by a flat-cone 2+1 drawing.

The main view uses (x,y,t), with g^{-1}(dt,dt)=-1. It shows the stationary
null sheets x=h(y) and x=-h(y) over -2<=t<=4, the overlap
-h(y)<x<h(y), the rider at x=y=0, and the planar patches |y|<a. The
top/bottom mesh edges are finite plotting cuts, not infinity or cap
crossing surfaces. The red rim worldlines likewise mark the boundary of
the planar horizon patch; their finite-t points are ordinary events.

The small wire cones consist of frozen tangent vectors
(dx,dy,dt)=(v+cos(alpha),sin(alpha),1), scaled for display. They are not
drawn as finite geodesic segments. Actual null rays emitted by the rider
are integrated separately using the stationary null Hamiltonian

\[
 E=v p_x+\sqrt{p_x^2+p_y^2},\qquad
 \dot x=v+p_x/|p|,\quad\dot y=p_y/|p|,\quad
 \dot p_x=-v_xp_x,\quad\dot p_y=-v_yp_x.
\]

The displayed rays conserve E and remain on the reachable side of the
sending horizon. Colored curves on the sheets follow their null
generators. A constant-time cross-section makes the transverse lens,
planar aperture and outward horizon wings explicit.

The cap detail uses the exact product coordinates

\[
 X=(p+q)/2,\quad T=(p-q)/2,\qquad
 g=C(pq)(dX^2-dT^2)+dy^2,\quad C>0.
\]

Here g^{-1}(dT,dT)=-1/C<0. Longitudinal null curves at fixed y have
dX=+/-dT; the viewer includes an axial projection in which those
directions are at 45 degrees. The transverse cone opening is controlled
by C, rather than silently assigned a flat-space value. At q=0 the
normalization gives C=2, so the displayed tangent cone has dy/dT=
sqrt(2) sin(alpha), dX/dT=cos(alpha). Perspective and the explicitly
compressed transverse axis in the static close-up are presentation
choices, not claims about Euclidean angles of all null directions.

The magenta curve is the SAME unit timelike geodesic from the checked
FrontCollar construction, at y=0.3. In the original patch its events are
reconstructed by x=F^{-1}(pq), t=log(Q(x)/q), q>0. In the cap chart the
geodesic continues through q=0 with finite proper time and increasing T.
The plotted original segment begins at t approximately 2.19764 and is
cut at t=4; it has not crossed the cap at that finite cut. The cap detail
shows the actual crossing at proper time approximately 0.056184 after
the chosen initial event. The two coordinate descriptions agree at
shared events to approximately 2.6e-15.

No curve is continued across the rim, and the regular cap is not labeled
as ordinary null infinity. The main view covers a finite-time body and
the close-up covers a regular cap neighborhood: this is explicitly a
paired geometry illustration, not a completed global conformal diagram.

## 23. Connecting the useful view to the axial conformal diagram

`exploration/connect_2p1_penrose.py` uses the SAME globally bounded capped
profile and traveler as section 22. In the entire planar slab |y|<0.6,
the shift is independent of y. Consequently the selected y=0.3 slice is
totally geodesic and isometric to the axial 1+1 metric. The black stationary
observer in this slice has the same reduced trajectory as the central rider.
This identification does not extend to slices through the curved wings.

Write v0(x)=W(x^2-1), and define optical coordinates u=t+f(x), w=t+g(x),
where f'=-1/(v0+1) and g'=1/(1-v0). Numerically integrate the smooth
remainder

\[
 R'(x)=-\frac{1}{v_0(x)+1}+\frac{2}{1-x^2},\quad R(0)=0,
 \qquad G'(x)=\frac{1}{1-v_0(x)},\quad G(0)=0.
\]

The residual R' vanishes identically in the exact affine collars of both
roots. If s is the FrontCollar scale and h(x)=2 arctan(x/sqrt(3))/sqrt(3),
choose

\[
 f(x)=\log\left|\frac{1-x}{1+x}\right|+R(x)+\log s-R(1),
 \qquad g(x)=G(x)-[G(1)-h(1)]-\log s.
\]

These constants give exp(u)=p on the interior side of the front collar,
exp(u)=-p on its exterior side, and exp(-w)=q on both original sides.
Compactify using

\[
 \alpha=\begin{cases}
 \frac23[\pi-\arctan(e^u)]-\frac\pi6,&x<-1,\\
 \frac23\arctan(e^u)-\frac\pi6,&-1<x<1,\\
 -\frac23\arctan(e^u)-\frac\pi6,&x>1,
 \end{cases}
 \qquad \beta=\frac\pi2-2\arctan(e^{-w}),
 \quad (\mathsf X,\mathsf T)=\left(\frac{\beta-\alpha}{2},
                                      \frac{\beta+\alpha}{2}\right).
\]

Both null families are exactly at 45 degrees in this 1+1 diagram. The
pullback of dX^2-dT^2 is a positive multiple of the physical axial metric.
Across the front generator the signed coordinate p makes alpha smooth;
across the rear generator the same is true in the signed exp(-u) coordinate.
The front collar is exactly

\[
 \alpha=-\pi/6+(2/3)\arctan p,\qquad
 \beta=\pi/2-2\arctan q,
\]

which continues smoothly through q=0. Thus the continuation in this figure
is the actual regular cap chart, not a separately positioned schematic box.
The displayed added rectangle is -0.32<=p<=0.7, -0.14<=q<=0. Its vertices
and the monotonicity of F(x)=pq ensure |x^2-1|<0.25 throughout, so it stays
within the exact affine cap collar. Dotted outer edges are chart cuts.

The boundary limits are:

* Ordinary future null infinity: alpha=pi/2, or beta=pi/2 with alpha>pi/6.
* Future front-cap boundary: beta=pi/2, -pi/2<alpha<pi/6.
* Front generator endpoint C+: alpha=-pi/6, beta=pi/2.
* Rider future endpoint P+: alpha=pi/6, beta=pi/2.
* Ordinary past null infinity: alpha=-pi/2, or beta=-pi/2 with alpha<-pi/6.
* Past rear-cap boundary: beta=-pi/2, -pi/6<alpha<pi/2.

For example, in the exactly flat exterior x tends to minus infinity on
either future null family: w constant gives alpha=pi/2, while u constant
in the rear exterior gives beta=pi/2 and alpha>pi/6. The affine distance
diverges there. In contrast, finite p with q tending to zero approaches
x=1 with finite traveler proper time, even though t tends to infinity.
These limiting statements, not the apparent shape of a diamond edge,
distinguish ordinary null infinity from the cap boundary.

The traveler crosses at alpha approximately -0.166238, strictly between
C+ and P+. Events A (initial) and B (t=4) appear in both views; E is the
crossing. The same-event discrepancy is about 1.3e-13. Independent finite
differences check the optical null equations, conformal pullback, and
future temporal orientation in all three regions. An escaping w-constant
ray illustrates the separate ordinary-scri endpoint.

This is an exact axial conformal coordinate construction rendered with
numerical curves, paired with the physical 2+1 view. It does not establish
a smooth higher-dimensional conformal boundary at the rider ends, extend
through the cap rims, or claim maximality of the displayed added patch.

## 24. Transverse wings: cap strip versus angular null infinity

`exploration/horizon_boundary_attachments.py` makes the connections to the
section 23 diagram explicit, retaining the signed meridional view used in
the physical figure. Folding y and -y gives the angular quotient; it is
not necessary to interpret the double as an extra azimuthal dimension.

The cap line q=0 in the reduced diagram becomes the open null surface

\[
 \mathcal C^+=\{q=0,\ p\in\mathbb R,\ -a<y<a\},\qquad a=0.6.
\]

The physical metric is C(pq) dp dq+dy^2, with C(0)=2. Its restriction
to the cap is dy^2: p is the null direction within the strip. The planar
sending-horizon patch is p=0,q>0, and its generator endpoints form
the spacelike curve p=q=0, -a<y<a. This is what the reduced C+ point
becomes. The traveler crosses at p approximately 0.59406,y=0.3, so the
crossing event is not on that C+ curve. The rim curves y=+/-a remain
excluded from the regular extension; nothing here repairs them.

At any finite t the entire sending horizon is the single smooth sheet
x=h(y). It is x=1 within the planar patch and bends into the outer wings.
The finite-time joining of these pieces does not imply that their limiting
endpoints lie on the same regular boundary surface. In the exact flat
exterior, h(y)=C_h-sqrt(3)|y|, C_h approximately 2.637158424722. In lab
coordinates X=x+2t the upper and lower wings satisfy

\[
 t=n_\pm\cdot(X,y)+u_M,\quad
 n_\pm=(1/2,\ \pm\sqrt3/2),\quad u_M=-C_h/2.
\]

These are null planes. Their future null generators have constant
laboratory velocity n_+ or n_- and infinite future affine length. For any
fixed generator (X,y)=z_0+n_\pm t on its plane,

\[
 \theta\longrightarrow\pm\pi/3,\qquad
 u=t-|(X,y)|\longrightarrow u_M.
\]

Thus fixed outer generators end at the two points Q+ and Q- of ordinary
future null infinity. These are distinct from all finite cap crossing
points and from the cap C+ curve. The finite sample events F+ and F-
are t=0,y=+/-1.6,x=h(1.6); the figure tracks exactly the same generators
through those events in its physical and exterior panels.

The full closure of each wing is larger than the endpoint of one fixed
generator. Put r=1/R, theta=arg(X+iy). The wing equation is exactly

\[
 r(u-u_M)+1-\cos(\theta-\theta_M)=0,
 \qquad \theta_M=\pm\pi/3.
\]

For r>0 this implies u<=uM. For every fixed deficit d=uM-u>0, choosing
theta=thetaM+/-arccos(1-r*d) gives points on the wing approaching the
ordinary-scri point (u,thetaM). The closure is consequently the half-line
theta=thetaM,u<=uM. This varies the generator while taking the limit;
it must not be described as the endpoint of a single light ray.

Ordinary future null infinity itself has coordinates (u,theta) with theta
periodic, so in the signed 2+1 view its regular part is a null cylinder
R x S^1. In the exterior,

\[
 r^2g=2\,du\,dr-r^2du^2+d\theta^2.
\]

The induced metric at r=0 is dtheta^2. The two future-scri components
visible in the 1+1 slice select the generators theta=0 and theta=pi of
this cylinder. They are drawn as green dashed lines, while the wing
contacts are the distinct theta=+/-pi/3 half-lines.

For display only, the exterior panel uses
(cos(theta)/(1+2r),sin(theta)/(1+2r),u). This is an injective boundary
coordinate display for finite r>=0 and periodic theta, not a flat Lorentzian
embedding. The selected u range has artificial top and bottom cuts.
Only surface points with |y| above the exact flat-exterior threshold are
rendered. The cap and physical panels use their own stated coordinates;
the relation is supplied by matched events and the equations above,
not by drawing an unproved smooth bridge from cap rim to null infinity.

Numerical checks rerun the horizon audit, confirm the exact null-plane
equation and generator trajectories, and construct sequences reaching
the wing closure below uM. The same-event and plane residual is below
1.2e-13; the closure sequence residual is below 4e-12. The corresponding
rear/past relations follow under (t,x,y)->(-t,-x,y).

## 25. One coordinate picture of the front/future attachments

`exploration/unified_attachment_view.py` places the physical horizon,
regular cap, actual generator curves and ordinary future null infinity
in one shared coordinate system. It reuses Z=grad(Phi) from sections
16--21 for this limited purpose. That map was rejected as an effective
time-oriented Penrose visualization; this figure does not reinstate
that interpretation. It is explicitly an attachment map with a
non-temporal display height.

To make the small cap visible, apply the SAME presentation diffeomorphism
to every vertex, curve and limiting boundary point:

\[
 H=Z_t+2Z_X,\quad
 X_d=Z_X+0.24\log(1+e^{(Z_X-1.1)/0.08}),
\]
\[
 Y_d=Z_y+0.4\,\sigma((Z_X-1.15)/0.06)\tanh(Z_y/0.04),
 \quad \sigma(s)=(1+e^{-s})^{-1}.
\]

This is globally invertible: dXd/dZX=1+3sigma>0 and dYd/dZy=
1+10sigma sech^2>0, while Zt=H-2ZX. In particular it cannot create
an intersection between the cap and scri. It retains the regularity of
the previously checked cap and scri coordinate charts. H=2beta on the
front cap, but H is not asserted temporal anywhere else.

The cap is mapped using the exact qbar=exp(-t), lambda=(x-1)/qbar
branch, taking qbar=0. Its planar generator endpoint curve has lambda=0.
Ordinary scri uses the exact scri_map(u,theta) boundary value of the same
Z map. Every finite horizon point uses coordinates(t,h(y),y), and the
far wing sampling uses the exact null-plane equation from section 24
before applying that same map. No independently positioned surface or
invented connecting face is used.

The same traveler is transformed with the global interior map for q>0
and the regular signed-qbar cap formula after crossing. At the crossing
lambda=-2p/scale, so its finite endpoint is matched exactly. The
continuation of the curve beyond the original patch uses a cap
neighborhood, not a new maximal-extension construction.

The physical sheet is sampled for 0<=t<=6, with the planar patch sampled
farther toward its endpoint and additional exterior sampling up to scri.
Visible mesh edges are sampling cuts, not a claimed complete list of
spacetime boundaries. The singular/resolved boundary shell is omitted,
as are the rear/past surfaces. In particular the picture does not draw a
regular bridge through the rim or identify different stationary ends.

The global coordinate audit is rerun. The maximum sampled inverse error
is about 1.6e-10; the cap/interior chart mismatch is below 1.7e-14. The
positive cap/scri separating-functional gap is about 0.17868 before
the injective display transformation. Actual wing generators approach
the checked Q+/- points; the finite t=800 sample is within 0.0016 in Z,
followed by the analytically established endpoint. These finite sampling
errors do not constitute a new proof of the boundary limits; the proofs
and exact formulas are in sections 19 and 24.

The HTML camera presets all show the SAME scene, with rotation and layer
controls. The static figure is one perspective of that scene. Neither
height nor Euclidean angles in this figure encode the physical light cones.

## Reproduction

Run `python exploration/joint_boundary_limits.py`. Symbolic checks verify
the radial and corrected-label metrics, determinants, and conformal-gauge
matching. Seventy-digit calculations check angular limits. Independent
backward integrations verify the inverse scattering labels at two start
times. Outputs are in `output/joint_boundary_limits/`.

The diagnostic plot shows four approaches to the same point u=0.7,
theta=0. The uncorrected label has different limits, including divergence;
the corrected label agrees at approximately -1.19985339386782. The plot
is a convergence check, not a global conformal diagram.

For the new rider calculations run `python exploration/rider_endpoint_audit.py`.
It checks explicit timelike transfer paths, the exact cap emission-time
asymptotic, and the old sending-wing misidentification. The topological
claims rest on the proofs above, not on numerical sampling.

Run `python exploration/exceptional_boundary_audit.py` for sections 11--15.
It checks the full rim metric, a monotone Riemann bound for h>0, explicit
late rider departures to Q_n, separating witnesses, and canonical timelike
rim curves. `output/exceptional_boundary_audit/boundary_incidence.png` is a
diagram of verified boundary relations, explicitly not a conformal embedding.

Run `python exploration/global_convex_conformal.py` for the unified
construction in sections 16--21. It checks the Hessian, inverse map,
preservation of null vectors, regular cap and scri Jacobians and metrics,
the separating gap, horizon contacts, and mixed wall/rim attachments.
It writes `output/global_convex_conformal/checks.json`, the static PNG,
and a self-contained interactive HTML viewer. The gray convex hull is a
sampled rendering of the exact support-function domain; regular faces
and the enlarged cap are plotted from their explicit parametric formulas.

For the current useful geometry view run `python exploration/useful_2p1_view.py`.
It writes `output/useful_2p1_view/checks.json`, a three-panel static PNG,
and the standalone interactive HTML. The checks include horizon nullness,
null-geodesic energy conservation, the timelike normalization, and exact
matching of the traveler between the two temporal coordinate charts.
