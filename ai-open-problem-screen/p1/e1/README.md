# E1: exact LR counts and rational interpolation

This directory contains the production E1 evaluator and the executable half of
the P1 dry-run parity gate.  It uses the WSL project environment's `lrcalc 2.1`
and Python `fractions.Fraction`; it never imports the dry-run evaluator and never
writes `dryrun/frontier_baseline.json`.

The lrcalc convention is pinned by asymmetric anchors:

```text
lrcalc.lrcoef(out, inn1, inn2)
c^nu_{lam,mu} = lrcalc.lrcoef(nu, lam, mu)
```

## Run the tests

From the project root in WSL:

```bash
.venv-wsl/bin/python -m unittest discover -s p1/e1 -p 'test_*.py' -v
```

## Run the complete parity gate

```bash
.venv-wsl/bin/python p1/e1/parity.py --mode adaptive --workers 4
```

The command independently enumerates the complete `length <= 5`, inner
`size <= 7` box, applies only the sound swap symmetry, filters nonzero triples
with lrcalc, recomputes all stretched polynomials, and compares the canonical
payload to the frozen 7,549-record hash.  It writes deterministic artifacts to
`p1/e1/out/`:

- `actual_frontier.json` (the independently recomputed 7,549 records, allowing
  the controller to hash payload bytes instead of trusting the report)
- `parity_report.json`
- `mismatches.json` (an empty `items` array on success)
- `artifact_manifest.json` (byte sizes and SHA-256 hashes for all three artifacts)

Elapsed time is printed to stderr and intentionally omitted from the report, so
identical inputs and options produce identical report bytes.

## Interpolation modes

- `adaptive` reproduces the frozen P1 baseline policy: increase a consecutive value
  prefix until the top finite-difference level vanishes, then enforce the hive
  dimension degree bound. Its P1 acceptance is additionally pinned to the
  independently generated baseline payload; it is not the scientific-pilot or
  candidate-certification mode.
- `bounded` fits through the dimension bound `B` and verifies at `N=B+1`.
  This is the routine frontier/scientific-pilot mode.
- `conservative` fits at `N=0..B` and verifies every point through `N=2B+2`,
  using `2B+3` samples.  At seven rows this is exactly `N=0..32`.  This mode is
  retained for final candidate verification and is not weakened merely because
  it is substantially slower on large anchors.

P1 does not pass on a partial run: the independently recomputed record count must
be 7,549 and its canonical payload SHA-256 must be exactly
`b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7`.
