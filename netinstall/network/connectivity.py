"""Read-only Internet connectivity checks for NetInstall."""

from __future__ import annotations

from dataclasses import dataclass
import socket
import ssl
from urllib import error, parse, request


@dataclass(frozen=True, slots=True)
class ConnectivityResult:
    """Result of an Internet endpoint check."""

    reachable: bool
    hostname: str
    status_code: int | None = None
    error: str | None = None


def check_https(url: str = "https://github.com/", *, timeout: float = 8.0) -> ConnectivityResult:
    """Check that an HTTPS endpoint can be reached without modifying system state."""
    request_obj = request.Request(url, method="HEAD", headers={"User-Agent": "NetInstall/0.1"})
    hostname = parse.urlparse(url).hostname or "unknown"
    try:
        with request.urlopen(request_obj, timeout=timeout, context=ssl.create_default_context()) as response:
            return ConnectivityResult(True, hostname, response.status)
    except (error.HTTPError, error.URLError, TimeoutError, socket.timeout, OSError) as exc:
        status = getattr(exc, "code", None)
        return ConnectivityResult(False, hostname, status, str(exc))
