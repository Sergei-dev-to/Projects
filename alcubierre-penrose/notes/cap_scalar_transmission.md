# Scalar transmission through a planar cap: first calculation

Status: exact reduced classical and quantum calculations, with local 4D checks.
This is an exploratory note, not a new result inserted into the manuscript.
No full four-dimensional quantum stress tensor or coupled stability theorem
is claimed. Units are hbar=c=k_B=1; one real scalar has central charge one.

## 1. The crossing and the precise solved problem

In the paper's product-cap cylinder,

\[
 ds^2=-dt^2+[dx-v(x)dt]^2+dy^2+dz^2,
 \qquad v(x_H)=-1,\quad v'(x_H)=-\kappa<0.
\]

Use the paper's null coordinates

\[
 u=t-\int\frac{dx}{v+1},\qquad
 w=t-\int\frac{dx}{v-1},\qquad
 p=e^{\kappa u},\quad q=e^{-\kappa w}
\]

on the bubble-interior branch. The future passage is q=0 with finite p>0.
We work on a closed interval of strictly positive p and strictly inside the
transverse cap. This avoids both the bifurcation disk p=q=0 and the cap rim.
Here w=t+O(1) along a crossing. These q,p are not the paper's original
U=e^{-kappa*t}, V=(x-x_H)/U, though the two charts overlap smoothly.

The longitudinal metric is ds2=C(pq) dp dq, C>0 smooth through q=0.
For the exactly flat cap germ v^2=1+2*kappa*s, s=x-x_H,

\[
 u-w=\kappa^{-1}\log|s|+\text{constant},\qquad
 pq=-c_0s,\qquad C=\frac{2}{c_0\kappa}.
\]

Consequently A=-q, B=p/(c0*kappa) give ds2=-2 dA dB exactly.
There is no imposed reflecting surface or boundary condition at q=0.

The global solvable comparison replaces the finite-aperture 4D bubble by
its complete stationary 1+1 axial metric, with smooth bounded v<=0 and
nondegenerate horizons. Classically it also describes a transversely
constant field wherever the full geometry remains a product. Such a field
does not represent a finite-energy localized 4D packet over an infinite plane.
Quantizing this 2D field is not the same as quantizing the full 4D field.

## 2. Classical compact initial data transmit regularly in the reduced model

A minimally coupled massless scalar in 1+1 obeys

\[
 \Box\phi=0,\qquad \phi=F(u)+G(w).
\]

This is exact for any v(x); there is no longitudinal scattering potential
for this massless conformal channel. At t=0 prescribe smooth compact data
h(x)=phi(0,x), Pi(x)=partial_t phi(0,x). (Pi here is the coordinate-time
derivative, not the normal momentum.) Their incoming component satisfies

