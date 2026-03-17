from __future__ import annotations

import re
from typing import Any

import requests


def _parse_semver(v: str) -> tuple[int, int, int, str]:
    if not v:
        return (0, 0, 0, "")
    v = v.strip()
    v = v[1:] if v.startswith(("v", "V")) else v
    m = re.match(r"^(\\d+)\\.(\\d+)\\.(\\d+)(.*)$", v)
    if not m:
        return (0, 0, 0, v)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) or "")


def is_newer(latest: str, current: str) -> bool:
    return _parse_semver(latest) > _parse_semver(current)


def fetch_latest_release(repo: str, timeout_s: int = 10, token: str | None = None) -> dict[str, Any]:
    """
    Fetches latest GitHub release metadata.
    `repo` format: "owner/name".
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(
        f"https://api.github.com/repos/{repo}/releases/latest",
        timeout=timeout_s,
        headers=headers,
    )
    resp.raise_for_status()
    return resp.json()


def stream_asset_download(url: str, timeout_s: int = 60, token: str | None = None):
    headers = {"Accept": "application/octet-stream"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(url, stream=True, timeout=timeout_s, headers=headers)
    resp.raise_for_status()
    return resp
