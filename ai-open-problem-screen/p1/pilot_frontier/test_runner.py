"""Tests for real evaluation, immutable chunks, and intentional stop/resume."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .runner import (
    B0_7_EXPECTED_STRUCTURAL_COUNT,
    FrontierError,
    evaluate_item,
    initialize_run,
    make_plan,
    run_frontier,
    sha256_json,
    sha256_file,
    status,
    verify_run,
    _plan_digest,
    _validate_record,
)


class ScientificPilotTests(unittest.TestCase):
    def install_test_only_authorization(self, work_dir: Path) -> None:
        """Install a visibly non-scientific stand-in; validation is mocked.

        Production CLI evaluation has no bypass and is tested separately.  The
        stand-in lets unit tests exercise real lrcalc/chunk crash semantics even
        while another agent is rebuilding the hardened P1 evidence bundle.
        """

        (work_dir / "authorization.json").write_text(
            json.dumps({"test_only": True}), encoding="utf-8"
        )

    def test_b0_7_structural_plan_count_and_invariants(self) -> None:
        plan = make_plan(
            6,
            7,
            chunk_size=128,
            expected_structural_count=B0_7_EXPECTED_STRUCTURAL_COUNT,
        )
        self.assertEqual(len(plan["items"]), 18_287)
        self.assertEqual(plan["canonicalization"]["version"], "swap-only-v1")
        self.assertEqual(plan["evaluator"]["interpolation_mode"], "bounded")
        self.assertEqual(plan["outcome_label"], "not-outcome-B")
        self.assertFalse(plan["outcome_b_eligible"])
        self.assertTrue(all(item["lam"] <= item["mu"] for item in plan["items"]))
        self.assertEqual(plan["frozen_prefix"]["structural_triple_count"], 14_302)
        self.assertEqual(
            len(plan["items"]) - plan["frozen_prefix"]["structural_triple_count"],
            3_985,
        )
        self.assertEqual(plan["b0_7_expected_counts"]["new_nonzero"], 1_929)

    def test_real_new_length_six_record_has_separate_e1_e2_agreement(self) -> None:
        plan = make_plan(6, 7, chunk_size=8)
        target = next(
            item
            for item in plan["items"]
            if item["lam"] == []
            and item["mu"] == [1, 1, 1, 1, 1, 1]
            and item["nu"] == [1, 1, 1, 1, 1, 1]
        )
        self.assertEqual(target["provenance_class"], "new-extension")
        record = evaluate_item(plan, target)
        self.assertEqual(record["status"], "nonzero")
        self.assertEqual(record["canonical_polynomial"], ["1"])
        self.assertEqual(record["e1_record"]["evaluator"], "lrcalc-interp")
        self.assertEqual(record["e1_record"]["interpolation_mode"], "bounded")
        self.assertEqual(record["e1_record"]["raw_evidence"]["mode"], "bounded")
        self.assertEqual(
            record["e1_record"]["raw_evidence"]["checked_max_n"],
            record["e1_record"]["raw_evidence"]["degree_bound"] + 1,
        )
        self.assertEqual(record["e2_record"]["evaluator"], "normaliz-ehrhart")
        self.assertTrue(record["agreement_record"]["all_agree"])
        self.assertEqual(record["e1_record"]["canonical_polynomial"], ["1"])
        self.assertEqual(record["e2_record"]["canonical_polynomial"], ["1"])
        rows = record["e2_record"]["typed_input"]["normaliz"]["rows"]
        self.assertTrue(all(type(value) is int for row in rows for value in row))
        _validate_record(record, _plan_digest(plan), target)

        # Recompute all enclosing hashes after corrupting one Normaliz input
        # coefficient.  Semantic exact-integer validation must still reject it.
        tampered = deepcopy(record)
        tampered["e2_record"]["typed_input"]["normaliz"]["rows"][0][0] = True
        e2_core = {
            key: value
            for key, value in tampered["e2_record"].items()
            if key != "record_sha256"
        }
        tampered["e2_record"]["record_sha256"] = sha256_json(e2_core)
        tampered["agreement_record"]["e2_record_sha256"] = tampered["e2_record"]["record_sha256"]
        agreement_core = {
            key: value
            for key, value in tampered["agreement_record"].items()
            if key != "record_sha256"
        }
        tampered["agreement_record"]["record_sha256"] = sha256_json(agreement_core)
        record_core = {
            key: value for key, value in tampered.items() if key != "record_sha256"
        }
        tampered["record_sha256"] = sha256_json(record_core)
        with self.assertRaisesRegex(FrontierError, "bool, float, or non-exact"):
            _validate_record(tampered, _plan_digest(plan), target)

    def test_bool_partition_input_fails_closed_before_tools(self) -> None:
        plan = make_plan(2, 1, chunk_size=2)
        item = dict(plan["items"][0])
        item.update({
            "lam": [True],
            "mu": [],
            "nu": [1],
            "provenance_class": "new-extension",
        })
        core = {
            key: item[key]
            for key in ("ordinal", "lam", "mu", "nu", "provenance_class")
        }
        item["work_sha256"] = sha256_json(core)
        with self.assertRaisesRegex(FrontierError, "bool, float, or non-exact"):
            evaluate_item(plan, item)

    def test_run_requires_frozen_p1_authorization(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work_dir = Path(temporary)
            initialize_run(
                work_dir,
                maximum_length=2,
                maximum_size=1,
                chunk_size=2,
            )
            with self.assertRaisesRegex(FrontierError, "not authorized"):
                run_frontier(work_dir, max_chunks=1)

    def test_intentional_stop_checkpoint_loss_resume_and_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work_dir = Path(temporary)
            initial = initialize_run(
                work_dir,
                maximum_length=3,
                maximum_size=3,
                chunk_size=3,
                champion_limit=10,
            )
            self.assertTrue(initial["partial"])
            self.assertEqual(initial["next_ordinal"], 0)
            self.install_test_only_authorization(work_dir)

            with patch(f"{run_frontier.__module__}._validate_authorization", return_value={}):
                stopped = run_frontier(work_dir, max_chunks=1)
            self.assertTrue(stopped["partial"])
            self.assertEqual(stopped["next_ordinal"], 3)
            self.assertFalse((work_dir / "completion.json").exists())
            self.assertEqual(stopped["outcome_label"], "not-outcome-B")
            self.assertNotIn("min_coefficient", stopped)
            self.assertNotIn("champions", stopped)
            first_prefix = stopped["prefix_sha256"]

            # Model the safe crash window after a chunk rename but before the
            # sidecar/checkpoint updates: the durable chunk remains the source
            # of truth and both derivative artifacts are reconstructed.
            (work_dir / "checkpoint.json").unlink()
            first_chunk = next((work_dir / "chunks").glob("*.json"))
            first_chunk.with_suffix(".json.sha256").unlink()
            with patch(f"{run_frontier.__module__}._validate_authorization", return_value={}):
                repaired = status(work_dir, repair_checkpoint=True)
            self.assertEqual(repaired["next_ordinal"], 3)
            self.assertEqual(repaired["prefix_sha256"], first_prefix)
            self.assertTrue(first_chunk.with_suffix(".json.sha256").exists())

            with patch(f"{run_frontier.__module__}._validate_authorization", return_value={}):
                complete = run_frontier(work_dir)
            self.assertTrue(complete["complete"])
            self.assertFalse(complete["partial"])
            self.assertEqual(sum(complete["counts"].values()), complete["structural_triple_count"])
            with patch(f"{run_frontier.__module__}._validate_authorization", return_value={}):
                verification = verify_run(work_dir)
            self.assertTrue(verification["valid"])
            self.assertTrue(verification["complete"])
            self.assertEqual(verification["prefix_sha256"], complete["prefix_sha256"])

            completion = json.loads((work_dir / "completion.json").read_text(encoding="utf-8"))
            self.assertEqual(completion["evidence_classification"], "partial-extension")
            self.assertEqual(completion["outcome_label"], "not-outcome-B")
            self.assertFalse(completion["outcome_b_eligible"])
            self.assertIn("min_coefficient", completion["summary"])
            self.assertIn("min_nonleading_coefficient", completion["summary"])
            self.assertEqual(completion["counts"]["error"], 0)
            sidecar = (work_dir / "completion.json.sha256").read_text(encoding="utf-8")
            self.assertEqual(sidecar, f"{sha256_file(work_dir / 'completion.json')}  completion.json\n")

            # A second narrow crash window can leave a valid immutable
            # completion without its digest sidecar; an authorized resume
            # reconstructs only that missing sidecar.
            (work_dir / "completion.json.sha256").unlink()
            with patch(f"{run_frontier.__module__}._validate_authorization", return_value={}):
                resumed_complete = run_frontier(work_dir, max_chunks=0)
            self.assertTrue(resumed_complete["complete"])
            self.assertTrue((work_dir / "completion.json.sha256").exists())

    def test_chunk_tampering_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            work_dir = Path(temporary)
            initialize_run(
                work_dir,
                maximum_length=2,
                maximum_size=2,
                chunk_size=2,
            )
            self.install_test_only_authorization(work_dir)
            with patch(f"{run_frontier.__module__}._validate_authorization", return_value={}):
                run_frontier(work_dir, max_chunks=1)
            chunk = next((work_dir / "chunks").glob("*.json"))
            data = json.loads(chunk.read_text(encoding="utf-8"))
            data["records"][0]["status"] = "error"
            chunk.write_text(json.dumps(data), encoding="utf-8")
            with patch(f"{run_frontier.__module__}._validate_authorization", return_value={}):
                with self.assertRaisesRegex(FrontierError, "payload digest mismatch|digest mismatch"):
                    verify_run(work_dir, require_complete=False)


if __name__ == "__main__":
    unittest.main()
