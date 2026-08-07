"""Derive and draw the quotient/overlay diagrams for the sech warp profile.

This script deliberately keeps the picture tied to the null-coordinate
construction.  It is not a hand sketch: curves are generated from the
closed-form 1+1 coordinates in sech_extension.py, and the 3+1 overlay only
adds the local product/obstruction information established by the curvature
calculation.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

from sech_extension import Params, compact, horizons, w_coord


matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
        "mathtext.fontset": "stixsans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


BASE_DIR = Path(__file__).resolve().parent
OUT = BASE_DIR / "output/sech"
PAPER_FIGURES = BASE_DIR.parent.parent / "figures"


def endpoint_coordinates() -> dict[str, tuple[float, float]]:
    """Return the two finite-affine endpoint locations in the compact chart."""
    b = 0.5 * np.pi
    a0 = float(np.arctan(0.5))

    # The regularized three-region chart uses
    #   X=(Wbar-Ubar)/2, T=(Wbar+Ubar)/2.
    #
    # Future front endpoint: r2 bubble-side generator has Ubar=-atan(1/2)
    # and reaches Wbar=+pi/2.
    c_plus = (0.5 * (b + a0), 0.5 * (b - a0))

    # Past rear endpoint: r1 bubble-side generator has Ubar=+atan(1/2)
    # and reaches Wbar=-pi/2.
    c_minus = (-0.5 * (b + a0), -0.5 * (b - a0))
    return {"C+": c_plus, "C-": c_minus}


def draw_base_patch(ax: plt.Axes, p: Params, *, light: bool = False) -> None:
    """Draw the exact 1+1 quotient patch from closed-form coordinates."""
    r1, r2 = horizons(p)
    eps = 1.0e-5 * (r2 - r1)
    grids = {
        "I": np.linspace(-p.r_max, r1 - eps, p.n_grid),
        "II": np.linspace(r1 + eps, r2 - eps, p.n_grid),
        "III": np.linspace(r2 + eps, p.r_max, p.n_grid),
    }

    const_t_color = "#9aa0a6" if light else "#6b6f73"
    const_r_color = "#52575c" if light else "#20252b"
    horizon_color = "#0b7a63"

    for t0 in np.linspace(-p.t_max, p.t_max, 11):
        for region, r in grids.items():
            x, y = compact(region, np.full_like(r, t0), r, p)
            ax.plot(x, y, color=const_t_color, lw=0.65, ls=(0, (7, 6)), alpha=0.45 if light else 0.68)

    r_samples = {
        "I": np.linspace(-p.r_max + 0.35, r1 - 0.28, 4),
        "II": np.r_[np.linspace(r1 + 0.28, -0.20, 3), [0.0], np.linspace(0.20, r2 - 0.28, 3)],
        "III": np.linspace(r2 + 0.28, p.r_max - 0.35, 4),
    }
    t = np.linspace(-p.t_max, p.t_max, 1300)
    for region, values in r_samples.items():
        for r0 in values:
            x, y = compact(region, t, np.full_like(t, r0), p)
            rider = region == "II" and abs(r0) < 1.0e-12
            ax.plot(
                x,
                y,
                color="#c14d3f" if rider else const_r_color,
                lw=2.5 if rider else 0.95,
                alpha=0.95 if rider else 0.6 if light else 0.9,
            )

    # Horizon generators are null: constant regularized U, hence 45-degree
    # diagonals in (X,T).  We still draw them from the exact chart.
    for region, r0 in [("I", r1 - eps), ("II", r1 + eps), ("II", r2 - eps), ("III", r2 + eps)]:
        x, y = compact(region, t, np.full_like(t, r0), p)
        ax.plot(x, y, color=horizon_color, lw=2.0, ls="--", alpha=0.88)

    b = 0.5 * np.pi
    a0 = float(np.arctan(0.5))

    def from_null(ubar: np.ndarray | float, wbar: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
        return 0.5 * (np.asarray(wbar) - np.asarray(ubar)), 0.5 * (np.asarray(wbar) + np.asarray(ubar))

    # Compactification frame.
    for ubar in (b, -b):
        s = np.linspace(-b, b, 300)
        ax.plot(*from_null(np.full_like(s, ubar), s), color="#777777", lw=1.0, alpha=0.7)
    for umin, umax in [(a0, b), (-a0, a0), (-b, -a0)]:
        s = np.linspace(umin, umax, 300)
        ax.plot(*from_null(s, np.full_like(s, b)), color="#777777", lw=1.0, alpha=0.7)
        ax.plot(*from_null(s, np.full_like(s, -b)), color="#777777", lw=1.0, alpha=0.7)

    ax.text(-0.62, 0.02, "I", ha="center", va="center", fontsize=9, color="#333333")
    ax.text(0.0, 0.02, "II", ha="center", va="center", fontsize=9, color="#333333")
    ax.text(0.62, 0.02, "III", ha="center", va="center", fontsize=9, color="#333333")

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.72, 1.72)
    ax.set_ylim(-1.72, 1.72)
    ax.set_xlabel(r"$X=(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"$T=(\mathcal{W}+\mathcal{U})/2$")
    ax.grid(True, alpha=0.14)


def draw_overlay() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p = Params()
    endpoints = endpoint_coordinates()

    fig, axs = plt.subplots(1, 2, figsize=(14.0, 7.0), constrained_layout=True)

    draw_base_patch(axs[0], p)
    axs[0].set_title("Exact 1+1 quotient diagram")
    axs[0].text(
        -1.62,
        1.54,
        "green dashed: null horizons\n"
        "red: center rider\n"
        "solid: constant r\n"
        "dashed gray: constant t",
        fontsize=8.5,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#dddddd", "alpha": 0.9, "pad": 3.0},
    )

    draw_base_patch(axs[1], p, light=True)
    axs[1].set_title("Same quotient with 3+1 local interpretation")

    for label, xy in endpoints.items():
        axs[1].scatter([xy[0]], [xy[1]], s=84, color="#b6202d", zorder=5)
        axs[1].text(xy[0] + 0.08, xy[1] + 0.06, label, color="#b6202d", fontsize=11, weight="bold")

    # Do not draw a finite continuation region here.  The calculation proves
    # a local extension germ in Kruskal coordinates for the product case; its
    # size in this compact diagram is chart- and normalization-dependent.
    for label, xy in endpoints.items():
        axs[1].scatter(
            [xy[0]],
            [xy[1]],
            s=260,
            facecolors="none",
            edgecolors="#2a9d68",
            linewidths=2.0,
            zorder=4,
        )

    axs[1].text(
        -1.62,
        1.54,
        "green ring: product extension germ for v=v(x)\n"
        "red dot: rounded/nonuniform endpoint obstruction\n"
        "where positive-boost-weight curvature diverges",
        fontsize=8.4,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#dddddd", "alpha": 0.9, "pad": 3.0},
    )
    axs[1].text(
        -1.60,
        -1.55,
        "The quotient diagram alone cannot decide the 3+1 question.\n"
        "A transversely uniform planar patch lifts as diagram x R^2;\n"
        "a rounded finite bubble does not lift through the marked endpoints.",
        fontsize=8.4,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#dddddd", "alpha": 0.9, "pad": 3.0},
    )

    fig.savefig(OUT / "quotient_product_obstruction_overlay.png", dpi=220)
    plt.close(fig)


def draw_clean_calculated_patch() -> None:
    """Draw the closed-form sech three-region patch without diagnostic clutter."""
    OUT.mkdir(parents=True, exist_ok=True)
    p = Params(n_grid=1800, t_max=7.0, r_max=7.5)
    r1, r2 = horizons(p)
    eps = 1.0e-5 * (r2 - r1)
    endpoints = endpoint_coordinates()

    fig, ax = plt.subplots(figsize=(7.2, 6.4), constrained_layout=True)

    b = 0.5 * np.pi
    a0 = float(np.arctan(0.5))

    def from_null(ubar: np.ndarray | float, wbar: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
        return 0.5 * (np.asarray(wbar) - np.asarray(ubar)), 0.5 * (np.asarray(wbar) + np.asarray(ubar))

    def exact_horizon_point(t0: float, root: float, ubar: float) -> tuple[float, float]:
        """Return the common chart limit of a constant-t slice at a horizon."""
        wbar = float(np.arctan(w_coord(np.array([t0]), np.array([root]), p)[0]))
        x, y = from_null(ubar, wbar)
        return float(x), float(y)

    boundary_color = "#20242a"
    const_xi_color = "#59636e"
    const_t_color = "#9aa1a9"
    horizon_color = "#0072b2"
    rider_color = "#d55e00"

    grids = {
        "I": np.linspace(-p.r_max, r1 - eps, p.n_grid),
        "II": np.linspace(r1 + eps, r2 - eps, p.n_grid),
        "III": np.linspace(r2 + eps, p.r_max, p.n_grid),
    }

    # Constant-t slices.  Append their exact horizon limits so the separately
    # evaluated regional pieces meet even where the fixed-epsilon approximation
    # is nonuniform at large |t|.
    for t0 in np.linspace(-p.t_max, p.t_max, 9):
        h1 = exact_horizon_point(float(t0), r1, +a0)
        h2 = exact_horizon_point(float(t0), r2, -a0)
        for region, r in grids.items():
            x, y = compact(region, np.full_like(r, t0), r, p)
            if region == "I":
                x = np.r_[x, h1[0]]
                y = np.r_[y, h1[1]]
            elif region == "II":
                x = np.r_[h1[0], x, h2[0]]
                y = np.r_[h1[1], y, h2[1]]
            else:
                x = np.r_[h2[0], x]
                y = np.r_[h2[1], y]
            ax.plot(x, y, color=const_t_color, lw=0.85, ls=(0, (7, 6)))

    # Constant-r curves.
    r_samples = {
        "I": np.linspace(-p.r_max + 0.45, r1 - 0.32, 3),
        "II": np.r_[np.linspace(r1 + 0.30, -0.25, 2), [0.0], np.linspace(0.25, r2 - 0.30, 2)],
        "III": np.linspace(r2 + 0.32, p.r_max - 0.45, 3),
    }
    t = np.linspace(-p.t_max, p.t_max, 1200)
    t_rider = np.linspace(-40.0, 40.0, 2000)
    for region, values in r_samples.items():
        for r0 in values:
            rider = region == "II" and abs(r0) < 1.0e-12
            curve_t = t_rider if rider else t
            x, y = compact(region, curve_t, np.full_like(curve_t, r0), p)
            ax.plot(
                x,
                y,
                color=rider_color if rider else const_xi_color,
                lw=2.8 if rider else 1.0,
            )

    # The two horizons are exact constant-Ubar null segments.  Drawing them
    # analytically avoids the noncommuting fixed-offset and |t|->infinity limits
    # that make near-horizon constant-xi curves peel toward unrelated boundaries.
    wbar = np.linspace(-b, b, 500)
    horizon_curves = {
        "xi1": from_null(np.full_like(wbar, +a0), wbar),
        "xi2": from_null(np.full_like(wbar, -a0), wbar),
    }
    x_h1, y_h1 = horizon_curves["xi1"]
    x_h2, y_h2 = horizon_curves["xi2"]
    assert np.allclose(np.diff(y_h1), np.diff(x_h1))
    assert np.allclose(np.diff(y_h2), np.diff(x_h2))
    assert np.allclose((x_h1[0], y_h1[0]), endpoints["C-"])
    assert np.allclose((x_h2[-1], y_h2[-1]), endpoints["C+"])
    for x_horizon, y_horizon in horizon_curves.values():
        ax.plot(
            x_horizon,
            y_horizon,
            color=horizon_color,
            lw=2.4,
            ls=(0, (4, 2)),
            zorder=4,
        )

    # Compactification frame used by the regularized closed-form coordinates.
    for ubar in (b, -b):
        s = np.linspace(-b, b, 300)
        ax.plot(*from_null(np.full_like(s, ubar), s), color=boundary_color, lw=1.4)
    for umin, umax in [(a0, b), (-a0, a0), (-b, -a0)]:
        s = np.linspace(umin, umax, 300)
        ax.plot(*from_null(s, np.full_like(s, b)), color=boundary_color, lw=1.4)
        ax.plot(*from_null(s, np.full_like(s, -b)), color=boundary_color, lw=1.4)

    # Standard compactification labels for the outer diamond.
    ax.text(0.0, b - 0.08, r"$i^+$", ha="center", va="top", fontsize=12)
    ax.text(0.0, -b + 0.08, r"$i^-$", ha="center", va="bottom", fontsize=12)
    ax.text(-b + 0.08, 0.0, r"$i^0_L$", ha="left", va="center", fontsize=11.5)
    ax.text(b - 0.08, 0.0, r"$i^0_R$", ha="right", va="center", fontsize=11.5)

    # The two finite-affine endpoints in this compact chart.
    for label, xy in endpoints.items():
        ax.scatter([xy[0]], [xy[1]], s=92, color="#111111", zorder=6)
        if label == "C+":
            ax.annotate(
                "future finite-affine\n" + r"$\xi_2$ endpoint",
                xy=xy,
                xytext=(xy[0] + 0.28, xy[1] + 0.16),
                ha="left",
                va="bottom",
                fontsize=11.5,
                arrowprops=dict(arrowstyle="->", lw=1.0, color="0.15"),
            )
        else:
            ax.annotate(
                "past finite-affine\n" + r"$\xi_1$ endpoint",
                xy=xy,
                xytext=(xy[0] - 0.34, xy[1] - 0.18),
                ha="right",
                va="top",
                fontsize=11.5,
                arrowprops=dict(arrowstyle="->", lw=1.0, color="0.15"),
            )

    ax.text(-0.64, 0.02, "I", ha="center", va="center", fontsize=14.5)
    ax.text(0.0, 0.03, "II", ha="center", va="center", fontsize=14.5)
    ax.text(0.64, 0.02, "III", ha="center", va="center", fontsize=14.5)

    x1, y1 = from_null(+a0, -0.78)
    x2, y2 = from_null(-a0, +0.78)
    horizon_label = dict(
        color=horizon_color,
        fontsize=11.5,
        rotation=45,
        ha="center",
        va="bottom",
        rotation_mode="anchor",
        bbox=dict(facecolor="white", edgecolor="none", pad=0.6),
    )
    ax.text(float(x1), float(y1), r"$\xi=\xi_1$", **horizon_label)
    ax.text(float(x2), float(y2), r"$\xi=\xi_2$", **horizon_label)

    legend_items = [
        Line2D([0], [0], color=const_xi_color, lw=1.2, label=r"constant-$\xi$ lines"),
        Line2D([0], [0], color=const_t_color, lw=1.0, ls=(0, (7, 6)), label=r"constant-$t$ lines"),
        Line2D([0], [0], color=horizon_color, lw=2.4, ls=(0, (4, 2)), label=r"horizons $\xi=\xi_1,\xi_2$"),
        Line2D([0], [0], color=rider_color, lw=2.8, label=r"center rider $\xi=0$"),
    ]
    ax.legend(
        handles=legend_items,
        loc="upper left",
        frameon=True,
        framealpha=1.0,
        facecolor="white",
        edgecolor="#d8d8d8",
        fontsize=11.0,
    )

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.66, 1.66)
    ax.set_ylim(-1.66, 1.66)
    ax.set_xlabel(r"$X=(\bar{\mathcal{W}}-\bar{\mathcal{U}})/2$", fontsize=12)
    ax.set_ylabel(r"$T=(\bar{\mathcal{W}}+\bar{\mathcal{U}})/2$", fontsize=12)
    ax.tick_params(labelsize=11)
    ax.grid(False)

    for ext in ("png", "pdf", "eps"):
        fig.savefig(OUT / f"calculated_three_region_endpoint_patch.{ext}", dpi=240, bbox_inches="tight")
        PAPER_FIGURES.mkdir(parents=True, exist_ok=True)
        fig.savefig(PAPER_FIGURES / f"calculated_three_region_endpoint_patch.{ext}", dpi=240, bbox_inches="tight")
    plt.close(fig)


def write_derivation_note() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    text = """Diagram derivation: quotient versus 3+1 overlay

