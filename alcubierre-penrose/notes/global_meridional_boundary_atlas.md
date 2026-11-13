# Global meridional construction: bulk chart and separate boundary charts

This continues `axial_boundary_control.md`. It establishes a global chart
on the original spacetime and compatible charts on its open ordinary null
infinities. For a planar cap, the existing physical extension charts supply
another, different boundary component. It does **not** yet establish a
compact boundary-resolved global diagram. No new figure or manuscript edit
has been made on the strength of these calculations.

## 1. Which three-dimensional spacetime?

For an axisymmetric bubble,

\[
 g_4=-dt^2+[dx-v(x,\rho)dt]^2+d\rho^2+\rho^2d\phi^2.
\]

Suppressing the angular coordinate gives the causal quotient

\[
 g_3=-dt^2+[dx-v(x,\rho)dt]^2+d\rho^2,\qquad \rho\geq0.
\]

The axis is a quotient edge, not a physical boundary. Work first on the
smooth signed meridional double, with coordinate y in R and shift
v(x,y)=v(x,-y), then fold y<0 onto y>0. A doubled spatial slice is R^2;
the actual angular quotient is a half-plane. Neither operation makes the
metric rotationally symmetric in the (x,y) plane. Rotating the axial
Penrose diamond would impose a symmetry that the metric does not have.

The computations below use v=2 sech(sqrt(x^2+y^2))-2 for the rounded
example. The bulk coordinate construction applies more generally to any
smooth bounded axial shift v0(x)=v(x,0).

## 2. An exact global optical pair

The inverse meridional metric is

\[
 g_3^{-1}=-\partial_t^2-2v\partial_t\partial_x
 +(1-v^2)\partial_x^2+\partial_y^2.
\]

Consequently t-y and t+y are exact optical functions:

\[
 g_3^{-1}(d(t-y),d(t-y))=
 g_3^{-1}(d(t+y),d(t+y))=0.
\]

These are transverse plane-wave null foliations, not the radial light
cones of Minkowski space. Their future null generators have tangent
\(\partial_t+v\partial_x\pm\partial_y\), with affine parameter t.
Set

\[
 U=\arctan(t-y),\qquad V=\arctan(t+y),\qquad
 \tau=(U+V)/2.
\]

Then

\[
 g_3^{-1}(d\tau,d\tau)=-\cos^2U\cos^2V<0,
 \qquad (\partial_t+v\partial_x)\tau
 =\tfrac12(\cos^2U+\cos^2V)>0.
\]

Thus tau is a global future temporal function. Unlike the failed
background double-cone time, it never turns backward on the rider.

## 3. Preserve the distinct axial ends with a smooth flow coordinate

Let Phi_t(xi) be the complete flow of the axial outgoing null vector field:

\[
 \frac{d\Phi_t}{dt}=1+v_0(\Phi_t),\qquad \Phi_0(\xi)=\xi.
\]

Boundedness of the vector field implies completeness for finite t. Its
derivative is

