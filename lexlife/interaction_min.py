from __future__ import annotations

from lexocyte_min import Lexocyte


Coord = tuple[int, int]


def dominant_token(tokens: list[int], silence_token: int) -> int:
    if not tokens:
        return silence_token
    counts: dict[int, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return max(sorted(counts), key=lambda token: counts[token])


def mixed_token(tokens: list[int], silence_token: int, vocab_size: int) -> int:
    if not tokens:
        return silence_token
    counts: dict[int, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    dominant = max(sorted(counts), key=lambda token: counts[token])
    dominant_count = counts[dominant]
    if dominant_count == len(tokens):
        return dominant
    # Remap mixed neighborhoods into the upper half of the vocabulary.
    return (dominant + max(1, vocab_size // 2)) % vocab_size


class GridInteraction:
    def __init__(
        self,
        width: int,
        height: int,
        silence_token: int = 0,
        encoder_mode: str = "mode",
        vocab_size: int = 4,
    ) -> None:
        self.width = width
        self.height = height
        self.silence_token = silence_token
        self.encoder_mode = encoder_mode
        self.vocab_size = vocab_size

    def in_bounds(self, coord: Coord) -> bool:
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def neighborhood(self, coord: Coord) -> list[Coord]:
        x, y = coord
        neighbors: list[Coord] = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                target = (x + dx, y + dy)
                if self.in_bounds(target):
                    neighbors.append(target)
        return neighbors

    def encode(self, grid: dict[Coord, Lexocyte]) -> dict[Coord, int]:
        observations: dict[Coord, int] = {}
        for coord in grid:
            tokens: list[int] = []
            for neighbor in self.neighborhood(coord):
                cell = grid.get(neighbor)
                if cell is not None:
                    tokens.append(cell.emission)
            observations[coord] = self.encode_tokens(tokens)
        return observations

    def encode_tokens(self, tokens: list[int]) -> int:
        if self.encoder_mode == "mode":
            return dominant_token(tokens, self.silence_token)
        if self.encoder_mode == "mode_mixed":
            return mixed_token(tokens, self.silence_token, self.vocab_size)
        raise ValueError(f"unknown encoder_mode: {self.encoder_mode}")
