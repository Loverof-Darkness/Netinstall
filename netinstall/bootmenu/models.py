"""Models for network boot entries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BootEntry:
    """One network-install boot option."""

    id: str
    title: str
    installer: str
    kernel_url: str
    initrd_urls: tuple[str, ...]
    kernel_args: tuple[str, ...] = ()

    def to_ipxe(self) -> str:
        args = " ".join(self.kernel_args)
        lines = [f"kernel {self.kernel_url} {args}".rstrip()]
        lines.extend(f"initrd {url}" for url in self.initrd_urls)
        lines.append("boot")
        return "\n".join(lines)
