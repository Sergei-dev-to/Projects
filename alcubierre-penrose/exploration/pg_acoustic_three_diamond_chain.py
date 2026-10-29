"""Vertex-attached PG/acoustic conformal chain for the planar sech warp slab.

The calculation uses the exact null coordinates for

    ds^2 = -dt^2 + [dx - v(x) dt]^2,
    v(x) = 2(sech x - 1),

and then places the calculated exterior branches at the finite-affine
endpoint vertices of the central Alcubierre/bubble interval.  This is the
extension relevant to the C-/C+ endpoint calculation: the attachment is at a
corner, not along a whole horizon edge.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from sech_extension import Params, compact, horizons, kappa, u_region, w_coord


OUT = Path("output/sech")


def penrose(U: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    uu = np.arctan(U)
    vv = np.arctan(V)
    return 0.5 * (vv - uu), 0.5 * (vv + uu)


def plot() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p = Params()
    kap = kappa(p)
    r1, r2 = horizons(p)
    eps = 2.0e-5 * (r2 - r1)

    # Exact C-/C+ endpoint locations in the central compact chart.
    b = 0.5 * np.pi
    a0 = float(np.arctan(0.5))
    c_minus = np.array([-0.5 * (b - a0), -0.5 * (b + a0)])
    c_plus = np.array([0.5 * (b - a0), 0.5 * (b + a0)])

    fig, ax = plt.subplots(figsize=(10.4, 8.0), constrained_layout=True)

    # Central original patch: use exact closed-form coordinates.
    r_grid = np.linspace(r1 + eps, r2 - eps, p.n_grid)
    for t0 in np.linspace(-p.t_max, p.t_max, 13):
        x, y = compact("II", np.full_like(r_grid, t0), r_grid, p)
        ax.plot(x, y, color="#7a8188", lw=0.65, ls=(0, (7, 6)), alpha=0.55)

    t = np.linspace(-p.t_max, p.t_max, 1600)
    for r0 in np.r_[np.linspace(r1 + 0.24, -0.18, 4), [0.0], np.linspace(0.18, r2 - 0.24, 4)]:
        x, y = compact("II", t, np.full_like(t, r0), p)
        rider = abs(r0) < 1.0e-12
        ax.plot(x, y, color="#c14d3f" if rider else "#20252b", lw=2.6 if rider else 0.9, alpha=0.95)

    # Central horizon generators, approached from the bubble side.
    x1, y1 = compact("II", t, np.full_like(t, r1 + eps), p)
    x2, y2 = compact("II", t, np.full_like(t, r2 - eps), p)
    ax.plot(x1, y1, color="#0b7a63", lw=2.0, ls="--", alpha=0.90)
    ax.plot(x2, y2, color="#0b7a63", lw=2.0, ls="--", alpha=0.90)

    # Draw light local branch backgrounds at the endpoints.  These are not
    # global conformal diamonds; the attached branch is only represented in
    # its own local Kruskal coordinates translated to C-/C+.
    scale = 0.95
    ax.text(
        c_minus[0] - 0.86,
        c_minus[1] - 0.62,
        "left exterior\nPG/acoustic\nlocal chart",
        ha="center",
        va="center",
        fontsize=9,
        alpha=0.9,
        bbox={"facecolor": "#f5f1e8", "edgecolor": "#d8d0c2", "alpha": 0.78, "pad": 4},
    )
    ax.text(
        c_plus[0] + 0.88,
        c_plus[1] + 0.62,
        "right exterior\nPG/acoustic\nlocal chart",
        ha="center",
        va="center",
        fontsize=9,
        alpha=0.9,
        bbox={"facecolor": "#f5f1e8", "edgecolor": "#d8d0c2", "alpha": 0.78, "pad": 4},
    )

    # Attached Region-I branch at C-; V<0 on U=0 points to the past/SW.
    def rear_coords(t0: np.ndarray, r0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region("I", t0, r0, p)
        w = w_coord(t0, r0, p)
        U = np.exp(-kap * u)
        V = -np.exp(kap * w)
        x, y = penrose(U, V)
        return c_minus[0] + scale * x, c_minus[1] + scale * y

    # Attached Region-III branch at C+; rotate the local chart by pi so the
    # continued r2 generator leaves the original endpoint to the future/NE.
    def front_coords(t0: np.ndarray, r0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region("III", t0, r0, p)
        w = w_coord(t0, r0, p)
        U = np.exp(kap * u)
        V = -np.exp(-kap * w)
        x, y = penrose(U, V)
        return c_plus[0] - scale * x, c_plus[1] - scale * y

    tv_rear = np.linspace(-16.0, 7.0, 900)
    for r0 in r1 - np.array([0.05, 0.11, 0.25, 0.55, 1.2, 2.7, 6.0, 13.0]):
        ax.plot(*rear_coords(tv_rear, np.full_like(tv_rear, r0)), color="#20252b", lw=0.8, alpha=0.68)
    tv_front = np.linspace(-7.0, 16.0, 900)
    for r0 in r2 + np.array([0.05, 0.11, 0.25, 0.55, 1.2, 2.7, 6.0, 13.0]):
        ax.plot(*front_coords(tv_front, np.full_like(tv_front, r0)), color="#20252b", lw=0.8, alpha=0.68)

    Vh = -np.geomspace(1.0, 0.018, 330)
    xh, yh = penrose(np.zeros_like(Vh), Vh)
    ax.plot(c_minus[0] + scale * xh, c_minus[1] + scale * yh, color="#c14d3f", lw=2.6)
    ax.plot(c_plus[0] - scale * xh, c_plus[1] - scale * yh, color="#c14d3f", lw=2.6)

    ax.scatter([c_minus[0], c_plus[0]], [c_minus[1], c_plus[1]], color="#20252b", s=42, zorder=6)
    ax.text(c_minus[0] - 0.08, c_minus[1] + 0.10, r"$C^-$", ha="right", va="bottom", fontsize=11)
    ax.text(c_plus[0] + 0.08, c_plus[1] - 0.10, r"$C^+$", ha="left", va="top", fontsize=11)
    ax.text(-0.03, 0.10, "central\nAlcubierre\npatch", ha="center", va="center", fontsize=10)
    ax.text(0.08, 0.42, "rider x=0", color="#c14d3f", fontsize=9, ha="left")

    ax.text(
        -2.18,
        1.55,
        "Calculated for v(x)=2(sech x-1)\n"
        "solid black: constant x coordinate curves\n"
        "gray dashed: constant t\n"
        "green dashed: central null horizons\n"
        "black dots: finite-affine endpoints",
        fontsize=9,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92, "pad": 3},
    )
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-1.65, 1.80)
    ax.axis("off")
    ax.set_title("Planar PG/acoustic endpoint extension", pad=12)
    fig.savefig(OUT / "pg_acoustic_three_diamond_chain.png", dpi=220)
    fig.savefig(OUT / "pg_acoustic_vertex_extension_chain.png", dpi=220)
    plt.close(fig)


def write_note() -> None:
    r1, r2 = horizons(Params())
    text = f"""Planar PG/acoustic three-diamond chain

