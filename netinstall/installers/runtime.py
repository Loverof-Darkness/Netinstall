"""Safe runtime handoff for OS installer environments."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

from .base import InstallerAdapter


@dataclass(frozen=True, slots=True)
class BootHandoff:
    installer: str
    kernel_url: str
    initrd_urls: tuple[str, ...]
    kernel_args: tuple[str, ...]

    def as_ipxe(self) -> str:
        args = " ".join(self.kernel_args)
        lines = [f"kernel {self.kernel_url} {args}".rstrip()]
        lines.extend(f"initrd {url}" for url in self.initrd_urls)
        lines.append("boot")
        return "\n".join(lines)


def autoinstall_handoff(adapter: InstallerAdapter, kernel_url: str, initrd_url: str, config_url: str) -> BootHandoff:
    """Build an Ubuntu-style autoinstall handoff without executing it."""
    if not config_url.startswith(("https://", "http://")):
        raise ValueError("installer configuration URL must use HTTP(S)")
    config = quote(config_url, safe=":/?=&%._-~")
    return BootHandoff(
        installer=adapter.id,
        kernel_url=kernel_url,
        initrd_urls=(initrd_url,),
        kernel_args=(f"autoinstall ds=nocloud-net;s={config.rstrip('/')}/",),
    )


def debian_handoff(adapter: InstallerAdapter, kernel_url: str, initrd_url: str, preseed_url: str) -> BootHandoff:
    """Build a Debian Installer preseed handoff without executing it."""
    if not preseed_url.startswith(("https://", "http://")):
        raise ValueError("preseed URL must use HTTP(S)")
    return BootHandoff(
        installer=adapter.id,
        kernel_url=kernel_url,
        initrd_urls=(initrd_url,),
        kernel_args=("auto=true", "priority=critical", f"preseed/url={preseed_url}"),
    )


def fedora_handoff(adapter: InstallerAdapter, kernel_url: str, initrd_url: str, kickstart_url: str) -> BootHandoff:
    """Build a Fedora Anaconda Kickstart handoff without executing it."""
    if not kickstart_url.startswith(("https://", "http://")):
        raise ValueError("Kickstart URL must use HTTP(S)")
    return BootHandoff(
        installer=adapter.id,
        kernel_url=kernel_url,
        initrd_urls=(initrd_url,),
        kernel_args=(f"inst.ks={kickstart_url}",),
    )
