"""Generate schematic figures for the front-tip PP singularity note.

The figures are deliberately schematic.  They identify where the local
calculation lives and what geometric data enter the leading coefficient.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)


def save(fig, stem: str) -> None:
    for ext in ("png", "pdf"):
        fig.savefig(FIG / f"{stem}.{ext}", bbox_inches="tight", dpi=220)
    plt.close(fig)


def axial_endpoint_schematic() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.set_aspect("equal")
    ax.axis("off")

    # Conformal diamond skeleton.
    diamond = np.array([[0.0, -1.0], [1.15, 0.0], [0.0, 1.0], [-1.15, 0.0], [0.0, -1.0]])
    ax.plot(diamond[:, 0], diamond[:, 1], color="0.45", lw=1.8)

    # Center rider.
    s = np.linspace(-0.82, 0.82, 300)
    x_center = 0.12 * np.sin(np.pi * s)
    ax.plot(x_center, s, color="#c94f43", lw=3.0, label="center rider")

    # Axial horizons / Cauchy endpoints.
    ax.plot([-0.78, 0.52], [-0.70, 0.72], color="#0b7a75", lw=2.7, ls="--")
    ax.plot([-0.52, 0.78], [-0.72, 0.70], color="#0b7a75", lw=2.7, ls="--")
    ax.scatter([0.52], [0.72], s=62, color="#111111", zorder=5)
    ax.scatter([-0.52], [-0.72], s=62, color="#111111", zorder=5)

    # Highlight the endpoint used in the proof.
    ax.annotate(
        "future front axial endpoint\nfinite affine distance\nPP curvature blow-up",
        xy=(0.52, 0.72),
        xytext=(0.03, 1.18),
        ha="center",
        va="bottom",
        fontsize=10,
        arrowprops=dict(arrowstyle="->", lw=1.2, color="0.2"),
    )
    ax.annotate(
        "time-reversed\nrear endpoint",
        xy=(-0.52, -0.72),
        xytext=(-1.18, -1.08),
        ha="left",
        va="top",
        fontsize=9.5,
        arrowprops=dict(arrowstyle="->", lw=1.0, color="0.3"),
    )

    # Null infinity labels, deliberately generic schematic.
    ax.text(0, 1.06, r"$i^+$", ha="center", va="bottom", fontsize=12)
    ax.text(0, -1.08, r"$i^-$", ha="center", va="top", fontsize=12)
    ax.text(-1.22, 0, r"$i^0_L$", ha="right", va="center", fontsize=11)
    ax.text(1.22, 0, r"$i^0_R$", ha="left", va="center", fontsize=11)
    ax.text(-0.58, 0.58, r"$\mathscr{I}^+$", ha="right", va="bottom", fontsize=11, color="0.3")
    ax.text(0.58, -0.58, r"$\mathscr{I}^-$", ha="left", va="top", fontsize=11, color="0.3")

    ax.text(0.23, -0.05, r"$r=0$", color="#c94f43", fontsize=11)
    ax.text(-0.86, -0.45, r"$H^-$", color="#0b7a75", fontsize=12)
    ax.text(0.78, 0.42, r"$H^+$", color="#0b7a75", fontsize=12)

    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.25, 1.35)
    save(fig, "axial_endpoint_schematic")


def reduced_three_region_endpoint_schematic() -> None:
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    ax.set_aspect("equal")
    ax.axis("off")

    # Outer compactified stationary patch.
    diamond = np.array(
        [[0.0, -1.35], [1.35, 0.0], [0.0, 1.35], [-1.35, 0.0], [0.0, -1.35]]
    )
    ax.plot(diamond[:, 0], diamond[:, 1], color="0.35", lw=1.7)

    # Two horizon segments divide the reduced patch into the three standard regions.
    bottom_endpoint = np.array([-0.48, -0.92])
    top_endpoint = np.array([0.48, 0.92])
    left_boundary = np.array([-0.92, -0.48])
    right_boundary = np.array([0.92, 0.48])

    horizon_color = "#087c6f"
    ax.plot(
        [left_boundary[0], top_endpoint[0]],
        [left_boundary[1], top_endpoint[1]],
        color=horizon_color,
        lw=2.8,
        ls="--",
    )
    ax.plot(
        [bottom_endpoint[0], right_boundary[0]],
        [bottom_endpoint[1], right_boundary[1]],
        color=horizon_color,
        lw=2.8,
        ls="--",
    )

    # Center-rider worldline inside the bubble region.
    s = np.linspace(0.0, 1.0, 220)
    x = bottom_endpoint[0] * (1 - s) + top_endpoint[0] * s + 0.07 * np.sin(np.pi * s)
    y = bottom_endpoint[1] * (1 - s) + top_endpoint[1] * s - 0.05 * np.sin(2 * np.pi * s)
    ax.plot(x, y, color="#c34a3d", lw=3.0)

    # Finite-affine generator endpoints.
    ax.scatter(
        [bottom_endpoint[0], top_endpoint[0]],
        [bottom_endpoint[1], top_endpoint[1]],
        s=92,
        color="#111111",
        zorder=5,
    )

    # Minimal labels.
    ax.text(-0.73, 0.02, "I", ha="center", va="center", fontsize=16)
    ax.text(0.0, 0.02, "II", ha="center", va="center", fontsize=16)
    ax.text(0.73, 0.02, "III", ha="center", va="center", fontsize=16)

    ax.text(-0.87, -0.64, r"$H_-$", color=horizon_color, fontsize=13, ha="right")
    ax.text(0.88, 0.62, r"$H_+$", color=horizon_color, fontsize=13, ha="left")
    ax.text(0.18, 0.52, r"$r=0$", color="#c34a3d", fontsize=12, rotation=61)

    ax.annotate(
        "finite-affine\nendpoint",
        xy=top_endpoint,
        xytext=(0.92, 1.10),
        ha="left",
        va="center",
        fontsize=10,
        arrowprops=dict(arrowstyle="->", lw=1.0, color="0.2"),
    )
    ax.annotate(
        "time-reversed\nendpoint",
        xy=bottom_endpoint,
        xytext=(-1.15, -1.12),
        ha="right",
        va="center",
        fontsize=10,
        arrowprops=dict(arrowstyle="->", lw=1.0, color="0.2"),
    )

    ax.text(0, 1.43, r"$i^+$", ha="center", va="bottom", fontsize=12)
    ax.text(0, -1.43, r"$i^-$", ha="center", va="top", fontsize=12)
    ax.text(-1.43, 0, r"$i^0_L$", ha="right", va="center", fontsize=11)
    ax.text(1.43, 0, r"$i^0_R$", ha="left", va="center", fontsize=11)

    ax.set_xlim(-1.58, 1.58)
    ax.set_ylim(-1.55, 1.58)
    save(fig, "reduced_three_region_endpoint_schematic")


def front_tip_geometry() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.set_aspect("equal")
    ax.axis("off")

    y = np.linspace(-1.1, 1.1, 300)
    R = 1.0
    C = 0.75
    x = R - 0.5 * C * y**2

    # Front cap cross-section and exterior/interior labels.
    ax.plot(x, y, color="#222222", lw=2.7)
    ax.fill_betweenx(y, x, 1.25, color="#e8f1f2", alpha=0.9)
    ax.fill_betweenx(y, -0.20, x, color="#f7f2e8", alpha=0.75)
    ax.text(1.18, 0.88, "exterior", ha="right", va="center", fontsize=11, color="0.25")
    ax.text(0.15, -0.94, "bubble side", ha="left", va="center", fontsize=11, color="0.25")
    ax.text(0.63, 1.13, r"$v=-1$", ha="center", fontsize=12)

    # Axial tip and directions.
    tip = (R, 0.0)
    ax.scatter([tip[0]], [tip[1]], s=70, color="#111111", zorder=5)
    ax.annotate(r"$K=q\,\partial_t$", xy=tip, xytext=(1.0, 0.78), ha="center", fontsize=12,
                arrowprops=dict(arrowstyle="->", lw=1.3, color="#c94f43"), color="#c94f43")
    ax.annotate(r"$Y$", xy=(R, 0.0), xytext=(R, 0.52), ha="center", va="bottom", fontsize=12,
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#2b6cb0"), color="#2b6cb0")
    ax.annotate(r"$Z$", xy=(R, 0.0), xytext=(1.28, -0.20), ha="left", va="center", fontsize=12,
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#2b6cb0"), color="#2b6cb0")

    # Curvature data annotation.
    ax.annotate(
        r"$X_{YY}=-C_1,\quad X_{ZZ}=-C_2$" "\n"
        r"$R_{KYKY}=-\frac{C_1}{\kappa(\lambda_*-\lambda)^2}$",
        xy=(0.83, 0.52),
        xytext=(-0.12, 0.55),
        ha="left",
        va="center",
        fontsize=11,
        arrowprops=dict(arrowstyle="->", lw=1.0, color="0.25"),
    )

    # x-axis and tip label.
    ax.annotate("", xy=(1.32, 0), xytext=(-0.18, 0), arrowprops=dict(arrowstyle="->", lw=1.0, color="0.45"))
    ax.text(1.34, 0, r"$x$", va="center", ha="left", fontsize=11, color="0.35")
    ax.text(1.02, -0.08, r"$p_+$", fontsize=12, ha="left", va="top")

    ax.set_xlim(-0.2, 1.38)
    ax.set_ylim(-1.22, 1.28)
    save(fig, "front_tip_geometry")


if __name__ == "__main__":
    axial_endpoint_schematic()
    reduced_three_region_endpoint_schematic()
    front_tip_geometry()
    print(f"Wrote figures to {FIG}")
