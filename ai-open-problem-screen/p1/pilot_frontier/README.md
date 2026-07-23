# Scientific pilot frontier runner

This package runs real LR evaluations through `p1.e1.evaluator` and
`p1.e2.hive_e2`. It does not reuse the orchestration-only records from
`p1.control.pilot`.

Its output is always labelled **`partial-extension / not-outcome-B`**. Even a
fully consumed pilot plan is not one of the preregistered B1-B4 boxes, and E1
alone does not certify a negative candidate.

## Safety and reproducibility

- deterministic structural enumeration, sorted by `(len(nu),nu,lam,mu)`;
- swap-only canonicalization (`swap-only-v1`), never conjugation;
- the verified length-at-most-5, size-at-most-7 baseline as a hash-bound frozen
  structural prefix (14,302 structural records, 7,549 nonzero);
- exact bounded `lrcalc`/`Fraction` E1 evaluation for every new nonzero: fit at
  `N=0..B`, where `B` is the hive ambient-dimension bound, and require the
  reserved `N=B+1` holdout to agree;
- a separate explicit-hive Normaliz-Ehrhart record for every new nonzero;
- exact canonical-polynomial and N=1 agreement between those two records;
- raw typed hive matrices and raw Normaliz results retained in immutable chunks;
- an immutable frozen-prefix chunk followed by fixed 32-record extension chunks,
  all with file hashes and a per-record prefix hash chain;
- checkpoint reconstruction after a crash (the checkpoint is never trusted as
  the source of truth);
- an immutable completion certificate only after every planned ordinal exists;
- zero, nonzero, and error counts at every durable boundary;
- minima and champions appear only in the completion artifact;
- an explicit passing P1 gate must be validated and frozen before evaluation.

## B0-7 command sequence (do not authorize/run before integrator approval)

From the repository root in the existing WSL virtual environment:

```bash
.venv-wsl/bin/python -m p1.pilot_frontier init \
  --work-dir run/pilot-frontier/B0-7 \
  --max-length 6 --max-size 7 --chunk-size 32 --b0-7

.venv-wsl/bin/python -m p1.pilot_frontier authorize \
  --work-dir run/pilot-frontier/B0-7 \
  --gate-report run/p1/gate_report.json \
  --evidence-manifest run/p1/evidence_manifest.json \
  --evidence-root . \
  --confirm-p1-passed

.venv-wsl/bin/python -m p1.pilot_frontier run \
  --work-dir run/pilot-frontier/B0-7

.venv-wsl/bin/python -m p1.pilot_frontier verify \
  --work-dir run/pilot-frontier/B0-7
```

The first command only creates the 18,287-item structural plan. It preregisters
the 14,302-item frozen prefix, 3,985-item new structural suffix, and the
independently counted 1,929 new nonzero records that must pass E1/E2 agreement.
The second is
the explicit P1 authorization boundary. The third is idempotent and resumes at
the first missing fixed chunk. For a deliberate bounded stop, add
`--max-chunks 1`; rerunning without it resumes safely.

For an initial post-authorization runtime sample, use `--max-chunks 2`. In
B0-7 that commits the single frozen-prefix chunk and exactly one 32-record new
extension chunk, giving a representative persisted E1/E2 timing boundary
without launching the whole suffix. A later command without `--max-chunks`
continues from the next ordinal.

## Tests

```bash
.venv-wsl/bin/python -m unittest p1.pilot_frontier.test_runner -v
```

The suite builds the B0-7 plan in memory but does not run it. One direct small
length-6 witness exercises separate real E1/E2 evaluation. Resume tests use a
tiny scope, deliberately stop after one chunk, remove the
checkpoint to model the crash window, reconstruct it from immutable chunks,
resume to completion, and verify every digest.
