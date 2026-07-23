"""Canonical JSON, exact-rational, and SHA-256 helpers."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from .errors import ValidationError


def canonical_json_bytes(value: Any) -> bytes:
    """Return the campaign's canonical UTF-8 JSON representation."""

    try:
        encoded = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"value is not canonical-JSON serializable: {exc}") from exc
    return encoded.encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def canonical_fraction(value: object) -> str:
    """Validate and return a reduced Fraction string.

    This rejects alternate-but-equal spellings (``2/2``, ``+1``, ``1/01``), so
    equality of polynomial arrays is also equality of their serialized bytes.
    """

    if not isinstance(value, str) or not value:
        raise ValidationError("coefficient must be a non-empty string")
    try:
        fraction = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValidationError(f"invalid rational coefficient {value!r}") from exc
    normalized = str(fraction)
    if value != normalized:
        raise ValidationError(
            f"non-canonical rational coefficient {value!r}; expected {normalized!r}"
        )
    return normalized
