"""Windows WinPE deployment handoff adapter."""

from __future__ import annotations

import json
from pathlib import Path

from .base import InstallerContext


class WindowsInstallerError(ValueError):
    """Raised when the Windows handoff cannot be prepared."""


def prepare_windows(context: InstallerContext) -> Path:
    """Prepare a WinPE-based deployment plan without modifying a disk."""
    if context.architecture != "x86_64":
        raise WindowsInstallerError("Windows adapter currently targets x86_64")
    context.workspace.mkdir(parents=True, exist_ok=True)
    plan = {
        "os_id": context.os_id,
        "architecture": context.architecture,
        "installer": "windows-winpe",
        "mode": "winpe-handoff",
        "disk_write": False,
        "requires": ["WinPE boot environment", "Windows installation source"],
        "notes": "Microsoft installation media is not bundled or redistributed by NetInstall.",
    }
    output = context.workspace / f"{context.os_id}-installer-plan.json"
    output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return output
