"""Exact lrcalc + rational-interpolation evaluator used by the P1 gate.

The lrcalc extension's positional convention is::

    lrcalc.lrcoef(out, inn1, inn2)

Thus ``c^nu_{lam,mu}`` is evaluated as ``lrcoef(nu, lam, mu)``.  This module
keeps that convention in one small wrapper and checks it with asymmetric
anchors in :func:`run_anchor_checks`.

There are three interpolation modes:

``adaptive``
    Matches the dry-run/search policy: grow a consecutive prefix until a top
    finite-difference level vanishes, with the hive dimension bound as a hard
    guard.  This is an empirical stability check, not candidate certification.

``bounded``
    Fit at ``N=0..B`` where ``B`` is the hive dimension upper bound and verify
    at the extra point ``N=B+1``.

``conservative``
    Fit at ``N=0..B`` and verify every point through ``N=2B+2``.  It uses
    ``2B+3`` samples (for rows <= 7 this is at most N=0..32) and is the mode
    intended for final candidate verification.

All interpolation and comparison arithmetic is exact ``fractions.Fraction``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version as package_version
import operator
from typing import Callable, Iterable, Sequence

import lrcalc


Partition = tuple[int, ...]
Triple = tuple[Partition, Partition, Partition]
Polynomial = tuple[Fraction, ...]
Counter = Callable[[Partition, Partition, Partition], int]


class EvaluationError(RuntimeError):
    """Base class for deterministic E1 evaluation failures."""


class DegreeBoundError(EvaluationError):
    """Raised when the inferred polynomial exceeds the hive dimension bound."""


class StabilityError(EvaluationError):
    """Raised when sampled values do not pass the requested stability check."""


@dataclass(frozen=True)
class Evaluation:
    polynomial: Polynomial
    values: tuple[int, ...]
    degree_bound: int
    inferred_degree: int
    mode: str
    fit_max_n: int
    checked_max_n: int

    def polynomial_strings(self) -> list[str]:
        """Return canonical monomial coefficients, constant term first."""

        return [str(value) for value in self.polynomial]

    def evidence(self) -> dict[str, object]:
        """Return a JSON-safe deterministic evaluation trace."""

        return {
            "checked_max_n": self.checked_max_n,
            "degree_bound": self.degree_bound,
            "fit_max_n": self.fit_max_n,
            "inferred_degree": self.inferred_degree,
            "mode": self.mode,
            "polynomial": self.polynomial_strings(),
            "values": list(self.values),
        }


def normalize_partition(parts: Iterable[int]) -> Partition:
    """Validate and normalize a partition to a tuple of positive integers."""

    normalized: list[int] = []
    for part in parts:
        if isinstance(part, bool):
            raise ValueError("boolean values are not partition parts")
        try:
            normalized.append(operator.index(part))
        except TypeError as exc:
            raise ValueError(f"partition part is not an integer: {part!r}") from exc
    partition = tuple(normalized)
    if any(part <= 0 for part in partition):
        raise ValueError(f"partition parts must be positive: {partition!r}")
    if any(partition[index] < partition[index + 1]
           for index in range(len(partition) - 1)):
        raise ValueError(f"partition must be weakly decreasing: {partition!r}")
    return partition


def scale(partition: Partition, factor: int) -> Partition:
    """Dilate a partition, with scale-by-zero normalized to the empty one."""

    if factor < 0:
        raise ValueError("scale factor must be nonnegative")
    if factor == 0:
        return ()
    return tuple(factor * part for part in partition)


def contains(outer: Partition, inner: Partition) -> bool:
    """Return whether ``inner`` is contained in ``outer`` as Young diagrams."""

    return (len(inner) <= len(outer)
            and all(inner[index] <= outer[index]
                    for index in range(len(inner))))


def canonical_triple(lam: Iterable[int], mu: Iterable[int],
                     nu: Iterable[int]) -> Triple:
    """Return the baseline's only sound canonicalization: swap-only, order 2."""

    left = normalize_partition(lam)
    right = normalize_partition(mu)
    outer = normalize_partition(nu)
    if right < left:
        left, right = right, left
    return left, right, outer


