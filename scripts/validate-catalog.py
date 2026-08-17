#!/usr/bin/env python3
"""Validate that catalog entries are internally consistent and bootable."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from netinstall.catalog.loader import CatalogError, load_file  # noqa: E402


catalog = ROOT / "catalog" / "operating-systems.json"
try:
    entries = load_file(catalog)
except CatalogError as exc:
    print(f"catalog validation failed: {exc}", file=sys.stderr)
    raise SystemExit(1)

for entry in entries:
    if not entry.architecture:
        raise SystemExit(f"{entry.id}: no architecture declared")
    if entry.status == "ready" and len(entry.artifacts) < 2:
        raise SystemExit(f"{entry.id}: ready entry needs kernel and initrd artifacts")
    if entry.status != "ready" and not entry.artifacts:
        continue
    names = {artifact.name for artifact in entry.artifacts}
    if entry.status == "ready" and not {"kernel", "initrd"}.issubset(names):
        raise SystemExit(f"{entry.id}: ready entry must define kernel and initrd")
    for artifact in entry.artifacts:
        if not artifact.url.startswith("https://"):
            raise SystemExit(f"{entry.id}/{artifact.name}: artifact URL must use HTTPS")
        if artifact.sha256 is not None and len(artifact.sha256) != 64:
            raise SystemExit(f"{entry.id}/{artifact.name}: SHA-256 must be 64 hex characters")

print(f"catalog OK: {len(entries)} operating systems")
