"""Read-only hardware and firmware capability probing.

The probe deliberately avoids privileged operations. It is intended to run
inside a normal OS first and later inside the NetInstall recovery environment.
"""

from __future__ import annotations

import os
import platform
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class HardwareSnapshot:
    """Small, serialisable snapshot of the host hardware environment."""

    system: str
    release: str
    machine: str
    firmware: str | None
    vendor: str | None
    product: str | None
    secure_boot: bool | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _read_text(path: str) -> str | None:
    try:
        value = Path(path).read_text(encoding="utf-8", errors="replace").strip()
    except (OSError, UnicodeError):
        return None
    return value or None


def _secure_boot_state() -> bool | None:
    """Return Secure Boot state when Linux exposes it through efivars."""
    efivarfs = Path("/sys/firmware/efi/efivars")
    if not efivarfs.is_dir():
        return None

    matches = list(efivarfs.glob("SecureBoot-*"))
    if not matches:
        return None

    try:
        data = matches[0].read_bytes()
    except OSError:
        return None

    # UEFI variable data has a 4-byte attributes header followed by the value.
    return bool(len(data) >= 5 and data[4] == 1)


def snapshot() -> HardwareSnapshot:
    """Collect read-only hardware/firmware information."""
    firmware = "UEFI" if Path("/sys/firmware/efi").is_dir() else "Legacy/unknown"
    return HardwareSnapshot(
        system=platform.system(),
        release=platform.release(),
        machine=platform.machine(),
        firmware=firmware,
        vendor=_read_text("/sys/class/dmi/id/sys_vendor"),
        product=_read_text("/sys/class/dmi/id/product_name"),
        secure_boot=_secure_boot_state(),
    )
