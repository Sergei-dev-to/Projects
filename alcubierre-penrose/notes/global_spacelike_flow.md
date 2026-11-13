# Global coordinates through the cap: construction and remaining scri problem

This is a new global coordinate calculation, not a juxtaposition of local
charts. It covers the entire original signed meridional spacetime and has
regular continuations through both open caps. It does **not** yet complete
the requested global conformal compactification at ordinary null infinity.
No global Penrose diagram should be drawn from it until that step is solved.

## Exact global foliation

Let v0(x)=v(x,0) for the bounded capped profile. Monotonicity of W and
nonnegativity of psi imply v(x,y)<=v0(x) everywhere. Fix eta=0.05 and solve

\[
 F_t=v_0(F)+1+\epsilon(t),\qquad F(0,A)=A,
 \qquad \epsilon(t)=\eta\operatorname{sech}^2t.
\]

The right side and its spatial derivative are globally bounded. Thus the
flow exists for all finite t,A, and

\[
 a=F_A=\exp\left(\int_0^t v_0'(F(s,A))ds\right)>0.
\]

Also |F(t,A)-A| <= (1+eta)|t|, so A -> F(t,A) is onto R at every finite t.
The coordinates (T,t,y), with T=-A and x=F(t,-T), are therefore one global
diffeomorphism on the original spacetime. This statement is analytic, not
an inference from sampled Jacobians.

Write D=1+epsilon+v0(F)-v(F,y). Direct substitution gives

\[
 g=a^2dT^2-2aD\,dTdt+(D^2-1)dt^2+dy^2,
 \qquad \det g=-a^2,
\]

\[
 \boxed{g^{-1}(dT,dT)=-(D^2-1)/a^2<0.}
\]

D>=1+epsilon>1 holds for all x,y,t. The future Eulerian vector has
dT(e0)=D/a>0. Thus T is future-increasing for every future causal curve,
including nonaxial curves. Any positive conformal factor preserves this.

## Regular continuation at the front cap

For the open interval of flow labels whose trajectories approach x=1 as
t -> infinity, use q=exp(-t), and put

\[
 F=1+qL(A,q),\qquad a=q\ell(A,q).
\]

Once the trajectory is in the exact affine collar, its flow and variational
equations become the regular equations

\[
 L_q=\tfrac12L^2-\frac{4\eta}{(1+q^2)^2},\qquad
 \ell_q=L\ell.
\]

They continue smoothly through q=0. In the open transverse cap |y|<0.6,
define delta=4 eta q^2/(1+q^2)^2 and

\[
 B(q)=\frac{8\eta}{(1+q^2)^2}
       +\frac{16\eta^2q^2}{(1+q^2)^4}.
\]

The physical metric in (T,q,y) is exactly

\[
 g= q^2\ell^2dT^2+2\ell(1+\delta)dT\,dq+B(q)dq^2+dy^2,
 \qquad\det g=-\ell^2.
\]

At q=0 it is

\[
 g=2\ell_0dT\,dq+8\eta dq^2+dy^2,
 \qquad g^{-1}(dT,dT)=-8\eta/\ell_0^2<0.
\]

Thus the SAME global time extends as a temporal coordinate through the
regular cap; the transverse metric remains nondegenerate. The original
cap factor has the smooth expression

\[
 \Omega=
 \frac1{\sqrt{(1+L^2)(1+q^2)}}+
 \frac q{\sqrt{[1+(2+qL)^2q^2](1+q^2)}},
\]

so Omega -> (1+L0^2)^(-1/2)>0. This is the already chosen global factor
restricted to the cap, with signed q giving its continuation.

Time reversal gives the rear cap. Using z=tanh(t/2), the original spacetime
has the single coordinate domain R_T x (-1,1)_z x R_y. Since
q=(1-z)/(1+z) has a nonzero derivative at z=1, the front cap is a regular
open part of the face z=1. Similarly the rear cap lies on z=-1. Thin
continuation collars can be added in these same coordinates. This makes
the two cap attachments part of one global coordinate construction.

The future separatrix is the unique trajectory asymptotic to x=-1.
Backward shooting from t=16,20,24 agrees on its initial label to better
than 1e-10. Its value, the cap-limit data, and checks on both sides of the
cap are in `output/global_spacelike_flow/checks.json`.

## Why the present spatial compactification is still insufficient

For labels on the escaping side of the separatrix, the trajectory is
eventually in the exact flat exterior, where

\[
 F(t,A)=-t+\eta\tanh t+\mathcal B(A),\qquad
 a=\mathcal B'(A)>0.
\]

At fixed A and bounded y, t -> infinity approaches the forward generator
of ordinary future scri, with retarded time u -> -eta-B(A).
The chosen conformal factor behaves as Omega~1/t. In q=exp(-t),

\[
 \widehat g_{Tq}\sim\frac{\mathcal B'(A)}{q\,t^2},
\]

which diverges. Thus z=tanh(t/2) is not a smooth boundary coordinate at
ordinary scri, despite being regular at the cap. A conformal factor alone
cannot make this the requested unified drawing.

Moreover changing the rate of q alone is insufficient. At nonaxial scri,
the transverse coordinate must scale with the radius, and the time/label
coordinate needs a transverse correction. The exact flat-space identity
illustrates the coupled requirement. For

\[
 g=-du\,dv+dy^2,\quad Q=1/v,\quad Y=y/v,\quad U=u-y^2/v,
\]

one has

\[
 Q^2g=dU\,dQ+dY^2.
\]

The correction y^2/v cancels terms that otherwise diverge when Y remains
finite at the boundary. This ordinary-scri chart covers finite U,Y and
misses the opposite angular generator, which also needs to be included
in a global construction. Directly applying this correction at the cap
would produce 1/t terms and spoil its smooth exponential coordinate.

The outstanding problem is therefore explicit: construct a smooth,
injective joint coordinate change incorporating this exterior correction
and its other angular direction while preserving the cap coordinates.
No such change, global Jacobian proof, or complete boundary identification
has been established here. This note records progress, not a completed
answer to the user's global-compaction request.

## Reproduction

Run `python exploration/global_spacelike_flow.py`. It checks the metric
and inverse-time identities symbolically, integrates the global flow,
checks the separatrix shooting, and uses the regular q equations to test
the cap metric and conformal factor on both sides of q=0. Its numerical
checks supplement the global temporal-coordinate proof above.
