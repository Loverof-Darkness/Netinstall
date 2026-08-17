"""Secure artifact downloading and SHA-256 verification."""

from __future__ import annotations

import hashlib
from pathlib import Path
from urllib.request import Request, urlopen


class DownloadError(RuntimeError):
    """Raised when an artifact cannot be downloaded or verified."""


def download(
    url: str,
    destination: str | Path,
    *,
    sha256: str | None = None,
    timeout: int = 60,
    require_sha256: bool = True,
) -> Path:
    """Download an HTTPS artifact and verify its SHA-256 digest.

    Production callers should keep ``require_sha256=True`` so an unpinned
    remote artifact can never silently enter an installation workflow.
    """
    if not url.lower().startswith("https://"):
        raise DownloadError("Only HTTPS artifact URLs are permitted")
    if require_sha256 and not sha256:
        raise DownloadError("A SHA-256 pin is required before downloading an installation artifact")

    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    try:
        request = Request(url, headers={"User-Agent": "NetInstall/0.1"})
        with urlopen(request, timeout=timeout) as response, target.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
                digest.update(chunk)
    except OSError as exc:
        target.unlink(missing_ok=True)
        raise DownloadError(f"Download failed: {exc}") from exc

    actual = digest.hexdigest()
    if sha256 and actual.lower() != sha256.lower():
        target.unlink(missing_ok=True)
        raise DownloadError(f"SHA-256 mismatch: expected {sha256}, got {actual}")
    return target
