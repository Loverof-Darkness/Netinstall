"""Command-line entry point for NetInstall."""

from __future__ import annotations

import argparse

from . import __version__
from .github.client import GitHubClient, GitHubError
from .hardware.probe import snapshot
from .network.connectivity import check_https
from .network.probe import interfaces
from .network.wifi import WifiError, available_backends, scan


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level NetInstall argument parser."""
    parser = argparse.ArgumentParser(
        prog="netinstall",
        description="Universal network-based operating system deployment and recovery toolkit.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    status = subparsers.add_parser("status", help="Show NetInstall capability status.")
    status.set_defaults(handler=_status)

    diagnose = subparsers.add_parser(
        "diagnose",
        help="Inspect hardware, firmware, and network capabilities without changing state.",
    )
    diagnose.set_defaults(handler=_diagnose)

    wifi = subparsers.add_parser("wifi", help="Inspect available Wi-Fi networks.")
    wifi_subparsers = wifi.add_subparsers(dest="wifi_command")
    wifi_scan = wifi_subparsers.add_parser("scan", help="Scan for nearby Wi-Fi networks.")
    wifi_scan.add_argument("--interface", help="Wi-Fi interface to scan with.")
    wifi_scan.set_defaults(handler=_wifi_scan)

    network = subparsers.add_parser("network", help="Check Internet connectivity.")
    network.set_defaults(handler=_network_check)

    github = subparsers.add_parser("github", help="Verify access to the NetInstall GitHub repository.")
    github.set_defaults(handler=_github_check)

    return parser


def _status(_args: argparse.Namespace) -> int:
    """Print the minimal current status without requiring privileged access."""
    print("NetInstall bootstrap project")
    print(f"Version: {__version__}")
    print("Status: development")
    return 0


def _diagnose(_args: argparse.Namespace) -> int:
    """Print a human-readable read-only capability report."""
    host = snapshot()
    nets = interfaces()

    print("NetInstall diagnostics")
    print("======================")
    print(f"System       : {host.system} {host.release}")
    print(f"Architecture : {host.machine}")
    print(f"Firmware     : {host.firmware}")
    print(f"Vendor       : {host.vendor or 'unknown'}")
    print(f"Product      : {host.product or 'unknown'}")
    secure_boot = (
        "enabled" if host.secure_boot else "disabled" if host.secure_boot is False else "unknown"
    )
    print(f"Secure Boot  : {secure_boot}")
    print("\nNetwork interfaces")
    if not nets:
        print("  none detected")
        return 0

    for interface in nets:
        state = interface.state or "unknown"
        marker = "Wi-Fi" if interface.wireless else "wired/other"
        mac = interface.mac or "unknown"
        print(f"  {interface.name:<12} {marker:<12} state={state:<10} mac={mac}")
    return 0


def _wifi_scan(args: argparse.Namespace) -> int:
    """Scan for Wi-Fi networks without changing network configuration."""
    print("NetInstall Wi-Fi scan")
    print("=====================")
    print("Backends:", ", ".join(available_backends()) or "none")
    try:
        networks = scan(args.interface)
    except WifiError as exc:
        print(f"Error: {exc}")
        return 2

    if not networks:
        print("No networks found.")
        return 0
    for network in networks:
        signal = f"{network.signal}%" if network.signal is not None else "unknown"
        security = network.security or "open/unknown"
        print(f"  {network.ssid:<32} signal={signal:<8} security={security}")
    return 0


def _network_check(_args: argparse.Namespace) -> int:
    """Check direct HTTPS connectivity to GitHub."""
    result = check_https()
    if result.reachable:
        print(f"Internet: reachable ({result.hostname}, HTTP {result.status_code})")
        return 0
    print(f"Internet: unavailable ({result.hostname})")
    if result.error:
        print(f"Reason: {result.error}")
    return 2


def _github_check(_args: argparse.Namespace) -> int:
    """Check that the public NetInstall repository API is reachable."""
    try:
        metadata = GitHubClient().repository_metadata()
    except GitHubError as exc:
        print(f"GitHub: unavailable ({exc})")
        return 2
    if not isinstance(metadata, dict):
        print("GitHub: invalid repository response")
        return 2
    print(f"GitHub: reachable ({metadata.get('full_name', 'unknown repository')})")
    print(f"Default branch: {metadata.get('default_branch', 'unknown')}")
    return 0


def main() -> int:
    """Run the NetInstall CLI."""
    parser = build_parser()
    args = parser.parse_args()
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
