from __future__ import annotations

from dataclasses import dataclass
import math
import random


Vector = list[float]
Matrix = list[list[float]]


@dataclass(frozen=True)
class Lexocyte:
    hidden: Vector
    prediction: int
    emission: int
    token_embedding: Matrix
    hidden_weights: Matrix
    input_weights: Matrix
    hidden_bias: Vector
    prediction_head: Matrix
    prediction_bias: Vector
    emission_head: Matrix
    emission_bias: Vector
    age: int = 0


def dot(left: Vector, right: Vector) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [dot(row, vector) for row in matrix]


def add(left: Vector, right: Vector) -> Vector:
    return [a + b for a, b in zip(left, right, strict=True)]


def tanh_vector(values: Vector) -> Vector:
    return [math.tanh(value) for value in values]


def argmax(values: Vector) -> int:
    return max(range(len(values)), key=lambda index: (values[index], -index))


def random_vector(rng: random.Random, size: int, scale: float) -> Vector:
    return [rng.uniform(-scale, scale) for _ in range(size)]


def random_matrix(rng: random.Random, rows: int, cols: int, scale: float) -> Matrix:
    return [random_vector(rng, cols, scale) for _ in range(rows)]


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high))


def initial_lexocyte(
    rng: random.Random,
    config: dict[str, int | float],
) -> Lexocyte:
    hidden_size = int(config["hidden_size"])
    vocab_size = int(config["vocab_size"])
    embedding_size = int(config["embedding_size"])
    weight_scale = float(config["weight_scale"])

    token_embedding = random_matrix(rng, vocab_size, embedding_size, weight_scale)
    hidden_weights = random_matrix(rng, hidden_size, hidden_size, weight_scale)
    input_weights = random_matrix(rng, hidden_size, embedding_size, weight_scale)
    hidden_bias = random_vector(rng, hidden_size, weight_scale)
    prediction_head = random_matrix(rng, vocab_size, hidden_size, weight_scale)
    prediction_bias = random_vector(rng, vocab_size, weight_scale)
    emission_head = random_matrix(rng, vocab_size, hidden_size, weight_scale)
    emission_bias = random_vector(rng, vocab_size, weight_scale)

    hidden = random_vector(rng, hidden_size, weight_scale)
    prediction = rng.randrange(vocab_size)
    emission = rng.randrange(vocab_size)

    return Lexocyte(
        hidden=hidden,
        prediction=prediction,
        emission=emission,
        token_embedding=token_embedding,
        hidden_weights=hidden_weights,
        input_weights=input_weights,
        hidden_bias=hidden_bias,
        prediction_head=prediction_head,
        prediction_bias=prediction_bias,
        emission_head=emission_head,
        emission_bias=emission_bias,
        age=0,
    )


def step_lexocyte(cell: Lexocyte, observed_token: int) -> Lexocyte:
    observed_embedding = cell.token_embedding[observed_token]
    hidden_from_hidden = matvec(cell.hidden_weights, cell.hidden)
    hidden_from_input = matvec(cell.input_weights, observed_embedding)
    next_hidden = tanh_vector(add(add(hidden_from_hidden, hidden_from_input), cell.hidden_bias))

    prediction_logits = add(matvec(cell.prediction_head, next_hidden), cell.prediction_bias)
    emission_logits = add(matvec(cell.emission_head, next_hidden), cell.emission_bias)

    return Lexocyte(
        hidden=next_hidden,
        prediction=argmax(prediction_logits),
        emission=argmax(emission_logits),
        token_embedding=cell.token_embedding,
        hidden_weights=cell.hidden_weights,
        input_weights=cell.input_weights,
        hidden_bias=cell.hidden_bias,
        prediction_head=cell.prediction_head,
        prediction_bias=cell.prediction_bias,
        emission_head=cell.emission_head,
        emission_bias=cell.emission_bias,
        age=cell.age + 1,
    )
