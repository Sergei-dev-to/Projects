"""Explicit Knutson--Tao hive polytopes and an independent Normaliz evaluator.

The coordinate and inequality convention is deliberately encoded without using
the dry-run LR implementation.  A hive of side ``n`` has vertices ``q[i,j]``
with ``i,j >= 0`` and ``i+j <= n``.  Boundary values are

    q[k,0]     = lambda_1 + ... + lambda_k,
    q[0,k]     = nu_1     + ... + nu_k,
    q[n-k,k]   = |lambda| + mu_1 + ... + mu_k.

Every elementary rhombus uses two consecutive triangular-lattice directions
``a,b`` and imposes

    q[p+a] + q[p+b] - q[p] - q[p+a+b] >= 0.

The three direction pairs are listed in ``RHOMBUS_DIRECTIONS`` below.  This is
the "obtuse vertices >= acute vertices" convention.  Interior hive labels are
ordinary integer coordinates, so eliminating the fixed boundary gives the
correct lattice directly; no lattice projection or saturation is hidden here.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
import operator
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


Coord = tuple[int, int]
Partition = tuple[int, ...]


class HiveInputError(ValueError):
    """Raised before calling Normaliz when a hive boundary is malformed."""


RHOMBUS_DIRECTIONS: tuple[tuple[str, Coord, Coord], ...] = (
    ("east_north", (1, 0), (0, 1)),
    ("north_northwest", (0, 1), (-1, 1)),
    ("northwest_west", (-1, 1), (-1, 0)),
)


def _add(*points: Coord) -> Coord:
    return (sum(p[0] for p in points), sum(p[1] for p in points))


def _partition(value: Sequence[int], name: str) -> Partition:
    try:
        parts: list[int] = []
        for item in value:
            if isinstance(item, bool):
                raise TypeError("boolean values are not partition parts")
            parts.append(operator.index(item))
        result = tuple(parts)
    except TypeError as exc:
        raise HiveInputError(f"{name} must be a sequence of integers") from exc
    if any(x < 0 for x in result):
        raise HiveInputError(f"{name} must have nonnegative parts")
    if any(result[i] < result[i + 1] for i in range(len(result) - 1)):
        raise HiveInputError(f"{name} is not weakly decreasing: {result}")
    while result and result[-1] == 0:
        result = result[:-1]
    return result


def _pad(partition: Partition, n: int) -> Partition:
    if len(partition) > n:
        raise HiveInputError(
            f"partition {partition} has {len(partition)} parts, exceeding n={n}"
        )
    return partition + (0,) * (n - len(partition))


def _partial_sums(partition: Partition) -> list[int]:
    values = [0]
    for part in partition:
        values.append(values[-1] + part)
    return values


def _coord_name(coord: Coord) -> str:
    return f"q_{coord[0]}_{coord[1]}"


@dataclass(frozen=True)
class LinearForm:
    """An integer affine form ``sum(coeffs[k] * x[k]) + constant``."""

    coefficients: tuple[int, ...]
    constant: int

    def row(self) -> list[int]:
        """Raw Normaliz ``inhom_inequalities`` row (form is >= 0)."""

        return [*self.coefficients, self.constant]

    def is_constant(self) -> bool:
        return not any(self.coefficients)

    def scaled(self, scalar: int) -> "LinearForm":
        return LinearForm(
            tuple(scalar * c for c in self.coefficients), scalar * self.constant
        )

    def plus(self, other: "LinearForm") -> "LinearForm":
        if len(self.coefficients) != len(other.coefficients):
            raise AssertionError("linear-form ambient dimensions disagree")
        return LinearForm(
            tuple(a + b for a, b in zip(self.coefficients, other.coefficients)),
            self.constant + other.constant,
        )


@dataclass(frozen=True)
class RhombusInequality:
    family: str
    base: Coord
    direction_a: Coord
    direction_b: Coord
    obtuse_vertices: tuple[Coord, Coord]
    acute_vertices: tuple[Coord, Coord]
    form: LinearForm

    def as_dict(self, variable_names: Sequence[str]) -> dict[str, Any]:
        terms = {
            name: coefficient
            for name, coefficient in zip(variable_names, self.form.coefficients)
            if coefficient
        }
        return {
            "family": self.family,
            "base": list(self.base),
            "direction_a": list(self.direction_a),
            "direction_b": list(self.direction_b),
            "obtuse_vertices": [list(c) for c in self.obtuse_vertices],
            "acute_vertices": [list(c) for c in self.acute_vertices],
            "semantic": "sum(obtuse) - sum(acute) >= 0",
            "terms": terms,
            "constant": self.form.constant,
            "normaliz_row": self.form.row(),
        }


@dataclass(frozen=True)
class HivePolytope:
    n: int
    lam: Partition
    mu: Partition
    nu: Partition
    padded_lam: Partition
    padded_mu: Partition
    padded_nu: Partition
    boundary: Mapping[Coord, int]
    variables: tuple[Coord, ...]
    rhombi: tuple[RhombusInequality, ...]

    @property
    def variable_names(self) -> tuple[str, ...]:
        return tuple(_coord_name(c) for c in self.variables)

    @property
    def ambient_dimension(self) -> int:
        return len(self.variables)

    @property
    def expected_rhombi_per_family(self) -> int:
        return self.n * (self.n - 1) // 2

    @property
    def normaliz_rows(self) -> list[list[int]]:
        """Semantics-preserving rows passed to Normaliz.

        Constant tautologies are omitted.  Constant contradictions are retained,
        because they are the exact certificate that the polytope is empty.
        Duplicates are intentionally retained: the raw representation remains in
        one-to-one correspondence with non-tautological geometric rhombi.
        """

        rows: list[list[int]] = []
        for rhombus in self.rhombi:
            form = rhombus.form
            if form.is_constant() and form.constant >= 0:
                continue
            rows.append(form.row())
        return rows

    @property
    def has_constant_contradiction(self) -> bool:
        return any(r.form.is_constant() and r.form.constant < 0 for r in self.rhombi)

    def input_dict(self) -> dict[str, Any]:
        family_counts = {
            family: sum(r.family == family for r in self.rhombi)
            for family, _, _ in RHOMBUS_DIRECTIONS
        }
        return {
            "schema_version": 1,
            "coordinate_convention": "q[i,j], i>=0, j>=0, i+j<=n",
            "boundary_convention": {
                "lambda_edge": "q[k,0]=sum(lambda[1..k])",
                "nu_edge": "q[0,k]=sum(nu[1..k])",
                "mu_edge": "q[n-k,k]=|lambda|+sum(mu[1..k])",
            },
            "rhombus_convention": "sum(obtuse)-sum(acute)>=0",
            "n": self.n,
            "lam": list(self.lam),
            "mu": list(self.mu),
            "nu": list(self.nu),
            "padded": {
                "lam": list(self.padded_lam),
                "mu": list(self.padded_mu),
                "nu": list(self.padded_nu),
            },
            "boundary": {
                _coord_name(coord): value
                for coord, value in sorted(self.boundary.items())
            },
            "variables": list(self.variable_names),
            "ambient_dimension": self.ambient_dimension,
            "rhombus_family_counts": family_counts,
            "rhombi": [r.as_dict(self.variable_names) for r in self.rhombi],
            "normaliz": {
                "input_type": "inhom_inequalities",
                "row_semantics": "a_1*x_1+...+a_d*x_d+b>=0",
                "rows": self.normaliz_rows,
                "omitted_constant_tautologies": sum(
                    r.form.is_constant() and r.form.constant >= 0 for r in self.rhombi
                ),
            },
        }

    def normaliz_input_text(self) -> str:
        """Return a replayable Normaliz CLI input for positive ambient dimension."""

        if self.ambient_dimension == 0:
            raise HiveInputError("Normaliz CLI has no useful zero-dimensional ambient input")
        rows = self.normaliz_rows
        lines = [
            f"amb_space {self.ambient_dimension}",
            f"inhom_inequalities {len(rows)}",
            *(" ".join(str(x) for x in row) for row in rows),
            "EhrhartSeries",
            "EhrhartQuasiPolynomial",
            "NumberLatticePoints",
            "AffineDim",
            "VerticesOfPolyhedron",
            "SupportHyperplanes",
            "LatticePoints",
            "",
        ]
        return "\n".join(lines)


def _rhombus_bases(n: int, family: str) -> Iterable[Coord]:
    if family == "east_north":
        for i in range(n - 1):
            for j in range(n - 1 - i):
                yield (i, j)
        return
    if family == "north_northwest":
        for i in range(1, n):
            for j in range(n - i):
                yield (i, j)
        return
    if family == "northwest_west":
        for i in range(2, n + 1):
            for j in range(n - i + 1):
                yield (i, j)
        return
    raise AssertionError(f"unknown rhombus family {family}")


def build_hive_polytope(
    lam: Sequence[int],
    mu: Sequence[int],
    nu: Sequence[int],
    *,
    n: int | None = None,
) -> HivePolytope:
    """Eliminate the fixed boundary and return the explicit hive inequalities."""

    lam_t = _partition(lam, "lambda")
    mu_t = _partition(mu, "mu")
    nu_t = _partition(nu, "nu")
    inferred_n = max(len(lam_t), len(mu_t), len(nu_t), 1)
    if n is None:
        n = inferred_n
    if isinstance(n, bool):
        raise HiveInputError("n must be a positive integer")
    try:
        n = operator.index(n)
    except TypeError as exc:
        raise HiveInputError("n must be a positive integer") from exc
    if n < 1:
        raise HiveInputError("n must be a positive integer")
    if n < inferred_n:
        raise HiveInputError(f"n={n} is smaller than a partition length {inferred_n}")

    lam_n = _pad(lam_t, n)
    mu_n = _pad(mu_t, n)
    nu_n = _pad(nu_t, n)
    if sum(lam_n) + sum(mu_n) != sum(nu_n):
        raise HiveInputError(
            "boundary sizes are incompatible: "
            f"|lambda|+|mu|={sum(lam_n)+sum(mu_n)} != |nu|={sum(nu_n)}"
        )

    lam_sums = _partial_sums(lam_n)
    mu_sums = _partial_sums(mu_n)
    nu_sums = _partial_sums(nu_n)
    boundary: dict[Coord, int] = {}

    def set_boundary(coord: Coord, value: int, edge: str) -> None:
        if coord in boundary and boundary[coord] != value:
            raise HiveInputError(
                f"incompatible {edge} value at {coord}: {value} != {boundary[coord]}"
            )
        boundary[coord] = value

    for k in range(n + 1):
        set_boundary((k, 0), lam_sums[k], "lambda")
        set_boundary((0, k), nu_sums[k], "nu")
        set_boundary((n - k, k), lam_sums[n] + mu_sums[k], "mu")

    variables = tuple(
        (i, j)
        for i in range(1, n)
        for j in range(1, n - i)
    )
    variable_index = {coord: index for index, coord in enumerate(variables)}
    ambient_dimension = len(variables)

    def vertex_form(coord: Coord) -> LinearForm:
        i, j = coord
        if i < 0 or j < 0 or i + j > n:
            raise AssertionError(f"rhombus generator left the hive triangle: {coord}")
        if coord in boundary:
            return LinearForm((0,) * ambient_dimension, boundary[coord])
        try:
            index = variable_index[coord]
        except KeyError as exc:
            raise AssertionError(f"unclassified hive coordinate {coord}") from exc
        coefficients = [0] * ambient_dimension
        coefficients[index] = 1
        return LinearForm(tuple(coefficients), 0)

    rhombi: list[RhombusInequality] = []
    for family, direction_a, direction_b in RHOMBUS_DIRECTIONS:
        for base in _rhombus_bases(n, family):
            obtuse = (_add(base, direction_a), _add(base, direction_b))
            acute = (base, _add(base, direction_a, direction_b))
            form = vertex_form(obtuse[0]).plus(vertex_form(obtuse[1]))
            form = form.plus(vertex_form(acute[0]).scaled(-1))
            form = form.plus(vertex_form(acute[1]).scaled(-1))
            rhombi.append(
                RhombusInequality(
                    family=family,
                    base=base,
                    direction_a=direction_a,
                    direction_b=direction_b,
                    obtuse_vertices=obtuse,
                    acute_vertices=acute,
                    form=form,
                )
            )

    result = HivePolytope(
        n=n,
        lam=lam_t,
        mu=mu_t,
        nu=nu_t,
        padded_lam=lam_n,
        padded_mu=mu_n,
        padded_nu=nu_n,
        boundary=boundary,
        variables=variables,
        rhombi=tuple(rhombi),
    )
    expected = result.expected_rhombi_per_family
    for family, _, _ in RHOMBUS_DIRECTIONS:
        actual = sum(r.family == family for r in result.rhombi)
        if actual != expected:
            raise AssertionError(f"{family}: generated {actual} rhombi, expected {expected}")
    if len(result.rhombi) != 3 * expected:
        raise AssertionError("total rhombus count is wrong")
    return result


def _fraction_strings(values: Sequence[Fraction]) -> list[str]:
    return [str(value) for value in values]


def _normaliz_quasipolynomial(raw: Sequence[Any]) -> tuple[list[list[Fraction]], int]:
    """Decode PyNormaliz's ``[residue numerators..., common denominator]``."""

    if len(raw) < 2 or isinstance(raw[-1], bool):
        raise RuntimeError(f"unexpected EhrhartQuasiPolynomial payload: {raw!r}")
    try:
        denominator = operator.index(raw[-1])
    except TypeError as exc:
        raise RuntimeError(f"unexpected EhrhartQuasiPolynomial payload: {raw!r}") from exc
    if denominator == 0:
        raise RuntimeError(f"unexpected EhrhartQuasiPolynomial payload: {raw!r}")
    residues: list[list[Fraction]] = []
    for numerators in raw[:-1]:
        if not isinstance(numerators, (list, tuple)):
            raise RuntimeError(f"unexpected residue polynomial: {numerators!r}")
        coefficients: list[Fraction] = []
        for value in numerators:
            if isinstance(value, bool):
                raise RuntimeError(f"unexpected residue coefficient: {value!r}")
            try:
                numerator = operator.index(value)
            except TypeError as exc:
                raise RuntimeError(f"unexpected residue coefficient: {value!r}") from exc
            coefficients.append(Fraction(numerator, denominator))
        residues.append(coefficients or [Fraction(0)])
    return residues, denominator