\[
 G'(w_0(x))=\frac{1-v(x)}2
       [\Pi(x)+(v(x)+1)h'(x)],\qquad
 w_0'(x)=\frac1{1-v(x)}>0.
\]

Since v is bounded and nonpositive, w0 is a smooth diffeomorphism R -> R.
Thus compact initial data make G' compactly supported in w. There exists
w_max such that G'(w)=0 for w>w_max. Near the crossing,

\[
 \phi(p,q)=F(\kappa^{-1}\log p)
          +G(-\kappa^{-1}\log q),\qquad
 T_{qq}=\frac{[G'(w)]^2}{\kappa^2q^2}.
\]

For q<exp(-kappa*w_max), G is exactly constant. The field extends smoothly
through q=0 on every finite p>0 interval and all of its reduced classical
stress components are finite. The extension can keep G constant just beyond
the crossing; further characteristic data on the added side are not unique.

This proves regular transmission for an entire class of reduced compact
perturbations, not only a single specially chosen ray. It does not prove
regular transmission after scattering from the transverse rim in 4D.

For noncompact illumination, the sharp componentwise criterion is

\[
 |G'(w)|=O(e^{-\kappa w})\quad\Longleftrightarrow\quad
 T_{qq}=O(1).
\]

Boundedness of this component alone does not ensure smoothness of the field.
If G'~a exp(-alpha*w), then Tqq~(a^2/kappa^2)
exp(2*(kappa-alpha)*w). A power-law tail has divergent Tqq. Compact pulses,
constant illumination and slow tails must therefore be distinguished.
Small amplitude alone does not control an arbitrarily long-lived tail.

## 3. Exact quantum answer in the flat 1+1 cap

Let tau_w(w) denote the incoming chiral state function, normal ordered
relative to the w-conformal vacuum. It is NOT the full covariant Tww
in the curved geometry. In a constant exterior it equals the incoming
flux component measured in that affine null coordinate, up to normalization.

With Minkowski subtraction in the flat cap, the renormalized stress is

\[
 \langle T_{qq}\rangle
 =\left(\frac{dw}{dq}\right)^2\tau_w(w)
   -\frac1{24\pi}\{w,q\},\qquad
 \{w,q\}=\frac1{2q^2}.
\]

This is the transformation of the chiral normal-ordering/state term.
The full renormalized stress tensor for a fixed state transforms tensorially;
the Schwarzian accounts for the change of subtraction prescription.
The flat cap has no additional local curvature term. Therefore

\[
 \boxed{\displaystyle
 \langle T_{qq}\rangle
  =\frac1{\kappa^2q^2}
      \left[\tau_w(w)-\frac{\kappa^2}{48\pi}\right].}
\]

For the incoming w-vacuum, tau_w=0, so

\[
 \langle T_{qq}\rangle=-\frac1{48\pi q^2}.
\]

The divergence is genuine in the regular chart. For a smooth timelike
crossing with nonzero dot(q)_*, and finite other stress components,

\[
 \langle T_{ab}\rangle \dot\gamma^a\dot\gamma^b
 \sim-\frac1{48\pi(\tau_*-\tau)^2}.
\]

No reflection or backflow from the added region enters this calculation.
The outgoing sector cannot cancel this null component. This is a reduced
semiclassical obstruction for a specified state on a prescribed background,
not a solved Einstein-backreaction problem.

For a stationary incoming thermal state, tau_w=pi*T^2/12. Thus

\[
 \langle T_{qq}\rangle
  =\frac1{48\pi q^2}
       \left[\left(\frac{T}{T_H}\right)^2-1\right],
 \qquad T_H=\frac{\kappa}{2\pi}.
\]

At T=T_H the dangerous component cancels exactly. This is the incoming
sector of a state regular in the inertial cap coordinate q. Taking the
other sector regular in p as well gives the ordinary local Minkowski vacuum.
It is the familiar Rindler/Minkowski mechanism, not a new stabilization law.
Regularity of the stress expectation alone is weaker than extendibility of
the full state's two-point function as a Hadamard state.

More generally bounded Tqq requires

\[
 \tau_w(w)-\frac{\kappa^2}{48\pi}=O(e^{-2\kappa w}).
\]

A persistent temperature mismatch T=(1+epsilon)*TH leaves coefficient
(2*epsilon+epsilon^2)/(48*pi*q^2). By contrast, adding a compact reduced
classical/coherent pulse to a regular state changes tau_w only for a finite
interval of w, and does not spoil its eventual horizon regularity. A changed
temperature bath persists forever and is not a compact finite-energy
perturbation of that state. Therefore this calculation must not be described
as proving instability under every arbitrarily small localized perturbation.

For a nonflat but smooth product cap, the conformal vacuum-polarization
term in the p,q chart is smooth. The same q^-2 state obstruction persists,
up to finite geometric terms. This follows locally from smooth positive C;
the script uses the exactly flat case to avoid a renormalization ambiguity.

## 4. What changes in four dimensions

In a product cap the exact wave equation is

\[
 \frac4{C(pq)}\partial_p\partial_q\phi
       +\Delta_\perp\phi=0.
\]

A transverse Fourier mode with wave number k obeys

\[
 \partial_p\partial_q\phi_k
       =\frac{C(pq)|k|^2}4\phi_k.
\]

The coefficients are regular at q=0. For the flat cap this is just the
ordinary 4D Minkowski wave equation. For example
cos(a*A+b*B+ky*y+kz*z) solves it when 2ab=ky^2+kz^2 and has finite
stress at A=0. Smooth localized Minkowski Cauchy data also transmit locally
by ordinary hyperbolic evolution; no local high-frequency obstruction is
implied by the coordinate change.

However, smooth data prescribed across the extension are not a proof that
arbitrary original-bubble data evolve to such data. The finite aperture and
the wall can scatter radiation between transverse and longitudinal sectors.
Four-dimensional vacuum fluctuations require all transverse modes and 4D
renormalization, not the 2D conformal stress formula divided by an area.

For the actual stationary capped metric the full classical equation is

\[
 -\phi_{tt}-2v\phi_{tx}-v_x\phi_t
 +(1-v^2)\phi_{xx}-2vv_x\phi_x+\Delta_\perp\phi=0.
\]

Equivalently, using normal momentum P=phi_t+v*phi_x,

\[
 \phi_t=P-v\phi_x,\qquad P_t=\Delta\phi-\partial_x(vP).
\]

The divergence form is useful for a 2+1 axisymmetric classical computation,
with Delta_perp=partial_rho^2+rho^-1 partial_rho and regularity at rho=0.
One must measure flux in a smooth null chart on a fixed interior cap disk,
not infer singularity from stationary-frame energy alone. The required
global result is the late-w tail generated by compact original Cauchy data.
It has not been computed here. A full quantum result additionally requires
a global state (or a formation history selecting it) and its two-point function.

## 5. Interpretation for the draft

Established at this stage:

* The outlet transmits compact classical pulses regularly in the exact 1+1
  problem. The coordinate blueshift does not force all perturbations to fail.
* The same open passage has divergent reduced quantum stress for the incoming
  w-vacuum, even when the crossing neighborhood is exactly flat.
* A horizon-regular incoming state removes that divergence; compact reduced
  pulses preserve its eventual regularity. Persistent mismatched illumination
  does not. This is a state- and tail-dependent statement.
* The finite-aperture four-dimensional stability question remains unresolved.

Appropriate paper wording would distinguish regular geometry, regular field
states, and stability under specified perturbations. These calculations do
not justify either 'the cap is stable' or 'every cap transit is unstable'.

## 6. Verification and sources

`sim/cap_scalar_transmission.py` checks the Schwarzian and its sign by an
independent point-splitting limit, exact thermal cancellation, the flat-germ
coordinate coefficient, reduced Cauchy-data reconstruction, tail exponents,
and an exact nonzero-transverse-mode solution. Its output is in
`output/cap_scalar_transmission/`.

The conformal stress and horizon-state mechanism are standard. Relevant
comparisons are Finazzi, Liberati and Barcelo (2009), especially II.2 and
IV.3: https://arxiv.org/html/0904.0141v2 ; and Barcelo et al. (2022), III.3:
https://arxiv.org/html/2207.06458v1 . The former studies a particular dynamically
selected state; the latter explicitly estimates the higher-dimensional
stress from geodesics rather than calculating the full RSET. Neither should
be represented as having solved our finite-aperture 4D transmission problem.
