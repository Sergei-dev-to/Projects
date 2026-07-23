"""Generate an immutable, checksummed dry-run frontier baseline.

Produces frontier_baseline.json (complete canonical triple set + every exact
stretched polynomial) and frontier_baseline.sha256. The production pipeline
(Phase 1) must reproduce the canonical ``triples`` payload and its hash; the
hash is deliberately not a hash of the complete JSON file.

CANONICALIZATION (order-2, swap-only — the only provably valid choice here):
  quotient by the swap lam<->mu, the ONLY symmetry that preserves the stretched
  polynomial P(N)=c^{Nnu}_{Nlam,Nmu}.  Simultaneous conjugation is a symmetry of
  the unstretched coefficient but NOT of P (scaling and transpose don't commute),
  so it is NOT used.  The full valid group is the honeycomb S_3 (order 6);
  implementing it (rectangle-complement transforms) with per-generator property
  tests against the oracle is a pre-P2 task.  Swap-only over-computes honeycomb
  duplicates but never drops a case, so the frontier stays exhaustive.

SERIALIZATION CONVENTION (defines canonical payload equality):
  each triple -> {"lam":[..],"mu":[..],"nu":[..],"poly":["p/q",..]}
    - lam,mu,nu: lists of ints (the canonical representative)
    - poly: exact monomial coeffs low->high degree, str(Fraction) (e.g. "1","11/6")
  triples list sorted by (len(nu), nu, lam, mu).
  PARITY HASH = sha256( json.dumps(triples, sort_keys=True,
                                   separators=(",", ":")).encode() ).
  Every nonzero-coefficient canonical triple is included (constant and linear
  polynomials too) so the record is a complete finite box, not a filtered view.
"""

import json, hashlib, sys, time
from fractions import Fraction
from lr_dryrun import (partitions_upto, contains, lr_coeff_tableaux,
                       lr_coeff_schur, stretched_poly, canonical_triple, scale)

def build(max_len, max_size, crosscheck_N=1):
    t0 = time.time()
    parts = partitions_upto(max_len, max_size)
    seen = set()
    triples = []
    xchecked = 0
    for lam in parts:
        for mu in parts:
            if sum(mu) < sum(lam):
                continue
            tgt = sum(lam) + sum(mu)
            for nu in partitions_upto(max_len, tgt):
                if sum(nu) != tgt or not contains(nu, lam) or not contains(nu, mu):
                    continue
                key = canonical_triple(lam, mu, nu)
                if key in seen:
                    continue
                seen.add(key)
                cl, cm, cn = key
                if lr_coeff_tableaux(cl, cm, cn) == 0:
                    continue
                poly, vals = stretched_poly(cl, cm, cn)
                if poly is None:
                    raise RuntimeError(f"unresolved polynomial for {key}")
                # independent coefficient cross-check at small N (M1 vs M2)
                for N in range(min(crosscheck_N, len(vals) - 1) + 1):
                    if lr_coeff_schur(scale(cl, N), scale(cm, N),
                                      scale(cn, N)) != vals[N]:
                        raise RuntimeError(f"M1/M2 mismatch at N={N} for {key}")
                xchecked += 1
                triples.append({
                    "lam": list(cl), "mu": list(cm), "nu": list(cn),
                    "poly": [str(c) for c in poly],
                })
    triples.sort(key=lambda r: (len(r["nu"]), r["nu"], r["lam"], r["mu"]))
    payload = json.dumps(triples, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode()).hexdigest()
    meta = {
        "scope": {"max_length": max_len, "max_size": max_size},
        "canonicalization": "order-2 swap-only (the only symmetry that preserves the stretched polynomial); conjugation is NOT a valid P-symmetry",
        "serialization": "poly = exact monomial coeffs low->high as str(Fraction); "
                         "triples sorted by (len(nu),nu,lam,mu)",
        "parity_hash_definition": "sha256(json.dumps(triples,sort_keys=True,separators=(',',':')))",
        "count": len(triples),
        "crosschecked_N_upto": crosscheck_N,
        "crosschecked_triples": xchecked,
        "generator": "dryrun/baseline.py (stdlib M1 counts + exact interpolation)",
    }
    obj = {"meta": meta, "sha256": digest, "triples": triples}
    print(f"[baseline len<={max_len} size<={max_size}] "
          f"triples={len(triples)}  xchecked={xchecked}  "
          f"sha256={digest}  ({round(time.time()-t0,1)}s)")
    return obj, digest, payload

if __name__ == "__main__":
    ml = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    ms = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    obj, digest, payload = build(ml, ms)
    with open("frontier_baseline.json", "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
    with open("frontier_baseline.sha256", "w") as f:
        f.write(digest + "  frontier_baseline.json:triples (canonical payload)\n")
    # negative-coefficient audit over the baseline
    negs = [t for t in obj["triples"]
            if any(Fraction(c) < 0 for c in t["poly"])]
    print(f"  negative-coefficient triples in baseline: {len(negs)}")
