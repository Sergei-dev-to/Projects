"""Causal geodesic check at a transverse-gradient rim point.

For the stationary Alcubierre form

    ds^2 = -dt^2 + (dx - v(x,y,z) dt)^2 + dy^2 + dz^2,

this records the Hamiltonian argument used in the paper: a simple point with
v=-1, v_x != 0, and some transverse v_A != 0 cannot be approached by a causal
geodesic with t -> +infinity at finite affine/proper parameter.
"""

from __future__ import annotations

from pathlib import Path


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = [
        "Causal rim geodesic check",
        "",
        "Metric:",
        "  ds^2 = -dt^2 + (dx - v dt)^2 + dy^2 + dz^2",
        "",
        "Inverse metric in (t,x,A):",
        "  g^{tt}=-1, g^{tx}=-v, g^{xx}=1-v^2, g^{AB}=delta^{AB}",
        "",
        "Use E=-p_t, P=p_x, Q_A=p_A, epsilon=0 null / 1 timelike.",
        "Hamiltonian constraint H=-epsilon/2 gives:",
        "  dot t = E - v P",
        "  dot t^2 = P^2 + Q_A Q_A + epsilon",
        "",
        "Hamilton equations for spatial covectors:",
        "  dot P   = -v_x P dot t",
        "  dot Q_A = -v_A P dot t",
        "so wherever P dot t != 0:",
        "  dQ_A/dP = v_A/v_x",
        "",
        "Suppose a causal geodesic approaches a simple rim point p with",
        "  v(p)=-1, v_x(p)!=0, and some v_A(p)!=0,",
        "while t -> +infinity at finite affine/proper parameter.",
        "Then dot t is unbounded, so P^2 + Q_A Q_A -> infinity.",
        "",
        "If P stayed bounded, the Q_A equations would have locally bounded",
        "coefficients and at most linear growth in |Q|:",
        "  |dot Q_A| <= C |dot t| <= C'(1+|Q|).",
        "On a finite parameter interval this prevents finite-parameter blow-up",
        "by Gronwall's inequality.  Thus P must diverge.",
        "",
        "But the momentum ratio gives, for any transverse direction with v_A(p)!=0,",
        "  Q_A = c_A P + o(P),  c_A = v_A(p)/v_x(p) != 0.",
        "Then dot t ~ |P| sqrt(1+sum_A c_A^2), and",
        "  dot P = -v_x P dot t",
        "implies |P| ~ 1/(lambda_* - lambda).  Hence",
        "  dot y^A = Q_A ~ c_A/(lambda_* - lambda),",
        "so at least one transverse coordinate diverges logarithmically.",
        "This contradicts approach to the finite spatial point p.",
        "",
        "Equivalently, a point with transverse gradient v_A != 0 is not a",
        "stationary null generator of the v^2=1 surface.  It cannot serve as",
        "the finite-parameter endpoint of the reduced axial diagram.",
        "",
        "Conclusion:",
        "  A transverse-gradient rim point does not provide the finite-parameter",
        "  causal endpoint present in the 1+1 axial reduction.",
    ]
    text = "\n".join(lines) + "\n"
    (OUT / "rim_causal_geodesic_check.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
