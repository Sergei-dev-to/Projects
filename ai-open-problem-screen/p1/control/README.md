# Executable orchestration controls

This package implements the run book's control plane using only the Python
standard library. It does not construct hives, evaluate LR coefficients,
transition state on a successful gate, authorize P2, or start P2.

## Authority and write ownership

- Scientific runners own evaluator outputs and immutable artifact manifests.
- The designated integrator is the only campaign-state writer.
- A gate report is evidence for an integrator decision; it is never a state
  transition by itself.
- Every state write needs an exclusive lock, the prior revision, and the prior
  canonical document SHA-256. Lock files are never stolen or expired
  automatically.
- Atomic writes use a same-directory temporary file, `fsync`, and `os.replace`.

The allowed state path ends at `P2_AWAITING_AUTHORIZATION`; there is deliberately
no `P2_RUNNING` transition in this package.

## Artifact contract for P1

Create a manifest rooted at the repository. The gate requires exactly one each of
`baseline-frontier`, `e1-parity-report`, `e1-frontier-payload`,
`e1-mismatch-bundle`, `e1-artifact-manifest`, `fixture-definition-set`,
`fixture-agreement`, `fixture-evaluator-lrcalc`,
`fixture-evaluator-normaliz`, `e2-fixture-summary`, and `e2-summary-sidecar`.
It also requires the complete per-fixture `fixture-comparison-report`,
`explicit-hive-input`, `normaliz-input`, and `normaliz-raw-output` sets.

The controller directly hashes the independently recomputed E1 frontier; parity
cannot be established by a self-authored summary report. The internal E1 manifest
must bind the frontier, report, and empty mismatch bundle.

The default P1 policy independently recomputes the baseline `triples` payload
hash and count. Fixture evidence requires both evaluator names, canonical reduced
monomial coefficients, exact agreement, at least six fixtures, and these coverage
tags (derived from the pinned fixture facts, not trusted from the adapter):

`boundary.lambda`, `boundary.mu`, `boundary.nu`, `rhombus.type-a`,
`rhombus.type-b`, `rhombus.type-c`, `dimension.zero`, `dimension.positive`,
`dimension.degenerate`, `dimension.empty`, `coefficient.zero`,
`coefficient.one`, `coefficient.multiple`, and `anchor.degree6`.

The policy pins the exact `p1/e2/fixtures.json` file hash. For every fixed
fixture, the gate links its definition, exact all-pass comparison report,
explicit hive input bytes/canonical hash, typed lrcalc samples, and typed
PyNormaliz output. It independently decodes the raw Ehrhart quasipolynomial and
checks `P(1) == number_lattice_points`. Normaliz CLI `.out` is hash-linked
corroborating provenance only; its prose is not the canonical arithmetic source.
The canonical E2 source is the exact PyNormaliz data preserved in the typed and
per-fixture JSON reports.

The CLI can evaluate an explicitly supplied policy for review, but campaign-state
transitions rerun the built-in versioned policy. Changing fixture nomenclature or
requirements therefore needs a reviewed control/schema version change; a runner
cannot supply a weaker policy merely to make the state gate pass.

Transitioning to `P1_ORACLE_VALIDATED` requires both the gate report and its
evidence manifest. The state store reruns the gate from the manifested repository
bytes and requires the recorded report to equal that fresh result. A standalone
JSON document claiming `passed: true` is insufficient.

## Commands

Run from the repository root, preferably inside the recorded WSL environment:

```text
.venv-wsl/bin/python -m p1.control --help
.venv-wsl/bin/python -m p1.control pilot run --work-dir <pilot-dir> --stop-after 3
.venv-wsl/bin/python -m p1.control pilot verify-snapshot --work-dir <pilot-dir> --snapshot <pilot-dir>/checkpoint-snapshots/000003.json --require-current
.venv-wsl/bin/python -m p1.control pilot run --work-dir <pilot-dir>
.venv-wsl/bin/python -m p1.control pilot verify --work-dir <pilot-dir>
.venv-wsl/bin/python -m p1.control pilot verify-snapshot --work-dir <pilot-dir> --snapshot <pilot-dir>/checkpoint-snapshots/000003.json
.venv-wsl/bin/python -m p1.control gate --root <evidence-root> --manifest <manifest.json> --out <gate-report.json>
.venv-wsl/bin/python -m p1.control readiness --repo-root . --p1-evidence-root <root> --p1-manifest <manifest.json> --pilot-dir <pilot-dir> --state <state.json> --out <readiness.json>
```

The pilot is orchestration-only. Every artifact says
`not_scientific_evidence: true`, and completion says `may_authorize_p2: false`.
It verifies deterministic order, immutable per-item results, crash recovery when
a result is durable but its checkpoint lags, tamper detection, and identical
one-shot/resumed completion.

An incomplete `pilot run` also writes a deterministic immutable snapshot at
`checkpoint-snapshots/<next_index>.json` (six-digit zero padding). Campaign
state must record this file as `pilot-checkpoint-snapshot`; it must never record
the mutable `checkpoint.json` pointer. Entry to `PILOT_CHECKPOINTED` validates
that the snapshot is the current durable head. `pilot verify-snapshot` validates
the same snapshot against its exact result prefix even after the pointer advances
or the pilot completes. Snapshot files are create-once and are deliberately not
part of the completion manifest, so one-shot and resumed completions remain
byte-identical.

State chains produced by the older mutable-pointer contract are not migrated in
place: their historical SHA-256 record cannot be repaired without changing every
later state digest. Archive the old state and pilot directory, choose fresh paths,
run the pilot with an intentional partial stop, initialize/replay the state chain
using the generated `pilot-checkpoint-snapshot`, then resume the pilot and record
completion. Treat the old chain as superseded audit evidence, not a valid input
to further transitions.

For the first real post-P1 checkpoint exercise, use a separately implemented and
clearly labeled partial extension such as length <= 6, size <= 7 (B0-7), not this
toy pilot and not preregistered B1. It cannot count as outcome B.

## Tests

```text
.venv-wsl/bin/python -m unittest discover -s p1/control/tests -v
```
