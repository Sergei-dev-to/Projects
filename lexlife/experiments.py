from __future__ import annotations

import argparse
from pathlib import Path

from config_utils import load_config
from metrics import summarize_step
from viz import render_emissions, render_observations, render_predictions
from world_min import WorldMin


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the lexlife take-one simulator.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to the config file.",
    )
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="Show prediction and observation fields at each snapshot.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    world = WorldMin(config)
    world.seed_initial_population()

    print("Initial field")
    print(render_emissions(world))
    print()
    if args.diagnostics:
        print("Initial predictions")
        print(render_predictions(world))
        print()
        print("Initial observations")
        print(render_observations(world))
        print()

    for _ in range(config["steps"]):
        metrics = summarize_step(world, world.step())
        if (
            world.tick == 1
            or world.tick % config["snapshot_interval"] == 0
            or world.tick == config["steps"]
        ):
            print(
                f"tick={metrics['tick']:>2.0f} "
                f"phase={metrics['event_phase']:<11} "
                f"population={metrics['population']:>3.0f} "
                f"deaths={metrics['deaths']:>2.0f} "
                f"accuracy={metrics['prediction_accuracy']:.2f} "
                f"avg_viability={metrics['avg_viability']:.2f} "
                f"isolation={metrics['isolation_ratio']:.2f} "
                f"largest_cluster={metrics['largest_cluster']:>3.0f} "
                f"components={metrics['component_count']:>3.0f} "
                f"in_region={metrics['in_region_population']:>3.0f} "
                f"out_region={metrics['out_region_population']:>3.0f}"
            )
            print(f"emissions   {metrics['emission_counts']}")
            print(f"predictions {metrics['prediction_counts']}")
            print(f"observations {metrics['observation_counts']}")
            print(render_emissions(world))
            print()
            if args.diagnostics:
                print("Predictions")
                print(render_predictions(world))
                print()
                print("Observations")
                print(render_observations(world))
                print()


if __name__ == "__main__":
    main()
