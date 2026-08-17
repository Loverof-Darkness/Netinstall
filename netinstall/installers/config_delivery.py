"""Build immutable, per-deployment installer configuration bundles."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import PurePosixPath
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class ConfigBundle:
    """Files and metadata needed by an unattended installer."""

    os_id: str
    files: tuple[tuple[str, str], ...]

    def validate(self) -> None:
        if not self.os_id or "/" in self.os_id or "\\" in self.os_id:
            raise ValueError("invalid OS id")
        for path, content in self.files:
            normalized = PurePosixPath(path)
            if normalized.is_absolute() or ".." in normalized.parts:
                raise ValueError(f"unsafe configuration path: {path}")
            if not isinstance(content, str):
                raise TypeError("configuration content must be text")

    def manifest(self) -> str:
        self.validate()
        return json.dumps(
            {"schema_version": 1, "os_id": self.os_id, "files": [p for p, _ in self.files]},
            indent=2,
            sort_keys=True,
        ) + "\n"


def https_base_url(value: str) -> str:
    """Validate and normalize an HTTPS configuration base URL."""
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("configuration base URL must be HTTPS")
    return value.rstrip("/") + "/"
