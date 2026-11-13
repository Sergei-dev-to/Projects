# Exact matching of the tube to ordinary null infinity

The new calculation establishes an actual overlap of the tube chart and
the exterior conformal chart. It does **not** establish a single global
coordinate embedding of the completed spacetime. The figure identifies
the same finite event and the same null ray in both charts. The manuscript
and saved PDF are unchanged.

## The direct overlap and the matched null generator

For the bounded capped profile, the exterior sending wing is exactly
x=C-sqrt(3)|y|, C=2.637158424722. The communication tube ends transversely
at y*=C/sqrt(3), approximately 1.52256. The full metric is already flat
for |y|>=1.31221, so the tube and exterior charts have an open overlap.

Choose event A: t=0, y=-1.4, x=C-1.4 sqrt(3)=0.212287294126.
The actual full shift there is v=-2, while its axial reference v0(x)=0.
The check uses the full metric, not the product-cap approximation.

The exact affine null geodesic through A is

    t=s, x=x_A-1.5s, y=-1.4-sqrt(3)s/2.

Its laboratory velocity is (1/2,-sqrt(3)/2). It leaves the communication
tube at x=0, |y|=y*, s=0.141524862750, and continues on the sending
horizon to ordinary future scri. The complete horizon extends outside
the communication tube; the tube itself does not reach this finite-u
scri point.

## The two maps and their conformal transition

In the overlap |x|<0.5 the axial core is flat, giving exactly

    p=exp(t-x), q=exp(-t-x),
    alpha=2 tanh((t-x)/2), beta=tanh((t+x)/2),
    T_tube=(alpha+beta)/2, X_tube=(beta-alpha)/2,
    Y_tube=sqrt(2/C0)(1-alpha beta/2)y,
    C0=2.772600879803.

The exterior chart uses laboratory X=x+2t, R=hypot(X,y), theta=atan2(y,X):

    T_ext=atan(t-R)+atan(t+R),
    chi=atan(t+R)-atan(t-R),
    Z1=chi cos(theta), Z2=chi sin(theta).

Its conformal metric is -dT_ext^2+dchi^2+sin(chi)^2 dtheta^2 and
Omega_ext=cos(T_ext)+cos(chi). Composing the physical-coordinate maps
gives the actual chart transition. The metric pullback residual is below
2e-15; the metrics agree under transition with the relative conformal
factor (Omega_tube/Omega_ext)^2. The ray is null and future-oriented in
both charts.

A has tube coordinates (0.15862022,-1.20234431,-0.05287341) and exterior
coordinates (0.28662095,-1.89021831,0). The figure's dashed double arrow
identifies these depictions of the SAME EVENT, not a flight between them.

## Ordinary scri and the separate cap exit

The highlighted null generator tends to theta=-pi/3, u=t-R=-C/2,
approximately -1.318579212361. Its exterior display endpoint is
(1.24637111,-2.15877809,0.64885043). The large-radius calculation agrees
with this analytic limit. Time reversal and x reflection give the
receiving horizon's past-scri connection. The bold half-generators on
scri still denote the full surface closure, as derived in the earlier
notes; a fixed generator ends at the endpoint of that half-generator.

The existing unit timelike cap-crossing geodesic is transformed into the
tube chart after matching its P,Q normalization, not by reusing its old
local p,q numbers. Its global crossing label is p=1.053825924953 and its
conformal factor at q=0 is 0.827061269287, strictly positive. The local
physical continuation passes to q<0; this is the purple curve.

On its original side, q=exp(-10),exp(-20),exp(-40) gives lab retarded
times about -10.1467,-20.1456,-40.1450. Its crossing point is therefore
distinct from the ordinary finite-u scri point reached by the exterior
wing. This does not determine the eventual asymptotic future of the
continued traveler: the paper specifies a local cap attachment, not a
unique complete continuation with fixed asymptotic regions.

## The unresolved single-domain construction

Applying the exterior formula merely as a background coordinate map to
the actual rider gives T_ext=0.06634766 at t=10 and 0.03329327 at t=20.
Its time decreases along the future-timelike rider. In that background
map, infinite rider time and finite-parameter bubble ends collapse to
the spatial corner. This is a coordinate-map failure, not a physical
identification of those ends with spatial infinity.

An unchanged Minkowski cone therefore cannot serve as a common
coordinate domain with the derived tube simply placed inside it. A
different global map may exist, but needs a construction through that
corner which separates these ends. The finite overlap and matched rays
established here do not supply it.

Together with the stationary chart for nonflat events outside the tube,
these charts give the global open atlas described in
`capped_global_horizon_atlas.md`. The new figure emphasizes its actual
tube-to-exterior overlap. It does not represent every event of the
additional stationary chart, or complete the spatial corner, rider
ends and excluded rim.

Run `exploration/tube_scri_matching.py`; checks precede drawing. Outputs:

- `output/global_2p1/tube_scri_matching_check.json`
- `output/global_2p1/tube_to_scri_matched.png`

This is a checked matched-chart connection, not the requested single
completed global 2+1 conformal coordinate picture. That gap remains.
