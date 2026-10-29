# Scalar-shift extension classification

Working proof audit, 2026-08-06.

## Verdict

For the stationary scalar-shift class used in the paper, the pointwise
positive-boost-weight calculation and the transverse-geodesic argument combine
into an exact criterion.  The bounded-frame issue in the necessity direction
has been closed by launching geodesics with the observer's rest vectors and
using stationary translation only after fixing their extension limits.  The
result is now incorporated as Theorem 1 and Appendix B.5--B.7 of the draft:

> **Classification theorem.** Assume the boundedness, exterior decay,
> compact regular wall, and simple-generator hypotheses of the paper.  Then
> the spacetime admits a proper Hausdorff (C^2) extension if and only if its
> stationary-generator locus contains an open patch on which the wall is
> planar and the nonzero inaffinity
> (kappa=-v_x) is constant.  Equivalently, the wall contains an open
> constant-surface-gravity Killing-horizon patch.  Whenever the condition
> holds, the extension can be chosen smooth and is the local Kruskal
> continuation fibered over that patch.

The theorem says more than the current (H_{AB}\ne0) sufficient condition.
It also says more than the finite-jet improvement
(H_{AB}\ne0) or (partial_A\kappa\ne0): an isolated higher-order flat point
with both tensors zero is still obstructed unless the constant-(kappa)
Killing-horizon geometry persists on an open transverse neighborhood.

## 1. Full positive-boost-weight curvature at a generator

At (p\in\mathcal G), put

\[
 \ell=e_0+e_1=\chi,qquad
 n=\frac12(e_0-e_1)=\frac12\partial_t-\partial_x,
 \qquad \kappa=-v_x(p).
\]

If (K=q\ell) and (N=n/q), then

\[
 \nabla_KK=0,qquad \nabla_KN=0,qquad \nabla_KE_A=0,
\]

and the positive-boost-weight Riemann components are

\[
 \begin{aligned}
 R(K,E_A,K,E_B)&=q^2 v_{AB},\\
 R(K,E_A,K,N)&=q\,\partial_A\kappa,\\
 R(K,E_A,E_B,E_C)&=0.
 \end{aligned}
\]

The weight-zero longitudinal component is

\[
 R(K,N,K,N)=v_{xx}-v_x^2.
\]

Thus the exact null generator has a pp curvature singularity whenever

\[
 H_{AB}=v_{AB}\ne0
 \quad\hbox{or}\quad
 d_\perp\kappa\ne0,
\]

with rates (q^2) and (q), respectively.  This is the scalar-shift form of
the two positive graded pieces of the Killing-horizon curvature identity.

The frame-free object is

\[
 \mathcal B_p([E],[Y])=R(\chi,E,\chi,Y),
 \qquad
 [E]\in\chi^\perp/\langle\chi\rangle,
 \quad [Y]\in T_pM/\langle\chi\rangle.
\]

It is nonzero exactly when (H\ne0) or (d_\perp\kappa\ne0).

## 2. Algebraic boost lemma

The (+1) term also works for the arbitrary timelike exit supplied by the
global extension theorem; no rate estimate from the capture proof is needed.

Let (u_j) be unit timelike and tend projectively to a null vector (ell).
After a spatial rotation tending to the identity, write

\[
 u_j=\gamma_j(e_0+\beta_j e_1),\qquad
 s_{1,j}=\gamma_j(\beta_j e_0+e_1),
 \qquad \gamma_j\to\infty.
\]

With

\[
 A_j=\gamma_j(1+\beta_j),\qquad
 \ell_j=e_0+e_1,\qquad n_j=\frac12(e_0-e_1),
\]

the observer-adapted null frame is exactly

\[
 u_j+s_{1,j}=A_j\ell_j,qquad
 \frac12(u_j-s_{1,j})=A_j^{-1}n_j.
\]

If all Riemann components in the observer's orthonormal frame remain bounded,
then so do the corresponding null-frame components.  Therefore

\[
 \begin{aligned}
 A_j^2R(\ell_j,E_A,\ell_j,E_B)&=O(1),\\
 A_jR(\ell_j,n_j,\ell_j,E_A)&=O(1).
 \end{aligned}
\]

Taking the limit forces every boost-weight (+2) and (+1) component of the
limiting Riemann tensor to vanish.  This proves that the proposed hypothesis

\[
 H\ne0\quad\hbox{or}\quad d_\perp\kappa\ne0
\]

can replace (H\ne0) in the paper's present global theorem without changing
the capture proposition.

## 3. Why the finite-jet condition is still not the exact boundary

Consider the perfectly regular local germ

\[
 v=-1-\kappa x+c(y^4+z^4).
\]

At the stationary generator (x=y=z=0), both
(H_{AB}=0) and (d_\perp\kappa=0).  Nevertheless, the wall is not a
Killing-horizon patch.  A regular endpoint neighborhood samples fixed
nonzero transverse displacement, where the boosted curvature is nonzero.
Thus the stronger pointwise condition covers generic degenerate tips but does
not close the higher-order gap.

The missing information is not another derivative at (p); it is whether
the regular horizon geometry persists on an open neighborhood.

## 4. Transverse propagation from a hypothetical extension

