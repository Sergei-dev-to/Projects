from __future__ import annotations

from world_min import StepMetrics, WorldMin


def format_token_counts(counts: dict[int, int]) -> str:
    return " ".join(f"{token}:{count}" for token, count in sorted(counts.items()))


def summarize_step(world: WorldMin, step_metrics: StepMetrics) -> dict[str, float]:
    total_viability = sum(world.viability.values())
    if step_metrics.evaluated == 0:
        prediction_accuracy = 0.0
        isolation_ratio = 0.0
    else:
        prediction_accuracy = 1 - (step_metrics.prediction_errors / step_metrics.evaluated)
        isolation_ratio = step_metrics.isolated / step_metrics.evaluated
    if step_metrics.population == 0:
        avg_viability = 0.0
    else:
        avg_viability = total_viability / step_metrics.population
    return {
        "tick": world.tick,
        "evaluated": step_metrics.evaluated,
        "population": step_metrics.population,
        "deaths": step_metrics.deaths,
        "prediction_accuracy": prediction_accuracy,
        "avg_viability": avg_viability,
        "isolation_ratio": isolation_ratio,
        "largest_cluster": step_metrics.largest_cluster,
        "component_count": step_metrics.component_count,
        "in_region_population": step_metrics.in_region_population,
        "out_region_population": step_metrics.out_region_population,
        "event_phase": step_metrics.event_phase,
        "emission_counts": format_token_counts(world.token_counts("emission")),
        "prediction_counts": format_token_counts(world.token_counts("prediction")),
        "observation_counts": format_token_counts(world.token_counts("observation")),
    }