Metric and profile
------------------
  ds^2 = -dt^2 + [dx - v(x) dt]^2
  v(x) = 2(sech x - 1)

The horizons are the simple roots of v+1=0:

  r1 = {r1:.12f}
  r2 = {r2:.12f}

Null coordinates
----------------
The null slopes are dx/dt=v+1 and dx/dt=v-1.  Therefore

  u = t - int dx/(v+1)
  w = t - int dx/(v-1)

are null coordinates and

  ds^2 = -(1-v^2) du dw.

Equivalently, after the Painleve-Gullstrand to static time shift

  dT = dt + v dx/(1-v^2),
  x_* = int dx/(1-v^2),
  u = T - x_*,
  w = T + x_*.

Block structure
---------------
For the sech profile, 1-v^2 is positive between r1 and r2 and negative
outside.  The three intervals

  I   : x < r1,
  II  : r1 < x < r2,
  III : x > r2

each have x_* range (-infinity,+infinity), so each interval compactifies to
a diamond.  Simple horizons are null edges of these diamonds.

The figure places the exterior PG/acoustic branches at the endpoint vertices
C- and C+.  This is a corner attachment, not an edge-to-edge gluing.  The
front r2 generator reaches C+ and its continuation leaves the vertex in the
same future null direction.  The rear r1 generator has the time-reversed
past continuation through C-.

The central curves and the exterior branch curves are computed from the exact
sech u,w coordinates.  The exterior branches are drawn in translated local
Kruskal charts, not inside a single global compactification frame.  Their
drawn size is therefore a chart convention; the endpoint attachment,
generator direction, and branch type are the invariant causal information
established by the local calculation.  The solid black curves are constant-x
coordinate curves, not timelike geodesics.

3+1 interpretation
------------------
If v=v(x), the full metric is the above 1+1 PG/acoustic diagram crossed with
R^2.  For a rounded finite bubble, this quotient diagram is only the 1+1
temptation; the full 3+1 rounded endpoint has the PP-curvature obstruction.
"""
    (OUT / "pg_acoustic_three_diamond_chain.txt").write_text(text, encoding="utf-8")


def main() -> None:
    plot()
    write_note()


if __name__ == "__main__":
    main()
