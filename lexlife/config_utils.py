from __future__ import annotations

from pathlib import Path


def parse_scalar(raw: str) -> int | float | str:
    raw = raw.strip()
    if raw.lower() in {"true", "false"}:
        return 1 if raw.lower() == "true" else 0
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    if "." in raw:
        try:
            return float(raw)
        except ValueError:
            return raw
    try:
        return int(raw)
    except ValueError:
        return raw


def load_config(path: Path) -> dict[str, int | float | str]:
    config: dict[str, int | float | str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, value = stripped.split(":", 1)
        config[key.strip()] = parse_scalar(value)
    return config
