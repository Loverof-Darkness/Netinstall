"""Read-only network interface discovery.

Linux wireless discovery uses the standard ``iw`` utility when available.
The Linux Wireless documentation identifies ``iw`` as the modern nl80211
interface for inspecting wireless devices and capabilities.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class NetworkInterface:
    """Description of one locally visible network interface."""

    name: str
    kind: str
    state: str | None
    wireless: bool
    mac: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _read(path: Path) -> str | None:
    try:
        value = path.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return None
    return value or None


def _iw_wireless_names() -> set[str]:
    """Return wireless interface names reported by ``iw dev``."""
    iw = shutil.which("iw")
    if not iw:
        return set()
    try:
        result = subprocess.run(
            [iw, "dev"],
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.SubprocessError):
        return set()

    names: set[str] = set()
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("Interface "):
            names.add(stripped.split(maxsplit=1)[1])
    return names


def interfaces() -> list[NetworkInterface]:
    """Discover interfaces without changing network state."""
    root = Path("/sys/class/net")
    if not root.is_dir():
        return []

    wireless_names = _iw_wireless_names()
    found: list[NetworkInterface] = []

    for entry in sorted(root.iterdir(), key=lambda p: p.name):
        name = entry.name
        state = _read(entry / "operstate")
        mac = _read(entry / "address")
        wireless = (entry / "wireless").exists() or name in wireless_names
        kind = "wireless" if wireless else "ethernet/other"
        found.append(
            NetworkInterface(
                name=name,
                kind=kind,
                state=state,
                wireless=wireless,
                mac=mac,
            )
        )

    return found
