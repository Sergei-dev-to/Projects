"""Durable atomic file replacement helpers."""

from __future__ import annotations

import json
import os
import secrets
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes
from .errors import ControlError, ValidationError


def atomic_write_bytes(path: Path, payload: bytes, *, overwrite: bool = True) -> None:
    """Write *payload* via fsync + same-directory ``os.replace``.

    The parent directory must already exist.  Requiring callers to create the
    intended directory explicitly avoids a typo silently creating a new control
    tree.  ``overwrite=False`` is used for immutable artifacts.
    """

    path = Path(path)
    parent = path.parent
    if not parent.is_dir():
        raise ControlError(f"parent directory does not exist: {parent}")
    if not overwrite and path.exists():
        raise ControlError(f"refusing to overwrite immutable artifact: {path}")

    temp = parent / f".{path.name}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = None
    try:
        descriptor = os.open(temp, flags, 0o600)
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            descriptor = None
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if overwrite:
            os.replace(temp, path)
        else:
            # A pre-write existence check alone is racy.  A same-filesystem hard
            # link gives us an atomic create-if-absent operation on both NTFS and
            # POSIX filesystems; unlinking the temporary name leaves the durable
            # destination inode in place.
            try:
                os.link(temp, path)
            except FileExistsError as exc:
                raise ControlError(f"refusing to overwrite immutable artifact: {path}") from exc
            temp.unlink()
        _fsync_directory(parent)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        try:
            temp.unlink()
        except FileNotFoundError:
            pass


def atomic_write_json(path: Path, value: Any, *, overwrite: bool = True) -> None:
    atomic_write_bytes(path, canonical_json_bytes(value) + b"\n", overwrite=overwrite)


def load_json(path: Path) -> Any:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read valid JSON from {path}: {exc}") from exc


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
