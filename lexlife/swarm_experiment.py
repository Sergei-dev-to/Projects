from __future__ import annotations

import argparse
from pathlib import Path

from config_utils import load_config
from swarm_world import SwarmWorld


def render_atoms(world: SwarmWorld, field: str) -> str:
    chars = "0123"
    rows: list[str] = []
    for y in range(world.height):
        row: list[str] = []
        for x in range(world.width):
            atom = world.grid.get((x, y))
            if atom is None:
                row.append(".")
                continue
            if field == "emission":
                row.append(chars[atom.emission])
            elif field == "prediction":
                row.append(chars[atom.prediction])
            else:
                row.append("?")
        rows.append("".join(row))
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the swarm-specific disturbance/repair experiment.")
    parser.add_argument("--config", type=Path, default=Path("swarm_config.yaml"))
    parser.add_argument("--diagnostics", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    world = SwarmWorld(config)
    world.seed_initial_population()

    print("Initial emissions")
    print(render_atoms(world, "emission"))
    print()

    for _ in range(int(config["steps"])):
        metrics = world.step()
        if (
            metrics.tick == 1
            or metrics.tick % int(config["snapshot_interval"]) == 0
            or metrics.tick == int(config["steps"])
        ):
            prediction_accuracy = 0.0
            if metrics.population > 0:
                prediction_accuracy = metrics.matching_predictions / max(1, metrics.population)
            print(
                f"tick={metrics.tick:>2} "
                f"phase={metrics.phase:<11} "
                f"population={metrics.population:>3} "
                f"largest_cluster={metrics.largest_cluster:>3} "
                f"components={metrics.component_count:>3} "
                f"in_region={metrics.in_region_population:>3} "
                f"out_region={metrics.out_region_population:>3} "
                f"accuracy={prediction_accuracy:.2f} "
                f"mismatch={metrics.mismatching_atoms:>3} "
                f"disturbance_contacts={metrics.disturbance_contacts:>3}"
            )
            print(render_atoms(world, "emission"))
            print()
            if args.diagnostics:
                print("Predictions")
                print(render_atoms(world, "prediction"))
                print()


if __name__ == "__main__":
    main()
