from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import tempfile
import unittest

from p3 import bakeoff


class AllocationTests(unittest.TestCase):
    def test_largest_remainder_is_exact_and_deterministic(self) -> None:
        counts = {(4, 8): 1, (5, 9): 2, (6, 10): 3}
        self.assertEqual(
            bakeoff._largest_remainder_quotas(counts, 4),
            {(4, 8): 1, (5, 9): 1, (6, 10): 2},
        )

    def test_largest_remainder_rejects_oversize_panel(self) -> None:
        with self.assertRaises(bakeoff.BakeoffError):
            bakeoff._largest_remainder_quotas({(4, 8): 2}, 3)


class ReeveGeometryTests(unittest.TestCase):
    def test_reeve_volume_in_saturated_lattice(self) -> None:
        vertices = [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [1, 1, 13, 0, 0],
        ]
        self.assertEqual(bakeoff.normalized_tetrahedron_volume(vertices), 13)
        self.assertEqual(
            bakeoff._reeve_polynomial(13), ["1", "-1/6", "1", "13/6"]
        )

    def test_volume_uses_saturated_affine_lattice(self) -> None:
        # The plane's ambient coordinates carry a common factor, but its
        # saturated affine lattice removes that embedding index.
        vertices = [
            [0, 0, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 1, 2, 3],
        ]
        self.assertEqual(bakeoff.normalized_tetrahedron_volume(vertices), 1)

    def test_vertex_decoder_preserves_rationals(self) -> None:
        vertices, integral = bakeoff._decode_vertices([[2, 4, 2]], 2)
        self.assertEqual(vertices, [[Fraction(1), Fraction(2)]])
        self.assertTrue(integral)
        vertices, integral = bakeoff._decode_vertices([[1, 4, 2]], 2)
        self.assertEqual(vertices, [[Fraction(1, 2), Fraction(2)]])
        self.assertFalse(integral)

    def test_degenerate_tetrahedron_fails_closed(self) -> None:
        with self.assertRaises(bakeoff.BakeoffError):
            bakeoff.normalized_tetrahedron_volume(
                [[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]]
            )


class RankingAndMetricTests(unittest.TestCase):
    def setUp(self) -> None:
        self.entry = {
            "triple": {"lam": [4, 2], "mu": [4, 2], "nu": [6, 4, 2]},
        }

    def test_reeve_signature_beats_positive_tetrahedron(self) -> None:
        negative = {
            "predicted_reeve_negative_signature": True,
            "predicted_empty_integral_tetrahedron": True,
            "normalized_volume": 13,
            "affine_dimension": 3,
            "vertex_count": 4,
        }
        positive = {
            **negative,
            "predicted_reeve_negative_signature": False,
            "normalized_volume": 12,
        }
        self.assertLess(
            bakeoff._ranking_key("reeve_volume", self.entry, negative),
            bakeoff._ranking_key("reeve_volume", self.entry, positive),
        )

    def test_metrics_exclude_constant_and_leading_terms(self) -> None:
        metrics = bakeoff._polynomial_metrics(["1", "5/12", "1/24"])
        self.assertEqual(metrics["min_interior_coefficient"], "5/12")
        self.assertEqual(metrics["gain"], "7/12")
        self.assertTrue(metrics["subunit_interior"])
        self.assertFalse(metrics["has_negative_coefficient"])

    def test_negative_is_target_not_subunit_proxy(self) -> None:
        metrics = bakeoff._polynomial_metrics(["1", "-1/6", "1", "13/6"])
        self.assertTrue(metrics["has_negative_coefficient"])
        self.assertEqual(metrics["negative_indices"], [1])


class ArtifactTests(unittest.TestCase):
    def test_pinned_json_round_trip_and_mutation_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.json"
            digest = bakeoff._write_pinned_json(path, {"b": 2, "a": 1})
            value, observed = bakeoff._load_pinned_json(path)
            self.assertEqual(value, {"a": 1, "b": 2})
            self.assertEqual(observed, digest)
            with self.assertRaises(bakeoff.BakeoffError):
                bakeoff._write_pinned_json(path, {"a": 2})


if __name__ == "__main__":
    unittest.main()
