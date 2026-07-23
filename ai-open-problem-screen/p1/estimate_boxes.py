"""Deterministic pre-oracle size estimates for the preregistered P2 boxes.

This counts *support-compatible* triples only: unordered ``(lam, mu)`` pairs and
partitions ``nu`` with the required weight and diagram containment.  It does not
apply Horn inequalities or evaluate an LR coefficient, so its triple count is an
upper bound on the nonzero frontier and must never be reported as an evaluated
or certified count.

Small boxes are counted exactly.  If a box has more than ``--exact-max-pairs``
unordered pairs, pairs are sampled uniformly from the triangular index set with
the campaign seed and a normal-approximation confidence interval is reported.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from functools import lru_cache
import json
import math
import random
from statistics import fmean, stdev
from typing import Iterable


BOXES = {
    "B1": (6, 12),
    "B2": (6, 20),
    "B3": (7, 16),
    "B4": (7, 30),
}


def partitions_upto(max_len: int, max_size: int) -> list[tuple[int, ...]]:
    """Return every positive-part partition in the finite box, including ()."""
    result: list[tuple[int, ...]] = []

    def visit(remaining: int, ceiling: int, current: list[int]) -> None:
        result.append(tuple(current))
        if len(current) == max_len:
            return
        for part in range(min(ceiling, remaining), 0, -1):
            current.append(part)
            visit(remaining - part, part, current)
            current.pop()

    visit(max_size, max_size, [])
    # The recursive tree reaches each partition once, but keep the invariant
    # executable in case this generator is changed later.
    assert len(result) == len(set(result))
    return result


def _padded(part: tuple[int, ...], rows: int) -> tuple[int, ...]:
    return part + (0,) * (rows - len(part))


@lru_cache(maxsize=None)
def count_nu(
    lower: tuple[int, ...], target_weight: int
) -> int:
    """Count partitions of ``target_weight`` componentwise above ``lower``."""
    rows = len(lower)

    @lru_cache(maxsize=None)
    def rec(position: int, previous: int, remaining: int) -> int:
        if position == rows:
            return int(remaining == 0)
        minimum = lower[position]
        # Leave at least the componentwise lower bound for later rows.
        later_minimum = sum(lower[position + 1 :])
        maximum = min(previous, remaining - later_minimum)
        if maximum < minimum:
            return 0
        total = 0
        for value in range(minimum, maximum + 1):
            total += rec(position + 1, value, remaining - value)
        return total

    return rec(0, target_weight, target_weight)


def compatible_nu_count(
    lam: tuple[int, ...], mu: tuple[int, ...], rows: int
) -> int:
    lp, mp = _padded(lam, rows), _padded(mu, rows)
    lower = tuple(max(a, b) for a, b in zip(lp, mp))
    return count_nu(lower, sum(lam) + sum(mu))


def unordered_pair_count(n: int) -> int:
    return n * (n + 1) // 2


def iter_unordered_pairs(
    parts: list[tuple[int, ...]],
) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    for i, lam in enumerate(parts):
        for mu in parts[i:]:
            yield lam, mu


def _row_starts(n: int) -> list[int]:
    # Row i contains triangular indices for (i,j), j=i..n-1.
    starts = [0]
    for i in range(n):
        starts.append(starts[-1] + n - i)
    return starts


def unrank_pair(index: int, n: int, starts: list[int]) -> tuple[int, int]:
    if not 0 <= index < starts[-1]:
        raise IndexError(index)
    i = bisect_right(starts, index) - 1
    return i, i + index - starts[i]


def estimate_box(
    name: str,
    rows: int,
    size: int,
    *,
    exact_max_pairs: int,
    samples: int,
    seed: int,
) -> dict[str, object]:
    parts = partitions_upto(rows, size)
    pair_count = unordered_pair_count(len(parts))
    base: dict[str, object] = {
        "box": name,
        "max_length": rows,
        "max_size_each_of_lam_mu": size,
        "partition_count": len(parts),
        "unordered_pair_count": pair_count,
        "quantity": "support-compatible triple upper bound before LR/Horn tests",
    }
    if pair_count <= exact_max_pairs:
        total = sum(compatible_nu_count(a, b, rows) for a, b in iter_unordered_pairs(parts))
        return base | {
            "method": "exact",
            "support_compatible_triples": total,
        }

    rng = random.Random(seed)
    starts = _row_starts(len(parts))
    values: list[int] = []
    for _ in range(samples):
        i, j = unrank_pair(rng.randrange(pair_count), len(parts), starts)
        values.append(compatible_nu_count(parts[i], parts[j], rows))
    mean = fmean(values)
    standard_error = stdev(values) / math.sqrt(len(values)) if len(values) > 1 else 0.0
    low_mean = max(0.0, mean - 1.96 * standard_error)
    high_mean = mean + 1.96 * standard_error
    return base | {
        "method": "uniform-unordered-pair-sample",
        "seed": seed,
        "samples": samples,
        "mean_compatible_nu_per_pair": mean,
        "sample_standard_error": standard_error,
        "estimated_support_compatible_triples": round(pair_count * mean),
        "approx_95pct_interval": [
            round(pair_count * low_mean),
            round(pair_count * high_mean),
        ],
        "caveat": "normal-approximation sampling interval, not a completeness certificate",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-max-pairs", type=int, default=1_500_000)
    parser.add_argument("--samples", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260723)
    parser.add_argument("--output")
    args = parser.parse_args()
    report = {
        "schema_version": 1,
        "estimator": "p1/estimate_boxes.py",
        "boxes": [
            estimate_box(
                name,
                rows,
                size,
                exact_max_pairs=args.exact_max_pairs,
                samples=args.samples,
                seed=args.seed + index,
            )
            for index, (name, (rows, size)) in enumerate(BOXES.items())
        ],
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        # This script intentionally writes only an explicitly named report.
        with open(args.output, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
