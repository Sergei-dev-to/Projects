"""Exact N=1 nonzero-frontier counts for bounded planning boxes.

This is a cost-estimation pass, not a stretched-polynomial scan and not a P2
completion certificate.  For each unordered ``(lambda, mu)`` pair, lrcalc's
Schur-product enumerator returns exactly the outer partitions with positive LR
coefficient.  Counting those dictionary keys therefore gives the swap-only
canonical nonzero count at N=1.  Saturation makes this the correct support for a
later stretch scan, but no Ehrhart coefficients are computed here.
"""

from __future__ import annotations

import argparse
from collections import Counter
from importlib.metadata import version
import json
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import lrcalc

try:
    from .estimate_boxes import BOXES, partitions_upto, unordered_pair_count
except ImportError:
    from estimate_boxes import BOXES, partitions_upto, unordered_pair_count  # type: ignore


Partition = tuple[int, ...]
Multiplier = Callable[[Sequence[int], Sequence[int], int], Mapping[Partition, int]]

PLANNING_BOXES = {"B0-7": (6, 7), **BOXES}


def _contains(outer: Partition, inner: Partition) -> bool:
    return all(part <= (outer[index] if index < len(outer) else 0)
               for index, part in enumerate(inner))


def _lrcalc_product(
    lam: Sequence[int], mu: Sequence[int], rows: int
) -> Mapping[Partition, int]:
    return lrcalc.mult(list(lam), list(mu), rows=rows)


def count_box(
    name: str,
    rows: int,
    size: int,
    *,
    multiplier: Multiplier = _lrcalc_product,
) -> dict[str, Any]:
    """Return an exact, deterministic support summary for one finite box."""

    partitions = partitions_upto(rows, size)
    nonzero_count = 0
    coefficient_sum_at_one = 0
    maximum_lr_at_one = 0
    maximum_outputs_per_pair = 0
    output_length_counts: Counter[int] = Counter()

    for index, lam in enumerate(partitions):
        for mu in partitions[index:]:
            outputs = multiplier(lam, mu, rows)
            if not isinstance(outputs, Mapping):
                raise TypeError("lrcalc product result must be a mapping")
            maximum_outputs_per_pair = max(maximum_outputs_per_pair, len(outputs))
            target_weight = sum(lam) + sum(mu)
            for raw_nu, coefficient in outputs.items():
                nu = tuple(raw_nu)
                if (
                    not nu
                    and target_weight != 0
                    or any(isinstance(part, bool) or not isinstance(part, int) or part <= 0
                           for part in nu)
                    or any(nu[i] < nu[i + 1] for i in range(len(nu) - 1))
                    or len(nu) > rows
                    or sum(nu) != target_weight
                    or not _contains(nu, lam)
                    or not _contains(nu, mu)
                ):
                    raise ValueError(
                        f"invalid outer partition {raw_nu!r} for {lam!r}, {mu!r}"
                    )
                if (
                    isinstance(coefficient, bool)
                    or not isinstance(coefficient, int)
                    or coefficient <= 0
                ):
                    raise ValueError(
                        f"invalid LR coefficient {coefficient!r} for {lam!r}, {mu!r}, {nu!r}"
                    )
                nonzero_count += 1
                coefficient_sum_at_one += coefficient
                maximum_lr_at_one = max(maximum_lr_at_one, coefficient)
                output_length_counts[len(nu)] += 1

    return {
        "box": name,
        "max_length": rows,
        "max_size_each_of_lam_mu": size,
        "partition_count": len(partitions),
        "unordered_pair_count": unordered_pair_count(len(partitions)),
        "nonzero_canonical_triples_at_n1": nonzero_count,
        "sum_of_lr_coefficients_at_n1": coefficient_sum_at_one,
        "maximum_lr_coefficient_at_n1": maximum_lr_at_one,
        "maximum_nonzero_outputs_for_one_pair": maximum_outputs_per_pair,
        "nonzero_count_by_outer_length": {
            str(length): output_length_counts[length]
            for length in sorted(output_length_counts)
        },
        "canonicalization": "swap-only-order2",
        "method": "exact lrcalc.mult Schur-product support enumeration at N=1",
        "scope_guard": (
            "planning support count only; no stretched polynomials or Normaliz "
            "evaluations; not a completed P2 box"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--boxes",
        nargs="+",
        choices=tuple(PLANNING_BOXES),
        default=["B0-7", "B1"],
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    report = {
        "schema_version": "lr-lrcalc-support-counts/v1",
        "lrcalc_version": version("lrcalc"),
        "boxes": [
            count_box(name, *PLANNING_BOXES[name])
            for name in args.boxes
        ],
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_name(f".{args.output.name}.tmp")
        temporary.write_text(rendered, encoding="utf-8", newline="\n")
        temporary.replace(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
