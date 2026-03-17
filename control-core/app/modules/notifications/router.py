from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.modules.auth.deps import get_current_user
from app.modules.auth.models import User
from app.modules.notifications import crud, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.NotificationResponse])
def list_my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    return crud.list_notifications(db, user_id=str(current_user.id), skip=skip, limit=limit)


@router.post("/{notification_id}/read", response_model=schemas.NotificationResponse)
def mark_notification_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    n = crud.mark_read(db, notification_id, user_id=str(current_user.id))
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    return n

