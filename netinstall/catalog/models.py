"""Typed models for the NetInstall operating-system catalog."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BootArtifact:
    """A bootable artifact required by an installer."""

    name: str
    url: str
    sha256: str | None = None


@dataclass(frozen=True, slots=True)
class OperatingSystem:
    """An OS entry exposed by the NetInstall catalog."""

    id: str
    name: str
    version: str
    architecture: tuple[str, ...]
    installer: str
    artifacts: tuple[BootArtifact, ...]
    description: str = ""

    def supports(self, architecture: str) -> bool:
        """Return whether this OS supports the requested architecture."""
        return architecture in self.architecture
