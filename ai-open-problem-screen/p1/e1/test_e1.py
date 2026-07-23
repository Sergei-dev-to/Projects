from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

import lrcalc

try:
    from .evaluator import (
        DEGREE_SIX_POLYNOMIAL,
        DEGREE_SIX_PARTITIONS,
        DegreeBoundError,
        StabilityError,
        canonical_polynomial_strings,
        canonical_triple,
        enumerate_structural_triples,
        evaluate_polynomial,
        evaluate_stretched,
        hive_dimension_bound,
        lr_coefficient,
        partitions_exact,
        polynomial_from_consecutive_values,
        run_anchor_checks,
        scale,
        stabilized_polynomial,
        triple_sort_key,
    )
    from .parity import (
        DEFAULT_BASELINE,
        DEFAULT_SIDECAR,
        EXPECTED_BASELINE_COUNT,
        EXPECTED_BASELINE_HASH,
        payload_hash,
        run_gate,
        validate_baseline,
    )
except ImportError:
    from evaluator import (
        DEGREE_SIX_POLYNOMIAL,
        DEGREE_SIX_PARTITIONS,
        DegreeBoundError,
        StabilityError,
        canonical_polynomial_strings,
        canonical_triple,
        enumerate_structural_triples,
        evaluate_polynomial,
        evaluate_stretched,
        hive_dimension_bound,
        lr_coefficient,
        partitions_exact,
        polynomial_from_consecutive_values,
        run_anchor_checks,
        scale,
        stabilized_polynomial,
        triple_sort_key,
    )
    from parity import (
        DEFAULT_BASELINE,
        DEFAULT_SIDECAR,
        EXPECTED_BASELINE_COUNT,
        EXPECTED_BASELINE_HASH,
        payload_hash,
        run_gate,
        validate_baseline,
    )


class PartitionTests(unittest.TestCase):
    def test_scale_zero_is_empty(self) -> None:
        self.assertEqual(scale((4, 2), 0), ())

    def test_swap_only_canonicalizer(self) -> None:
        self.assertEqual(
            canonical_triple((3,), (1, 1, 1), (4, 1, 1)),
            ((1, 1, 1), (3,), (4, 1, 1)),
        )

    def test_partition_normalization_rejects_nonintegers(self) -> None:
        with self.assertRaises(ValueError):
            canonical_triple((1.5,), (1,), (2,))

    def test_exact_partitions(self) -> None:
        self.assertEqual(
            partitions_exact(5, 3),
            ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1)),
        )

    def test_structural_enumeration_is_canonical_and_sorted(self) -> None:
        triples = enumerate_structural_triples(2, 2)
        self.assertEqual(triples, sorted(triples, key=triple_sort_key))
        self.assertEqual(len(triples), len(set(triples)))
        self.assertTrue(all(lam <= mu for lam, mu, _ in triples))


class InterpolationTests(unittest.TestCase):
    polynomial = tuple(map(Fraction, ("1", "3/2", "1/2")))

    def test_exact_rational_interpolation(self) -> None:
        values = [evaluate_polynomial(self.polynomial, point) for point in range(6)]
        self.assertEqual(
            polynomial_from_consecutive_values(values, maximum_degree=2),
            self.polynomial,
        )
        self.assertEqual(
            canonical_polynomial_strings(self.polynomial), ["1", "3/2", "1/2"]
        )

    def test_stabilization_requires_zero_top_difference(self) -> None:
        values = [evaluate_polynomial(self.polynomial, point) for point in range(3)]
        self.assertIsNone(stabilized_polynomial(values))
        values.append(evaluate_polynomial(self.polynomial, 3))
        self.assertEqual(stabilized_polynomial(values), self.polynomial)

    def test_bounded_interpolation_rejects_bad_holdout(self) -> None:
        with self.assertRaises(StabilityError):
            polynomial_from_consecutive_values([1, 1, 2], maximum_degree=0)

    def test_adaptive_mode_enforces_hive_degree_bound(self) -> None:
        # A synthetic linear sequence attached to a one-row (bound-zero) triple.
        def synthetic(lam, _mu, _nu):
            point = 0 if not lam else lam[0]
            return point + 1

        with self.assertRaises(DegreeBoundError):
            evaluate_stretched((1,), (1,), (2,), counter=synthetic)

    def test_conservative_mode_checks_beyond_bounded_mode(self) -> None:
        # For B=0 bounded checks through N=1; conservative checks through N=2.
        def late_failure(lam, _mu, _nu):
            point = 0 if not lam else lam[0]
            return 1 if point < 2 else 2

        bounded = evaluate_stretched(
            (1,), (1,), (2,), mode="bounded", counter=late_failure
        )
        self.assertEqual(bounded.polynomial, (Fraction(1),))
        with self.assertRaises(StabilityError):
            evaluate_stretched(
                (1,), (1,), (2,), mode="conservative", counter=late_failure
            )

    def test_row_seven_conservative_range_is_zero_through_32(self) -> None:
        bound = hive_dimension_bound(7)
        self.assertEqual(bound, 15)
        self.assertEqual(2 * bound + 2, 32)


