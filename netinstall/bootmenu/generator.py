"""Generate a safe, data-driven iPXE menu from the OS catalog."""

from __future__ import annotations

from .models import BootEntry


def render(entries: tuple[BootEntry, ...], title: str = "NetInstall") -> str:
    """Render a human-readable iPXE menu."""
    lines = ["#!ipxe", "", f"set menu-title {title}", "menu ${menu-title}"]
    for entry in entries:
        lines.append(f"item {entry.id} {entry.title}")
    lines += ["item shell iPXE shell", "choose --default shell --timeout 10000 selected || goto shell", "goto ${selected}", ""]
    for entry in entries:
        lines += [f":{entry.id}", entry.to_ipxe(), "", "goto failed"]
    lines += [":shell", "shell", "", ":failed", "echo Boot entry failed.", "prompt --key 0x02 Press Ctrl-B for the iPXE shell... ||", "exit"]
    return "\n".join(lines) + "\n"
