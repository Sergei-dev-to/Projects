"""Kruskal-chart continuity check at the rim of a planar cap.

A locally planar cap with v=v(s), s=x-x_H, admits the usual local extension
with U=exp(-kappa t) and s=UV.  If a finite cap ends by bending the front
surface to x=F(Y)+s, the same chart has a mixed metric component

    g_{UY} = -F_Y/(kappa U) + O(U).

This script records the consequence: even if F_Y vanishes to all orders at the
rim point, the product Kruskal extension is not continuous in any neighborhood
containing non-product points with F_Y != 0 arbitrarily close to the rim.
"""

from __future__ import annotations

from pathlib import Path


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = [
        "Rim Kruskal continuity check",
        "",
        "Planar near-horizon model:",
        "  s = x - x_H",
        "  v = -1 - kappa s + O(s^2)",
        "  U = exp(-kappa t),  s = U V",
        "",
        "Bent/transitioning front:",
        "  x = F(Y) + s",
        "  dx = V dU + U dV + F_Y dY",
        "  dt = -dU/(kappa U)",
        "",
        "Substituting in ds^2=-dt^2+(dx-vdt)^2+dY^2+... gives",
        "  g_UY = -F_Y/(kappa U) + O(U).",
        "",
        "If the planar cap ends smoothly, F_Y may vanish to all orders at the",
        "rim point Y=0.  But if the cap is finite and the product structure",
        "really ends, there are points Y_n -> 0 with F_Y(Y_n) != 0.",
        "",
        "Then along paths U_n = F_Y(Y_n)^2,",
        "  |g_UY| ~ 1/(kappa |F_Y(Y_n)|) -> infinity.",
        "Along paths U_n = F_Y(Y_n),",
        "  g_UY -> -1/kappa.",
        "Along paths with Y=0 inside the flat jet,",
        "  g_UY -> 0.",
        "",
        "Conclusion:",
        "  The product Kruskal extension is not even C0 at the rim as a",
        "  neighborhood extension unless F_Y vanishes on an open neighborhood,",
        "  i.e. unless the product structure persists beyond the rim.",
    ]
    text = "\n".join(lines) + "\n"
    (OUT / "rim_kruskal_continuity_check.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
