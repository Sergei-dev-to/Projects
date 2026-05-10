from __future__ import annotations

from dataclasses import dataclass
import math


Vector = list[float]
Coord = tuple[int, int]


@dataclass(frozen=True)
class SwarmAtom:
    hidden: Vector
    prediction: int
    emission: int
    mismatch: float
    age: int = 0


VOCAB_SIZE = 4
HIDDEN_SIZE = 3

# Weak shared dynamics: interchangeable atoms with small internal memory.
OBS_EMBEDDINGS: dict[int, Vector] = {
    0: [-0.25, -0.20, 0.45],  # sparse / broken neighborhood
    1: [0.00, 0.15, 0.10],    # mixed / transitional neighborhood
    2: [0.20, 0.55, -0.20],   # coherent local structure
    3: [1.10, 0.55, -0.35],   # active disturbance
}

RECURRENT_WEIGHTS: list[list[float]] = [
    [0.70, 0.15, -0.05],
    [0.10, 0.82, -0.10],
    [-0.05, -0.10, 0.68],
]

EMISSION_HEAD: list[list[float]] = [
    [-0.75, -0.85, 0.90],   # calm / drift
    [0.10, -0.10, 0.60],    # scout / activity
    [0.35, 1.05, -0.25],    # cohesion
    [1.20, 0.35, -0.40],    # alert / repair
]

PREDICTION_HEAD: list[list[float]] = [
    [-0.35, -0.40, 0.40],
    [0.10, 0.20, 0.25],
    [0.20, 0.90, -0.10],
    [1.00, 0.20, -0.20],
]

MATCH_SIGNAL: dict[int, Vector] = {
    0: [-0.10, 0.05, 0.05],   # local world behaved as expected
    1: [0.90, 0.25, -0.20],   # expectation violated
}


def dot(left: Vector, right: Vector) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def matvec(matrix: list[list[float]], vector: Vector) -> Vector:
    return [dot(row, vector) for row in matrix]


def add(left: Vector, right: Vector) -> Vector:
    return [a + b for a, b in zip(left, right, strict=True)]


def tanh_vector(values: Vector) -> Vector:
    return [math.tanh(value) for value in values]


def argmax(values: Vector) -> int:
    return max(range(len(values)), key=lambda index: (values[index], -index))


def initial_atom() -> SwarmAtom:
    return SwarmAtom(hidden=[0.0, 0.0, 0.4], prediction=0, emission=0, mismatch=0.0, age=0)


def step_atom(atom: SwarmAtom, observed_token: int) -> SwarmAtom:
    mismatch = 1 if atom.prediction != observed_token else 0
    observation = OBS_EMBEDDINGS[observed_token]
    match_signal = MATCH_SIGNAL[mismatch]
    recurrent = matvec(RECURRENT_WEIGHTS, atom.hidden)
    next_hidden = tanh_vector(add(add(recurrent, observation), match_signal))
    next_prediction = argmax(matvec(PREDICTION_HEAD, next_hidden))
    next_emission = argmax(matvec(EMISSION_HEAD, next_hidden))
    return SwarmAtom(
        hidden=next_hidden,
        prediction=next_prediction,
        emission=next_emission,
        mismatch=float(mismatch),
        age=atom.age + 1,
    )
