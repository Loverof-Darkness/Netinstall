"""Common installer adapter contract.

Adapters generate installer handoff plans; they do not modify disks directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class InstallerContext:
    os_id: str
    architecture: str
    workspace: Path


class InstallerAdapter(Protocol):
    id: str

    def validate(self, context: InstallerContext) -> None: ...

    def prepare(self, context: InstallerContext) -> Path: ...
