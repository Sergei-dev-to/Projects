#!/usr/bin/env python3
"""Fixed-seed regression checks for detachment diagnostics."""
from __future__ import annotations

from sector_detachment_diagnostics import Params, build_transition, diagnostics


def assert_close(name: str, actual: float, expected: float, tol: float = 5e-4) -> None:
    if abs(actual - expected) > tol:
        raise AssertionError(f"{name}: expected {expected:.8g}, got {actual:.8g}")


def run_case(operator: str, bandwidth: float, expected: dict[str, float]) -> None:
    params = Params(n=8, q=2, operator=operator, bandwidth=bandwidth, seed=2468)
    d, eval_high, eval_low_tiled, labels = build_transition(params)
    diag = diagnostics(params, d, eval_high, eval_low_tiled, labels)
    for key, value in expected.items():
        assert_close(f"{operator}:{key}", float(diag[key]), value)


def main() -> None:
    run_case(
        "local",
        0.25,
        {
            "spectral_participation_norm": 0.780278,
            "channel_gram_participation_norm": 0.972194,
            "initial_gram_participation_norm": 0.972194,
            "accessible_record_gram_participation_norm": 0.999939,
            "accessible_record_width_participation_norm": 1.0,
            "c_long_mean": 0.00379586,
        },
    )
    run_case(
        "aligned",
        0.25,
        {
            "spectral_participation_norm": 0.789028,
            "channel_gram_participation_norm": 0.00391443,
            "initial_gram_participation_norm": 0.00391443,
            "accessible_record_gram_participation_norm": 0.5,
            "accessible_record_width_participation_norm": 1.0,
            "largest_channel_width_fraction": 0.998954,
        },
    )
    print("detachment diagnostics regression passed")


if __name__ == "__main__":
    main()
