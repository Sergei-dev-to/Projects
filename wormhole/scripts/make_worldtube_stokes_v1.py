import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse


def main():
    fig, ax = plt.subplots(figsize=(5.8, 3.1))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.set_aspect("equal")
    ax.axis("off")

    blue = "#245b8f"
    green = "#3f7f4f"
    gray = "#666666"
    black = "#222222"

    # A single spatial slice. The throat is a schematic handle connecting mouths.
    x_a, y_a = 3.0, 3.0
    x_b, y_b = 7.0, 3.0
    theta = np.linspace(0, 2 * np.pi, 300)

    upper_x = np.linspace(x_a, x_b, 160)
    upper_y = 3.42 + 0.32 * np.sin(np.linspace(0, np.pi, 160))
    lower_x = np.linspace(x_a, x_b, 160)
    lower_y = 2.58 - 0.32 * np.sin(np.linspace(0, np.pi, 160))
    ax.plot(upper_x, upper_y, color="#9a9a9a", lw=2.0, zorder=1)
    ax.plot(lower_x, lower_y, color="#9a9a9a", lw=2.0, zorder=1)

    for x, y, label in [(x_a, y_a, "mouth A"), (x_b, y_b, "mouth B")]:
        ax.add_patch(Circle((x, y), 0.38, fill=False, edgecolor=black, lw=1.6, zorder=3))
        ax.add_patch(Circle((x, y), 0.12, color=black, zorder=4))
        ax.text(x, 1.35, label, ha="center", va="center", fontsize=11)

    # Measuring surface around mouth A. Drawn as a loop on the suppressed 2D slice.
    ax.add_patch(Ellipse((x_a, y_a), 2.05, 1.55, fill=False, edgecolor=blue, lw=2.4, zorder=5))
    ax.text(x_a - 1.18, y_a + 1.05, r"$S_t$", color=blue, fontsize=15, ha="center")

    ax.text(x_a + 1.25, y_a + 1.15, r"history: $\mathcal{T}=\cup_t S_t$", color=gray, fontsize=11, ha="left")
    ax.text(x_a - 1.8, y_a - 1.1, r"$\Delta\!\int_{S_t}\star F=0$", color=blue, fontsize=14, ha="left")

    # Source motion near mouth B stays outside the measured surface.
    path_y = np.linspace(2.1, 4.35, 180)
    path_x = x_b + 1.0 + 0.18 * np.sin(2.5 * (path_y - 2.1))
    ax.plot(path_x, path_y, color=green, lw=2.2)
    ax.add_patch(Circle((path_x[40], path_y[40]), 0.11, color=green, zorder=5))
    ax.add_patch(Circle((path_x[135], path_y[135]), 0.11, color=green, zorder=5))
    ax.text(8.35, 4.3, "source motion\nnear B", ha="center", va="center", fontsize=11, color=green)
    ax.text(6.95, 4.85, r"no current through $\mathcal{T}$", ha="center", fontsize=11, color=green)

    fig.tight_layout(pad=0.1)
    fig.savefig("fig_worldtube_stokes.pdf", bbox_inches="tight")
    fig.savefig("fig_worldtube_stokes.png", dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
