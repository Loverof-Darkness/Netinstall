"""High-level, non-destructive deployment preparation."""

from __future__ import annotations

import platform

from ..catalog.service import find_operating_system
from .planner import DeploymentPlan, create_plan


class DeploymentError(RuntimeError):
    """Raised when a deployment cannot be prepared."""


def prepare(os_id: str, architecture: str | None = None) -> DeploymentPlan:
    """Resolve an OS and validate a deployment plan; never writes to disks."""
    target_arch = architecture or platform.machine()
    if target_arch == "AMD64":
        target_arch = "x86_64"
    try:
        operating_system = find_operating_system(os_id)
        return create_plan(operating_system, target_arch)
    except (LookupError, ValueError) as exc:
        raise DeploymentError(str(exc)) from exc
