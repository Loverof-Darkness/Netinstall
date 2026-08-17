"""Command-line entry point for NetInstall."""

from __future__ import annotations

import argparse

from . import __version__
from .bootstrap.builder import build_staging
from .bootstrap.validate import BootstrapValidationError, validate
from .catalog.service import list_operating_systems
from .deployment.engine import DeploymentError, prepare
from .github.client import GitHubClient, GitHubError
from .hardware.probe import snapshot
from .network.connectivity import check_https
from .network.probe import interfaces
from .network.wifi import WifiError, available_backends, scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="netinstall", description="Universal network-based operating system deployment and recovery toolkit.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    status = subparsers.add_parser("status", help="Show NetInstall capability status."); status.set_defaults(handler=_status)
    diagnose = subparsers.add_parser("diagnose", help="Inspect hardware, firmware, and network capabilities without changing state."); diagnose.set_defaults(handler=_diagnose)
    wifi = subparsers.add_parser("wifi", help="Inspect available Wi-Fi networks.")
    wifi_subparsers = wifi.add_subparsers(dest="wifi_command")
    wifi_scan = wifi_subparsers.add_parser("scan", help="Scan for nearby Wi-Fi networks."); wifi_scan.add_argument("--interface"); wifi_scan.set_defaults(handler=_wifi_scan)
    network = subparsers.add_parser("network", help="Check Internet connectivity"); network.set_defaults(handler=_network_check)
    github = subparsers.add_parser("github", help="Verify access to the NetInstall GitHub repository"); github.set_defaults(handler=_github_check)
    catalog = subparsers.add_parser("os", help="Inspect the supported operating-system catalog"); catalog.set_defaults(handler=_os_list)
    bootstrap = subparsers.add_parser("bootstrap", help="Build or validate a USB bootstrap staging tree")
    bootstrap_sub = bootstrap.add_subparsers(dest="bootstrap_command")
    build = bootstrap_sub.add_parser("build", help="Create a safe staging directory"); build.add_argument("output"); build.set_defaults(handler=_bootstrap_build)
    check = bootstrap_sub.add_parser("validate", help="Validate an existing staging tree"); check.add_argument("path"); check.set_defaults(handler=_bootstrap_validate)
    deploy = subparsers.add_parser("deploy", help="Prepare a non-destructive OS deployment plan")
    deploy.add_argument("os_id", help="Catalog OS identifier")
    deploy.add_argument("--architecture", help="Target architecture (default: host architecture)")
    deploy.set_defaults(handler=_deploy)
    return parser


def _status(_args):
    print("NetInstall bootstrap project"); print(f"Version: {__version__}"); print("Status: development"); return 0


def _diagnose(_args):
    host, nets = snapshot(), interfaces()
    print("NetInstall diagnostics\n======================")
    print(f"System       : {host.system} {host.release}"); print(f"Architecture : {host.machine}"); print(f"Firmware     : {host.firmware}")
    print(f"Vendor       : {host.vendor or 'unknown'}"); print(f"Product      : {host.product or 'unknown'}")
    secure_boot = "enabled" if host.secure_boot else "disabled" if host.secure_boot is False else "unknown"
    print(f"Secure Boot  : {secure_boot}\n\nNetwork interfaces")
    for interface in nets:
        marker = "Wi-Fi" if interface.wireless else "wired/other"
        print(f"  {interface.name:<12} {marker:<12} state={interface.state or 'unknown':<10} mac={interface.mac or 'unknown'}")
    if not nets: print("  none detected")
    return 0


def _wifi_scan(args):
    print("NetInstall Wi-Fi scan\n====================="); print("Backends:", ", ".join(available_backends()) or "none")
    try: networks = scan(args.interface)
    except WifiError as exc: print(f"Error: {exc}"); return 2
    for network in networks:
        signal = f"{network.signal}%" if network.signal is not None else "unknown"
        print(f"  {network.ssid:<32} signal={signal:<8} security={network.security or 'open/unknown'}")
    if not networks: print("No networks found.")
    return 0


def _network_check(_args):
    result = check_https(); print(f"Internet: {'reachable' if result.reachable else 'unavailable'} ({result.hostname})")
    if result.error: print(f"Reason: {result.error}")
    return 0 if result.reachable else 2


def _github_check(_args):
    try: metadata = GitHubClient().repository_metadata()
    except GitHubError as exc: print(f"GitHub: unavailable ({exc})"); return 2
    print(f"GitHub: reachable ({metadata.get('full_name', 'unknown repository')})"); print(f"Default branch: {metadata.get('default_branch', 'unknown')}"); return 0


def _os_list(_args):
    print("NetInstall operating-system catalog\n===================================")
    for os in list_operating_systems(): print(f"  {os.id:<24} {os.name} {os.version} [{', '.join(os.architecture)}]\n    installer: {os.installer}")
    return 0


def _bootstrap_build(args):
    root = build_staging(args.output); print(f"Bootstrap staging created: {root}"); print("No disk was formatted or modified."); return 0


def _bootstrap_validate(args):
    try: data = validate(args.path)
    except BootstrapValidationError as exc: print(f"Bootstrap: invalid ({exc})"); return 2
    print(f"Bootstrap: valid (version {data.get('bootstrap_version', 'unknown')})"); return 0


def _deploy(args):
    try: plan = prepare(args.os_id, args.architecture)
    except DeploymentError as exc: print(f"Deployment: invalid ({exc})"); return 2
    print("NetInstall deployment plan")
    print("==========================")
    print(f"OS          : {plan.operating_system.name} {plan.operating_system.version}")
    print(f"Architecture: {plan.architecture}")
    print(f"Installer   : {plan.installer}")
    print(f"Artifacts   : {len(plan.artifacts)}")
    print("Mode        : planning only; no disk changes")
    return 0


def main() -> int:
    parser = build_parser(); args = parser.parse_args(); handler = getattr(args, "handler", None)
    if handler is None: parser.print_help(); return 0
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
