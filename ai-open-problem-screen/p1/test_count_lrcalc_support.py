from __future__ import annotations

import unittest

try:
    from .count_lrcalc_support import count_box
except ImportError:
    from count_lrcalc_support import count_box  # type: ignore


class LrcalcSupportCountTests(unittest.TestCase):
    def test_b0_count_matches_independent_per_triple_filter(self) -> None:
        report = count_box("B0-7", 6, 7)
        self.assertEqual(report["partition_count"], 44)
        self.assertEqual(report["unordered_pair_count"], 990)
        self.assertEqual(report["nonzero_canonical_triples_at_n1"], 9478)
        self.assertEqual(
            sum(report["nonzero_count_by_outer_length"].values()), 9478
        )

    def test_empty_box(self) -> None:
        report = count_box("zero", 1, 0)
        self.assertEqual(report["partition_count"], 1)
        self.assertEqual(report["nonzero_canonical_triples_at_n1"], 1)
        self.assertEqual(report["maximum_lr_coefficient_at_n1"], 1)


if __name__ == "__main__":
    unittest.main()