class LrcalcIntegrationTests(unittest.TestCase):
    def test_raw_api_argument_order_is_outer_then_inners(self) -> None:
        self.assertEqual(lrcalc.lrcoef([3], [2], [1]), 1)
        self.assertEqual(lrcalc.lrcoef([2], [1], [3]), 0)

    def test_known_coefficient(self) -> None:
        self.assertEqual(lr_coefficient((2, 1), (2, 1), (3, 2, 1)), 2)

    def test_all_mandatory_anchors(self) -> None:
        checks = run_anchor_checks()
        self.assertTrue(all(check["pass"] for check in checks), checks)

    def test_degree_six_anchor_polynomial(self) -> None:
        evaluation = evaluate_stretched(*DEGREE_SIX_PARTITIONS, mode="adaptive")
        self.assertEqual(evaluation.polynomial, DEGREE_SIX_POLYNOMIAL)
        self.assertEqual(
            evaluation.values, (1, 16, 126, 616, 2200, 6336, 15631, 34336)
        )


class BaselineTests(unittest.TestCase):
    def test_frozen_baseline_integrity(self) -> None:
        integrity, records, errors = validate_baseline(
            DEFAULT_BASELINE, DEFAULT_SIDECAR
        )
        self.assertEqual(errors, [])
        self.assertEqual(integrity["status"], "pass")
        self.assertEqual(len(records), EXPECTED_BASELINE_COUNT)
        self.assertEqual(payload_hash(records), EXPECTED_BASELINE_HASH)

    def test_failure_artifacts_are_deterministic(self) -> None:
        baseline = json.loads(DEFAULT_BASELINE.read_text(encoding="utf-8"))
        baseline["triples"][0]["poly"] = ["2"]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bad_baseline = root / "bad.json"
            bad_baseline.write_text(json.dumps(baseline), encoding="utf-8")
            first = root / "first"
            second = root / "second"
            first_report, _ = run_gate(
                bad_baseline, DEFAULT_SIDECAR, first,
                mode="adaptive", workers=1,
            )
            second_report, _ = run_gate(
                bad_baseline, DEFAULT_SIDECAR, second,
                mode="adaptive", workers=1,
            )
            self.assertEqual(first_report["status"], "fail")
            self.assertEqual(
                (first / "parity_report.json").read_bytes(),
                (second / "parity_report.json").read_bytes(),
            )
            self.assertEqual(
                (first / "mismatches.json").read_bytes(),
                (second / "mismatches.json").read_bytes(),
            )
            self.assertEqual(
                (first / "artifact_manifest.json").read_bytes(),
                (second / "artifact_manifest.json").read_bytes(),
            )
            self.assertEqual(
                (first / "actual_frontier.json").read_bytes(),
                (second / "actual_frontier.json").read_bytes(),
            )
            actual_frontier = json.loads(
                (first / "actual_frontier.json").read_text(encoding="utf-8")
            )
            self.assertEqual(actual_frontier["triples"], [])
            self.assertIsNone(actual_frontier["triples_payload_sha256"])


if __name__ == "__main__":
    unittest.main()
