from __future__ import annotations

from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.logs import models


def create_log(db: Session, level: str, message: str, context: str | None = None) -> models.SystemLog:
    entry = models.SystemLog(id=str(uuid4()), level=level, message=message, context=context)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_logs(db: Session, skip: int = 0, limit: int = 200) -> list[models.SystemLog]:
    return db.query(models.SystemLog).order_by(models.SystemLog.created_at.desc()).offset(skip).limit(limit).all()

