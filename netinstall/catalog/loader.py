"""Load and validate OS catalog manifests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import BootArtifact, OperatingSystem


class CatalogError(ValueError):
    """Raised when a catalog manifest is invalid."""


def load_file(path: str | Path) -> tuple[OperatingSystem, ...]:
    """Load a JSON catalog from a local file."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CatalogError(f"Unable to load catalog: {exc}") from exc
    return parse(data)


def parse(data: Any) -> tuple[OperatingSystem, ...]:
    """Validate catalog data and convert it to typed OS entries."""
    if not isinstance(data, dict) or not isinstance(data.get("operating_systems"), list):
        raise CatalogError("Catalog must contain an 'operating_systems' list")

    entries: list[OperatingSystem] = []
    seen_ids: set[str] = set()
    for raw in data["operating_systems"]:
        if not isinstance(raw, dict):
            raise CatalogError("Every operating system entry must be an object")
        required = ("id", "name", "version", "architecture", "installer", "artifacts")
        missing = [key for key in required if key not in raw]
        if missing:
            raise CatalogError(f"OS entry is missing: {', '.join(missing)}")

        os_id = raw["id"]
        if not isinstance(os_id, str) or not os_id or os_id in seen_ids:
            raise CatalogError(f"Invalid or duplicate OS id: {os_id!r}")
        seen_ids.add(os_id)

        architectures = raw["architecture"]
        if isinstance(architectures, str):
            architectures = [architectures]
        if not isinstance(architectures, list) or not all(isinstance(x, str) for x in architectures):
            raise CatalogError(f"Invalid architecture list for {os_id}")

        artifacts: list[BootArtifact] = []
        if not isinstance(raw["artifacts"], list):
            raise CatalogError(f"Artifacts for {os_id} must be a list")
        for artifact in raw["artifacts"]:
            if not isinstance(artifact, dict) or not isinstance(artifact.get("name"), str) or not isinstance(artifact.get("url"), str):
                raise CatalogError(f"Invalid artifact in {os_id}")
            artifacts.append(BootArtifact(artifact["name"], artifact["url"], artifact.get("sha256")))

        entries.append(
            OperatingSystem(
                id=os_id,
                name=str(raw["name"]),
                version=str(raw["version"]),
                architecture=tuple(architectures),
                installer=str(raw["installer"]),
                artifacts=tuple(artifacts),
                description=str(raw.get("description", "")),
            )
        )
    return tuple(entries)
