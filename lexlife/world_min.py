from __future__ import annotations

from dataclasses import dataclass
import random

from interaction_min import Coord, GridInteraction
from lexocyte_min import Lexocyte, clamp, initial_lexocyte, step_lexocyte


@dataclass
class StepMetrics:
    evaluated: int
    population: int
    deaths: int
    prediction_errors: int
    isolated: int
    largest_cluster: int
    component_count: int
    in_region_population: int
    out_region_population: int
    event_phase: str


class WorldMin:
    def __init__(self, config: dict[str, int | float]) -> None:
        self.config = config
        self.width = int(config["grid_width"])
        self.height = int(config["grid_height"])
        self.rng = random.Random(int(config["seed"]))
        self.grid: dict[Coord, Lexocyte] = {}
        self.viability: dict[Coord, int] = {}
        self.tick = 0
        self.interaction = GridInteraction(
            width=self.width,
            height=self.height,
            silence_token=int(config.get("silence_token", 0)),
            encoder_mode=str(config.get("encoder_mode", "mode")),
            vocab_size=int(config["vocab_size"]),
        )
        self.observations: dict[Coord, int] = {}
        self.region_center = (
            int(config.get("region_center_x", self.width // 2)),
            int(config.get("region_center_y", self.height // 2)),
        )
        self.region_radius = int(config.get("region_radius", 3))
        self.disturbance_start = int(config.get("disturbance_start", 0))
        self.disturbance_end = int(config.get("disturbance_end", 0))
        self.damage_step = int(config.get("damage_step", 0))
        self.damage_fraction = float(config.get("damage_fraction", 0.0))

    def seed_initial_population(self) -> None:
        while len(self.grid) < int(self.config["initial_population"]):
            coord = (self.rng.randrange(self.width), self.rng.randrange(self.height))
            if coord in self.grid:
                continue
            self.grid[coord] = initial_lexocyte(self.rng, self.config)
            self.viability[coord] = int(self.config["initial_viability"])
        self.observations = self.interaction.encode(self.grid)

    def token_counts(self, field: str) -> dict[int, int]:
        counts = {token: 0 for token in range(int(self.config["vocab_size"]))}
        if field == "emission":
            for cell in self.grid.values():
                counts[cell.emission] += 1
            return counts
        if field == "prediction":
            for cell in self.grid.values():
                counts[cell.prediction] += 1
            return counts
        if field == "observation":
            for token in self.observations.values():
                counts[token] += 1
            return counts
        raise ValueError(f"unknown field: {field}")

    def count_neighbors(self, coord: Coord, grid: dict[Coord, Lexocyte]) -> int:
        return sum(1 for neighbor in self.interaction.neighborhood(coord) if neighbor in grid)

    def connected_components(self) -> list[set[Coord]]:
        remaining = set(self.grid)
        components: list[set[Coord]] = []
        while remaining:
            start = remaining.pop()
            stack = [start]
            component = {start}
            while stack:
                coord = stack.pop()
                for neighbor in self.interaction.neighborhood(coord):
                    if neighbor in remaining and neighbor in self.grid:
                        remaining.remove(neighbor)
                        component.add(neighbor)
                        stack.append(neighbor)
            components.append(component)
        return components

    def largest_cluster_size(self) -> int:
        components = self.connected_components()
        if not components:
            return 0
        return max(len(component) for component in components)

    def component_count(self) -> int:
        return len(self.connected_components())

    def in_region(self, coord: Coord) -> bool:
        dx = coord[0] - self.region_center[0]
        dy = coord[1] - self.region_center[1]
        return (dx * dx) + (dy * dy) <= (self.region_radius * self.region_radius)

    def region_populations(self) -> tuple[int, int]:
        inside = sum(1 for coord in self.grid if self.in_region(coord))
        outside = len(self.grid) - inside
        return inside, outside

    def event_phase(self) -> str:
        next_tick = self.tick + 1
        if self.disturbance_start and self.disturbance_start <= next_tick <= self.disturbance_end:
            return "disturbance"
        if self.damage_step and next_tick == self.damage_step:
            return "damage"
        return "baseline"

    def support_for_neighbors(self, neighbor_count: int) -> int:
        support_key = f"support_{neighbor_count}"
        if support_key in self.config:
            return int(self.config[support_key])
        return int(self.config.get("support_default", 0))

    def next_viability(
        self,
        current_viability: int,
        prediction: int,
        observed_token: int,
        neighbor_count: int,
        disturbed: bool,
    ) -> tuple[int, bool]:
        correct = prediction == observed_token
        value = current_viability - int(self.config["maintenance_decay"])
        value += self.support_for_neighbors(neighbor_count)
        if not correct:
            value -= int(self.config["mismatch_cost"])
        if disturbed:
            value += int(self.config.get("disturbance_support", 0))
        return clamp(value, 0, int(self.config["max_viability"])), (not correct)

    def apply_damage(self) -> None:
        if not self.damage_step or self.tick != self.damage_step:
            return
        region_coords = [coord for coord in self.grid if self.in_region(coord)]
        if not region_coords:
            return
        remove_count = max(1, int(len(region_coords) * self.damage_fraction))
        self.rng.shuffle(region_coords)
        for coord in region_coords[:remove_count]:
            self.grid.pop(coord, None)
            self.viability.pop(coord, None)
        self.observations = self.interaction.encode(self.grid)

    def step(self) -> StepMetrics:
        current_observations = self.observations or self.interaction.encode(self.grid)

        provisional_grid: dict[Coord, Lexocyte] = {}
        for coord, cell in sorted(self.grid.items()):
            observed_token = current_observations.get(coord, int(self.config.get("silence_token", 0)))
            provisional_grid[coord] = step_lexocyte(cell, observed_token)

        next_observations = self.interaction.encode(provisional_grid)

        survivors: dict[Coord, Lexocyte] = {}
        next_viability: dict[Coord, int] = {}
        deaths = 0
        prediction_errors = 0
        isolated = 0

        for coord, cell in provisional_grid.items():
            observed_token = next_observations.get(
                coord,
                int(self.config.get("silence_token", 0)),
            )
            neighbor_count = self.count_neighbors(coord, provisional_grid)
            viability, mismatch = self.next_viability(
                current_viability=self.viability[coord],
                prediction=cell.prediction,
                observed_token=observed_token,
                neighbor_count=neighbor_count,
                disturbed=self.disturbance_start <= (self.tick + 1) <= self.disturbance_end and self.in_region(coord),
            )
            prediction_errors += 1 if mismatch else 0
            isolated += 1 if neighbor_count == 0 else 0
            if viability <= 0:
                deaths += 1
                continue
            survivors[coord] = cell
            next_viability[coord] = viability

        self.grid = survivors
        self.viability = next_viability
        self.observations = self.interaction.encode(self.grid)
        self.tick += 1
        self.apply_damage()
        inside, outside = self.region_populations()

        return StepMetrics(
            evaluated=len(provisional_grid),
            population=len(self.grid),
            deaths=deaths,
            prediction_errors=prediction_errors,
            isolated=isolated,
            largest_cluster=self.largest_cluster_size(),
            component_count=self.component_count(),
            in_region_population=inside,
            out_region_population=outside,
            event_phase=self.event_phase(),
        )
