"""Linux installer adapters for network-install workflows."""

from __future__ import annotations

import json
from pathlib import Path

from .base import InstallerContext


class LinuxInstallerError(ValueError):
    """Raised when a Linux installer plan cannot be prepared."""


def _write_plan(context: InstallerContext, installer: str, extra: dict[str, object] | None = None) -> Path:
    context.workspace.mkdir(parents=True, exist_ok=True)
    plan = {
        "os_id": context.os_id,
        "architecture": context.architecture,
        "installer": installer,
        "mode": "network-handoff",
        "disk_write": False,
        "notes": "Installer handoff only. Disk partitioning requires a later explicit deployment step.",
    }
    if extra:
        plan.update(extra)
    output = context.workspace / f"{context.os_id}-installer-plan.json"
    output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return output


def prepare_ubuntu(context: InstallerContext) -> Path:
    """Prepare an Ubuntu autoinstall handoff plan."""
    if context.architecture != "x86_64":
        raise LinuxInstallerError("Ubuntu adapter currently targets x86_64")
    return _write_plan(context, "ubuntu-autoinstall", {"config": "autoinstall/cloud-init"})


def prepare_debian(context: InstallerContext) -> Path:
    """Prepare a Debian Installer network handoff plan."""
    if context.architecture != "x86_64":
        raise LinuxInstallerError("Debian adapter currently targets x86_64")
    return _write_plan(context, "debian-installer", {"config": "preseed-or-auto-mode"})


def prepare_fedora(context: InstallerContext) -> Path:
    """Prepare a Fedora Kickstart network handoff plan."""
    if context.architecture != "x86_64":
        raise LinuxInstallerError("Fedora adapter currently targets x86_64")
    return _write_plan(context, "fedora-kickstart", {"config": "kickstart"})
