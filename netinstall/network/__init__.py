"""Network discovery and connectivity primitives."""

from .wifi import WifiError, WifiNetwork, available_backends, connect, scan

__all__ = ["WifiError", "WifiNetwork", "available_backends", "connect", "scan"]