1+1 quotient metric
-------------------
Start with

  ds^2 = -dt^2 + [dx - v(x) dt]^2
       = -(1-v^2) dt^2 - 2 v dt dx + dx^2.

The two radial null families obey

  dx/dt = v+1,        dx/dt = v-1.

Therefore define null coordinates

  u = t - int dx/(v+1),
  w = t - int dx/(v-1).

Then u is constant on the first null family and w is constant on the
second.  Solving for dt and dx gives

  dt = [(1+v)/2] du + [(1-v)/2] dw,
  dx = [(1-v^2)/2] (dw-du),

and hence

  ds^2 = -(1-v^2) du dw.

The conformal diagram is obtained by replacing u,w by regularized horizon
coordinates and compactifying them.  The horizons are null because they are
constant-u or constant-regularized-U lines.

Front endpoint
--------------
At the front root x=x2, take v=-1 and v_x=-kappa<0.  With s=x-x2,

  v = -1 - kappa s + O(s^2),
  1-v^2 = -2 kappa s + O(s^2),
  u = t + (1/kappa) log|s| + O(1),
  w = t + O(1).

A local endpoint chart is

  U = +exp(kappa u) in region II,
  U = -exp(kappa u) in region III,
  V = exp(-kappa w).

Then

  ds^2 = [(1-v^2)/(kappa^2 U V)] dU dV,

