from __future__ import annotations

import platform
from pathlib import Path

from control_center_desktop.api import ApiClient, ApiError
from control_center_desktop.version import __version__


def check_update(api: ApiClient) -> dict:
    return api.get("/api/v1/updates/check", params={"current_version": __version__})


def download_best_asset(update_payload: dict, output_dir: Path) -> Path:
    assets = update_payload.get("assets") or []
    if not assets:
        raise ApiError("No release assets found.")

    sys_name = platform.system().lower()
    preferred_ext = ".exe" if "windows" in sys_name else ".zip"

    best = None
    for a in assets:
        name = (a.get("name") or "").lower()
        if name.endswith(preferred_ext):
            best = a
            break
    best = best or assets[0]

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / (best.get("name") or "update.bin")
    # Use backend proxy to support private repos / tokens.
    api = ApiClient(base_url=update_payload.get("_api_base_url") or "", access_token=update_payload.get("_access_token"))
    if not api.base_url:
        raise ApiError("Missing api_base_url in update payload")
    api.download("/api/v1/updates/download", out, params={"asset": best.get("name")})
    return out
