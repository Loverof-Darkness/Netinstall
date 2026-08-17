"""OS-specific installer adapters."""

from .base import InstallerAdapter, InstallerContext
from .registry import get_installer, installer_ids

__all__ = ["InstallerAdapter", "InstallerContext", "get_installer", "installer_ids"]
