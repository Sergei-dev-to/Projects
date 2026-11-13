# Exploration scripts

`analytic_cap_continuation.py` computes the analytic continuation of the
plotted planar cap germ onto an added outgoing branch. Its polynomial F
has regular horizons but scalar curvature diverging at x=+infinity,
reached by the plotted massive traveler in finite further proper time.
The exactly flat cap variant instead has an isolated Minkowski analytic
development. Neither calculation establishes maximality for the full
compact nonanalytic bubble. See `notes/analytic_cap_continuation.md`.

## Current useful 2+1 view

`useful_2p1_view.py` makes a physical geometry illustration with time
pointing upward: stationary horizon sheets, their transverse wings,
local tangent cones, integrated null rays, a spatial communication
cross-section, and a regular cap detail. The SAME unit timelike geodesic
is shown in the original patch and crossing the cap. Both time coordinates
are temporal, and shared events are matched numerically.

Open `output/useful_2p1_view/useful_2p1_geometry.html` to rotate the sheets,
look down the time axis, or inspect the cap crossing. The cap's axial
projection shows the longitudinal null directions at 45 degrees. The
static PNG accompanies it. This supplements the 1+1 Penrose diagram; it
does not claim a full 2+1 diagram with flat light cones everywhere.
See section 22 of the boundary notes. The manuscript is unchanged.

`connect_2p1_penrose.py` adds a matched axial conformal diagram for this
same bounded capped profile, with the same traveler and labeled shared
events. The optical coordinates agree with the regular cap coordinates;
ordinary null infinity, cap crossings, the front generator end, and the
rider end are distinguished explicitly. The selected y=0.3 slice is
isometric to the axis because the shift is independent of y throughout
the planar slab. Outputs are `penrose_connection.png`, `.svg`, and
`penrose_connection_checks.json` in the same output directory. See
section 23 of the boundary notes for the map and boundary limits.

`horizon_boundary_attachments.py` connects that reference diagram to the
open cap strip and the angular surface of ordinary future null infinity.
It tracks the same finite events F+ and F- on exterior null generators in
the physical and boundary charts. The wing generator endpoints at
theta=+/-60 degrees, u=uM are distinguished from the closure of the whole
wing on u<=uM. The cap's C+ point becomes a transverse curve, while the
traveler crosses elsewhere on the cap strip. The output is
`horizon_boundary_attachments.png` / `.svg`, with numerical checks in
`horizon_attachment_checks.json`. This is a matched attachment atlas,
not a claim that these panels share one Euclidean embedding. See section 24.

`unified_attachment_view.py` now puts the front cap, sending-horizon sheet,
outer wing contacts and ordinary future null infinity into ONE coordinate
picture, with a rotatable `unified_attachments.html` and a static PNG/SVG.
It reuses the verified convex coordinate map for **attachments only**, then
applies a smooth injective display stretch to enlarge the cap. The height
is explicitly not physical time. This does not revive the old claim that
the convex picture is a useful global Penrose diagram. The front/future
surfaces are selected samples, with finite mesh cuts; no smooth cap-rim
bridge or full boundary classification is claimed. See section 25.

## Earlier global coordinate compactification

The following convex construction remains a coordinate/metric calculation,
but was rejected as an effective causal visualization. Its displayed
height is not temporal, and the drawing does not visually encode a
standard light cone. Do not present it as the requested finished
Penrose-style diagram.

`global_convex_conformal.py` now constructs ONE bounded domain for the
entire original patch. The map is the gradient of a strictly convex
potential, with a global inverse characterized by minimization. The same
positive conformal factor gives regular null infinity and regular open
cap crossings in these global coordinates. Other boundary pieces retain
approach directions and are allowed to be singular. See sections 16--21
of [`notes/joint_boundary_limits.md`](../notes/joint_boundary_limits.md).

