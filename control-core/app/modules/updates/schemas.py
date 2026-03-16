from __future__ import annotations

from pydantic import BaseModel


class UpdateCheckResponse(BaseModel):
    update_available: bool
    latest_version: str | None = None
    current_version: str | None = None
    release_name: str | None = None
    release_url: str | None = None
    published_at: str | None = None
    assets: list[dict] = []

