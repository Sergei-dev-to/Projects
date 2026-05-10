from __future__ import annotations

from dataclasses import dataclass
import random

from swarm_atom import SwarmAtom, initial_atom, step_atom


Coord = tuple[int, int]


@dataclass
class SwarmStepMetrics:
    tick: int
    phase: str
    population: int
    largest_cluster: int
    component_count: int
    in_region_population: int
    out_region_population: int
    matching_predictions: int
    disturbance_contacts: int
    mismatching_atoms: int


class SwarmWorld:
    def __init__(self, config: dict[str, int | float | str]) -> None:
        self.config = config
        self.width = int(config["grid_width"])
        self.height = int(config["grid_height"])
        self.rng = random.Random(int(config["seed"]))
        self.grid: dict[Coord, SwarmAtom] = {}
        self.tick = 0

        self.region_center = (
            int(config.get("region_center_x", self.width // 2)),
            int(config.get("region_center_y", self.height // 2)),
        )
        self.region_radius = int(config.get("region_radius", 3))
        self.disturbance_radius = int(config.get("disturbance_radius", self.region_radius + 3))
        self.disturbance_start = int(config.get("disturbance_start", 6))
        self.disturbance_end = int(config.get("disturbance_end", 12))
        self.damage_step = int(config.get("damage_step", 18))
        self.damage_fraction = float(config.get("damage_fraction", 0.4))

    def seed_initial_population(self) -> None:
        while len(self.grid) < int(self.config["initial_population"]):
            coord = (self.rng.randrange(self.width), self.rng.randrange(self.height))
            if coord in self.grid:
                continue
            self.grid[coord] = initial_atom()

    def in_bounds(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbors(self, coord: Coord) -> list[Coord]:
        x, y = coord
        results: list[Coord] = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                target = (x + dx, y + dy)
                if self.in_bounds(target):
                    results.append(target)
        return results

    def in_region(self, coord: Coord) -> bool:
        dx = coord[0] - self.region_center[0]
        dy = coord[1] - self.region_center[1]
        return (dx * dx) + (dy * dy) <= (self.region_radius * self.region_radius)

    def disturbance_active(self) -> bool:
        return self.disturbance_start <= (self.tick + 1) <= self.disturbance_end

    def disturbance_visible(self, coord: Coord) -> bool:
        dx = coord[0] - self.region_center[0]
        dy = coord[1] - self.region_center[1]
        return (dx * dx) + (dy * dy) <= (self.disturbance_radius * self.disturbance_radius)

    def phase_for_tick(self, tick_value: int) -> str:
        if self.disturbance_start <= tick_value <= self.disturbance_end:
            return "disturbance"
        if tick_value == self.damage_step:
            return "damage"
        if tick_value > self.damage_step:
            return "recovery"
        return "baseline"

    def region_populations(self) -> tuple[int, int]:
        inside = sum(1 for coord in self.grid if self.in_region(coord))
        return inside, len(self.grid) - inside

    def dominant_neighbor_emission(self, coord: Coord) -> int:
        counts: dict[int, int] = {}
        for neighbor in self.neighbors(coord):
            atom = self.grid.get(neighbor)
            if atom is None:
                continue
            counts[atom.emission] = counts.get(atom.emission, 0) + 1
        if not counts:
            return 0
        return max(sorted(counts), key=lambda token: counts[token])

    def neighbor_profile(self, coord: Coord) -> tuple[int, int]:
        counts: dict[int, int] = {}
        neighbor_count = 0
        for neighbor in self.neighbors(coord):
            atom = self.grid.get(neighbor)
            if atom is None:
                continue
            neighbor_count += 1
            counts[atom.emission] = counts.get(atom.emission, 0) + 1
        dominant_count = max(counts.values(), default=0)
        return neighbor_count, dominant_count

    def observation_for(self, coord: Coord) -> int:
        if self.disturbance_active() and self.disturbance_visible(coord):
            return 3
        neighbor_count, dominant_count = self.neighbor_profile(coord)
        if neighbor_count <= 1:
            return 0
        if dominant_count >= max(2, neighbor_count - 1):
            return 2
        return 1

    def local_density(self, coord: Coord, positions: set[Coord]) -> int:
        return sum(1 for neighbor in self.neighbors(coord) if neighbor in positions)

    def pull_to_region(self, coord: Coord) -> float:
        dx = abs(coord[0] - self.region_center[0])
        dy = abs(coord[1] - self.region_center[1])
        return -float(dx + dy)

    def movement_score(self, atom: SwarmAtom, target: Coord, occupied: set[Coord]) -> float:
        density = self.local_density(target, occupied)
        alarm, cohesion, spread = atom.hidden
        mismatch = atom.mismatch
        score = 0.6 * cohesion * density
        score -= 0.45 * spread * density
        score += 0.9 * alarm * self.pull_to_region(target)
        score += 0.75 * mismatch * density
        if self.disturbance_active() and self.disturbance_visible(target):
            score += 1.2 + (0.4 * alarm) + (0.9 * mismatch)
        elif not self.disturbance_active():
            score += 0.25 * cohesion * self.pull_to_region(target)
        if mismatch > 0:
            score += 1.1 * self.pull_to_region(target)
            if self.in_region(target):
                score += 0.8
        if atom.emission == 3:
            score += 0.8 + (0.4 * mismatch)
        elif atom.emission == 2:
            score += 0.4
        else:
            score += 0.2 * spread
        return score

    def move_atoms(self, updated: dict[Coord, SwarmAtom]) -> dict[Coord, SwarmAtom]:
        occupied = set(updated)
        proposals: list[tuple[float, Coord, Coord, SwarmAtom]] = []
        for coord, atom in updated.items():
            candidate_coords = [coord]
            for neighbor in self.neighbors(coord):
                if neighbor not in occupied:
                    candidate_coords.append(neighbor)
            best_score = None
            best_target = coord
            for target in candidate_coords:
                score = self.movement_score(atom, target, occupied)
                score += self.rng.uniform(-0.05, 0.05)
                if best_score is None or score > best_score:
                    best_score = score
                    best_target = target
            proposals.append((best_score or 0.0, coord, best_target, atom))

        proposals.sort(reverse=True)
        next_grid: dict[Coord, SwarmAtom] = {}
        used_targets: set[Coord] = set()
        for _, origin, target, atom in proposals:
            chosen = target if target not in used_targets else origin
            if chosen in used_targets:
                continue
            next_grid[chosen] = atom
            used_targets.add(chosen)
        return next_grid

    def apply_damage(self) -> None:
        if self.tick != self.damage_step:
            return
        region_coords = [coord for coord in self.grid if self.in_region(coord)]
        if not region_coords:
            return
        remove_count = max(1, int(len(region_coords) * self.damage_fraction))
        self.rng.shuffle(region_coords)
        for coord in region_coords[:remove_count]:
            self.grid.pop(coord, None)

    def connected_components(self) -> list[set[Coord]]:
        remaining = set(self.grid)
        components: list[set[Coord]] = []
        while remaining:
            start = remaining.pop()
            stack = [start]
            component = {start}
            while stack:
                coord = stack.pop()
                for neighbor in self.neighbors(coord):
                    if neighbor in remaining and neighbor in self.grid:
                        remaining.remove(neighbor)
                        component.add(neighbor)
                        stack.append(neighbor)
            components.append(component)
        return components

    def largest_cluster(self) -> int:
        components = self.connected_components()
        if not components:
            return 0
        return max(len(component) for component in components)

    def step(self) -> SwarmStepMetrics:
        phase = self.phase_for_tick(self.tick + 1)
        observations = {coord: self.observation_for(coord) for coord in self.grid}
        matching_predictions = 0
        disturbance_contacts = 0
        mismatching_atoms = 0
        updated: dict[Coord, SwarmAtom] = {}

        for coord, atom in self.grid.items():
            observed = observations[coord]
            matching_predictions += 1 if atom.prediction == observed else 0
            mismatching_atoms += 1 if atom.prediction != observed else 0
            disturbance_contacts += 1 if observed == 3 else 0
            updated[coord] = step_atom(atom, observed)

        self.grid = self.move_atoms(updated)
        self.tick += 1
        self.apply_damage()
        inside, outside = self.region_populations()

        components = self.connected_components()
        return SwarmStepMetrics(
            tick=self.tick,
            phase=phase,
            population=len(self.grid),
            largest_cluster=max((len(component) for component in components), default=0),
            component_count=len(components),
            in_region_population=inside,
            out_region_population=outside,
            matching_predictions=matching_predictions,
            disturbance_contacts=disturbance_contacts,
            mismatching_atoms=mismatching_atoms,
        )
