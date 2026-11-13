# What the known 1+1 diagram tells us about the global construction

2026-10-30. Control calculation for the proposed higher-dimensional diagram.
This does not construct a global 2+1 completion. The manuscript is unchanged.

## Main finding

The background Minkowski compactification fails the SAME test in 1+1
dimensions, where the metric-adapted causal diagram is already known. It
collapses a complete center worldline and finite-parameter front endpoints
to its background spatial-infinity point. The known warp chart separates
them. Thus the failure of the background map must not be treated as an
obstruction to a higher-dimensional construction.

The useful starting point is the actual null geometry, followed by an atlas
of boundary charts with the appropriate scaling at each type of end.

## 1. Boundary coordinates

For v(x)=2(sech x-1), RF=acosh(2), kappa=sqrt(3)/2, write

\[
 u=t-\int\frac{dx}{v+1},\qquad w=t-\int\frac{dx}{v-1},
 \qquad \alpha=\arctan\mathcal U(u),\quad\beta=\arctan w.
\]

Use the three regionwise functions in the draft:

\[
 \mathcal U_I=\tfrac12+e^{-\kappa u},\quad
 \mathcal U_{II}=\tfrac12\tanh(\kappa u/2),\quad
 \mathcal U_{III}=-\tfrac12-e^{\kappa u}.
\]

Let a=atan(1/2), b=pi/2. The diagram coordinates are
X=(beta-alpha)/2, T=(beta+alpha)/2. Both null families are future-oriented
toward increasing alpha or beta, so T is a temporal function of the actual
two-dimensional metric. It is not the background Minkowski time.

The entire square -b<alpha,beta<b represents the original reduced
spacetime, with regions I, II, III corresponding respectively to alpha>a,
-a<alpha<a, and alpha<-a.

## 2. Three distinct future ends

| Curve | Future limit (alpha,beta) | Parameter behavior |
| --- | --- | --- |
| Center, x=0 | P+=(a,b) | Infinite proper time |
| Front stationary null generator, x=RF | C+=(-a,b) | Finite affine parameter |
| Outgoing massive geodesic from the core | (alpha_star,b), -a<alpha_star<a | Finite proper time |

The center's future end is NOT the diagram's exterior i+ vertex (b,b).
The rear generator instead has future end P+ and infinite future affine
parameter. Its finite past affine endpoint is C-=(a,-b). The center's past
end is P-=(-a,-b), also distinct from the exterior i- vertex.

In laboratory background coordinates X_lab=x+2t, the center and finite
front-ending trajectories all go to the SAME background diagram point
(X_compact,T_compact)=(pi/2,0). This collapse already occurs in 1+1.

## 3. The outer edge is not all ordinary null infinity

The future ordinary null infinities are:

- alpha=b, -b<beta<b;
- beta=b, a<alpha<b.

The future front boundary that is regularly extendible in the reduced
metric is beta=b, -b<alpha<a. It contains C+. The point P+ separates this
boundary from the ordinary-null-infinity portion of the same drawn edge.

The past ordinary null infinities are:

- alpha=-b, -b<beta<b;
- beta=-b, -b<alpha<-a.

The reduced past-rear extension boundary is beta=-b, -a<alpha<b, separated
from ordinary past null infinity by P-.

These classifications follow by taking limits along EXACT null rays of
the warp metric. In region I, u=constant with x->-infinity gives ordinary
future right-going null infinity; w=constant with x->-infinity gives the
other future component. Region III supplies the past counterparts.
At finite u with x->RF, t->+infinity while x remains finite, giving the
front extension boundary instead. An outgoing null ray has dx/dlambda=E,
so its remaining affine distance to RF is finite.

The plotted edge by itself therefore does not determine whether the
physical conformal factor vanishes, whether affine length is infinite,
or whether a physical extension exists. Separate regular charts are needed.

## 4. Checked massive example

Launch at x=0,t=-2 with E=sqrt(2), initial spatial momentum 1. The first
integrals give

\[
 \dot x=\sqrt{E^2-1+v^2},\qquad
 \dot t=\frac{E-v\dot x}{1-v^2}.
\]

After subtracting the logarithmic stationary-time pole and integrating with
75-digit arithmetic, the elapsed proper time to the front boundary is
1.1911230632459 (profile scale a=1), with limiting u=-0.005546109519525.
Its diagram endpoint is approximately (X,T)=(0.78599855,0.78479778), between
C+ and P+. This is an illustrative geodesic calculation, not a new
literature-priority claim. The general core-to-cap crossing is already
proved in the manuscript.

## 5. What the calculation suggests for 2+1

The axial chart resolves the front approach through

\[
 u=t+\kappa^{-1}\log|x-R_F|+O(1).
\]

It preserves the distinct finite limits of u when
|x-RF| is proportional to exp(-kappa*t). This is the information discarded
by the background compactification.

However, simply copying the axial functions off axis does not work. With
v0=v(x,0), delta=v(x,rho)-v0, and the full inverse meridional metric,

\[
 g_3^{-1}(du,du)=\frac{\delta(2-\delta)}{(v_0+1)^2},\qquad
 g_3^{-1}(dw,dw)=-\frac{\delta(2+\delta)}{(v_0-1)^2}.
\]

These are generically nonzero. A transverse-aware optical construction
must use the full eikonal equation

\[
 (F_t+v F_x)^2=F_x^2+F_\rho^2.
\]

The axial construction is a control and matching condition, not a unique
noncharacteristic initial-value prescription for that PDE. Appropriate
data, multiple charts through caustics, and separate boundary regularity
checks are still needed. A double-cone outline or a rotation of the axial
diamond would not supply them.

## Reproduction

`exploration/axial_compactification_control.py` checks the actual null
coordinate equations, orientation of the diagram time, null-ray boundary
limits, the massive finite-time example, and the off-axis gradient norms.
It then regenerates `output/global_2p1/axial_boundary_control.png` and
`output/global_2p1/axial_control_check.txt`.

The source construction is the one already credited in the draft to
Finazzi, Liberati and Barcelo (2009), section II.A. The boundary comparison
and explicit control tests above are our audit of the proposed global map.
