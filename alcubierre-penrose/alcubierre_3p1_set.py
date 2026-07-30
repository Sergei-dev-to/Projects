"""Numerical 3+1 Einstein-tensor check for the Alcubierre metric.

This checks the real stationary 3+1 comoving metric

    ds^2 = -dt^2 + [dx - v(r) dt]^2 + dy^2 + dz^2
    r = sqrt(x^2+y^2+z^2)
    v(r) = alpha [sech(r/a)-1]

near the front/rear axis tips corresponding to the 1+1 horizons.
It deliberately avoids the 1+1 reduction and computes the 4D Einstein
tensor from the metric by finite-differencing Christoffels.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


OUT = Path("output/sech")
ALPHA = 2.0
A = 1.0
H = 2.0e-4


def sech(x: float) -> float:
    return 1.0 / np.cosh(x)


def vbar_xyz(x: float, y: float, z: float) -> float:
    r = np.sqrt(x * x + y * y + z * z)
    return ALPHA * (sech(r / A) - 1.0)


def metric(point: np.ndarray) -> np.ndarray:
    _, x, y, z = point
    v = vbar_xyz(x, y, z)
    g = np.zeros((4, 4), dtype=float)
    g[0, 0] = v * v - 1.0
    g[0, 1] = g[1, 0] = -v
    g[1, 1] = 1.0
    g[2, 2] = 1.0
    g[3, 3] = 1.0
    return g


def d_metric(point: np.ndarray, mu: int, h: float = H) -> np.ndarray:
    if mu == 0:
        return np.zeros((4, 4), dtype=float)
    step = np.zeros(4)
    step[mu] = h
    return (metric(point + step) - metric(point - step)) / (2.0 * h)


def christoffel(point: np.ndarray, h: float = H) -> np.ndarray:
    g = metric(point)
    gi = np.linalg.inv(g)
    dg = [d_metric(point, mu, h) for mu in range(4)]
    gam = np.zeros((4, 4, 4), dtype=float)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                s = 0.0
                for d in range(4):
                    s += gi[a, d] * (dg[b][d, c] + dg[c][d, b] - dg[d][b, c])
                gam[a, b, c] = 0.5 * s
    return gam


def d_christoffel(point: np.ndarray, mu: int, h: float = H) -> np.ndarray:
    if mu == 0:
        return np.zeros((4, 4, 4), dtype=float)
    step = np.zeros(4)
    step[mu] = h
    return (christoffel(point + step, h) - christoffel(point - step, h)) / (2.0 * h)


def einstein(point: np.ndarray, h: float = H) -> tuple[np.ndarray, float, np.ndarray]:
    g = metric(point)
    gi = np.linalg.inv(g)
    gam = christoffel(point, h)
    dgam = [d_christoffel(point, mu, h) for mu in range(4)]

    ric = np.zeros((4, 4), dtype=float)
    for a in range(4):
        for b in range(4):
            val = 0.0
            for c in range(4):
                val += dgam[c][c, a, b]
                val -= dgam[b][c, a, c]
                for d in range(4):
                    val += gam[c, a, b] * gam[d, c, d]
                    val -= gam[d, a, c] * gam[c, b, d]
            ric[a, b] = val

    scalar = float(np.einsum("ab,ab->", gi, ric))
    G = ric - 0.5 * g * scalar
    return G, scalar, ric


def raise2(tensor: np.ndarray, gi: np.ndarray) -> np.ndarray:
    return np.einsum("ac,bd,cd->ab", gi, gi, tensor)


def tensor_square(tensor: np.ndarray, gi: np.ndarray) -> float:
    up = raise2(tensor, gi)
    return float(np.einsum("ab,ab->", tensor, up))


def eulerian_normal(point: np.ndarray) -> np.ndarray:
    # ADM lapse is 1 and beta^x=-v, so n^mu=(1,-beta^i)=(1,v,0,0).
    _, x, y, z = point
    v = vbar_xyz(x, y, z)
    return np.array([1.0, v, 0.0, 0.0])


def format_matrix(mat: np.ndarray) -> list[str]:
    return ["  [" + ", ".join(f"{mat[i, j]: .8e}" for j in range(4)) + "]" for i in range(4)]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    r_h = float(np.arccosh(2.0))
    points = [
        ("front axis tip", np.array([0.0, r_h, 0.0, 0.0])),
        ("rear axis tip", np.array([0.0, -r_h, 0.0, 0.0])),
        ("front near off-axis y=1e-3", np.array([0.0, r_h, 1.0e-3, 0.0])),
        ("rear near off-axis y=1e-3", np.array([0.0, -r_h, 1.0e-3, 0.0])),
    ]

    lines = [
        "3+1 Alcubierre Einstein-tensor check",
        "",
        "Metric:",
        "  ds^2 = -dt^2 + [dx - v(r)dt]^2 + dy^2 + dz^2",
        "  r = sqrt(x^2+y^2+z^2)",
        "  v(r) = alpha[sech(r/a)-1]",
        f"  alpha={ALPHA}, a={A}",
        "",
        f"axis tip radius r_h=acosh(2)={r_h:.12f}",
        f"finite-difference step h={H:.1e}",
        "",
        "Einstein tensor G_ab component order: (t,x,y,z).",
        "T_ab = G_ab/(8*pi) if this metric is imposed as a 3+1 GR solution.",
    ]

    for label, point in points:
        G, R, _ = einstein(point)
        gi = np.linalg.inv(metric(point))
        n = eulerian_normal(point)
        rho_no_8pi = float(n @ G @ n)
        g2 = tensor_square(G, gi)
        lines.extend(
            [
                "",
                label,
                f"  point = {point.tolist()}",
                f"  Ricci scalar R = {R:.12e}",
                f"  G_ab G^ab = {g2:.12e}",
                f"  Eulerian energy density numerator G_ab n^a n^b = {rho_no_8pi:.12e}",
            ]
        )
        lines.extend(format_matrix(G))

    lines.extend(["", "Approach to the front and rear tips along the axis:"])
    for side, sign in [("front", 1.0), ("rear", -1.0)]:
        lines.append(f"  {side}")
        for eps in [1.0e-1, 1.0e-2, 1.0e-3, 1.0e-4]:
            point = np.array([0.0, sign * (r_h + eps), 0.0, 0.0])
            G, R, _ = einstein(point)
            gi = np.linalg.inv(metric(point))
            n = eulerian_normal(point)
            rho_no_8pi = float(n @ G @ n)
            g2 = tensor_square(G, gi)
            lines.append(
                f"    eps={eps:.0e}: R={R:.8e}, G2={g2:.8e}, Gnn={rho_no_8pi:.8e}"
            )

    lines.extend(
        [
            "",
            "Interpretation:",
            "  The true 3+1 Einstein tensor is finite at the front/rear axis tips",
            "  for this smooth sech profile. The samples near the tips approach",
            "  finite values rather than blowing up.",
            "",
            "Caution:",
            "  This verifies local 3+1 curvature/SET regularity at the original",
            "  axis tips. It does not by itself construct the full 3+1 extension",
            "  off axis, where the horizon structure differs from the 1+1 reduction.",
        ]
    )

    (OUT / "alcubierre_3p1_set_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:14]))


if __name__ == "__main__":
    main()
