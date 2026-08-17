#!/usr/bin/env python3
"""Download catalog artifacts and print a hash-pinned catalog.

This intentionally writes a new JSON file instead of modifying the repository
in place. A maintainer can review the resulting hashes before committing them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path


def sha256_url(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "NetInstall/0.1"})
    digest = hashlib.sha256()
    with urllib.request.urlopen(request, timeout=60) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Pin SHA-256 hashes for NetInstall catalog artifacts")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    for operating_system in data.get("operating_systems", []):
        for artifact in operating_system.get("artifacts", []):
            url = artifact.get("url")
            if not url or not url.startswith("https://"):
                raise SystemExit(f"Refusing non-HTTPS artifact URL: {url!r}")
            print(f"Hashing {operating_system['id']} / {artifact['name']} ...", flush=True)
            artifact["sha256"] = sha256_url(url)
            artifact["verification"] = "sha256-pinned"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
