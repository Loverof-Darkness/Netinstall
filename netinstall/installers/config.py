"""Installer configuration models and validation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstallerConfig:
    """Configuration that can be passed to an installer runtime."""

    hostname: str = "netinstall"
    locale: str = "en_US.UTF-8"
    timezone: str = "UTC"
    username: str = "installer"
    wipe_disk: bool = False

    def validate(self) -> None:
        if not self.hostname or len(self.hostname) > 63:
            raise ValueError("hostname must be 1-63 characters")
        if not self.username or len(self.username) > 32:
            raise ValueError("username must be 1-32 characters")
        if self.wipe_disk:
            raise ValueError("destructive disk wiping must be explicitly handled by a future privileged runtime")
