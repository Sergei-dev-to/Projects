from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from p3 import reeve_scan as scan


class DirectScanContractTests(unittest.TestCase):
    def test_plan_is_direct_search_without_bakeoff_arms(self) -> None:
        plan = scan.build_plan()
        self.assertEqual(
            plan["classification"],
            "internal-bounded-non-certifying-direct-search",
        )
        self.assertNotIn("arms", plan)
        self.assertEqual(
            plan["outcomes"]["zero_hit"],
            "BUDGET_STOP_NO_HIT_IN_FROZEN_PANEL",
        )
        self.assertFalse(plan["superseded_gate_revived"])

    def test_selection_hash_is_deterministic_and_domain_separated(self) -> None:
        triple = ((2, 1), (2, 1), (3, 2, 1))
        self.assertEqual(scan._selection_hash(triple), scan._selection_hash(triple))
        self.assertNotEqual(scan._selection_hash(triple), scan.core._triple_id(triple))

    def test_max_items_rejects_bool_negative_and_noninteger(self) -> None:
        for value in (True, -1, 1.5):
            with self.subTest(value=value):
                with self.assertRaises(scan.ScanError):
                    scan._validate_max_items(value)  # type: ignore[arg-type]
        self.assertEqual(scan._validate_max_items(0), 0)
        self.assertIsNone(scan._validate_max_items(None))

    def test_workdir_must_stay_below_run_p3(self) -> None:
        with self.assertRaises(scan.ScanError):
            scan._validate_work_dir(scan.REPO_ROOT)
        accepted = scan._validate_work_dir(Path("run/p3/unit-test-scan"))
        self.assertIn(scan.RUN_ROOT, accepted.parents)

    def test_runtime_is_the_pinned_wsl_environment(self) -> None:
        identity = scan._runtime_identity()
        self.assertTrue(identity["wsl"])
        self.assertEqual(identity["lrcalc_version"], "2.1")
        self.assertEqual(identity["pynormaliz_version"], "2.19")


class CrashArtifactTests(unittest.TestCase):
    def test_orphan_json_is_validated_then_sidecar_repaired(self) -> None:
        with tempfile.TemporaryDirectory(dir=scan.RUN_ROOT) as directory:
            path = Path(directory) / "item.json"
            payload = scan.core._canonical_file_bytes({"x": 1})
            path.write_bytes(payload)
            self.assertFalse(scan.core._sidecar(path).exists())
            digest = scan.core._write_pinned_json(path, {"x": 1})
            self.assertEqual(
                scan.core._sidecar(path).read_text(encoding="ascii").strip(),
                digest,
            )

    def test_sidecar_without_json_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=scan.RUN_ROOT) as directory:
            path = Path(directory) / "item.json"
            scan.core._sidecar(path).write_text("0" * 64 + "\n", encoding="ascii")
            with self.assertRaises(scan.core.BakeoffError):
                scan.core._load_pinned_json(path)


if __name__ == "__main__":
    unittest.main()
