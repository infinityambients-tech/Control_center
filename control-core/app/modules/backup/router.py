from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.modules.auth.deps import get_current_admin
from app.modules.auth.models import User

router = APIRouter()


@router.post("/database")
def admin_backup_database(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Creates a best-effort backup for SQLite databases by copying the DB file.
    For PostgreSQL, use `pg_dump` (see README).
    """
    if not settings.DATABASE_URL.startswith("sqlite:///"):
        raise HTTPException(status_code=400, detail="Automatic backup is supported only for SQLite in this MVP.")

    db_path = settings.DATABASE_URL.replace("sqlite:///", "", 1)
    src = Path(db_path).resolve()
    if not src.exists():
        raise HTTPException(status_code=404, detail=f"Database file not found: {src}")

    out_dir = Path(__file__).resolve().parents[2] / "static" / "backups"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    dst = out_dir / f"backup_{stamp}.db"
    shutil.copy2(src, dst)
    return {"success": True, "path": str(dst)}

