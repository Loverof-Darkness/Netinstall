"""Installer adapter registry."""

from __future__ import annotations

from collections.abc import Callable

from .base import InstallerContext
from .linux import prepare_debian, prepare_fedora, prepare_ubuntu
from .windows import prepare_windows

_PREPARERS: dict[str, Callable[[InstallerContext], object]] = {
    "ubuntu-autoinstall": prepare_ubuntu,
    "debian-installer": prepare_debian,
    "fedora-kickstart": prepare_fedora,
    "windows-winpe": prepare_windows,
}


def installer_ids() -> tuple[str, ...]:
    return tuple(sorted(_PREPARERS))


def get_installer(installer_id: str) -> Callable[[InstallerContext], object]:
    try:
        return _PREPARERS[installer_id]
    except KeyError as exc:
        raise LookupError(f"Unsupported installer adapter: {installer_id}") from exc
