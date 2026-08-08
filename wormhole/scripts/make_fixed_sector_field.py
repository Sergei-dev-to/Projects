"""Calculated fixed-sector field lines near one wormhole mouth.

This computes the axisymmetric electrostatic short-throat matching problem in
a 2D meridional slice.  A point charge q is held at distance A from mouth B.
The two spherical mouth boundaries of radius R are glued with continuity of
potential and the orientation-reversed normal derivative.  The l=0 throat flux
sector is held fixed to zero; the constant potential offset between the two
ends absorbs the l=0 boundary value.  The plotted source-side field therefore
contains the actual source plus the l>=1 harmonic corrections, but no induced
mouth monopole.

The script writes fig_fixed_sector_field.svg.  It uses only the Python standard
library.
"""

from __future__ import annotations

import html
import math
from pathlib import Path


OUT = Path("fig_fixed_sector_field.svg")

R = 1.0
Q = 1.0
A = 2.55
L_MAX = 70

XMIN, XMAX = -2.20, 3.80
YMIN, YMAX = -2.12, 2.12
WIDTH, HEIGHT = 1080, 720
PAD = 42


def legendre_values(mu: float, lmax: int) -> list[float]:
    vals = [1.0]
    if lmax == 0:
        return vals
    vals.append(mu)
    for ell in range(1, lmax):
        vals.append(((2 * ell + 1) * mu * vals[-1] - ell * vals[-2]) / (ell + 1))
    return vals


def phi(x: float, y: float) -> float:
    """Source-side potential in the zero l=0 flux sector."""
    rho = math.hypot(x - A, y)
    val = Q / max(rho, 1.0e-8)

    r = math.hypot(x, y)
    if r <= R:
        return float("nan")
    mu = x / r
    p = legendre_values(mu, L_MAX)

    # Matching coefficients for ell>=1:
    # a_l = - q R^(2l+1) / [2(l+1) A^(l+1)].
    # The ell=0 term is omitted because the throat flux sector is fixed.
    for ell in range(1, L_MAX + 1):
        a_ell = -Q * R ** (2 * ell + 1) / (2 * (ell + 1) * A ** (ell + 1))
        val += a_ell * p[ell] / (r ** (ell + 1))
    return val


def field(x: float, y: float) -> tuple[float, float]:
    """Electric field E=-grad Phi by a small central difference."""
    h = 1.5e-4
    if math.hypot(x, y) <= R + 2 * h:
        return (0.0, 0.0)
    ex = -(phi(x + h, y) - phi(x - h, y)) / (2 * h)
    ey = -(phi(x, y + h) - phi(x, y - h)) / (2 * h)
    return ex, ey


def inside_mouth(x: float, y: float, margin: float = 0.0) -> bool:
    return x * x + y * y <= (R + margin) ** 2


def near_charge(x: float, y: float) -> bool:
    return (x - A) * (x - A) + y * y < 0.026


def to_px(x: float, y: float) -> tuple[float, float]:
    sx = PAD + (x - XMIN) / (XMAX - XMIN) * (WIDTH - 2 * PAD)
    sy = HEIGHT - PAD - (y - YMIN) / (YMAX - YMIN) * (HEIGHT - 2 * PAD)
    return sx, sy


def path_d(points: list[tuple[float, float]]) -> str:
    if not points:
        return ""
    x0, y0 = to_px(*points[0])
    parts = [f"M {x0:.2f} {y0:.2f}"]
    for p in points[1:]:
        x, y = to_px(*p)
        parts.append(f"L {x:.2f} {y:.2f}")
    return " ".join(parts)


def trace(seed: tuple[float, float], sign: float, ds: float = 0.016, nmax: int = 1700) -> list[tuple[float, float]]:
    x, y = seed
    pts: list[tuple[float, float]] = []
    for _ in range(nmax):
        if x < XMIN or x > XMAX or y < YMIN or y > YMAX:
            break
        if inside_mouth(x, y, 0.006) or near_charge(x, y):
            if pts:
                break
        pts.append((x, y))
        ex, ey = field(x, y)
        n = math.hypot(ex, ey)
        if n < 1.0e-9:
            break
        x += sign * ds * ex / n
        y += sign * ds * ey / n
    return pts


