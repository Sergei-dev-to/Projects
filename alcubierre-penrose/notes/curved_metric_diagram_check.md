# Drawing the rescaled metric: what passes and what fails

The interior inverse coloring passes, but the laboratory double-cone
coordinates do not supply a unified boundary chart for the regular
completion constructed in `proper_conformal_completion.md`.
The new drawing is a diagnostic, not a completed global Penrose diagram.
No manuscript figures or claims have been changed.

Reproduce with Python 3.12 and numpy/scipy/matplotlib:

    python exploration/curved_metric_diagram.py

Outputs:

- `output/global_2p1/actual_curved_conformal_metric.png`
- `output/global_2p1/curved_metric_diagram_check.json`

## Metric and gauge used for this drawing

Keep the same physical metric, cap gauge and comoving cutoff as in the
previous construction. In the exterior replace the hyperboloidal gauge
by the equivalent full Einstein-cylinder gauge

\[
 \omega_E={2\over\sqrt{1+(t-R)^2}\sqrt{1+(t+R)^2}},\qquad
 \Omega_D=\chi\omega_c+(1-\chi)\omega_E.
\]

This is positive and smooth on the original spacetime, and equals the
previous factor near the cap. On every finite ordinary-scri cut it
differs from the previous factor by a smooth positive multiplier; the
boundary ratio is \((1+\tau^2)^{-1/2}\). It also allows the usual exterior
timelike vertices to be included. Rider, rim and spatial corners remain
unadjoined.

Let f be the laboratory double-cone map, with Jacobian J. The actual
metric plotted is

\[
 G=\Omega_D^2 J^{-T}gJ^{-1}.
\]

The red tangent cones are obtained by applying J to the actual future
null vectors \((1,v+\cos\alpha,\sin\alpha)\). Their normalized squared
norms in G are below 3.6e-16 in the audit. The exterior metric agrees
with the standard cylinder metric to 1.6e-15 in a checked sample.
The independent cap-chart null check is below 6.7e-16.

The earlier inverse classification and surface tests are reused:
1,523,395 interior grid points; the bubble is inside the communication
region at every sampled point. The directly transformed wall and tube
boundaries satisfy the inverse equations to below 3.6e-11 and 2e-11.
These checks validate the finite-interior image, not its boundary.

## Height is not physical future time

For the rider x=y=0, V=2 and t>0,

\[
 z_c=\arctan(3t)-\arctan(t),\qquad
 x_c=\arctan(3t)+\arctan(t).
\]

Its height reaches pi/6 at t=1/sqrt(3), then decreases towards zero.
At t=1.5 the future rider tangent has dz_c/dt=-0.1665158371. The actual
cones tilt accordingly. This is consistent with a curved conformal
metric in these coordinates; it rules out interpreting z_c as a global
temporal coordinate or using the background cylinder cones inside the
bubble. A downward coordinate tangent does not itself disprove a
conformal rescaling.

For example at the center the future outgoing null vector has image
(6,0,2). Its actual rescaled squared norm is zero; its reference
cylinder squared norm is +32. The reference cones are therefore wrong
there even before considering endpoints.

## The decisive boundary failure

In this same map the following three distinct approaches all tend to
the coordinate value (x_c,y_c,z_c)=(pi,0,0):

1. Rider future: t -> infinity, x=y=0.
2. A finite front-cap crossing: q -> 0+, fixed finite p, |y|<0.6.
3. Ordinary spatial infinity: t=0, x -> infinity, y=0.

Indeed every bounded comoving (x,y) sequence with t -> infinity has
R=2t+x+O(1/t), hence t-R -> -infinity and t+R -> infinity.
All finite p and y values on the front-cap exit face have the same
double-cone coordinate limit. The time-reversed collision occurs at
(-pi,0,0).

These are not consistent identifications in the chosen completion:
Omega_D tends to zero on the rider and spatial sequences, whereas it
has a positive limit at a finite cap crossing. In the supplement's
normalization, p=0.4 gives cap Omega=0.9226043263. The exit face is a
regular physical surface, with metric

\[
 \widehat g=\Omega_D^2[C(pq)\,dp\,dq+dy^2],\qquad C(0)=2.
\]

It is not ordinary null infinity. Along the original-side approach to
this face the laboratory retarded coordinate u=t-R tends to -infinity;
it does not tend to any finite ordinary-scri cut.

Thus the common coordinate corner cannot be used as a single boundary
point with continuous Omega_D, or as a chart on the specified cap
continuation. The full two-dimensional cap face has been collapsed,
not just the rider endpoint. Interior invertibility does not prevent
this boundary collapse.

## Consequence for the proposed figure

The large panel shows the checked interior coloring and actual local
cones. Open orange marks are finite cutoffs indicating rider approach,
not attached endpoints. The waist and its identifications are excluded.
The separate cap panel shows q=0, p=0, a timelike crossing and excluded
rim marks. It is a different regular chart on the conformal metric,
not an extra piece of ordinary scri.

An actual unified diagram still needs a coordinate construction that
resolves the collapsed corner into the distinct cap faces and remaining
ideal ends, while matching the exterior boundary. The earlier global
positive rescaling and regular boundary atlas did not establish this
coordinate construction. This failure does not prove that such a
construction is impossible.
