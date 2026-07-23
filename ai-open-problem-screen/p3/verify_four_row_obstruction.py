"""Reproduce the finite normal-minor certificate used by the four-row theorem.

This verifier is deliberately standard-library-only and independent of the LR
counter. It regenerates the side-four rhombus rows from the triangular geometry,
enumerates all 816 three-row minors, checks the preregistered census, and emits a
canonical semantic certificate.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import gcd
import argparse
import hashlib
import json
from typing import Iterable


Coord = tuple[int, int]
Row = tuple[int, int, int]

N = 4
VARIABLES: tuple[Coord, ...] = ((1, 1), (1, 2), (2, 1))
DIRECTIONS: tuple[tuple[str, Coord, Coord], ...] = (
    ("east_north", (1, 0), (0, 1)),
    ("north_northwest", (0, 1), (-1, 1)),
    ("northwest_west", (-1, 1), (-1, 0)),
)

EXPECTED_ABS_COUNTS = {0: 299, 1: 468, 2: 48, 4: 1}
EXPECTED_UNIQUE_MAX = frozenset(
    {
        (1, 1, -1),
        (1, -1, 1),
        (-1, 1, 1),
    }
)


def add(*coords: Coord) -> Coord:
    return (sum(coord[0] for coord in coords), sum(coord[1] for coord in coords))


def rhombus_bases(family: str) -> Iterable[Coord]:
    if family == "east_north":
        for i in range(N - 1):
            for j in range(N - 1 - i):
                yield (i, j)
        return
    if family == "north_northwest":
        for i in range(1, N):
            for j in range(N - i):
                yield (i, j)
        return
    if family == "northwest_west":
        for i in range(2, N + 1):
            for j in range(N - i + 1):
                yield (i, j)
        return
    raise AssertionError(f"unknown rhombus family: {family}")


def vertex_row(coord: Coord) -> Row:
    i, j = coord
    if i < 0 or j < 0 or i + j > N:
        raise AssertionError(f"coordinate outside hive triangle: {coord}")
    if coord not in VARIABLES:
        return (0, 0, 0)
    index = VARIABLES.index(coord)
    return tuple(1 if k == index else 0 for k in range(3))  # type: ignore[return-value]


def combine(positive: tuple[Coord, Coord], negative: tuple[Coord, Coord]) -> Row:
    values = [0, 0, 0]
    for coord in positive:
        row = vertex_row(coord)
        for index, value in enumerate(row):
            values[index] += value
    for coord in negative:
        row = vertex_row(coord)
        for index, value in enumerate(row):
            values[index] -= value
    return tuple(values)  # type: ignore[return-value]


def generate_rows() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for family, direction_a, direction_b in DIRECTIONS:
        for base in rhombus_bases(family):
            row = combine(
                (add(base, direction_a), add(base, direction_b)),
                (base, add(base, direction_a, direction_b)),
            )
            records.append({"family": family, "base": list(base), "row": list(row)})
    return records


def determinant(rows: tuple[Row, Row, Row]) -> int:
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")


def build_certificate() -> dict[str, object]:
    row_records = generate_rows()
    rows = [tuple(record["row"]) for record in row_records]

    if len(rows) != 18:
        raise AssertionError(f"expected 18 rhombus rows, got {len(rows)}")
    if any(row == (0, 0, 0) for row in rows):
        raise AssertionError("unexpected zero rhombus row")
    if any(gcd(gcd(abs(row[0]), abs(row[1])), abs(row[2])) != 1 for row in rows):
        raise AssertionError("all rhombus rows must be primitive")

    counts: Counter[int] = Counter()
    max_triples: list[dict[str, object]] = []
    for indices in combinations(range(len(rows)), 3):
        chosen = tuple(rows[index] for index in indices)
        value = determinant(chosen)  # type: ignore[arg-type]
        magnitude = abs(value)
        counts[magnitude] += 1
        if magnitude == 4:
            max_triples.append(
                {
                    "indices": list(indices),
                    "rows": [list(row) for row in chosen],
                    "determinant": value,
                }
            )

    if dict(sorted(counts.items())) != EXPECTED_ABS_COUNTS:
        raise AssertionError(f"minor census mismatch: {dict(sorted(counts.items()))}")
    if sum(counts.values()) != 816:
        raise AssertionError(f"expected 816 minors, got {sum(counts.values())}")
    if len(max_triples) != 1:
        raise AssertionError(f"expected one magnitude-four triple, got {len(max_triples)}")
    unique_rows = frozenset(tuple(row) for row in max_triples[0]["rows"])
    if unique_rows != EXPECTED_UNIQUE_MAX:
        raise AssertionError(f"wrong magnitude-four triple: {sorted(unique_rows)}")

    payload: dict[str, object] = {
        "schema_version": 1,
        "hive_side": N,
        "variables": [list(coord) for coord in VARIABLES],
        "row_count": len(rows),
        "rows": row_records,
        "minor_count": sum(counts.values()),
        "absolute_determinant_counts": {
            str(key): value for key, value in sorted(counts.items())
        },
        "unique_absolute_determinant_four": max_triples[0],
    }
    return {
        **payload,
        "certificate_sha256": hashlib.sha256(canonical_bytes(payload)).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretty", action="store_true", help="indent the JSON output")
    args = parser.parse_args()
    certificate = build_certificate()
    if args.pretty:
        print(json.dumps(certificate, sort_keys=True, indent=2))
    else:
        print(canonical_bytes(certificate).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
