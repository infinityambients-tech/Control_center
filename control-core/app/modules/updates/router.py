from __future__ import annotations

import re
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.modules.auth.deps import get_current_user
from app.modules.auth.models import User
from app.modules.settings import crud as settings_crud
from app.modules.updates import schemas
from app.modules.updates.service import fetch_latest_release, is_newer, stream_asset_download

router = APIRouter()


@router.get("/check", response_model=schemas.UpdateCheckResponse)
def check_update(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_version: str = Query(default=settings.VERSION),
):
    repo_setting = settings_crud.get_setting(db, "github_repo")
    repo = (repo_setting.value if repo_setting and repo_setting.value else settings.GITHUB_REPO) or ""
    repo = repo.strip()
    if not repo:
        raise HTTPException(status_code=400, detail="Missing GitHub repo. Set DB setting `github_repo` or env `GITHUB_REPO` (owner/repo).")

    token_setting = settings_crud.get_setting(db, "github_token")
    token = (token_setting.value if token_setting and token_setting.value else settings.GITHUB_TOKEN) or None
    try:
        release = fetch_latest_release(repo, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"GitHub release check failed: {e}")

    latest_version = (release.get("tag_name") or "").strip()
    available = bool(latest_version) and is_newer(latest_version, current_version)

    assets = []
    for a in release.get("assets", []) or []:
        assets.append(
            {
                "name": a.get("name"),
                "size": a.get("size"),
                "download_url": a.get("browser_download_url"),
            }
        )

    return schemas.UpdateCheckResponse(
        update_available=available,
        latest_version=latest_version or None,
        current_version=current_version,
        release_name=release.get("name"),
        release_url=release.get("html_url"),
        published_at=release.get("published_at"),
        assets=assets,
    )


@router.get("/download")
def download_asset(
    asset: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Proxies a single GitHub release asset download via backend (supports private repos / tokens).
    Query param `asset` must match an asset name from `/updates/check`.
    """
    if not re.match(r"^[A-Za-z0-9._-]{1,200}$", asset):
        raise HTTPException(status_code=400, detail="Invalid asset name")

    repo_setting = settings_crud.get_setting(db, "github_repo")
    repo = (repo_setting.value if repo_setting and repo_setting.value else settings.GITHUB_REPO) or ""
    repo = repo.strip()
    if not repo:
        raise HTTPException(status_code=400, detail="Missing GitHub repo configuration")

    token_setting = settings_crud.get_setting(db, "github_token")
    token = (token_setting.value if token_setting and token_setting.value else settings.GITHUB_TOKEN) or None

    try:
        release = fetch_latest_release(repo, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"GitHub release fetch failed: {e}")

    asset_url = None
    for a in release.get("assets", []) or []:
        if a.get("name") == asset:
            asset_url = a.get("browser_download_url")
            break

    if not asset_url:
        raise HTTPException(status_code=404, detail="Asset not found in latest release")

    try:
        resp = stream_asset_download(asset_url, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Asset download failed: {e}")

    def iter_bytes():
        for chunk in resp.iter_content(chunk_size=1024 * 256):
            if chunk:
                yield chunk

    headers = {"Content-Disposition": f'attachment; filename="{asset}"'}
    return StreamingResponse(iter_bytes(), media_type="application/octet-stream", headers=headers)