def boundary_flux_density(theta: float) -> float:
    x = (R + 0.004) * math.cos(theta)
    y = (R + 0.004) * math.sin(theta)
    ex, ey = field(x, y)
    return ex * math.cos(theta) + ey * math.sin(theta)


def source_seeds() -> list[tuple[float, float]]:
    eps = 0.17
    angles = [
        -2.55, -2.25, -1.95, -1.65, -1.35, -1.05, -0.78, -0.52,
        -0.27, 0.0, 0.27, 0.52, 0.78, 1.05, 1.35, 1.65, 1.95, 2.25, 2.55,
    ]
    return [(A + eps * math.cos(t), eps * math.sin(t)) for t in angles]


def mouth_outflow_seeds() -> list[tuple[float, float]]:
    seeds: list[tuple[float, float]] = []
    # Seed only where the source-side field leaves the mouth sphere into this
    # exterior.  Where it enters the mouth, source-origin lines terminate.
    for i in range(240):
        theta = -math.pi + 2 * math.pi * i / 240
        if boundary_flux_density(theta) > 0.035:
            # Keep the set sparse and visually legible.
            if not seeds or abs(theta - math.atan2(seeds[-1][1], seeds[-1][0])) > 0.22:
                seeds.append(((R + 0.026) * math.cos(theta), (R + 0.026) * math.sin(theta)))
    return seeds


def contour_segments(levels: list[float]) -> list[str]:
    nx, ny = 142, 100
    xs = [XMIN + i * (XMAX - XMIN) / (nx - 1) for i in range(nx)]
    ys = [YMIN + j * (YMAX - YMIN) / (ny - 1) for j in range(ny)]
    vals = [[phi(x, y) if not inside_mouth(x, y, 0.02) and not near_charge(x, y) else float("nan") for x in xs] for y in ys]
    out: list[str] = []

    def interp(p0, p1, level):
        x0, y0, v0 = p0
        x1, y1, v1 = p1
        if not (math.isfinite(v0) and math.isfinite(v1)) or abs(v1 - v0) < 1e-12:
            return None
        if (v0 - level) * (v1 - level) > 0:
            return None
        t = (level - v0) / (v1 - v0)
        if 0 <= t <= 1:
            return (x0 + t * (x1 - x0), y0 + t * (y1 - y0))
        return None

    for level in levels:
        for j in range(ny - 1):
            for i in range(nx - 1):
                c = [
                    (xs[i], ys[j], vals[j][i]),
                    (xs[i + 1], ys[j], vals[j][i + 1]),
                    (xs[i + 1], ys[j + 1], vals[j + 1][i + 1]),
                    (xs[i], ys[j + 1], vals[j + 1][i]),
                ]
                hits = []
                for k0, k1 in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                    hit = interp(c[k0], c[k1], level)
                    if hit is not None:
                        hits.append(hit)
                if len(hits) == 2:
                    p0, p1 = to_px(*hits[0]), to_px(*hits[1])
                    out.append(f'<path d="M {p0[0]:.2f} {p0[1]:.2f} L {p1[0]:.2f} {p1[1]:.2f}" class="equip"/>')
    return out


def text(x: float, y: float, s: str, cls: str = "label", anchor: str = "middle") -> str:
    px, py = to_px(x, y)
    return f'<text x="{px:.2f}" y="{py:.2f}" text-anchor="{anchor}" class="{cls}">{html.escape(s)}</text>'


def flux_check() -> float:
    # Axisymmetric 3D flux through the mouth sphere, proportional to
    # integral E_r sin(theta) dtheta.  It should be numerically near zero.
    n = 2200
    total = 0.0
    for i in range(n):
        th = math.pi * (i + 0.5) / n
        total += boundary_flux_density(th) * math.sin(th)
    return 2 * math.pi * R * R * total * math.pi / n


