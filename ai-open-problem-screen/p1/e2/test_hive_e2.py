"""Unit and WSL integration tests for the independent E2 hive evaluator."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest

try:
    from .hive_e2 import (
        HiveInputError,
        RHOMBUS_DIRECTIONS,
        build_hive_polytope,
        evaluate_polynomial,
        evaluate_with_normaliz,
        interpolate_polynomial,
        load_fixtures,
        lr_count,
    )
except ImportError:
    from hive_e2 import (  # type: ignore
        HiveInputError,
        RHOMBUS_DIRECTIONS,
        build_hive_polytope,
        evaluate_polynomial,
        evaluate_with_normaliz,
        interpolate_polynomial,
        load_fixtures,
        lr_count,
    )


HERE = Path(__file__).resolve().parent


class HiveConstructionTests(unittest.TestCase):
    def test_variable_and_rhombus_counts(self) -> None:
        for n in range(2, 8):
            polytope = build_hive_polytope([1], [1], [2], n=n)
            self.assertEqual(polytope.ambient_dimension, (n - 1) * (n - 2) // 2)
            expected = n * (n - 1) // 2
            counts = Counter(r.family for r in polytope.rhombi)
            self.assertEqual(
                counts,
                Counter({family: expected for family, _, _ in RHOMBUS_DIRECTIONS}),
            )
            self.assertEqual(len(polytope.rhombi), 3 * expected)

    def test_buch_boundary_and_exact_bounds(self) -> None:
        polytope = build_hive_polytope([2, 1], [2, 1], [3, 2, 1], n=3)
        self.assertEqual(polytope.variables, ((1, 1),))
        self.assertEqual(
            dict(polytope.boundary),
            {
                (0, 0): 0,
                (1, 0): 2,
                (2, 0): 3,
                (3, 0): 3,
                (0, 1): 3,
                (0, 2): 5,
                (0, 3): 6,
                (2, 1): 5,
                (1, 2): 6,
            },
        )
        rows = [tuple(r.form.row()) for r in polytope.rhombi]
        self.assertEqual(set(rows), {(1, -4), (-1, 5)})
        self.assertIn((1, -4), rows)
        self.assertIn((-1, 5), rows)

    def test_degenerate_and_empty_one_variable_bounds(self) -> None:
        point = build_hive_polytope([2, 1], [2, 1], [4, 2], n=3)
        empty = build_hive_polytope([2, 1], [2, 1], [5, 1], n=3)
        point_rows = {tuple(r.form.row()) for r in point.rhombi}
        empty_rows = {tuple(r.form.row()) for r in empty.rhombi}
        self.assertIn((1, -5), point_rows)
        self.assertIn((-1, 5), point_rows)
        self.assertIn((1, -6), empty_rows)
        self.assertIn((-1, 5), empty_rows)

    def test_invalid_boundaries_fail_before_normaliz(self) -> None:
        with self.assertRaises(HiveInputError):
            build_hive_polytope([1, 2], [1], [2, 2], n=2)
        with self.assertRaises(HiveInputError):
            build_hive_polytope([1], [1], [3], n=2)
        with self.assertRaises(HiveInputError):
            build_hive_polytope([1, 1, 1], [1], [4], n=2)
        for malformed in ([1.9], [True], ["1"]):
            with self.subTest(malformed=malformed), self.assertRaises(HiveInputError):
                build_hive_polytope(malformed, [1], [2], n=2)
        for malformed_n in (True, 2.5, "2"):
            with self.subTest(n=malformed_n), self.assertRaises(HiveInputError):
                build_hive_polytope([1], [1], [2], n=malformed_n)  # type: ignore[arg-type]

    def test_lr_count_rejects_coercible_nonintegers(self) -> None:
        for malformed in ([1.9], [True], ["1"]):
            with self.subTest(malformed=malformed), self.assertRaises(HiveInputError):
                lr_count(malformed, [1], [2])
        for stretch in (True, 1.5, "1"):
            with self.subTest(stretch=stretch), self.assertRaises(ValueError):
                lr_count([1], [1], [2], stretch)  # type: ignore[arg-type]

    def test_zero_variable_boundary(self) -> None:
        polytope = build_hive_polytope([1], [1], [2], n=2)
        self.assertEqual(polytope.ambient_dimension, 0)
        result = evaluate_with_normaliz(polytope)
        self.assertEqual(result["canonical_polynomial"], ["1"])
        self.assertEqual(result["number_lattice_points"], 1)

    def test_exact_interpolation_from_positive_stretches(self) -> None:
        samples = {1: 2, 2: 3, 3: 4}
        self.assertEqual(interpolate_polynomial(samples), [Fraction(1), Fraction(1)])
        zero = {1: 0, 2: 0}
        self.assertEqual(interpolate_polynomial(zero), [Fraction(0)])
        for malformed in ({1.5: 2}, {1: 2.5}, {True: 2}):
            with self.subTest(malformed=malformed), self.assertRaises(ValueError):
                interpolate_polynomial(malformed)  # type: ignore[arg-type]


@unittest.skipUnless(
    importlib.util.find_spec("PyNormaliz") and importlib.util.find_spec("lrcalc"),
    "WSL PyNormaliz and lrcalc are required for integration tests",
)
class FixtureIntegrationTests(unittest.TestCase):
    def test_all_fixed_fixtures_match_normaliz_and_lrcalc(self) -> None:
        fixtures = load_fixtures(HERE / "fixtures.json")
        self.assertGreaterEqual(len(fixtures), 6)
        for fixture in fixtures:
            with self.subTest(fixture=fixture["id"]):
                polytope = build_hive_polytope(
                    fixture["lam"], fixture["mu"], fixture["nu"], n=fixture["n"]
                )
                result = evaluate_with_normaliz(polytope)
                self.assertEqual(
                    result["canonical_polynomial"], fixture["expected_polynomial"]
                )
                self.assertEqual(
                    result["affine_dimension"], fixture["expected_affine_dimension"]
                )
                self.assertEqual(
                    result["number_lattice_points"], fixture["expected_lr_at_1"]
                )
                self.assertEqual(
                    lr_count(fixture["lam"], fixture["mu"], fixture["nu"]),
                    fixture["expected_lr_at_1"],
                )
                coefficients = [Fraction(x) for x in fixture["expected_polynomial"]]
                for stretch in range(1, max(3, len(coefficients) + 1) + 1):
                    self.assertEqual(
                        lr_count(
                            fixture["lam"], fixture["mu"], fixture["nu"], stretch
                        ),
                        evaluate_polynomial(coefficients, stretch),
                    )


@unittest.skipUnless(
    (HERE / "reports" / "fixture_agreement.json").is_file(),
    "run_fixtures must create the controller adapter first",
)
class ControllerAdapterTests(unittest.TestCase):
    def test_adapter_passes_control_gate_fixture_validator(self) -> None:
        from p1.control.canonical import sha256_file
        from p1.control.gate import (
            DEFAULT_P1_POLICY,
            _Collector,
            _derived_coverage_tags,
            _validate_fixture_evaluator_artifacts,
            _validate_fixtures,
        )

        reports = HERE / "reports"
        lrcalc_path = reports / "lrcalc_interp_evaluator.json"
        normaliz_path = reports / "normaliz_ehrhart_evaluator.json"
        agreement_path = reports / "fixture_agreement.json"
        selected = {
            "fixture-evaluator-lrcalc": {
                "logical_path": lrcalc_path.relative_to(HERE.parent.parent).as_posix(),
                "sha256": sha256_file(lrcalc_path),
            },
            "fixture-evaluator-normaliz": {
                "logical_path": normaliz_path.relative_to(HERE.parent.parent).as_posix(),
                "sha256": sha256_file(normaliz_path),
            },
        }
        collector = _Collector([], [])
        evaluator_maps = _validate_fixture_evaluator_artifacts(
            HERE.parent.parent, selected, collector
        )
        self.assertIsNotNone(evaluator_maps)
        _validate_fixtures(
            agreement_path,
            DEFAULT_P1_POLICY,
            {
                "lrcalc-interp": selected["fixture-evaluator-lrcalc"]["sha256"],
                "normaliz-ehrhart": selected["fixture-evaluator-normaliz"]["sha256"],
            },
            evaluator_maps,
            {
                fixture["id"]: _derived_coverage_tags(fixture)
                for fixture in load_fixtures(HERE / "fixtures.json")
            },
            collector,
        )
        self.assertEqual(collector.failures, [], collector.checks)


if __name__ == "__main__":
    unittest.main(verbosity=2)
