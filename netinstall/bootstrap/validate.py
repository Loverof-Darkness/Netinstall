"""Validate a bootstrap staging tree before packaging."""

from __future__ import annotations

import json
from pathlib import Path

from .layout import BootstrapLayout


class BootstrapValidationError(ValueError):
    """Raised when bootstrap staging is incomplete or malformed."""


def validate(root: str | Path) -> dict[str, object]:
    """Validate required directories and the bootstrap manifest."""
    layout = BootstrapLayout(Path(root).expanduser().resolve())
    if not layout.efi_boot.is_dir():
        raise BootstrapValidationError("Missing EFI/BOOT directory")
    if not layout.config.is_dir():
        raise BootstrapValidationError("Missing netinstall directory")
    if not layout.manifest.is_file():
        raise BootstrapValidationError("Missing netinstall/bootstrap.json")
    try:
        data = json.loads(layout.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapValidationError(f"Invalid bootstrap manifest: {exc}") from exc
    if data.get("schema_version") != 1:
        raise BootstrapValidationError("Unsupported bootstrap manifest schema")
    return data
