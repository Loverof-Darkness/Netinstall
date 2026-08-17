"""Small dependency-free GitHub HTTP client used by NetInstall."""

from __future__ import annotations

import json
import ssl
from dataclasses import dataclass
from urllib import error, request


class GitHubError(RuntimeError):
    """Raised when a GitHub resource cannot be fetched or decoded."""


@dataclass(frozen=True, slots=True)
class GitHubClient:
    """Read-only client for public GitHub resources."""

    owner: str = "Loverof-Darkness"
    repository: str = "Netinstall"
    timeout: float = 10.0

    @property
    def api_base(self) -> str:
        return f"https://api.github.com/repos/{self.owner}/{self.repository}"

    def get_json(self, path: str) -> object:
        """Fetch and decode a public GitHub API JSON resource."""
        if not path.startswith("/"):
            path = "/" + path
        req = request.Request(
            self.api_base + path,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "NetInstall/0.1",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with request.urlopen(req, timeout=self.timeout, context=ssl.create_default_context()) as response:
                return json.loads(response.read().decode("utf-8"))
        except (error.HTTPError, error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise GitHubError(f"GitHub request failed: {exc}") from exc

    def repository_metadata(self) -> object:
        """Return metadata for the configured public repository."""
        return self.get_json("")
