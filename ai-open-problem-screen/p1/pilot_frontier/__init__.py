"""Crash-safe scientific pilot frontier runner.

This package is deliberately separate from :mod:`p1.control.pilot`: the latter
tests orchestration with toy payloads, while this package evaluates real LR
triples through the production E1 lrcalc evaluator.
"""

from .runner import (
    B0_7_EXPECTED_STRUCTURAL_COUNT,
    FrontierError,
    authorize_run,
    initialize_run,
    run_frontier,
    status,
    verify_run,
)

__all__ = [
    "B0_7_EXPECTED_STRUCTURAL_COUNT",
    "FrontierError",
    "authorize_run",
    "initialize_run",
    "run_frontier",
    "status",
    "verify_run",
]