def evaluate_polynomial(coefficients: Sequence[Fraction], n: int) -> int | Fraction:
    value = sum(coefficient * (n**degree) for degree, coefficient in enumerate(coefficients))
    return value.numerator if value.denominator == 1 else value


def interpolate_polynomial(samples: Mapping[int, int]) -> list[Fraction]:
    """Interpolate exact monomial coefficients from distinct integer samples.

    This small Lagrange implementation is used only for the independent lrcalc
    side of the fixture adapter.  It deliberately does not import the dry-run or
    production E1 interpolation code.
    """

    points: list[tuple[int, int]] = []
    for x, y in samples.items():
        if isinstance(x, bool) or isinstance(y, bool):
            raise ValueError("interpolation samples must be exact integers")
        try:
            points.append((operator.index(x), operator.index(y)))
        except TypeError as exc:
            raise ValueError("interpolation samples must be exact integers") from exc
    points.sort()
    if not points or len({x for x, _ in points}) != len(points):
        raise ValueError("interpolation requires nonempty samples at distinct x values")

    def multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
        product = [Fraction(0)] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                product[i + j] += a * b
        return product

    result = [Fraction(0)] * len(points)
    for index, (x_i, y_i) in enumerate(points):
        basis = [Fraction(1)]
        denominator = Fraction(1)
        for other_index, (x_j, _) in enumerate(points):
            if other_index == index:
                continue
            basis = multiply(basis, [Fraction(-x_j), Fraction(1)])
            denominator *= x_i - x_j
        scale = Fraction(y_i, 1) / denominator
        for degree, coefficient in enumerate(basis):
            result[degree] += scale * coefficient
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def evaluate_with_normaliz(polytope: HivePolytope) -> dict[str, Any]:
    """Compute the exact E2 result through PyNormaliz.

    A zero-variable hive is checked directly because its only possible point is
    the unique boundary labeling.  Every positive-dimensional ambient input is
    handed to Normaliz, including infeasible systems.
    """

    if polytope.ambient_dimension == 0:
        empty = polytope.has_constant_contradiction
        coefficients = [Fraction(0 if empty else 1)]
        return {
            "engine": "exact-zero-variable-boundary-check",
            "empty": empty,
            "number_lattice_points": 0 if empty else 1,
            "affine_dimension": -1 if empty else 0,
            "vertices_of_polyhedron_raw": [] if empty else [[]],
            "lattice_points_raw": [] if empty else [[]],
            "support_hyperplanes_raw": [],
            "ehrhart_series_raw": [[0], [], 0] if empty else [[1], [1], 0],
            "ehrhart_quasipolynomial_raw": [[], 1] if empty else [[1], 1],
            "raw_period": 1,
            "raw_common_denominator": 1,
            "residue_polynomials": [_fraction_strings(coefficients)],
            "period_collapses_to_one": True,
            "canonical_polynomial": _fraction_strings(coefficients),
        }

    try:
        from PyNormaliz import Cone
    except ImportError as exc:  # pragma: no cover - exercised by readiness checks
        raise RuntimeError("PyNormaliz is required for the E2 evaluator") from exc

    cone = Cone(inhom_inequalities=polytope.normaliz_rows)
    raw_quasipolynomial = cone.EhrhartQuasiPolynomial()
    residues, common_denominator = _normaliz_quasipolynomial(raw_quasipolynomial)
    period_collapses = bool(residues) and all(r == residues[0] for r in residues[1:])
    if not period_collapses:
        raise RuntimeError(
            "Normaliz returned a nontrivial Ehrhart quasiperiod; refusing to "
            f"coerce it to a polynomial: {raw_quasipolynomial!r}"
        )
    canonical = residues[0]
    number_lattice_points = int(cone.NumberLatticePoints())
    return {
        "engine": "PyNormaliz.Cone(inhom_inequalities=rows)",
        "empty": number_lattice_points == 0 and int(cone.AffineDim()) == -1,
        "number_lattice_points": number_lattice_points,
        "affine_dimension": int(cone.AffineDim()),
        "vertices_of_polyhedron_raw": cone.VerticesOfPolyhedron(),
        "lattice_points_raw": cone.LatticePoints(),
        "support_hyperplanes_raw": cone.SupportHyperplanes(),
        "ehrhart_series_raw": cone.EhrhartSeries(),
        "ehrhart_quasipolynomial_raw": raw_quasipolynomial,
        "raw_period": len(residues),
        "raw_common_denominator": common_denominator,
        "residue_polynomials": [_fraction_strings(r) for r in residues],
        "period_collapses_to_one": period_collapses,
        "canonical_polynomial": _fraction_strings(canonical),
    }


