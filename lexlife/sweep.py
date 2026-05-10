from __future__ import annotations

import argparse
import itertools
from pathlib import Path

from config_utils import load_config
from world_min import WorldMin


def run_world(config: dict[str, int | float | str]) -> dict[str, int | float | str]:
    world = WorldMin(config)
    world.seed_initial_population()
    peak_population = len(world.grid)
    peak_cluster = world.largest_cluster_size()
    for _ in range(int(config["steps"])):
        world.step()
        peak_population = max(peak_population, len(world.grid))
        peak_cluster = max(peak_cluster, world.largest_cluster_size())
        if not world.grid:
            break

    final_population = len(world.grid)
    final_cluster = world.largest_cluster_size()
    avg_viability = 0.0
    if world.viability:
        avg_viability = sum(world.viability.values()) / len(world.viability)

    return {
        "seed": int(config["seed"]),
        "encoder_mode": str(config["encoder_mode"]),
        "initial_population": int(config["initial_population"]),
        "final_population": final_population,
        "peak_population": peak_population,
        "final_cluster": final_cluster,
        "peak_cluster": peak_cluster,
        "avg_viability": round(avg_viability, 2),
        "in_region": world.region_populations()[0],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep world-min configurations.")
    parser.add_argument("--config", type=Path, default=Path("config.yaml"))
    parser.add_argument("--seeds", nargs="*", type=int, default=[1, 2, 3, 4, 5])
    parser.add_argument("--populations", nargs="*", type=int, default=[48, 64, 80])
    parser.add_argument(
        "--encoders",
        nargs="*",
        default=["mode", "mode_mixed"],
        help="Encoder modes to sweep.",
    )
    parser.add_argument("--top", type=int, default=10, help="How many top rows to print.")
    args = parser.parse_args()

    base_config = load_config(args.config)
    results: list[dict[str, int | float | str]] = []

    for seed, population, encoder in itertools.product(args.seeds, args.populations, args.encoders):
        config = dict(base_config)
        config["seed"] = seed
        config["initial_population"] = population
        config["encoder_mode"] = encoder
        results.append(run_world(config))

    results.sort(
        key=lambda row: (
            int(row["final_population"]),
            int(row["final_cluster"]),
            int(row["peak_population"]),
            float(row["avg_viability"]),
        ),
        reverse=True,
    )

    print("seed encoder     init final peak cluster peak_cl in_reg avg_v")
    for row in results[: args.top]:
        print(
            f"{int(row['seed']):>4} "
            f"{str(row['encoder_mode']):<11} "
            f"{int(row['initial_population']):>4} "
            f"{int(row['final_population']):>5} "
            f"{int(row['peak_population']):>4} "
            f"{int(row['final_cluster']):>7} "
            f"{int(row['peak_cluster']):>7} "
            f"{int(row['in_region']):>6} "
            f"{float(row['avg_viability']):>5.2f}"
        )


if __name__ == "__main__":
    main()
