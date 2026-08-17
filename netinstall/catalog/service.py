"""High-level catalog service used by the CLI and bootstrap layers."""

from __future__ import annotations

from pathlib import Path

from .loader import load_file
from .models import OperatingSystem

DEFAULT_CATALOG = Path(__file__).resolve().parents[2] / "catalog" / "operating-systems.json"


def list_operating_systems(path: str | Path = DEFAULT_CATALOG) -> tuple[OperatingSystem, ...]:
    """Return all OS definitions from a catalog."""
    return load_file(path)


def find_operating_system(os_id: str, path: str | Path = DEFAULT_CATALOG) -> OperatingSystem:
    """Find one OS definition by its stable catalog id."""
    for operating_system in list_operating_systems(path):
        if operating_system.id == os_id:
            return operating_system
    raise LookupError(f"Operating system not found: {os_id}")
