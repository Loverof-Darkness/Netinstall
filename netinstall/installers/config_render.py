"""Generate installer configuration documents from safe templates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UbuntuAutoinstallConfig:
    """Minimal Ubuntu cloud-config autoinstall document.

    A password hash is intentionally supplied by the caller; the project never
    stores plaintext credentials in the repository.
    """

    hostname: str
    username: str
    password_hash: str

    def render_user_data(self) -> str:
        if not self.password_hash or not self.password_hash.startswith("$"):
            raise ValueError("password_hash must be a crypt(3)-style hash")
        if not self.hostname or not self.username:
            raise ValueError("hostname and username are required")
        return (
            "#cloud-config\n"
            "autoinstall:\n"
            "  version: 1\n"
            "  identity:\n"
            f"    hostname: {self.hostname}\n"
            f"    username: {self.username}\n"
            f"    password: '{self.password_hash}'\n"
        )


def render_meta_data(instance_id: str = "netinstall") -> str:
    """Render the NoCloud metadata document."""
    if not instance_id or any(ch in instance_id for ch in "\r\n"):
        raise ValueError("invalid instance_id")
    return f"instance-id: {instance_id}\nlocal-hostname: {instance_id}\n"