def main() -> None:
    lines: list[str] = []
    for seed in source_seeds():
        pts = trace(seed, +1)
        if len(pts) > 12:
            lines.append(f'<path d="{path_d(pts)}" class="field" marker-end="url(#arrow)"/>')
        pts_back = trace(seed, -1)
        if len(pts_back) > 12:
            lines.append(f'<path d="{path_d(pts_back)}" class="field back" marker-end="url(#arrow)"/>')

    for seed in mouth_outflow_seeds():
        pts = trace(seed, +1)
        if len(pts) > 12:
            lines.append(f'<path d="{path_d(pts)}" class="field mouthline" marker-end="url(#arrow)"/>')

    equip = contour_segments([-0.38, -0.26, -0.16, -0.08, 0.08, 0.16, 0.28, 0.44, 0.70, 1.05])
    cx, cy = to_px(0, 0)
    rx = (WIDTH - 2 * PAD) * R / (XMAX - XMIN)
    ry = (HEIGHT - 2 * PAD) * R / (YMAX - YMIN)
    qx, qy = to_px(A, 0)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<defs>
<style>
.bg {{ fill: #fbfaf6; }}
.equip {{ stroke: #d9ccba; stroke-width: 1.0; fill: none; opacity: 0.60; }}
.field {{ stroke: #2f6f9f; stroke-width: 1.85; fill: none; stroke-linecap: round; opacity: 0.94; }}
.back {{ opacity: 0.82; }}
.mouthline {{ stroke: #3f7fa6; opacity: 0.82; }}
.mouth {{ fill: #eef2f6; stroke: #20242a; stroke-width: 2.0; }}
.rim {{ fill: none; stroke: #b8c2ce; stroke-width: 1.5; }}
.charge {{ fill: #b23b3b; stroke: #20242a; stroke-width: 1.2; }}
.label {{ font: 18px Georgia, 'Times New Roman', serif; fill: #20242a; }}
.small {{ font: 15px Georgia, 'Times New Roman', serif; fill: #68707d; }}
.title {{ font: bold 20px Georgia, 'Times New Roman', serif; fill: #20242a; }}
.measure {{ stroke: #68707d; stroke-width: 1.4; fill: none; }}
</style>
<marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.2" markerHeight="5.2" orient="auto">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#2f6f9f"/>
</marker>
<marker id="arrowSmall" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto">
<path d="M 0 0 L 10 5 L 0 10 z" fill="#68707d"/>
</marker>
<marker id="arrowSmallBack" viewBox="0 0 10 10" refX="1.5" refY="5" markerWidth="5" markerHeight="5" orient="auto">
<path d="M 10 0 L 0 5 L 10 10 z" fill="#68707d"/>
</marker>
</defs>
<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" class="bg"/>
<rect x="16" y="16" width="{WIDTH-32}" height="{HEIGHT-32}" rx="8" fill="none" stroke="#ddd4c6"/>
{''.join(equip)}
{''.join(lines)}
<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" class="mouth"/>
<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{0.82*rx:.2f}" ry="{0.82*ry:.2f}" class="rim"/>
<circle cx="{qx:.2f}" cy="{qy:.2f}" r="13.5" class="charge"/>
{text(A + 0.14, 0.18, "q", "label", "start")}
<path d="M {to_px(0,-0.66)[0]:.2f} {to_px(0,-0.66)[1]:.2f} L {to_px(A,-0.66)[0]:.2f} {to_px(A,-0.66)[1]:.2f}" class="measure" marker-start="url(#arrowSmallBack)" marker-end="url(#arrowSmall)"/>
{text(A/2, -0.82, "A", "small")}
{text(0, -1.30, "mouth sphere S_B", "label")}
<text x="{to_px(-2.02,1.94)[0]:.2f}" y="{to_px(-2.02,1.94)[1]:.2f}" text-anchor="start" class="title">fixed-sector multipole solution</text>
<text x="{to_px(-2.02,1.69)[0]:.2f}" y="{to_px(-2.02,1.69)[1]:.2f}" text-anchor="start" class="small">short-throat matching, modes ell=1..{L_MAX}</text>
<text x="{to_px(-2.02,1.46)[0]:.2f}" y="{to_px(-2.02,1.46)[1]:.2f}" text-anchor="start" class="small">ell=0 throat flux held fixed to zero</text>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"L_MAX={L_MAX}, A/R={A/R:.3f}, flux_check={flux_check():+.3e}")


if __name__ == "__main__":
    main()
