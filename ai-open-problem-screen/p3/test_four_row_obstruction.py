"""Tests for the standalone four-row normal-minor certificate."""

from __future__ import annotations

import unittest

from p3.verify_four_row_obstruction import build_certificate


class FourRowObstructionCertificateTests(unittest.TestCase):
    def test_exact_minor_census(self) -> None:
        certificate = build_certificate()
        self.assertEqual(certificate["row_count"], 18)
        self.assertEqual(certificate["minor_count"], 816)
        self.assertEqual(
            certificate["absolute_determinant_counts"],
            {"0": 299, "1": 468, "2": 48, "4": 1},
        )
        maximum = certificate["unique_absolute_determinant_four"]
        self.assertEqual(abs(maximum["determinant"]), 4)
        self.assertEqual(
            {tuple(row) for row in maximum["rows"]},
            {(1, 1, -1), (1, -1, 1), (-1, 1, 1)},
        )


if __name__ == "__main__":
    unittest.main()
