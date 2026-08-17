"""Plan deployments without making destructive changes."""

from __future__ import annotations

from dataclasses import dataclass

from ..catalog.models import OperatingSystem


@dataclass(frozen=True, slots=True)
class DeploymentPlan:
    """A validated, non-destructive installation plan."""

    operating_system: OperatingSystem
    architecture: str
    installer: str
    artifacts: tuple[str, ...]


def create_plan(operating_system: OperatingSystem, architecture: str) -> DeploymentPlan:
    """Validate architecture compatibility and create a deployment plan."""
    if not operating_system.supports(architecture):
        raise ValueError(
            f"{operating_system.name} {operating_system.version} does not support {architecture}"
        )
    return DeploymentPlan(
        operating_system=operating_system,
        architecture=architecture,
        installer=operating_system.installer,
        artifacts=tuple(artifact.url for artifact in operating_system.artifacts),
    )
