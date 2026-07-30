"""Degenerate axial root check for the Alcubierre metric.

This records the local calculation for a higher-order root

    v + 1 = -a s^m + ...

at an axial point with v_y=0.  The exact stationary generator has zero
non-affinity when m>1 and is not a finite-affine endpoint.  However, causal
geodesics crossing the root still reach s=0 at finite affine/proper parameter,
and transverse Hessian data produce a stronger PP tidal blow-up.
"""

from __future__ import annotations

from pathlib import Path


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = [
        "Degenerate root causal tidal check",
        "",
        "Local model on the axis:",
        "  s = x - x_H",
        "  v(s,y) = -1 - a s^m + (1/2) H y^2 + ...",
        "  m >= 2, a != 0, H = v_yy(p)",
        "",
        "Regularity note:",
        "  If v=-1 is a regular smooth front surface and the stationary",
        "  axial curve is geodesic, then v_A=0 and grad(v) != 0 force",
        "  v_x != 0.  Thus a degenerate axial root is outside the regular",
        "  smooth-front theorem.",
        "",
        "Coordinate Riemann components at v_y=0:",
        "  R_tyty = -v H",
        "  R_t y x y = H/2",
        "  R_xyxy = 0",
        "",
        "Causal geodesics with conserved E=-p_t and P=p_x satisfy",
        "  dot t = E - v P",
        "  dot t^2 = P^2 + Q_A Q_A + epsilon",
        "For the branch with t -> +infinity at v -> -1,",
        "  P/dot t -> 1",
        "  dot s -> E",
        "  dot t ~ E/(1+v) ~ -E/(a s^m)",
        "so s is linear in the finite affine/proper parameter.",
        "",
        "For a transverse vector Y=partial_y at the axial point,",
        "  R(dot gamma,Y,dot gamma,Y)",
        "       = R_tyty dot t^2 + 2 R_t y x y dot t dot x",
        "       = H dot t P",
        "       ~ H dot t^2",
        "       ~ H E^2/[a^2 s^(2m)].",
        "",
        "Conclusion:",
        "  The exact degenerate stationary generator is not incomplete at",
        "  finite affine parameter, but crossing causal geodesics encounter",
        "  a transverse tidal blow-up if H != 0.",
    ]
    text = "\n".join(lines) + "\n"
    (OUT / "degenerate_root_causal_tidal_check.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
