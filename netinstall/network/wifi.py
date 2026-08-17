"""Wi-Fi discovery and connection orchestration.

The core project must work in both a normal Linux installation and a small
bootstrap environment.  Therefore this module deliberately avoids a hard
Python dependency on a particular network manager.  It detects available
system backends and exposes a small, predictable API for the rest of
NetInstall.
"""

from __future__ import annotations

from dataclasses import dataclass
import shutil
import subprocess
from typing import Sequence


@dataclass(frozen=True, slots=True)
class WifiNetwork:
    """A Wi-Fi network discovered during a scan."""

    ssid: str
    signal: int | None = None
    security: str | None = None


class WifiError(RuntimeError):
    """Raised when a Wi-Fi operation cannot be completed."""


_BACKENDS = ("nmcli", "iwctl")


def available_backends() -> tuple[str, ...]:
    """Return supported command-line Wi-Fi backends available on this host."""
    return tuple(command for command in _BACKENDS if shutil.which(command))


def _run(command: Sequence[str], *, timeout: int = 20) -> str:
    """Run a system networking command and return stdout."""
    try:
        result = subprocess.run(
            list(command),
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise WifiError(f"Required command is unavailable: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "command failed").strip()
        raise WifiError(detail) from exc
    except subprocess.TimeoutExpired as exc:
        raise WifiError(f"Command timed out: {command[0]}") from exc
    return result.stdout


def scan(interface: str | None = None) -> list[WifiNetwork]:
    """Scan for nearby Wi-Fi networks using the best available backend."""
    backends = available_backends()
    if "nmcli" in backends:
        command = ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "device", "wifi", "list"]
        if interface:
            command.extend(["ifname", interface])
        output = _run(command)
        return _parse_nmcli_scan(output)

    if "iwctl" in backends:
        if not interface:
            raise WifiError("iwctl requires a Wi-Fi interface for scanning")
        _run(["iwctl", "station", interface, "scan"])
        output = _run(["iwctl", "station", interface, "get-networks"])
        return _parse_iwctl_scan(output)

    raise WifiError("No supported Wi-Fi backend found (need nmcli or iwctl)")


def connect(ssid: str, password: str, *, interface: str | None = None) -> None:
    """Connect to a WPA/WPA2/WPA3 network without exposing the password in logs."""
    if not ssid:
        raise ValueError("SSID must not be empty")

    backends = available_backends()
    if "nmcli" in backends:
        command = ["nmcli", "device", "wifi", "connect", ssid, "password", password]
        if interface:
            command.extend(["ifname", interface])
        _run(command, timeout=45)
        return

    if "iwctl" in backends:
        if not interface:
            raise WifiError("iwctl requires a Wi-Fi interface for connection")
        _run(["iwctl", "station", interface, "connect", ssid], timeout=45)
        return

    raise WifiError("No supported Wi-Fi backend found (need nmcli or iwctl)")


def _parse_nmcli_scan(output: str) -> list[WifiNetwork]:
    networks: dict[str, WifiNetwork] = {}
    for line in output.splitlines():
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue
        ssid, signal, security = (part.strip() for part in parts)
        if not ssid:
            continue
        try:
            signal_value = int(signal) if signal else None
        except ValueError:
            signal_value = None
        networks[ssid] = WifiNetwork(ssid, signal_value, security or None)
    return sorted(networks.values(), key=lambda network: network.signal or -1, reverse=True)


def _parse_iwctl_scan(output: str) -> list[WifiNetwork]:
    networks: list[WifiNetwork] = []
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("SSID") or stripped.startswith("Network"):
            continue
        parts = stripped.split()
        if not parts:
            continue
        ssid = parts[0]
        security = " ".join(parts[1:]) or None
        networks.append(WifiNetwork(ssid=ssid, security=security))
    return networks