Suppose a proper (C^2) extension exists.  The paper's global theorem and
capture proposition give a finite-proper-time timelike exit with translated
spatial data tending to some (p\in\mathcal G), and with its unit tangent
boosting projectively toward (ell_p=e_0+e_1).

Choose an observer-bounded transverse rest frame at the exit points and shoot
short spacelike geodesics in every transverse direction, transporting the
whole frame along them.  In a (C^2) extension the initial data converge, so
geodesics and parallel transport exist for a uniform transverse radius and
all resulting curvature components remain bounded.

In the original scalar-shift coordinates,

\[
 \Gamma^\mu{}_{AB}=0,
 \qquad A,B\in\{y,z\}.
\]

Consequently the limiting transverse geodesics are the straight coordinate
lines at fixed (t,x).  Along such a line,

\[
 \nabla_Ae_0=\frac{v_A}{2}e_1,qquad
 \nabla_Ae_1=\frac{v_A}{2}e_0,
\]

so parallel transport of the two stationary null directions gives

\[
 \widehat\ell=e^{-[v-v(p)]/2}(e_0+e_1),qquad
 \widehat n=e^{+[v-v(p)]/2}\frac{e_0-e_1}{2}.
\]

At every point (q) of a sufficiently small transverse disk centered at
(p), the boost lemma therefore forces

\[
 R(\widehat\ell,E_A,\widehat\ell,E_B)=0.
\]

Direct evaluation gives

\[
 R(e_0+e_1,E_A,e_0+e_1,E_B)
   =v_{AB}-v_Av_B.
\]

Hence on the entire disk

\[
 v_{AB}-v_Av_B=0.
\]

For (f=e^{-v}), this is (f_{AB}=0).  Thus (f) is affine on the disk.
Since (p\in\mathcal G), (v_A(p)=0), so its affine gradient vanishes and

\[
 v(p_x,y,z)=-1
\]

throughout the disk.  The wall is therefore planar there and the disk times
the Killing orbits is a genuine Killing horizon.

On this disk the weight-(+1) identity becomes

\[
 R(\ell,n,\ell,E_A)=-v_{xA}=\partial_A\kappa.
\]

The same boost lemma forces it to vanish throughout the disk, so (v_x), and
hence (kappa=-v_x), is constant.  This proves the necessary half of the
classification.

The argument also settles the edge of a flat cap.  The cap interior satisfies
the condition; at its edge every transverse neighborhood meets points where
the wall is no longer planar.  Such an edge cannot be a regular (C^2)
endpoint even though all positive-weight components may vanish to infinite
order on the edge generator itself.

## 5. Sufficiency and the extension obtained

Conversely, suppose a transverse disk at (x=x_H) satisfies

\[
 v(x_H,y,z)=-1,qquad v_x(x_H,y,z)=-\kappa,qquad
 \kappa\ne0
\]

with the same constant (kappa) throughout the disk.  Hadamard's lemma with
parameters gives, for (s=x-x_H),

\[
 v=-1-\kappa s+s^2d(s,y,z)
\]

for a smooth (d).  With

\[
 U=e^{-\kappa t},\qquad s=UV,
\]

the metric becomes

\[
\begin{aligned}
 ds^2={}&U^2dV^2+
 \left[-\frac{2}{\kappa}
 +\frac{2U^2V^2}{\kappa}d(UV,y,z)\right]dU\,dV\\
 &+\left[-\frac{2V^2}{\kappa^2}d(UV,y,z)
 +\frac{U^2V^4}{\kappa^2}d(UV,y,z)^2\right]dU^2
 +dy^2+dz^2.
\end{aligned}
\]

All coefficients are smooth at (U=0), and the determinant of the
((U,V)) block is (-\kappa^{-2}).  A patch with (U<0) glues to the whole
original spacetime along (U>0).  The graph of the gluing map is closed:
any sequence approaching (U=0) has (t\to+\infty) and no limit in the
original (mathbb R^4).  The quotient is therefore Hausdorff.

This proves sufficiency directly in the scalar-shift class, without needing a
global R\'acz--Wald extension theorem.  Geometrically it is exactly their
regular branch: a constant-nonzero-surface-gravity Killing horizon continued
to a bifurcate horizon.  The continuation adds the opposite Kruskal
quadrants over the open transverse disk.

## 6. Consequences for the paper

1. The immediate low-cost improvement proposed by Claude is correct:
   replace (H\ne0) by (H\ne0) or (d_\perp\kappa\ne0), and generalize the
   amplification lemma from screen tidal curvature to all positive boost
   weights.
2. It should not be described as closing every higher-order critical point.
   Vanishing of both tensors at one point is possible without local
   extendibility.
3. The neighborhood argument gives the cleaner final theorem: the spacetime
   is extendible exactly when a constant-(kappa) Killing-horizon patch has
   deliberately been installed.
4. R\'acz--Wald's warning about failure of a *global bifurcate extension* does
   not block sufficiency here.  The scalar-shift manifold is (mathbb R^4)
   with a global time coordinate; the explicit open-patch gluing has closed
   graph and is Hausdorff.  Only a proper extension is needed.
5. The flat-cap example realizes the extendible branch.  Its open cap becomes
   a bifurcate-horizon aperture, while its edge lies on the inextendible
   branch.  Thus the original spacetime is extendible, although no one chart
   can continue the whole compact wall.
