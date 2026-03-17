from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.modules.auth.deps import get_current_admin
from app.modules.auth.models import User
from app.modules.logs import crud, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.SystemLogResponse])
def admin_list_logs(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=500),
):
    return crud.list_logs(db, skip=skip, limit=limit)

