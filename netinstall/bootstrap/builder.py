"""Build a staging directory for the NetInstall bootstrap volume.

This builder intentionally does not partition, format, or write raw disks.
It creates a deterministic directory tree which can later be copied to a
FAT32 EFI System Partition by an explicit, user-confirmed packaging step.
"""

from __future__ import annotations

import json
from pathlib import Path

from .layout import BootstrapLayout

BOOTSTRAP_VERSION = "0.1.0"


def build_staging(output: str | Path) -> Path:
    """Create a portable bootstrap staging tree and return its root."""
    root = Path(output).expanduser().resolve()
    layout = BootstrapLayout(root)
    layout.create()

    manifest = {
        "schema_version": 1,
        "bootstrap_version": BOOTSTRAP_VERSION,
        "architecture": "x86_64",
        "boot_method": "uefi",
        "repository": "Loverof-Darkness/Netinstall",
        "entrypoint": "netinstall/bootstrap",
        "note": "EFI binaries are supplied by the bootstrap packaging stage; this staging builder does not download or flash them.",
    }
    layout.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return root
