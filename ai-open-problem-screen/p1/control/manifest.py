"""Content-addressed artifact manifests with path-containment checks."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from .canonical import is_sha256, sha256_file, sha256_json
from .errors import ValidationError

MANIFEST_SCHEMA = "lr-artifact-manifest/v1"


@dataclass(frozen=True)
class ManifestVerification:
    valid: bool
    errors: tuple[str, ...]
    manifest_sha256: str | None
    artifacts: tuple[dict[str, Any], ...]


def build_manifest(
    *,
    root: Path,
    artifact_specs: Iterable[dict[str, str]],
    producer: dict[str, str],
    scope: str,
    created_utc: str,
) -> dict[str, Any]:
    """Hash the specified files and return a deterministically ordered manifest."""

    root = Path(root).resolve()
    if not root.is_dir():
        raise ValidationError(f"artifact root is not a directory: {root}")
    artifacts: list[dict[str, Any]] = []
    seen: set[str] = set()
    for spec in artifact_specs:
        if not isinstance(spec, dict):
            raise ValidationError("artifact spec must be an object")
        logical_path = _validate_logical_path(spec.get("logical_path"))
        if logical_path in seen:
            raise ValidationError(f"duplicate artifact path: {logical_path}")
        seen.add(logical_path)
        role = _nonempty(spec.get("role"), "artifact role")
        media_type = _nonempty(
            spec.get("media_type", "application/octet-stream"), "artifact media_type"
        )
        physical = _contained_file(root, logical_path)
        artifacts.append(
            {
                "logical_path": logical_path,
                "role": role,
                "media_type": media_type,
                "size_bytes": physical.stat().st_size,
                "sha256": sha256_file(physical),
            }
        )
    artifacts.sort(key=lambda item: (item["logical_path"], item["role"]))
    producer_record = {
        "actor": _nonempty(producer.get("actor"), "producer.actor"),
        "writer_id": _nonempty(producer.get("writer_id"), "producer.writer_id"),
        "tool": _nonempty(producer.get("tool"), "producer.tool"),
        "tool_version": _nonempty(producer.get("tool_version"), "producer.tool_version"),
    }
    identity = {
        "schema_version": MANIFEST_SCHEMA,
        "scope": _nonempty(scope, "scope"),
        "producer": producer_record,
        "artifacts": artifacts,
    }
    return {
        **identity,
        "manifest_id": f"sha256:{sha256_json(identity)}",
        "created_utc": _nonempty(created_utc, "created_utc"),
    }


def verify_manifest(root: Path, manifest: Any) -> ManifestVerification:
    """Verify shape, containment, file sizes, and every content hash."""

    errors: list[str] = []
    artifacts: list[dict[str, Any]] = []
    digest: str | None = None
    if not isinstance(manifest, dict):
        return ManifestVerification(False, ("manifest must be a JSON object",), None, ())
    try:
        digest = sha256_json(manifest)
    except ValidationError as exc:
        errors.append(str(exc))

    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        errors.append(f"unsupported manifest schema: {manifest.get('schema_version')!r}")
    for field in ("scope", "created_utc"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            errors.append(f"manifest.{field} must be a non-empty string")
    producer = manifest.get("producer")
    if not isinstance(producer, dict):
        errors.append("manifest.producer must be an object")
    else:
        for field in ("actor", "writer_id", "tool", "tool_version"):
            if not isinstance(producer.get(field), str) or not producer[field].strip():
                errors.append(f"manifest.producer.{field} must be a non-empty string")

    raw_artifacts = manifest.get("artifacts")
    if not isinstance(raw_artifacts, list) or not raw_artifacts:
        errors.append("manifest.artifacts must be a non-empty list")
        raw_artifacts = []
    seen_paths: set[str] = set()
    for index, item in enumerate(raw_artifacts):
        prefix = f"manifest.artifacts[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        logical = item.get("logical_path")
        try:
            logical = _validate_logical_path(logical)
        except ValidationError as exc:
            errors.append(f"{prefix}: {exc}")
            continue
        if logical in seen_paths:
            errors.append(f"duplicate artifact path: {logical}")
        seen_paths.add(logical)
        for field in ("role", "media_type"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        if not isinstance(item.get("size_bytes"), int) or isinstance(item.get("size_bytes"), bool):
            errors.append(f"{prefix}.size_bytes must be an integer")
        if not is_sha256(item.get("sha256")):
            errors.append(f"{prefix}.sha256 must be a lowercase SHA-256")
        try:
            physical = _contained_file(Path(root).resolve(), logical)
        except ValidationError as exc:
            errors.append(f"{prefix}: {exc}")
            continue
        actual_size = physical.stat().st_size
        if item.get("size_bytes") != actual_size:
            errors.append(
                f"{prefix}: size mismatch for {logical}: "
                f"manifest={item.get('size_bytes')}, actual={actual_size}"
            )
        actual_hash = sha256_file(physical)
        if item.get("sha256") != actual_hash:
            errors.append(f"{prefix}: SHA-256 mismatch for {logical}")
        artifacts.append(item)

    identity = {
        "schema_version": manifest.get("schema_version"),
        "scope": manifest.get("scope"),
        "producer": manifest.get("producer"),
        "artifacts": raw_artifacts,
    }
    expected_id = f"sha256:{sha256_json(identity)}"
    if manifest.get("manifest_id") != expected_id:
        errors.append("manifest_id does not match the canonical manifest identity")
    return ManifestVerification(not errors, tuple(errors), digest, tuple(artifacts))


def artifacts_by_role(artifacts: Iterable[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in artifacts:
        grouped.setdefault(item["role"], []).append(item)
    return grouped


def _validate_logical_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValidationError("logical_path must be a non-empty POSIX path")
    if "\\" in value:
        raise ValidationError("logical_path must use '/' separators")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValidationError(f"unsafe logical_path: {value!r}")
    normalized = path.as_posix()
    if normalized != value:
        raise ValidationError(f"non-canonical logical_path: {value!r}")
    return normalized


def _contained_file(root: Path, logical_path: str) -> Path:
    candidate = root.joinpath(*PurePosixPath(logical_path).parts)
    if candidate.is_symlink():
        raise ValidationError(f"symlink artifacts are forbidden: {logical_path}")
    resolved = candidate.resolve(strict=False)
    try:
        common = Path(os.path.commonpath((str(root), str(resolved))))
    except ValueError as exc:
        raise ValidationError(f"artifact escapes root: {logical_path}") from exc
    if common != root:
        raise ValidationError(f"artifact escapes root: {logical_path}")
    if not candidate.is_file():
        raise ValidationError(f"artifact is missing or not a regular file: {logical_path}")
    return candidate


def _nonempty(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return value