Outputs in `output/global_convex_conformal/` include the checked metric
data, `global_conformal_domain.png`, and the self-contained interactive
`global_conformal_domain.html`. The enlarged cap view is part of the same
global coordinate body. This is not an everywhere-smooth completion, a
minimal Penrose boundary, or a maximal physical extension. The display
height is not asserted to be a global time function. The manuscript is
unchanged.

## Earlier causal-boundary analysis

The exceptional-end analysis is in sections 11--15 of
[`notes/joint_boundary_limits.md`](../notes/joint_boundary_limits.md), checked
by `exceptional_boundary_audit.py`. It constructs distinct finite-label rim
families, proves a uniform escape bound outside the receiving region,
classifies several large-label limits, and proves that the standard
chronological c-boundary is **non-Hausdorff** at the Mach-direction contact:
one sequence of ordinary-scri endpoints converges both to a scri point and
to the rider point. This obstructs a faithful Hausdorff drawing of that
causal completion. It does not rule out every conformal completion with
a different topology, nor complete the classification of all mixed ends.
`output/exceptional_boundary_audit/boundary_incidence.png` shows only these
verified relations; it is not a global conformal embedding.

The rider-end classification is now proved in sections 6--10 of
[`notes/joint_boundary_limits.md`](../notes/joint_boundary_limits.md), with
quantitative checks in `rider_endpoint_audit.py`. The original patch has
one future and one past **causal** rider endpoint. An exact signal-time
criterion determines convergence from the closed receiving region; the negative
infinite end of the front cap attaches to the future rider point. These
are not regular smooth conformal vertices. The later sections above
address the rim and several horizon/spatial limits.

The uniformly pinched closure in `band_tube_shape.py` is **retired as a
causal or conformal completion**: it sends fixed-position sending-horizon
sequences to the future rider point, contradicting openness of chronology.
Its finite-interior coordinate calculations remain valid. This warning
also applies to later pictures that reuse that boundary identification.

The joint angular analysis is now in `joint_boundary_limits.py` and
[`notes/joint_boundary_limits.md`](../notes/joint_boundary_limits.md).
It proves uniform exclusion of finite scri at the critical label and
supplies the corrected flow label, inverse map, full-angular scri metric,
and regular boundary transition domains. The remaining exceptional-end
topology is open; the convergence plot is not a global Penrose diagram.

The latest global calculation is `global_spacelike_flow.py`, documented in
[`notes/global_spacelike_flow.md`](../notes/global_spacelike_flow.md).
It supplies one transverse-safe temporal coordinate on the whole original
spacetime and extends through both open caps. The joint angular analysis
above supplies the ordinary-scri chart; exceptional ends still prevent
claiming a completed global diagram.

Use `verified_2p1_start.py` and
[`notes/verified_2p1_start.md`](../notes/verified_2p1_start.md). This starts
from the exact physical cap metric and the exact flat exterior, reuses
the checked conformal factor, and verifies their local boundary charts.
It does not assume a global boundary shape or identify rider ends.

The laboratory double-cone approach (`cone_point_classifier.py`,
`color_full_cone.py`, and `curved_metric_diagram.py`) is **retired as a
candidate global conformal construction**. Its interior coordinate and
coloring checks do not validate its boundary identifications. The old
code, notes and images remain diagnostic records, not inputs or templates
for the new construction. In particular `inverse_colored_full_cone.png`
and `actual_curved_conformal_metric.png` must not be used as global
Penrose diagrams.

## Development history

Development-history calculations for *When Warp Horizons Extend: Curvature
Boundaries of Alcubierre Spacetimes*.  These are the working scripts as they
were written during the investigation, including approaches that were later
superseded or cut from the paper.

**This is not the reproducibility package.**  The curated, documented and
runnable checks that accompany the manuscript live in `paper/supplement/`;
run them with `python run_all.py` from that directory.  Where a script here
shares a name with one there, the `paper/supplement/` copy is canonical.
