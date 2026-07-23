#!/usr/bin/env python3
"""Recompute the complete dry-run frontier with production E1.

This command never writes the baseline.  It independently enumerates the finite
box, filters it with lrcalc at N=1, recomputes every stretched polynomial, and
emits deterministic ``parity_report.json`` and ``mismatches.json`` artifacts.
Runtime is printed only to stderr so repeated successful runs produce identical
artifact bytes.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import time
from typing import Iterable

try:  # package execution: python -m p1.e1.parity
    from .evaluator import (
        Evaluation,
        Triple,
        canonical_polynomial_strings,
        canonical_triple,
        enumerate_structural_triples,
        evaluate_stretched,
        lr_coefficient,
        lrcalc_version,
        normalize_partition,
        run_anchor_checks,
        triple_sort_key,
    )
except ImportError:  # direct script execution from p1/e1
    from evaluator import (
        Evaluation,
        Triple,
        canonical_polynomial_strings,
        canonical_triple,
        enumerate_structural_triples,
        evaluate_stretched,
        lr_coefficient,
        lrcalc_version,
        normalize_partition,
        run_anchor_checks,
        triple_sort_key,
    )


SCHEMA_VERSION = 1
CANONICALIZER_VERSION = "swap-only-v1"
EXPECTED_BASELINE_COUNT = 7_549
EXPECTED_BASELINE_HASH = (
    "b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7"
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE = REPOSITORY_ROOT / "dryrun" / "frontier_baseline.json"
DEFAULT_SIDECAR = REPOSITORY_ROOT / "dryrun" / "frontier_baseline.sha256"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "out"


def canonical_payload(records: list[dict[str, object]]) -> str:
    """Serialize exactly as ``dryrun/baseline.py``."""

    return json.dumps(records, sort_keys=True, separators=(",", ":"))


def payload_hash(records: list[dict[str, object]]) -> str:
    return hashlib.sha256(canonical_payload(records).encode("utf-8")).hexdigest()


def record_hash(record: dict[str, object]) -> str:
    """Hash one canonical record for compact per-mismatch identification."""

    serialized = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _record_triple(record: dict[str, object]) -> Triple:
    return canonical_triple(record["lam"], record["mu"], record["nu"])


def _triple_json(triple: Triple) -> dict[str, list[int]]:
    lam, mu, nu = triple
    return {"lam": list(lam), "mu": list(mu), "nu": list(nu)}


def _mismatch_sort_key(item: dict[str, object]) -> tuple[object, ...]:
    triple_data = item.get("triple", {})
    if isinstance(triple_data, dict):
        triple = (
            tuple(triple_data.get("lam", ())),
            tuple(triple_data.get("mu", ())),
            tuple(triple_data.get("nu", ())),
        )
    else:
        triple = ((), (), ())
    return (str(item.get("kind", "")),) + triple_sort_key(triple)


def validate_baseline(path: Path, sidecar_path: Path) -> tuple[
    dict[str, object], list[dict[str, object]], list[str]
]:
    """Validate both the artifact's shape and the campaign's frozen anchors."""

    errors: list[str] = []
    try:
        baseline = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {}, [], [f"cannot read baseline: {type(exc).__name__}: {exc}"]
    if not isinstance(baseline, dict):
        return {}, [], ["baseline root must be a JSON object"]
    records = baseline.get("triples")
    if not isinstance(records, list):
        return baseline, [], ["baseline.triples must be a JSON list"]

    actual_hash = payload_hash(records)
    embedded_hash = baseline.get("sha256")
    if actual_hash != EXPECTED_BASELINE_HASH:
        errors.append(
            f"payload hash {actual_hash} != frozen {EXPECTED_BASELINE_HASH}"
        )
    if embedded_hash != actual_hash:
        errors.append(f"embedded hash {embedded_hash!r} != payload hash {actual_hash}")
    if len(records) != EXPECTED_BASELINE_COUNT:
        errors.append(
            f"record count {len(records)} != frozen {EXPECTED_BASELINE_COUNT}"
        )

    try:
        sidecar_token = sidecar_path.read_text(encoding="utf-8").split()[0]
    except Exception as exc:
        sidecar_token = None
        errors.append(f"cannot read hash sidecar: {type(exc).__name__}: {exc}")
    if sidecar_token != actual_hash:
        errors.append(f"sidecar hash {sidecar_token!r} != payload hash {actual_hash}")

    meta = baseline.get("meta")
    if not isinstance(meta, dict):
        errors.append("baseline.meta must be an object")
    else:
        scope = meta.get("scope")
        if scope != {"max_length": 5, "max_size": 7}:
            errors.append(f"unexpected baseline scope: {scope!r}")
        if meta.get("count") != len(records):
            errors.append("baseline.meta.count does not match triples length")

    previous_key: tuple[object, ...] | None = None
    seen: set[Triple] = set()
    for index, raw_record in enumerate(records):
        prefix = f"triples[{index}]"
        if not isinstance(raw_record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if set(raw_record) != {"lam", "mu", "nu", "poly"}:
            errors.append(f"{prefix} has noncanonical keys: {sorted(raw_record)}")
            continue
        try:
            raw_lam = normalize_partition(raw_record["lam"])
            raw_mu = normalize_partition(raw_record["mu"])
            raw_nu = normalize_partition(raw_record["nu"])
            triple = canonical_triple(raw_lam, raw_mu, raw_nu)
        except (TypeError, ValueError) as exc:
            errors.append(f"{prefix} invalid partition: {exc}")
            continue
        if triple != (raw_lam, raw_mu, raw_nu):
            errors.append(f"{prefix} is not swap-only canonical")
        lam, mu, nu = triple
        if len(lam) > 5 or len(mu) > 5 or len(nu) > 5:
            errors.append(f"{prefix} exceeds maximum length 5")
        if sum(lam) > 7 or sum(mu) > 7:
            errors.append(f"{prefix} exceeds inner size bound 7")
        if sum(lam) + sum(mu) != sum(nu):
            errors.append(f"{prefix} violates partition size conservation")
        key = triple_sort_key(triple)
        if previous_key is not None and key <= previous_key:
            errors.append(f"{prefix} is out of order or duplicated")
        previous_key = key
        if triple in seen:
            errors.append(f"{prefix} duplicates a canonical triple")
        seen.add(triple)
        polynomial = raw_record["poly"]
        if not isinstance(polynomial, list) or not polynomial:
            errors.append(f"{prefix}.poly must be a nonempty list")
        else:
            try:
                fractions = [Fraction(value) for value in polynomial]
            except (TypeError, ValueError, ZeroDivisionError) as exc:
                errors.append(f"{prefix}.poly is invalid: {exc}")
            else:
                if canonical_polynomial_strings(fractions) != polynomial:
                    errors.append(f"{prefix}.poly is not canonically serialized")

    integrity = {
        "embedded_payload_sha256": embedded_hash,
        "errors": errors,
        "record_count": len(records),
        "sidecar_payload_sha256": sidecar_token,
        "status": "pass" if not errors else "fail",
        "triples_payload_sha256": actual_hash,
    }
    return integrity, records, errors


def _evaluate_job(arguments: tuple[Triple, str]) -> tuple[
    Triple, dict[str, object] | None, dict[str, object] | None, dict[str, str] | None
]:
    """Process-pool worker; return a deterministic value or error description."""

    triple, mode = arguments
    lam, mu, nu = triple
    try:
        n1 = lr_coefficient(lam, mu, nu)
        if n1 == 0:
            return triple, None, None, None
        evaluation = evaluate_stretched(
            lam, mu, nu, mode=mode, known_n1=n1
        )
        record: dict[str, object] = {
            "lam": list(lam),
            "mu": list(mu),
            "nu": list(nu),
            "poly": evaluation.polynomial_strings(),
        }
        return triple, record, evaluation.evidence(), None
    except Exception as exc:
        return triple, None, None, {
            "message": str(exc),
            "type": type(exc).__name__,
        }


def _evaluate_all(
    triples: list[Triple], mode: str, workers: int,
) -> Iterable[tuple[
    Triple, dict[str, object] | None, dict[str, object] | None,
    dict[str, str] | None
]]:
    jobs = ((triple, mode) for triple in triples)
    if workers == 1:
        return map(_evaluate_job, jobs)
    executor = ProcessPoolExecutor(max_workers=workers)
    # The caller exhausts this iterator before function exit; attach the executor
    # so its lifetime is coupled to the generator and always shut down cleanly.
    def results() -> Iterable[tuple[
        Triple, dict[str, object] | None, dict[str, object] | None,
        dict[str, str] | None
    ]]:
        try:
            yield from executor.map(_evaluate_job, jobs, chunksize=32)
        finally:
            executor.shutdown(wait=True, cancel_futures=True)
    return results()


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, indent=2, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_gate(baseline_path: Path, sidecar_path: Path, output_dir: Path,
             *, mode: str, workers: int) -> tuple[dict[str, object], float]:
    started = time.perf_counter()
    integrity, expected_records, baseline_errors = validate_baseline(
        baseline_path, sidecar_path
    )
    anchors = run_anchor_checks()
    mismatches: list[dict[str, object]] = []
    for error in baseline_errors:
        mismatches.append({"kind": "baseline-integrity", "message": error})
    for anchor in anchors:
        if not anchor["pass"]:
            mismatches.append({
                "anchor": anchor,
                "kind": "anchor-failure",
            })

    structural_triples: list[Triple] = []
    actual_records: list[dict[str, object]] = []
    evaluation_errors = 0
    missing_count = 0
    extra_count = 0
    polynomial_mismatch_count = 0
    actual_digest: str | None = None

    # Fail closed: never use an untrusted baseline as the comparison oracle.
    if not baseline_errors and all(anchor["pass"] for anchor in anchors):
        scope = {"max_length": 5, "max_size": 7}
        structural_triples = enumerate_structural_triples(
            scope["max_length"], scope["max_size"]
        )
        expected_by_triple = {
            _record_triple(record): record for record in expected_records
        }
        evidence_by_triple: dict[Triple, dict[str, object]] = {}
        for triple, record, evidence, error in _evaluate_all(
            structural_triples, mode, workers
        ):
            if error is not None:
                evaluation_errors += 1
                mismatches.append({
                    "error": error,
                    "kind": "evaluation-error",
                    "triple": _triple_json(triple),
                })
                continue
            if record is not None:
                actual_records.append(record)
                if evidence is not None:
                    evidence_by_triple[triple] = evidence

        actual_records.sort(key=lambda record: triple_sort_key(_record_triple(record)))
        actual_by_triple = {
            _record_triple(record): record for record in actual_records
        }
        expected_set = set(expected_by_triple)
        actual_set = set(actual_by_triple)
        for triple in sorted(expected_set - actual_set, key=triple_sort_key):
            missing_count += 1
            mismatches.append({
                "expected": expected_by_triple[triple],
                "expected_record_sha256": record_hash(expected_by_triple[triple]),
                "kind": "missing-triple",
                "triple": _triple_json(triple),
            })
        for triple in sorted(actual_set - expected_set, key=triple_sort_key):
            extra_count += 1
            mismatches.append({
                "actual": actual_by_triple[triple],
                "actual_record_sha256": record_hash(actual_by_triple[triple]),
                "evidence": evidence_by_triple.get(triple),
                "kind": "extra-triple",
                "triple": _triple_json(triple),
            })
        for triple in sorted(expected_set & actual_set, key=triple_sort_key):
            expected_polynomial = expected_by_triple[triple]["poly"]
            actual_polynomial = actual_by_triple[triple]["poly"]
            if expected_polynomial != actual_polynomial:
                polynomial_mismatch_count += 1
                mismatches.append({
                    "actual": actual_polynomial,
                    "actual_record_sha256": record_hash(actual_by_triple[triple]),
                    "evidence": evidence_by_triple.get(triple),
                    "expected": expected_polynomial,
                    "expected_record_sha256": record_hash(expected_by_triple[triple]),
                    "kind": "polynomial-mismatch",
                    "triple": _triple_json(triple),
                })
        actual_digest = payload_hash(actual_records)

    mismatch_counts = {
        "anchor_failures": sum(item["kind"] == "anchor-failure"
                               for item in mismatches),
        "baseline_integrity_errors": sum(item["kind"] == "baseline-integrity"
                                         for item in mismatches),
        "evaluation_errors": evaluation_errors,
        "extra_triples": extra_count,
        "missing_triples": missing_count,
        "polynomial_mismatches": polynomial_mismatch_count,
    }
    status = "pass" if (
        not mismatches
        and len(actual_records) == EXPECTED_BASELINE_COUNT
        and actual_digest == EXPECTED_BASELINE_HASH
    ) else "fail"
    mismatch_document = {
        "gate": "P1_E1_BASELINE_PARITY",
        "items": sorted(mismatches, key=_mismatch_sort_key),
        "schema_version": SCHEMA_VERSION,
        "status": "empty" if not mismatches else "mismatches",
    }
    report: dict[str, object] = {
        "actual": {
            "record_count": len(actual_records),
            "triples_payload_sha256": actual_digest,
        },
        "anchors": anchors,
        "baseline_integrity": integrity,
        "canonicalization": {
            "name": "order-2 swap-only",
            "sort": "(len(nu), nu, lam, mu)",
            "version": CANONICALIZER_VERSION,
        },
        "comparison": {
            **mismatch_counts,
            "mismatch_bundle": "mismatches.json",
        },
        "enumeration": {
            "nonzero_triple_count": len(actual_records),
            "structural_candidate_count": len(structural_triples),
        },
        "evaluator": {
            "arithmetic": "exact integers + fractions.Fraction",
            "interpolation_mode": mode,
            "lrcalc_call": "lrcoef(out=nu, inn1=lam, inn2=mu)",
            "lrcalc_version": lrcalc_version(),
            "name": "lrcalc-interp",
            "python": platform.python_version(),
            "stability_policy": (
                "empirical top finite-difference stabilization within hive bound"
                if mode == "adaptive"
                else (
                    "fit N=0..B; verify N=B+1"
                    if mode == "bounded"
                    else "fit N=0..B; verify through N=2B+2 (2B+3 samples)"
                )
            ),
        },
        "expected": {
            "record_count": EXPECTED_BASELINE_COUNT,
            "scope": {"max_length": 5, "max_size": 7},
            "triples_payload_sha256": EXPECTED_BASELINE_HASH,
        },
        "gate": "P1_E1_BASELINE_PARITY",
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "workers": workers,
    }
    frontier_document = {
        "canonicalization": {
            "name": "order-2 swap-only",
            "sort": "(len(nu), nu, lam, mu)",
            "version": CANONICALIZER_VERSION,
        },
        "gate": "P1_E1_BASELINE_PARITY",
        "record_count": len(actual_records),
        "schema_version": SCHEMA_VERSION,
        "triples": actual_records,
        "triples_payload_sha256": actual_digest,
    }
    frontier_path = output_dir / "actual_frontier.json"
    mismatch_path = output_dir / "mismatches.json"
    report_path = output_dir / "parity_report.json"
    _atomic_json(frontier_path, frontier_document)
    _atomic_json(mismatch_path, mismatch_document)
    _atomic_json(report_path, report)
    manifest = {
        "artifacts": [
            {
                "bytes": frontier_path.stat().st_size,
                "path": frontier_path.name,
                "sha256": _file_sha256(frontier_path),
            },
            {
                "bytes": report_path.stat().st_size,
                "path": report_path.name,
                "sha256": _file_sha256(report_path),
            },
            {
                "bytes": mismatch_path.stat().st_size,
                "path": mismatch_path.name,
                "sha256": _file_sha256(mismatch_path),
            },
        ],
        "gate": "P1_E1_BASELINE_PARITY",
        "schema_version": SCHEMA_VERSION,
    }
    _atomic_json(output_dir / "artifact_manifest.json", manifest)
    return report, time.perf_counter() - started


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline", type=Path, default=DEFAULT_BASELINE,
        help="immutable dry-run baseline JSON (read only)",
    )
    parser.add_argument(
        "--sidecar", type=Path, default=DEFAULT_SIDECAR,
        help="canonical triples-payload SHA-256 sidecar (read only)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=DEFAULT_OUTPUT,
        help="directory for deterministic gate artifacts",
    )
    parser.add_argument(
        "--mode", choices=("adaptive", "bounded", "conservative"),
        default="adaptive",
        help=(
            "adaptive is baseline/search parity; conservative is the N=0..2B+2 "
            "candidate-verification policy"
        ),
    )
    parser.add_argument(
        "--workers", type=int, default=1,
        help="number of deterministic process workers (default: 1)",
    )
    arguments = parser.parse_args(argv)
    if arguments.workers < 1:
        parser.error("--workers must be at least 1")
    return arguments


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    report, elapsed = run_gate(
        arguments.baseline,
        arguments.sidecar,
        arguments.output_dir,
        mode=arguments.mode,
        workers=arguments.workers,
    )
    print(
        f"E1 parity {report['status']}: "
        f"{report['actual']['record_count']} records, "
        f"payload={report['actual']['triples_payload_sha256']}, "
        f"elapsed={elapsed:.3f}s",
        file=sys.stderr,
    )
    print(arguments.output_dir / "parity_report.json")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