and the bracket has a finite nonzero limit because U V is proportional to
-s.  The front generator is
U=0; its future finite-affine endpoint is U=V=0.

3+1 product lift
----------------
If the full metric is transversely uniform on an open patch,

  ds^2 = ds^2_1+1 + dy^2 + dz^2,

then the 1+1 extension lifts directly as a product.  The conformal diagram
is the quotient diagram; each point represents an R^2 transverse plane, or
a transverse disk if only a finite local planar window is assumed.

Rounded/nonuniform obstruction
------------------------------
At a stationary front generator in the full metric

  ds^2 = -dt^2 + [dx - v(x,y,z)dt]^2 + dy^2 + dz^2,

the affine tangent is K=q partial_t with

  q = 1/[kappa(lambda_* - lambda)].

The positive-boost-weight components are

  R_KNK A = -v_xA q,
  R_KA K B = v_AB q^2,       A,B in {y,z}.

Thus a rounded front wall, or transverse variation of the wall data,
generically produces a parallel-propagated curvature blow-up at the same
endpoint where the 1+1 quotient permits a formal extension.  This is why
the overlay marks the product extension as allowed only for v=v(x), and
marks the rounded finite-bubble endpoint as obstructed.
"""
    (OUT / "quotient_product_obstruction_overlay.txt").write_text(text, encoding="utf-8")


def main() -> None:
    draw_overlay()
    draw_clean_calculated_patch()
    write_derivation_note()


if __name__ == "__main__":
    main()
