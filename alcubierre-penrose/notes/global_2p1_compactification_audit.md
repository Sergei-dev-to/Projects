# Global 2+1 compactification: boundary audit

2026-10-30. Research calculation; not a completed boundary-resolved Penrose
diagram. No new figure has been drawn from this construction.

## What has been constructed

The standard Einstein-cylinder coordinate compactification covers the entire
signed meridional Alcubierre spacetime and has a smooth Lorentzian conformal
metric at ordinary past and future null infinity, away from the vertices.
It does **not** give a continuous nondegenerate conformal metric at its
standard spatial-infinity point. It collapses distinct bubble-end behaviors
there, and its plotted time is not a temporal function for the warp metric.

The direct radial hyperboloidal height-function construction also fails to
be a global future time along the eternal superluminal bubble center.
These are failures of the two proposed constructions in these gauges, not a
theorem excluding every possible global conformal completion.

Terminology is important: every occurrence of the "standard i0" below means
the point assigned that label by the BACKGROUND Minkowski/Einstein-cylinder
attachment. The failed attachment does not establish the intrinsic causal
classification or topology of the warp spacetime's missing ends. In
particular, a physical timelike bubble-center worldline is spacelike with
respect to the auxiliary Minkowski background; its background endpoint
cannot simply be called physical spatial infinity.

The underlying spacetime is R x R^3. The spherical level-set wall is
R x S^2 and its interior is R x B^3. Those interior topologies do not
determine how either temporal end attaches to a conformal boundary. A
finite-affine null endpoint cannot be a regular ordinary scri point: under
g_tilde=Omega^2 g, physical and unphysical affine parameters satisfy
d lambda/d lambda_tilde=constant/Omega^2, which has divergent integral at a
smooth zero of Omega. This does not exclude a singular corner abutting
scri; it distinguishes such a corner from its regular null-infinity part.

The next required step is an atlas or boundary resolution that retains the
distinct bubble ends instead of identifying them with ordinary spatial
infinity. Neither the present calculation nor the local cap extension proves
the existence or regularity of that resolution.

Follow-up control: `notes/axial_boundary_control.md` applies the SAME failed
background map to the known 1+1 problem. It fails there as well, while the
actual null-coordinate construction successfully separates the complete
center end, finite-parameter front boundary, and ordinary null infinity.
This is direct evidence to change the construction, not to infer that the
desired higher-dimensional diagram is impossible.

## 1. Exact spacetime and global interior map

Use the signed meridional plane of the axisymmetric four-dimensional metric.
In laboratory coordinates its induced metric is

\[
 g_3=-dt^2+[dX-b(t,X,Y)dt]^2+dY^2,
 \qquad b=V\operatorname{sech}r_b,
 \qquad r_b^2=(X-Vt)^2+Y^2,
 \qquad V>1.
\]

The half-plane \(Y\geq0\) is the angular quotient; doubling it across the
symmetry axis gives the full meridional double-cone display. This is the
actual warp metric, not a bubble drawn on a flat metric.

Put \(R=\sqrt{X^2+Y^2}\), \(X=R\cos\theta\), \(Y=R\sin\theta\), and

\[
 u=t-R,\quad v=t+R,\quad P=\arctan u,\quad Q=\arctan v,
 \quad T=P+Q,\quad\chi=Q-P.
\]

The entire interior maps to \(|T|+\chi<\pi\), with inverse

\[
 \Omega=\cos T+\cos\chi=2\cos P\cos Q,
 \qquad t=\frac{\sin T}{\Omega},
 \qquad R=\frac{\sin\chi}{\Omega}.
\]

The apparent angular degeneracy at \(R=0\) is removed by Cartesian spatial
coordinates, as in Minkowski space. Global interior coverage is not the
problem; boundary regularity is.

## 2. Pull back the full metric

Define

\[
 A=\frac{1+\cos T\cos\chi}{\Omega},\qquad
 B=\frac{\sin T\sin\chi}{\Omega},\qquad A^2-B^2=1.
\]

Then the exact scaled coframe is

\[
 a=\Omega\,dt=A\,dT+B\,d\chi,\qquad
 c=\Omega\,dR=B\,dT+A\,d\chi,
\]

\[
 e_X=\Omega\,dX=\cos\theta\,c-\sin\theta\sin\chi\,d\theta,
 \qquad
 e_Y=\Omega\,dY=\sin\theta\,c+\cos\theta\sin\chi\,d\theta.
\]

Consequently

\[
 \widetilde g_3=\Omega^2g_3
 =-a^2+(e_X-ba)^2+e_Y^2
 =-dT^2+d\chi^2+\sin^2\chi\,d\theta^2+b^2a^2-2b\,a e_X.
\]

The determinant in this polar chart is \(-\sin^2\chi\), independently of
the shift. Thus the interior is Lorentzian. Merely plotting the flat
Einstein-cylinder metric plus a bubble tube would discard the last two terms
and would not be this construction.

## 3. Ordinary null infinity passes the regularity check

At a fixed ordinary future-null-infinity point, \(t=R+u_0\), and

\[
 r_b\geq V|t|-R\geq(V-1)R-O(1).
\]

