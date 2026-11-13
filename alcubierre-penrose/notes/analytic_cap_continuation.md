# Analytic continuation of the cap germ

The compact bubble is globally smooth and nonanalytic. This calculation
continues only the analytic metric germ at its planar aperture onto an
added branch. It does not replace the original bounded profile W outside
its affine collar, and does not prove a maximal extension of the full bubble.

## Plotted cap

In the normalization L=kappa=1, the plotted collar has

\[
v_0(x)=-(1+x^2)/2,\qquad
F(x)=1-v_0(x)^2=(1-x^2)(x^2+3)/4.
\]

The germ is analytic and independent of the transverse coordinates. On a
selected added product branch its analytic continuation retains this F.
The two roots x=+/-1 are simple, regular Killing horizons. Static T fails
there, but the existing Kruskal coordinates are analytic through the front.

For the four-dimensional product metric,

\[
R=-F''=1+3x^2,\qquad
R_{abcd}R^{abcd}=(1+3x^2)^2.
\]

There is no curvature obstruction at finite x. The future outgoing branch
past the front has x>1 and reaches x=+infinity, where both invariants diverge.
For a longitudinal unit timelike geodesic with Killing energy E,

\[
\dot x=+\sqrt{E^2-F(x)},\qquad
\Delta\tau=\int_1^\infty\frac{dx}{\sqrt{E^2-F(x)}}<\infty.
\]

The integrand is asymptotic to 2/x^2. The traveler used in the figures has
E approximately 1.18630752167; the remaining proper time after crossing is
approximately 1.50863164525 in these normalized units.

For non-generator longitudinal null geodesics, dx/dlambda is constant,
so the same x=infinity limit is at infinite affine parameter. Finite proper
time for massive outgoing geodesics must not be generalized to every null ray.

The front regular coordinates obey

\[
pq=s^2\frac{1-x}{1+x}
\exp\left[-\frac2{\sqrt3}\arctan(x/\sqrt3)\right],
\quad s^2=2e^{\pi/(3\sqrt3)}.
\]

Thus x=+infinity is the finite product value
pq=-2 exp[-2pi/(3sqrt(3))], approximately -0.596872118385. This is a genuine
curvature end, not a failure of the inverse transformation at a regular point.

## Exactly flat variant

For the tailored germ v=-sqrt(1+2kappa(x-L)),

\[
F=-2\kappa(x-L),\qquad R=0.
\]

The isolated metric germ has Minkowski analytic development. Failure of
the square-root shift to stay real for all x is a failure of that chosen
coordinate representation, not a curvature obstruction of Minkowski space.

More concretely, inside the front horizon set x-L=-kappa*r^2/2. The static
metric becomes -kappa^2*r^2*dT^2+dr^2+dy^2+dz^2. Coordinates
TM=r*sinh(kappa*T), XM=r*cosh(kappa*T) identify it with a right Rindler
wedge. Its future horizon opens into the Minkowski future wedge TM>|XM|.
An inertial timelike trajectory crossing that future horizon stays in the
future wedge thereafter. For a longitudinal unit-mass geodesic with
conserved Killing energy E>0, the continuation has

\[
 x-L=E(\tau-\tau_*)+\frac\kappa2(\tau-\tau_*)^2.
\]

It has arbitrarily large future proper time, with zero curvature. This is
a natural unbounded far-side choice for the exactly flat aperture germ.
It does not require the original core and curved wall to become Minkowski:
only the overlapping flat collar is identified. The longitudinal statement
does not resolve the transverse attachments or maximality of the entire
compact bubble. The smooth metric can retain the curved original regions
and the added flat sector; a global analytic metric could not do so.

Neither this fact nor the polynomial continuation automatically incorporates
the full original compact bubble. Original nonanalytic transition layers must
be retained by smooth overlap gluing; they cannot be recovered by analytic
continuation of the cap germ. The rim obstruction continues to apply. A
globally analytic connected extension cannot contain the entire original
nonanalytic bubble isometrically with its given smooth structure.

## Reproduction

Run `python exploration/analytic_cap_continuation.py`. It checks the curvature
polynomial, evaluates the timelike proper-time integral, and verifies the
front-chart product limit. Results are saved in
`output/useful_2p1_view/analytic_cap_continuation_checks.json`.
