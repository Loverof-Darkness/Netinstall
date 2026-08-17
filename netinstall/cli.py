"""Command-line entry point for NetInstall."""

from __future__ import annotations

import argparse

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level NetInstall argument parser."""
    parser = argparse.ArgumentParser(
        prog="netinstall",
        description="Universal network-based operating system deployment and recovery toolkit.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")

    status = subparsers.add_parser("status", help="Show NetInstall capability status.")
    status.set_defaults(handler=_status)

    return parser


def _status(_args: argparse.Namespace) -> int:
    """Print the minimal current status without requiring privileged access."""
    print("NetInstall bootstrap project")
    print(f"Version: {__version__}")
    print("Status: development")
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
