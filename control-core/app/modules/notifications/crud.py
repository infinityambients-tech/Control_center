from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.modules.notifications import models


def list_notifications(db: Session, user_id: str, skip: int = 0, limit: int = 200) -> list[models.Notification]:
    return (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id)
        .order_by(models.Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_notification(
    db: Session,
    user_id: str,
    title: str,
    message: str | None = None,
    type: str = "info",
    metadata_json: dict[str, Any] | None = None,
) -> models.Notification:
    n = models.Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
        metadata_json=metadata_json,
    )
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


def mark_read(db: Session, notification_id: str, user_id: str) -> models.Notification | None:
    n = (
        db.query(models.Notification)
        .filter(models.Notification.id == notification_id)
        .filter(models.Notification.user_id == user_id)
        .first()
    )
    if not n:
        return None
    n.read_at = datetime.utcnow()
    db.add(n)
    db.commit()
    db.refresh(n)
    return n

