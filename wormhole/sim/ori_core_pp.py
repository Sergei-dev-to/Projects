"""
Ori (2007) pseudo-Schwarzschild core, Eq. (2):
   ds^2 = (1-2mu/r) dv^2 + 2 dv dr + r^2 (dth^2 + sinh^2(th) dph^2),   v ~ v + l

Cauchy horizon at r = 2mu.  Question: is the finite-affine endpoint of the
closed null generator a non-scalar (parallel-propagated) curvature singularity,
as in the Alcubierre case, or genuinely mild as Krasnikov/Ori assume?

Control: the same script run on Schwarzschild in Eddington form must give
R_KAKB = 0 on the horizon (PG-Schwarzschild control from the Alcubierre paper).
"""
import sympy as sp

def analyse(name, gmat, coords, horizon_sub, transverse_norms):
    v, r, th, ph = coords
    n = 4
    g = sp.Matrix(gmat)
    ginv = g.inv()
    print("=" * 70)
    print(name)
    print("=" * 70)
    print("signature check, eigenvalue signs of g at a sample point:")
    samp = {r: sp.Rational(5, 1), th: sp.Rational(1, 1)}
    gs = g.subs(horizon_sub.get('params', {})).subs(samp)
    print("   ", [sp.sign(e).simplify() for e in gs.eigenvals()])

    # Christoffels
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d] * (sp.diff(g[d, b], coords[c])
                                       + sp.diff(g[d, c], coords[b])
                                       - sp.diff(g[b, c], coords[d]))
                Gam[a][b][c] = sp.simplify(s / 2)

    # Riemann R^a_{bcd}
    Riem = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    expr = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
                    for e in range(n):
                        expr += Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c]
                    Riem[a][b][c][d] = sp.simplify(expr)

    # lower first index
    Rd = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rd[a][b][c][d] = sp.simplify(sum(g[a, e] * Riem[e][b][c][d] for e in range(n)))

    # --- is dr null on the horizon?  g^{rr} ---
    print("\ng^{rr} =", sp.simplify(ginv[1, 1]),
          "  -> on horizon:", sp.simplify(ginv[1, 1].subs(horizon_sub['sub'])))

    # --- is d_v null and geodesic on the horizon? ---
    xi = sp.Matrix([1, 0, 0, 0])          # d_v
    xi2 = sp.simplify((xi.T * g * xi)[0])
    print("g(d_v,d_v) =", xi2, " -> on horizon:", sp.simplify(xi2.subs(horizon_sub['sub'])))

    acc = []                               # (nabla_xi xi)^a
    for a in range(n):
        s = 0
        for b in range(n):
            for c in range(n):
                s += Gam[a][b][c] * xi[b] * xi[c]
        acc.append(sp.simplify(s.subs(horizon_sub['sub'])))
    print("(nabla_xi xi)^a on horizon =", acc)
    kappa = sp.simplify(acc[0])
    print("surface gravity kappa =", kappa)

    # --- parallel null frame on the horizon ---
    # K = q d_v ;  N = -(1/q) d_r ;  Y,Z unit transverse
    q = sp.symbols('q', positive=True)
    K = sp.Matrix([q, 0, 0, 0])
    N = sp.Matrix([0, -1 / q, 0, 0])
    Y = sp.Matrix([0, 0, transverse_norms[0], 0])
    Z = sp.Matrix([0, 0, 0, transverse_norms[1]])
    frame = {'K': K, 'N': N, 'Y': Y, 'Z': Z}

    print("\nframe normalisation on horizon:")
    for na, A in frame.items():
        for nb, B in frame.items():
            val = sp.simplify(((A.T * g * B)[0]).subs(horizon_sub['sub']))
            if val != 0:
                print(f"   g({na},{nb}) = {val}")

    def Rf(a, b, c, d):
        tot = 0
        A, B, C, D = frame[a], frame[b], frame[c], frame[d]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for m in range(n):
                        if A[i] == 0 or B[j] == 0 or C[k] == 0 or D[m] == 0:
                            continue
                        tot += Rd[i][j][k][m] * A[i] * B[j] * C[k] * D[m]
        return sp.simplify(sp.simplify(tot).subs(horizon_sub['sub']))

    print("\nRiemann components in the parallel frame ON THE HORIZON")
    print("(boost weight +2 are the ones that can diverge as q -> oo)\n")
    comps = [
        ('R_KYKY', ('K', 'Y', 'K', 'Y'), '+2'),
        ('R_KZKZ', ('K', 'Z', 'K', 'Z'), '+2'),
        ('R_KYKZ', ('K', 'Y', 'K', 'Z'), '+2'),
        ('R_KNKY', ('K', 'N', 'K', 'Y'), '+1'),
        ('R_KNKZ', ('K', 'N', 'K', 'Z'), '+1'),
        ('R_KYNY', ('K', 'Y', 'N', 'Y'), ' 0'),
        ('R_KNKN', ('K', 'N', 'K', 'N'), ' 0'),
        ('R_YZYZ', ('Y', 'Z', 'Y', 'Z'), ' 0'),
        ('R_NYNY', ('N', 'Y', 'N', 'Y'), '-2'),
        ('R_NZNZ', ('N', 'Z', 'N', 'Z'), '-2'),
    ]
    for label, idx, bw in comps:
        val = Rf(*idx)
        print(f"  bw {bw}   {label:9s} = {val}")

    # Kretschmann for reference
    K2 = 0
    Ru = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Ru[a][b][c][d] = sum(ginv[c, e] * ginv[d, f_] * Rd[a][b][e][f_]
                                         for e in range(n) for f_ in range(n))
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    K2 += Rd[a][b][c][d] * Ru[a][b][c][d]
    K2 = sp.simplify(K2)
    print("\nKretschmann =", K2, "  -> on horizon:", sp.simplify(K2.subs(horizon_sub['sub'])))


v, r, th, ph, mu = sp.symbols('v r theta phi mu', positive=True)

# ---------- Ori pseudo-Schwarzschild core, hyperbolic transverse space ----------
f_ori = 1 - 2 * mu / r
g_ori = [[f_ori, 1, 0, 0],
         [1, 0, 0, 0],
         [0, 0, r**2, 0],
         [0, 0, 0, r**2 * sp.sinh(th)**2]]
analyse("ORI 2007 pseudo-Schwarzschild core  (transverse = hyperbolic, sinh^2)",
        g_ori, (v, r, th, ph),
        {'sub': {r: 2 * mu}, 'params': {mu: 1}},
        (1 / r, 1 / (r * sp.sinh(th))))

# ---------- control: ordinary Schwarzschild, Eddington form ----------
g_sch = [[-(1 - 2 * mu / r), 1, 0, 0],
         [1, 0, 0, 0],
         [0, 0, r**2, 0],
         [0, 0, 0, r**2 * sp.sin(th)**2]]
analyse("CONTROL: Schwarzschild, ingoing Eddington  (transverse = sphere)",
        g_sch, (v, r, th, ph),
        {'sub': {r: 2 * mu}, 'params': {mu: 1}},
        (1 / r, 1 / (r * sp.sin(th))))
