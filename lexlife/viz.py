from __future__ import annotations

from world_min import WorldMin


SYMBOL_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def render_field(world: WorldMin, field: str) -> str:
    rows: list[str] = []
    for y in range(world.height):
        chars: list[str] = []
        for x in range(world.width):
            cell = world.grid.get((x, y))
            if cell is None:
                chars.append(".")
                continue
            if field == "emission":
                chars.append(SYMBOL_CHARS[cell.emission])
            elif field == "prediction":
                chars.append(SYMBOL_CHARS[cell.prediction])
            elif field == "observation":
                chars.append(SYMBOL_CHARS[world.observations.get((x, y), int(world.config.get("silence_token", 0)))])
            else:
                raise ValueError(f"unknown field: {field}")
        rows.append("".join(chars))
    return "\n".join(rows)


def render_emissions(world: WorldMin) -> str:
    return render_field(world, "emission")


def render_predictions(world: WorldMin) -> str:
    return render_field(world, "prediction")


def render_observations(world: WorldMin) -> str:
    return render_field(world, "observation")
