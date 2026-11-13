# Inverse-classified bubble and communication tube inside the full cone

This calculation colors the actual finite spacetime interior in the
background double-cone coordinates. It does not assign a resolved
boundary meaning to that cone's vertices or waist.

## Pointwise construction

The cone coordinates are (xc,yc,zc), with zc compact background time,
chi=hypot(xc,yc), and |zc|+chi<pi. Define D=cos(zc)+cos(chi). Then

    t=sin(zc)/D,
    Xlab=sinc(chi/pi)*xc/D,
    y=sinc(chi/pi)*yc/D,
    x=Xlab-2t.

Here numpy's sinc convention is sin(pi z)/(pi z), so its appearance
above means sin(chi)/chi, with the usual removable value 1 at chi=0.

At every finite point the bubble-interior test is

    x^2+psi(y)-1 < 0,

where psi(y) is the code's signed-y version of the manuscript's function
of rho squared. The communication-tube test is

    -h(y) < x < h(y).

The figure uses purple for the former and teal for the additional part
of the latter. White points are outside both. The capped profile has
V=2, L=1, aperture a=0.6, and the previously specified globally bounded
W. The physical symmetry-angle quotient folds the signed y halves.

## Sampling and independent checks

A 181-by-181-by-181 display grid is streamed through the inverse. There
are 1,523,395 strictly interior sample points. Of these, 294,185 are in
the bubble and 329,705 are in the communication tube. These are grid
counts, not physical spacetime volume fractions. Every sampled bubble
point is also in the communication tube.

Surface meshes generated from the actual wall and the previously
calculated horizons supplement the grid where the coordinate ends
become thin. Their original times extend to about +/-100.17. Every
finite mesh point is inverted independently before drawing. The maximum
wall-function residual is 3.53e-11; the maximum communication-boundary
residual is 1.90e-11. The maximum coordinate round-trip error on those
large-time surfaces is 1.64e-10.

The axial slice yc=0 independently gives identical classifications for
the two regions, as expected: both reduce to -1<x<1 there. The
equatorial slice zc=0 is exactly the original t=0 section and displays
their transverse difference.

## What the coordinate image shows

Both regions run across the waist of the full double cone, forming a
curved, flattened volume. The central rider traces an S-shaped axial
curve. Its maximum compact height is pi/6 at t=1/sqrt(3), after which
the displayed height decreases while physical rider time increases.

All bounded fixed comoving positions approach (xc,yc,zc)=(pi,0,0) as
t goes to plus infinity and (-pi,0,0) as t goes to minus infinity in
this directional display. Thus this picture visually compresses distinct
bubble end behaviors. The finite-interior coloring is exact; it does
not resolve that boundary compression or identify these auxiliary
limits with a particular physical infinity. The previous pinched-tube
image used different coordinates and a different conformal gauge.

Outputs:

- `output/global_2p1/inverse_colored_full_cone.png`
- `output/global_2p1/inverse_colored_full_cone_check.json`

Reproduction: `exploration/color_full_cone.py`, using
`exploration/cone_point_classifier.py` for the inverse and
`exploration/capped_horizon_atlas.py` for the actual capped profile
and horizon. The paper and saved PDF are unchanged.
