"""Resolve boot artifacts from catalog entries without downloading them."""

from __future__ import annotations

from dataclasses import dataclass

from .models import OperatingSystem


@dataclass(frozen=True, slots=True)
class ResolvedArtifacts:
    """Artifacts required to construct an installer boot entry."""

    kernel_url: str
    initrd_urls: tuple[str, ...]
    checksums: tuple[str | None, ...]


def resolve(os: OperatingSystem) -> ResolvedArtifacts:
    """Resolve kernel/initrd artifacts by conventional artifact names."""
    kernel = next((a for a in os.artifacts if a.name == "kernel"), None)
    initrds = tuple(a for a in os.artifacts if a.name.startswith("initrd"))
    if kernel is None:
        raise ValueError(f"No kernel artifact defined for {os.id}")
    if not initrds:
        raise ValueError(f"No initrd artifact defined for {os.id}")
    return ResolvedArtifacts(kernel.url, tuple(a.url for a in initrds), tuple([kernel.sha256, *[a.sha256 for a in initrds]]))
