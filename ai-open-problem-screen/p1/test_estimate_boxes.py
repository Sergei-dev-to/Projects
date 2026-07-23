import unittest

try:
    from .estimate_boxes import (
        compatible_nu_count,
        partitions_upto,
        unrank_pair,
        unordered_pair_count,
        _row_starts,
    )
except ImportError:
    from estimate_boxes import (  # type: ignore
        compatible_nu_count,
        partitions_upto,
        unrank_pair,
        unordered_pair_count,
        _row_starts,
    )


class EstimateBoxesTests(unittest.TestCase):
    def test_partition_generator(self):
        self.assertEqual(
            set(partitions_upto(2, 3)),
            {(), (1,), (2,), (3,), (1, 1), (2, 1)},
        )

    def test_pair_unranking_is_bijective(self):
        for n in range(1, 12):
            starts = _row_starts(n)
            pairs = [unrank_pair(k, n, starts) for k in range(starts[-1])]
            self.assertEqual(len(pairs), unordered_pair_count(n))
            self.assertEqual(len(set(pairs)), len(pairs))
            self.assertTrue(all(0 <= i <= j < n for i, j in pairs))

    def test_compatible_nu_small(self):
        # For lambda=mu=(1), target weight 2 and at most two rows, the
        # containing partitions are (2) and (1,1).
        self.assertEqual(compatible_nu_count((1,), (1,), 2), 2)
        # Empty x empty has only the empty output partition.
        self.assertEqual(compatible_nu_count((), (), 4), 1)

    def test_compatible_count_matches_brute_force(self):
        parts = partitions_upto(4, 6)
        for lam in partitions_upto(4, 3):
            for mu in partitions_upto(4, 3):
                target = sum(lam) + sum(mu)
                brute = sum(
                    1
                    for nu in parts
                    if sum(nu) == target
                    and all(
                        (lam[i] if i < len(lam) else 0) <=
                        (nu[i] if i < len(nu) else 0)
                        for i in range(4)
                    )
                    and all(
                        (mu[i] if i < len(mu) else 0) <=
                        (nu[i] if i < len(nu) else 0)
                        for i in range(4)
                    )
                )
                self.assertEqual(compatible_nu_count(lam, mu, 4), brute)


if __name__ == "__main__":
    unittest.main()
