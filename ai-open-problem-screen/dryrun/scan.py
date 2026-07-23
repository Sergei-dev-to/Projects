"""Stage 2 frontier scan: map the minimum monomial coefficient of the stretched
LR polynomial over small-length triples, looking for a negative one."""
import sys, time
from fractions import Fraction
from lr_dryrun import (partitions_upto, contains, lr_coeff_tableaux,
                       lr_coeff_schur, stretched_poly, canonical_triple,
                       hive_dim_bound, conj)

def run(max_len, max_size, crosscheck=True, sample_report=12):
    t0 = time.time()
    # Stage 1 cross-check at this scope
    if crosscheck:
        parts = partitions_upto(max_len, min(max_size, 8))
        tests = mism = 0
        for lam in parts:
            for mu in parts:
                tgt = sum(lam) + sum(mu)
                for nu in partitions_upto(max_len, tgt):
                    if sum(nu) != tgt or not contains(nu, lam) or not contains(nu, mu):
                        continue
                    if lr_coeff_tableaux(lam, mu, nu) != lr_coeff_schur(lam, mu, nu):
                        mism += 1
                    tests += 1   # per tested triple (was erroneously per (lam,mu))
        print(f"[xcheck len<={max_len} size<=min({max_size},8)] "
              f"mismatches={mism}  ({round(time.time()-t0,1)}s)")

    # Stage 2 scan
    parts = partitions_upto(max_len, max_size)
    seen = set()
    n_triples = 0
    n_nontrivial = 0
    min_coeff = None
    min_examples = []          # (coeff, deg, lam, mu, nu, poly)
    negatives = []
    unresolved = 0
    champions = []             # smallest positive min-coeff per triple

    for lam in parts:
        for mu in parts:
            if sum(mu) < sum(lam):
                continue
            tgt = sum(lam) + sum(mu)
            for nu in partitions_upto(max_len, tgt):
                if sum(nu) != tgt:
                    continue
                if not contains(nu, lam) or not contains(nu, mu):
                    continue
                key = canonical_triple(lam, mu, nu)
                if key in seen:
                    continue
                seen.add(key)
                c1 = lr_coeff_tableaux(lam, mu, nu)
                if c1 == 0:
                    continue
                n_triples += 1
                poly, vals = stretched_poly(lam, mu, nu)
                if poly is None:
                    unresolved += 1
                    continue
                deg = len(poly) - 1
                if deg < 1:
                    continue        # constant polynomial, not informative
                n_nontrivial += 1
                mn = min(poly)
                # also track the smallest NON-leading coefficient: the leading
                # (volume) coeff shrinks with dimension and is always > 0, so the
                # negativity phenomenon lives in the lower/middle coefficients.
                sub = min(poly[:-1]) if deg >= 1 else mn
                champions.append((sub, mn, deg, lam, mu, nu, [str(c) for c in poly]))
                if mn < 0:
                    negatives.append((lam, mu, nu, [str(c) for c in poly]))
                if min_coeff is None or mn < min_coeff:
                    min_coeff = mn

    champions.sort(key=lambda x: (x[0], -x[2]))
    dt = round(time.time() - t0, 1)
    print(f"[scan len<={max_len} size<={max_size}] canonical nontrivial triples: "
          f"{n_nontrivial}  (total nonzero {n_triples}, unresolved {unresolved})  {dt}s")
    print(f"  global minimum monomial coefficient = {min_coeff}")
    print(f"  negative-coefficient triples found: {len(negatives)}")
    for lam, mu, nu, poly in negatives[:20]:
        print(f"    NEGATIVE  lam={lam} mu={mu} nu={nu}  P={poly}")
    print(f"  smallest NON-leading coefficient champions (subcoeff, mincoeff, deg):")
    for sub, mn, deg, lam, mu, nu, poly in champions[:sample_report]:
        print(f"    sub={sub} min={mn} deg={deg}  lam={lam} mu={mu} nu={nu}  P={poly}")
    sys.stdout.flush()
    return champions, negatives

if __name__ == "__main__":
    ml = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    ms = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    run(ml, ms)