def lr_count(
    lam: Sequence[int], mu: Sequence[int], nu: Sequence[int], stretch: int = 1
) -> int:
    """Independent E1 point-count query used only for fixture comparison."""

    if isinstance(stretch, bool):
        raise ValueError("fixture comparisons use positive integer stretches")
    try:
        stretch = operator.index(stretch)
    except TypeError as exc:
        raise ValueError("fixture comparisons use positive integer stretches") from exc
    if stretch < 1:
        raise ValueError("fixture comparisons use positive integer stretches")
    try:
        import lrcalc
    except ImportError as exc:  # pragma: no cover - exercised by readiness checks
        raise RuntimeError("the Python lrcalc package is required for fixture checks") from exc
    normalized_lam = _partition(lam, "lam")
    normalized_mu = _partition(mu, "mu")
    normalized_nu = _partition(nu, "nu")
    scaled_lam = [stretch * x for x in normalized_lam]
    scaled_mu = [stretch * x for x in normalized_mu]
    scaled_nu = [stretch * x for x in normalized_nu]
    return int(lrcalc.lrcoef(scaled_nu, scaled_lam, scaled_mu))


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_fixtures(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != 1 or not isinstance(data.get("fixtures"), list):
        raise HiveInputError("unsupported or malformed fixture manifest")
    return data["fixtures"]