\[
 \partial_\xi\Phi_t=
 \exp\!\left(\int_0^t v_0'(\Phi_s)\,ds\right)>0.
\]

Define

\[
 A=-\arctan\!\left(\frac{\Phi_{-t}(x)}{2R_F}\right).
\]

This is globally smooth, including the stationary axial null generators;
it avoids needing to match regionwise compactifying functions at a
horizon. The inverse of the full chart is explicit in terms of the flow:

\[
 t=\tfrac12(\tan U+\tan V),\quad
 y=\tfrac12(\tan V-\tan U),\quad
 x=\Phi_t(-2R_F\tan A).
\]

The entire original signed meridional spacetime is therefore the open
cube |A|,|U|,|V|<pi/2. The actual quotient is its wedge U<=V. This is a
global **bulk** chart, not an assertion about its naive closed cube.

Write J=(partial x/partial A)_{t}<0 and delta=v(x,y)-v0(x). Since
dx=(1+v0)dt+JdA, the exact full metric is

\[
 g_3=-\sec^2U\sec^2V\,dU\,dV
 +\left[JdA+\frac{1-\delta}{2}
 (\sec^2U\,dU+\sec^2V\,dV)\right]^2.
\]

With Omega0=cos U cos V, its determinant is

\[
 \det(\Omega_0^2g_3)=-\tfrac14 J^2\cos^2U\cos^2V<0.
\]

This verifies the pullback and Lorentzian signature in the whole interior.
It does not establish a nondegenerate limiting metric on every cube face.

For the sech example let a=atan(1/2), b=pi/2. The important axial limits are

| End | (A,U,V) | Physical parameter |
| --- | --- | --- |
| Center future P+ | (a,b,b) | Proper time infinite |
| Front stationary generator C+ | (-a,b,b) | Affine time finite |
| Other finite axial front ends | (A,b,b), -b<A<a | Finite affine/proper time on the appropriate geodesics |
| Center past P- | (-a,-b,-b) | Proper time infinite |
| Rear stationary generator C- | (a,-b,-b) | Past affine time finite |

The label A is a smooth reparametrization of the axial outgoing family,
not numerically the same function as alpha in the earlier diagram. The
boundary distinctions and the two marked horizon labels agree.

## 4. Ordinary null infinity needs its own charts

In laboratory coordinates X=x+V_b t, Y=y, let
R=sqrt(X^2+Y^2), theta=atan2(Y,X). Here V_b>1 is the bubble speed, not the
compact coordinate V. For future scri use

\[
 s=1/R,\quad u=t-R,\quad
 t=u+1/s,\quad X=\cos\theta/s,\quad Y=\sin\theta/s.
\]

The physical metric is Minkowski plus
\(b_w^2dt^2-2b_wdt\,dX\), where b_w=V_b sech(r_b) for the rounded
example and r_b=sqrt((X-V_b t)^2+Y^2). On a bounded u interval,

\[
 r_b\geq(V_b-1)/s-V_b|u|.
\]

Thus the warp correction to s^2 g is flat at s=0: it and all its
derivatives vanish. The limiting chart metric is

\[
 s^2g_3=-s^2du^2+2du\,ds+d\theta^2+\text{flat correction}.
\]

Its determinant is exactly -1, including before taking the limit, and ds
has null norm at s=0. The past chart uses w=t+R and the opposite sign in
the cross term. These give the ordinary open scri cylinders R x S^1 on
the signed double, or R x [0,pi] on the angular quotient. For an exactly
constant exterior the correction is identically zero near each such
boundary point.

Transition functions to the bulk chart are explicit. On future scri's
physical overlap,

\[
 U=\arctan[u+(1-\sin\theta)/s],\quad
 V=\arctan[u+(1+\sin\theta)/s],
\]

with t and x=(cos(theta)-V_b)/s-V_b u substituted into A's flow formula.
Generic scri points collapse to the same corner of the naive bulk cube;
the scri charts retain the missing information. More strongly, A does not
in general have a continuous extension to ordinary scri: near the forward
direction, angular approaches with theta^2/s finite can have different
limiting A at the same finite-u scri point. It is only an interior chart
coordinate. The construction must not identify the regular scri attachment
with the naive cube closure, or describe the replacement as an already
proved blowup of that closure. The bounded cube alone is not a
boundary-resolved compactification.

## 5. The planar cap is a different boundary component

Within an open planar cap, the already established front chart is

\[
 p=P(x)e^{\kappa t},\qquad q=Q(x)e^{-\kappa t},\qquad
 g_3=C(pq)\,dp\,dq+dy^2,
\]

with C(0)>0, Q(R_F)>0 and P(R_F)=0. The original side has q>0. The
physical metric is nondegenerate at q=0 for finite p and |y|<a_cap.
This is a physical extension boundary with conformal factor positive,
not ordinary scri with conformal factor zero. The null boundary is an
open strip parametrized by (p,y). In four dimensions it is R x B^2.

Where both flow and cap charts are defined,

\[
 p=P(\Phi_{-t}(x))=P(-2R_F\tan A).
\]

Thus resolving the bulk corner U=V=b with finite p and finite y recovers
the cap's transverse aperture, rather than discarding y at that corner.
The front generator is p=0; it is not the entire boundary strip.

These open cap and finite-u scri attachments do not collide. On compact
sets of cap-boundary labels (p,y), q->0 entails t->+infinity, x->R_F and
bounded y, hence

\[
 u_{lab}=t-\sqrt{(V_b t+x)^2+y^2}
 =-(V_b-1)t-R_F+o(1)\longrightarrow-\infty.
\]

This convergence is uniform on those compact sets. A cap boundary point
can therefore be separated from every finite-u scri point by disjoint
coordinate neighborhoods. Together with the existing Hausdorff cap
attachment proof and the standard exterior scri charts, this gives a
consistent **open partial completion** of the entire original spacetime.
It does not yet attach the ends u=-infinity or p=+/-infinity, or the cap
rim. Those are precisely among the remaining junctions to resolve.

These local conformal representatives can also be patched: take a smooth
positive interior conformal factor equal to s near each ordinary-scri
point and equal to 1 near each finite cap-boundary point. A partition of
unity supplies the interpolation. The missing junctions are not part of
this open completion, so their limiting scalings are not being asserted.
This gives a conformal atlas on the original whole bulk with the stated
open regular boundary pieces. It is noncompact; it does not supply the
compact boundary of a closed global drawing. Allowing q<0 recovers the
physical cap crossing locally, without asserting a maximal continuation.

For the rounded bubble the analogous (p,q,y) physical metric fails at
fixed nonzero y. Attaching the same regular strip would contradict the
proved transverse tidal obstruction. The failed chart is not a proof of
the dimension or topology of a singular causal boundary.

## 6. Transverse behavior at the rounded tip

Along an outgoing axial null geodesic with energy E>0,

\[
 x=R_F-E(\lambda_*-\lambda),\qquad
 \frac{dt}{d\lambda}=\frac{E}{1+v_0(x)}.
\]

Reflection symmetry makes partial_y a parallel screen vector on the axis.
The linear transverse Jacobi amplitude obeys

\[
 \frac{d^2Y}{d\lambda^2}
 =-\frac{E^2 v_{yy}(x,0)}{(1+v_0(x))^2}Y.
\]

For the radial profile v_yy=v0'(x)/x. Near the front,

\[
 Y''=\left[\frac{1}{\kappa R_F(\lambda_*-\lambda)^2}
 +O((\lambda_*-\lambda)^{-1})\right]Y.
\]

The indicial powers are

\[
 p_\pm=\frac{1\pm\sqrt{1+4/(\kappa R_F)}}2,
 \qquad Y\sim c_+(\lambda_*-\lambda)^{p_+}
             +c_-(\lambda_*-\lambda)^{p_-}.
\]

For V_b=2, R_F=acosh(2), kappa=sqrt(3)/2, these are approximately
1.561505447373 and -0.561505447373. One mode collapses, the other grows.
The latter leaves the small-variation regime; this calculation does not
classify the endpoints of all nonlinear off-axis rays. Inside an exactly
planar cap v_yy=0, so Y''=0 instead and nonzero finite transverse endpoint
separations are allowed.

## 7. Why a singular end cannot be relabeled ordinary scri

Suppose a physical null geodesic has a regular null-geodesic endpoint in
a C^2 unphysical metric ghat=Omega^2 g, with Omega C^1 and Omega=0 there.
Writing unphysical affine parameter as ell, the physical affine parameter
satisfies d lambda/d ell = constant/Omega^2. Regularity at the endpoint
implies Omega <= C(ell_*-ell). Hence physical affine length diverges.

The finite-affine front generator therefore cannot end at such a regular
zero-Omega boundary. For a cap it has a regular positive-Omega physical
extension. For the rounded bubble its C^2 physical extension is obstructed
by the pp curvature divergence. Any global diagram must mark that end as
singular; it cannot obtain a smooth Penrose boundary there by simply
choosing a vanishing conformal factor.

This does not prevent a causal diagram with explicitly singular boundary
pieces. Nor does it supply their complete topology automatically.

## 8. What is checked, and what is not

Checked: the full bulk chart and inverse; global time orientation; exact
metric pullback; separate, regular ordinary-scri charts; the preservation
of the axial end distinctions; compatibility and separation of the open
cap and scri attachments; the rounded transverse indicial equation.

Still needed for a genuinely compact global drawing: the attachment at
the ends of the scri charts, its relation to P+/- and spatial directions,
the singular rounded-front boundary's topology, and the cap-rim junctions.
Until those are checked, neither a closed cube nor a decorated Minkowski
double cone is the derived global Penrose diagram.

Reproduction: `exploration/global_boundary_atlas.py` performs the symbolic
and numerical checks and writes
`output/global_2p1/global_boundary_atlas_check.txt`. It intentionally has
no plotting step. The cap's local metric and gluing proof are in the
manuscript and the existing meridional checks; they are not claimed as a
new numerical verification of a complete capped spacetime here.
