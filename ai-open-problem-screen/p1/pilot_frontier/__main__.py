"""Command-line interface for the scientific pilot frontier runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .runner import (
    B0_7_EXPECTED_STRUCTURAL_COUNT,
    FrontierError,
    authorize_run,
    initialize_run,
    run_frontier,
    status,
    verify_run,
)


def _print(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a real, crash-safe, dual-evaluator LR pilot (never outcome B)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="write/verify an immutable structural plan")
    init.add_argument("--work-dir", type=Path, required=True)
    init.add_argument("--max-length", type=int, required=True)
    init.add_argument("--max-size", type=int, required=True)
    init.add_argument("--chunk-size", type=int, default=32)
    init.add_argument("--champion-limit", type=int, default=100)
    init.add_argument("--expect-count", type=int)
    init.add_argument(
        "--b0-7",
        action="store_true",
        help="require exactly the B0-7 scope (length<=6,size<=7,count=18287)",
    )

    authorize = subparsers.add_parser(
        "authorize", help="validate and freeze a passing P1 gate before evaluation"
    )
    authorize.add_argument("--work-dir", type=Path, required=True)
    authorize.add_argument("--gate-report", type=Path, required=True)
    authorize.add_argument("--evidence-manifest", type=Path, required=True)
    authorize.add_argument("--evidence-root", type=Path, required=True)
    authorize.add_argument(
        "--confirm-p1-passed",
        action="store_true",
        help="explicit operator confirmation required for authorization",
    )

    run = subparsers.add_parser("run", help="run/resume authorized immutable chunks")
    run.add_argument("--work-dir", type=Path, required=True)
    run.add_argument(
        "--max-chunks",
        type=int,
        help="intentional bounded stop after this many new chunks; omit to finish",
    )

    show = subparsers.add_parser("status", help="verify the durable prefix")
    show.add_argument("--work-dir", type=Path, required=True)
    show.add_argument("--repair-checkpoint", action="store_true")

    verify = subparsers.add_parser("verify", help="verify all hashes and completion")
    verify.add_argument("--work-dir", type=Path, required=True)
    verify.add_argument("--allow-partial", action="store_true")

    args = parser.parse_args()
    try:
        if args.command == "init":
            expected = args.expect_count
            if args.b0_7:
                if (args.max_length, args.max_size) != (6, 7):
                    raise FrontierError("--b0-7 requires --max-length 6 --max-size 7")
                if expected not in (None, B0_7_EXPECTED_STRUCTURAL_COUNT):
                    raise FrontierError("--b0-7 conflicts with --expect-count")
                expected = B0_7_EXPECTED_STRUCTURAL_COUNT
            result = initialize_run(
                args.work_dir,
                maximum_length=args.max_length,
                maximum_size=args.max_size,
                chunk_size=args.chunk_size,
                champion_limit=args.champion_limit,
                expected_structural_count=expected,
            )
        elif args.command == "authorize":
            result = authorize_run(
                args.work_dir,
                gate_report_path=args.gate_report,
                evidence_manifest_path=args.evidence_manifest,
                evidence_root=args.evidence_root,
                explicit_confirmation=args.confirm_p1_passed,
            )
        elif args.command == "run":
            result = run_frontier(args.work_dir, max_chunks=args.max_chunks)
        elif args.command == "status":
            result = status(args.work_dir, repair_checkpoint=args.repair_checkpoint)
        else:
            result = verify_run(args.work_dir, require_complete=not args.allow_partial)
    except FrontierError as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    _print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
