"""Complete four-row screen for the empty-tetrahedron (Reeve) mechanism,
over the CORRECTED official domain.

Domain (four-row slice): all three partitions have length <= 4, and
  |nu| = |lam| + |mu| <= 30            (the corrected official bound)
Hive dimension for n=4 is (n-1)(n-2)/2 = 3, so deg P <= 3.

Mechanism and exact test
------------------------
A known low-rank fact (Buch, after Example 2) says integral-boundary hives have
integral vertices for n <= 4. Thus the lattice-polytope argument below applies
to every member of this slice.

A 3-dimensional lattice polytope with exactly 4 lattice points is an *empty
tetrahedron*; by White's classification its Ehrhart polynomial is
    P(t) = (D/6) t^3 + t^2 + (2 - D/6) t + 1,      D = normalized volume,
so  P(1) = 4  identically and  P(2) = D + 9.
The linear coefficient is negative  <=>  D > 12  <=>  P(2) > 21.

Dimension does not need to be determined separately: a lattice polytope of
dimension <= 2 with exactly 4 lattice points has P(2) <= 10
  (dim 1: P = 3t+1 -> P(2) = 7;  dim 2 by Pick with I+B=4: P(2) in {9,10}),
so any hit with P(2) > 21 is necessarily a 3-dimensional empty tetrahedron with
D > 12, hence a genuine negative Ehrhart coefficient.

Therefore the screen is exactly:
    c(1) == 4   and   c(2) > 21     =>  NEGATIVE COEFFICIENT (counterexample)

Both tests use *capped* LR counting and abort once the decision threshold is
reached. This avoids constructing larger counts but is not an O(cap) worst-case
time guarantee because the backtracking tree can contain dead branches.

Scope: this is complete for the empty-tetrahedron mechanism in the four-row
slice. It does NOT screen dimension-3 hives with more than 4 lattice points, nor
lengths 5-7. Null result = "the Reeve mechanism does not occur here", not
"positivity holds".
"""

import json, hashlib, sys, time

# ---------------------------------------------------------------- partitions

def parts_le(maxlen, maxsize):
    out = []
    def rec(rem, mx, cur):
        out.append(tuple(cur))
        if len(cur) == maxlen:
            return
        for p in range(min(mx, rem), 0, -1):
            cur.append(p); rec(rem - p, p, cur); cur.pop()
    rec(maxsize, maxsize, [])
    return [p for p in dict.fromkeys(out) if sum(p) <= maxsize]

def contains(nu, lam):
    if len(lam) > len(nu):
        return False
    return all(lam[i] <= nu[i] for i in range(len(lam)))

def scale(p, N):
    return tuple(x * N for x in p if x * N)

# --------------------------------------------- capped LR coefficient counter

def lr_count_capped(lam, mu, nu, cap):
    """Number of LR tableaux of shape nu/lam, content mu, but stop counting at
    `cap` (returns cap if the true count is >= cap)."""
    if sum(lam) + sum(mu) != sum(nu):
        return 0
    if not contains(nu, lam):
        return 0
    nrows = len(nu)
    lam = tuple(lam) + (0,) * (nrows - len(lam))
    cells = []
    for r in range(nrows):
        for c in range(nu[r], lam[r], -1):      # right -> left
            cells.append((r, c))
    ncells = len(cells)
    maxval = len(mu)
    if ncells == 0:
        return 1 if maxval == 0 else (1 if sum(mu) == 0 else 0)
    grid = {}
    cnt = [0] * (maxval + 2)
    remaining = list(mu)
    total = 0

    def bt(idx):
        nonlocal total
        if total >= cap:
            return
        if idx == ncells:
            total += 1
            return
        r, c = cells[idx]
        right = grid.get((r, c + 1))
        above = grid.get((r - 1, c))
        hi = right if right is not None else maxval
        lo = (above + 1) if above is not None else 1
        for v in range(lo, hi + 1):
            if v > maxval:
                break
            if remaining[v - 1] <= 0:
                continue
            if v > 1 and cnt[v] + 1 > cnt[v - 1]:
                continue
            grid[(r, c)] = v; cnt[v] += 1; remaining[v - 1] -= 1
            bt(idx + 1)
            remaining[v - 1] += 1; cnt[v] -= 1; del grid[(r, c)]
            if total >= cap:
                return

    bt(0)
    return total

# ------------------------------------------------------------------- screen

def run(maxlen=4, maxsize=30, progress_every=250000):
    t0 = time.time()
    allp = parts_le(maxlen, maxsize)
    bysize = {}
    for p in allp:
        bysize.setdefault(sum(p), []).append(p)

    n_triples = 0
    n_nonzero = 0
    pool = 0                 # c(1) == 4
    hits = []                # c(2) > 21
    c2_max = 0
    c2_max_witness = None
    c1_hist = {}

    for nu in allp:
        n = sum(nu)
        if n == 0:
            continue
        for a in range(0, n // 2 + 1):
            for lam in bysize.get(a, []):
                if not contains(nu, lam):
                    continue
                for mu in bysize.get(n - a, []):
                    if not contains(nu, mu):
                        continue
                    if a == n - a and mu < lam:
                        continue
                    n_triples += 1
                    c1 = lr_count_capped(lam, mu, nu, 5)
                    if c1 == 0:
                        continue
                    n_nonzero += 1
                    c1_hist[c1] = c1_hist.get(c1, 0) + 1
                    if c1 != 4:
                        continue
                    pool += 1
                    c2 = lr_count_capped(scale(lam, 2), scale(mu, 2),
                                         scale(nu, 2), 22)
                    if c2 > c2_max:
                        c2_max = c2
                        c2_max_witness = (lam, mu, nu)
                    if c2 > 21:
                        hits.append({"lam": list(lam), "mu": list(mu),
                                     "nu": list(nu), "c1": 4, "c2_capped": c2})
                    if progress_every and n_triples % progress_every == 0:
                        sys.stderr.write(
                            f"  {n_triples:,} triples  nonzero={n_nonzero:,} "
                            f"pool(c1=4)={pool:,} hits={len(hits)} "
                            f"({round(time.time()-t0)}s)\n")
                        sys.stderr.flush()

    dt = round(time.time() - t0, 1)
    result = {
        "scope": {"max_length": maxlen, "max_size_nu": maxsize,
                  "note": ("domain: |nu|=|lam|+|mu|<="
                           f"{maxsize}, all lengths<={maxlen}")},
        "mechanism": ("integral four-row empty-tetrahedron channel: "
                      "c(1)==4 and c(2)>21 iff negative linear coefficient"),
        "support_compatible_triples": n_triples,
        "nonzero_triples": n_nonzero,
        "mechanism_pool_c1_eq_4": pool,
        "hits_negative_coefficient": hits,
        "n_hits": len(hits),
        "max_c2_in_pool_capped_at_22": c2_max,
        "max_c2_witness": ([list(x) for x in c2_max_witness]
                           if c2_max_witness else None),
        "c1_histogram_capped_at_5": {str(k): v for k, v in sorted(c1_hist.items())},
        "seconds": dt,
    }
    return result

if __name__ == "__main__":
    ml = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    ms = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    res = run(ml, ms)
    payload = json.dumps(res, sort_keys=True, separators=(",", ":"))
    res["sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    out = f"four_row_screen_len{ml}_size{ms}.json"
    with open(out, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("c1_histogram_capped_at_5",)}, indent=1))
    print("histogram c(1) (capped at 5):", res["c1_histogram_capped_at_5"])
    print("written:", out, "sha256:", res["sha256"])