def triple_sort_key(triple: Triple) -> tuple[object, ...]:
    """Ordering used by ``dryrun/baseline.py`` and its canonical payload."""

    lam, mu, nu = triple
    return len(nu), nu, lam, mu


def hive_dimension_bound(rows: int) -> int:
    """Ambient hive dimension bound ``(rows-1)(rows-2)/2``."""

    if rows < 0:
        raise ValueError("row count must be nonnegative")
    return ((rows - 1) * (rows - 2) // 2) if rows >= 2 else 0


def lrcalc_version() -> str:
    """Return the installed Python distribution version."""

    try:
        return package_version("lrcalc")
    except PackageNotFoundError:
        return "unknown"


def lr_coefficient(lam: Iterable[int], mu: Iterable[int],
                   nu: Iterable[int]) -> int:
    """Compute ``c^nu_{lam,mu}`` exactly using lrcalc 2.1.

    Invalid size/containment cases are returned as zero without calling the C
    extension.  The sole extension call is deliberately written with keywords
    echoed in the local names to make its positional convention hard to invert.
    """

    inn1 = normalize_partition(lam)
    inn2 = normalize_partition(mu)
    out = normalize_partition(nu)
    if sum(inn1) + sum(inn2) != sum(out):
        return 0
    if not contains(out, inn1) or not contains(out, inn2):
        return 0
    result = lrcalc.lrcoef(list(out), list(inn1), list(inn2))
    if not isinstance(result, int) or result < 0:
        raise EvaluationError(f"lrcalc returned a non-count: {result!r}")
    return result


def _difference_rows(values: Sequence[int | Fraction]) -> list[list[Fraction]]:
    if not values:
        raise ValueError("at least one value is required")
    rows = [[Fraction(value) for value in values]]
    while len(rows[-1]) > 1:
        previous = rows[-1]
        rows.append([previous[index + 1] - previous[index]
                     for index in range(len(previous) - 1)])
    return rows


def _poly_add(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    size = max(len(left), len(right))
    return [
        (left[index] if index < len(left) else Fraction(0))
        + (right[index] if index < len(right) else Fraction(0))
        for index in range(size)
    ]


def _poly_multiply(left: list[Fraction],
                   right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return result


def _trim(polynomial: list[Fraction]) -> Polynomial:
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return tuple(polynomial)


def polynomial_from_consecutive_values(
    values: Sequence[int | Fraction],
    maximum_degree: int | None = None,
) -> Polynomial:
    """Interpolate values at ``N=0,1,...`` in the monomial basis.

    When ``maximum_degree`` is supplied, only the first
    ``maximum_degree + 1`` Newton coefficients are used.  All supplied values
    are then exact hold-outs and must agree with that bounded-degree polynomial.
    """

    if not values:
        raise ValueError("at least one value is required")
    if maximum_degree is None:
        degree_limit = len(values) - 1
    else:
        if maximum_degree < 0:
            raise ValueError("maximum degree must be nonnegative")
        if len(values) < maximum_degree + 1:
            raise ValueError(
                f"need at least {maximum_degree + 1} values for degree bound "
                f"{maximum_degree}"
            )
        degree_limit = maximum_degree

    rows = _difference_rows(values)
    polynomial = [Fraction(0)]
    falling_factorial = [Fraction(1)]
    factorial = 1
    for degree in range(degree_limit + 1):
        if degree:
            falling_factorial = _poly_multiply(
                falling_factorial,
                [Fraction(-(degree - 1)), Fraction(1)],
            )
            factorial *= degree
        coefficient = rows[degree][0] / factorial
        term = [coefficient * value for value in falling_factorial]
        polynomial = _poly_add(polynomial, term)

    result = _trim(polynomial)
    for point, expected in enumerate(values):
        actual = evaluate_polynomial(result, point)
        if actual != Fraction(expected):
            raise StabilityError(
                f"degree-{degree_limit} interpolation fails at N={point}: "
                f"expected {expected}, got {actual}"
            )
    return result


def stabilized_polynomial(values: Sequence[int | Fraction]) -> Polynomial | None:
    """Return the minimal polynomial once the sampled top difference is zero."""

    rows = _difference_rows(values)
    if len(rows) == 1 or rows[-1][0] != 0:
        return None
    degree = max(
        (index for index, row in enumerate(rows) if any(value != 0 for value in row)),
        default=0,
    )
    return polynomial_from_consecutive_values(values, maximum_degree=degree)


def evaluate_polynomial(polynomial: Sequence[Fraction], point: int) -> Fraction:
    """Evaluate a low-to-high monomial polynomial exactly by Horner's rule."""

    result = Fraction(0)
    for coefficient in reversed(polynomial):
        result = result * point + coefficient
    return result


def canonical_polynomial_strings(polynomial: Sequence[Fraction]) -> list[str]:
    """Serialize reduced rational coefficients in low-to-high degree order."""

    if not polynomial:
        raise ValueError("polynomial coefficient list cannot be empty")
    normalized = _trim([Fraction(value) for value in polynomial])
    return [str(value) for value in normalized]


def evaluate_stretched(
    lam: Iterable[int],
    mu: Iterable[int],
    nu: Iterable[int],
    *,
    mode: str = "adaptive",
    counter: Counter = lr_coefficient,
    known_n1: int | None = None,
) -> Evaluation:
    """Evaluate the stretched LR polynomial in the requested stability mode."""

    left, right, outer = canonical_triple(lam, mu, nu)
    if sum(left) + sum(right) != sum(outer):
        raise EvaluationError("partition sizes do not satisfy |lam|+|mu|=|nu|")
    bound = hive_dimension_bound(len(outer))
    cache: dict[int, int] = {}
    if known_n1 is not None:
        cache[1] = int(known_n1)

    def value(point: int) -> int:
        if point not in cache:
            count = counter(
                scale(left, point), scale(right, point), scale(outer, point)
            )
            if not isinstance(count, int) or count < 0:
                raise EvaluationError(f"counter returned a non-count: {count!r}")
            cache[point] = count
        return cache[point]

    if value(1) == 0:
        raise EvaluationError(
            "unstretched coefficient is zero; saturation excludes this triple"
        )

    if mode == "adaptive":
        cap = 2 * bound + 4
        sample_count = min(6, cap)
        while True:
            values = tuple(value(point) for point in range(sample_count))
            polynomial = stabilized_polynomial(values)
            if polynomial is not None:
                inferred_degree = len(polynomial) - 1
                if inferred_degree > bound:
                    raise DegreeBoundError(
                        f"inferred degree {inferred_degree} exceeds hive bound {bound}"
                    )
                return Evaluation(
                    polynomial=polynomial,
                    values=values,
                    degree_bound=bound,
                    inferred_degree=inferred_degree,
                    mode=mode,
                    fit_max_n=inferred_degree,
                    checked_max_n=sample_count - 1,
                )
            if sample_count >= cap:
                raise StabilityError(
                    f"no stabilized polynomial through N={sample_count - 1}; "
                    f"adaptive cap is {cap} samples for degree bound {bound}"
                )
            sample_count = min(sample_count + 2, cap)

    if mode == "bounded":
        checked_max_n = bound + 1
    elif mode == "conservative":
        checked_max_n = 2 * bound + 2
    else:
        raise ValueError(
            f"unknown interpolation mode {mode!r}; expected adaptive, bounded, "
            "or conservative"
        )

    values = tuple(value(point) for point in range(checked_max_n + 1))
    polynomial = polynomial_from_consecutive_values(values, maximum_degree=bound)
    inferred_degree = len(polynomial) - 1
    if inferred_degree > bound:
        raise DegreeBoundError(
            f"inferred degree {inferred_degree} exceeds hive bound {bound}"
        )
    return Evaluation(
        polynomial=polynomial,
        values=values,
        degree_bound=bound,
        inferred_degree=inferred_degree,
        mode=mode,
        fit_max_n=bound,
        checked_max_n=checked_max_n,
    )


@lru_cache(maxsize=None)
def _partitions_exact_cached(total: int, maximum_part: int,
                             slots: int) -> tuple[Partition, ...]:
    if total == 0:
        return ((),)
    if slots == 0 or maximum_part == 0:
        return ()
    result: list[Partition] = []
    for first in range(min(total, maximum_part), 0, -1):
        for suffix in _partitions_exact_cached(total - first, first, slots - 1):
            result.append((first,) + suffix)
    return tuple(result)


def partitions_exact(total: int, maximum_length: int) -> tuple[Partition, ...]:
    """Enumerate all partitions of an exact size with bounded length."""

    if total < 0 or maximum_length < 0:
        raise ValueError("partition size and maximum length must be nonnegative")
    return _partitions_exact_cached(total, total, maximum_length)


def partitions_upto(maximum_length: int, maximum_size: int) -> tuple[Partition, ...]:
    """Enumerate the same finite partition set used by the dry-run baseline."""

    if maximum_length < 0 or maximum_size < 0:
        raise ValueError("partition bounds must be nonnegative")
    return tuple(
        partition
        for size in range(maximum_size + 1)
        for partition in partitions_exact(size, maximum_length)
    )


def enumerate_structural_triples(maximum_length: int,
                                 maximum_size: int) -> list[Triple]:
    """Enumerate canonical triples before the lrcalc nonzero filter.

    Both inner partitions independently satisfy the size and length bounds.
    The final sort key is byte-for-byte compatible with ``baseline.py``'s
    canonical payload order.
    """

    inner_partitions = partitions_upto(maximum_length, maximum_size)
    triples: list[Triple] = []
    for left in inner_partitions:
        for right in inner_partitions:
            if right < left:
                continue
            total = sum(left) + sum(right)
            for outer in partitions_exact(total, maximum_length):
                if contains(outer, left) and contains(outer, right):
                    triples.append((left, right, outer))
    triples.sort(key=triple_sort_key)
    return triples


DEGREE_SIX_PARTITIONS: Triple = (
    (4, 3, 2, 1),
    (4, 3, 2, 1),
    (6, 5, 4, 3, 2),
)
DEGREE_SIX_POLYNOMIAL: Polynomial = tuple(map(Fraction, (
    "1", "13/4", "37/8", "4", "9/4", "3/4", "1/8",
)))


def run_anchor_checks() -> list[dict[str, object]]:
    """Run deterministic anchors that pin lrcalc's argument convention."""

    # These two calls deliberately bypass lr_coefficient's validity guards: the
    # asymmetric pair proves the extension itself is being called in the
    # documented (out, inn1, inn2) order.
    raw_order_anchors = [
        (
            "asymmetric-raw-order-positive",
            ([3], [2], [1]),
            1,
        ),
        (
            "rotated-raw-order-is-zero",
            ([2], [1], [3]),
            0,
        ),
    ]
    checks: list[dict[str, object]] = []
    for anchor_id, arguments, expected in raw_order_anchors:
        actual = lrcalc.lrcoef(*arguments)
        checks.append({
            "actual": actual,
            "expected": expected,
            "id": anchor_id,
            "note": f"raw lrcalc.lrcoef{tuple(arguments)!r}",
            "pass": actual == expected,
        })

    wrapper_anchors = [
        (
            "documented-order-known-two",
            ((2, 1), (2, 1), (3, 2, 1)),
            2,
            "lrcoef(out=nu, inn1=lam, inn2=mu)",
        ),
        (
            "empty-partition-normalization",
            ((), (), ()),
            1,
            "lrcoef([],[],[])",
        ),
    ]
    for anchor_id, (lam, mu, nu), expected, note in wrapper_anchors:
        actual = lr_coefficient(lam, mu, nu)
        checks.append({
            "actual": actual,
            "expected": expected,
            "id": anchor_id,
            "note": note,
            "pass": actual == expected,
        })

    evaluation = evaluate_stretched(*DEGREE_SIX_PARTITIONS, mode="adaptive")
    checks.append({
        "actual": evaluation.polynomial_strings(),
        "expected": canonical_polynomial_strings(DEGREE_SIX_POLYNOMIAL),
        "id": "campaign-degree-six-polynomial",
        "note": "lam=mu=(4,3,2,1), nu=(6,5,4,3,2)",
        "pass": evaluation.polynomial == DEGREE_SIX_POLYNOMIAL,
        "values": list(evaluation.values),
    })
    return checks
