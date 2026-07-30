"""2+1 conformal-background trip diagram for a warp-bubble comparison.

This is not the exact Penrose compactification of a full 2+1 Alcubierre metric.
It is a compactified 2+1 Minkowski background with a finite-radius warp-bubble
world tube overlaid, useful for comparing:

  * two static stars outside the bubble tube,
  * an ordinary subluminal traveler,
  * the bubble center/rider.

Minkowski compactification:
    u = t - rho
    v = t + rho
    U = arctan(u)
    V = arctan(v)
    T = U + V
    chi = V - U
    X = chi cos(phi)
    Y = chi sin(phi)

The conformal boundary is |T| + chi = pi.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection


@dataclass(frozen=True)
class Params:
    out_dir: Path = Path("output")
    star_distance: float = 8.0
    star_offset: float = 2.4
    bubble_speed: float = 2.0
    ordinary_speed: float = 0.75
    bubble_radius: float = 0.85
    t_margin: float = 2.0


def compactify(t: np.ndarray, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rho = np.hypot(x, y)
    phi = np.arctan2(y, x)
    U = np.arctan(t - rho)
    V = np.arctan(t + rho)
    T = U + V
    chi = V - U
    return chi * np.cos(phi), chi * np.sin(phi), T


def curve(t: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    X, Y, T = compactify(t, x, y)
    return np.column_stack([X, Y, T])


def add_line(ax, pts: np.ndarray, color: str, lw: float, label: str, ls: str = "-") -> None:
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=color, lw=lw, ls=ls, label=label)


def add_tube(ax, p: Params, t: np.ndarray, n_phi: int = 44) -> None:
    """Draw the compactified surface of the bubble world tube."""
    phis = np.linspace(0.0, 2.0 * np.pi, n_phi, endpoint=False)
    rings = []
    for ti in t:
        cx = p.bubble_speed * ti
        cy = 0.0
        x = cx + p.bubble_radius * np.cos(phis)
        y = cy + p.bubble_radius * np.sin(phis)
        X, Y, T = compactify(np.full_like(x, ti), x, y)
        rings.append(np.column_stack([X, Y, T]))

    faces = []
    for i in range(len(rings) - 1):
        for j in range(n_phi):
            faces.append([rings[i][j], rings[i][(j + 1) % n_phi], rings[i + 1][(j + 1) % n_phi], rings[i + 1][j]])

    tube = Poly3DCollection(faces, facecolor="#7d4fa3", edgecolor="none", alpha=0.16)
    ax.add_collection3d(tube)

    # A few circular cross sections keep the tube legible.
    cross_sections = np.linspace(0, len(rings) - 1, 7, dtype=int)
    segments = []
    for idx in cross_sections:
        ring = rings[idx]
        for j in range(n_phi):
            segments.append([ring[j], ring[(j + 1) % n_phi]])
    ax.add_collection3d(Line3DCollection(segments, colors="#7d4fa3", linewidths=0.6, alpha=0.45))


def add_boundary(ax, n_t: int = 22, n_phi: int = 96) -> None:
    """Draw the 2+1 Minkowski conformal boundary cones."""
    phi = np.linspace(0.0, 2.0 * np.pi, n_phi)

    for sign in [1.0, -1.0]:
        tvals = np.linspace(0.0, sign * np.pi, n_t)
        rings = []
        for T in tvals:
            chi = np.pi - abs(T)
            rings.append(np.column_stack([chi * np.cos(phi), chi * np.sin(phi), np.full_like(phi, T)]))

        for ring in rings[::3]:
            ax.plot(ring[:, 0], ring[:, 1], ring[:, 2], color="#b8bdc3", lw=0.45, alpha=0.38)

        for j in range(0, n_phi, 12):
            pts = np.array([ring[j] for ring in rings])
            ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="#b8bdc3", lw=0.55, alpha=0.35)

    equator = np.column_stack([np.pi * np.cos(phi), np.pi * np.sin(phi), np.zeros_like(phi)])
    ax.plot(equator[:, 0], equator[:, 1], equator[:, 2], color="#8d949b", lw=1.0, alpha=0.65)


def plot() -> None:
    p = Params()
    p.out_dir.mkdir(parents=True, exist_ok=True)

    L = p.star_distance
    y_star = p.star_offset

    t_depart = 0.0
    t_bubble_arrive = L / p.bubble_speed
    t_ordinary_arrive = np.hypot(L, 0.0) / p.ordinary_speed
    t_min = -p.t_margin
    t_max = t_ordinary_arrive + p.t_margin
    t = np.linspace(t_min, t_max, 900)

    fig = plt.figure(figsize=(10.5, 10.0), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    add_boundary(ax)

    # Static stars are off the bubble axis, so their worldlines stay outside the tube.
    star_a = curve(t, np.zeros_like(t), np.full_like(t, y_star))
    star_b = curve(t, np.full_like(t, L), np.full_like(t, y_star))
    add_line(ax, star_a, "#4b4f54", 2.2, "star A, static outside tube", ":")
    add_line(ax, star_b, "#1f2328", 2.2, "star B, static outside tube", ":")

    # Ordinary subluminal traveler from A to B at fixed y=y_star.
    t_ord = np.linspace(t_depart, t_ordinary_arrive, 500)
    x_ord = p.ordinary_speed * t_ord
    ordinary = curve(t_ord, x_ord, np.full_like(t_ord, y_star))
    add_line(ax, ordinary, "#1f6f8b", 2.8, f"ordinary rider, speed {p.ordinary_speed}")

    # Bubble rider and finite-radius tube on a separate path y=0.
    t_bub = np.linspace(t_min, t_max, 650)
    rider = curve(t_bub, p.bubble_speed * t_bub, np.zeros_like(t_bub))
    add_tube(ax, p, np.linspace(t_min, t_max, 110))
    add_line(ax, rider, "#c14d3f", 3.2, f"bubble rider, speed {p.bubble_speed}")

    # Connector events: nearest transfer from star A/B to the bubble path.
    events = [
        ("depart near A", t_depart, 0.0, 0.0, "#c14d3f"),
        ("bubble reaches B x-coordinate", t_bubble_arrive, L, 0.0, "#c14d3f"),
        ("ordinary reaches B", t_ordinary_arrive, L, y_star, "#1f6f8b"),
    ]
    for label, ti, xi, yi, color in events:
        pt = curve(np.array([ti]), np.array([xi]), np.array([yi]))[0]
        ax.scatter([pt[0]], [pt[1]], [pt[2]], color=color, s=42, depthshade=False)
        ax.text(pt[0], pt[1], pt[2] + 0.07, label, color=color, fontsize=8)

    # Show short spatial connectors at departure/arrival to make the off-axis geometry explicit.
    for ti, x0 in [(t_depart, 0.0), (t_bubble_arrive, L)]:
        yline = np.linspace(0.0, y_star, 80)
        connector = curve(np.full_like(yline, ti), np.full_like(yline, x0), yline)
        add_line(ax, connector, "#d99022", 1.4, "local transfer connector" if ti == t_depart else "", "--")

    ax.text(0, 0, np.pi + 0.08, r"$i^+$", fontsize=14, ha="center")
    ax.text(0, 0, -np.pi - 0.12, r"$i^-$", fontsize=14, ha="center")
    ax.text(np.pi + 0.08, 0, 0, r"$i^0$ circle", fontsize=10)
    ax.text(-1.85, -2.55, 2.25, r"$\mathscr{I}^+$ cone", color="#697078", fontsize=10)
    ax.text(1.65, 2.45, -2.35, r"$\mathscr{I}^-$ cone", color="#697078", fontsize=10)

    ax.set_title("2+1 conformal-background trip diagram with warp-bubble tube")
    ax.set_xlabel("compact X")
    ax.set_ylabel("compact Y")
    ax.set_zlabel("compact T")
    ax.set_box_aspect((1, 1, 1.05))
    lim = 3.35
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-3.35, 3.35)
    ax.view_init(elev=22, azim=-54)
    ax.legend(loc="upper left", fontsize=8)
    fig.savefig(p.out_dir / "conformal_2p1_trip.png", dpi=180)
    ax.view_init(elev=10, azim=-82)
    fig.savefig(p.out_dir / "conformal_2p1_trip_side.png", dpi=180)
    ax.view_init(elev=58, azim=-48)
    fig.savefig(p.out_dir / "conformal_2p1_trip_top.png", dpi=180)
    plt.close(fig)

    summary = (
        "2+1 conformal-background trip diagram\n"
        "This is compactified Minkowski with an overlaid finite-radius bubble tube, not the exact full warp compactification.\n"
        f"star separation L = {L}\n"
        f"star transverse offset y = {y_star}\n"
        f"bubble radius R = {p.bubble_radius}\n"
        f"bubble speed = {p.bubble_speed}, arrival x=L at t = {t_bubble_arrive:.6f}\n"
        f"ordinary speed = {p.ordinary_speed}, arrival at t = {t_ordinary_arrive:.6f}\n"
        "outputs:\n"
        "  conformal_2p1_trip.png\n"
        "  conformal_2p1_trip_side.png\n"
        "  conformal_2p1_trip_top.png\n"
    )
    (p.out_dir / "conformal_2p1_trip_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    plot()
