"""Stage 1-2 dry run for the LR-positivity campaign.

Two independent exact evaluators of the Littlewood-Richardson coefficient:

  M1  lr_coeff_tableaux : combinatorial, counts LR skew tableaux (ballot).
  M2  lr_coeff_schur    : algebraic, Jacobi-Trudi h-determinant expansion of
                          the skew Schur function s_{nu/lam}, coefficient of s_mu.

They share no computational core, so agreement is a real cross-check.

Then: stretched polynomial P(N) = c^{N nu}_{N lam, N mu} by exact finite-
difference interpolation over the rationals (M1 as the workhorse), with a
degree-stability self-check, and a small-length frontier scan looking for the
minimum monomial coefficient (target: a negative one).
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product as iproduct
import sys

# ----------------------------------------------------------------------------
# partitions
# ----------------------------------------------------------------------------

def scale(p, N):
    # Strip zeros so scale(p, 0) is the empty partition, not (0,...,0).
    # Parts are positive, so x*N == 0 only when N == 0.
    return tuple(x * N for x in p if x * N)

def conj(p):
    """Conjugate (transpose) partition."""
    if not p:
        return ()
    m = p[0]
    return tuple(sum(1 for x in p if x >= c) for c in range(1, m + 1))

def contains(nu, lam):
    """lam subset of nu as Young diagrams."""
    if len(lam) > len(nu):
        return False
    return all(lam[i] <= nu[i] for i in range(len(lam)))

def partitions_upto(max_len, max_size):
    """All partitions with length <= max_len and size <= max_size (incl empty)."""
    out = []
    def rec(remaining, max_part, cur):
        out.append(tuple(cur))
        if len(cur) == max_len:
            return
        top = min(max_part, remaining)
        for part in range(top, 0, -1):
            cur.append(part)
            rec(remaining - part, part, cur)
            cur.pop()
    rec(max_size, max_size, [])
    # dedupe (empty added once); keep size<=max_size
    seen = set()
    res = []
    for p in out:
        if p not in seen and sum(p) <= max_size:
            seen.add(p)
            res.append(p)
    return res

# ----------------------------------------------------------------------------
# M1: LR coefficient by counting LR skew tableaux
# ----------------------------------------------------------------------------

def lr_coeff_tableaux(lam, mu, nu):
    """c^nu_{lam mu} = number of LR tableaux of shape nu/lam, content mu.

    Fill cells top-to-bottom, right-to-left in each row (reverse reading order).
    SSYT: weakly increasing along rows, strictly increasing down columns.
    Content mu; reverse reading word is a lattice (ballot) word.
    """
    if sum(lam) + sum(mu) != sum(nu):
        return 0
    if not contains(nu, lam):
        return 0
    nrows = len(nu)
    lam = tuple(lam) + (0,) * (nrows - len(lam))
    # cells per row: columns lam[r]+1 .. nu[r]   (1-indexed columns)
    rows = [list(range(lam[r] + 1, nu[r] + 1)) for r in range(nrows)]
    # build a flat cell list in fill order: row 0..nrows-1, within row right->left
    cells = []
    for r in range(nrows):
        for c in reversed(rows[r]):
            cells.append((r, c))
    ncells = len(cells)
    maxval = len(mu)
    mu = tuple(mu)

    # grid[(r,c)] = value; helpers for neighbours
    grid = {}
    cnt = [0] * (maxval + 2)      # cnt[v] = number of v placed so far
    remaining = list(mu)          # remaining copies allowed per value (1-indexed)

    result = 0

    def backtrack(idx):
        nonlocal result
        if idx == ncells:
            result += 1
            return
        r, c = cells[idx]
        right = grid.get((r, c + 1))          # already placed (same row, to right)
        above = grid.get((r - 1, c))          # already placed (row above)
        hi = right if right is not None else maxval
        lo = (above + 1) if above is not None else 1
        for v in range(lo, hi + 1):
            if v > maxval:
                break
            if remaining[v - 1] <= 0:
                continue
            # ballot: after placing v, need cnt[v] <= cnt[v-1]
            if v > 1 and cnt[v] + 1 > cnt[v - 1]:
                continue
            grid[(r, c)] = v
            cnt[v] += 1
            remaining[v - 1] -= 1
            backtrack(idx + 1)
            remaining[v - 1] += 1
            cnt[v] -= 1
            del grid[(r, c)]

    backtrack(0)
    return result

# ----------------------------------------------------------------------------
# M2: LR coefficient via Jacobi-Trudi + Schur decomposition (algebraic)
# ----------------------------------------------------------------------------
# Symmetric functions as dict {partition: int coeff} in the complete-homogeneous
# expansion is awkward; instead we work in the Schur basis directly using the
# skew Jacobi-Trudi determinant expressed via the h-to-Schur Pieri rule.
#
# We compute s_{nu/lam} in the Schur basis, then read the coefficient of s_mu.
# s_{nu/lam} = det( h_{nu_i - lam_j - i + j} ).  We expand the determinant as a
# signed sum of products of h's, and multiply out using the Pieri rule
#   s_kappa * h_r = sum over kappa+horizontal r-strip.
# h_0 = 1, h_{<0} = 0.  This shares no code with the tableau counter.

def h_times_schur(schur_dict, r):
    """Multiply a Schur-basis element sum by h_r using the Pieri rule."""
    if r == 0:
        return dict(schur_dict)
    if r < 0:
        return {}
    out = {}
    for kappa, coeff in schur_dict.items():
        for newp in pieri_h(kappa, r):
            out[newp] = out.get(newp, 0) + coeff
    return out

def pieri_h(kappa, r):
    """All partitions obtained from kappa by adding a horizontal r-strip.

    mu contains kappa and mu/kappa is a horizontal strip iff
        kappa[i] <= mu[i] <= kappa[i-1]   (kappa[-1] = +inf)
    with sum(mu) = sum(kappa) + r.  new[i] <= new[i-1] follows automatically.
    """
    kap = list(kappa) + [0]
    L = len(kap)
    results = set()

    def rec(i, added, cur):
        if i == L:
            if added == r:
                results.add(tuple(x for x in cur if x > 0))
            return
        lo = kap[i]
        hi = kap[i] + (r - added)          # cannot add more than r boxes total
        if i > 0:
            hi = min(hi, kap[i - 1], cur[i - 1])   # horizontal strip + partition
        for val in range(lo, hi + 1):
            cur.append(val)
            rec(i + 1, added + (val - kap[i]), cur)
            cur.pop()

    rec(0, 0, [])
    return results

def skew_schur_in_schur(lam, nu):
    """Return dict {partition: coeff} = s_{nu/lam} in the Schur basis."""
    nrows = len(nu)
    lam = tuple(lam) + (0,) * (nrows - len(lam))
    nu = tuple(nu)
    n = nrows
    # Jacobi-Trudi matrix exponents: M[i][j] = nu[i] - lam[j] - i + j  (0-indexed)
    M = [[nu[i] - lam[j] - i + j for j in range(n)] for i in range(n)]
    # expand determinant: sum over permutations sgn * prod h_{M[i][perm(i)]}
    from itertools import permutations
    total = {(): 0}
    total = {}
    for perm in permutations(range(n)):
        # sign
        sgn = 1
        pl = list(perm)
        for a in range(n):
            for b in range(a + 1, n):
                if pl[a] > pl[b]:
                    sgn = -sgn
        exps = [M[i][perm[i]] for i in range(n)]
        if any(e < 0 for e in exps):
            continue
        # product of h_{exps} applied to 1 (empty partition)
        cur = {(): 1}
        ok = True
        for e in exps:
            cur = h_times_schur(cur, e)
            if not cur:
                ok = False
                break
        if not ok:
            continue
        for p, c in cur.items():
            total[p] = total.get(p, 0) + sgn * c
    return {p: c for p, c in total.items() if c != 0}

def lr_coeff_schur(lam, mu, nu):
    if sum(lam) + sum(mu) != sum(nu):
        return 0
    if not contains(nu, lam):
        return 0
    d = skew_schur_in_schur(lam, nu)
    return d.get(tuple(mu), 0)

# ----------------------------------------------------------------------------
# stretched polynomial via exact finite differences
# ----------------------------------------------------------------------------

def stretched_values(lam, mu, nu, npts):
    return [lr_coeff_tableaux(scale(lam, N), scale(mu, N), scale(nu, N))
            for N in range(npts)]

def poly_from_values(values):
    """Given P(0),P(1),...,P(m), return exact monomial coeffs [a0,a1,...,ad]
    of the minimal-degree polynomial, or None if values are not polynomial
    within the sampled range (degree not stabilized)."""
    m = len(values) - 1
    # forward difference table
    diffs = [list(map(Fraction, values))]
    for k in range(1, m + 1):
        prev = diffs[-1]
        diffs.append([prev[i + 1] - prev[i] for i in range(len(prev) - 1)])
    # degree = largest k with a nonzero entry at level k
    deg = 0
    for k in range(m + 1):
        if any(x != 0 for x in diffs[k]):
            deg = k
    # stability: all difference levels beyond deg must be entirely zero
    for k in range(deg + 1, m + 1):
        if any(x != 0 for x in diffs[k]):
            return None  # not stabilized -> need more points
    # need at least deg+2 points to have seen one extra zero level (stability)
    if m < deg + 1:
        return None
    # Newton forward: P(x) = sum_{k=0}^{deg} diffs[k][0] * C(x,k)
    # convert binomial basis to monomial via building polynomials
    # represent polynomials as coeff lists
    def poly_add(a, b):
        n = max(len(a), len(b))
        return [ (a[i] if i < len(a) else Fraction(0)) + (b[i] if i < len(b) else Fraction(0)) for i in range(n)]
    def poly_scale(a, s):
        return [c * s for c in a]
    def poly_mul(a, b):
        res = [Fraction(0)] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                res[i + j] += ai * bj
        return res
    # C(x,k) = product_{i=0}^{k-1} (x - i) / k!
    binom = [Fraction(1)]  # C(x,0)=1
    poly = poly_scale(binom, diffs[0][0])
    running = [Fraction(1)]
    for k in range(1, deg + 1):
        running = poly_mul(running, [Fraction(-(k - 1)), Fraction(1)])  # *(x-(k-1))
        ck = poly_scale(running, Fraction(1, _fact(k)))
        poly = poly_add(poly, poly_scale(ck, diffs[k][0]))
    # trim
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly

@lru_cache(maxsize=None)
def _fact(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r

def hive_dim_bound(nrows):
    return (nrows - 1) * (nrows - 2) // 2 if nrows >= 2 else 0

def stretched_poly(lam, mu, nu):
    nrows = len(nu)
    dbound = hive_dim_bound(nrows)
    cap = 2 * dbound + 4
    npts = min(6, cap)
    vals = stretched_values(lam, mu, nu, npts)
    poly = poly_from_values(vals)
    while poly is None and npts < cap:
        npts = min(npts + 2, cap)
        vals = stretched_values(lam, mu, nu, npts)
        poly = poly_from_values(vals)
    return poly, vals

# ----------------------------------------------------------------------------
# canonicalization under LR symmetry (dedupe scan)
# ----------------------------------------------------------------------------

def canonical_triple(lam, mu, nu):
    # ONLY the swap lam<->mu is a valid symmetry of the STRETCHED polynomial
    # P(N) = c^{Nnu}_{Nlam,Nmu}.  Simultaneous conjugation is a symmetry of the
    # unstretched coefficient (N=1) but NOT of P, because scaling and transpose
    # do not commute: (N lam)' != N(lam').  Verified counterexample:
    # lam=mu=(4,2), nu=(6,4,2) gives P = 1 + 2t, but the conjugate triple gives
    # 1 + (3/2)t + (1/2)t^2.  So conjugation must NOT be used to deduplicate.
    # The full valid group is the honeycomb S_3 (order 6, Ehrhart-preserving);
    # implementing it needs rectangle-complement transforms + property tests and
    # is deferred.  Swap-only (order 2) is provably valid and used here.
    a, b = tuple(lam), tuple(mu)
    if b < a:
        a, b = b, a
    return (a, b, tuple(nu))

if __name__ == "__main__":
    print("== Stage 1: cross-check M1 (tableaux) vs M2 (Jacobi-Trudi/Schur) ==")
    tests = 0
    mism = 0
    parts = partitions_upto(4, 8)
    for lam in parts:
        for mu in parts:
            if sum(mu) < sum(lam):
                continue
            target = sum(lam) + sum(mu)
            for nu in partitions_upto(4, target):
                if sum(nu) != target:
                    continue
                if not contains(nu, lam) or not contains(nu, mu):
                    continue
                c1 = lr_coeff_tableaux(lam, mu, nu)
                c2 = lr_coeff_schur(lam, mu, nu)
                tests += 1
                if c1 != c2:
                    mism += 1
                    if mism <= 10:
                        print(f"  MISMATCH lam={lam} mu={mu} nu={nu}: M1={c1} M2={c2}")
    print(f"  checked {tests} coefficients, mismatches: {mism}")
    # known-value spot checks
    spot = [
        ((1,),(1,),(2,),1),
        ((1,),(1,),(1,1),1),
        ((2,1),(2,1),(3,2,1),2),
        ((2,1),(2,1),(4,2),1),
        ((2,1),(2,1),(2,2,2),1),
        ((3,2,1),(3,2,1),(4,4,4) ,None),
    ]
    print("  spot checks (M1):")
    for lam,mu,nu,exp in spot:
        c = lr_coeff_tableaux(lam,mu,nu)
        tag = "" if exp is None else ("  OK" if c==exp else f"  EXPECTED {exp}")
        print(f"    c^{nu}_{{{lam},{mu}}} = {c}{tag}")
    print(f"\n  M1==M2 on all {tests} tested triples: {mism==0}")
    sys.stdout.flush()
