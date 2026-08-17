"""Define the portable EFI bootstrap layout."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class BootstrapLayout:
    """Filesystem layout expected on a NetInstall bootstrap volume."""

    root: Path

    @property
    def efi_boot(self) -> Path:
        return self.root / "EFI" / "BOOT"

    @property
    def config(self) -> Path:
        return self.root / "netinstall"

    @property
    def manifest(self) -> Path:
        return self.config / "bootstrap.json"

    def create(self) -> None:
        """Create directories without modifying disks or firmware."""
        self.efi_boot.mkdir(parents=True, exist_ok=True)
        self.config.mkdir(parents=True, exist_ok=True)
