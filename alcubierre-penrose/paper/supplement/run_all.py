"""Run the supplementary verification scripts for the Alcubierre paper.

The scripts write human-readable outputs under scripts/output/sech and regenerate
the conformal-diagram figure under the paper's figures directory.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent / "scripts"

SCRIPTS = [
    "front_tip_adm_derivation.py",
    "front_tip_full_parallel_frame.py",
    "front_tip_scalar_invariants.py",
    "front_tip_general_convex_wall.py",
    "front_tip_einstein_parallel_frame.py",
    "flat_cap_partial_extension.py",
    "natario_local_jet.py",
    "front_tip_taylor_metric_check.py",
    "front_tip_numerical_frame_check.py",
    "front_tip_parallel_tidal_analytic.py",
    "diagram_derivation_overlay.py",
]


def main() -> int:
    for script in SCRIPTS:
        print(f"\n=== {script} ===", flush=True)
        subprocess.run([sys.executable, script], cwd=SCRIPT_DIR, check=True)
    print("\nAll supplementary checks completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