The past case has the analogous estimate with \(v_0=t+R\) fixed. The sech
shift and all its derivatives therefore decay exponentially. This beats the
polynomial growth of the coordinate coframe at every nonvertex scri point.
The warp correction vanishes to all orders there, leaving the regular
Einstein-cylinder metric. For a compact-transition profile the correction
vanishes identically in a neighborhood of each such point.

For the limiting metric,

\[
 \widetilde g^{-1}(d\Omega,d\Omega)
 =-\sin^2 T+\sin^2\chi=0\qquad\text{on }\mathscr I^\pm.
\]

The angular cross-section has coefficient \(\sin^2\chi>0\) away from the
vertices. These are ordinary null infinities. The usual \(i^\pm\) vertices
also have a flat neighborhood for a compact-transition profile; the sech
correction decays to all orders there.

## 4. Spatial infinity fails even in a regular pole chart

The bubble-center worldline is \(X=Vt,Y=0\), with physical proper time
\(\tau=t\). As \(t\to+\infty\),

\[
 T\sim\frac{2}{(V^2-1)t},\qquad
 \epsilon:=\pi-\chi\sim\frac{2V}{(V^2-1)t},\qquad\theta=0.
\]

Thus it reaches the standard spatial-infinity point \(i^0\), not ordinary
\(\mathscr I^+\). Its past end approaches the same standard \(i^0\) from
the opposite spatial direction. The circular base of a double-cone picture
keeps these spatial directions visible, but the Einstein-cylinder completion
identifies that polar circle to one point.

The vanishing coefficient of \(d\theta^2\) alone would only be a polar
coordinate artifact. To avoid that mistake use a regular south-pole chart

\[
 Z_1=(\pi-\chi)\cos\theta,\qquad
 Z_2=(\pi-\chi)\sin\theta.
\]

At \(Y=0,X>0\), \(d\chi=-dZ_1\), and
\(\sin\chi\,d\theta=[\sin\epsilon/\epsilon]dZ_2\).
Along the bubble center,

\[
 A\longrightarrow\frac{V^2+1}{V^2-1},\qquad
 B\longrightarrow\frac{2V}{V^2-1},\qquad b=V.
\]

For the draft's \(V=2\) example this gives, in the regular
\((T,Z_1,Z_2)\) chart,

\[
 \widetilde g_3\longrightarrow
 \begin{pmatrix}
  11/9&2/9&0\\
  2/9&-7/9&0\\
  0&0&1
 \end{pmatrix}.
\]

Along the exterior path \(X=Vt+\sqrt t,Y=0\), the same point and the same
first-order direction are approached, but \(b\to0\), so the limit is
\(\operatorname{diag}(-1,1,1)\). The limits disagree. There is no continuous
metric extension at this standard \(i^0\).

Nor can changing only the scalar conformal factor fix this in the same pole
chart: both paths have limiting \(ZZ\) transverse component 1 and zero
transverse mixed components. A continuous nondegenerate limit forces a
finite nonzero common rescaling, which cannot reconcile the other entries.
A different boundary attachment or differentiable structure is not excluded.

The stationary front null orbit \(X=Vt+R_F,Y=0\) approaches this same
\(i^0\), although its affine parameter is finite at the future end. It is
collapsed together with the proper-time-complete center. A bare cone plot
would therefore hide the boundary distinction needed for the extension
question.

## 5. The displayed time and a direct hyperboloidal alternative

On the center worldline,

\[
 \frac{dT}{dt}=
 \frac{2[1-(V^2-1)t^2]}
 {[1+(V-1)^2t^2][1+(V+1)^2t^2]}.
\]

It becomes negative at late \(t\), despite the worldline being future
timelike. The background double-cone time cannot be presented as a globally
future-increasing time for the warp metric.

For the direct radial hyperboloidal ansatz \(\tau=t-h(R)\), the usual
outgoing scri condition \(h'(R)\to1\) gives

\[
 \frac{d\tau}{dt}\bigg|_{X=Vt,Y=0}
 =1-Vh'(Vt)\longrightarrow1-V<0.
\]

Thus this ansatz is not a global future time either. Matching it to an
interior foliation at a fixed laboratory radius does not remedy the issue,
because the eternal bubble eventually leaves every such radius. A moving
or angular-dependent matching construction requires a separate proof.

## 6. Checks and references

`exploration/global_2p1_compactification.py` checks the full coframe pullback,
determinant, global inverse, null boundary normal, regular-scri limits,
the nonmatching limits in the regular pole chart, and the center-time
derivative. It uses symbolic identities and 70-digit numerical evaluation.
Output: `output/global_2p1/compactification_check.txt`.

The pole-chart discrepancy converges to the analytic values; at \(t=10^4\)
the center and exterior matrix errors are below \(6\times10^{-9}\). It is
not a floating-point artifact.

Sources for the proposed constructions:

- Cameron, *Conformal Properties of Spacetime*, section 2.2, equations
  (2.2.4)--(2.2.7), figures 2.5--2.6:
  https://www.damtp.cam.ac.uk/user/md327/cameron_thesis.pdf
- Zenginoglu, *Hyperboloidal foliations and scri-fixing* (2008), sections
  III and VI: https://arxiv.org/html/0712.4333

Their application here is the calculation above, not a result claimed by
either reference.
